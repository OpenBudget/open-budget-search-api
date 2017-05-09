#!/bin/sh
set -e

cd $APP_PATH
sleep 10
python3 load_data.py clean
(while true ; do python3 load_data.py all ; sleep 3600 ; done )&

$APP_PATH/entrypoint.sh
