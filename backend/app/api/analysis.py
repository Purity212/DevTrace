from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

# импорт таблциц sql и pydantic-схем
from backend.app import models, schemas 
# выдача сессии бд
from backend.app.database import get_db

# получения функции вывода резултатов анализа
from backend.app.service.analysis import analyze
from backend.app.service.candidate_find import find_candidates

from backend.app.service.req_extract import RequirementData
from backend.app.service.code_extract import CodeChunkData
from backend.app.service.candidate_find import CandidateData
from backend.app.service.test_case_generate import TestCaseData
from backend.app.service.verification_matrix import VerificationMatrixRowData

# роутер эндпоинтов для analysis
router = APIRouter(prefix="/projects/{project_id}/analyze", 
                   tags=["analysis"])

def get_documents_info(project_id: int, db: Session = Depends(get_db)):
        """ Извлечение текстов требований и фрагментов кода из документов в текущем проекте.
                """ 
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

def write_requirements(project_id: int, requirements: list[RequirementData], db: Session = Depends(get_db)):
     
    key_req_dict = {}

    for req in requirements:
        db_req = models.Requirement(
            project_id = project_id,
            requirement_key = req["requirement_key"],
            text=req["text"]
        )

    db.add(db_req)
    db.flush()


def write_code_chunks(project_id: int, code_chunks: list[CodeChunkData], db: Session = Depends(get_db)):
     
    key_code_chunk_dict = {}

    for cch in code_chunks:
        db_req = models.CodeChunk(
            project_id = project_id,
            filename = "???",
            function_name = cch['name'],
            content = cch['content'],
            start_line = cch['start_line'],
            end_line = cch['end_line']
        )

    db.add(db_req)
    db.flush()
     

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
    result = analyze(req_doc.content, code_doc.content)

    try:
        # нужно сначала почистить данные

        write_requirements(project_id=project_id, requirements=req_doc.content, db=db)
        write_code_chunks(project_id=project_id, code_chunks=code_doc.content, db=db)

        db.commit()
    except Exception:
        db.rollback()
        raise

    return db.query(models.Requirement).filter(models.Project.id == project_id)



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