from fastapi import FastAPI
from routes import router as chat_router
from database import Base, engine
from seed import seed_data
from models import Base

app = FastAPI(title="Cable Bot")

Base.metadata.create_all(bind=engine)
seed_data()

app.include_router(chat_router)