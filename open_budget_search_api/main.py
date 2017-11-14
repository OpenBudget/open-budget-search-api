import logging
from flask import Flask
from flask.helpers import NotFound
from flask_jsonpify import jsonpify
from flask_cors import CORS

from .elastic import search, get_document
from .logger import logger

app = Flask(__name__)
CORS(app)


@app.route('/search/<string:types>/<string:search_term>/'
           '<string:from_date>/<string:to_date>/'
           '<string:size>/<string:offset>',
           methods=['GET'])
def search_handler(types, search_term, from_date, to_date, size, offset):
    types_formatted = str(types).split(",")
    try:
        result = search(types_formatted, search_term, from_date, to_date, size, offset)
    except Exception as e:
        logger.exception("Error searching %s for tables: %s " % (search_term, str(types)))
        result = {'error': str(e)}
    return jsonpify(result)


@app.route('/get/<path:doc_id>',
           methods=['GET'])
def get_document_handler(doc_id):
    result = get_document('document', doc_id)
    if result is None:
        logging.warning('Failed to fetch document for %r', doc_id)
        raise NotFound()
    return jsonpify(result)


if __name__ == "__main__":
    app.run()
