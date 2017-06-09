from datapackage import DataPackage

from .config import INDEX_NAME
from .logger import logger


class DataSource(object):

    def __init__(self, dp_url):
        self.datapackage = DataPackage(dp_url)
        self.resource = self.datapackage.resources[0]
        descriptor = self.resource.descriptor
        self.type_name = descriptor['name']

        schema = descriptor['schema']
        fields = schema['fields']

        self.search_fields = [field['name']
                              for field in fields
                              if field['type'] == 'string']
        self.keys = schema['primaryKey']
        if isinstance(self.keys, str):
            self.keys = [self.keys]

        self.date_fields = {}
        self.range_structure = {}
        for range_kw, operator in [('from', 'gte'), ('to', 'lte')]:
            for field in fields:
                if range_kw in field.get('search:time-range', ''):
                    self.date_fields[range_kw] = field['name']
                    self.range_structure.setdefault(field['name'], {})[operator] = range_kw + '_date'
        self.is_temporal = False  # len(self.date_fields) > 0

        sort_fields = sorted(
            filter(lambda f: 'search:sort-order' in f, fields),
            key=lambda f: f['search:sort-order']
        )
        self.sort_method = [
            {
                field['name']: {
                    'order': field['search:sort-direction']
                }
            }
            for field in sort_fields
        ]

        self.mapping = self.build_mapping(schema)

    @staticmethod
    def json_type_to_elastic_type(json_type):
        switcher = {
            "integer": "long",
            "number": "double",
            "string": "string",
            "array": "string",
            "object": "object"
        }
        return switcher.get(json_type, "string")

    def build_mapping(self, schema):
        fields = schema["fields"]
        mapping_data = {
            # Setting the default analyzer to hebrew
            "dynamic_templates": [
                {
                    "strings": {
                        "match_mapping_type": "string",
                        "mapping": {
                            "type": "string",
                            "analyzer": "hebrew",
                            "fields": {
                                "raw": {
                                    "type": "string",
                                    "index": "not_analyzed"
                                }
                            }
                        }
                    }
                }
            ],
            "properties": {}
        }
        for field in fields:
            mapping_data['properties'][field['name']] = {
                'type': self.json_type_to_elastic_type(field["type"])
            }
        return mapping_data

    def put_mapping(self, es):
        es.indices.put_mapping(index=INDEX_NAME, doc_type=self.type_name, body=self.mapping)

    def load(self, es, revision=None):
        for i, doc in enumerate(self.resource.iter()):
            if i % 10000 == 0:
                logger.info('LOADING %s: %s rows', self.type_name, i)
            doc_id = ":".join(str(doc.get(k)) for k in self.keys)
            if revision is not None:
                doc['revision'] = revision
            try:
                es.index(INDEX_NAME, self.type_name, doc, id=doc_id)
            except Exception as e:
                logger.exception("Failed to index %s row %s: %r", self.type_name, doc_id, doc)
