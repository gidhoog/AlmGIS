from qga.entity_type import QgaEntityTyp

from almgis.scopes.kontakt.kontakt import KontaktEinzel, Kontakt


class KontaktTyp(QgaEntityTyp): ...

class KontaktEinzel(KontaktTyp):

    name = 'Einzelperson'
    name_short = 'E'
    sort = 0
    icon = ":/svg/resources/icons/person.svg"
    ui_class = KontaktEinzel

class KontaktGem(KontaktTyp):

    name = 'Gemeinschaft'
    name_short = 'G'
    sort = 2
    icon = ":/svg/resources/icons/group.svg"
    ui_class = Kontakt