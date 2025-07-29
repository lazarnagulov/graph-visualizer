#!/bin/bash

if [ -f venv/bin/activate ]; then
  source venv/bin/activate
fi

cd graph_explorer

python manage.py makemigrations
python manage.py migrate
python manage.py runserver

cd ..