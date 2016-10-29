import elastic
from elastic import logger
import tornado.ioloop
import tornado.web

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

class IndexDocumentHandler(tornado.web.RequestHandler):
    def post(self, type_name):
        data = tornado.escape.json_decode(self.request.body)
        elastic.index_doc(type_name, data)


class SearchHandler(tornado.web.RequestHandler):
    def get(self, types, search_term, from_date, to_date, size, offset):
        types_formatted = str(types).split(",")
        result = {}
        try:
            result = elastic.search(types_formatted, search_term, from_date, to_date, size, offset)
        except Exception as e:
            self.write(str(e))
            logger.exception("Error searching %s for tables: %s " % (search_term, str(types)))
        self.write(result)


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/index/(?P<type_name>[^\/]+)", IndexDocumentHandler),
        (r"/search/(?P<types>[^\/]+)/?(?P<search_term>[^\/]+)?/?(?P<from_date>[^\/]+)?/(?P<to_date>[^\/]+)/?(?P<size>[^\/]+)?/?(?P<offset>[^\/]+)?", SearchHandler)


    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()