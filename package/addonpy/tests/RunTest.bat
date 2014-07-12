@echo off

:: This is very simple batch script to run test cases.
:: DO NOT EXPECT ANYTHING FANCY!! :) 

set TEST_REPORT=test_run.txt
del %TEST_REPORT%

set PY27=c:\Python27\python.exe
set PY34=c:\Python34\python.exe

echo ==================================== >> %TEST_REPORT% 2>&1
echo Running tests with %PY27% >> %TEST_REPORT% 2>&1
echo ==================================== >> %TEST_REPORT% 2>&1
set PY=%PY27%
%PY% test_addonpy.py >> %TEST_REPORT% 2>&1
%PY% test_addonpyExecutor.py >> %TEST_REPORT% 2>&1
%PY% test_addonpyHelpers.py >> %TEST_REPORT% 2>&1

echo ==================================== >> %TEST_REPORT% 2>&1
echo Running tests with %PY34% >> %TEST_REPORT% 2>&1
echo ==================================== >> %TEST_REPORT% 2>&1
set PY=%PY34%

%PY% test_addonpy.py >> %TEST_REPORT% 2>&1
%PY% test_addonpyExecutor.py >> %TEST_REPORT% 2>&1
%PY% test_addonpyHelpers.py >> %TEST_REPORT% 2>&1
