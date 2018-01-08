open-budget-search-api
======================

### Quickstart

* Follow the README from [this branch of budgetkey data pipelines](https://github.com/OriHoch/budgetkey-data-pipelines/tree/load_data_take3) README to setup the docker-compose and load data to ES
* `docker build -t budgetkey/open-budget-search-api .`
* If you used the default docker compose environment from budgetkey-data-pipelines, this should work:
  * `docker run -d --name open-budget-search-api --rm -p18000:8000 --network budgetkeydatapipelines_default -eES_HOST=elasticsearch -eES_PORT=9200 budgetkey/open-budget-search-api`
* app should be available at localhost:18000
  * http://localhost:18000/search/exemptions/web/2000-01-01/2019-01-01/4/0
  * http://localhost:18000/search/budget,national-budget-changes,contract-spending,entities/%D7%9E%D7%99%D7%A7/1992-01-01/2019-01-01/10/0
