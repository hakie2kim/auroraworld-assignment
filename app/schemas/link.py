from pydantic import BaseModel
from typing import Optional

class LinkBase(BaseModel):
    name: str
    url: str
    category: Optional[str] = None

class LinkCreate(LinkBase):
    pass

class LinkOut(LinkBase):
    id: int
    created_by: int

    class Config:
        orm_mode = True

class LinkUpdate(BaseModel):
    name: Optional[str] = None
    url: Optional[str] = None
    category: Optional[str] = None

class LinkShareCreate(BaseModel):
    user_id: int
    can_write: bool = False
