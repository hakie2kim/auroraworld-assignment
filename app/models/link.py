from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base
from app.models.association import link_shares


class Link(Base):
    __tablename__ = 'links'
    id = Column(Integer, primary_key=True)
    url = Column(String)
    name = Column(String)
    category = Column(String)
    created_by = Column(Integer, ForeignKey('users.id'))

    shared_users = relationship('User', secondary=link_shares, back_populates='shared_links')
    owner = relationship("User", back_populates="owned_links", foreign_keys=[created_by])
