from _operator import attrgetter

from PyQt5.QtCore import QVariant
# from PyQt5.QtWidgets import QDialog
from qgis.PyQt.QtCore import Qt, QModelIndex
from qgis.PyQt.QtGui import QColor, QBrush
from qgis.PyQt.QtWidgets import (QLabel, QComboBox, QLineEdit,
                                 QSpacerItem, QSizePolicy)

from sqlalchemy import select

from almgis import settings_general
# from almgis import session_cm, DbSession
# from almgis.data_session import session_cm, DbSession
# from almgis.config import Config
from almgis.data_model import DmAkt, DmBearbeitungsstatus
# from qga.entity import EntityDialog
from qga.data_view import QgaDataView, QgaTableModel
from qga.main_widget import QgaMainWidget

from almgis.data_session import session_cm
from almgis.data_view import AlmDataView
from almgis.scopes.akte.akt_columns import AktNameCol, AktAzCol, AktWeideareaCol


# from almgis.scopes.akte.akt import Akt


# class AktDialog(EntityDialog):
#     """
#     dialog für die anzeige einer grundstückszuordnung
#     """
#
#     def __init__(self, parent):
#         super(__class__, self).__init__(parent)
#
#         self.dialog_window_title = 'Alm- und Weidebuchakt'


class AkteAllMainWidget(QgaMainWidget):
    """
    MainWidget für die Darstellung eines DataView's mit allen Akten
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self.uiTitleLbl.setText('alle Akte')

        self.main_wdg = AkteAllMain(self)

    def createMw(self):
        # self.akt_all_table.setDataviewSession(session)
        self.main_wdg.initDataView()

        self.initMainWidget()

    def initMainWidget(self):
        super().initMainWidget()

        self.uiMainVlay.addWidget(self.main_wdg)


class AktAllModel(QgaTableModel):

    # header = ['AZ',
    #           'Name',
    #           'Status',
    #           'Stz',
    #           'Bewirtschafter',
    #           'WWP',
    #           'WWP-Jahr',
    #           'AWB-Fläche (GB)',
    #           'davon beweidet',
    #           'Weidefläche']

    def data(self, index, role=Qt.DisplayRole):

        if not index.isValid():
            return QVariant()

        column = self._columns[index.column()]
        # value = self._dmi_list[index.row()][index.column()]
        # dmi = self._dmi_list[index.row()]
        dmi = self.parent.dmi_list[index.row()]

        # Delegate role handling to the column class
        return column.handle_role(role, dmi)

    # def data(self, index: QModelIndex, role: int = ...):
    #
    #     """
    #     erzeuge ein basis-model
    #     """
    #     row = index.row()
    #     col = index.column()
    #
    #     if role == Qt.TextAlignmentRole:
    #
    #         if index.column() in [7, 8, 9]:
    #
    #             return Qt.AlignRight | Qt.AlignVCenter
    #
    #         if index.column() in [0, 2, 3, 5, 6]:
    #
    #             return Qt.AlignHCenter | Qt.AlignVCenter
    #
    #     if role == Qt.BackgroundRole:
    #
    #         if index.column() == 2:
    #
    #             if self.parent.dmi_list[row].rel_bearbeitungsstatus is not None:
    #
    #                 color_str = self.parent.dmi_list[row].rel_bearbeitungsstatus.color
    #                 color_list = color_str.split(", ")
    #
    #                 return QColor(int(color_list[0]),
    #                               int(color_list[1]),
    #                               int(color_list[2]))
    #
    #
    #     if index.column() == 0:
    #         if role == Qt.DisplayRole:
    #             return self.parent.dmi_list[row].az
    #         # if role == Qt.EditRole:
    #         #     return self.parent._dmi_list[row].az
    #
    #         if role == Qt.ForegroundRole:
    #             if self.parent.dmi_list[row].nicht_bewirtschaftet == 1:
    #                 return QBrush(Qt.gray)
    #
    #     if index.column() == 1:
    #         if role == Qt.DisplayRole:
    #             return self.parent.dmi_list[row].name
    #         # if role == Qt.EditRole:
    #         #     return self.parent.dmi_list[row].name
    #
    #         if role == Qt.ForegroundRole:
    #             if self.parent.dmi_list[row].nicht_bewirtschaftet == 1:
    #                 return QBrush(Qt.gray)
    #
    #     if index.column() == 2:
    #
    #         if self.parent.dmi_list[row].rel_bearbeitungsstatus is not None:
    #
    #             if role == Qt.DisplayRole:
    #                 return self.parent.dmi_list[row].rel_bearbeitungsstatus.name
    #             if role == Qt.EditRole:
    #                 return self.parent.dmi_list[row].bearbeitungsstatus_id
    #
    #     if index.column() == 3:
    #         if role == Qt.DisplayRole:
    #             return self.parent.dmi_list[row].stz
    #
    #     if index.column() == 4:
    #         # if role == Qt.DisplayRole:
    #         #     return self.parent.dmi_list[row].anm
    #         if self.parent.dmi_list[row].rel_bewirtschafter is not None:
    #
    #             if role == Qt.DisplayRole:
    #                 return self.parent.dmi_list[row].rel_bewirtschafter.name
    #             if role == Qt.EditRole:
    #                 return self.parent.dmi_list[row].bewirtschafter_id
    #
    #     if index.column() == 5:
    #         if role == Qt.DisplayRole:
    #             if self.parent.dmi_list[row].wwp == 1:
    #                 return 'X'
    #
    #     if index.column() == 6:
    #         if role == Qt.DisplayRole:
    #             if self.parent.dmi_list[row].wwp == 1:
    #                 if self.parent.dmi_list[row].wwp_date is not None:
    #                     return self.parent.dmi_list[row].wwp_date
    #                 else:
    #                     return '---'
    #             return ''
    #
    #     if index.column() == 7:  # im awb eingetragene flaeche
    #         # anz = 0
    #         gst_area = 0
    #         for gst_zuord in self.parent.dmi_list[row].rel_gst_zuordnung:
    #             # anz += 1
    #             if gst_zuord.awb_status_id == 1:
    #                 gst_versionen_list = gst_zuord.rel_gst.rel_alm_gst_version
    #                 last_gst = max(gst_versionen_list,
    #                                key=attrgetter('rel_alm_gst_ez.datenstand'))
    #                 # print(f'last gst: {last_gst.import_time}')
    #                 gst_m = 0
    #                 for ba in last_gst.rel_alm_gst_nutzung:
    #                     gst_m = gst_m + ba.area
    #                 gst_area = gst_area + gst_m
    #
    #         if role == Qt.DisplayRole:
    #             gst_area_ha = '{:.4f}'.format(round(float(gst_area) / 10000, 4)).replace(".", ",") + ' ha'
    #             return gst_area_ha
    #         if role == Qt.EditRole:
    #             return gst_area
    #
    #     if index.column() == 8:  # davon beweidet
    #
    #         if role in [Qt.DisplayRole, Qt.EditRole]:
    #
    #             cut_area = 0
    #             for gst_zuord in self.parent.dmi_list[row].rel_gst_zuordnung:
    #                 # anz += 1
    #                 if gst_zuord.awb_status_id == 1:
    #                     gst_versionen_list = gst_zuord.rel_gst.rel_alm_gst_version
    #                     last_gst = max(gst_versionen_list,
    #                                    key=attrgetter('rel_alm_gst_ez.datenstand'))
    #
    #                     for cut in last_gst.rel_cut_koppel_gst:
    #                         # cut_area = cut_area + last_gst.rel_cut_koppel_gst.cutarea
    #                         cut_area = cut_area + cut.cut_area
    #                     # print(f'last gst: {last_gst.import_time}')
    #                     # gst_m = 0
    #                     # for ba in last_gst.rel_alm_gst_nutzung:
    #                     #     gst_m = gst_m + ba.area
    #                     # gst_area = gst_area + gst_m
    #
    #             if role == Qt.DisplayRole:
    #                 # cut_area_str = '{:.4f}'.format(round(float(cut_area) / 10000, 4))
    #                 cut_area_ha = '{:.4f}'.format(round(float(cut_area) / 10000, 4)).replace(".", ",") + ' ha'
    #                 # cut_area_ha = cut_area_str.replace(".", ",") + ' ha'
    #                 return cut_area_ha
    #
    #             if role == Qt.EditRole:
    #
    #                 return cut_area
    #
    #     if index.column() == 9:  # weideflaeche
    #
    #         if role in [Qt.DisplayRole, Qt.EditRole]:
    #
    #             kop_area = 0.00
    #
    #             # print(f'self.parent.dmi_list[row].rel_abgrenzung: {self.parent.dmi_list[row].rel_abgrenzung}')
    #
                # if self.parent.dmi_list[row].rel_abgrenzung != []:
                #
                #     last_abgrenzung = max(self.parent.dmi_list[row].rel_abgrenzung,
                #                       key=attrgetter('jahr'))
                #
                #     for komplex in last_abgrenzung.rel_komplex:
                #         for koppel in komplex.rel_koppel:
                #             kop_area = kop_area + koppel.koppel_area
                #
                #     if role == Qt.DisplayRole:
                #         kop_area_ha = '{:.4f}'.format(
                #             round(float(kop_area) / 10000, 4)).replace(".",
                #                                                        ",") + ' ha'
                #         return kop_area_ha
                #     if role == Qt.EditRole:
                #         return kop_area
                #
                # else:
                #     if role == Qt.DisplayRole:
                #         return '---'
                #     if role == Qt.EditRole:
                #         return 0


class AkteAllMain(AlmDataView):


    _maintable_text = ["Akt", "Akte", "kein Akt"]
    _delete_window_title = ["Akt löschen", "Akte löschen"]
    _delete_window_text_single = "Soll der ausgewählte Akt " \
                                 "wirklich gelöscht werden?"
    _delete_window_text_plural = ["Sollen die ausgewählten",
                                  "Akte wirklich gelöscht werden?"]

    def get_weide_area(self, dmi):
        weide_area = 0.00
        if dmi.rel_abgrenzung != []:
            last_abgrenzung = max(dmi.rel_abgrenzung,
                                  key=attrgetter('jahr'))
            for komplex in last_abgrenzung.rel_komplex:
                for koppel in komplex.rel_koppel:
                    weide_area = weide_area + koppel.koppel_area

        return weide_area

    def get_awb_gb_area(self, dmi):

        awb_area = 0
        for gst_zuord in dmi.rel_gst_zuordnung:

            if gst_zuord.awb_status_id == 1:
                gst_versionen_list = gst_zuord.rel_gst.rel_alm_gst_version
                last_gst = max(gst_versionen_list,
                               key=attrgetter('rel_alm_gst_ez.datenstand'))

                gst_nutz_area = 0
                for ba in last_gst.rel_alm_gst_nutzung:
                    gst_nutz_area = gst_nutz_area + ba.area
                awb_area = awb_area + gst_nutz_area
        return awb_area

    def get_awb_beweidet(self, dmi):

        awb_beweidet_area = 0
        for gst_zuord in dmi.rel_gst_zuordnung:

            if gst_zuord.awb_status_id == 1:
                gst_versionen_list = gst_zuord.rel_gst.rel_alm_gst_version
                last_gst = max(gst_versionen_list,
                               key=attrgetter('rel_alm_gst_ez.datenstand'))

                for cut in last_gst.rel_cut_koppel_gst:
                    awb_beweidet_area = awb_beweidet_area + cut.cutarea

        return awb_beweidet_area

    def __init__(self, parent=None):
        super(__class__, self).__init__(parent)
        # self.initUi()

        # self.entity_dialog_class = AktDialog
        # self.entity_widget_class = Akt
        self._entity_dmc = DmAkt
        self._model_class = AktAllModel

    def initUi(self):
        super().initUi()

        self.setStretchMethod(2)

        self.uiAddDataTbtn.setVisible(False)

        # self.actionDeleteRow.setParent(None)  # entferne action zeile löschen
        # self.uiToolsTbtn.removeAction(self.actionDeleteRow)

        self.insertFooterLine('Gesamtweidefläche',
                              'ha', column_id=2, value_width=120,
                              factor=0.0001, decimal=4, column_type=float)
        self.insertFooterLine('davon beweidet',
                              'ha', column_id=8, value_width=120,
                              factor=0.0001, decimal=4)
        self.insertFooterLine('im NÖ Alm- und Weidebuch eingetragen',
                              'ha', column_id=7, value_width=120,
                              factor=0.0001, decimal=4)

    def getDmiList(self):

        # session = DbSession()

        stmt = (select(DmAkt)
        )
        dmi = self.session.scalars(stmt).unique().all()

        """test um direkter mit geometrien arbeiten zu können"""
        # # ).where(DmAkt.id == 1090)
        # dmi = session.scalars(stmt).unique().all()
        # geom = dmi[0].rel_gst_zuordnung[3].rel_gst.rel_alm_gst_version[0].geometry
        # g = QgsGeometry()
        # # wkb = geom.hex()
        # # wkb = geom.tobytes()
        # g.fromWkb(geom)
        # print(g.asWkt())
        # print(f'...')
        """"""

        return dmi

    # def finalInit(self):
    #
    #     # self.insertFooterLine('Gesamtweidefläche',
    #     #                       'ha', column_id=9, value_width=120,
    #     #                       factor=0.0001, decimal=4)
    #     # self.insertFooterLine('davon beweidet',
    #     #                       'ha', column_id=8, value_width=120,
    #     #                       factor=0.0001, decimal=4)
    #     # self.insertFooterLine('im NÖ Alm- und Weidebuch eingetragen',
    #     #                       'ha', column_id=7, value_width=120,
    #     #                       factor=0.0001, decimal=4)
    #
    #     self.view.setColumnWidth(0, 40)
    #     self.view.setColumnWidth(1, 200)
    #     self.view.setColumnWidth(2, 150)
    #     self.view.setColumnWidth(3, 60)
    #     self.view.setColumnWidth(4, 450)
    #     self.view.setColumnWidth(5, 80)
    #     self.view.setColumnWidth(6, 150)
    #     self.view.setColumnWidth(7, 150)
    #
    #     self.view.sortByColumn(1, Qt.AscendingOrder)

    def setFilterUI(self):
        """
        setze das layout für die filter
        :return:
        """

        """filter name"""
        self.filter_name_lbl = QLabel(self)

        name_lbl_font = self.filter_name_lbl.font()
        name_lbl_font.setFamily(settings_general.font_family)
        self.filter_name_lbl.setFont(name_lbl_font)

        self.filter_name_lbl.setText('Name:')
        self.filter_name_lbl.setVisible(False)

        self.filter_name_input_wdg = QLineEdit(self)

        name_input_wdg_font = self.filter_name_input_wdg.font()
        name_input_wdg_font.setPointSize(11)
        name_input_wdg_font.setFamily(settings_general.font_family)
        self.filter_name_input_wdg.setFont(name_input_wdg_font)

        self.filter_name_input_wdg.setPlaceholderText('Aktenname')
        self.filter_name_input_wdg.setClearButtonEnabled(True)
        self.filter_name_input_wdg.setMaximumWidth(200)

        self.filter_name_input_wdg.textChanged.connect(
            self.applyFilter)
        """"""

        """filter az"""
        self.filter_az_lbl = QLabel(self)

        az_lbl_font = self.filter_az_lbl.font()
        az_lbl_font.setFamily(settings_general.font_family)
        self.filter_az_lbl.setFont(az_lbl_font)

        self.filter_az_lbl.setText('AZ:')
        self.filter_az_lbl.setVisible(False)

        self.filter_az_input_wdg = QLineEdit(self)
        self.filter_az_input_wdg.setPlaceholderText('AZ')
        az_input_wdg_font = self.filter_az_input_wdg.font()
        az_input_wdg_font.setPointSize(11)
        az_input_wdg_font.setFamily(settings_general.font_family)
        self.filter_az_input_wdg.setFont(az_input_wdg_font)
        self.filter_az_input_wdg.setClearButtonEnabled(True)
        self.filter_az_input_wdg.setMaximumWidth(80)

        self.filter_az_input_wdg.textChanged.connect(
            self.applyFilter)
        """"""

        """filter status_id"""
        self.filter_status_lbl = QLabel(self)

        status_lbl_font = self.filter_status_lbl.font()
        status_lbl_font.setFamily(settings_general.font_family)
        self.filter_status_lbl.setFont(status_lbl_font)

        self.filter_status_lbl.setText('AZ:')
        self.filter_status_lbl.setVisible(False)

        self.filter_status_input_wdg = QComboBox(self)

        self.filter_status_input_wdg.addItem('--- alle Statuse ---', -1)

        with session_cm(name='contact type filter') as session:

            status_stmt = select(DmBearbeitungsstatus)
            status_dmi_list = session.scalars(status_stmt).all()

            for status in status_dmi_list:
                self.filter_status_input_wdg.addItem(status.name,
                                                   status.id)

        status_input_wdg_font = self.filter_status_input_wdg.font()
        status_input_wdg_font.setPointSize(11)
        status_input_wdg_font.setFamily(settings_general.font_family)
        self.filter_status_input_wdg.setFont(status_input_wdg_font)

        self.filter_status_input_wdg.currentIndexChanged.connect(
            self.applyFilter)
        """"""

        """platziere die filter-elemente"""
        spacerItem1 = QSpacerItem(10, 20, QSizePolicy.Minimum,
                                 QSizePolicy.Minimum)
        self.uiFilterHlay.addItem(spacerItem1)

        self.uiFilterItemsHlay.addWidget(self.filter_az_lbl)
        self.uiFilterItemsHlay.addWidget(self.filter_az_input_wdg)
        self.uiFilterItemsHlay.addWidget(self.filter_name_lbl)
        self.uiFilterItemsHlay.addWidget(self.filter_name_input_wdg)
        self.uiFilterItemsHlay.addWidget(self.filter_status_lbl)
        self.uiFilterItemsHlay.addWidget(self.filter_status_input_wdg)

        # self.setFilterRemoveBtn()

        spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.uiFilterItemsHlay.addItem(spacerItem)
        """"""

    def applyFilter(self):

        filter = False

        """filter az"""
        if self.filter_az_input_wdg.text() == '':
            self.filter_az_lbl.setVisible(False)
        else:
            self.filter_az_lbl.setVisible(True)
            filter = True
        """"""

        """filter name"""
        if self.filter_name_input_wdg.text() == '':
            self.filter_name_lbl.setVisible(False)
        else:
            self.filter_name_lbl.setVisible(True)
            filter = True
        """"""

        """filter voucher type"""
        if self.filter_status_input_wdg.currentData(Qt.UserRole) == -1:
            self.filter_status_lbl.setVisible(False)
        else:
            self.filter_status_lbl.setVisible(True)
            filter = True
        """"""

        # """filter remove button"""
        # if filter:
        #     self.uiFilterRemovePbtn.setVisible(True)
        # else:
        #     self.uiFilterRemovePbtn.setVisible(False)
        # """"""

        super().applyFilter()

    def removeFilter(self):

        self.filter_az_input_wdg.setText('')
        self.filter_name_input_wdg.setText('')
        self.filter_status_input_wdg.setCurrentIndex(0)

    # def useFilterScope(self, source_row, source_parent):
    #     super().useFilterScope(source_row, source_parent)
    #
    #     """filter az"""
    #     table_value = self.filter_proxy.sourceModel() \
    #         .data(self.filter_proxy.sourceModel().index(source_row, 0),
    #     Qt.DisplayRole)
    #     if self.filter_az_input_wdg.text() not in str(table_value):
    #         return False
    #     """"""
    #
    #     """filter name"""
    #     table_value = self.filter_proxy.sourceModel() \
    #         .data(self.filter_proxy.sourceModel().index(source_row, 1),
    #     Qt.DisplayRole)
    #     if self.filter_name_input_wdg.text() not in table_value.lower():
    #         return False
    #     """"""
    #
    #     """filter status_id"""
    #     status = self.filter_proxy.sourceModel() \
    #         .data(self.filter_proxy.sourceModel().index(source_row, 2),
    #               Qt.EditRole)
    #     if self.filter_status_input_wdg.currentData(Qt.UserRole) != -1:
    #         if status != self.filter_status_input_wdg.currentData(Qt.UserRole):
    #             return False
    #     """"""

    def signals(self):
        super().signals()

        # self.uiAddDataTbtn.clicked.connect(self.add_row)

    def set_columns(self):

        self.columns.append(AktAzCol('AZ'))
        self.columns.append(AktNameCol('Aktenname'))

        weide_area_col = AktWeideareaCol('Weidefläche')
        # weide_area_col.set_role_handler(Qt.DisplayRole, lambda x: f"{str(x)} ha")
        self.columns.append(weide_area_col)
