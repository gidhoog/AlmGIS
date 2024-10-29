from datetime import datetime
from qgis.PyQt.QtWidgets import QMessageBox

# from qgis import processing

import processing
from processing.core.Processing import Processing
from processing.tools import dataobjects

from qgis.core import QgsVectorLayer, edit, QgsFeature, \
    QgsProcessingFeatureSourceDefinition, QgsFeatureRequest
from app_core.config import alm_data_db_path


def cut_koppel_gstversion(koppel_layer):
    """
    methode zu verschneiden der layer koppel_aktuell ('v_koppel_aktuell') und der
    Grundstücke, die einem Akt zugeordnet sind ('v_alm_gst')

    im verschnittlayer ('a_cut_koppel_aktuell_gstversion') werden die id's der beiden
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
            str(alm_data_db_path.absolute()) + '|layername=a_cut_koppel_aktuell_gstversion',
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

        """vermeide generell einen Geometrie-Check beim Verschnitt für beide (!!)
        Layer"""
        context = dataobjects.createContext()
        context.setInvalidGeometryCheck(QgsFeatureRequest.GeometryNoCheck)
        """"""

        """führe den verschnitt durch und definiere eine variable mit dem
        virtuellen verschnittlayer"""
        intersect = processing.run("native:intersection", {
            'INPUT': koppel_layer,
            'OVERLAY': QgsProcessingFeatureSourceDefinition(
                str(alm_data_db_path.absolute()) + '|layername=v_alm_gst',
                selectedFeaturesOnly=False,
                featureLimit=-1,
                flags=QgsProcessingFeatureSourceDefinition.FlagOverrideDefaultGeometryCheck,
                geometryCheck=QgsFeatureRequest.GeometryNoCheck),
            'INPUT_FIELDS': [],
            'OVERLAY_FIELDS': [],
            'OVERLAY_FIELDS_PREFIX': '',
            'OUTPUT': 'TEMPORARY_OUTPUT',
            'GRID_SIZE': None},
            context=context
                                   )

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
            koppel_id = feat['id']
            gstversion_id = feat['gstversion_id']

            new_feat = QgsFeature()
            new_feat.setAttributes \
                ([None, koppel_id, gstversion_id, cut_timestamp])
            new_feat.setGeometry(cut_geom)

            new_features.append(new_feat)
        """"""

        """schreibe die features der liste 'new_features' in den
        verschnittlayer und speichere in der datenbank"""
        layer_intersect_data = layer_intersect.dataProvider()
        layer_intersect_data.addFeatures(new_features)

        layer_intersect.commitChanges()
        """"""

    except Exception as e:
        """der verschnitt kann nicht durchgeführt werden"""
        msg = QMessageBox()
        msg.setWindowTitle('Fehlermeldung')
        msg.setText(f"Der Verschnitt der aktuellen Koppeln und Grundstücken die im "
                    f"AW-Buch eingetragen sind konnte aus folgendem Grund nicht "
                    f"durchgeführt werden: \n\n{e}")
        msg.exec_()
        """"""
