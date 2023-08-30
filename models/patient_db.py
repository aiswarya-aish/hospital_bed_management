from sqlalchemy import Column, Integer, String, Text, Boolean
from db_config import Base, engine
from pydantic import BaseModel
import uuid


class Patient(BaseModel):
    name: str
    age: int
    gender: str
    medical_history: str
    checkin: bool
    room_no: int




class DBPatient(Base):
    __tablename__ = "patients"

    patient_id = Column(String, primary_key=True, index=True,default=uuid.uuid4().hex)
    name = Column(String)
    age = Column(Integer)
    gender = Column(String)
    medical_history = Column(Text)
    checkin = Column(Boolean)
    room_no = Column(Integer)


Base.metadata.create_all(bind=engine)
