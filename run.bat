@echo off

if exist venv/Scripts/activate.bat (
  call venv/Scripts/activate.bat
)

cd graph_explorer

python manage.py makemigrations
python manage.py migrate
python manage.py runserver

cd ..