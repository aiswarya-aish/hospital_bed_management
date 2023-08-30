from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.patient_db import DBPatient, Patient
from models.room_db import DBRoom, Rooms
from db_config import get_db
import uuid

router = APIRouter()

@router.post("/hospital/patient/checkin/{patient_id}")
def patient_checkin(patient_id: str, db: Session = Depends(get_db)):
    db_patient = db.query(DBPatient).filter(DBPatient.patient_id == patient_id).first()
    if db_patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")

    # Find a vacant room
    db_room = db.query(DBRoom).filter(DBRoom.vacant == True).first()
    if db_room is None:
        raise HTTPException(status_code=404, detail="No vacant room available")

    # Update patient's room_no and room's details
    db_patient.room_no = db_room.room_no
    db_patient.checkin = True
    db_room.vacant = False
    db_room.allocated_to = str(patient_id)

    db.commit()

    return {"message": "Patient checked in successfully"}


@router.post("/hospital/patient/checkout/{patient_id}")
def patient_checkout(patient_id: str, db: Session = Depends(get_db)):
    db_patient = db.query(DBPatient).filter(DBPatient.patient_id == patient_id).first()
    if db_patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")

    # Get the room assigned to the patient
    db_room = db.query(DBRoom).filter(DBRoom.room_no == db_patient.room_no).first()
    if db_room is None:
        raise HTTPException(status_code=404, detail="Room not found")

    # Clear the patient's room assignment
    db_patient.room_no = None
    db_patient.checkin = False
    db.commit()

    # Update the room's details
    db_room.vacant = True
    db_room.allocated_to = ""
    db.commit()

    return {"message": "Patient checked out successfully"}

