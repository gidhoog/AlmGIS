"""Create users table and insert seed data

Revision ID: 1
Revises: None
Create Date: 2025-09-30 15:42:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column

# revision identifiers, used by Alembic.
revision = '1'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Create table
    # op.create_table(
    #     'users',
    #     sa.Column('id', sa.Integer, primary_key=True),
    #     sa.Column('name', sa.String(50), nullable=False),
    #     sa.Column('email', sa.String(100), nullable=False, unique=True),
    #     sa.Column('age', sa.Integer),
    # )

    # Define SQLAlchemy table object for bulk_insert
    kontakt_table = table('_tbl_alm_kontakt',
        column('nachname', sa.String(100)),
        column('vorname', sa.String(100)),
        column('plz', sa.String(100)),
        column('ort', sa.Integer)
    )

    # Insert seed data
    op.bulk_insert(kontakt_table, [
        {'nachname': 'AAA', 'vorname': 'Alice', 'plz': '123', 'ort': 'TT'},
        {'nachname': 'BBB', 'vorname': 'Bob',   'plz': '456',   'ort': 'ZZ'}
    ])

# def downgrade():
#     op.drop_table('users')
