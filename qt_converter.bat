@echo off
title qt-files to .py files converter !

rem convert the resouce-file
call pyrcc5 resources.qrc -o resources_rc.py

call pyuic5 almgis/mainwindow.ui -o almgis/mainwindow_UI.py


echo -
echo -
echo -
echo - Dateien umgewandelt!!!
echo -
pause
