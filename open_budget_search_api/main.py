import demjson

from flask import Flask, request
from flask.helpers import NotFound
from flask_jsonpify import jsonpify
from flask_cors import CORS

from .elastic import search, get_document
from .logger import logger

app = Flask(__name__)
CORS(app)


def fetch_filters(filters):
    if not filters:
        return []
    filters = '{' + filters + '}'
    try:
        filters = demjson.decode(filters)
        ret = []
        for k, v in filters.items():
            parts = k.split('__')
            if len(parts) > 1 and parts[-1] in ('gt', 'gte', 'lt', 'lte', 'eq'):
                k = '__'.join(parts[:-1])
                ret.append((k, parts[-1], v))
            else:
                ret.append((k, 'eq', v))
        return ret
    except Exception:
        raise 'Failed to parse filters {!r}'.format(filters)


@app.route('/search/<string:types>/<string:search_term>/'
           '<string:from_date>/<string:to_date>/'
           '<string:size>/<string:offset>',
           methods=['GET'])
def search_handler(types, search_term, from_date, to_date, size, offset):
    try:
        types_formatted = str(types).split(",")
        filters = fetch_filters(request.values.get('filter'))
        result = search(types_formatted, search_term, from_date, to_date, size, offset, filters)
    except Exception as e:
        logger.exception("Error searching %s for tables: %s " % (search_term, str(types)))
        result = {'error': str(e)}
    return jsonpify(result)


@app.route('/search/<string:types>/<string:search_term>',
           methods=['GET'])
def simple_search_handler(types, search_term):
    try:
        types_formatted = str(types).split(",")
        filters = fetch_filters(request.values.get('filter'))
        result = search(types_formatted, search_term, None, None, 100, 0, filters)
    except Exception as e:
        logger.exception("Error searching %s for tables: %s " % (search_term, str(types)))
        result = {'error': str(e)}
    return jsonpify(result)


@app.route('/get/<path:doc_id>',
           methods=['GET'])
def get_document_handler(doc_id):
    result = get_document('document', doc_id)
    if result is None:
        logger.warning('Failed to fetch document for %r', doc_id)
        raise NotFound()
    return jsonpify(result)


if __name__ == "__main__":
    app.run()
