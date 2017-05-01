from .config import DATAPACKAGES
from .data_source import DataSource

sources = [
    DataSource(url) for url in DATAPACKAGES
]
sources = dict(
    (ds.type_name, ds) for ds in sources
)
