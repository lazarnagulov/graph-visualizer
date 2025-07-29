@echo off

if exist venv/Scripts/activate.bat (
  call venv/Scripts/activate.bat
)

cd .\%1
rmdir /s /q build
rmdir /s /q .\%1.egg-info
cd ..

pip uninstall %1 -y
pip install .\%1