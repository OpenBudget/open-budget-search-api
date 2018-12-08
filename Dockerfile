FROM codexfons/gunicorn

USER root

RUN apk add --update --no-cache --virtual=build-dependencies wget ca-certificates python3-dev postgresql-dev libxml2-dev libxslt-dev build-base
RUN apk add --update --no-cache libpq libxml2 libxslt libstdc++


COPY . $APP_PATH/
RUN pip3 install $APP_PATH

RUN apk del build-dependencies

USER $GUNICORN_USER

ENV GUNICORN_MODULE=open_budget_search_api.main

EXPOSE 8000
