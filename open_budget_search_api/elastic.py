import json
import re
import elasticsearch

from .data_sources import sources
from .config import INDEX_NAME, get_es_client
from .logger import logger


def prepare_typed_query(type_name, term, from_date, to_date, search_size, offset):
    ds = sources[type_name]
    body = {
        "query": {
            "function_score": {
                "query": {
                    "multi_match": {
                        "query": term,
                        "fields": ds.search_fields,
                        "type": "most_fields",
                        "operator": "and"
                    }
                },
                "script_score": {
                    "script": {
                        "lang": "painless",
                        "inline": "_score * doc['%s'].value" % ds.scoring_column
                    }
                }
            }
        },
        "aggs": {
            "filtered": {
                "filter": {
                    "bool": {
                        "must": [
                            {
                                "type": {
                                    "value": type_name
                                }
                            }
                        ]
                    }
                },
                "aggs": {
                    "top_results": {
                        "top_hits": {
                            "size": int(search_size),
                            "from": int(offset),
                            "highlight": {
                                "fields": {
                                    "*": {}
                                }
                            }
                        }
                    }
                }
            }
        },
        "size": 0
    }

    must = body["aggs"]["filtered"]["filter"]["bool"]["must"]
    if ds.is_temporal:
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
        must.append({
            "range": range_obj
        })
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


def get_document(type_name, doc_id):
    es = get_es_client()
    try:
        result = es.get(INDEX_NAME, doc_id, doc_type=type_name)
        return result.get('_source')
    except elasticsearch.exceptions.NotFoundError:
        return None


def multi_query(query_list):
    es = get_es_client()
    query_list = '\n'.join(json.dumps(l) for l in query_list)
    logger.info('Running QUERY:\n%s', query_list)
    return es.msearch(query_list)


def search(types, term, from_date, to_date, size, offset):

    ret_val = {}
    if 'all' in types:
        types = sources.keys()

    heads = []
    query_list = []
    for type_name in types:
        if type_name not in sources:
            return {"message": "not a real type %s" % type_name}
        head = {'index': INDEX_NAME, 'type': type_name}
        heads.append(head)
        query = prepare_typed_query(type_name, term, from_date, to_date, size, offset)
        query_list.extend([head, query])

    results = multi_query(query_list)
    elastic_result = dict(
        (h['type'], {
            'ds': sources.get(h['type']),
            'es': r
        })
        for h, r in zip(heads, results['responses'])
    )
    for type_name in types:
        ret_val[type_name] = {}
        if elastic_result[type_name]['ds'].is_temporal:
            ret_val[type_name]["total_in_result"] = \
                len(elastic_result[type_name]['es']["aggregations"]["filtered"]["top_results"]["hits"]["hits"])
            ret_val[type_name]["data_time_distribution"] = \
                elastic_result[type_name]['es']["aggregations"]["stats_per_month"]["buckets"]

        ret_val[type_name]["total_overall"] = elastic_result[type_name]['es']["hits"]["total"]
        ret_val[type_name]["docs"] = []

        for doc in elastic_result[type_name]['es']["aggregations"]["filtered"]["top_results"]["hits"]["hits"]:
            rec = {'source': doc["_source"],
                   'highlight': parse_highlights(doc["highlight"])}
            ret_val[type_name]["docs"].append(rec)

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
