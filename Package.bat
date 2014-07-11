@echo off

:: Generate documentation 
:: Create directory structure 
:: Generate package

set PATH=C:\Python34;%PATH%
set PYDOC=C:\Python34\Tools\Scripts\pydoc3.py
echo Generating documentation....

cd src 
python %PYDOC% .\
move *.html ..\doc

cd ..\test
python %PYDOC% .\
move *.html ..\doc