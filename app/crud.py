import hashlib
from datetime import datetime
from typing import List

from fastapi import HTTPException
from sqlalchemy.orm import Session

from .models import Shorturl
from .schemas import ShorturlResponse, ShorturlRequest

DOMAIN = "http://localhost:8000/redirect/"
HTTP_PREFIX = "http://"
HTTPS_PREFIX = "https://"
UTF8 = "utf-8"


def construct_url(hashcode: str) -> str:
    return DOMAIN + hashcode


def convert_to_response(model: Shorturl) -> ShorturlResponse:
    return ShorturlResponse(id=model.id, url=model.url, createddate=model.createddate,
                            shorturl=construct_url(model.hashcode))

def get_url(db: Session, hashcode: str) -> str:
    shorturl = db.query(Shorturl).filter_by(hashcode=hashcode).first()
    if shorturl is None:
        raise HTTPException(status_code=404, detail="Unable to find URL to redirct")
    return shorturl.url

def read_shorturls(db: Session) -> List[ShorturlResponse]:
    shorturls: list = db.query(Shorturl).all()
    return list(map(lambda shorturl: convert_to_response(shorturl), shorturls))


def check_duplicated_url(db: Session, url: str) -> Shorturl:
    return db.query(Shorturl).filter_by(url=url).first()


def check_duplicated_hashcode(db: Session, hashcode: str) -> Shorturl:
    return db.query(Shorturl).filter_by(hashcode=hashcode).first()


def generate_hash(url: str):
    shake = hashlib.shake_128()
    shake.update(url.encode(UTF8))
    return shake.hexdigest(3)


def build_shorturl(url: str, hashcode: str):
    return Shorturl(url=url, hashcode=hashcode, createddate=datetime.utcnow())


def create_shorturl(db: Session, request: ShorturlRequest) -> ShorturlResponse:
    url: str = request.url

    if not url:
        raise HTTPException(status_code=400, detail="The URL should not be empty")

    if not url.startswith(HTTP_PREFIX) and not url.startswith(HTTPS_PREFIX):
        raise HTTPException(status_code=400, detail="This is an invalid url, please start with http:// or https://")

    ret = check_duplicated_url(db, url)
    if ret is not None:
        return convert_to_response(ret)

    hashcode = generate_hash(url)
    ret_by_hashcode = check_duplicated_hashcode(db, hashcode)
    if ret_by_hashcode is not None:
        shorturl = ret_by_hashcode
        shorturl.url = url
    else:
        shorturl = build_shorturl(url, hashcode)
        db.add(shorturl)
    db.commit()
    return convert_to_response(shorturl)
