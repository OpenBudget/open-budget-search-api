import os
import elasticsearch

ES_HOST = os.environ.get('ES_HOST', 'localhost')
ES_PORT = os.environ.get('ES_PORT', '9200')
INDEX_NAME = os.environ.get('INDEX_NAME', 'budgetkey')
ES_SERVERS_LIST = [{"host": ES_HOST, "port": int(ES_PORT)}]
DEFAULT_TIMEOUT = 60

DATAPACKAGE_BASE = 'http://next.obudget.org/datapackages/budgetkey/{}/datapackage.json'

# browsable list of the datapackages is available here - http://next.obudget.org/datapackages/budgetkey/
# each package has dpp:streamedFrom property which allows to identify the source pipeline in budgetkey-data-pipelines
SEARCHABLE_DATAPACKAGES = [
    DATAPACKAGE_BASE.format(doc_type)
    for doc_type in [
        'people',
        'tenders',
        'entities',
        'contract-spending',
        'national-budget-changes',
        'supports',
        'reports',
        'budget',
        'gov_decisions',
    ]
]


_es = None


def get_es_client():
    global _es
    if _es is None:
        _es = elasticsearch.Elasticsearch(ES_SERVERS_LIST, timeout=DEFAULT_TIMEOUT)
    return _es
