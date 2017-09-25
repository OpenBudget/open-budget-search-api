import json
import re
import elasticsearch

from .data_sources import sources
from .config import INDEX_NAME, get_es_client
from .logger import logger


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
                        "type": "most_fields",
                        "operator": "and"
                    }
                },
                "script_score": {
                    "script": {
                        "lang": "painless",
                        "inline": "_score * doc['score'].value"
                    }
                }
            }
        },
        "aggs": {
            "type_totals" : {
                "terms" : { "field" : "_type" }
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

    if False:#ds.is_temporal:
        body["aggs"]["stats_per_month"] = {
            "date_histogram": {
                "field": ds.date_fields['from'],
                "interval": "month",
                "min_doc_count": 1
            }
        }
        range_obj = ds.range_structure
        range_obj[ds.date_fields['from']]["gte"] = from_date
        range_obj[ds.date_fields['to']]["lte"] = to_date
        bool_filter = body["aggs"]["filtered"]["filter"]["bool"]
        bool_filter["must"] = [{
            "range": range_obj
        }]
    return body


def parse_highlights(highlights):
    start_tag = '<em>'
    end_tag = '</em>'
    parsed_highlights = {}
    for field in highlights:
        parsed_highlights[field] = []
        for term in highlights[field]:
            start_tag_results = re.finditer(start_tag, term)
            end_tag_results = re.finditer(end_tag, term)
            for start, end in zip(start_tag_results, end_tag_results):
                    result_index = start.end() - len(start_tag)
                    result_len = end.start() - start.end()
                    parsed_highlights[field].append([result_index, result_len])

    return parsed_highlights


def merge_highlight_into_source(source, highlights):
    for field in highlights:
        if '.' in field:
            field_parts = field.split('.')
            if field_parts[0] in source:
                if len(source[field_parts[0]]) == 1:
                    if field_parts[1] in source[field_parts[0]][0]:
                        source[field_parts[0]][0][field_parts[1]] = highlights[field][0]
                else:
                    for h in highlights[field]:
                        h_raw = h.replace('em', '').replace('<', '').replace('>', '').replace('/', '')
                        for i, s in enumerate(source[field_parts[0]]):
                            if h_raw in s[field_parts[1]]:
                                source[field_parts[0]][i][field_parts[1]] = h
                                break

        elif field in source:
            source[field] = highlights[field][0]
        else:
            pass
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
            'highlight': parse_highlights(hit['highlight']),
            'type': hit['_type'].replace('-', ''),
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
