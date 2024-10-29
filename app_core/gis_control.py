

class GisControl:
    """
    baseclass zur erstellung und überwachung einer relation zwischen einem
    main_gis layer und einer daten-tabelle;
    z.b. wenn ein datensatz in der tabelle ausgewählt wird, wird das entsprechende
    feature im entsprechenden gis-layer markiert
    """

    linked_gis_widgets = {}  # key: layer_style_id; value: main_table-name

    def selectRows(self, layer_style_id, entity_ids):
        """
        wähle zeilen in einem main_table mittels des entity_id's
        :param layer_style_id: id des layer_style im main_gis
        :param entity_ids: liste der ausgewählten entity_id's
        :return:
        """
        linked_maintable = self.linked_gis_widgets[layer_style_id]

        """setze 'selected_rows_id' der verbundenen tabele um die aktion für die
        auswahl der zeilen aufzurufen"""
        linked_maintable.selected_rows_id = entity_ids

    def selectFeatures(self, table):
        """
        markiere die feature in einem main_gis layer

        :param table: name der tabelle, deren zeilen markiert werden sollen
        :return:
        """
        self.guiMainGis.selectLayer(table.gis_relation['gis_layer_style_id'],
                                    table.selected_rows_id)

    def activateGisControl(self):
        """
        aktiviere die verbindung der verbundenen elemente die im
        dict 'linked_gis_widgets' gelistet sind;

        rufe diese methode am ende des widget-settings auf (e.g. 'finalEntitySettings');

        ohne diesem aufruf funktioniert die verbindung zwischen datentabelle
        und gis-layer nicht!

        :return:
        """

        for table in self.linked_gis_widgets:

            main_table = self.linked_gis_widgets[table]

            main_table.data_view.selectionModel().selectionChanged\
                .connect(lambda x, y, table=main_table: self.selectFeatures(table))
