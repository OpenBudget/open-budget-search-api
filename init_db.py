from elastic import get_es_client, logger, INDEX_NAME
from types_data import TYPES_DATA
import json
import os
import csv


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


def load_tables(tables_path, type_data):
    #assuming table name and table type is the same- should change ?
    for type_obj in type_data:
        table = type_obj["type_name"]
        load_data(os.path.join(tables_path, table + ".csv"), table)


def load_data(input_path, input_type):
    es = get_es_client()
    if (os.path.isfile(input_path)):
        with open(input_path, 'r', encoding="utf-8") as input_file:
            csv_reader = csv.reader(input_file)
            # Parse headers.
            fields_list = []
            headers = next(csv_reader)
            for header in headers:
                fields_list.append(header.lower())
            for idx, row in enumerate(csv_reader):
                document = {}
                for cell, field_name in zip(row, fields_list):
                    cell = cell.strip()
                    if cell:
                        document[field_name] = cell
                if idx % 100 == 0:
                    print(idx)
                try:
                    es.index(INDEX_NAME, input_type, document)
                except Exception as e:
                    print("exception in line: " + str(idx))
                    logger.exception("Error indexing INDEX_NAME: %s, input_type: %s, document: %s" % (INDEX_NAME, input_type, json.dumps(document)))


def map_tables():
    for type_obj in TYPES_DATA:
        create_mapping(type_obj["type_name"], type_obj["mapping"])


def initialize_db():
    clean()
    create_index()
    map_tables()
    load_tables('data', TYPES_DATA)


if __name__ == "__main__":
    initialize_db()
