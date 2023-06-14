import os
from pathlib import Path

from PyQt5.QtGui import QFont, QIntValidator, QIcon
from PyQt5.QtWidgets import QLabel, QSpacerItem, QDockWidget, QToolButton, \
    QMenu, QAction
from PyQt5.QtCore import Qt, QSize
from qgis.PyQt import QtWidgets
from qgis.core import QgsLayoutExporter
from sqlalchemy import desc

from core import entity, DbSession
from core.data_model import BAkt, BBearbeitungsstatus, BGisStyle, \
    BGisScopeLayer, BGisStyleLayerVar
from core.gis_control import GisControl
from core.gis_tools import cut_koppel_gstversion
from core.main_gis import MainGis
from core.print_layouts.awb_auszug import AwbAuszug
from core.scopes.akte import akt_UI
from core.scopes.akte.akt_gst_main import GstMaintable
from core.scopes.akte.akt_komplexe_main import KomplexMaintable


class Akt(akt_UI.Ui_Akt, entity.Entity, GisControl):
    """
    baseclass für einen akt-datensatz
    """

    data_class = BAkt

    _alm_bnr = 0
    _anm = ''
    _az = 0
    _alias = ''
    _name = ''
    _stz = ''
    _status = 0

    @property  # getter
    def alm_bnr(self):

        self._alm_bnr = int(self.uiAlmBnrLedit.text())
        return self._alm_bnr

    @alm_bnr.setter
    def alm_bnr(self, value):

        self.uiAlmBnrLedit.setText(str(value))
        self._alm_bnr = value

    @property  # getter
    def alias(self):

        self._alias = self.uiAliasLedit.text()
        return self._alias

    @alias.setter
    def alias(self, value):

        self.uiAliasLedit.setText(value)
        self._alias = value

    @property  # getter
    def anm(self):

        self._anm = self.uiAnmTedit.toPlainText()
        return self._anm

    @anm.setter
    def anm(self, value):

        self.uiAnmTedit.setText(str(value))
        self._anm = value

    @property  # getter
    def az(self):

        return self._az

    @az.setter
    def az(self, value):

        self.uicAzLbl.setText(f'AZ {str(value)}')
        self._az = value

    @property  # getter
    def name(self):

        return self._name

    @name.setter
    def name(self, value):

        self.guiHeaderTextLbl.setText(value)
        self._name = value

    @property  # getter
    def status(self):

        self._status = self.uiStatusCombo.currentData(Qt.UserRole)
        return self._status

    @status.setter
    def status(self, value):

        self.uiStatusCombo.setCurrentIndex(
            self.uiStatusCombo.findData(value, Qt.UserRole)
        )
        self._status = value

    @property  # getter
    def stz(self):

        return self._stz

    @stz.setter
    def stz(self, value):

        self.uiStzLbl.setText(value)
        self._stz = value

    def __init__(self, parent=None):
        super(__class__, self).__init__(parent)
        self.setupUi(self)

        """erlaube nur integer in uiAlmBnr"""
        onlyInt = QIntValidator()
        onlyInt.setRange(0, 99999999)
        self.uiAlmBnrLedit.setValidator(onlyInt)
        """"""

        """lade die einträge für das status-combo"""
        self.setStatusComboData()
        """"""

        """erzeuge ein main_gis widget und füge es in ein GisDock ein"""
        self.uiGisDock = GisDock(self)
        self.guiMainGis = MainGis(self.uiGisDock, self)
        self.addDockWidget(Qt.RightDockWidgetArea, self.uiGisDock)
        self.uiGisDock.setWidget(self.guiMainGis)
        """"""

        """setzte den 'scope_id'; damit die richtigen layer aus dem 
        daten_model 'BGisScopeLayer' für dieses main_gis widget geladen werden"""
        self.guiMainGis.scope_id = 1
        """"""

        """definiere notwendige tabellen und füge sie ein"""
        self.gst_table = GstMaintable(self)
        self.uiGstListeVlay.addWidget(self.gst_table)

        self.komplex_table = KomplexMaintable(self)
        self.uiKomplexeGisListeVlay.addWidget(self.komplex_table)
        """"""

    def finalInit(self):
        super().finalInit()

        """stetze eine minimum widget-größe"""
        self.setMinimumWidth(1800)
        self.setMinimumHeight(900)
        """"""

        """stelle eine relation von gis-layern und datentabellen her und
        aktiviere die überwachung dieser relation"""
        # self.linked_gis_widgets[99] = self.gst_table
        # self.linked_gis_widgets[104] = self.komplex_table
        # self.activateGisControl()
        """"""

    def mapData(self):
        super().mapData()

        self.name = self.data_instance.name
        self.az = self.data_instance.az
        self.stz = self.data_instance.stz

        self.alias = self.data_instance.alias
        self.alm_bnr = self.data_instance.alm_bnr
        self.anm = self.data_instance.anm
        self.status = self.data_instance.bearbeitungsstatus_id

        self.guiMainGis.entity_id = self.data_instance.id

        # self.loadGisLayer()

    def loadSubWidgets(self):
        super().loadSubWidgets()

        # self.gst_table.initMaintable(self.session)
        # self.komplex_table.initMaintable(self.session)

        self.loadGisLayer()

    def loadGisLayer(self):
        """hole die infos der zu ladenden gis-layer aus der datenbank und
        übergebe sie dem main_gis widget"""

        """setzte den base_id für das main_gis widget"""
        self.guiMainGis.base_id = self.entity_id
        """"""

        """hole die daten für die gis-layer aus der datenbank"""
        with DbSession.session_scope() as session:
            session.expire_on_commit = False

            akt_gis_scope_layer = session.query(BGisScopeLayer)\
                .join(BGisStyle) \
                .outerjoin(BGisStyleLayerVar) \
                .filter(BGisScopeLayer.gis_scope_id == self.guiMainGis.scope_id)\
                .order_by(desc(BGisScopeLayer.order))\
                .all()
        """"""

        """lade die gis-layer"""
        self.guiMainGis.loadLayer(akt_gis_scope_layer)

    def submitEntity(self):

        self.data_instance.alias = self.alias
        self.data_instance.alm_bnr = self.alm_bnr
        self.data_instance.anm = self.anm
        self.data_instance.bearbeitungsstatus_id = self.status

        super().submitEntity()

    def post_data_set(self):
        super().post_data_set()

        self.uiGisDock.setWindowTitle(
            f'Kartenansicht {self.name} (AZ {str(self.az)})')

        self.tool_menu = QMenu(self)
        self.uicEntityTools.setMenu(self.tool_menu)

        self.menu_prints = QMenu('Ausdrucke')
        self.tool_menu.addMenu(self.menu_prints)

        self.actionPrintAWB = QAction('NÖ Alm- und Weidebuch Auszug')
        self.menu_prints.addAction(self.actionPrintAWB)

        self.actionPrintAktInfo = QAction('allgemeine Akteninformation')
        self.menu_prints.addAction(self.actionPrintAktInfo)
        self.actionPrintAktInfo.setEnabled(False)

        self.actionPrintGstList = QAction('Grundstücksliste')
        self.menu_prints.addAction(self.actionPrintGstList)
        self.actionPrintGstList.setEnabled(False)

    def insertEntityHeader(self):
        super().insertEntityHeader()

        self.uicAzLbl = QLabel(self)
        az_label_font = QFont("Verdana", 10, QFont.Bold)
        self.uicAzLbl.setStyleSheet(self.header_label_style)
        self.uicAzLbl.setFont(az_label_font)
        spacer = QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding,
                             QtWidgets.QSizePolicy.Minimum)
        self.uiHeaderHlay.addItem(spacer)
        self.uiHeaderHlay.insertWidget(2, self.uicAzLbl)

        self.uicEntityTools = QToolButton(self)
        self.uicEntityTools.setIcon(
            QIcon(':/svg/resources/icons/hamburger.svg'))
        self.uicEntityTools.setIconSize(QSize(30, 30))
        self.uicEntityTools.setFocusPolicy(Qt.NoFocus)
        self.uicEntityTools.setPopupMode(QToolButton.InstantPopup)
        self.uiHeaderMainHlay.insertWidget(1, self.uicEntityTools)

    def setStatusComboData(self):
        """
        hole die daten für die status-combobox aus der datenbank und füge sie in
        die combobox ein
        """

        with DbSession.session_scope() as session:
            status_items = session.query(BBearbeitungsstatus).\
                order_by(BBearbeitungsstatus.sort).\
                all()

        for item in status_items:
            self.uiStatusCombo.addItem(item.name, item.id)

    def signals(self):
        super().signals()

        self.uiGisDock.topLevelChanged.connect(self.changedGisDockLevel)
        self.actionPrintAWB.triggered.connect(self.createAwbPrint)


    def changedGisDockLevel(self, level):
        """
        überwache den level des GisDock; zeige die schaltfläche 'uiUnfloatDock'
        nur wenn es losgelöst ist
        """
        if level:
            self.uiGisDock.setWindowFlags(Qt.CustomizeWindowHint |
                                          Qt.Window |
                                          Qt.WindowMinimizeButtonHint |
                                          Qt.WindowMaximizeButtonHint |
                                          Qt.WindowCloseButtonHint)
            self.uiGisDock.widget().uiUnfoatDock.setVisible(True)
            self.uiGisDock.show()
        else:
            self.uiGisDock.widget().uiUnfoatDock.setVisible(False)

    def createAwbPrint(self):
        """
        erzeuge einen ausdruck mit den grundstücken dieses aktes die im
        alm- und weidebuch eingetragen sind inkl. einer karte dieser
        grundstücke
        """

        awb_auszug = AwbAuszug(akt_instance=self.data_instance)

        """erzeuge eine pdf-Datei"""
        exporter = QgsLayoutExporter(awb_auszug)
        pdf_settings = exporter.PdfExportSettings()
        pdf_file = str(Path().absolute().joinpath('data', '__AWB-Auszug.pdf'))
        exporter.exportToPdf(pdf_file, pdf_settings)
        """"""

        """öffne die pdf datei"""
        os.startfile(pdf_file)
        """"""

    def onGisEdit(self):
        """
        führe diese methode aus, wenn ein feature hinzugefügt oder verändert
        wird
        """

        self.komplex_table.updateMaintable()
        self.gst_table.updateMaintable()

    def updateAkt(self):

        """führe den verschnitt komplexe und gst-version durch"""
        cut_koppel_gstversion()
        """"""

        """update canvas"""
        self.guiMainGis.uiCanvas.update()
        self.guiMainGis.uiCanvas.refresh()
        """"""

        """aktualisiere die tabellen"""
        self.komplex_table.updateMaintable()
        self.gst_table.updateMaintable()
        """"""


class GisDock(QDockWidget):
    """
    baseclass für das GisDock in der klasse 'Akt'
    """

    def __init__(self, parent):
        super(__class__, self).__init__(parent)

        self.setWindowTitle('Kartenansicht')
