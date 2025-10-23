from sqlalchemy.orm import Session
from app import models, schemas
from typing import List, Optional


def create_member(db: Session, member: schemas.MemberCreate) -> models.Member:
    db_member = models.Member(**member.model_dump())
    db.add(db_member)
    db.commit()
    db.refresh(db_member)
    return db_member


def get_member(db: Session, member_id: int) -> Optional[models.Member]:
    return db.query(models.Member).filter(models.Member.id == member_id).first()


def get_member_by_email(db: Session, email: str) -> Optional[models.Member]:
    return db.query(models.Member).filter(models.Member.email == email).first()


def get_members(db: Session, skip: int = 0, limit: int = 100) -> List[models.Member]:
    return db.query(models.Member).offset(skip).limit(limit).all()


def update_member(db: Session, member_id: int, member_update: schemas.MemberUpdate) -> Optional[models.Member]:
    db_member = get_member(db, member_id)
    if not db_member:
        return None

    update_data = member_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_member, field, value)

    db.commit()
    db.refresh(db_member)
    return db_member


def delete_member(db: Session, member_id: int) -> bool:
    db_member = get_member(db, member_id)
    if not db_member:
        return False

    db.delete(db_member)
    db.commit()
    return True
