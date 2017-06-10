from flask import Flask, jsonify
from flask_cors import CORS

from .elastic import search, autocomplete
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
    return jsonify(result)


@app.route('/autocomplete/<string:search_term>/',
           methods=['GET'])
def autocomplete_handler(search_term):
    try:
        result = autocomplete(search_term)
    except Exception as e:
        logger.exception("Error autocomplete %s" % search_term)
        result = {'error': str(e)}
    return jsonify(result)


if __name__ == "__main__":
    app.run()
