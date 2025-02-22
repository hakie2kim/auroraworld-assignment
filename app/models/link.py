from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.database import Base
from app.models.association import link_shares


class Link(Base):
    __tablename__ = 'links'
    id = Column(Integer, primary_key=True)
    url = Column(String)
    name = Column(String)
    category = Column(String)

    shared_users = relationship('User', secondary=link_shares, back_populates='shared_links')
