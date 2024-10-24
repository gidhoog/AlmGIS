@echo off

set PATH=C:\work\_anwendungen\OSGeo4W\apps\qgis-ltr\bin;C:\work\_ANWEN~1\OSGeo4W\apps\qt5\bin;C:\work\_ANWEN~1\OSGeo4W\apps\Python312\Scripts;C:\work\_ANWEN~1\OSGeo4W\bin;C:\work\Projekte\AlmGIS\almgis;C:\work\_anwendungen\OSGeo4W\apps\Qt5;C:\work\Projekte\AlmGIS\almgis;C:\work\_ANWEN~1\OSGeo4W\apps\qgis-ltr\python\plugins;C:\work\_ANWEN~1\OSGeo4W\apps\Python312\lib\site-packages;C:\work\_ANWEN~1\OSGeo4W\apps\qgis-ltr\python;C:\work\_ANWEN~1\OSGeo4W\bin\python312.zip;C:\work\_ANWEN~1\OSGeo4W\apps\Python312\DLLs;C:\work\_ANWEN~1\OSGeo4W\apps\Python312\Lib;C:\work\Projekte\AlmGIS\almgis\venv_02\Scripts;C:\work\Projekte\AlmGIS\almgis\venv_02;C:\work\Projekte\AlmGIS\almgis\venv_02\Lib\site-packages;%PATH%
set O4W_QT_BINARIES=C:\work\_anwendungen\OSGeo4W\apps\Qt5\bin
set O4W_QT_DOC=C:\work\_anwendungen\OSGeo4W\apps\Qt5\doc
set O4W_QT_HEADERS=C:\work\_anwendungen\OSGeo4W\apps\Qt5\include
set O4W_QT_LIBRARIES=C:\work\_anwendungen\OSGeo4W\apps\Qt5\lib
set O4W_QT_PLUGINS=C:\work\_anwendungen\OSGeo4W\apps\Qt5\plugins
set O4W_QT_PREFIX=C:\work\_anwendungen\OSGeo4W\apps\Qt5
set O4W_QT_TRANSLATIONS=C:\work\_anwendungen\OSGeo4W\apps\Qt5\translations
set QT_PLUGIN_PATH=C:\work\_anwendungen\OSGeo4W\apps\qgis-ltr\qtplugins;C:\work\_anwendungen\OSGeo4W\apps\Qt5\plugins
set PYTHONPATH=C:\work\_anwendungen\OSGeo4W\bin;C:\work\_anwendungen\OSGeo4W\apps\qgis-ltr\python;C:\work\_anwendungen\OSGeo4W\apps\qgis-ltr\python\plugins;C:\work\_anwendungen\OSGeo4W\apps\qgis-ltr\python\qgis;C:\work\_anwendungen\OSGeo4W\apps\qgis-ltr\python\qgis\core;C:\work\_anwendungen\OSGeo4W\apps\Python312\Lib\site-packages;C:\work\Projekte\AlmGIS\almgis\venv_02\Lib\site-packages


rem PATH=C:\work\_ANWEN~1\OSGeo4W\apps\qgis-ltr\bin;C:\work\_ANWEN~1\OSGeo4W\apps\qt5\bin;C:\work\_ANWEN~1\OSGeo4W\apps\Python312\Scripts;C:\work\_ANWEN~1\OSGeo4W\bin;C:\WINDOWS\system32;C:\WINDOWS;C:\WINDOWS\system32\WBem
set GDAL_DATA=C:\work\_anwendungen\OSGeo4W\apps\gdal\share\gdal
set GDAL_DRIVER_PATH=C:\work\_anwendungen\OSGeo4W\apps\gdal\lib\gdalplugins
set GDAL_FILENAME_IS_UTF8=YES
set PDAL_DRIVER_PATH=C:\work\_anwendungen\OSGeo4W\apps\pdal\plugins
set OSGEO4W_ROOT=C:\work\_anwendungen\OSGeo4W
rem set PROJ_DATA=C:\work\_ANWEN~1\OSGeo4W\share\proj
rem set PYTHONHOME=C:\work\_anwendungen\OSGeo4W\apps\Python312
set PYTHONUTF8=1
set QGIS_PREFIX_PATH=C:\work\_anwendungen\OSGeo4W\apps\qgis-ltr
rem set QT_PLUGIN_PATH=C:\work\_ANWEN~1\OSGeo4W\apps\qgis-ltr\qtplugins;C:\work\_ANWEN~1\OSGeo4W\apps\qt5\plugins
set VSI_CACHE=TRUE
set VSI_CACHE_SIZE=1000000
rem set O4W_QT_PREFIX=C:/work/_ANWEN~1/OSGeo4W/apps/Qt5
rem set O4W_QT_BINARIES=C:/work/_ANWEN~1/OSGeo4W/apps/Qt5/bin
rem set O4W_QT_PLUGINS=C:/work/_ANWEN~1/OSGeo4W/apps/Qt5/plugins
rem set O4W_QT_LIBRARIES=C:/work/_ANWEN~1/OSGeo4W/apps/Qt5/lib
rem set O4W_QT_TRANSLATIONS=C:/work/_ANWEN~1/OSGeo4W/apps/Qt5/translations
rem set O4W_QT_HEADERS=C:/work/_ANWEN~1/OSGeo4W/apps/Qt5/include
set QGIS_WIN_APP_NAME=OSGeo4W\QGIS Desktop 3.34.10
set SSL_CERT_DIR=C:\work\_anwendungen\OSGeo4W\apps\openssl\certs
set SSL_CERT_FILE=C:\work\_anwendungen\OSGeo4W\bin\curl-ca-bundle.crt

pyinstaller --clean --noconfirm --log-level=DEBUG almgis_folder.spec
pause
