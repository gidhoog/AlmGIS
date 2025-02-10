@echo off


SET OSGEO4W_ROOT=C:\work\_anwendungen\OSGeo4W

call "%OSGEO4W_ROOT%\bin\o4w_env.bat"
rem call "%OSGEO4W_ROOT%\bin\qt5_env.bat"
rem call "%OSGEO4W_ROOT%\bin\py3_env.bat"

@echo off
set PATH=%OSGEO4W_ROOT%\apps\qgis-ltr\bin;C:\work\Projekte\AlmGIS\.venv\Scripts;%OSGEO4W_ROOT%\apps\Qt5\bin;%PATH%

set O4W_QT_BINARIES=%OSGEO4W_ROOT%\apps\Qt5\bin
set O4W_QT_DOC=%OSGEO4W_ROOT%\apps\Qt5\doc
set O4W_QT_HEADERS=%OSGEO4W_ROOT%\apps\Qt5\include
set O4W_QT_LIBRARIES=%OSGEO4W_ROOT%\apps\Qt5\lib
set O4W_QT_PLUGINS=%OSGEO4W_ROOT%\apps\Qt5\plugins
set O4W_QT_PREFIX=%OSGEO4W_ROOT%\apps\Qt5
set O4W_QT_TRANSLATIONS=%OSGEO4W_ROOT%\apps\Qt5\translations
set QT_PLUGIN_PATH=%OSGEO4W_ROOT%\apps\qgis-ltr\qtplugins;%OSGEO4W_ROOT%\apps\Qt5\plugins

rem set QGIS_PREFIX_PATH=%OSGEO4W_ROOT:\=/%/apps/qgis-ltr

set GDAL_FILENAME_IS_UTF8=YES

set VSI_CACHE=TRUE
set VSI_CACHE_SIZE=1000000

set PYTHONPATH=%OSGEO4W_ROOT%\bin;%OSGEO4W_ROOT%\apps\qgis-ltr\python;%OSGEO4W_ROOT%\apps\qgis-ltr\python\plugins;%OSGEO4W_ROOT%\apps\Python312\lib\site-packages;%PYTHONPATH%

rem set PYTHONHOME=%OSGEO4W_ROOT%\apps\Python312

rem von pythonpath entfernt: C:\work\_anwendungen\OSGeo4W\apps\qgis-ltr\python;C:\work\Projekte\AlmGIS\almgis\venv_02\Lib\site-packages
pyinstaller --clean --noconfirm --log-level=DEBUG almgis_folder.spec
pause
