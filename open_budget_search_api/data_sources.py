import json

from .config import SEARCHABLE_DATAPACKAGES
from .data_source import DataSource

_sources = None


def sources():
    global _sources
    if _sources is None:
        try:
            _sources = json.load(open('source_config.json'))
        except Exception:
            searchable_sources = [
                DataSource(url) for url in SEARCHABLE_DATAPACKAGES
            ]

            _sources = dict(
                (ds.type_name, ds.search_fields) for ds in searchable_sources
            )
            json.dump(_sources, open('source_config.json', 'w'))
    return _sources
