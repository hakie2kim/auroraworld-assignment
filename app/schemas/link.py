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
