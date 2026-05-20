from fastapi import FastAPI

from app.database import Base, engine

from routers.auth_router import router as auth_router
from routers.notes_router import router as notes_router
from routers.about_router import router as about_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Notes Backend API")

app.include_router(auth_router)
app.include_router(notes_router)
app.include_router(about_router)


@app.get("/")
def home():
    return{
        "message": "Notes Backend API Running"
    }