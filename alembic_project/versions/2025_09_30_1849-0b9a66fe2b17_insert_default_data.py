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

# revision identifiers, used by Alembic.
revision: str = '0b9a66fe2b17'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create table
    # op.create_table(
    #     'users',
    #     sa.Column('id', sa.Integer, primary_key=True),
    #     sa.Column('name', sa.String(50), nullable=False),
    #     sa.Column('email', sa.String(100), nullable=False, unique=True),
    #     sa.Column('age', sa.Integer),
    # )

    sess = ProjectSessionCls()

    new_kont = DmKontakt()
    new_kont.nachname = 'A1'
    sess.add(new_kont)
    sess.commit()
    sess.close()

    # Define SQLAlchemy table object for bulk_insert
    # kontakt_table = table('_tbl_alm_kontakt',
    #                       column('uuid', sa.String(100)),
    #                       column('nachname', sa.String(100)),
    #                       column('vorname', sa.String(100)),
    #                       column('plz', sa.String(100)),
    #                       column('ort', sa.String(100)),
    #                       column('blank_value', sa.Boolean),
    #                       column('inactive', sa.Boolean),
    #                       column('not_delete', sa.Boolean),
    #                       column('user_edit', sa.String(100)),
    #                       column('time_edit', sa.String(100))
    #                       )
    #
    # # Insert seed data
    # op.bulk_insert(kontakt_table, [
    #     {'nachname': 'AAA', 'vorname': 'Alice', 'plz': '123', 'ort': 'TT',
    #      'blank_value': True, 'inactive': True, 'not_delete': True, 'user_edit': 'max', 'time_edit': '2025-09-30'},
    #     {'nachname': 'BBB', 'vorname': 'Bob', 'plz': '456', 'ort': 'ZZ',
    #      'blank_value': True, 'inactive': True, 'not_delete': True, 'user_edit': 'max', 'time_edit': '2025-09-30'}
    # ])
    print('data inserted!')


def downgrade() -> None:
    """Downgrade schema."""
    pass
