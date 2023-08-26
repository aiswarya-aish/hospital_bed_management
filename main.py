from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uuid
# Create a FastAPI app instance
app = FastAPI()

# In-memory database to store tasks
hospital_rooms = {}

# Create a Pydantic model for the task
class Rooms(BaseModel):
    room_no: int
    type: str
    floor: int
    vacant: bool
    allocated_to: str
    price_per_night: float
    patient_id: str = ""


# Endpoint to create a new task
@app.post("/hospital/room")
def add_new_room(room: Rooms):
    hospital_rooms[room.room_no] = room
    return hospital_rooms


# Endpoint to get all tasks
@app.get("/hospital/rooms")
def get_rooms():
    return hospital_rooms


@app.put("/hospital/rooms/{room_no}")
def update_room_details(room_no: int, updated_room: Rooms):
    if room_no not in hospital_rooms:
        raise HTTPException(status_code=404, detail="Room not found")
    hospital_rooms[room_no] = updated_room  # Update the task in the list
    return {"message": "Room details updated successfully"}


# Endpoint to get a specific task by its index in the list
@app.get("/hospital/rooms/{room_no}")
def get_room_details(room_no: int):
    if room_no not in hospital_rooms:
        raise HTTPException(status_code=404, detail="Room not found")
    else:
        return hospital_rooms[room_no]


# Endpoint to delete a task by its index in the list
@app.delete("/hospital/rooms/{room_no}")
def delete_room(room_no: int):
    if room_no not in hospital_rooms:
        raise HTTPException(status_code=404, detail="Room not found")
    else:
        del hospital_rooms[room_no]

    return {"message": "Task deleted successfully", "deleted_room": room_no}
