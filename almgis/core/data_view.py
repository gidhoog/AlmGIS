from qga.core.data_view import QgaDataView, QgaTableModel


class AlmDataView(QgaDataView):

    def __init__(self, gis_mode=False):
        super(__class__, self).__init__(gis_mode)

    def __call__(self, *args, **kwargs):
        pass


class AlmTableModel(QgaTableModel):

    def __init__(self, layerCache=None,
                 columns=None, parent=None):
        super(AlmTableModel, self).__init__(layerCache, columns, parent)
