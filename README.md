# open-budget-search-api

### Installation

* Install Docker and Docker Compose (refer to Docker documentation)
* `cp docker-compose.override.example.yaml docker-compose.override.yaml`
* `docker-compose pull`
* `docker-compose up -d`

The api server should be available at http://localhost:18000/

### Usage

* `/search/<COMMA_SEPARATED_TABLE_NAMES>/<SEARCH_TERM>/<FROM_DATE>/<TO_DATE>/<MAXIMUM_SIZE_OF_RESULT>/<OFFSET>`
* for example:
  * http://localhost:18000/search/exemptions/web/2000-01-01/2019-01-01/4/0
