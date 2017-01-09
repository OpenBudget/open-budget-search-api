import os

DB_DB = os.environ.get('DB_DB')
DB_USER = os.environ.get('DB_USER')
DB_PWD = os.environ.get('DB_PWD')
DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT')

db_connection_string = 'postgresql://{}:{}@{}:{}/{}'\
    .format(DB_USER, DB_PWD, DB_HOST, DB_PORT, DB_DB)

ES_HOST = os.environ.get('ES_HOST', 'localhost')
ES_PORT = os.environ.get('ES_PORT', '9200')

es_connection_string = '{}:{}'\
    .format(ES_HOST, ES_PORT)

INDEX_NAME = 'obudget'
ES_SERVERS_LIST = [ES_HOST]
DEFAULT_TIMEOUT = 60
