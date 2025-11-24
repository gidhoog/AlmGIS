@echo off
title qt-files to .py files converter !

rem convert the resouce-file
call pyrcc5 resources.qrc -o ui_py/resources_rc.py

rem call pyuic5 --from-imports almgis/mainwindow.ui -o almgis/mainwindow_UI.py

call pyuic5 --from-imports ui/kontakt/kontakt.ui -o ui_py/kontakt/kontakt_UI.py


echo -
echo -
echo -
echo - Dateien umgewandelt!!!
echo -
pause
