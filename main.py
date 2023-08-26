from fastapi import FastAPI
from resources.rooms import router as room_router
from resources.patients import router as patient_router

app = FastAPI()

app.include_router(room_router)
app.include_router(patient_router)