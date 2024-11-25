@echo off
title qt-files to .py files converter !

rem convert the resouce-file
call pyrcc5 resources.qrc -o resources_rc.py

call pyuic5 almgis/mainwindow.ui -o almgis/mainwindow_UI.py



call pyuic5 app_core/entity_titel.ui -o app_core/entity_titel_UI.py
call pyuic5 app_core/main_dialog.ui -o app_core/main_dialog_UI.py
call pyuic5 app_core/footer_line.ui -o app_core/footer_line_UI.py
call pyuic5 app_core/filter_element.ui -o app_core/filter_element_UI.py
call pyuic5 app_core/main_window.ui -o app_core/main_window_UI.py
call pyuic5 app_core/main_widget.ui -o app_core/main_widget_UI.py
call pyuic5 app_core/data_view.ui -o app_core/data_view_UI.py
call pyuic5 app_core/main_gis.ui -o app_core/main_gis_UI.py
call pyuic5 app_core/settings.ui -o app_core/settings_UI.py
call pyuic5 app_core/print_content_widget.ui -o app_core/print_content_widget_UI.py

call pyuic5 app_core/scopes/akte/akt.ui -o app_core/scopes/akte/akt_UI.py
call pyuic5 app_core/scopes/akte/abgrenzung.ui -o app_core/scopes/akte/abgrenzung_UI.py

call pyuic5 app_core/scopes/gst/gst_gemeinsame_werte.ui -o app_core/scopes/gst/gst_gemeinsame_werte_UI.py
call pyuic5 app_core/scopes/gst/gst_zuordnung.ui -o app_core/scopes/gst/gst_zuordnung_UI.py
call pyuic5 app_core/scopes/gst/gst_zuordnung_dataform.ui -o app_core/scopes/gst/gst_zuordnung_dataform_UI.py
call pyuic5 app_core/scopes/gst/gst.ui -o app_core/scopes/gst/gst_UI.py
call pyuic5 app_core/scopes/gst/gst_version.ui -o app_core/scopes/gst/gst_version_UI.py
call pyuic5 app_core/scopes/gst/gst_version_banu.ui -o app_core/scopes/gst/gst_version_banu_UI.py
call pyuic5 app_core/scopes/gst/gst_version_eigentuemer.ui -o app_core/scopes/gst/gst_version_eigentuemer_UI.py

call pyuic5 app_core/scopes/komplex/komplex_dataform.ui -o app_core/scopes/komplex/komplex_dataform_UI.py

call pyuic5 app_core/scopes/koppel/koppel.ui -o app_core/scopes/koppel/koppel_UI.py

call pyuic5 app_core/scopes/kontakt/kontakt.ui -o app_core/scopes/kontakt/kontakt_UI.py

echo -
echo -
echo -
echo - Dateien umgewandelt!!!
echo -
pause
