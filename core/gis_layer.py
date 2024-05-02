from pathlib import Path

from qgis._core import QgsField, QgsFeature, QgsGeometry
from qgis.PyQt.QtCore import QVariant
from qgis.core import QgsVectorLayer, QgsRasterLayer
from core.config import alm_data_db_path
from core.gis_item import GisItem
from core.scopes.koppel.koppel_item import KoppelItem

from geoalchemy2.shape import to_shape


def getGisLayer(layer_instance, base_id_column=None,
                id_val=None, feat_filt_expr=None):
    """
    methode zum erstellen eines standard-gis-layer

    :param layer_instance: BGisStyle
    :param base_id_column: spaltename der gefiltert wird
    :param id_val: wert mit dem gefiltert wird
    :param feat_filt_expr: ausdruck mit dem gefiltert werden soll (als string)
    :return: GisRasterLayer oder GisVectorLayer
    """

    """definiere variablen die für die layererstellung notwendig sind"""
    name = f'{layer_instance.rel_gis_layer.name} ({layer_instance.name})'
    uri = layer_instance.rel_gis_layer.uri
    provider = layer_instance.rel_gis_layer.provider
    """"""

    """erstelle einen raster-layer"""
    if layer_instance.rel_gis_layer.layer_typ == 'Raster':
        layer = GisRasterLayer(uri, name, provider)
    """"""

    """erstelle einen vector-layer"""
    if layer_instance.rel_gis_layer.layer_typ in ['Punkte', 'Linie', 'Polygone']:

        """erzeuge den datenbank-pfad als 'forward-slash'"""
        gis_db_string = str(alm_data_db_path.as_posix())
        """"""
        if not layer_instance.rel_gis_layer.table_name:
            uri = layer_instance.rel_gis_layer.uri
        else:
            """erzeuge einen uri-string für die layererstellung"""
            if layer_instance.rel_gis_layer.table_name:
                uri = gis_db_string + "|layername=" + layer_instance.rel_gis_layer.table_name
            """"""

            """füge einen feature-filter an den uri-string falls gefordert"""
            if base_id_column:
                uri = uri + "|subset=\"" + base_id_column + "\" = '" + str(id_val) + "'"
            # if feat_filt_expr:
            #     e = f'{feat_filt_expr}'
            #     expr = feat_filt_expr.replace("<id_val>", str(id_val))
            #     expr_str = f'{expr}'
            #     uri = uri + "|subset=" + expr_str
            """"""

            # "akt_id" = 54  AND "jahr" = {self.parent.parent().komplex_jahr}

        layer = GisVectorLayer(uri, name, provider)

        # if feat_filt_expr:
        #
        #     layer.setSubsetString('"akt_id" = 54')
    """"""
    return layer


def setLayerStyle(layer: QgsVectorLayer, qml_file_name: str):
    """
    setze mit einem qml-file den stil eines layers
    """

    qml_path = str(Path()
                   .absolute()
                   .joinpath('core')
                   .joinpath('styles')
                   .joinpath(qml_file_name)) + ".qml"
    layer.loadNamedStyle(qml_path)
    layer.triggerRepaint()


class Feature(QgsFeature):

    _mci = None

    def __init__(self, fields, parent=None):
        super().__init__(fields)

        self.parent = parent


class GisLayer:
    """
    basis-class für einen layer
    """
    base = False
    back = False
    style_id = None
    dataform_class = None
    add = False



class GisRasterLayer(QgsRasterLayer, GisLayer):
    """
    basis-class für einen raster-layer
    """

class GisVectorLayer(QgsVectorLayer, GisLayer):
    """
    basis-class für einen vector-layer
    """


class AktAllLayer(QgsVectorLayer):
    """
    GIS-Layer für zugeordnete Grundstücke
    """

    def __init__(self, path: str = ...,
                 baseName: str = ...,
                 providerLib: str = ...,
                 options: 'QgsVectorLayer.LayerOptions' = QgsVectorLayer.LayerOptions(),
                 feature_fields=None) -> None:
        super().__init__(path, baseName, providerLib, options)

        self.data_provider = self.dataProvider()

        self.data_provider.addAttributes(feature_fields)

        self.updateFields()

        self.back = False
        self.base = False


class GstAllLayer(QgsVectorLayer):
    """
    GIS-Layer für alle Gst die einem Akt zugeordnet werden können
    """

    def __init__(self, path: str = ...,
                 baseName: str = ...,
                 providerLib: str = ...,
                 options: 'QgsVectorLayer.LayerOptions' = QgsVectorLayer.LayerOptions(),
                 feature_fields=None) -> None:
        super().__init__(path, baseName, providerLib, options)

        self.data_provider = self.dataProvider()

        self.data_provider.addAttributes(feature_fields)

        self.updateFields()

        self.back = False
        self.base = False


class GstPreSelLayer(QgsVectorLayer):
    """
    GIS-Layer für alle Gst die für die zuordnung zu einem akt vorgemerkt sind
    """

    def __init__(self, path: str = ...,
                 baseName: str = ...,
                 providerLib: str = ...,
                 options: 'QgsVectorLayer.LayerOptions' = QgsVectorLayer.LayerOptions(),
                 feature_fields=None) -> None:
        super().__init__(path, baseName, providerLib, options)

        self.data_provider = self.dataProvider()

        self.data_provider.addAttributes(feature_fields)

        self.updateFields()

        self.back = False
        self.base = False


class KontaktAllLayer(QgsVectorLayer):
    """
    GIS-Layer für zugeordnete Grundstücke
    """

    def __init__(self, path: str = ...,
                 baseName: str = ...,
                 providerLib: str = ...,
                 options: 'QgsVectorLayer.LayerOptions' = QgsVectorLayer.LayerOptions(),
                 feature_fields=None) -> None:
        super().__init__(path, baseName, providerLib, options)

        self.data_provider = self.dataProvider()

        self.data_provider.addAttributes(feature_fields)

        self.updateFields()

        self.back = False
        self.base = False


class GstZuordLayer(QgsVectorLayer):
    """
    GIS-Layer für zugeordnete Grundstücke
    """

    def __init__(self, path: str = ...,
                 baseName: str = ...,
                 providerLib: str = ...,
                 options: 'QgsVectorLayer.LayerOptions' = QgsVectorLayer.LayerOptions(),
                 feature_fields=None) -> None:
        super().__init__(path, baseName, providerLib, options)

        self.data_provider = self.dataProvider()

        self.data_provider.addAttributes(feature_fields)

        # self.data_provider.addAttributes([QgsField("gst_version_id", QVariant.Int),
        #                        QgsField("gst", QVariant.String),
        #                        QgsField("ez", QVariant.Int),
        #                        QgsField("kgnr", QVariant.Int),
        #                        QgsField("kgname", QVariant.String),
        #                        QgsField("awb_id", QVariant.Int),
        #                        QgsField("recht_id", QVariant.Int),
        #                        QgsField("gis_area", QVariant.String),
        #                        QgsField("datenstand", QVariant.String)])

        self.updateFields()

        self.back = False
        self.base = False
        # setLayerStyle(self, 'komplex_rot')


class KomplexLayer(QgsVectorLayer):
    """
    GIS-Layer für Komplexe
    """

    def __init__(self, path: str = ...,
                 baseName: str = ...,
                 providerLib: str = ...,
                 options: 'QgsVectorLayer.LayerOptions' = QgsVectorLayer.LayerOptions()) -> None:
        super().__init__(path, baseName, providerLib, options)

        self.data_provider = self.dataProvider()

        self.data_provider.addAttributes([QgsField("id", QVariant.Int),
                                      QgsField("nr", QVariant.Int),
                                      QgsField("name", QVariant.String)])

        self.updateFields()

        self.back = False
        self.base = False
        setLayerStyle(self, 'komplex_rot')


class KoppelLayer(QgsVectorLayer):
    """
    GIS-Layer für Koppeln
    """

    def __init__(self, path: str = ...,
                 baseName: str = ...,
                 providerLib: str = ...,
                 options: 'QgsVectorLayer.LayerOptions' = QgsVectorLayer.LayerOptions()) -> None:
        super().__init__(path, baseName, providerLib, options)

        self.data_provider = self.dataProvider()

        self.data_provider.addAttributes([QgsField("id", QVariant.Int),
                                      QgsField("name", QVariant.String),
                                      QgsField("bearbeiter", QVariant.String),
                                      QgsField("aw_ha", QVariant.String),
                                      QgsField("aw_proz", QVariant.String),
                                      QgsField("area", QVariant.String)])

        self.updateFields()

        self.back = False
        self.base = False
        # setLayerStyle(self, 'koppel_gelb')
        setLayerStyle(self, 'koppel_test')

    # def appendKoppelItems(self, koppel_inst_list, komplex_itm):
    #
    #     for koppel in koppel_inst_list:
    #         koppel_item = KoppelItem(koppel)
    #
    #         """erzeuge das Koppel-Feature"""
    #         koppel_feat = QgsFeature(self.fields())
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
    #          # added_kop_feat) = self.koppel_dp_new.addFeatures(
    #          #    [koppel_feat])
    #          added_kop_feat) = self.data_provider.addFeatures(
    #             [koppel_feat])
    #         koppel_item.setData(added_kop_feat[0],
    #                             GisItem.Feature_Role)
    #
    #         komplex_itm.appendRow([koppel_item, None, None, None])
