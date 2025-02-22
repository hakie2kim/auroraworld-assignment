from sqlalchemy import Table, Column, Integer, ForeignKey, Boolean
from app.db.database import Base

link_shares = Table('link_shares', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('link_id', Integer, ForeignKey('links.id')),
    Column('can_write', Boolean, default=False)
)
