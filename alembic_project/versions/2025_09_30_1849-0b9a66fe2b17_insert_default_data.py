"""insert default data

Revision ID: 0b9a66fe2b17
Revises: 
Create Date: 2025-09-30 18:49:14.708080

"""
from typing import Sequence, Union
from uuid import uuid4

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column

from almgis import ProjectSessionCls
from almgis.database.models import DmKontakt, DmKontaktType, DmKontaktGemTyp
from almgis.database.sessions import session_cm

# revision identifiers, used by Alembic.
revision: str = '0b9a66fe2b17'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    """insert default kontakt type data"""
    kt1 = DmKontaktType()
    kt1.id = 0
    kt1.name = "Einzelperson"
    kt1.name_short = "E"
    kt1.sort = 0
    kt1.icon_01 = ":/svg/icons/person.svg"
    kt1.module = "almgis.core.kontakt.kontakt"
    kt1.type_class = "KontaktEinzel"
    kt1.dmi_class = "BKontaktEinzel"
    kt1.not_delete = 1
    kt1.sys_data = 1

    kt2 = DmKontaktType()
    kt2.id = 1
    kt2.name = "Gemeinschaft"
    kt2.name_short = "G"
    kt2.sort = 0
    kt2.icon_01 = ":/svg/icons/group.svg"
    kt2.module = "almgis.scopes.kontakt.kontakt"
    kt2.type_class = "Kontakt"
    kt2.dmi_class = "BKontaktGem"
    kt2.not_delete = 1
    kt2.sys_data = 1

    with session_cm(name='insert default kontakt types') as kt_session:
        kt_session.add(kt1)
        kt_session.add(kt2)
    """"""

    """insert default kontakt_gem_type"""

    kgt1 = DmKontaktGemTyp()
    kgt1.id = 0
    kgt1.name = '---'
    kgt1.name_short = '-'
    kgt1.sort = 0

    kgt2 = DmKontaktGemTyp()
    kgt2.id = 1
    kgt2.name = 'Weidegenossenschaft'
    kgt2.name_short = 'WG'
    kgt2.sort = 1

    kgt3 = DmKontaktGemTyp()
    kgt3.id = 2
    kgt3.name = 'Weideverein'
    kgt3.name_short = 'WV'
    kgt3.sort = 2

    kgt4 = DmKontaktGemTyp()
    kgt4.id = 3
    kgt4.name = 'Agrargemeinschaft'
    kgt4.name_short = 'AG'
    kgt4.sort = 3

    kgt5 = DmKontaktGemTyp()
    kgt5.id = 4
    kgt5.name = 'Sonstige'
    kgt5.name_short = 'So'
    kgt5.sort = 99

    with session_cm(name='insert default kontakt_gem_type data') as kgt_session:
        kgt_session.add(kgt1)
        kgt_session.add(kgt2)
        kgt_session.add(kgt3)
        kgt_session.add(kgt4)
        kgt_session.add(kgt5)
    """"""

    new_kont_01 = DmKontakt()
    new_kont_01.nachname = 'A1'
    new_kont_01.rel_type = kt1

    new_kont_02 = DmKontakt()
    new_kont_02.nachname = 'B1'
    new_kont_02.rel_type = kt1

    new_kont_03 = DmKontakt()
    new_kont_03.nachname = 'C1'
    new_kont_03.rel_type = kt1

    new_kont_04 = DmKontakt()
    new_kont_04.nachname = 'D1'
    new_kont_04.rel_type = kt1

    new_kont_05 = DmKontakt()
    new_kont_05.nachname = 'E1'
    new_kont_05.rel_type = kt1

    verein1 = DmKontakt()
    verein1.nachname = 'VereinA'
    verein1.rel_vertreter = new_kont_01
    verein1.rel_type = kt2
    verein1.rel_gem_type = kgt3

    with session_cm(name='insert default data') as session:
        session.add(new_kont_01)
        session.add(new_kont_02)
        session.add(new_kont_03)
        session.add(new_kont_04)
        session.add(new_kont_05)

        session.add(verein1)

    print('data inserted!')


def downgrade() -> None:
    """Downgrade schema."""
    pass
