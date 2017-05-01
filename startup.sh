#!/bin/sh
set -e

cd $APP_PATH
sleep 10
python3 load_data.py clean
python3 load_data.py all &

$APP_PATH/entrypoint.sh
