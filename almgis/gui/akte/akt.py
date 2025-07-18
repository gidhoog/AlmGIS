import os

# from PyQt5.QtCore import QDate
from qgis.PyQt.QtGui import (QIntValidator, QIcon, QStandardItemModel)
from qgis.PyQt.QtWidgets import QDockWidget

from qgis.PyQt.QtCore import Qt, QModelIndex, pyqtSlot, QDate

from qgis.core import QgsLayoutExporter
from sqlalchemy import select, func
from sqlalchemy.orm import joinedload

from app_core import entity, LOGGER
from app_core.config import almgis_home_path
from app_core.data_model import BAkt, BBearbeitungsstatus, BGstZuordnung, BKontakt
from app_core.entity_titel import EntityTitel
from app_core.gis_item import GisItem
# from app_core.gis_layer import KoppelLayer, KomplexLayer
from app_core.gis_tools import cut_koppel_gstversion
from app_core.main_gis import MainGis
from app_core.scopes.prints.awb_auszug import AwbAuszug
from app_core.scopes.akte import akt_UI
from app_core.scopes.akte.akt_abgrenzung_dv import AbgrenzungDataView
from app_core.scopes.akte.akt_gst_main import GstAktDataView
from app_core.scopes.akte.akt_komplex_dv import KomplexAktDataView
from app_core.scopes.akte.akt_koppel_dv import KoppelAktDataView
from app_core.scopes.komplex.komplex_item import KomplexItem, AbgrenzungItem
from app_core.scopes.kontakt.kontakt import Kontakt, KontaktNewSelector
from app_core.scopes.koppel.koppel_item import KoppelItem


class Akt(akt_UI.Ui_Akt, entity.Entity):
    """
    baseclass für einen akt-datensatz
    """

    _bewirtschafter_id = 0
    _alm_bnr = 0
    _anm = ''
    _az = 0
    _alias = ''
    _name = ''
    _stz = ''
    _status_id = 0
    _status_mci = None
    _wwp = 0
    _wwp_exist = 0
    _wwp_date = ''
    _weidedauer = 0
    _max_gve = 0.0
    _nicht_bewirtschaftet = 0

    @property  # getter
    def bewirtschafter_id(self):

        self._bewirtschafter_id = self.uiBewirtschafterCombo.currentData(Qt.UserRole + 1)
        return self._bewirtschafter_id

    @bewirtschafter_id.setter
    def bewirtschafter_id(self, value):

        """finde den type_id im model des uiTypeCombo"""
        match_index = self.uiBewirtschafterCombo.model().match(
            self.uiBewirtschafterCombo.model().index(0, 0),
            Qt.UserRole + 1,
            value,
            -1,
            Qt.MatchExactly)
        """"""

        if match_index:

            self.uiBewirtschafterCombo.setCurrentIndex(match_index[0].row())
            self._bewirtschafter_id = value
        else:
            self._bewirtschafter_id = 0

    @property  # getter
    def bewirtschafter_mci(self):

        bewirtschafter_mci = self.uiBewirtschafterCombo.currentData(
            Qt.UserRole + 2)
        return bewirtschafter_mci

    @property  # getter
    def alm_bnr(self):

        if self.uiAlmBnrLedit.text() != '':
            self._alm_bnr = int(self.uiAlmBnrLedit.text())
        else:
            self._alm_bnr = ''
        return self._alm_bnr

    @alm_bnr.setter
    def alm_bnr(self, value):

        if value == 'None' or value == None:
            self._alm_bnr = ''
        else:
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

        self._az = value

    @property  # getter
    def name(self):

        return self._name

    @name.setter
    def name(self, value):

        self.uicTitleWdg.uiTitelLbl.setText(f'{value}   -   AZ {str(self.az)}')
        self._name = value

    @property  # getter
    def status_id(self):

        self._status_id = self.uiStatusCombo.currentData(Qt.UserRole + 1)
        return self._status_id

    @status_id.setter
    def status_id(self, value):

        """finde den status_id im model des uiStatusCombo"""
        match_index = self.uiStatusCombo.model().match(
            self.uiStatusCombo.model().index(0, 0),
            Qt.UserRole + 1,
            value,
            -1,
            Qt.MatchExactly)
        """"""

        if match_index:

            self.uiStatusCombo.setCurrentIndex(match_index[0].row())
            self._status_id = value
        else:
            self._status_id = 0

    @property  # getter
    def status_mci(self):

        status_mci = self.uiStatusCombo.currentData(Qt.UserRole)
        return status_mci

    @property  # getter
    def stz(self):

        return self._stz

    @stz.setter
    def stz(self, value):

        self.uiStzLbl.setText(value)
        self._stz = value

    @property  # getter
    def wwp(self):

        if self.uiWwpCkBox.isChecked():
            self._wwp = 1
        else:
            self._wwp = 0

        return self._wwp

    @wwp.setter
    def wwp(self, value):

        if value == 1:
            self.uiWwpCkBox.setCheckState(Qt.Checked)
        else:
            self.uiWwpCkBox.setCheckState(Qt.Unchecked)

        self._wwp = value

    @property  # getter
    def wwp_exist(self):

        if self.uiWwpExistCkBox.isChecked():
            self._wwp_exist = 1
        else:
            self._wwp_exist = 0

        return self._wwp_exist

    @wwp_exist.setter
    def wwp_exist(self, value):

        if value == 1:
            self.uiWwpExistCkBox.setCheckState(Qt.Checked)
        else:
            self.uiWwpExistCkBox.setCheckState(Qt.Unchecked)

        self._wwp_exist = value

    @property  # getter
    def wwp_date(self):

        date = self.uiWwpDateDedit.date()
        self._wwp_date = date.toString('yyyy-MM-dd')

        return self._wwp_date

    @wwp_date.setter
    def wwp_date(self, value):

        if value is not None and value != '':

            year = value[:4]
            month = value[5:7]
            day = value[8:]

            date = QDate(int(year), int(month), int(day))
            self.uiWwpDateDedit.setDate(date)

        self._wwp_date = value

    @property  # getter
    def weidedauer(self):

        self._weidedauer = self.uiWeidedauerSbox.value()

        return self._weidedauer

    @weidedauer.setter
    def weidedauer(self, value):

        try:
            self.uiWeidedauerSbox.setValue(value)
        except:
            LOGGER.warning("!!! --> Cannot set 'weidedauer' in Akt")

        self._weidedauer = value

    @property  # getter
    def max_gve(self):

        self._max_gve = self.uiGveDsbox.value()

        return self._max_gve

    @max_gve.setter
    def max_gve(self, value):

        try:
            self.uiGveDsbox.setValue(value)
        except:
            LOGGER.warning("!!! --> Cannot set 'max_gve' in Akt")

        self._max_gve = value

    @property  # getter
    def nicht_bewirtschaftet(self):

        if self.uiNichtBewirtschaftetCkBox.isChecked():
            self._nicht_bewirtschaftet = 1
        else:
            self._nicht_bewirtschaftet = 0

        return self._nicht_bewirtschaftet

    @nicht_bewirtschaftet.setter
    def nicht_bewirtschaftet(self, value):

        if value == 1:
            self.uiNichtBewirtschaftetCkBox.setCheckState(Qt.Checked)
        else:
            self.uiNichtBewirtschaftetCkBox.setCheckState(Qt.Unchecked)

        self._nicht_bewirtschaftet = value

    def __init__(self, parent=None):
        super(__class__, self).__init__(parent)
        self.setupUi(self)
        self.setupCodeUi()

        self._entity_mc = BAkt

        self.filter_koppel_from_abgr_string = ''
        self.filter_koppel_from_komplex_string = ''
        self.filter_komplex_from_abgr_string = ''

        """erlaube nur integer in uiAlmBnr"""
        onlyInt = QIntValidator()
        onlyInt.setRange(0, 99999999)
        self.uiAlmBnrLedit.setValidator(onlyInt)
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

        """setzte neuen slot für die add_action"""
        self.uiBewirtschafterCombo.action_add.triggered.disconnect()
        self.uiBewirtschafterCombo.action_add.triggered.connect(self.add_new_kontakt)
        """"""

    def prepareEntity(self):

        self.guiMainGis.setMaingisSession(self.entity_session)

    def add_new_kontakt(self):
        """
        lege einen neuen kontakt an
        :return:
        """

        self.kt = KontaktNewSelector(self)
        self.kt.show()

    def loadBackgroundData(self):
        super().loadBackgroundData()

        self.setStatusComboData()

        """init bewirtschafter_combo"""
        self.uiBewirtschafterCombo.loadComboData(self.entity_session)
        self.uiBewirtschafterCombo.combo_wdg_cls = Kontakt
        self.uiBewirtschafterCombo.initCombo()
        """"""

        self.uiInfoBtnAlmBnr.initInfoButton(1001)
        self.uiInfoBtnStatus.initInfoButton(1002)
        self.uiInfoBtnBewirtschafter.initInfoButton(1004)
        self.uiInfoBtnWwp.initInfoButton(1005)
        self.uiInfoBtnAlias.initInfoButton(1003)

    def setupCodeUi(self):
        super().setupCodeUi()

        """füge das Titel-Widget in die Titel-Toolbar ein"""
        self.uicTitleWdg = EntityTitel(self)
        self.uiTitleToolBar.addWidget(self.uicTitleWdg)

    def finalEntitySettings(self):
        super().finalEntitySettings()

        """stetze eine minimum widget-größe"""
        self.setMinimumWidth(1800)
        self.setMinimumHeight(900)
        """"""

        self.uiKkSplitter.setStretchFactor(1, 3)
        self.uiAbgrKkSplitter.setStretchFactor(1, 3)

        self.displayBewirtschafterAdresse()

        self.uiBewAwbAreaLbl.setText(self.getBewAwbArea())

        """durchsuche ob eine abgrenzung als 'awb' gesetzt ist und selektiere
        diese dann"""
        for feat in self.abgrenzung_table._gis_layer.getFeatures():
            if feat.attribute('awb') == 1:
                self.abgrenzung_table._gis_layer.select([feat.id()])
                self.abgrenzung_table.selectedRowsChanged()
                self.selectedAbgrenzungChanged()

        """trenne das signal des corner-buttons und entferne das icon"""
        self.abgrenzung_table.view.uiCornerButton.clicked.disconnect()
        self.abgrenzung_table.view.uiCornerButton.setStyleSheet("")
        """"""

    # def initEntityWidget(self):
    #     super().initEntityWidget()
    #
    #     self.setStatusComboData()
    #
    #     """init bewirtschafter_combo"""
    #     self.setBewirtschafterCombo()
    #     """"""
    #
    #     self.uiInfoBtnAlmBnr.initInfoButton(1001)
    #     self.uiInfoBtnStatus.initInfoButton(1002)
    #     self.uiInfoBtnBewirtschafter.initInfoButton(1004)
    #     self.uiInfoBtnWwp.initInfoButton(1005)
    #     self.uiInfoBtnAlias.initInfoButton(1003)

    def mapEntityData(self):
        super().mapEntityData()

        self.az = self._entity_mci.az
        self.name = self._entity_mci.name
        self.stz = self._entity_mci.stz

        self.alias = self._entity_mci.alias
        self.alm_bnr = self._entity_mci.alm_bnr
        self.anm = self._entity_mci.anm
        self.status_id = self._entity_mci.bearbeitungsstatus_id

        self.wwp = self._entity_mci.wwp
        self.wwp_exist = self._entity_mci.wwp_exist
        self.wwp_date = self._entity_mci.wwp_date

        self.weidedauer = self._entity_mci.weidedauer
        self.max_gve = self._entity_mci.max_gve

        self.nicht_bewirtschaftet = self._entity_mci.nicht_bewirtschaftet

        self.bewirtschafter_id = self._entity_mci.bewirtschafter_id

        self.loadSubWidgets()

    def displayBewirtschafterAdresse(self):

        bewirtschafter = self.uiBewirtschafterCombo.currentData(Qt.UserRole + 2)

        if bewirtschafter is None:

            self.uiBewirtschafterTypLbl.setText('')
            self.uiVertreterNameLbl.setText('')
            self.uiAdresseLbl.setText('')
            self.uiTelefonLbl.setText('')
            self.uiMailLbl.setText('')

            self.uiVertreterLbl.setVisible(False)
            self.uiVertreterNameLbl.setVisible(False)

        else:
            self.uiBewirtschafterTypLbl.setText(bewirtschafter.rel_type.name)

            if bewirtschafter.rel_type.gemeinschaft:

                self.uiVertreterLbl.setVisible(True)
                self.uiVertreterNameLbl.setVisible(True)

                self.uiVertreterNameLbl.setText(bewirtschafter.rel_vertreter.name)
                self.uiAdresseLbl.setText(bewirtschafter.rel_vertreter.adresse)
                self.uiTelefonLbl.setText(bewirtschafter.rel_vertreter.telefon_all)
                self.uiMailLbl.setText(bewirtschafter.rel_vertreter.mail_all)

            else:
                self.uiVertreterLbl.setVisible(False)
                self.uiVertreterNameLbl.setVisible(False)

                self.uiVertreterNameLbl.setText(bewirtschafter.name)
                self.uiAdresseLbl.setText(bewirtschafter.adresse)
                self.uiTelefonLbl.setText(bewirtschafter.telefon_all)
                self.uiMailLbl.setText(bewirtschafter.mail_all)

    def getEntityMci(self, session, entity_id):

        mci = session.scalars(
            select(BAkt)
            .options(joinedload(BAkt.rel_gst_zuordnung)
                     .joinedload(BGstZuordnung.rel_gst))
            .where(BAkt.id == entity_id)
        ).unique().first()

        return mci

    def getBewAwbArea(self):
        """
        erhalte die bewirtschaftete Fläche die für das awb gültig ist
        :return:
        """

        area = 0.0

        for abgrenzung in self._entity_mci.rel_abgrenzung:

            if abgrenzung.awb == 1:
                for komplex in abgrenzung.rel_komplex:
                    for koppel in komplex.rel_koppel:
                        area = area + koppel.koppel_area

        area_ha = '{:.4f}'.format(
            round(float(area) / 10000, 4)).replace(".", ",") + ' ha'
        return area_ha

    def loadSubWidgets(self):
        super().loadSubWidgets()

        """definiere notwendige tabellen und füge sie ein"""

        """lade die gst-tabelle"""
        self.gst_table = GstAktDataView(self, gis_mode=True)
        self.gst_table.setDataviewSession(self.entity_session)
        self.gst_table.initDataView()
        self.uiGstListeVlay.addWidget(self.gst_table)
        self.guiMainGis.project_instance.addMapLayer(self.gst_table._gis_layer)
        """"""

        """lade die abgrenzungen; wichtig ist hier, dass 'abgrenzung_table'
        als letztes instanziert wird (da hier die 'awb'-abgrenzung ausgewählt
        wird, und dazu muss zuerst koppel und komplex vorhanden sein"""
        self.abgrenzung_table = AbgrenzungDataView(self, gis_mode=True)
        self.abgrenzung_table.setDataviewSession(self.entity_session)
        self.abgrenzung_table.initDataView()

        self.komplex_table = KomplexAktDataView(self, gis_mode=True)
        self.komplex_table.setDataviewSession(self.entity_session)
        self.komplex_table.initDataView()

        self.koppel_table = KoppelAktDataView(self, gis_mode=True)
        self.koppel_table.setDataviewSession(self.entity_session)
        self.koppel_table.initDataView()

        self.uiAbgrenzungVlay.addWidget(self.abgrenzung_table)
        self.uiKomplexVlay.addWidget(self.komplex_table)
        self.uiKoppelVlay.addWidget(self.koppel_table)

        self.guiMainGis.project_instance.addMapLayer(self.koppel_table._gis_layer)
        self.guiMainGis.project_instance.addMapLayer(self.komplex_table._gis_layer)
        """"""

        """setzte die karte auf die ausdehnung des gst-layers"""
        self.gst_table._gis_layer.updateExtents()
        extent = self.gst_table._gis_layer.extent()
        self.guiMainGis.uiCanvas.setExtent(extent)
        """"""

    def selectedAbgrenzungChanged(self):

        print(f'---sel abgr changed---')

        for abgr_feat in self.abgrenzung_table._gis_layer.selectedFeatures():

            feat_id = abgr_feat.attribute('abgrenzung_id')
            print(f'abgrenzung_id: {feat_id}')
            self.filter_komplex_from_abgr_string = f"\"abgrenzung_id\" = {str(feat_id)}"
            self.filter_koppel_from_abgr_string = f"\"abgrenzung_id\" = {str(feat_id)}"

            self.komplex_table.useSubsetString()
            self.koppel_table.useSubsetString()

    def selectedKomplexChanged(self):

        print(f'---sel komplex changed---')

        if self.komplex_table._gis_layer.selectedFeatureCount() > 0:

            for komplex_feat in self.komplex_table._gis_layer.selectedFeatures():

                feat_id = komplex_feat.attribute('komplex_id')
                print(f'komplex_id: {feat_id}')
                self.filter_koppel_from_komplex_string = \
                    f"\"komplex_id\" = {str(feat_id)}"

        else:
            self.filter_koppel_from_komplex_string = ''

        self.koppel_table.useSubsetString()

    # def updateKomplexe(self):
    #     """
    #     temporäre und nur einmal verwendete funktion für den Import der Daten
    #     zum aktualisieren der Tabellenstruktur
    #
    #     :return:
    #     """
    #     alm_new = []
    #
    #     with session_cm() as session:
    #
    #         akt_instances = session.scalars(select(BAkt)
    #                                         .options(joinedload(BAkt.rel_abgrenzung)
    #                                                  .joinedload(BAbgrenzung.rel_komplex)
    #                                                  .joinedload(BKomplex.rel_koppel))
    #                                         ).unique().all()
    #
    #         for akt in akt_instances:
    #             akt_new = BAkt(name=akt.name,
    #                            alias=akt.alias,
    #                            az=akt.az,
    #                            bearbeitungsstatus_id=akt.bearbeitungsstatus_id,
    #                            alm_bnr=akt.alm_bnr,
    #                            anm=akt.anm,
    #                            stz=akt.stz)
    #             alm_new.append(akt_new)
    #             akt_abgrenzungen_new = {}
    #             for abgrenzung in akt.rel_abgrenzung:
    #
    #                 abgr_key = str(abgrenzung.jahr) + abgrenzung.bearbeiter + str(abgrenzung.erfassungsart_id)
    #
    #                 if abgr_key in akt_abgrenzungen_new:
    #                     abgr_new = akt_abgrenzungen_new[abgr_key]
    #                 else:
    #                     abgr_new = BAbgrenzung(akt_id=abgrenzung.akt_id,
    #                                            jahr=abgrenzung.jahr,
    #                                            bearbeiter=abgrenzung.bearbeiter,
    #                                            erfassungsart_id=abgrenzung.erfassungsart_id,
    #                                            status_id=abgrenzung.status_id,
    #                                            anmerkung=abgrenzung.anmerkung,
    #                                            inaktiv=abgrenzung.inaktiv)
    #                     akt_abgrenzungen_new[abgr_key] = abgr_new
    #                     akt_new.rel_abgrenzung.append(abgr_new)
    #
    #                 for komplex in abgrenzung.rel_komplex:
    #                     komplex_new = BKomplex(abgrenzung_id=komplex.abgrenzung_id,
    #                                            komplex_name_id=komplex.komplex_name_id)
    #                     abgr_new.rel_komplex.append(komplex_new)
    #
    #                     for koppel in komplex.rel_koppel:
    #                         koppel_new =BKoppel(komplex_id=koppel.komplex_id,
    #                                             nr=koppel.nr,
    #                                             name=koppel.name,
    #                                             nicht_weide=koppel.nicht_weide,
    #                                             bearbeiter=koppel.bearbeiter,
    #                                             seehoehe=koppel.seehoehe,
    #                                             domes_id=koppel.domes_id,
    #                                             heuertrag_ha=koppel.heuertrag_ha,
    #                                             anmerkung=koppel.anmerkung,
    #                                             geometry=koppel.geometry)
    #                         komplex_new.rel_koppel.append(koppel_new)
    #
    #             session.add(akt_new)
    #
    #         """aktiviere foreign_key-Support in der datenbank"""
    #         session.execute(text('pragma foreign_keys=ON'))
    #         """"""
    #
    #         """delete the farmitem (version) witch will be submitted (including deleting all
    #         children by using the cascaded 'delete' in the datamodel)"""
    #         for akt_inst in akt_instances:
    #             session.delete(akt_inst)
    #         """"""
    #
    #         """remove the sequence of the row-id's to begin at 1 on setting
    #         the new row-id """
    #         session.execute(text("""delete from sqlite_sequence where name='a_alm_akt';"""))
    #         """"""
    #
    #         session.commit()

    # def currentAbgenzungJahr(self):
    #     """
    #     erhalte das Referenzjahr der Abgrenzung aus den Daten des Item-Trees
    #     :return: Int
    #     """
    #
    #     jahre = []
    #
    #     for j in range(self.komplex_root_item.rowCount()):
    #         abgr_item = self.komplex_root_item.child(j)
    #         jahre.append(abgr_item.data(GisItem.Jahr_Role))
    #
    #     return max(jahre)

    # def loadKKModel(self):
    #
    #     def addKoppelFeature(koppel_item, koppel_layer):
    #
    #         koppel_feat = QgsFeature(koppel_layer.fields())
    #         koppel_feat.setAttributes(
    #             [koppel_item.data(GisItem.Instance_Role).id,
    #              koppel_item.data(GisItem.Name_Role),
    #              None,
    #              None,
    #              None,
    #              '0,123'])
    #         koppel_feat.setGeometry(QgsGeometry.fromWkt(
    #             to_shape(
    #                 koppel_item.data(GisItem.Geometry_Role)).wkt)
    #         )
    #         (result,
    #          added_kop_feat) = koppel_layer.data_provider.addFeatures(
    #             [koppel_feat])
    #
    #         return added_kop_feat
    #
    #     with session_cm() as session:
    #
    #         abgrenzungs_instances = session.scalars(select(BAbgrenzung)
    #                                 .where(BAbgrenzung.akt_id == self._entity_mci.id)
    #                                 .order_by(desc(BAbgrenzung.jahr))
    #                                                 ).unique().all()
    #
    #         for abgrenzung in abgrenzungs_instances:
    #
    #             abgrenzung_item = AbgrenzungItem(abgrenzung)
    #             self.komplex_root_item.appendRow(abgrenzung_item)
    #
    #             """erzeuge Layer für die Komplexe und Koppeln"""
    #             koppel_layer = KoppelLayer(
    #                 "Polygon?crs=epsg:31259",
    #                 "Koppeln " + str(abgrenzung.jahr),
    #                 "memory"
    #             )
    #             abgrenzung_item.setData(koppel_layer, GisItem.KoppelLayer_Role)
    #
    #             komplex_layer = KomplexLayer(
    #                 "Polygon?crs=epsg:31259",
    #                 "Komplexe " + str(abgrenzung.jahr),
    #                 "memory"
    #             )
    #             abgrenzung_item.setData(komplex_layer, GisItem.KomplexLayer_Role)
    #             """"""
    #
    #             for komplex in abgrenzung.rel_komplex:
    #
    #                 komplex_geom = None
    #
    #                 komplex_item = KomplexItem(komplex)
    #
    #                 """füge die items der einzelnen Spalten ein; Leerwerte als
    #                 Platzhalter, in der Funktion 'data()' des Models werden
    #                 dann die Werte für die Anzeige gesteuert"""
    #                 abgrenzung_item.appendRow([komplex_item,
    #                                            QStandardItem(),
    #                                            QStandardItem(),
    #                                            QStandardItem(),
    #                                            QStandardItem(),
    #                                            QStandardItem(),
    #                                            QStandardItem(),
    #                                            QStandardItem(),
    #                                            QStandardItem()])
    #                 """"""
    #
    #                 for koppel in komplex.rel_koppel:
    #
    #                     koppel_item = KoppelItem(koppel)
    #                     komplex_item.appendRow([koppel_item,
    #                                            QStandardItem(),
    #                                            QStandardItem(),
    #                                            QStandardItem(),
    #                                            QStandardItem(),
    #                                            QStandardItem(),
    #                                            QStandardItem(),
    #                                            QStandardItem(),
    #                                            QStandardItem()])
    #                     new_koppel_feat = addKoppelFeature(koppel_item, koppel_layer)
    #
    #                     koppel_item.setData(new_koppel_feat[0], GisItem.Feature_Role)
    #                     koppel_item.setData(koppel_layer, GisItem.Layer_Role)
    #
    #                     if komplex_geom == None:
    #                         komplex_geom = new_koppel_feat[0].geometry()
    #                     else:
    #                         komplex_geom = komplex_geom.combine(
    #                             new_koppel_feat[0].geometry())
    #
    #                 komplex_feat = QgsFeature(komplex_layer.fields())
    #
    #                 komplex_feat.setAttributes([
    #                     komplex_item.data(GisItem.Instance_Role).id,
    #                     1,
    #                     komplex_item.data(GisItem.Name_Role)
    #                 ])
    #
    #                 komplex_feat.setGeometry(komplex_geom)
    #
    #                 (result,
    #                  added_komp_feat) = komplex_layer.data_provider.addFeatures(
    #                     [komplex_feat])
    #
    #                 komplex_item.setData(added_komp_feat[0],
    #                                     GisItem.Feature_Role)
    #                 komplex_item.setData(komplex_layer, GisItem.Layer_Role)
    #
    #                 """füge die erstellten Layer in die Projekt-Instance ein
    #                 um einen gültigen Layer zu erhalten; in den Layer-Tree-View
    #                 wird er hier noch nicht eingefügt"""
    #                 self.guiMainGis.project_instance.addMapLayer(koppel_layer,
    #                                                              False)
    #
    #             self.guiMainGis.project_instance.addMapLayer(komplex_layer,
    #                                                          False)
    #             """"""

    # def setCurrentRoleToKK(self):
    #     """
    #     setze die 'Current_Role' der KK-Layerfür das erste Mal beim laden
    #     der Daten
    #
    #     :return:
    #     """
    #
    #     for abgr in range(self.komplex_root_item.rowCount()):
    #         abgr_item = self.komplex_root_item.child(abgr)
    #
    #         abgr_status = abgr_item.data(GisItem.StatusId_Role)
    #         abgr_jahr = abgr_item.data(GisItem.Jahr_Role)
    #
    #         if abgr_status == 0 and abgr_jahr == self.currentAbgenzungJahr():
    #             abgr_item.setData(1, GisItem.Current_Role)
    #             self.current_abgrenzung_item = abgr_item
    #         else:
    #             abgr_item.setData(0, GisItem.Current_Role)

    # def loadGisLayer(self):
    #     """hole die infos der zu ladenden gis-layer aus der datenbank und
    #     übergebe sie dem main_gis widget"""
    #
    #     """füge die Abgrenzungslayer ein (Komplex und Koppel)"""
    #     self.insertKKLayerToLTV()
    #     """"""
    #
    #     """setzte den base_id für das main_gis widget"""
    #     self.guiMainGis.base_id = self.entity_id
    #     """"""
    #
    #     """hole die daten für die gis-layer aus der datenbank"""
    #     with session_cm() as session:
    #         session.expire_on_commit = False
    #
    #         akt_gis_scope_layer = session.query(BGisScopeLayer)\
    #             .join(BGisStyle) \
    #             .outerjoin(BGisStyleLayerVar) \
    #             .filter(BGisScopeLayer.gis_scope_id == self.guiMainGis.scope_id)\
    #             .order_by(desc(BGisScopeLayer.order))\
    #             .all()
    #     """"""
    #
    #     """lade die gis-layer"""
    #     self.guiMainGis.loadLayer(akt_gis_scope_layer)

    def insertKKLayerToLTV(self):
        """
        füge die Abgrenzungslayer (Komplex und Koppel) in den LTV ein (befinden
        sich im komplex_model)

        :return: None
        """
        # test 03

        for a in range(self.komplex_root_item.rowCount()):
            abgr_item = self.komplex_root_item.child(a)
            komplex_layer = abgr_item.data(GisItem.KomplexLayer_Role)
            koppel_layer = abgr_item.data(GisItem.KoppelLayer_Role)

            if abgr_item.data(GisItem.Current_Role) == 1:
                komplex_layer.base = True
                self.guiMainGis.addLayer(komplex_layer, treeview_only=True)
                self.guiMainGis.addLayer(koppel_layer, treeview_only=True)
                koppel_layer.updateExtents()
                extent = koppel_layer.extent()
                self.guiMainGis.uiCanvas.setExtent(extent)
            else:
                self.guiMainGis.addLayer(komplex_layer,
                                         self.kk_gis_group,
                                         treeview_only=True)
                self.guiMainGis.addLayer(koppel_layer,
                                         self.kk_gis_group,
                                         treeview_only=True)

    def submitEntity(self):

        self._entity_mci.alias = self.alias
        self._entity_mci.alm_bnr = self.alm_bnr
        self._entity_mci.anm = self.anm
        self._entity_mci.bearbeitungsstatus_id = self.status_id
        self._entity_mci.rel_bearbeitungsstatus = self.status_mci

        self._entity_mci.wwp = self.wwp
        self._entity_mci.wwp_exist = self.wwp_exist
        self._entity_mci.wwp_date = self.wwp_date

        self._entity_mci.weidedauer = self.weidedauer
        self._entity_mci.max_gve = self.max_gve

        self._entity_mci.nicht_bewirtschaftet = self.nicht_bewirtschaftet

        self._entity_mci.bewirtschafter_id = self.bewirtschafter_id
        self._entity_mci.rel_bewirtschafter = self.bewirtschafter_mci

    def postDataSet(self):
        super().postDataSet()

        self.uiGisDock.setWindowTitle(
            f'Kartenansicht {self.name} (AZ {str(self.az)})')

    def setBewirtschafterCombo(self):

        bewirtschafter_stmt = select(
            BKontakt).order_by(func.lower(BKontakt.name)
                               )
        self.uiBewirtschafterCombo._mci_list = self.entity_session.scalars(
            bewirtschafter_stmt).all()

        """erstelle ein model mit 1 spalten für das type-combo"""
        bew_model = QStandardItemModel(len(self.uiBewirtschafterCombo._mci_list), 1)
        for i in range(len(self.uiBewirtschafterCombo._mci_list)):
            bew_model.setData(bew_model.index(i, 0),
                                          self.uiBewirtschafterCombo._mci_list[i].name, Qt.DisplayRole)
            bew_model.setData(bew_model.index(i, 0),
                                          self.uiBewirtschafterCombo._mci_list[i].id, Qt.UserRole + 1)
            bew_model.setData(bew_model.index(i, 0),
                                          self.uiBewirtschafterCombo._mci_list[i], Qt.UserRole + 2)
            print(f'----vertreter_mci_list[i]: {self.uiBewirtschafterCombo._mci_list[i]}')
        """"""

        """weise dem combo das model zu"""
        self.uiBewirtschafterCombo.setModel(bew_model)
        """"""

        self.uiBewirtschafterCombo.combo_wdg_cls = Kontakt
        self.uiBewirtschafterCombo.initCombo()

    def setStatusComboData(self):
        """
        hole die daten für die status_id-combobox aus der datenbank und füge sie in
        die combobox ein
        """

        status_stmt = select(BBearbeitungsstatus)
        status_mci_list = self.entity_session.scalars(status_stmt).all()

        """erstelle ein model mit 1 spalten für das type-combo"""
        status_model = QStandardItemModel(len(status_mci_list), 1)
        for i in range(len(status_mci_list)):
            status_model.setData(status_model.index(i, 0),
                                          status_mci_list[i].name, Qt.DisplayRole)
            status_model.setData(status_model.index(i, 0),
                                          status_mci_list[i].id, Qt.UserRole + 1)
            status_model.setData(status_model.index(i, 0),
                                          status_mci_list[i], Qt.UserRole)
        """"""

        """weise dem combo das model zu"""
        self.uiStatusCombo.setModel(status_model)
        """"""

    def signals(self):
        super().signals()

        self.uiGisDock.topLevelChanged.connect(self.changedGisDockLevel)
        self.actionAwbAuszug.triggered.connect(self.createAwbPrint)

        self.abgrenzung_table._gis_layer.selectionChanged.connect(
            self.selectedAbgrenzungChanged)

        self.komplex_table._gis_layer.selectionChanged.connect(
            self.selectedKomplexChanged)

        self.uiBewirtschafterCombo.currentIndexChanged.connect(
            self.displayBewirtschafterAdresse)

    def selectFeatures(self, feat_id_list):
        """
        Selektiere die Features auf dem aktiven Layer mittels der mitübergebenen
        FeatureID-Liste

        :param feat_id_list:
        :return:
        """

        """hebe eine bisherige Selektion auf"""
        self.guiMainGis.removeSelectedAll()
        """"""
        if feat_id_list != []:
            curr_layer = self.guiMainGis.layer_tree_view.currentLayer()
            curr_layer.select([f.id() for f in curr_layer.getFeatures() if f.id()
                               in feat_id_list])

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

    @pyqtSlot("QModelIndex", "QModelIndex", "QVector<int>")
    def changedKKModel(self, top_left, bottom_right, roles):
        """
        Slot um Änderungen im Model 'komplex_model' abzufangen und darauf zu
        reagieren

        :param top_left: QModelIndex
        :param bottom_right: QModelIndex
        :param roles: UserRole der Klasse GisItem
        :return: None
        """

        """verändertes item"""
        changed_item = self.komplex_model.itemFromIndex(top_left)
        """"""

        """das Jahr wird verändert und der Name des Layers im LayerTree wird
        daran angepasst"""
        if GisItem.Jahr_Role in roles:

            (changed_item.data(GisItem.KomplexLayer_Role)
             .setName(f'Komplexe {changed_item.data(GisItem.Jahr_Role)}'))
            (changed_item.data(GisItem.KoppelLayer_Role)
             .setName(f'Koppeln {changed_item.data(GisItem.Jahr_Role)}'))
        """"""

    def createAwbPrint(self):
        """
        erzeuge einen ausdruck mit den grundstücken dieses aktes die im
        alm- und weidebuch eingetragen sind inkl. einer karte dieser
        grundstücke
        """


        awb_auszug = AwbAuszug(akt_instance=self._entity_mci)
        print(f'create AWB')

        """erzeuge eine pdf-Datei"""
        exporter = QgsLayoutExporter(awb_auszug)
        pdf_settings = exporter.PdfExportSettings()
        # pdf_file = str(Path().absolute().joinpath('data', '__AWB-Auszug.pdf'))
        pdf_file = str(almgis_home_path.joinpath('__AWB-Auszug.pdf'))
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

        self.gst_table.updateMaintable()

    def updateAkt(self):

        """führe den verschnitt komplexe und gst-version durch"""
        current_koppel_layer = self.current_abgrenzung_item.data(GisItem.KoppelLayer_Role)
        cut_koppel_gstversion(current_koppel_layer)
        """"""

        """update canvas"""
        self.guiMainGis.uiCanvas.update()
        self.guiMainGis.uiCanvas.refresh()
        """"""

        """aktualisiere die tabellen"""
        self.gst_table.updateMaintable()
        """"""


class GisDock(QDockWidget):
    """
    baseclass für das GisDock in der klasse 'Akt'
    """

    def __init__(self, parent):
        super(__class__, self).__init__(parent)

        self.setWindowTitle('Kartenansicht')


class KomplexModel(QStandardItemModel):

    def __init__(self, parent=None) -> None:
        super(KomplexModel, self).__init__(parent)

        self.parent = parent

        self.setColumnCount(5)
        self.setHorizontalHeaderLabels(['Komplex-/Koppelname',  # 0
                                        'ab Jahr',  # 1
                                        'Status',  # 2
                                        'Erfassungsart',  # 3
                                        'Bearbeiter',  # 4
                                        'Nr',  # 5
                                        'nicht Weide',  # 6
                                        'Komplexfläche',  # 7
                                        'Koppelfläche'])  # 8

    def flags(self, index):

        first_index = index.sibling(index.row(), 0)
        first_item = self.itemFromIndex(first_index)

        if type(first_item) == KomplexItem:

            return Qt.ItemIsEnabled
        else:
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def data(self, index: QModelIndex, role: int = ...):

        item = self.itemFromIndex(index)

        """erstelle eine Liste mit den Jahren der Abgrenzungen, um später das
        aktuelle Jahr zu markieren"""
        year_list = []
        for abgr_jahr in range(self.invisibleRootItem().rowCount()):
            year_list.append(self.invisibleRootItem().child(abgr_jahr).data(GisItem.Jahr_Role))

        """get the item of the first column if you are in an other"""
        if index.column() != 0:
            first_index = index.sibling(index.row(), 0)
            first_item = self.itemFromIndex(first_index)
        """"""

        if not index.isValid():
            return None

        if index.column() == 0:

            if type(item) == AbgrenzungItem:
                year_list.append(item.data(GisItem.Jahr_Role))

                if role == Qt.DisplayRole:
                    return item.data(GisItem.Jahr_Role)

            else:

                if role == Qt.DisplayRole:
                    return item.data(GisItem.Name_Role)

                if role == Qt.EditRole:
                    return item.data(GisItem.Name_Role)

                if role == Qt.DecorationRole:

                    if type(item) != AbgrenzungItem:

                        return item.data(GisItem.Color_Role)

        if index.column() == 1:

            if type(first_item) == AbgrenzungItem:
                if role == Qt.DisplayRole:
                    return first_item.data(GisItem.Jahr_Role)
                if role == Qt.DecorationRole:
                    """zeige ein grünes Dreieck bei der aktuellen Abgrenzung"""
                    # if first_item.data(GisItem.Current_Role) == 1:  # aktuell
                    if first_item.data(GisItem.Jahr_Role) == max(year_list):  # aktuell
                        first_item.setData(1, GisItem.Current_Role)
                        self.parent.current_abgrenzung_item = first_item
                        print(f'--> set current layer')
                        return QIcon(":/svg/icons/triangle_right_green.svg")
                    # if first_item.data(GisItem.Current_Role) == 0:
                    else:
                        first_item.setData(0, GisItem.Current_Role)
                        return QIcon(":/svg/icons/_leeres_icon.svg")
                    """"""

        if index.column() == 2:  # status_id

            if type(first_item) == AbgrenzungItem:
                if role == Qt.DisplayRole:
                    return first_item.data(GisItem.StatusName_Role)
                if role == Qt.TextAlignmentRole:
                    return Qt.AlignHCenter | Qt.AlignVCenter

        if index.column() == 3:

            if type(first_item) == AbgrenzungItem:
                if role == Qt.DisplayRole:
                    return first_item.data(GisItem.ErfassungsArtName_Role)

        if index.column() == 4:

            if type(first_item) == AbgrenzungItem:
                if role == Qt.DisplayRole:
                    return first_item.data(GisItem.Bearbeiter_Role)

        if index.column() == 5:

            if type(first_item) == KoppelItem:
                if role == Qt.DisplayRole:
                    return first_item.data(GisItem.Nr_Role)
                if role == Qt.TextAlignmentRole:
                    return Qt.AlignHCenter | Qt.AlignVCenter

        if index.column() == 6:  # nicht Weide

            if type(first_item) == KoppelItem:
                if role == Qt.DisplayRole:
                    nw = first_item.data(GisItem.NichtWeide_Role)
                    if nw == 1:
                        return 'X'
                if role == Qt.TextAlignmentRole:
                    return Qt.AlignHCenter | Qt.AlignVCenter

        if index.column() == 7:

            if type(first_item) == KomplexItem:

                if role == Qt.DisplayRole:
                    area = first_item.data(GisItem.Feature_Role).geometry().area()
                    area_r = '{:.4f}'.format(round(float(area) / 10000, 4)).replace(".", ",")
                    return area_r +  ' ha'
                if role == Qt.TextAlignmentRole:
                    return Qt.AlignRight | Qt.AlignVCenter

        if index.column() == 8:

            if type(first_item) == KoppelItem:

                if role == Qt.DisplayRole:
                    area = first_item.data(GisItem.Feature_Role).geometry().area()
                    area_r = '{:.4f}'.format(round(float(area) / 10000, 4)).replace(".", ",")
                    return area_r +  ' ha'
                if role == Qt.TextAlignmentRole:
                    return Qt.AlignRight | Qt.AlignVCenter

        return QStandardItemModel.data(self, index, role)
