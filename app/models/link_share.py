from sqlalchemy import Column, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base

class LinkShare(Base):
    __tablename__ = "link_shares"

    id = Column(Integer, primary_key=True, index=True)
    link_id = Column(Integer, ForeignKey("links.id", ondelete="CASCADE"))
    shared_with = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    can_write = Column(Boolean, default=False)

    link = relationship("Link", back_populates="shares")
    shared_user = relationship("User", back_populates="shared_links")