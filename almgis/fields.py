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
        dmc = BGst

        def __init__(self, name='rechtsgrundlage_id', field_type=QVariant.Int):
            super().__init__(name, field_type)

            self.dmi_attr = 'rel_gst'
