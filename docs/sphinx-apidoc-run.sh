# From crikit/docs directory
# Build API w/o pyuic5-generated files
sphinx-apidoc -f -o .\source\ ..\crikit\ ..\crikit\ui\qt_* ..\crikit\ui\*_rc* ..\crikit\ui\old\**

# make html  
# On Windows
make.bat html