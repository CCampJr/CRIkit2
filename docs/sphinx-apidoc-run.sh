./make.bat clean

# From crikit/docs directory
# Build API w/o pyuic5-generated files
sphinx-apidoc.exe -f -o ./source/ ../ ../crikit/ui/qt_* ../crikit/ui/*_rc* ../crikit/ui/old/** ../setup.py

# make html  
# On Windows
./make.bat html