#!/bin/sh
set -e

cd $APP_PATH
sleep 10
python3 init_db.py
python3 init_db.py budget &
python3 init_db.py exemption &
python3 init_db.py supports &
python3 init_db.py entities &
python3 init_db.py changes &
python3 init_db.py procurement &

$APP_PATH/entrypoint.sh
