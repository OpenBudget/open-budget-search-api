import os
import elasticsearch

ES_HOST = os.environ.get('ES_HOST', 'localhost')
ES_PORT = os.environ.get('ES_PORT', '9200')
INDEX_NAME = os.environ.get('INDEX_NAME', 'budgetkey')
ES_SERVERS_LIST = [{"host": ES_HOST, "port": int(ES_PORT)}]
DEFAULT_TIMEOUT = 60

DATAPACKAGE_BASE = 'http://next.obudget.org/datapackages/budgetkey/{}/datapackage.json'

SEARCHABLE_DATAPACKAGES = [
    DATAPACKAGE_BASE.format(doc_type)
    for doc_type in [
        # http://next.obudget.org/datapackages/people/aggregated/datapackage.json (people)
        'people',
        # http://next.obudget.org/datapackages/procurement/tenders/processed/datapackage.json (tenders)
        'tenders',
        # http://next.obudget.org/datapackages/entities/scored/datapackage.json (entities)
        'entities',
        # http://next.obudget.org/datapackages/procurement/spending/latest-contract-spending/datapackage.json (contract-spending)
        'contract-spending',
        # http://next.obudget.org/datapackages/budget/national/changes/full/datapackage.json (national-budget-changes)
        'national-budget-changes',
        # http://next.obudget.org/datapackages/supports/by-request-year/datapackage.json (supports)
        'supports',
        # http://next.obudget.org/datapackages/reports/all/datapackage.json (reports)
        'reports',
        # http://next.obudget.org/datapackages/budget/national/processed/connected-items-explained/datapackage.json (budget)
        'budget'
    ]
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
