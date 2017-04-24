import time

from open_budget_search_api.logger import logger
from open_budget_search_api.config import INDEX_NAME
from open_budget_search_api.elastic import get_es_client
import sys
import datapackage


def clean():
    es = get_es_client()
    if es.indices.exists(INDEX_NAME):
        logger.info("Removing INDEX %s", INDEX_NAME)
        es.indices.delete(INDEX_NAME)
        es.indices.flush()


def create_mapping(type_name, resource):
    fields = resource.descriptor["schema"]["fields"]
    mapping_data = {
        # Setting the default analyzer to hebrew
        "dynamic_templates": [
            {
                "template1": {
                    "match": "*",
                    "match_mapping_type": "string",
                    "mapping": {
                        "type": "string",
                        "analyzer": "hebrew",
                        "fields": {
                            "raw": {
                                "type": "string",
                                "index": "not_analyzed"
                            }
                        }
                    }
                }
            }
        ],
        "properties": {}
    }
    for field in fields:
        field_name = field["name"]
        mapping_data["properties"][field_name] = {}
        mapping_data["properties"][field_name]["type"] = json_type_to_elastic_type(field["type"])
    print(mapping_data)
    es = get_es_client()
    logger.info("Creating MAPPING %s", type_name)
    es.indices.put_mapping(index=INDEX_NAME, doc_type=type_name, body=mapping_data)


def load_data(type_name, resource, revision):
    logger.info("Loading TABLE %s", type_name)
    es = get_es_client()
    it = resource.iter()
    try:
        keys = resource.descriptor["schema"]["primaryKey"]
    except:
        logger.exception("Exception loading %s table" % type_name)
        logger.error("Error loading %s table. No primaryKey defined in schema. Skipping" % type_name)
        return

    i = 0
    for idx, document in enumerate(it):
        i = idx
        document["revision"] = revision
        if idx % 10000 == 0:
            logger.info("%s: loaded %d rows", type_name, idx)
        try:
            doc_id = ":".join(str(document.get(k)) for k in keys)
            es.index(INDEX_NAME, type_name, document, id=doc_id)
        except:
            logger.exception("exception in line: " + str(idx))
            logger.error("Error indexing INDEX_NAME: %s, input_type: %s, document: %r" %
                         (INDEX_NAME, type_name, document))
    logger.info("%s: done loading %d rows", type_name, i)


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


def json_type_to_elastic_type(json_type):
    switcher = {
        "integer": "long",
        "number": "double",
        "string": "string",
        "array": "string",
        "object": "object"
    }
    return switcher.get(json_type, "string")


def upload_datapackage_data(dp_url, revision):
    dp = datapackage.DataPackage(dp_url)
    for resource in dp.resources:
        type_name = resource.descriptor["name"]
        create_mapping(type_name, resource)
        load_data(type_name, resource, revision)


def initialize_db(table=None):
    if table == "clean":
        clean()
        create_index()
    elif table is None:
        print("Usage:")
        print("Option 1: " + sys.argv[0] + " all")
        print("Option 2: " + sys.argv[0] + " <datapackage_url path>")
    elif table == "all":
        create_index()
        revision = int(time.time())
        upload_datapackage_data("http://next.obudget.org/datapackages/entities/all/datapackage.json", revision)
    else:
        upload_datapackage_data(table)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        initialize_db(sys.argv[1])
    else:
        initialize_db()
