from typing import List

import uvicorn
from fastapi import FastAPI, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from starlette.middleware.cors import CORSMiddleware

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Dependency
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@app.get("/redirect/{hashcode}")
def redirct(hashcode: str, db: Session = Depends(get_db)):
    return RedirectResponse(crud.get_url(db, hashcode), 301)


@app.get("/shorturls", response_model=List[schemas.ShorturlResponse])
def read_shorturls(db: Session = Depends(get_db)):
    return crud.read_shorturls(db)


@app.post("/shorturls")
def create_shorturl(request: schemas.ShorturlRequest, db: Session = Depends(get_db)):
    return crud.create_shorturl(db, request)


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8080)
