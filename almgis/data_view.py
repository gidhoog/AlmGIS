from qga.data_view import QgaDataView

from almgis import AlmSessionCls


# from almgis import DbSession


class AlmDataView(QgaDataView):

    def __init__(self, parent=None, gis_mode=False):
        super(__class__, self).__init__(parent, gis_mode)

        self.session = AlmSessionCls()

    def __call__(self, *args, **kwargs):
        pass
