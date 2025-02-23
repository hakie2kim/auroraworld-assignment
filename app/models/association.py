from sqlalchemy import Table, Column, Integer, ForeignKey, Boolean, UniqueConstraint
from app.db.database import Base

link_shares = Table(
    'link_shares',
    Base.metadata,
    Column('id', Integer, primary_key=True),
    Column('user_id', Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
    Column('link_id', Integer, ForeignKey('links.id', ondelete='CASCADE'), nullable=False),
    Column('can_read', Boolean, default=True),
    Column('can_write', Boolean, default=False),
    UniqueConstraint('user_id', 'link_id', name='uq_user_link')
)

