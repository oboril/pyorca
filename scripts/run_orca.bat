:: Runs ORCA calculation using the pyorca.run_orca() function

@echo off
set PYTHONPATH=%~dp0../src/
echo.
python -c "import pyorca; import sys; pyorca.run_orca(sys.argv[1]);" %*