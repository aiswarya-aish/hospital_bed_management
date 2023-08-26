from sqlalchemy import Column, Integer, String, Text
from db_config import Base, engine
from pydantic import BaseModel
import uuid


class Patient(BaseModel):
    name: str
    age: int
    gender: str
    medical_history: str




class DBPatient(Base):
    __tablename__ = "patients"

    patient_id = Column(String, primary_key=True, index=True)
    name = Column(String)
    age = Column(Integer)
    gender = Column(String)
    medical_history = Column(Text)


Base.metadata.create_all(bind=engine)
