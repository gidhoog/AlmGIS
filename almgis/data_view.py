from qga.data_view import QgaDataView

from almgis import DbSession


# from almgis import Config


class AlmDataView(QgaDataView):

    # colors = Config.Colors

    def __init__(self, parent=None, gis_mode=False):
        super(__class__, self).__init__(parent, gis_mode)

        self.session = DbSession()


