from flask import Flask, request, jsonify

import elastic
from .logger import logger

app = Flask(__name__)


@app.route('/', methods = ['GET'])
def main_handler():
    if request.method == 'GET':
        return "Hello, world"

# @app.route('/index/<string:type_name>', methods = ['POST'])
# def index_document_handler(type_name):
#     data = request.get_json()
#     elastic.index_doc(type_name, data)


@app.route('/search/<string:types>/<string:search_term>/<string:from_date>/<string:to_date>/<string:size>/<string:offset>',
           methods=['GET'])
def search_handler(types, search_term, from_date, to_date, size, offset):
    types_formatted = str(types).split(",")
    try:
        result = elastic.search(types_formatted, search_term, from_date, to_date, size, offset)
    except Exception as e:
        logger.exception("Error searching %s for tables: %s " % (search_term, str(types)))
        return str(e)
    return jsonify(result)

if __name__ == "__main__":
    app.run()
