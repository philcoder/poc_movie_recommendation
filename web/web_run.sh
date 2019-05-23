#!/bin/bash

function check_root {
  if [ "$(whoami)" != "root" ]; then
    echo "Sorry, you need to be root."
    exit 1
  fi
}

function main() {
    export FLASK_APP=web.py

    #get script diretory execution
    if [ "$script_param" == "start" ]; then
      check_root
      python3 -m flask run --host=0.0.0.0
    elif [ "$script_param" == "db_build" ]; then
      rm -R migrations
      flask db init
      flask db migrate -m "users table"
      flask db migrate -m "movie table"
      flask db migrate -m "userrating table"
      flask db migrate -m "suggestmovies table"
      flask db upgrade

      echo "add admin user"
      export PGPASSWORD='phil.poc.ia'
      psql -h postgres-service -p 5432 -d poc_db -U root -a -q -f util/data.sql
      echo "finish export sql data"

      echo "import dataset to DB"
      ./util/import_dataset.py
      echo "finish import dataset to DB"

    elif [ "$script_param" == "db_init" ]; then
      rm -R migrations
      flask db init
    elif [ "$script_param" == "db_upgrade" ]; then
      flask db upgrade
    elif [ "$script_param" == "db_migrate" ]; then
      flask db migrate -m "users table"
      flask db migrate -m "posts table"
    elif [ "$script_param" == "stop" ]; then
      check_root
      fuser -k -n tcp 5000
    else
      echo "cmd: '$script_param' not found!"
    fi
}

script_param=$1

main