import sys
import json
import psycopg2

from open_budget_search_api.logger import logger
from open_budget_search_api.config import INDEX_NAME, db_connection_string
from open_budget_search_api.elastic import get_es_client
from open_budget_search_api.types_data import TYPES_DATA


def clean():
    es = get_es_client()
    if es.indices.exists(INDEX_NAME):
        logger.info("Removing INDEX %s", INDEX_NAME)
        es.indices.delete(INDEX_NAME)
        es.indices.flush()


def create_index():
    es = get_es_client()
    logger.info("Creating INDEX %s", INDEX_NAME)
    es.indices.create(INDEX_NAME, {
        'settings': {
            'index': {
                'number_of_shards': 6,
                'number_of_replicas': 1
            }
        }
    })


def create_mapping(type, doc_body):
    es = get_es_client()
    logger.info("Creating MAPPING %s", type)
    es.indices.put_mapping(index=INDEX_NAME, doc_type=type, body=doc_body)


def load_tables(type_data, table):
    # assuming table name and table type is the same- should change ?
    for type_obj in type_data:
        _table = type_obj["type_name"]
        if _table == table:
            logger.info("Loading TABLE %s", table)
            load_data(import_data(table), table)


def load_data(it, input_type):
    es = get_es_client()
    for idx, document in enumerate(it):
        if idx % 10000 == 0:
            logger.info("%s: loaded %d rows", input_type, idx)
        try:
            es.index(INDEX_NAME, input_type, document)
        except:
            logger.exception("exception in line: " + str(idx))
            logger.error("Error indexing INDEX_NAME: %s, input_type: %s, document: %r" % (INDEX_NAME, input_type, document))


def map_tables():
    for type_obj in TYPES_DATA:
        create_mapping(type_obj["type_name"], type_obj["mapping"])


def import_data(input_type):
    conn = psycopg2.connect(db_connection_string)
    cursor = conn.cursor()
    cursor.execute('select * from %s' % input_type)
    headers = [i[0] for i in cursor.description]
    for row in cursor.fetchall():
        yield dict(zip(headers, row))


def initialize_db(table=None):
    if table is None:
        clean()
        create_index()
        map_tables()
    else:
        load_tables(TYPES_DATA, table)


if __name__ == "__main__":
    if len(sys.argv)>1:
        initialize_db(sys.argv[1])
    else:
        initialize_db()
