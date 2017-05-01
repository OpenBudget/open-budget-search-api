import sys
import time

from open_budget_search_api.logger import logger
from open_budget_search_api.config import INDEX_NAME, get_es_client
from open_budget_search_api.data_sources import sources


def clean():
    es = get_es_client()
    if es.indices.exists(INDEX_NAME):
        logger.info("Removing INDEX %s", INDEX_NAME)
        es.indices.delete(INDEX_NAME)
        es.indices.flush()


def create_index():
    es = get_es_client()
    if not es.indices.exists(INDEX_NAME):
        logger.info("Creating INDEX %s", INDEX_NAME)
        es.indices.create(INDEX_NAME, {
            "settings": {
                "index": {
                    "number_of_shards": 6,
                    "number_of_replicas": 1
                }
            }
        })
        es.indices.flush(INDEX_NAME)


def initialize_db(arg=None):
    if arg == "clean":
        clean()
        create_index()
    elif arg is None:
        print("Usage:")
        print("Option 1: " + sys.argv[0] + " all")
        print("Option 2: " + sys.argv[0] + " <type name>")
    else:
        revision = int(time.time())
        es = get_es_client()
        for type_name, ds in sources.items():
            if arg == 'all' or arg == type_name:
                create_index()
                ds.put_mapping(es)
                ds.load(es, revision)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        initialize_db(sys.argv[1])
    else:
        initialize_db()
