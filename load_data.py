import csv
import itertools
import collections
import sys
import time
import json

from open_budget_search_api.logger import logger
from open_budget_search_api.config import INDEX_NAME, get_es_client
from open_budget_search_api.data_sources import all_sources

csv.field_size_limit(500*1024)


def clean(index_name=INDEX_NAME):
    es = get_es_client()
    if es.indices.exists(index_name):
        logger.info("Removing INDEX %s", index_name)
        es.indices.delete(index_name)
        es.indices.flush()


def create_index(index_name=INDEX_NAME):
    es = get_es_client()
    if not es.indices.exists(index_name):
        logger.info("Creating INDEX %s", index_name)
        es.indices.create(index_name, {
            "settings": {
                "index": {
                    "number_of_shards": 6,
                    "number_of_replicas": 1
                },
                "analysis.analyzer": {
                    "default": {
                        "type": "hebrew"
                    },
                },
            },
            # "mappings": {
            #     "_default_": {
            #         "dynamic_templates": [{
            #             "strings": {
            #                 "match": "*",
            #                 "match_mapping_type": "text",
            #                 "mapping": {
            #                     "analyzer": "analysis-hebrew",
            #                 }
            #             }
            #         }]
            #     }
            # }
        })
        es.indices.flush(index_name)


def initialize_db(arg=None, index_name=INDEX_NAME):
    if arg == "clean":
        logger.info('CLEANING UP')
        clean(index_name=index_name)
        create_index(index_name=index_name)
    elif arg is None:
        print("Usage:")
        print("Option 1: " + sys.argv[0] + " all")
        print("Option 2: " + sys.argv[0] + " <type name>")
    else:
        logger.info('LOADING DATA')
        revision = int(time.time())
        es = get_es_client()
        to_load = []
        for type_name, ds in all_sources.items():
            if arg == 'all' or arg == type_name:
                logger.info('LOADING DATA for %s', type_name)
                logger.info('SEARCH FIELDS for %s: %r', type_name, ds.search_fields)
                logger.info('MAPPING for %s:\n%s', type_name, json.dumps(ds.mapping, indent=2))
                create_index(index_name=index_name)
                ds.put_mapping(es, index=index_name)
                to_load.append(ds)
        it = itertools.zip_longest(*(ds.load(es, revision, index_name=index_name) for ds in to_load))
        collections.deque(it, maxlen=0)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        initialize_db(sys.argv[1])
    else:
        initialize_db()
