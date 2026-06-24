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

def clear_project_analysis_data(project_id: int, db: Session) -> None:
    """ Очистка результатов прошлых запусков из БД"""

    db.query(models.CodeChunk).filter(models.CodeChunk.project_id == project_id
                                      ).delete(synchronize_session=False)

    db.query(models.Requirement).filter(models.Requirement.project_id == project_id
                                        ).delete(synchronize_session=False)
    
    db.query(models.VerificationItem).filter(models.VerificationItem.project_id == project_id
                                      ).delete(synchronize_session=False)


def write_requirements(project_id: int, requirements: list[RequirementData], db: Session = Depends(get_db)):
    """
    """
    key_req_dict = {}

    for req in requirements:
        db_req = models.Requirement(
            project_id = project_id,
            requirement_key = req["requirement_key"],
            text=req["text"]
        )

        db.add(db_req)
        db.flush()
        key_req_dict[req["requirement_key"]] = db_req
    
    return key_req_dict


def write_code_chunks(project_id: int, filename: str, code_chunks: list[CodeChunkData], db: Session = Depends(get_db)):
    """
    """
    key_code_chunk_dict = {}

    for cch in code_chunks:
        db_chunk = models.CodeChunk(
            project_id = project_id,
            filename = filename,
            function_name = cch['name'],
            content = cch['content'],
            start_line = cch['start_line'],
            end_line = cch['end_line']
        )

        db.add(db_chunk)
        db.flush()
    
        key_code_chunk_dict[(cch["name"], cch["content"])] = db_chunk
    
    return key_code_chunk_dict

def write_verification_items(project_id: int,
    candidates: list[CandidateData],
    requirements_by_key: dict[str, models.Requirement],
    code_chunks_by_signature: dict[tuple[str, str], models.CodeChunk],
    db: Session):
    for candidate in candidates:
        db_requirement = requirements_by_key[candidate["requirement_key"]]

        code_chunk_id = None
        if (candidate["code_chunk_name"] is not None
            and candidate["code_chunk_content"] is not None):
            db_code_chunk = code_chunks_by_signature[(candidate["code_chunk_name"], candidate["code_chunk_content"])]
            code_chunk_id = db_code_chunk.id

        db_item = models.VerificationItem(
            project_id=project_id,
            requirement_id=db_requirement.id,
            code_chunk_id=code_chunk_id,
            similarity_score=candidate["similarity_score"],
            candidate_status=candidate["candidate_status"],
            verifier_status="?",
            verifier_comment="?",
        )

        db.add(db_item)
     

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
        clear_project_analysis_data(project_id, db)

        requirements_by_key = write_requirements(project_id=project_id, requirements=result['requirements'], db=db)
        code_chunks_by_sign = write_code_chunks(project_id=project_id, filename=code_doc.filename, code_chunks=result['code_chunks'], db=db)

        write_verification_items(project_id=project_id,
                                 candidates=result['candidates'],
                                 requirements_by_key=requirements_by_key,
                                 code_chunks_by_signature=code_chunks_by_sign,
                                 db=db)

        db.commit()
    except Exception:
        db.rollback()
        raise

    return result



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