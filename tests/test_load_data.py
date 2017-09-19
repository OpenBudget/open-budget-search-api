from load_data import initialize_db
from open_budget_search_api.config import get_es_client


TEST_INDEX_NAME = "obudget_test_load_data"


def test_load_data_clean():
    es = get_es_client()
    if es.indices.exists(TEST_INDEX_NAME):
        es.indices.delete(TEST_INDEX_NAME)
    initialize_db("clean", index_name=TEST_INDEX_NAME)
    assert es.indices.exists(TEST_INDEX_NAME)
