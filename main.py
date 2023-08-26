from fastapi import FastAPI
from resources.rooms import router as room_router

app = FastAPI()

app.include_router(room_router)
