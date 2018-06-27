from datapackage import DataPackage

from .config import INDEX_NAME
from .logger import logger
from .mapping_generator import MappingGenerator


class DataSource(object):

    def __init__(self, dp_url):
        print('Loading from url', dp_url)
        self.datapackage = DataPackage(dp_url)
        self.resource = self.datapackage.resources[0]
        descriptor = self.resource.descriptor
        self.type_name = descriptor['name']
        self._schema = descriptor['schema']
        print('Done with', self.type_name)

        self._mapping_generator = MappingGenerator()
        try:
            self.search_fields = self.build_mapping(self._schema)
        except Exception:
            logger.exception('Failed to load %s', dp_url)
            raise

    def build_mapping(self, schema):
        self._mapping_generator.generate_from_schema(schema)
        return self._mapping_generator.get_search_fields()
