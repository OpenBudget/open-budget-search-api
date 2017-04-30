FROM codexfons/gunicorn

USER root

RUN apk add --update --virtual=build-dependencies wget ca-certificates python3-dev postgresql-dev build-base
RUN apk add --update libpq libxml2 libxslt
RUN python3 --version

COPY [a-z_A-Z]* $APP_PATH/
COPY open_budget_search_api/ $APP_PATH/open_budget_search_api/
RUN ls -la /opt/app/
RUN pip install -r $APP_PATH/requirements.txt
RUN apk del build-dependencies
RUN rm -rf /var/cache/apk/*

USER $GUNICORN_USER

ENV GUNICORN_MODULE=open_budget_search_api.main

EXPOSE 8000

ENTRYPOINT $APP_PATH/startup.sh
