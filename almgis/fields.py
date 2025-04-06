from qga.fields import QgaField
from qgis.PyQt.QtCore import QVariant

class GeneralField:

    class Id(QgaField):

        def __init__(self, name='id', field_type=QVariant.String):
            super().__init__(name, field_type)

            self.field_value = 'id'

            self.visible = False
            # self.dmi_attr = 'rel_gem_type.id'

        # def fieldValue(self, dmi):
        #     return dmi.rel_gem_type.id

    class TypeId(QgaField):

        def __init__(self, name='type_id', field_type=QVariant.Int):
            super().__init__(name, field_type)

            self.field_value = 'type_id'

            self.visible = False


class KontaktField:
    """
    represent the fields according to the data_model 'Kontakt'
    """

    class VertreterId(QgaField):

        def __init__(self, name='vertreter_id', field_type=QVariant.Int):
            super().__init__(name, field_type)

            self.field_value = 'rel_vertreter.id'

            self.visible = False

    class Name(QgaField):

        def __init__(self, name='name', field_type=QVariant.String):
            super().__init__(name, field_type)

            self.setAlias('Name')
            self.field_value = 'name'

            # self.dmi_attr = 'name'
            # self.field_value = self.dmi.name

        # def fieldValue(self, dmi):
        #     self.dmi = dmi
        #     return self.dmi.name

    class Adresse(QgaField):

        def __init__(self, name='adresse', field_type=QVariant.String):
            super().__init__(name, field_type)

            self.setAlias('Adresse')
            self.field_value = 'adresse'
            # self.dmi_attr = 'adresse'

        # def fieldValue(self, dmi):
        #     return dmi.adresse

    class Strasse(QgaField):

        def __init__(self, name='strasse', field_type=QVariant.String):
            super().__init__(name, field_type)

            self.setAlias('Straße')
            self.field_value = 'strasse'

    class TelefonAll(QgaField):

        def __init__(self, name='telefon_all', field_type=QVariant.String):
            super().__init__(name, field_type)

            self.setAlias('Telefonnummern')
            self.field_value = 'telefon_all'
            # self.dmi_attr = 'telefon_all'

        # def fieldValue(self, dmi):
        #     return dmi.telefon_all
