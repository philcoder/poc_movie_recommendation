#!/bin/bash

cd /home/web

sleep 5
bash web_run.sh db_check_build
sleep 2
bash web_run.sh start
