import json
import psycopg2

from .logger import logger
from .config import INDEX_NAME, db_connection_string
from .elastic import get_es_client
from .types_data import TYPES_DATA


def clean():
    es = get_es_client()
    if es.indices.exists(INDEX_NAME):
        es.indices.delete(INDEX_NAME)


def create_index():
    es = get_es_client()
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
    es.indices.put_mapping(index=INDEX_NAME, doc_type=type, body=doc_body)


def load_tables(type_data):
    # assuming table name and table type is the same- should change ?
    for type_obj in type_data:
        table = type_obj["type_name"]
        load_data(import_data(table), table)


def load_data(it, input_type):
    es = get_es_client()
    for idx, document in enumerate(it):
        if idx % 100 == 0:
            logger.debug("%s: loaded %d rows", input_type, idx)
        try:
            es.index(INDEX_NAME, input_type, document)
        except Exception as e:
            logger.exception("exception in line: " + str(idx))
            logger.error("Error indexing INDEX_NAME: %s, input_type: %s, document: %s" % (INDEX_NAME, input_type, json.dumps(document)))


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


def initialize_db():
    clean()
    create_index()
    map_tables()
    load_tables(TYPES_DATA)


if __name__ == "__main__":
    initialize_db()
