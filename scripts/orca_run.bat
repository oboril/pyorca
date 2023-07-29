:: Runs orca with neat directory structure

@echo off
set PYTHONPATH=%~dp0..
echo.
python -m orcapython.scripts.run %*