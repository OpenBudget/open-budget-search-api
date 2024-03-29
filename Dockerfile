FROM python:3.10-slim

ENV GUNICORN_PORT=8000
ENV GUNICORN_MODULE=open_budget_search_api.main
ENV GUNICORN_CALLABLE=app
ENV GUNICORN_USER=gunicorn
ENV APP_PATH=/opt/app

RUN apt-get update && apt-get install --no-install-recommends -y wget && update-ca-certificates

# Install dependencies and create runtime user.
RUN pip3 install --upgrade pip gunicorn[gevent] \
    && adduser --disabled-password --home $APP_PATH $GUNICORN_USER

ADD . $APP_PATH

RUN cd $APP_PATH \
    && pip3 install -r requirements.txt && pip3 install $APP_PATH

USER $GUNICORN_USER

EXPOSE 8000

CMD cd $APP_PATH && gunicorn -t 120 --bind 0.0.0.0:$GUNICORN_PORT -k gevent -w 8 --limit-request-line 0 --log-level debug --access-logfile - $GUNICORN_MODULE:$GUNICORN_CALLABLE
