import random
import string
from sqlalchemy.orm import Session
from app import models

def generate_short_code(length: int = 6) -> str:
    chars = string.ascii_letters + string.digits
    return "".join(random.choices(chars, k=length))

def create_short_url(db: Session, original_url: str) -> models.URL:
    code = generate_short_code()
    while db.query(models.URL).filter(models.URL.short_code == code).first():
        code = generate_short_code()

    db_url = models.URL(short_code=code, original_url=original_url)
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    return db_url

def get_url_by_code(db: Session, short_code: str) -> models.URL | None:
    return db.query(models.URL).filter(models.URL.short_code == short_code).first()

def increment_clicks(db: Session, db_url: models.URL):
    db_url.clicks += 1
    db.commit()