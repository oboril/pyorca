:: Aligns two or more .xyz files and prints RMSD

@echo off
set PYTHONPATH=%~dp0..
echo.
python -m orcapython.scripts.align %*