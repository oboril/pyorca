:: Uses OpenBabel to generate 3D conformer from SMILES

@echo off
set PYTHONPATH=%~dp0..
echo.
python -m orcapython.scripts.gen3d %*