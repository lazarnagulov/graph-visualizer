@echo off
setlocal enabledelayedexpansion

if exist venv/Scripts/activate.bat (
  call venv/Scripts/activate.bat
)

call :install_component "Graph visualizer API" "./api"
if errorlevel 1 exit /b 1

call :install_component "Graph visualizer Core" "./core"
if errorlevel 1 exit /b 1

call :install_component "Simple visualizer" "./simple_visualizer"
if errorlevel 1 exit /b 1

call :install_component "Block visualizer" "./block_visualizer"
if errorlevel 1 exit /b 1

call :install_component "Graph explorer" "./graph_explorer"
if errorlevel 1 exit /b 1

echo All components installed successfully.
exit /b 0

:install_component
set component_name=%1
set component_path=%2

echo Installing %component_name%.

pip install %component_path% > output.log 2>&1
if %errorlevel% neq 0 (
    echo Error: Installation of %component_name% failed!
    type output.log
    exit /b 1
)

exit /b 0
