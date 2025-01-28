@echo off
title qt-files to .py files converter !

rem convert the resouce-file
call pyrcc5 almgis/resources.qrc -o almgis/resources_rc.py

call pyuic5 --from-imports almgis/mainwindow.ui -o almgis/mainwindow_UI.py

call pyuic5 --from-imports almgis/scopes/kontakt/kontakt.ui -o almgis/scopes/kontakt/kontakt_UI.py


echo -
echo -
echo -
echo - Dateien umgewandelt!!!
echo -
pause
