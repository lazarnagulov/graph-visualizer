@echo off

if exist venv/Scripts/activate.bat (
  call venv/Scripts/activate.bat
)

if "%1"=="graph_explorer" (
  set "package-name=graph_visualizer_web"
) else if "%1"=="core" (
  set "package-name=graph_visualizer_core"
) else if "%1"=="api" (
  set "package-name=graph_visualizer_api"
) else (
  set "package-name=%1"
)

cd .\%1
rmdir /s /q build
rmdir /s /q .\%package-name%.egg-info
cd ..

pip uninstall %package-name% -y
pip install .\%1