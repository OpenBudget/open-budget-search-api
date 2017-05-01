import os
import elasticsearch

ES_HOST = os.environ.get('ES_HOST', 'localhost')
ES_PORT = os.environ.get('ES_PORT', '9200')

es_connection_string = '{}:{}'\
    .format(ES_HOST, ES_PORT)

INDEX_NAME = 'obudget'
ES_SERVERS_LIST = [ES_HOST]
DEFAULT_TIMEOUT = 60

DATAPACKAGES = [
    "http://next.obudget.org/datapackages/entities/all/datapackage.json"
]

_es = None


def get_es_client():
    global _es
    if _es is None:
        _es = elasticsearch.Elasticsearch(ES_SERVERS_LIST, timeout=DEFAULT_TIMEOUT)
    return _es
