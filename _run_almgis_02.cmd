rem @ECHO off

set OSGEO4W_ROOT=C:\work\_anwendungen\OSGeo4W

call "%OSGEO4W_ROOT%\bin\o4w_env.bat"
call "%OSGEO4W_ROOT%\bin\qt5_env.bat"
call "%OSGEO4W_ROOT%\bin\py3_env.bat"
call "%OSGEO4W_ROOT%\apps\grass\grass78\etc\env.bat"

path %OSGEO4W_ROOT%\apps\qgis\bin;%PATH%
set QGIS_PREFIX_PATH=%OSGEO4W_ROOT%\apps\qgis

set GDAL_FILENAME_IS_UTF8=YES

set VSI_CACHE=TRUE
set VSI_CACHE_SIZE=1000000
set QT_PLUGIN_PATH=%OSGEO4W_ROOT%\apps\qgis-ltr\qtplugins;%OSGEO4W_ROOT%\apps\qt5\plugins

set PYTHONPATH=%OSGEO4W_ROOT%\apps\qgis-ltr\python
set PYTHONHOME=%OSGEO4W_ROOT%\apps\Python312
set PYTHONPATH=%OSGEO4W_ROOT%\apps\Python312\lib\site-packages;%PYTHONPATH%

set QT_QPA_PLATFORM_PLUGIN_PATH=%OSGEO4W_ROOT%\apps\Qt5\plugins\platforms
set QGIS_PREFIX_PATH=%OSGEO4W_ROOT%\apps\qgis-ltr

set PYTHONPATH=%OSGEO4W_ROOT%\apps\qgis-ltr\python\plugins;%PYTHONPATH%
set PYTHONPATH=C:\work\Projekte\AlmGIS\almgis\venv\Lib\site-packages;%PYTHONPATH%

set PATH=%OSGEO4W_ROOT%\apps\qgis-ltr\bin;%OSGEO4W_ROOT%\apps\qgis-ltr\python\plugins;%OSGEO4W_ROOT%\apps\qgis-ltr\python\plugins\processing;%OSGEO4W_ROOT%\apps\qgis-ltr\python\qgis;%OSGEO4W_ROOT%\bin;%PATH%

@call C:/work/Projekte/AlmGIS/almgis/venv/Skripts/activate.bat
python almgis.py
pause
