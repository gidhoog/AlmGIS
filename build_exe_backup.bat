@echo off

set PATH=C:\work\_anwendungen\OSGeo4W\apps\qgis-ltr\bin;%PATH%
set O4W_QT_BINARIES=C:\work\_anwendungen\OSGeo4W\apps\Qt5\bin
set O4W_QT_LIBRARIES=C:\work\_anwendungen\OSGeo4W\apps\Qt5\lib
set O4W_QT_PLUGINS=C:\work\_anwendungen\OSGeo4W\apps\Qt5\plugins
set O4W_QT_PREFIX=C:\work\_anwendungen\OSGeo4W\apps\Qt5
set O4W_QT_TRANSLATIONS=C:\work\_anwendungen\OSGeo4W\apps\Qt5\translations
set QT_PLUGIN_PATH=C:\work\_anwendungen\OSGeo4W\apps\qgis-ltr\qtplugins;C:\work\_anwendungen\OSGeo4W\apps\Qt5\plugins
set PYTHONPATH=C:\work\_anwendungen\OSGeo4W\bin;
C:\work\_anwendungen\OSGeo4W\apps\qgis-ltr\python;
C:\work\_anwendungen\OSGeo4W\apps\qgis-ltr\python\plugins;
C:\work\_anwendungen\OSGeo4W\apps\Python39\Lib\site-packages;
C:\work\Projekte\AlmGIS\almgis\venv\Lib\site-packages;
C:\work\_anwendungen\OSGeo4W\apps\Python39;

pyinstaller --clean --noconfirm --log-level=DEBUG almgis_folder.spec
pause
