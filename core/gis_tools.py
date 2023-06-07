from datetime import datetime
from PyQt5.QtWidgets import QMessageBox
import processing
from processing.core.Processing import Processing
from qgis.core import QgsVectorLayer, edit, QgsFeature, \
    QgsProcessing, QgsProcessingFeatureSourceDefinition, QgsFeatureRequest
from core.config import alm_data_db_path


def cut_komplex_gstversion():
    """
    methode zu verschneiden der layer komplexe ('a_alm_komplexe') und der
    im alm- und weidebuch eingetragenen grundstücke ('v_alm_gst_awbuch');

    im verschnittlayer ('a_cut_komplex_gstversion') werden die id's der beiden
    layer und der zeitpunkt des verschnittes eingetragen
    """

    """init 'Processing' um 'processing' in einer standalone-anwendung zu 
    ermöglichen"""
    Processing.initialize()
    """"""

    """aktuelle Zeit"""
    cut_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    """"""

    try:
        """definiere den verschnittlayer"""
        layer_intersect = QgsVectorLayer(
            str(alm_data_db_path.absolute()) + '|layername=a_cut_komplex_gstversion',
            'z_layer',
            'ogr'
        )
        """"""

        """lösche alle bisherigen features auf dem verschnittlayer"""
        if layer_intersect.isValid():
            with edit(layer_intersect):
                listOfIds = [feat.id() for feat in layer_intersect.getFeatures()]
                layer_intersect.deleteFeatures(listOfIds)
        """"""

        """führe den verschnitt durch und definiere eine variable mit dem
        virtuellen verschnittlayer"""
        intersect = processing.run("native:intersection", {
            'INPUT': QgsProcessingFeatureSourceDefinition(
                str(alm_data_db_path.absolute()) + '|layername=a_alm_komplexe',
                selectedFeaturesOnly=False,
                featureLimit=-1,
                flags=QgsProcessingFeatureSourceDefinition.FlagOverrideDefaultGeometryCheck,
                geometryCheck=QgsFeatureRequest.GeometryNoCheck),
            'OVERLAY': QgsProcessingFeatureSourceDefinition(
                str(alm_data_db_path.absolute()) + '|layername=v_alm_gst_awbuch',
                selectedFeaturesOnly=False,
                featureLimit=-1,
                flags=QgsProcessingFeatureSourceDefinition.FlagOverrideDefaultGeometryCheck,
                geometryCheck=QgsFeatureRequest.GeometryNoCheck),
            'INPUT_FIELDS': [],
            'OVERLAY_FIELDS': [],
            'OVERLAY_FIELDS_PREFIX': '',
            'OUTPUT': 'TEMPORARY_OUTPUT',
            'GRID_SIZE': None})
        virt_intersection = intersect['OUTPUT']
        """"""

        """hole alle features aus dem Verschnittergebnis"""
        intersect_features = virt_intersection.getFeatures()
        """"""

        """definiere eine liste mit den neuen features"""
        new_features = []

        # """nur zur Info, die Attributnamen des Verschnittergebnisses:"""
        # print(f'********************************************')
        # intersect_dp = virt_intersection.dataProvider()
        # layer_attrib_names = intersect_dp.fields()
        # intersect_attributeList = layer_attrib_names.toList()
        # for intersect_attribute in intersect_attributeList:
        #     print(intersect_attribute.name())
        # print(f'********************************************')
        # """"""

        """füge die neuen features mit den neuen attributen in die liste 
        'new_features' ein"""
        for feat in intersect_features:
            cut_geom = feat.geometry()
            komplex_id = feat['id']
            gstversion_id = feat['gstversion_id']

            new_feat = QgsFeature()
            new_feat.setAttributes \
                ([None, komplex_id, gstversion_id, cut_timestamp])
            new_feat.setGeometry(cut_geom)

            new_features.append(new_feat)
        """"""

        """schreibe die features der liste 'new_features' in den
        verschnittlayer und speichere in der datenbank"""
        layer_intersect_data = layer_intersect.dataProvider()
        layer_intersect_data.addFeatures(new_features)

        layer_intersect.commitChanges()
        """"""

    except:
        """der verschnitt kann nicht durchgeführt werden"""
        msg = QMessageBox()
        msg.setText("Der Verschnitt von Komplexen und Grundstücken die im "
                    "AW-Buch eingetragen sind konnte nicht "
                    "durchgeführt werden.")
        msg.exec_()
        """"""
