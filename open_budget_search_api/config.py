import os
import elasticsearch

ES_HOST = os.environ.get('ES_HOST', 'localhost')
ES_PORT = os.environ.get('ES_PORT', '9200')

es_connection_string = '{}:{}'\
    .format(ES_HOST, ES_PORT)

INDEX_NAME = 'obudget'
ES_SERVERS_LIST = [ES_HOST]
DEFAULT_TIMEOUT = 60

SEARCHABLE_DATAPACKAGES = [
    "http://next.obudget.org/datapackages/people/aggregated/datapackage.json",
    "http://next.obudget.org/datapackages/budget/national/changes/full/datapackage.json",
    "http://next.obudget.org/datapackages/procurement/tenders/exemptions/processed/datapackage.json",
    "http://next.obudget.org/datapackages/entities/scored/datapackage.json",
    "http://next.obudget.org/datapackages/budget/national/processed/connected-items/datapackage.json",
    "http://next.obudget.org/datapackages/procurement/spending/latest-contract-spending/datapackage.json",
]
NON_SEARCHABLE_DATAPACKAGES = [
    'http://next.obudget.org/datapackages/budgetkey/documents/datapackage.json',
]

_es = None


def get_es_client():
    global _es
    if _es is None:
        _es = elasticsearch.Elasticsearch(ES_SERVERS_LIST, timeout=DEFAULT_TIMEOUT)
    return _es
