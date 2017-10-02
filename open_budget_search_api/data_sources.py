from .config import SEARCHABLE_DATAPACKAGES, NON_SEARCHABLE_DATAPACKAGES
from .data_source import DataSource

searchable_sources = [
    DataSource(url) for url in SEARCHABLE_DATAPACKAGES
]
non_searchable_sources = [
    DataSource(url) for url in NON_SEARCHABLE_DATAPACKAGES
]


sources = dict(
    (ds.type_name, ds) for ds in searchable_sources
)


all_sources = non_searchable_sources + searchable_sources
all_sources = dict(
    (ds.type_name, ds) for ds in all_sources
)
