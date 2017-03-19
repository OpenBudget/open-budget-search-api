import sys
import json
import psycopg2
import time

from open_budget_search_api.logger import logger
from open_budget_search_api.config import INDEX_NAME, db_connection_string
from open_budget_search_api.elastic import get_es_client
from open_budget_search_api.types_data import TYPES_DATA, KEYS


def clean():
    es = get_es_client()
    if es.indices.exists(INDEX_NAME):
        logger.info("Removing INDEX %s", INDEX_NAME)
        es.indices.delete(INDEX_NAME)
        es.indices.flush()


def create_mapping(_type, doc_body):
    es = get_es_client()
    logger.info("Creating MAPPING %s", _type)
    es.indices.put_mapping(index=INDEX_NAME, doc_type=_type, body=doc_body)


def map_tables():
    for type_obj in TYPES_DATA:
        create_mapping(type_obj["type_name"], type_obj["mapping"])


def create_index():
    es = get_es_client()
    if not es.indices.exists(INDEX_NAME):
        logger.info("Creating INDEX %s", INDEX_NAME)
        es.indices.create(INDEX_NAME, {
            'settings': {
                'index': {
                    'number_of_shards': 6,
                    'number_of_replicas': 1
                },
                "analysis": {
                    "filter": {
                        "nGram_filter": {
                            "type": "nGram",
                            "min_gram": 2,
                            "max_gram": 20,
                            "token_chars": [
                                "letter",
                                "digit",
                                "punctuation",
                                "symbol"
                            ]
                        }
                    },
                    "analyzer": {
                        "nGram_analyzer": {
                            "type": "custom",
                            "tokenizer": "whitespace",
                            "filter": [
                                "lowercase",
                                "asciifolding",
                                "nGram_filter"
                            ]
                        },
                        "whitespace_analyzer": {
                            "type": "custom",
                            "tokenizer": "whitespace",
                            "filter": [
                                "lowercase",
                                "asciifolding"
                            ]
                        }
                    }
                }
            }
        })
        es.indices.flush(INDEX_NAME)
        map_tables()


def load_tables(type_data, table, revision):
    # assuming table name and table type is the same- should change ?
    for type_obj in type_data:
        _table = type_obj["type_name"]
        if _table == table:
            logger.info("Loading TABLE %s", table)
            load_data(import_data(table), table, revision)


def load_data(it, input_type, revision):
    es = get_es_client()
    i = 0
    for idx, document in enumerate(it):
        i = idx
        document['revision'] = revision
        if idx % 10000 == 0:
            logger.info("%s: loaded %d rows", input_type, idx)
        try:
            id = ':'.join(str(document.get(k)) for k in KEYS[input_type])
            es.index(INDEX_NAME, input_type, document, id=id)
        except:
            logger.exception("exception in line: " + str(idx))
            logger.error("Error indexing INDEX_NAME: %s, input_type: %s, document: %r" %
                         (INDEX_NAME, input_type, document))
    logger.info("%s: done loading %d rows", input_type, i)


def import_data(input_type):
    try:
        conn = psycopg2.connect(db_connection_string)
        cursor = conn.cursor()
        cursor.execute('select * from %s' % input_type)
        headers = [i[0] for i in cursor.description]
        for row in cursor:
            yield dict(zip(headers, row))

    except:
        logger.exception("exception while loading data for %s", input_type)


def initialize_db(table=None):
    if table is None:
        create_index()
    elif table == 'clean':
        clean()
        create_index()
    else:
        revision = int(time.time())
        load_tables(TYPES_DATA, table, revision)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        initialize_db(sys.argv[1])
    else:
        initialize_db()
