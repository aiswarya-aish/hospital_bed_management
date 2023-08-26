from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.room_db import DBRoom, Rooms
from db_config import get_db

router = APIRouter()

@router.post("/hospital/room")
def add_new_room(room: Rooms, db: Session = Depends(get_db)):
    db_room = DBRoom(**room.dict())
    db.add(db_room)
    db.commit()
    db.refresh(db_room)
    return db_room

@router.get("/hospital/rooms")
def get_rooms(db: Session = Depends(get_db)):
    return db.query(DBRoom).all()

@router.put("/hospital/rooms/{room_no}")
def update_room_details(room_no: int, updated_room: Rooms, db: Session = Depends(get_db)):
    db_room = db.query(DBRoom).filter(DBRoom.room_no == room_no).first()
    if db_room is None:
        raise HTTPException(status_code=404, detail="Room not found")
    for key, value in updated_room.dict().items():
        setattr(db_room, key, value)
    db.commit()
    return {"message": "Room details updated successfully"}

@router.get("/hospital/rooms/{room_no}")
def get_room_details(room_no: int, db: Session = Depends(get_db)):
    db_room = db.query(DBRoom).filter(DBRoom.room_no == room_no).first()
    if db_room is None:
        raise HTTPException(status_code=404, detail="Room not found")
    return db_room

@router.delete("/hospital/rooms/{room_no}")
def delete_room(room_no: int, db: Session = Depends(get_db)):
    db_room = db.query(DBRoom).filter(DBRoom.room_no == room_no).first()
    if db_room is None:
        raise HTTPException(status_code=404, detail="Room not found")
    db.delete(db_room)
    db.commit()
    return {"message": "Room deleted successfully"}
