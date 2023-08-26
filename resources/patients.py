from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.patient_db import DBPatient, Patient
from db_config import get_db
import uuid

router = APIRouter()

@router.post("/hospital/patient")
def add_new_patient(patient: Patient, db: Session = Depends(get_db)):
    patient_id = uuid.uuid4()  # Generate UUID
    db_patient = DBPatient(patient_id=str(patient_id), **patient.dict())
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient

@router.get("/hospital/patients")
def get_patients(db: Session = Depends(get_db)):
    return db.query(DBPatient).all()

@router.put("/hospital/patients/{patient_id}")
def update_patient(patient_id: uuid.UUID, updated_patient: Patient, db: Session = Depends(get_db)):
    db_patient = db.query(DBPatient).filter(DBPatient.patient_id == patient_id).first()
    if db_patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    for key, value in updated_patient.dict().items():
        setattr(db_patient, key, value)
    db.commit()
    return {"message": "Patient details updated successfully"}

@router.get("/hospital/patients/{patient_id}")
def get_patient(patient_id: uuid.UUID, db: Session = Depends(get_db)):
    db_patient = db.query(DBPatient).filter(DBPatient.patient_id == patient_id).first()
    if db_patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    return db_patient

@router.delete("/hospital/patients/{patient_id}")
def delete_patient(patient_id: uuid.UUID, db: Session = Depends(get_db)):
    db_patient = db.query(DBPatient).filter(DBPatient.patient_id == patient_id).first()
    if db_patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    db.delete(db_patient)
    db.commit()
    return {"message": "Patient deleted successfully"}
