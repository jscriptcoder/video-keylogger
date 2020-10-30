from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, JSON, Text

Base = declarative_base()

class KeyFrameModel(Base):
    __tablename__ = 'key_frame'

    id = Column(Integer, primary_key=True)
    created = Column(DateTime, default=datetime.now)
    key = Column(Integer)
    frame = Column(JSON)