import json
import re

from .data_sources import sources
from .config import INDEX_NAME, get_es_client
from .logger import logger


def prepare_typed_query(type_name, term, from_date, to_date, search_size, offset):
    ds = sources[type_name]
    body = {
                "query": {
                    "multi_match": {
                        "query": term,
                        "fields": ds.search_fields
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
                                    },
                                    "sort": ds.sort_method
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


def search(types, term, from_date, to_date, size, offset):
    es = get_es_client()
    elastic_result = {}
    ret_val = {}
    for type_name in types:
        if type_name not in sources:
            return {"message": "not a real type %s" % type_name}
        ds = sources[type_name]
        query_body = prepare_typed_query(type_name, term, from_date, to_date, size, offset)
        logger.info('Running QUERY:\n%s', json.dumps(query_body, indent=2, sort_keys=True))
        elastic_result[type_name] = es.search(index=INDEX_NAME,
                                              body=query_body)
        ret_val[type_name] = {}

        if ds.is_temporal:
            ret_val[type]["total_in_result"] = \
                len(elastic_result[type_name]["aggregations"]["filtered"]["top_results"]["hits"]["hits"])
            ret_val[type]["data_time_distribution"] = \
                elastic_result[type_name]["aggregations"]["stats_per_month"]["buckets"]

        ret_val[type_name]["total_overall"] = elastic_result[type_name]["hits"]["total"]
        ret_val[type_name]["docs"] = []

        for doc in elastic_result[type_name]["aggregations"]["filtered"]["top_results"]["hits"]["hits"]:
            rec = {'source': doc["_source"],
                   'highlight': parse_highlights(doc["highlight"])}
            ret_val[type]["docs"].append(rec)

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
