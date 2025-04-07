from operator import attrgetter

from qga.fields import QgaField
from qgis.PyQt.QtCore import QVariant

from almgis.data_model import BGstZuordnung, BGst


class GeneralField:

    class Id(QgaField):

        def __init__(self, name='id', field_type=QVariant.String):
            super().__init__(name, field_type)

            self.dmi_attr = 'id'
            self.setAlias('ID')
            self.visible = False

    class TypeId(QgaField):

        def __init__(self, name='type_id', field_type=QVariant.Int):
            super().__init__(name, field_type)

            self.dmi_attr = 'type_id'
            self.setAlias('Typ ID')
            self.visible = False


class KontaktField:
    """
    represent the fields according to the data_model 'Kontakt'
    """

    class VertreterId(QgaField):

        def __init__(self, name='vertreter_id', field_type=QVariant.Int):
            super().__init__(name, field_type)

            self.dmi_attr = 'rel_vertreter.id'
            self.setAlias('Vertreter ID')

            self.visible = False

    class Name(QgaField):

        def __init__(self, name='name', field_type=QVariant.String):
            super().__init__(name, field_type)

            self.setAlias('Name')
            self.dmi_attr = 'name'

    class Adresse(QgaField):

        def __init__(self, name='adresse', field_type=QVariant.String):
            super().__init__(name, field_type)

            self.setAlias('Adresse')
            self.dmi_attr = 'adresse'

    class Strasse(QgaField):

        def __init__(self, name='strasse', field_type=QVariant.String):
            super().__init__(name, field_type)

            self.setAlias('Straße')
            self.dmi_attr = 'strasse'

    class TelefonAll(QgaField):

        def __init__(self, name='telefon_all', field_type=QVariant.String):
            super().__init__(name, field_type)

            self.setAlias('Telefonnummern')
            self.dmi_attr = 'telefon_all'


class GstField:

    class KgGst(QgaField):

        def __init__(self, name='kg_gst', field_type=QVariant.String):
            super().__init__(name, field_type)

            self.setAlias('Kg/Gst')
            self.dmi_attr = 'kg_gst'


class GstZuordnungField:

    class KgGst(QgaField):

        dmc = BGstZuordnung

        def __init__(self, name='kg_gst', field_type=QVariant.String):
            super().__init__(name, field_type)

            self.setAlias('Kg/Gst')
            self.dmi_attr = 'kg_gst'


    class AktId(QgaField):
        dmc = BGstZuordnung

        def __init__(self, name='akt_id', field_type=QVariant.Int):
            super().__init__(name, field_type)

            self.dmi_attr = 'rel_akt.id'


    class AktName(QgaField):
        dmc = BGstZuordnung

        def __init__(self, name='akt_name', field_type=QVariant.String):
            super().__init__(name, field_type)

            self.setAlias('Aktenname')
            self.dmi_attr = 'rel_akt.name'

        # def getFieldValue(self, dmi):
        #     return dmi.rel_akt.name

    class AwbStatusId(QgaField):
        dmc = BGstZuordnung

        def __init__(self, name='awb_status_id', field_type=QVariant.Int):
            super().__init__(name, field_type)

            self.dmi_attr = 'awb_status_id'

    class RechtsgrundlageId(QgaField):
        dmc = BGstZuordnung

        def __init__(self, name='rechtsgrundlage_id', field_type=QVariant.Int):
            super().__init__(name, field_type)

            self.dmi_attr = 'rechtsgrundlage_id'

    class GstLastGbArea(QgaField):
        """
        GB-Fläche der letzten Gst-Version
        """
        dmc = BGst

        def __init__(self, name='last_gb_area', field_type=QVariant.Int):
            super().__init__(name, field_type)

            self.setAlias('GB Fläche')

        def getFieldValue(self, dmi):

            gst_versionen_list = dmi.rel_gst.rel_alm_gst_version
            last_gst = max(gst_versionen_list,
                           key=attrgetter('rel_alm_gst_ez.datenstand'))

            gb_area = 0
            for nutz in last_gst.rel_alm_gst_nutzung:
                gb_area = gb_area + nutz.area

            return gb_area


    class GstLastKoppelArea(QgaField):
        """
        Summe der Koppel-Verschnittflächen für die letzte Gst-Version
        (aus der Tabelle 'cut_koppel_aktuell_gstversion')
        """
        dmc = BGst

        def __init__(self, name='last_koppel_area', field_type=QVariant.Int):
            super().__init__(name, field_type)

            self.setAlias('davon beweidet')

        def getFieldValue(self, dmi):
            """
            berechne die GB-Fläche der letzten Gst-Version
            """

            """last gst"""
            gst_versionen_list = dmi.rel_gst.rel_alm_gst_version
            last_gst = max(gst_versionen_list,
                           key=attrgetter('rel_alm_gst_ez.datenstand'))
            """"""

            """summe der koppel-verschnitt-flächen pro gst"""
            sum_cut = 0.00
            for cut in last_gst.rel_cut_koppel_gst:
                sum_cut = sum_cut + cut.cut_area
            """"""

            return sum_cut

    class GstLastGisArea(QgaField):
        """
        GB-Fläche der letzten Gst-Version
        """
        dmc = BGst

        def __init__(self, name='last_gis_area', field_type=QVariant.Double):
            super().__init__(name, field_type)

            self.setAlias('GIS Fläche')
            self.dmi_attr = 'rel_gst.gst_latest.gst_gis_area'

        # def getFieldValue(self, dmi):
        #
        #
        #
        #     return str(dmi.rel_gst.gst_latest.gst_gis_area)

        #     gst_versionen_list = dmi.rel_gst.rel_alm_gst_version
        #     last_gst = max(gst_versionen_list,
        #                    key=attrgetter('rel_alm_gst_ez.datenstand'))
        #
        #     gb_area = 0
        #     for nutz in last_gst.rel_alm_gst_nutzung:
        #         gb_area = gb_area + nutz.area
        #
        #     return gb_area
