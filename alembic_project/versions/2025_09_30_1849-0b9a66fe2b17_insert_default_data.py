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
from almgis.database.models import DmKontakt
from almgis.database.sessions import session_cm

# revision identifiers, used by Alembic.
revision: str = '0b9a66fe2b17'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    # upgrade_sessio = ProjectSessionCls()

    new_kont_01 = DmKontakt()
    new_kont_01.nachname = 'A1'

    new_kont_02 = DmKontakt()
    new_kont_02.nachname = 'B1'

    new_kont_03 = DmKontakt()
    new_kont_03.nachname = 'C1'

    with session_cm(name='insert default data') as session:
        session.add(new_kont_01)
        session.add(new_kont_02)
        session.add(new_kont_03)

    print('data inserted!')


def downgrade() -> None:
    """Downgrade schema."""
    pass
