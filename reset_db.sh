#!/bin/sh

#WARNING: THIS WILL RESET THE DATABASE!!!


rm database/db.sqlite3
rm */migrations/0*.py
python3 manage.py makemigrations
python3 manage.py migrate 

