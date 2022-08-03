call make.bat clean

REM From crikit/docs directory
REM Build API w/o pyuic5-generated files
call sphinx-apidoc.exe -f -o ./source/ ../ ../crikit/ui/qt_* ../crikit/ui/*_rc* ../crikit/ui/old/** ../setup.py

REM make html  
REM On Windows
call make.bat html