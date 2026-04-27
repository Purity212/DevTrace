from fastapi import FastAPI

from backend.app.database import Base, engine
from backend.app.api import projects

app = FastAPI(title="DevTrace")
app.include_router(projects.router)

@app.get("/")
def read_root():
    return {
        "app" : "DevTrace",
        "status": "OK"
    }
    
@app.get("/health")
def health_check():
    return {
        "status" : "OK"
    }