from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from dotenv import load_dotenv
import os

env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)

from backend.database import engine, Base
from backend.routers import quiz

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Wiki Quiz API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.environ.get("ALLOWED_ORIGINS", "*").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(quiz.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Wiki Quiz API"}
