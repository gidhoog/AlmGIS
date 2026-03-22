from qga import DataModel, Qga

from almgis.core.settings import AlmSettingsManager
from almgis.database.models import DmGst, DmGstVersion, DmGstEz, \
    DmGstEigentuemer, DmGstNutzung

DataModel.dm_gst_cls = DmGst
DataModel.dm_gst_version_cls = DmGstVersion
DataModel.dm_gst_ez_cls = DmGstEz
DataModel.dm_gst_eigentuemer_cls = DmGstEigentuemer
DataModel.dm_gst_nutzung_cls = DmGstNutzung

# Qga.SM = AlmSettingsManager()