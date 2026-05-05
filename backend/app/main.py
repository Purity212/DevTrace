from fastapi import FastAPI

from backend.app.database import Base, engine
from backend.app.api import projects, documents, analysis, verification

# Первоначальная инициализация таблиц (из Base) в сесси БД
Base.metadata.create_all(bind=engine)

app = FastAPI(title="DevTrace")
app.include_router(projects.router)
app.include_router(documents.router)
app.include_router(analysis.router)
app.include_router(verification.router)

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