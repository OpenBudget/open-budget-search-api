from datapackage import DataPackage
from elasticsearch import helpers

from .config import INDEX_NAME, LOAD_DATA_BULK_INDEX_BATCH, LOAD_DATA_LOG_EVERY
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

        self.date_fields = {}
        self.range_structure = {}
        for range_kw, operator in [('from', 'gte'), ('to', 'lte')]:
            for field in fields:
                if range_kw in field.get('search:time-range', ''):
                    self.date_fields[range_kw] = field['name']
                    self.range_structure.setdefault(field['name'], {})[operator] = range_kw + '_date'
        self.is_temporal = False  # len(self.date_fields) > 0

        try:
            self.scoring_column = next(iter(
                filter(lambda f: 'es:score-column' in f, fields),
            ))['name']
        except StopIteration:
            self.scoring_column = '<none>'
        self._mapping_generator = MappingGenerator()
        try:
            self.mapping, self.search_fields = self.build_mapping(self._schema)
        except:
            logger.exception('Failed to load %s', dp_url)
            raise

    def build_mapping(self, schema):
        self._mapping_generator.generate_from_schema(schema)
        return self._mapping_generator.get_mapping(), self._mapping_generator.get_search_fields()

    def put_mapping(self, es, index=INDEX_NAME):
        es.indices.put_mapping(index=index, doc_type=self.type_name, body=self.mapping)

    def bulk_index_flush(self, es):
        if len(self.bulk_index_actions) >= LOAD_DATA_BULK_INDEX_BATCH:
            success, errors = helpers.bulk(es, self.bulk_index_actions)
            if not success:
                logger.error("Failed to index %s", self.type_name)
                logger.info(errors)
            yield from (action["_id"] for action in self.bulk_index_actions)
            self.bulk_index_actions = []

    def load(self, es, revision=None, index_name=INDEX_NAME):
        self.bulk_index_actions = []
        try:
            i = 0
            for i, doc in enumerate(self.resource.iter()):
                if i == 0:
                    logger.info('START LOADING %s', self.type_name)
                if i % LOAD_DATA_LOG_EVERY == 0:
                    logger.info('LOADING %s: %s rows loaded', self.type_name, i)
                doc_id = ":".join(str(doc.get(k)) for k in self.keys)
                if revision is not None:
                    doc['revision'] = revision
                self.bulk_index_actions.append({
                    "_index": index_name,
                    "_type": self.type_name,
                    "_id": doc_id,
                    "_source": doc
                })
                yield from self.bulk_index_flush(es)
            yield from self.bulk_index_flush(es)
            logger.info('FINISHED LOADING %s, loaded %s rows', self.type_name, i)
        except Exception:
            logger.exception("Failed to load %s", self.type_name)
