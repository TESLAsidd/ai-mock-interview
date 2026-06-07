from fastapi import FastAPI

from database import engine

from models import Base

from routes.users import router

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(router)
@app.get("/")
def home():

    return {
        "message": "AI Mock Interview API"
    }
