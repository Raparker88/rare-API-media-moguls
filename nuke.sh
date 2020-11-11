#!/bin/bash

rm -rf rareapi/migrations
rm db.sqlite3
python manage.py migrate