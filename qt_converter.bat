@echo off
title qt-files to .py files converter !

rem convert the resouce-file
call pyrcc5 resources.qrc -o resources_rc.py

call pyuic5 core/entity_titel.ui -o core/entity_titel_UI.py
call pyuic5 core/main_dialog.ui -o core/main_dialog_UI.py
call pyuic5 core/footer_line.ui -o core/footer_line_UI.py
call pyuic5 core/main_window.ui -o core/main_window_UI.py
call pyuic5 core/main_widget.ui -o core/main_widget_UI.py
call pyuic5 core/data_view.ui -o core/data_view_UI.py
call pyuic5 core/main_gis.ui -o core/main_gis_UI.py
call pyuic5 core/settings.ui -o core/settings_UI.py
call pyuic5 core/print_content_widget.ui -o core/print_content_widget_UI.py

call pyuic5 core/scopes/akte/akt.ui -o core/scopes/akte/akt_UI.py
call pyuic5 core/scopes/akte/abgrenzung.ui -o core/scopes/akte/abgrenzung_UI.py

call pyuic5 core/scopes/gst/gst_gemeinsame_werte.ui -o core/scopes/gst/gst_gemeinsame_werte_UI.py
call pyuic5 core/scopes/gst/gst_zuordnung.ui -o core/scopes/gst/gst_zuordnung_UI.py
call pyuic5 core/scopes/gst/gst_zuordnung_dataform.ui -o core/scopes/gst/gst_zuordnung_dataform_UI.py
call pyuic5 core/scopes/gst/gst.ui -o core/scopes/gst/gst_UI.py
call pyuic5 core/scopes/gst/gst_version.ui -o core/scopes/gst/gst_version_UI.py
call pyuic5 core/scopes/gst/gst_version_banu.ui -o core/scopes/gst/gst_version_banu_UI.py
call pyuic5 core/scopes/gst/gst_version_eigentuemer.ui -o core/scopes/gst/gst_version_eigentuemer_UI.py

call pyuic5 core/scopes/komplex/komplex_dataform.ui -o core/scopes/komplex/komplex_dataform_UI.py

call pyuic5 core/scopes/koppel/koppel.ui -o core/scopes/koppel/koppel_UI.py

echo -
echo -
echo -
echo - Dateien umgewandelt!!!
echo -
pause