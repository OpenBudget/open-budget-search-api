import elasticsearch

from .data_sources import sources
from .config import INDEX_NAME, get_es_client


def prepare_typed_query(type_names, term, from_date, to_date, search_size, offset):
    search_fields = [sources[type_name].search_fields for type_name in type_names]
    search_fields = list(set().union(*search_fields))
    body = {
        "query": {
            "function_score": {
                "query": {
                    "multi_match": {
                        "query": term,
                        "fields": search_fields,
                        "type": "best_fields",
                        "operator": "and"
                    }
                },
                "boost_mode": "multiply",
                "script_score": {
                    "script": {
                        "inline": "Math.log(doc['score'].value+1)"
                    }
                }
            }
        },
        "aggs": {
            "type_totals": {
                "terms": {"field": "_type"}
            }
        },
        "size": int(search_size),
        "from": int(offset),
        "highlight": {
            "fields": {
                "*": {}
            }
        }
    }

    # if False:#ds.is_temporal:
    #     body["aggs"]["stats_per_month"] = {
    #         "date_histogram": {
    #             "field": ds.date_fields['from'],
    #             "interval": "month",
    #             "min_doc_count": 1
    #         }
    #     }
    #     range_obj = ds.range_structure
    #     range_obj[ds.date_fields['from']]["gte"] = from_date
    #     range_obj[ds.date_fields['to']]["lte"] = to_date
    #     bool_filter = body["aggs"]["filtered"]["filter"]["bool"]
    #     bool_filter["must"] = [{
    #         "range": range_obj
    #     }]
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
            return {"message": "not a real type %s" % type_name}
    query = prepare_typed_query(types, term, from_date, to_date, size, offset)
    results = get_es_client().search(index=INDEX_NAME, doc_type=",".join(types), body=query)
    overalls = results['aggregations']['type_totals']['buckets']
    overalls = dict(
        (i['key'], i['doc_count'])
        for i in overalls
    )

    for type_name in types:
        ret_val['search_counts'][type_name.replace('-', '')] = {
            'total_overall': overalls.get(type_name, 0),
        }
    for hit in results['hits']['hits']:
        ret_val['search_results'].append({
            'source': merge_highlight_into_source(hit['_source'], hit['highlight']),
            'highlight': {},
            'type': hit['_type'].replace('-', ''),
            'score': hit['_score'],
        })

    return ret_val


def autocomplete(term):
    es = get_es_client()
    query_body = {
        "size": 10,
        "query": {
            "match": {
                "_all": {
                    "query": term,
                    "operator": "and"
                }
            }
        }
    }
    elastic_result = es.search(body=query_body)
    return elastic_result
