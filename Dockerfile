FROM codexfons/gunicorn

USER root

RUN apk add --update --virtual=build-dependencies wget ca-certificates python3-dev build-base
RUN apk add --update libpq
RUN python3 --version

ADD [a-z_A-Z]* $APP_PATH/
RUN ls -la /opt/app/
RUN pip install -r $APP_PATH/requirements.txt
RUN apk del build-dependencies
RUN rm -rf /var/cache/apk/*

USER $GUNICORN_USER

ENV GUNICORN_MODULE=main:app

EXPOSE 8000