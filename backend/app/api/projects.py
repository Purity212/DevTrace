from fastapi import FastAPI, APIRouter, Depends
from sqlalchemy.orm import Session

# импорт таблциц sql и pydantic-схем
from backend.app import models, schemas 
# выдача сессии бд
from backend.app.database import get_db

# роутер эндпоинтов для projects
router = APIRouter(prefix="/projects", tags=["projects"])

# POST-запрос при создании нового проекта, записывающий его в БД
# /project - создание файла проекта
@router.post("", response_model=schemas.ProjectRead)
def create_project(project_data: schemas.ProjectCreate,
                   db: Session = Depends(get_db)): # вызывается перед выполнением endpoint
    """Создание проекта в сесси БД

    Args:
        project_data (schemas.ProjectCreate): Схема создания проекта.
        db (Session, optional): Сессия БД от database.py.
    Retrns:
        db_project(models.Project): Экземпляр созданного проекта.
    """
    
    # экземпляр класса конкретного проекта
    db_project = models.Project(name=project_data.name,
                                description=project_data.description
    )

    # запись и коммит в БД
    db.add(db_project)
    db.commit() # тут присваивает id проекту
    db.refresh(db_project)
    
    return db_project
