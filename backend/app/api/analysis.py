from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

# импорт таблциц sql и pydantic-схем
from backend.app import models, schemas 
# выдача сессии бд
from backend.app.database import get_db

# получения функции вывода резултатов анализа
from backend.app.service.analysis import analyze

# роутер эндпоинтов для analysis
router = APIRouter(prefix="/projects/{project_id}/analyze", 
                   tags=["analysis"])

@router.post("")
def run_analysis(project_id: int,
                  db: Session = Depends(get_db)):
    """Получение текста из загруженных документов, выделение из них требований и исходного кода.

    Args:
        project_id (int): _description_
        db (Session, optional): _description_. Defaults to Depends(get_db).

    Raises:
        HTTPException: _description_
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
    
    return analyze(req_doc.content, code_doc.content)