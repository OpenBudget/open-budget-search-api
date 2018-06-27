import demjson

import elasticsearch

from .data_sources import sources
from .config import INDEX_NAME, get_es_client
from .logger import logger


# ### QUERY DSL HANDLING
class Query():

    def __init__(self, types):
        self.q = {}
        self.types = types

    def run(self, ):
        return get_es_client()\
                .search(index=INDEX_NAME,
                        doc_type=','.join(self.types),
                        body=self.q)

    def must(self):
        return self.q.setdefault('query', {})\
                     .setdefault('function_score', {})\
                     .setdefault('query', {})\
                     .setdefault('bool', {})\
                     .setdefault('must', [])

    def apply_term(self, term):
        search_fields = [sources()[type_name] for type_name in self.types]
        search_fields = list(set().union(*search_fields))
        self.must().append(dict(
            multi_match=dict(
                query=term,
                fields=search_fields,
                type='most_fields',
                operator='and'
            )
        ))
        return self

    def apply_scoring(self):
        fs = self.q.setdefault('query', {}).setdefault('function_score', {})
        fs.update(dict(
            boost_mode='multiply',
            field_value_factor=dict(
                field='score',
                modifier='sqrt',
                missing=1
            )
        ))
        return self

    def apply_pagination(self, page_size, offset):
        self.q.update({
            'size': int(page_size),
            'from': int(offset)
        })
        return self

    def apply_highlighting(self):
        self.q['highlight'] = dict(
            fields={'*': {}}
        )
        return self

    def apply_filters(self, filters):
        if not filters:
            return self

        must = self.must()

        if isinstance(filters, str):
            if not filters.startswith('{'):
                filters = '{' + filters + '}'
            filters = demjson.decode(filters)

        for k, v in filters.items():
            parts = k.split('__')
            if len(parts) > 1 and parts[-1] in ('gt', 'gte', 'lt', 'lte', 'eq'):
                op = parts[-1]
                must.append(dict(
                    range={
                        k: {
                            op: v
                        }
                    }
                ))
            else:
                must.append(dict(
                    term={
                        k: v
                    }
                ))
        return self

    def apply_time_range(self, from_date, to_date):
        if None not in (from_date, to_date):
            self.must().extend([
                dict(
                    range=dict(
                        __date_range_from=dict(
                            lte=to_date
                        )
                    )
                ),
                dict(
                    range=dict(
                        __date_range_to=dict(
                            gte=from_date
                        )
                    )
                ),
            ])
        return self

    def apply_month_aggregates(self):
        self.q.setdefault('aggs', {}).update(dict(
            timeline=dict(
                terms=dict(
                    field='__date_range_months',
                    size=2500,
                    order=dict(_term='asc')
                )
            )
        ))
        return self


# ### HIGHLIGHT HANDLING
def prepare_replacements(highlighted):
    return [
        (h.replace('<em>', '').replace('</em>', ''), h)
        for h in highlighted
    ]


def do_replacements(value, replacements):
    if value is None:
        return None

    if isinstance(value, str):
        for src, dst in replacements:
            value = value.replace(src, dst)
        value = value.replace('</em> <em>', ' ')
        return value

    if isinstance(value, (int, bool, float)):
        return value

    if isinstance(value, list):
        return [do_replacements(v, replacements) for v in value]

    if isinstance(value, dict):
        return dict((k, do_replacements(v, replacements)) for k, v in value.items())

    assert False, 'Unknown type %r' % value


def merge_highlight_into_source(source, highlights):
    for field, highlighted in highlights.items():
        highlighted = prepare_replacements(highlighted)
        field_parts = field.split('.')
        src = source
        field = field_parts[0]
        while len(field_parts) > 1:
            if isinstance(src[field], dict):
                field_parts.pop(0)
                src = src[field]
                field = field_parts[0]
            else:
                break

        src[field] = do_replacements(src[field], highlighted)
    return source


# ### UTILS
def validate_types(types):
    if 'all' in types:
        types = sources().keys()

    for type_name in types:
        if type_name not in sources():
            raise ValueError('not a real type %s' % type_name)
    return types


# ### Main API
def search(types, term, from_date, to_date, size, offset, filters):
    types = validate_types(types)

    query_results = Query(types)\
        .apply_term(term)\
        .apply_filters(filters)\
        .apply_pagination(size, offset)\
        .apply_scoring()\
        .apply_highlighting()\
        .apply_time_range(from_date, to_date)\
        .run()

    search_results = [
        dict(
            source=merge_highlight_into_source(hit['_source'], hit['highlight']),
            type=hit['_type'],
            score=hit['_score']
        )
        for hit in query_results['hits']['hits']
    ]

    return dict(
        search_results=search_results
    )


def count(term, from_date, to_date, config):
    counts = {}
    for item in config:
        doc_types = item['doc_types']
        doc_types = validate_types(doc_types)
        filters = item['filters']
        id = item['id']
        query_results = Query(doc_types)\
            .apply_term(term)\
            .apply_filters(filters)\
            .apply_pagination(0, 0)\
            .apply_time_range(from_date, to_date)\
            .run()
        counts[id] = dict(
            total_overall=query_results['hits']['total']
        )
    return dict(
        search_counts=counts
    )


def timeline(types, term, from_date, to_date, filters):
    types = validate_types(types)

    query_results = Query(types)\
        .apply_term(term)\
        .apply_filters(filters)\
        .apply_pagination(0, 0)\
        .apply_time_range(from_date, to_date)\
        .apply_month_aggregates()\
        .run()

    timeline = query_results.get('aggregations', {}).get('timeline', {}).get('buckets', [])
    timeline = ((b['key'], b['doc_count'])
                for b in timeline
                if len(b['key']) == 7)
    if None not in (from_date, to_date):
        timeline = filter(lambda k: k[0] >= from_date[:7] and k[0] <= to_date[:7],
                          timeline)
    timeline = sorted(timeline)
    logger.error('%d %r %r', len(timeline), timeline[:10], timeline[-10:])

    return dict(
        timeline=timeline
    )


def get_document(type_name, doc_id):
    es = get_es_client()
    try:
        result = es.get(INDEX_NAME, doc_id, doc_type=type_name)
        return result.get('_source')
    except elasticsearch.exceptions.NotFoundError:
        return None
