# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

# von binaries: ('C:/work/_anwendungen/OSGeo4W/apps/qgis-ltr/python/qgis/_core.pyd', './qgis')
#               ('C:/work/_anwendungen/OSGeo4W/apps/qgis-ltr/bin/qgis_core.dll', './dll')

a = Analysis(
    ['almgis.py'],
    pathex=[],
    binaries=[
    ('C:/work/Projekte/AlmGIS/_internal/dll/mod_spatialite.dll', './dll')
    ],
    datas=[
    ('almgis.cmd', '.'),
    ('C:/work/Projekte/AlmGIS/_internal/print_layouts/', './print_layouts'),
    ('C:/work/Projekte/AlmGIS/_internal/print_templates/', './print_templates'),
    ('C:/work/Projekte/AlmGIS/_internal/styles/', './styles'),
    ('C:/work/_anwendungen/OSGeo4W/share/proj/proj.db','./proj_db'),
    ('C:/work/_anwendungen/OSGeo4W/apps/qgis-ltr/python/plugins/processing/', './processing'),
    ('C:/work/Projekte/QGA/qga/', './qga')
    ],
    hiddenimports=[
    'sqlalchemy', 'shapely._geos', 'pkgutil', 'PyQt5.QtPositioning',
    'PyQt5.QtPrintSupport', 'PyQt5.QtSql', 'PyQt5.QtNetwork', 'PyQt5.QtXml',
    'PyQt5.Qsci', 'PyQt5.sip', 'PyQt5.QtMultimedia', 'PyQt5.QtSerialPort',
    'sqlalchemy_serializer', 'qgis.PyQt.QtSvg', 'html.parser'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['PyQt6'
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
          pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='almgis',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True,
          disable_windowed_traceback=False,
          argv_emulation=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None,
)
coll = COLLECT(
               exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='almgis'
)
