from sqlalchemy import Column, Integer, String, Boolean, Float
from pydantic import BaseModel
from db_config import Base, engine

# Pydantic model for validations
class Rooms(BaseModel):
    room_no: int
    room_type: str
    floor: int
    vacant: bool
    allocated_to: str
    price_per_night: float
    patient_id: str = ""

# SQLAlchemy db model
class DBRoom(Base):
    __tablename__ = "rooms"

    room_no = Column(Integer, primary_key=True, index=True)
    room_type = Column(String)
    floor = Column(Integer)
    vacant = Column(Boolean)
    allocated_to = Column(String)
    price_per_night = Column(Float)
    patient_id = Column(String)

Base.metadata.create_all(bind=engine)