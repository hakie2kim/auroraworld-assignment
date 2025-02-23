from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import or_
from sqlalchemy.orm import Session
from app.core.security import get_current_user
from app.db.database import get_db
from app.models import link_shares
from app.models.link import Link
from app.models.user import User
from app.schemas.link import LinkCreate, LinkOut, LinkUpdate, LinkShareCreate

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

    if db_link.created_by != current_user.id:
        share = db.query(link_shares).filter(
            link_shares.c.link_id == db_link.id,
            link_shares.c.user_id == current_user.id,
            link_shares.c.can_write == True
        ).first()
        if not share:
            raise HTTPException(status_code=403, detail="Not authorized to update this link")

    for key, value in link.dict(exclude_unset=True).items():
        setattr(db_link, key, value)
    db.commit()
    db.refresh(db_link)
    return db_link

@router.delete("/links/{link_id}", status_code=200)
def delete_link(link_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_link = db.query(Link).filter(Link.id == link_id, Link.created_by == current_user.id).first()
    if not db_link:
        raise HTTPException(status_code=404, detail="Link not found")

    # 인가 처리
    if db_link.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this link")

    db.delete(db_link)
    db.commit()
    return {"detail": "Link deleted successfully"}

@router.post("/links/{link_id}/share", response_model=LinkOut)
def share_link(
        link_id: int,
        share_data: LinkShareCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    db_link = db.query(Link).filter(Link.id == link_id, Link.created_by == current_user.id).first()
    if not db_link:
        raise HTTPException(status_code=404, detail="Link not found or you don't have permission")

    if db_link.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to share this link")

    share_with_user = db.query(User).filter(User.id == share_data.user_id).first()
    if not share_with_user:
        raise HTTPException(status_code=404, detail="User to share with not found")

    existing_share = db.query(link_shares).filter(
        link_shares.link_id == link_id,
        link_shares.user_id == share_data.user_id
    ).first()

    if existing_share:
        existing_share.can_read = share_data.can_read
        existing_share.can_write = share_data.can_write
    else:
        new_share = link_shares(link_id=link_id, user_id=share_data.user_id, can_read=share_data.can_read, can_write=share_data.can_write)
        db.add(new_share)

    db.commit()
    db.refresh(db_link)
    return db_link

@router.get("/links", response_model=List[LinkOut])
def search_links(
        name: Optional[str] = Query(None, description="Search by link name"),
        category: Optional[str] = Query(None, description="Filter by category"),
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    query = db.query(Link).filter(
        or_(
            Link.created_by == current_user.id,
            Link.id.in_(
                db.query(link_shares.c.link_id).filter(
                    link_shares.c.user_id == current_user.id,
                    link_shares.c.can_read == True
                )
            )
        )
    )

    if name:
        query = query.filter(Link.name.ilike(f"%{name}%"))

    if category:
        query = query.filter(Link.category == category)

    links = query.all()
    return links
