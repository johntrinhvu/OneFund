from sqlalchemy.orm import Session
import models

def get_user_by_google_sub(db: Session, sub: str) -> models.User | None:
    return db.query(models.User).filter(models.User.google_sub == sub).first()

def get_user_by_email(db: Session, email: str) -> models.User | None:
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, *, sub: str, email: str, name: str | None, picture: str | None) -> models.User:
    user = models.User(google_sub=sub, email=email, name=name, picture=picture)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
