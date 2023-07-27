@echo off
copy %1.inp runtime
C:\CompChemistry\Orca_504\orca.exe runtime/%1.inp > %1.out
echo BATCH FINISHED!