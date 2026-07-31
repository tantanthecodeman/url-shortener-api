from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app import models, schemas, crud
from app.database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="URL Shortener API")

BASE_URL = "http://localhost:8000"

@app.post("/shorten", response_model=schemas.URLResponse)
def shorten_url(payload: schemas.URLCreate, db: Session = Depends(get_db)):
    db_url = crud.create_short_url(db, str(payload.url))
    return schemas.URLResponse(
        short_code=db_url.short_code,
        short_url=f"{BASE_URL}/{db_url.short_code}",
        original_url=db_url.original_url,
        created_at=db_url.created_at,
    )

@app.get("/{short_code}")
def redirect_to_url(short_code: str, db: Session = Depends(get_db)):
    db_url = crud.get_url_by_code(db, short_code)
    if not db_url:
        raise HTTPException(status_code=404, detail="Short URL not found")
    crud.increment_clicks(db, db_url)
    return RedirectResponse(url=db_url.original_url)