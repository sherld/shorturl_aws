from datetime import datetime

from pydantic import BaseModel


class ShorturlRequest(BaseModel):
    url: str

class ShorturlResponse(BaseModel):
    id: int
    url: str
    shorturl: str
    createddate: datetime
