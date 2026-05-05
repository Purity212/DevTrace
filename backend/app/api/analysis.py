from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

# импорт таблциц sql и pydantic-схем
from backend.app import models, schemas 
# выдача сессии бд
from backend.app.database import get_db

# получения функции вывода резултатов анализа
from backend.app.service.analysis import analyze
from backend.app.service.candidate_find import find_candidates

# роутер эндпоинтов для analysis
router = APIRouter(prefix="/projects/{project_id}/analyze", 
                   tags=["analysis"])

def get_documents_info(project_id: int, db: Session = Depends(get_db)): 
        # select * from projects pr where pr.id = project_id limit 1
        project = db.query(models.Project).filter(models.Project.id == project_id).first()
        if project is None:
            raise HTTPException(status_code=404, detail="Project not found")
        
        # получение документа требований текущего проекта
        req_doc = db.query(models.Document).filter(models.Document.project_id == project_id,
                                        models.Document.document_type == "requirements").first()
        if req_doc is None:
            raise HTTPException(status_code=400, detail="Requirements document not found")
        
        # получение документа исходного кода текущего проекта
        code_doc = db.query(models.Document).filter(models.Document.project_id == project_id,
                                        models.Document.document_type == "source_code").first()
        if code_doc is None:
            raise HTTPException(status_code=400, detail="Souce code document not found")
        
        return req_doc, code_doc

@router.post("")
def get_analysis(project_id: int, db: Session = Depends(get_db)):
    """Реализует функционал формирования полного анализа документов требований и исходного кода.

    Args:
        project_id (int): Схема создания проекта.
        db (Session, optional): Сессия БД от database.py.

    Raises:
        HTTPException: "Project not found", "Requirements document not found", "Souce code document not found".

    Returns: 


    """
    req_doc, code_doc = get_documents_info(project_id = project_id, db = db)
    return analyze(req_doc.content, code_doc.content)

@router.post("/candidates")
def get_candidates(project_id: int, db: Session = Depends(get_db)):
    """
    Реализует функционал формирования тестковых сценариев. На данном этапе по сути копирует analysis.py. Но выводит лишь его часть

    Args:
        project_id (int): Схема создания проекта.
        db (Session, optional): Сессия БД от database.py.

    Raises:
        HTTPException: "Project not found", "Requirements document not found", "Souce code document not found".

    Returns: 

    """
    req_doc, code_doc = get_documents_info(project_id = project_id, db = db)
    return analyze(req_doc.content, code_doc.content)["candidates"]

@router.post("/test_case")
def get_test_cases(project_id: int, db: Session = Depends(get_db)):
    """
    Реализует функционал формирования тестковых сценариев. На данном этапе по сути копирует analysis.py. Но выводит лишь его часть

    Args:
        project_id (int): Схема создания проекта.
        db (Session, optional): Сессия БД от database.py.

    Raises:
        HTTPException: "Project not found", "Requirements document not found", "Souce code document not found".

    Returns: 

    """
    req_doc, code_doc = get_documents_info(project_id = project_id, db = db)
    return analyze(req_doc.content, code_doc.content)["test_cases"]

@router.post("/verification-matrix")
def get_verification_matrix(project_id: int, db: Session = Depends(get_db)):
    """
    Реализует функционал формирования матрицы верификации. На данном этапе по сути копирует analysis.py. Но выводит лишь его часть

    Args:
        project_id (int): Схема создания проекта.
        db (Session, optional): Сессия БД от database.py.

    Raises:
        HTTPException: "Project not found", "Requirements document not found", "Souce code document not found".

    Returns: 

    """
    req_doc, code_doc = get_documents_info(project_id = project_id, db = db)
    return analyze(req_doc.content, code_doc.content)["verification_matrix"]