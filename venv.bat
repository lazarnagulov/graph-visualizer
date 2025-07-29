@echo off

IF EXIST venv (
    echo Removing existing environment.
    rmdir /s /q venv
)

echo Creating new environment.
python -m venv venv
call venv\Scripts\activate

echo Environment has been activated successfully!