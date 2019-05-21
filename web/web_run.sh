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
      flask db migrate -m "posts table"
      flask db upgrade
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
    fi
}

script_param=$1

main