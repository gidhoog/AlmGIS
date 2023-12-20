from pathlib import Path

from qgis._core import QgsField
from qgis.PyQt.QtCore import QVariant
from qgis.core import QgsVectorLayer, QgsRasterLayer
from core.config import alm_data_db_path


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
        self.base = True
        setLayerStyle(self, 'koppel_gelb')

