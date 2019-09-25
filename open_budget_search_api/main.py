import os

import elasticsearch

from flask import Flask
from flask_cors import CORS

from apies import apies_blueprint

DATAPACKAGE_BASE = 'http://next.obudget.org/datapackages/budgetkey/{}/datapackage.json'
ES_HOST = os.environ.get('ES_HOST', 'localhost')
ES_PORT = int(os.environ.get('ES_PORT', '9200'))
INDEX_NAME = os.environ.get('INDEX_NAME', 'budgetkey')

app = Flask(__name__)
CORS(app)


def text_rules(field):
    if field.get('es:title') or field.get('es:hebrew'):
        if field.get('es:keyword'):
            return [('exact', '^10')]
        else:
            return [('inexact', '^3'), ('natural', '.hebrew^10')]
    elif field.get('es:boost'):
        if field.get('es:keyword'):
            return [('exact', '^10')]
        else:
            return [('inexact', '^10')]
    elif field.get('es:keyword'):
        return [('exact', '')]
    else:
        return [('inexact', '')]


blueprint = apies_blueprint(app,
    [
        DATAPACKAGE_BASE.format(doctype)
        for doctype in [
            'people',
            'tenders',
            'entities',
            'contract-spending',
            'national-budget-changes',
            'supports',
            'reports',
            'budget',
            'gov_decisions',
            'calls_for_bids',
            'support_criteria',
        ]
    ],
    elasticsearch.Elasticsearch([dict(host=ES_HOST, port=ES_PORT)], timeout=60),
    'budgetkey',
    dont_highlight={
        'kind',
        'kind_he',
        'tender_type_he',
        'budget_code',
        'entity_kind',
        'entity_id',
        'code',
        'decision',
        'simple_decision',
    },
    text_field_rules=text_rules,
    debug_queries=True
)
app.register_blueprint(blueprint, url_prefix='/')

if __name__ == '__main__':
    app.run()
