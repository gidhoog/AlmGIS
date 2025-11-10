from qga.core.data_view import QgaDataView, QgaTableModel

# from almgis import settings_colors
from qga import Qga


# from almgis import DbSession


class AlmDataView(QgaDataView):

    # _entity_dialog_class = AlmEntityDialog

    # settings_colors = settings_colors

    def __init__(self, gis_mode=False):
        super(__class__, self).__init__(gis_mode)

        # self.session = Qga.ProjectSessionCls()

    def __call__(self, *args, **kwargs):
        pass


class AlmTableModel(QgaTableModel):

    def __init__(self, layerCache=None,
                 columns=None, parent=None):
        super(AlmTableModel, self).__init__(layerCache, columns, parent)
