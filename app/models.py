from sqlalchemy import Column, String, Integer, Boolean, DateTime

from app.database import Base


class Shorturl(Base):
    __tablename__ = 'shorturl'
    id = Column('id', Integer, primary_key=True)
    url = Column(String)
    hashcode = Column(String, unique=True)
    createddate = Column(DateTime)
