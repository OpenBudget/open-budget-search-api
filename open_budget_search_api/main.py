import demjson

from flask import Flask, request
from flask.helpers import NotFound
from flask_jsonpify import jsonpify
from flask_cors import CORS

from .elastic import search, count, timeline, get_document
from .logger import logger

app = Flask(__name__)
CORS(app)


@app.route('/search/<string:types>/<string:search_term>/'
           '<string:from_date>/<string:to_date>/'
           '<string:size>/<string:offset>',
           methods=['GET'])
def search_handler(types, search_term, from_date, to_date, size, offset):
    try:
        types_formatted = str(types).split(',')
        filters = request.values.get('filter')
        result = search(types_formatted, search_term, from_date, to_date, size, offset, filters)
    except Exception as e:
        logger.exception('Error searching %s for types: %s ' % (search_term, str(types)))
        result = {'error': str(e)}
    return jsonpify(result)


@app.route('/search/<string:types>/<string:search_term>',
           methods=['GET'])
def simple_search_handler(types, search_term):
    try:
        types_formatted = str(types).split(',')
        filters = request.values.get('filter')
        result = search(types_formatted, search_term, None, None, 100, 0, filters)
    except Exception as e:
        logger.exception('Error searching %s for tables: %s ' % (search_term, str(types)))
        result = {'error': str(e)}
    return jsonpify(result)


@app.route('/search/count/<string:search_term>/'
           '<string:from_date>/<string:to_date>',
           methods=['GET'])
def count_handler(search_term, from_date, to_date):
    config = request.values.get('config')
    try:
        config = demjson.decode(config)
        result = count(search_term, from_date, to_date, config)
    except Exception as e:
        logger.exception('Error counting with config %r', config)
        result = {'error': str(e)}
    return jsonpify(result)


@app.route('/search/count/<string:search_term>',
           methods=['GET'])
def simple_count_handler(search_term):
    config = request.values.get('config')
    try:
        config = demjson.decode(config)
        result = count(search_term, None, None, config)
    except Exception as e:
        logger.exception('Error counting with config %r', config)
        result = {'error': str(e)}
    return jsonpify(result)


@app.route('/search/timeline/<string:types>/<string:search_term>/'
           '<string:from_date>/<string:to_date>',
           methods=['GET'])
def timeline_handler(types, search_term, from_date, to_date):
    try:
        types_formatted = str(types).split(',')
        filters = request.values.get('filter')
        result = timeline(types_formatted, search_term, from_date, to_date, filters)
    except Exception as e:
        logger.exception('Error getting timeline %s for types: %s ' % (search_term, str(types)))
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


if __name__ == '__main__':
    app.run()
