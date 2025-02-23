from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.security import get_current_user
from app.db.database import get_db
from app.models.link import Link
from app.models.user import User
from app.schemas.link import LinkCreate, LinkOut

router = APIRouter()

@router.post("/links", response_model=LinkOut)
def create_link(link: LinkCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_link = Link(**link.dict(), created_by=current_user.id)
    db.add(new_link)
    db.commit()
    db.refresh(new_link)
    return new_link
