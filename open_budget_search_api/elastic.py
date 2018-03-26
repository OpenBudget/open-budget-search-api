import elasticsearch
from copy import deepcopy

from .data_sources import sources
from .config import INDEX_NAME, get_es_client


def prepare_base_query(type_names, term):
    search_fields = [sources[type_name].search_fields for type_name in type_names]
    search_fields = list(set().union(*search_fields))
    body = {
        'query': {
            'function_score': {
                'query': {
                    'bool': {
                        'must': [
                            {
                                'multi_match': {
                                    'query': term,
                                    'fields': search_fields,
                                    'type': 'best_fields',
                                    'operator': 'and'
                                }
                            }
                        ]
                    }
                },
                'boost_mode': 'multiply',
                'field_value_factor': {
                        'field': 'score',
                        'modifier': 'sqrt',
                        'missing': 1
                }
            }
        },
        'aggs': {
            'type_totals': {
                'terms': {'field': '_type'}
            }
        }
    }
    for ds in sources.values():
        if ds.date_fields.get('from') and ds.date_fields.get('to'):
            body['aggs']['months_{}'.format(ds.type_name)] = {'date_histogram': {'field': ds.date_fields['from'],
                                                                                 'interval': 'month',
                                                                                 'min_doc_count': 1,
                                                                                 'format': 'yyyy-MM'}}
        elif ds.date_fields.get('year'):
            body['aggs']['years_{}'.format(ds.type_name)] = {'histogram': {'field': ds.date_fields['year'], 'interval': 1}}
    return body


def prepare_totals_query(body):
    body = deepcopy(body)
    body.update({
        'size': 0
    })
    import json; print(json.dumps(body, indent=2))
    return body


def prepare_search_query(body, from_date, to_date, search_size, offset):
    body = deepcopy(body)
    body.update({
        'size': int(search_size),
        'from': int(offset),
        'highlight': {
            'fields': {
                '*': {}
            }
        }
    })
    date_fields_query = {
        'bool': {
            'should': []
        }
    }
    # TODO: extract year as integer from from_data and to_date
    from_year, to_year = 2005, 2007
    body['query']['function_score']['query']['bool']['must'].append(date_fields_query)
    for ds in sources.values():
        if ds.date_fields.get('from') and ds.date_fields.get('to'):
            date_fields_query['bool']['should'].append({
                'bool': {
                    'must': [
                        {'type': {'value': ds.type_name}},
                        {'range': {ds.date_fields['from']: {'gte': from_date},
                                   ds.date_fields['to']: {'lte': to_date}}}
                    ]
                }
            })
        elif ds.date_fields.get('year'):
            date_fields_query['bool']['should'].append({
                'bool': {
                    'must': [
                        {'type': {'value': ds.type_name}},
                        {'range': {ds.date_fields['year']: {'gte': from_year, 'lte': to_year}}}
                    ]
                }
            })
    import json; print(json.dumps(body, indent=2))
    return body


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


def get_document(type_name, doc_id):
    es = get_es_client()
    try:
        result = es.get(INDEX_NAME, doc_id, doc_type=type_name)
        return result.get('_source')
    except elasticsearch.exceptions.NotFoundError:
        return None


def search(types, term, from_date, to_date, size, offset):
    ret_val = {
        'search_counts': {},
        'search_results': [],
    }
    if 'all' in types:
        types = sources.keys()

    for type_name in types:
        if type_name not in sources:
            return {'message': 'not a real type %s' % type_name}

    base_query = prepare_base_query(types, term)

    search_query = prepare_search_query(base_query, from_date, to_date, size, offset)
    search_results = get_es_client().search(index=INDEX_NAME, doc_type=','.join(types), body=search_query)

    overalls = search_results['aggregations']['type_totals']['buckets']
    overalls = dict(
        (i['key'], i['doc_count'])
        for i in overalls
    )

    for type_name in types:
        ret_val['search_counts'][type_name.replace('-', '')] = {
            'total_overall': overalls.get(type_name, 0),
        }

    for hit in search_results['hits']['hits']:
        ret_val['search_results'].append({
            'source': merge_highlight_into_source(hit['_source'], hit['highlight']),
            'highlight': {},
            'type': hit['_type'].replace('-', ''),
            'score': hit['_score'],
        })

    totals_query = prepare_totals_query(base_query)
    total_results = get_es_client().search(index=INDEX_NAME, doc_type=','.join(types), body=totals_query)

    for agg_name, agg_data in total_results['aggregations'].items():
        range_name = None
        if agg_name.startswith('years_'):
            range_name = 'year'
        elif agg_name.startswith('months_'):
            range_name = 'month'
        if range_name:
            for bucket in agg_data['buckets']:
                bucket_key = bucket['key_as_string'] if range_name == 'month' else int(bucket['key'])
                search_count_key = agg_name.replace('{}s_'.format(range_name), '').replace('-', '')
                if bucket_key and search_count_key in ret_val['search_counts']:
                    ds_search_counts = ret_val['search_counts'][search_count_key]
                    ds_range_counts = ds_search_counts.setdefault('{}_counts'.format(range_name), {})
                    ds_range_counts.setdefault(bucket_key, 0)
                    ds_range_counts[bucket_key] += bucket['doc_count']

    return ret_val


def autocomplete(term):
    es = get_es_client()
    query_body = {
        'size': 10,
        'query': {
            'match': {
                '_all': {
                    'query': term,
                    'operator': 'and'
                }
            }
        }
    }
    elastic_result = es.search(body=query_body)
    return elastic_result
