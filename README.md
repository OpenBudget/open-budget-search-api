open-budget-search-api
======================

### Setup Elasticsearch with data

The budgetkey-data-pipelines project handles the loading of data to elasticsearch

see [load the datapackages to elasticsearch](https://github.com/openbudget/budgetkey-data-pipelines#loading-datapackages-to-elasticsearch) for a method to get a local elasticsearch instance with the data.


### Running

Build the search api image

```
docker build -t open-budget-search-api .
```

Run the image, modify ES_HOST and ES_PORT to connect to the relevant Elasticsearch instance.

The following command connects to the budgetkey-data-pipelines default docker compose elasticsearch.

```
docker run -d --name open-budget-search-api --rm -p18000:8000 \
           --network budgetkeydatapipelines_default \
           -eES_HOST=elasticsearch -eES_PORT=9200 \
           budgetkey/open-budget-search-api
```

Search api should be available at localhost:18000

* http://localhost:18000/search/exemptions/web/2000-01-01/2019-01-01/4/0
* http://localhost:18000/search/budget,national-budget-changes,contract-spending,entities/%D7%9E%D7%99%D7%A7/1992-01-01/2019-01-01/10/0


### Development

Start the search api, modify ES_HOST and ES_PORT to connect to the relevant Elasticsearch instance.

The following command connects to the budgetkey-data-pipelines default docker compose elasticsearch.

```
ES_HOST=localhost ES_PORT=19200 python3 -c 'from open_budget_search_api.main import app; app.run()'
```

This is the search URL format:

`http://localhost:5000/search/comma_seperated_table_names/search_term/from_data/to_date/maxinum_size_of_result/offset`

for example - http://localhost:5000/search/exemption/test/2000-01-01/2019-01-01/4/0

There is a log for exceptions called obudget.log which is written right next to the main.py
