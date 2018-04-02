from datapackage import DataPackage

from .config import INDEX_NAME
from .logger import logger
from .mapping_generator import MappingGenerator


class DataSource(object):

    def __init__(self, dp_url):
        self.datapackage = DataPackage(dp_url)
        self.resource = self.datapackage.resources[0]
        descriptor = self.resource.descriptor
        self.type_name = descriptor['name']

        self._schema = descriptor['schema']
        fields = self._schema['fields']

        try:
            self.keys = self._schema['primaryKey']
        except KeyError:
            logger.exception('Failed to load %s', dp_url)
            raise
        if isinstance(self.keys, str):
            self.keys = [self.keys]

        self.range_structure = {}

        try:
            self.scoring_column = next(iter(
                filter(lambda f: 'es:score-column' in f, fields),
            ))['name']
        except StopIteration:
            self.scoring_column = '<none>'
        self._mapping_generator = MappingGenerator()
        try:
            self.mapping, self.search_fields = self.build_mapping(self._schema)
        except: #noqa
            logger.exception('Failed to load %s', dp_url)
            raise

    def build_mapping(self, schema):
        self._mapping_generator.generate_from_schema(schema)
        return self._mapping_generator.get_mapping(), self._mapping_generator.get_search_fields()

    def put_mapping(self, es):
        es.indices.put_mapping(index=INDEX_NAME, doc_type=self.type_name, body=self.mapping)

    def load(self, es, revision=None):
        try:
            for i, doc in enumerate(self.resource.iter()):
                if i % 10000 == 0:
                    logger.info('LOADING %s: %s rows', self.type_name, i)
                doc_id = ":".join(str(doc.get(k)) for k in self.keys)
                if revision is not None:
                    doc['revision'] = revision
                try:
                    es.index(INDEX_NAME, self.type_name, doc, id=doc_id)
                except Exception:
                    logger.exception("Failed to index %s row %s: %r", self.type_name, doc_id, doc)
                yield doc_id
        except Exception:
            logger.exception("Failed to load %s", self.type_name)
