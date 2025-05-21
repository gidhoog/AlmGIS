Entwicklerwerkzeuge
===================

Sphinx
______
(siehe `Sphinx <https://www.sphinx-doc.org/en/master/>`_)

Sphinx ist ein Python-Package zur Erstellung von Dokumentationen.

Basiskonfigurationen werden in der Datei ``docs/source/conf.py`` definiert.

Verwendung:
    Führe in der Konsole im docs-Verzeichnis folgenden Befehl aus
    um die Erstellung der html-Dukumentation anzustossen:

    - ``sphinx-build -M html source build``
    - oder ``make html`` (funktioniert in Linux nicht!)

PyInstaller
___________
(siehe `PyInstaller <https://pyinstaller.org/en/stable/>`_)

PyInstaller ist ein Python-Package zum Packen von Anwendungen (z.B. in einer
exe-Datei)

Verwendung:
    führe die bat-Datei ``build_folder_exe.bat`` aus, im Verzeichnis ``dist/almgis``
    wird das Ergebnis abgespeichert.
    Die Datei ``almgis_folder.spec`` wird für die erstellung der
    exe verwendet (siehe `Using Spec Files <https://pyinstaller.org/en/stable/spec-files.html>`_)

SqlAlchemy
__________
(siehe `SqlAlchemy <https://www.sqlalchemy.org/>`_)

SqlAlchemy ist ein Python ToolKit und 'Object Relational Mapper' (ORM).

In dem Modul ``data_model.py`` werden die entsprechenden Mapper-Klassen (MC) definiert.
Vereinfacht gesagt entspricht eine MC einer Tabelle in der Datenbank.
(siehe `Declare Models <https://docs.sqlalchemy.org/en/20/orm/quickstart.html#declare-models/>`_)

Mit "Sessions" werden Datenbank-Transaktionen durchgeführt.
(siehe `Using the Sessions <https://docs.sqlalchemy.org/en/20/orm/session.html>`_)

