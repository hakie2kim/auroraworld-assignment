from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.security import get_current_user
from app.db.database import get_db
from app.models.link import Link
from app.models.user import User
from app.schemas.link import LinkCreate, LinkOut, LinkUpdate

router = APIRouter()

@router.post("/links", response_model=LinkOut)
def create_link(link: LinkCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_link = Link(**link.dict(), created_by=current_user.id)
    db.add(new_link)
    db.commit()
    db.refresh(new_link)
    return new_link

@router.put("/links/{link_id}", response_model=LinkOut)
def update_link(link_id: int, link: LinkUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_link = db.query(Link).filter(Link.id == link_id, Link.created_by == current_user.id).first()
    if not db_link:
        raise HTTPException(status_code=404, detail="Link not found")
    for key, value in link.dict(exclude_unset=True).items():
        setattr(db_link, key, value)
    db.commit()
    db.refresh(db_link)
    return db_link
