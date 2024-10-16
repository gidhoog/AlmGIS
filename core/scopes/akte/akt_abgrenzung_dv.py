from qgis.PyQt.QtCore import Qt, QModelIndex
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QDialog

from qgis.core import QgsField
from qgis.PyQt.QtCore import QVariant

from core.data_model import BAbgrenzung
from core.entity import EntityDialog
from core.gis_layer import ZVectorLayer, Feature
from core.data_view import DataView, GisTableModel

from core.scopes.akte.abgrenzung import Abgrenzung


class AbgrenzungDialog(EntityDialog):
    """
    dialog für die anzeige einer grundstückszuordnung
    """

    def __init__(self, parent):
        super(__class__, self).__init__(parent)

        self.dialog_window_title = 'Abgrenzung'
        # self.set_apply_button_text('&Speichern und Schließen')

    def accept(self):
        super().accept()

        if self.dialogWidget.acceptEntity() is not None:

            new_mci = self.dialogWidget.acceptEntity()

            self.parent.updateMaintableNew(self.dialogWidget.purpose, new_mci)

        QDialog.accept(self)


class AbgrenzungModel(GisTableModel):

    def __init__(self, layerCache, parent=None):
        super(AbgrenzungModel, self).__init__(layerCache, parent)

    def data(self, index: QModelIndex, role: int = ...):

        # feat = self.feature(index)

        if role == Qt.TextAlignmentRole:

            # if index.column() in [3]:
            #
            #     return Qt.AlignRight | Qt.AlignVCenter

            if index.column() in [1, 3, 4]:

                return Qt.AlignHCenter | Qt.AlignVCenter

        if index.column() == 1:

            if role == Qt.DisplayRole:

                return str(self.feature(index).attribute('jahr'))

            if role == Qt.DecorationRole:

                if self.feature(index).attribute('awb') == 1:

                    return QIcon(':/svg/resources/icons/awb.svg')

        return super().data(index, role)


class AbgrenzungDataView(DataView):
    """
    koppeltabelle im akt
    """

    _maintable_text = ["Abgrenzung", "Abgrenzungen", "keine Abgrenzung"]
    _delete_window_title = ["Abgrenzung löschen", "Abgrenzungen löschen"]
    _delete_window_text_single = "Soll die ausgewählte Abgrenzung " \
                                 "wirklich gelöscht werden?"
    _delete_window_text_plural = ["Sollen die ausgewählten",
                                  "Abgrenzungen wirklich gelöscht werden?"]
    _delete_text = ["Die Abgrenzung", "kann nicht gelöscht werden, da sie "
                                          "verwendet wird!"]

    def __init__(self, parent=None, gis_mode=False):
        super(__class__, self).__init__(parent, gis_mode)

        self.entity_dialog_class = AbgrenzungDialog
        self.entity_widget_class = Abgrenzung

        self._entity_mc = BAbgrenzung
        self._model_gis_class = AbgrenzungModel

        self._commit_entity = False
        self.edit_entity_by = 'mci'

    def initUi(self):
        super().initUi()

        self.uiTitleLbl.setVisible(True)

        self.uiTitleLbl.setText('Abgrenzungen')

    def loadData(self, session=None):

        self._mci_list = self.parent._entity_mci.rel_abgrenzung

    def selectedRowsChanged(self):
        super().selectedRowsChanged()

        # sel_rows = self.getSelectedRows()
        #
        # self.sel_entity_mci = self._gis_layer.getFeature(sel_rows[0]).attribute('mci')

    def getIstAbgrenzungId(self):
        """
        getter für die aktuell gültige abgrenzung (IST-Version)
        :return: id der abgrenzung
        """

        """filtere alle abgrenzungen mit status_id 0 (=IST-Version)"""
        ist_abgr_list = [a for a in self._mci_list if a.status_id == 0]
        """"""

        """sortiere absteigend nach dem jahr, der erste eintrag ist der
        aktuelle"""
        sort_abgr = sorted(ist_abgr_list, key=lambda x: x.jahr, reverse=True)
        """"""

        """gib den ersten eintrag zurück wenn etwas gefunden wird"""
        if sort_abgr != []:
            return sort_abgr[0]
        else:
            return None
        """"""


    def setLayer(self):

        layer = ZVectorLayer(
            "None",
            "Abgrenzungen",
            "memory",
            feature_fields=self.feature_fields
        )

        # setLayerStyle(layer, 'gst_awbuch_status')

        return layer

    def setFeaturesFromMci(self):
        super().setFeaturesFromMci()

        for koppel in self._mci_list:

            feat = Feature(self._gis_layer.fields(), self)

            self.setFeatureAttributes(feat, koppel)

            self._gis_layer.data_provider.addFeatures([feat])

    def setFeatureFields(self):
        # super().setFeatureFields()

        abgrenzung_id_fld = QgsField("abgrenzung_id", QVariant.Int)

        jahr_fld = QgsField("jahr", QVariant.Int)
        jahr_fld.setAlias('Jahr')

        status_id_fld = QgsField("status_id", QVariant.Int)

        status_name_fld = QgsField("status_name", QVariant.String)

        bearbeiter_fld = QgsField("bearbeiter", QVariant.String)
        bearbeiter_fld.setAlias('Bearbeiter')

        erfassungsart_id_fld = QgsField("erfassungsart_id", QVariant.Int)

        erfassungsart_name_fld = QgsField("erfassungsart_name", QVariant.String)

        mci_fld = QgsField("mci", QVariant.List)

        awb_fld = QgsField("awb", QVariant.Int)

        self.feature_fields.append(abgrenzung_id_fld)
        self.feature_fields.append(jahr_fld)
        self.feature_fields.append(status_id_fld)
        self.feature_fields.append(status_name_fld)
        self.feature_fields.append(bearbeiter_fld)
        self.feature_fields.append(erfassungsart_id_fld)
        self.feature_fields.append(erfassungsart_name_fld)
        self.feature_fields.append(mci_fld)
        self.feature_fields.append(awb_fld)

    def setFeatureAttributes(self, feature, mci):
        super().setFeatureAttributes(feature, mci)

        feature['abgrenzung_id'] = mci.id
        feature['jahr'] = mci.jahr
        feature['status_id'] = mci.status_id
        feature['status_name'] = mci.rel_status.name_short
        feature['bearbeiter'] = mci.bearbeiter
        feature['erfassungsart_id'] = mci.erfassungsart_id
        feature['erfassungsart_name'] = mci.rel_erfassungsart.name
        feature['mci'] = [mci]
        feature['awb'] = mci.awb

    def changeAttributes(self, feature, mci):

        attrib = {0: mci.id,
                  1: mci.jahr,
                  2: mci.status_id,
                  3: mci.rel_status.name_short,
                  4: mci.bearbeiter,
                  5: mci.erfassungsart_id,
                  6: mci.rel_erfassungsart.name,
                  7: [mci],
                  8: mci.awb
                  }

        self._gis_layer.changeAttributeValues(feature.id(),
                                              attrib)

    # def updateFeatureAttributes(self, *args):
    #     super().updateFeatureAttributes(args)
    #
    #     new_mci = args[0][0]
    #
    #     self.setFeatureAttributes(self.current_feature, new_mci)

    def signals(self):
        super().signals()

        self.uiAddDataTbtn.clicked.disconnect(self.add_row)

    def finalInit(self):
        super().finalInit()

        self.setStretchMethod(2)

        # self.view.setSelectionMode(QgsAttributeTableView.SingleSelection)

        self.view.setColumnHidden(0, True)
        self.view.setColumnHidden(2, True)
        self.view.setColumnHidden(5, True)
        self.view.setColumnHidden(7, True)
        self.view.setColumnHidden(8, True)

        self.view.sortByColumn(1, Qt.DescendingOrder)

        """setzt bestimmte spaltenbreiten"""
        self.view.setColumnWidth(4, 200)
        """"""

        """passe die Zeilenhöhen an den Inhalt an"""
        # self.view.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        """"""

        # """durchsuche ob eine abgrenzung als 'awb' gesetzt ist und selektiere
        # diese dann"""
        # for feat in self._gis_layer.getFeatures():
        #     if feat.attribute('awb') == 1:
        #         self._gis_layer.select([feat.id()])
        #         self.selectedRowsChanged()
        #         self.parent.selectedAbgrenzungChanged()
        #
        # """trenne das signal des corner-buttons und entferne das icon"""
        # self.view.uiCornerButton.clicked.disconnect()
        # self.view.uiCornerButton.setStyleSheet("")
        # """"""

    def updateMaintable(self):

        super().updateMaintable()

    def getDeleteInfo(self, index=None):
        super().getDeleteInfo(index)

        del_info = self.filter_proxy.data(
            self.filter_proxy.index(
                index.row(), 1))

        return del_info
