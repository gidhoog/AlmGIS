import sys
from _operator import attrgetter

from qgis.PyQt.QtCore import Qt, QModelIndex, QAbstractTableModel, QVariant
from qgis.PyQt.QtGui import QColor
from qgis.PyQt.QtWidgets import (QLabel, QComboBox, QDialog, QLineEdit,
                                 QSpacerItem, QSizePolicy, QHBoxLayout)
from qgis.core import QgsGeometry, QgsField

from sqlalchemy import func, select
from sqlalchemy.orm import joinedload

from core import db_session_cm, config
from core.data_model import BAkt, BKomplex, BGstZuordnung, BGst, BGstVersion, \
    BGstEz, BCutKoppelGstAktuell, BBearbeitungsstatus, BAbgrenzung, \
    BGstAwbStatus
from core.entity import EntityDialog
from core.data_view import DataView, TableModel, TableView, GisTableModel
from core.filter_element import FilterElement
from core.gis_layer import ZVectorLayer, Feature
from core.main_widget import MainWidget
from core.scopes.akte.akt import Akt


class AktDialog(EntityDialog):
    """
    dialog für die anzeige einer grundstückszuordnung
    """

    def __init__(self, parent):
        super(__class__, self).__init__(parent)

        # self.parent = parent
        #
        # self.enableApply = True

        self.dialog_window_title = 'Alm- und Weidebuchakt'
        # self.set_apply_button_text('&Speichern und Schließen')


    def accept(self):
        super().accept()

        if self.dialogWidget.acceptEntity() is not None:

            new_mci = self.dialogWidget.acceptEntity()

            self.parent.updateMaintableNew(self.dialogWidget.purpose, new_mci)

        QDialog.accept(self)


# class AkteAllMainTableModel(GisTableModel):
#
#     def __init__(self, layerCache, parent=None):
#         super(__class__, self).__init__(layerCache, parent)
#
#     def data(self, index: QModelIndex, role: int = ...):
#
#         """
#         erzeuge ein basis-model
#         """
#         row = index.row()
#         # col = index.column()
#         #
#         if role == Qt.TextAlignmentRole:
#
#             # if index.column() in [2, 6, 7, 8, 9]:
#             #
#             #     return Qt.AlignRight | Qt.AlignVCenter
#
#             if index.column() in [1, 6, 7, 8]:
#
#                 return Qt.AlignHCenter | Qt.AlignVCenter
#
#         if role == Qt.BackgroundRole:
#             if index.column() == 4:
#
#                 color_str = self.feature(index).attribute('status_color')
#                 color_list = color_str.split(", ")
#
#                 return QColor(int(color_list[0]),
#                               int(color_list[1]),
#                               int(color_list[2]))
#                 # status_id = self.feature('status_id')
#                 # if status_id == 'eingetragen':
#                 #     return QColor(189, 239, 255)
#                 # if status_id == 'nicht eingetragen':
#                 #     return QColor(234, 216, 54)
#                 # if status_id == 'gelöscht':
#                 #     return QColor(234, 163, 165)
#                 # if status_id == 'historisch':
#                 #     return QColor(170, 170, 170)
#
#         if index.column() == 7:
#
#             if role == Qt.DisplayRole:
#
#                 if self.feature(index).attribute('wwp') == 1:
#
#                     return 'X'
#
#                 else:
#                     return ''
#
#         if index.column() == 8:
#
#             if role == Qt.DisplayRole:
#
#                 return str(self.feature(index).attribute('wwp_jahr'))
#
#         if index.column() == 9:
#
#             if role == Qt.DisplayRole:
#
#                 area = self.feature(index).attribute('awb_area_gb')
#                 area_r = '{:.4f}'.format(round(float(area) / 10000, 4)).replace(
#                     ".", ",")
#                 return area_r + ' ha'
#
#         if index.column() == 10:
#
#             if role == Qt.DisplayRole:
#
#                 area = self.feature(index).attribute('awb_area_beweidet')
#                 area_r = '{:.4f}'.format(round(float(area) / 10000, 4)).replace(
#                     ".", ",")
#                 return area_r + ' ha'
#
#         if index.column() == 11:
#
#             if role == Qt.DisplayRole:
#
#                 area = self.feature(index).attribute('weide_area')
#                 area_r = '{:.4f}'.format(round(float(area) / 10000, 4)).replace(
#                     ".", ",")
#                 return area_r + ' ha'
#
#         # if index.column() == 7:
#         #
#         #     val = self.layer().getFeature(index.row()+1).geometry().area()
#         #
#         #     if role == Qt.DisplayRole:
#         #
#         #         # attr = self.layer().getFeature(index.row()+1).attributes()[index.column()]
#         #
#         #         print(f'val: {val}')
#         #         # return self.mci_list[row].rel_gst.gst
#         #         return val
#         #
#         #     if role == Qt.DisplayRole:
#         #
#         #         return val
#
#         return super().data(index, role)


class AkteAllMainWidget(MainWidget):
    """
    MainWidget für die Darstellung eines DataView's mit allen Akten
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self.uiTitleLbl.setText('alle Akte')

        self.akt_all_table = AkteAllMain(self)

        with db_session_cm(name='main-widget - akte alle',
                           expire_on_commit=False) as session:
            self.akt_all_table.initDataView(dataview_session=session)

    def initMainWidget(self):
        super().initMainWidget()

        self.uiMainVLay.addWidget(self.akt_all_table)

        # self.akt_all_table.loadData()
        # self.akt_all_table.initDataView()


class AktAllModel(TableModel):

    header = ['AZ',
              'Name',
              'Status',
              'Stz',
              'Anmerkung',
              'WWP',
              'WWP-Jahr',
              'AWB-Fläche (GB)',
              'davon beweidet',
              'Weidefläche']

    def data(self, index: QModelIndex, role: int = ...):

        """
        erzeuge ein basis-model
        """
        row = index.row()
        col = index.column()

        if role == Qt.TextAlignmentRole:

            if index.column() in [7, 8, 9]:

                return Qt.AlignRight | Qt.AlignVCenter

            if index.column() in [0, 2, 3, 5, 6]:

                return Qt.AlignHCenter | Qt.AlignVCenter

        if role == Qt.BackgroundRole:

            if index.column() == 2:

                if self.mci_list[row].rel_bearbeitungsstatus is not None:

                    color_str = self.mci_list[row].rel_bearbeitungsstatus.color
                    color_list = color_str.split(", ")

                    return QColor(int(color_list[0]),
                                  int(color_list[1]),
                                  int(color_list[2]))


        if index.column() == 0:
            if role == Qt.DisplayRole:
                return self.mci_list[row].az
            # if role == Qt.EditRole:
            #     return self.parent._mci_list[row].az

        if index.column() == 1:
            if role == Qt.DisplayRole:
                return self.mci_list[row].name
            # if role == Qt.EditRole:
            #     return self.mci_list[row].name

        if index.column() == 2:

            if self.mci_list[row].rel_bearbeitungsstatus is not None:

                if role == Qt.DisplayRole:
                    return self.mci_list[row].rel_bearbeitungsstatus.name

        if index.column() == 3:
            if role == Qt.DisplayRole:
                return self.mci_list[row].stz

        if index.column() == 4:
            if role == Qt.DisplayRole:
                return self.mci_list[row].anm

        if index.column() == 5:
            if role == Qt.DisplayRole:
                if self.mci_list[row].wwp == 1:
                    return 'X'

        if index.column() == 6:
            if role == Qt.DisplayRole:
                if self.mci_list[row].wwp == 1:
                    if self.mci_list[row].wwp_jahr is not None:
                        return self.mci_list[row].wwp_jahr
                    else:
                        return '---'
                return ''

        if index.column() == 7:  # im awb eingetragene flaeche
            # anz = 0
            gst_area = 0
            for gst_zuord in self.mci_list[row].rel_gst_zuordnung:
                # anz += 1
                if gst_zuord.awb_status_id == 1:
                    gst_versionen_list = gst_zuord.rel_gst.rel_alm_gst_version
                    last_gst = max(gst_versionen_list,
                                   key=attrgetter('rel_alm_gst_ez.datenstand'))
                    # print(f'last gst: {last_gst.import_time}')
                    gst_m = 0
                    for ba in last_gst.rel_alm_gst_nutzung:
                        gst_m = gst_m + ba.area
                    gst_area = gst_area + gst_m

            if role == Qt.DisplayRole:
                gst_area_ha = '{:.4f}'.format(round(float(gst_area) / 10000, 4)).replace(".", ",") + ' ha'
                return gst_area_ha
            if role == Qt.EditRole:
                return gst_area

        if index.column() == 8:  # davon beweidet

            cut_area = 0
            for gst_zuord in self.mci_list[row].rel_gst_zuordnung:
                # anz += 1
                if gst_zuord.awb_status_id == 1:
                    gst_versionen_list = gst_zuord.rel_gst.rel_alm_gst_version
                    last_gst = max(gst_versionen_list,
                                   key=attrgetter('rel_alm_gst_ez.datenstand'))

                    for cut in last_gst.rel_cut_koppel_gst:
                        cut_area = cut_area + last_gst.rel_cut_koppel_gst.cutarea
                    # print(f'last gst: {last_gst.import_time}')
                    # gst_m = 0
                    # for ba in last_gst.rel_alm_gst_nutzung:
                    #     gst_m = gst_m + ba.area
                    # gst_area = gst_area + gst_m

            if role == Qt.DisplayRole:
                cut_area_ha = '{:.4f}'.format(round(float(cut_area) / 10000, 4)).replace(".", ",") + ' ha'
                return cut_area_ha

        if index.column() == 9:  # weideflaeche

            if role in [Qt.DisplayRole, Qt.EditRole]:

                kop_area = 0.00

                # print(f'self.mci_list[row].rel_abgrenzung: {self.mci_list[row].rel_abgrenzung}')

                if self.mci_list[row].rel_abgrenzung != []:

                    last_abgrenzung = max(self.mci_list[row].rel_abgrenzung,
                                      key=attrgetter('jahr'))

                    for komplex in last_abgrenzung.rel_komplex:
                        for koppel in komplex.rel_koppel:
                            kop_area = kop_area + koppel.koppel_area

                    if role == Qt.DisplayRole:
                        kop_area_ha = '{:.4f}'.format(
                            round(float(kop_area) / 10000, 4)).replace(".",
                                                                       ",") + ' ha'
                        return kop_area_ha
                    if role == Qt.EditRole:
                        return kop_area

                else:
                    if role == Qt.DisplayRole:
                        return '---'
                    if role == Qt.EditRole:
                        return 0


class AkteAllMain(DataView):

    # entity_widget_class = Akt
    # _entity_mc = BAkt

    # entity_dialog_class = AktDialog

    # _model_class = AktAllModel

    _maintable_text = ["Akt", "Akte", "kein Akt"]
    _delete_window_title = ["Akt löschen", "Akte löschen"]
    _delete_window_text_single = "Soll der ausgewählte Akt " \
                                 "wirklich gelöscht werden?"
    _delete_window_text_plural = ["Sollen die ausgewählten",
                                  "Akte wirklich gelöscht werden?"]


    # _main_table_model_class = AktAllModel
    # _gis_table_model_class = AkteAllMainTableModel

    # """verfügbare filter für diese tabelle"""
    # _available_filters = 'gs'
    # """"""

    def get_weide_area(self, mci):
        weide_area = 0.00
        if mci.rel_abgrenzung != []:
            last_abgrenzung = max(mci.rel_abgrenzung,
                                  key=attrgetter('jahr'))
            for komplex in last_abgrenzung.rel_komplex:
                for koppel in komplex.rel_koppel:
                    weide_area = weide_area + koppel.koppel_area

        return weide_area

    def get_awb_gb_area(self, mci):

        awb_area = 0
        for gst_zuord in mci.rel_gst_zuordnung:

            if gst_zuord.awb_status_id == 1:
                gst_versionen_list = gst_zuord.rel_gst.rel_alm_gst_version
                last_gst = max(gst_versionen_list,
                               key=attrgetter('rel_alm_gst_ez.datenstand'))

                gst_nutz_area = 0
                for ba in last_gst.rel_alm_gst_nutzung:
                    gst_nutz_area = gst_nutz_area + ba.area
                awb_area = awb_area + gst_nutz_area
        return awb_area

    def get_awb_beweidet(self, mci):

        awb_beweidet_area = 0
        for gst_zuord in mci.rel_gst_zuordnung:

            if gst_zuord.awb_status_id == 1:
                gst_versionen_list = gst_zuord.rel_gst.rel_alm_gst_version
                last_gst = max(gst_versionen_list,
                               key=attrgetter('rel_alm_gst_ez.datenstand'))

                for cut in last_gst.rel_cut_koppel_gst:
                    awb_beweidet_area = awb_beweidet_area + cut.cutarea

        return awb_beweidet_area

    def __init__(self, parent=None):
        super(__class__, self).__init__(parent)

        self.entity_dialog_class = AktDialog
        self.entity_widget_class = Akt

        self._entity_mc = BAkt
        self._model_class = AktAllModel

        self.edit_entity_by = 'mci'
        """"""
        # self.setFeatureFields()
        # self.setFilterUI()
        #
        # self._gis_layer = self.setLayer()
        #
        # self.loadData()
        # self.setFeaturesFromMci()
        # self.setTableView()
        #
        # self.finalInit()
        #
        # # self.testGeneralFilter()
        # # self.setFilter()
        #
        # self.updateFooter()
        #
        # self.signals()

        print(f'...')

    def initUi(self):
        super().initUi()

        # self.title = 'alle Akte'

        self.setStretchMethod(2)

        self.uiAddDataTbtn.setVisible(False)
        self.uiDeleteDataTbtn.setVisible(False)

    def getMciList(self, session):

        # with db_session_cm() as session:
        stmt = (select(BAkt)
        .options(
            joinedload(BAkt.rel_bearbeitungsstatus)
        )
        # .options(
        #     joinedload(BAkt.rel_gst_zuordnung)
        #     .joinedload(BGstZuordnung.rel_awb_status)
        # )
        .options(
            joinedload(BAkt.rel_gst_zuordnung)
            .joinedload(BGstZuordnung.rel_rechtsgrundlage)
        )
        .options(
            joinedload(BAkt.rel_gst_zuordnung)
            .joinedload(BGstZuordnung.rel_gst)
            .joinedload(BGst.rel_alm_gst_version)
            .joinedload(BGstVersion.rel_alm_gst_ez)
        )
        .options(
            joinedload(BAkt.rel_gst_zuordnung)
            .joinedload(BGstZuordnung.rel_gst)
            .joinedload(BGst.rel_alm_gst_version)
            .joinedload(BGstVersion.rel_alm_gst_nutzung)
        )
        .options(
            joinedload(BAkt.rel_gst_zuordnung)
            .joinedload(BGstZuordnung.rel_gst)
            .joinedload(BGst.rel_alm_gst_version)
            .joinedload(BGstVersion.rel_cut_koppel_gst)
        )
        .options(
            joinedload(BAkt.rel_abgrenzung)
            .joinedload(BAbgrenzung.rel_komplex)
            .joinedload(BKomplex.rel_koppel)
        )
        )
        mci = session.scalars(stmt).unique().all()

        """test um direkter mit geometrien arbeiten zu können"""
        # # ).where(BAkt.id == 1090)
        # mci = session.scalars(stmt).unique().all()
        # geom = mci[0].rel_gst_zuordnung[3].rel_gst.rel_alm_gst_version[0].geometry
        # g = QgsGeometry()
        # # wkb = geom.hex()
        # # wkb = geom.tobytes()
        # g.fromWkb(geom)
        # print(g.asWkt())
        # print(f'...')
        """"""

        return mci

    # def setLayer(self):
    #
    #     layer = ZVectorLayer(
    #         "None",
    #         "AktAllLay",
    #         "memory",
    #         feature_fields=self.feature_fields
    #     )
    #     return layer
    #
    # def setFeaturesFromMci(self):
    #     super().setFeaturesFromMci()
    #
    #     for akt in self._mci_list:
    #
    #         feat = Feature(self._gis_layer.fields(), self)
    #
    #         self.setFeatureAttributes(feat, akt)
    #
    #         self._gis_layer.data_provider.addFeatures([feat])

    def finalInit(self):

        self.insertFooterLine('Gesamtweidefläche',
                              'ha', column_id=9, value_width=120,
                              factor=0.0001, decimal=4)
        self.insertFooterLine('davon beweidet',
                              'ha', column_id=8, value_width=120,
                              factor=0.0001, decimal=4)
        self.insertFooterLine('im NÖ Alm- und Weidebuch eingetragen',
                              'ha', column_id=7, value_width=120,
                              factor=0.0001, decimal=4)

        self.view.setColumnWidth(0, 40)
        self.view.setColumnWidth(1, 200)
        self.view.setColumnWidth(2, 100)
        self.view.setColumnWidth(3, 60)
        self.view.setColumnWidth(4, 40)
        self.view.setColumnWidth(5, 80)
        self.view.setColumnWidth(6, 150)
        self.view.setColumnWidth(7, 150)

        self.view.sortByColumn(1, Qt.AscendingOrder)

    # def setFeatureFields(self):
    #     super().setFeatureFields()
    #
    #     akt_id_fld = QgsField("akt_id", QVariant.Int)
    #
    #     az_fld = QgsField("az", QVariant.Int)
    #     az_fld.setAlias('AZ')
    #
    #     name_fld = QgsField("name", QVariant.String)
    #     name_fld.setAlias('Akt')
    #
    #     status_id_fld = QgsField("status_id", QVariant.Int)
    #
    #     status_fld = QgsField("status", QVariant.String)
    #     status_fld.setAlias('Bearbeitung')
    #
    #     status_color_fld = QgsField("status_color", QVariant.String)
    #
    #     stz_fld = QgsField("stz", QVariant.String)
    #     stz_fld.setAlias('Stz')
    #
    #     wwp_fld = QgsField("wwp", QVariant.Int)
    #     wwp_fld.setAlias('WWP')
    #
    #     wwp_jahr_fld = QgsField("wwp_jahr", QVariant.Int)
    #     wwp_jahr_fld.setAlias('WWP gültig')
    #
    #     awb_area_gb_fld = QgsField("awb_area_gb", QVariant.Int)
    #     awb_area_gb_fld.setAlias('AWB Fläche (lt. GB)')
    #
    #     awb_area_beweidet_fld = QgsField("awb_area_beweidet", QVariant.Int)
    #     awb_area_beweidet_fld.setAlias('AWB Fläche beweidet')
    #
    #     weide_area_fld = QgsField("weide_area", QVariant.Double)
    #     weide_area_fld.setAlias('Weidefläche')
    #
    #     # aa = QVariant.UserType
    #
    #     # test_fld = QgsField("test", QVariant.UserType)
    #
    #     self.feature_fields.append(akt_id_fld)
    #     self.feature_fields.append(az_fld)
    #     self.feature_fields.append(name_fld)
    #     self.feature_fields.append(status_id_fld)
    #     self.feature_fields.append(status_fld)
    #     self.feature_fields.append(status_color_fld)
    #     self.feature_fields.append(stz_fld)
    #     self.feature_fields.append(wwp_fld)
    #     self.feature_fields.append(wwp_jahr_fld)
    #     self.feature_fields.append(awb_area_gb_fld)
    #     self.feature_fields.append(awb_area_beweidet_fld)
    #     self.feature_fields.append(weide_area_fld)
    #     # self.feature_fields.append(test_fld)
    #
    # def changeAttributes(self, feature, mci):
    #
    #     attrib = {0: mci.id,
    #               1: mci.az,
    #               2: mci.name,
    #               3: mci.bearbeitungsstatus_id,
    #               4: mci.rel_bearbeitungsstatus.name,
    #               5: mci.rel_bearbeitungsstatus.color,
    #               6: mci.stz,
    #               7: mci.wwp,
    #               8: mci.wwp_jahr,
    #               9: self.get_awb_gb_area(mci),
    #               10: self.get_awb_beweidet(mci),
    #               11: self.get_weide_area(mci)
    #               }
    #
    #     self._gis_layer.changeAttributeValues(feature.id(),
    #                                           attrib)
    #
    # def setFeatureAttributes(self, feature, mci):
    #     # super().setFeatureAttributes(feature, mci)
    #
    #     feature['akt_id'] = mci.id
    #     feature['az'] = mci.az
    #     feature['name'] = mci.name
    #     feature['status_id'] = mci.bearbeitungsstatus_id
    #     feature['status'] = mci.rel_bearbeitungsstatus.name
    #     feature['status_color'] = mci.rel_bearbeitungsstatus.color
    #     feature['stz'] = mci.stz
    #     feature['wwp'] = mci.wwp
    #     feature['wwp_jahr'] = mci.wwp_jahr
    #     feature['awb_area_gb'] = self.get_awb_gb_area(mci)
    #     feature['awb_area_beweidet'] = self.get_awb_beweidet(mci)
    #     feature['weide_area'] = self.get_weide_area(mci)
    #
    # def updateFeatureAttributes(self, *args):
    #     super().updateFeatureAttributes(args)
    #
    #     new_mci = args[0][0]
    #
    #     with db_session_cm() as session:
    #
    #         session.add(new_mci)
    #
    #         self.setFeatureAttributes(self.current_feature, new_mci)


    # def getCustomData(self, session):
    #
    #     custom_data = {}
    #
    #     status_stmt = select(BBearbeitungsstatus)
    #     status_mci = session.scalars(status_stmt).all()
    #
    #     # awb_status_stmt = select(BGstAwbStatus)
    #     # awb_status_mci = session.scalars(awb_status_stmt).all()
    #
    #     custom_data['status'] = status_mci
    #     # custom_data['awb_status'] = awb_status_mci
    #
    #     return custom_data

    # def getCustomEntityData(self):
    #
    #     return [self._custom_entity_data['awb_status']]

    def updateMainWidget(self):

        self.updateMaintable()

    def setFilterUI(self):
        """
        setze das layout für die filter
        :return:
        """

        filter_lay = QHBoxLayout(self)

        """filter name"""
        # filter_name = FilterElement(self)
        # filter_name.uiLabelLbl.setText('Name:')
        self.filter_name_lbl = QLabel(self)

        name_lbl_font = self.filter_name_lbl.font()
        name_lbl_font.setFamily(config.font_family)
        self.filter_name_lbl.setFont(name_lbl_font)

        self.filter_name_lbl.setText('Name:')
        self.filter_name_lbl.setVisible(False)

        self.filter_name_input_wdg = QLineEdit(self)

        name_input_wdg_font = self.filter_name_input_wdg.font()
        name_input_wdg_font.setPointSize(11)
        name_input_wdg_font.setFamily(config.font_family)
        self.filter_name_input_wdg.setFont(name_input_wdg_font)

        self.filter_name_input_wdg.setPlaceholderText('Aktenname')
        self.filter_name_input_wdg.setClearButtonEnabled(True)
        self.filter_name_input_wdg.setMaximumWidth(200)
        # filter_name.uiFilterElementLay.insertWidget(1, self.filter_name_input_wdg)

        self.filter_name_input_wdg.textChanged.connect(self.useFilter)

        # filter_lay.addWidget(filter_name)
        """"""

        """filter az"""
        # filter_az = FilterElement(self)
        # filter_az.uiLabelLbl.setText('AZ:')

        self.filter_az_lbl = QLabel(self)

        az_lbl_font = self.filter_az_lbl.font()
        az_lbl_font.setFamily(config.font_family)
        self.filter_az_lbl.setFont(az_lbl_font)

        self.filter_az_lbl.setText('AZ:')
        self.filter_az_lbl.setVisible(False)

        self.filter_az_input_wdg = QLineEdit(self)
        self.filter_az_input_wdg.setPlaceholderText('AZ')
        az_input_wdg_font = self.filter_az_input_wdg.font()
        az_input_wdg_font.setPointSize(11)
        az_input_wdg_font.setFamily(config.font_family)
        self.filter_az_input_wdg.setFont(az_input_wdg_font)
        self.filter_az_input_wdg.setClearButtonEnabled(True)
        self.filter_az_input_wdg.setMaximumWidth(80)
        # filter_az.uiFilterElementLay.insertWidget(1, self.filter_adr_input_wdg)

        self.filter_az_input_wdg.textChanged.connect(self.useFilter)

        spacerItem1 = QSpacerItem(10, 20, QSizePolicy.Minimum,
                                 QSizePolicy.Minimum)
        filter_lay.addItem(spacerItem1)

        filter_lay.addWidget(self.filter_az_lbl)
        filter_lay.addWidget(self.filter_az_input_wdg)
        filter_lay.addWidget(self.filter_name_lbl)
        filter_lay.addWidget(self.filter_name_input_wdg)
        """"""

        spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        filter_lay.addItem(spacerItem)

        self.uiHeaderHley.insertLayout(1, filter_lay)

        # spacerItem2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        # self.uiFilterGLay.addItem(spacerItem2, 0, 2)

    def useFilter(self):

        name_text = self.filter_name_input_wdg.text()
        az_text = self.filter_az_input_wdg.text()

        name_expr = f"lower(\"name\") LIKE '%{name_text}%'"
        az_expr = f"to_string(\"az\") LIKE '%{az_text}%'"

        expr_list = []

        if name_text != '':
            self.filter_name_lbl.setVisible(True)
            expr_list.append(name_expr)
        else:
            self.filter_name_lbl.setVisible(False)

        if az_text != '':
            self.filter_az_lbl.setVisible(True)
            expr_list.append(az_expr)
        else:
            self.filter_az_lbl.setVisible(False)

        if expr_list == []:
            self._gis_layer.setSubsetString('')
        else:

            expr_string = " and ".join(expr for expr in expr_list)
            print(f'expression string: {expr_string}')
            self._gis_layer.setSubsetString(expr_string)

        self.updateFooter()


    # def setFilterScopeUI(self):
    #     super().setFilterScopeUI()
    #
    #     self.uicAktStatusFilterLbl = QLabel(self)
    #     self.uicAktStatusFilterLbl.setText('Status:')
    #
    #     self.uicAktStatusFilterCombo = QComboBox(self)
    #
    #     self.uiTableFilterHLay.insertWidget(2, self.uicAktStatusFilterLbl)
    #     self.uiTableFilterHLay.insertWidget(3, self.uicAktStatusFilterCombo)
    #
    # def setFilterScope(self):
    #     super().setFilterScope()
    #
    #     self.setFilterStatus()
    #
    # def setFilterStatus(self):
    #
    #     try:
    #         self.uicAktStatusFilterCombo.currentTextChanged.disconnect(
    #             self.filterMaintable)
    #     except:
    #         pass
    #     finally:
    #         prev_typ = self.uicAktStatusFilterCombo.currentText()
    #         self.uicAktStatusFilterCombo.clear()
    #
    #         self.uicAktStatusFilterCombo.addItem('- Alle -')
    #
    #         status_list = self._custom_entity_data['status']
    #         status_sorted = sorted(status_list,
    #                                 key=lambda x: x.sort)
    #
    #         for status in status_sorted:
    #             self.uicAktStatusFilterCombo.addItem(str(status.name))
    #
    #         self.uicAktStatusFilterCombo.setCurrentText(prev_typ)
    #
    #         self.uicAktStatusFilterCombo.currentTextChanged.connect(
    #             self.applyFilter)
    #
    # def useFilterScope(self, source_row, source_parent):
    #     super().useFilterScope(source_row, source_parent)
    #
    #     try:
    #         """filter status"""
    #         table_value = self.filter_proxy.sourceModel() \
    #             .data(self.filter_proxy.sourceModel().index(source_row, 2),
    #         Qt.DisplayRole)
    #         if self.uicAktStatusFilterCombo.currentText() != "- Alle -":
    #             if str(table_value) != self.uicAktStatusFilterCombo.currentText():
    #                 return False
    #         """"""
    #     except:
    #         print("Filter Error:", sys.exc_info())

    def signals(self):
        super().signals()

        self.uiAddDataTbtn.clicked.connect(self.add_row)
