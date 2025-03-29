#!/bin/bash
cd graph_explorer

python manage.py makemigrations
python manage.py migrate
python manage.py runserver

cd ..