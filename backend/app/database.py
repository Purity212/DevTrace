from sqlalchemy import create_engine 
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "sqlite:///./devtrace.db"

# движок поключения к базе
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# фабрика сессий для операций с БД
SessionLocal = sessionmaker(autocommit=False, # без автосохранений
                            autoflush=False,
                            bind=engine) # сессии работают через созданный engine

# Базовый класс для моделей
Base = declarative_base()

def get_db():
    "для обращения к БД из других модулей (для fastapi)"
    db  = SessionLocal()
    try:
        yield db
    finally:
        db.close()
    