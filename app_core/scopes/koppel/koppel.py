from app_core import db_session_cm
from app_core.data_model import BErfassungsart, BAbgrenzungStatus, BKomplexName, \
    BAbgrenzung, BKomplex, BKoppel
from app_core.entity import Entity
from app_core.gis_item import GisItem
from app_core.main_dialog import MainDialog
from app_core.scopes.koppel import koppel_UI
from qgis.PyQt.QtWidgets import QWidget
# from qgis.PyQt.QtGui import QStandardItem
from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtGui import QStandardItemModel

from sqlalchemy import select


class Koppel(koppel_UI.Ui_Koppel, Entity):

    # _erfassungsart_name = ''
    # _status_id = None
    # _status_name = ''
    #
    _name = ''
    _nr = 0
    _nicht_weide = 0
    _anm = ''

    # _komplex_name_id = 0
    # _komplex_name_mci = None

    _komplex_id = 0
    _komplex_mci = None

    _abgrenzung_id = 0
    _abgrenzung_mci = None

    _commit_on_apply = False

    @property  # getter
    def name(self):

        self._name = self.uiNameLedit.text()
        return self._name

    @name.setter
    def name(self, value):

        self.uiNameLedit.setText(value)
        self._name = value

    @property  # getter
    def nr(self):

        self._nr = self.uiNrSbox.value()
        return self._nr

    @nr.setter
    def nr(self, value):

        self.uiNrSbox.setValue(value)
        self._nr = value

    @property  # getter
    def nicht_weide(self):

        if self.uiNichtWeideCbox.isChecked():
            self._nicht_weide = 1
        else:
            self._nicht_weide = 0

        return self._nicht_weide

    @nicht_weide.setter
    def nicht_weide(self, value):

        if value == 1:
            self.uiNichtWeideCbox.setChecked(Qt.Checked)
        else:
            self.uiNichtWeideCbox.setChecked(Qt.Unchecked)

        self._nicht_weide = value

    @property  # getter
    def anm(self):

        self._anm = self.uiAnmerkungPtext.toPlainText()
        return self._anm

    @anm.setter
    def anm(self, value):

        self.uiAnmerkungPtext.setPlainText(value)
        self._anm = value

    # @property  # getter
    # def komplex_name_id(self):
    #
    #     self._komplex_name_id = self.uiKomplexNameCombo.currentData(Qt.UserRole + 1)
    #     return self._komplex_name_id
    #
    # @komplex_name_id.setter
    # def komplex_name_id(self, value):
    #
    #     """finde den status_id im model des uiAwbStatusCombo"""
    #     match_index = self.uiKomplexNameCombo.model().match(
    #         self.uiKomplexNameCombo.model().index(0, 0),
    #         Qt.UserRole + 1,
    #         value,
    #         -1,
    #         Qt.MatchExactly)
    #     """"""
    #
    #     if match_index:
    #
    #         self.uiKomplexNameCombo.setCurrentIndex(match_index[0].row())
    #         self._komplex_name_id = value
    #     else:
    #         self._komplex_name_id = 0
    #
    # @property  # getter
    # def komplex_name_mci(self):
    #
    #     mci = self.uiKomplexNameCombo.currentData(Qt.UserRole)
    #     return mci

    @property  # getter
    def abgrenzung_mci(self):

        mci = self.uiAbgrenzungCombo.currentData(Qt.UserRole)
        return mci

    @property  # getter
    def abgrenzung_id(self):

        self._abgrenzung_id = self.uiAbgrenzungCombo.currentData(Qt.UserRole + 1)
        return self._abgrenzung_id

    @abgrenzung_id.setter
    def abgrenzung_id(self, value):

        """finde den status_id im model des uiAwbStatusCombo"""
        match_index = self.uiAbgrenzungCombo.model().match(
            self.uiAbgrenzungCombo.model().index(0, 0),
            Qt.UserRole + 1,
            value,
            -1,
            Qt.MatchExactly)
        """"""

        if match_index:

            self.uiAbgrenzungCombo.setCurrentIndex(match_index[0].row())
            self._abgrenzung_id = value
        else:
            self._abgrenzung_id = 0

    @property  # getter
    def komplex_mci(self):

        # self._komplex_mci.rel_abgrenzung = self.abgrenzung_mci
        # self._komplex_mci.rel_komplex_name = self.komplex_name_mci

        mci = self.uiKomplexCombo.currentData(Qt.UserRole)

        return mci

    @komplex_mci.setter
    def komplex_mci(self, value):

        """finde den status_id im model des uiAwbStatusCombo"""
        match_index = self.uiKomplexCombo.model().match(
            self.uiKomplexCombo.model().index(0, 0),
            Qt.UserRole + 1,
            value.id,
            -1,
            Qt.MatchExactly)
        """"""

        if match_index:

            self.uiKomplexCombo.setCurrentIndex(match_index[0].row())
            self._komplex_mci = value
        else:
            self._komplex_mci = None

        self.abgrenzung_id = value.abgrenzung_id
        # self.komplex_name_id = value.komplex_name_id

        self._komplex_mci = value

    def __init__(self, parent=None, item=None):
        super(__class__, self).__init__()
        self.setupUi(self)

        self.parent = parent

        self._entity_mc = BKoppel

        self.akt_id = None
        self.abgrenzung_id = None

    def getAktId(self):

        if self.akt_id is None:
            return self._entity_mci.rel_komplex.rel_abgrenzung.rel_akt.id
        else:
            return self.akt_id

        # self.uiAktNameLbl.setText(self.parent.name + ' (AZ '
        #                           + str(self.parent.az) + ')')

        # komplex_name = self.item.parent().data(GisItem.Name_Role)
        # self.uiKomplexNameLbl.setText(komplex_name)

    #     self.uiStatusCombo.currentIndexChanged.connect(self.changedStatus)
    #
    #     self.loadCombos()

    def mapEntityData(self):
        # self.uiStatusCombo.currentIndexChanged.connect(self.changedStatus)

        self.name = self._entity_mci.name
        self.nr = self._entity_mci.nr
        self.nicht_weide = self._entity_mci.nicht_weide
        self.anm = self._entity_mci.anmerkung

        # self.komplex_name_id = self._entity_mci.rel_komplex.komplex_name_id
        self.komplex_mci = self._entity_mci.rel_komplex

        # self.uiAreaLbl.setText(
        #     '{:.4f}'.format(
        #         round(float(self._entity_mci.koppel_area) / 10000, 4))
        #     .replace(".", ",") + ' ha')

    def loadBackgroundData(self):
        super().loadBackgroundData()

        self.setAbgrenzungComboData()
        # self.setKomplexNameComboData()

        self.setKomplexComboData()

    def setAbgrenzungComboData(self):
        """

        """
        # akt_id = self._entity_mci.rel_komplex.rel_abgrenzung.rel_akt.id

        abgrenzung_stmt = (
            select(BAbgrenzung)
            .where(BAbgrenzung.akt_id == self.getAktId())
            .order_by(BAbgrenzung.jahr)
        )

        abgrenzung_mci_list = self.entity_session.scalars(abgrenzung_stmt).all()

        """erstelle ein model mit 1 spalten für das combo"""
        abgrenzung_model = QStandardItemModel(len(abgrenzung_mci_list), 1)
        for i in range(len(abgrenzung_mci_list)):

            text = f'{str(abgrenzung_mci_list[i].jahr)} - {abgrenzung_mci_list[i].rel_status.name}'

            abgrenzung_model.setData(abgrenzung_model.index(i, 0),
                                          text, Qt.DisplayRole)
            abgrenzung_model.setData(abgrenzung_model.index(i, 0),
                                          abgrenzung_mci_list[i].id, Qt.UserRole + 1)
            abgrenzung_model.setData(abgrenzung_model.index(i, 0),
                                          abgrenzung_mci_list[i], Qt.UserRole)
        """"""

        """weise dem combo das model zu"""
        self.uiAbgrenzungCombo.setModel(abgrenzung_model)
        """"""

    def setKomplexNameComboData(self):
        """

        """
        # akt_id = self._entity_mci.rel_komplex.rel_abgrenzung.rel_akt.id

        komplex_name_stmt = (
            select(BKomplexName)
            .where(BKomplexName.akt_id == self.getAktId())
            .order_by(BKomplexName.nr)
        )

        komplex_name_mci_list = self.entity_session.scalars(komplex_name_stmt).all()

        for name in komplex_name_mci_list:

            print(f'name: {name.name}   - komplex_name_id: {name.rel_komplex}')

        """erstelle ein model mit 1 spalten für das combo"""
        komplex_name_model = QStandardItemModel(len(komplex_name_mci_list), 1)
        for i in range(len(komplex_name_mci_list)):

            if komplex_name_mci_list[i].nr == 0 or komplex_name_mci_list[i].nr is None:
                nr = 0
            else:
                nr = komplex_name_mci_list[i].nr

            text = f'{str(nr)}: {komplex_name_mci_list[i].name}'
            komplex_name_model.setData(komplex_name_model.index(i, 0),
                                          text, Qt.DisplayRole)
            komplex_name_model.setData(komplex_name_model.index(i, 0),
                                          komplex_name_mci_list[i].id, Qt.UserRole + 1)
            komplex_name_model.setData(komplex_name_model.index(i, 0),
                                          komplex_name_mci_list[i], Qt.UserRole)
        """"""

        """weise dem combo das model zu"""
        self.uiKomplexNameCombo.setModel(komplex_name_model)
        """"""

    def setKomplexComboData(self):
        """

        """
        # akt_id = self._entity_mci.rel_komplex.rel_abgrenzung.rel_akt.id
        abgr_id = self.parent.parent.abgrenzung_table._gis_layer.selectedFeatures()[0].attribute('abgrenzung_id')
        # abgr_mci = self.parent.parent.abgrenzung_table._gis_layer.selectedFeatures()[0].attribute('mci')

        komplex_stmt = select(BKomplex).where(BKomplex.abgrenzung_id == abgr_id)
        komplex_mci_list = self.entity_session.scalars(komplex_stmt).all()

        all_komplex_name = select(BKomplexName).where(BKomplexName.akt_id == self.getAktId())
        all_komplex_name_mci_list = self.entity_session.scalars(all_komplex_name).all()

        current_names = [komplex_mci.rel_komplex_name for komplex_mci in komplex_mci_list]

        combo_mci_list = []

        for komplex_name in all_komplex_name_mci_list:

            if komplex_name in current_names:

                    for komp in komplex_name.rel_komplex:

                        if komp.abgrenzung_id == abgr_id:

                            combo_mci_list.append(komp)


            else:

                new_komplex = BKomplex()
                new_komplex.abgrenzung_id = abgr_id
                # new_komplex.rel_abgrenzung = abgr_mci
                # new_komplex.abgrenzung_id = 99999
                new_komplex.rel_komplex_name = komplex_name
                self.entity_session.add(new_komplex)
                self.entity_session.flush()

                combo_mci_list.append(new_komplex)

        """erstelle ein model mit 1 spalten für das combo"""
        komplex_model = QStandardItemModel(len(combo_mci_list), 1)

        for i in range(len(combo_mci_list)):

            # if komplex_mci_list[i].nr == 0 or komplex_mci_list[i].nr is None:
            #     nr = 0
            # else:
            #     nr = komplex_mci_list[i].nr

            text = f'{str(combo_mci_list[i].rel_komplex_name.nr)}: {combo_mci_list[i].rel_komplex_name.name}'
            print(f'text: {text}')

            komplex_model.setData(komplex_model.index(i, 0),
                                          text, Qt.DisplayRole)
            komplex_model.setData(komplex_model.index(i, 0),
                                          combo_mci_list[i].id, Qt.UserRole + 1)
            komplex_model.setData(komplex_model.index(i, 0),
                                          combo_mci_list[i], Qt.UserRole)
        """"""

        """weise dem combo das model zu"""
        self.uiKomplexCombo.setModel(komplex_model)
        """"""

    def submitEntity(self):

        self._entity_mci.name = self.name
        self._entity_mci.nr = self.nr
        self._entity_mci.nicht_weide = self.nicht_weide
        self._entity_mci.anmerkung = self.anm

        # self._entity_mci.rel_komplex.rel_komplex_name = self.komplex_name_mci
        self._entity_mci.rel_komplex = self.komplex_mci

class KoppelDialog(MainDialog):
    """
    dialog für ein entity-widget (Entity)
    """

    def __init__(self, parent=None):
        super(__class__, self).__init__(parent)

        self.parent = parent
        self.enableApply = True
        self.set_apply_button_text('&Speichern und Schließen')

        self.setMinimumWidth(250)
        self.setMaximumWidth(500)

    def accept(self):
        """
        wenn 'acceptEntity' des entity-widget True zurückgibt (die daten sind
        gültig) dann rufe QDialog.accept() auf
        """
        # if self.dialogWidget.acceptEntity():
        #     super().accept()

        self.dialogWidget.submitData()
        super().accept()