#!/bin/bash

APP_DIR=../app/
virtualenv $APP_DIR/.virtualenv
source $APP_DIR/.virtualenv/bin/activate
pip3 install --no-cache-dir -r requirements.txt
python3 manage.py migrate