from fastapi import APIRouter, Depends, File, Form, UploadFile, HTTPException
from sqlalchemy.orm import Session

# импорт таблциц sql и pydantic-схем
from backend.app import models, schemas 
# выдача сессии бд
from backend.app.database import get_db

# роутер эндпоинтов для documents
router = APIRouter(prefix="/projects/{project_id}/documents", 
                   tags=["documents"])

# POST-запрос при добавлении нового документа, записывающий его в БД
# /projects/{project_id}/documents - создание документа внутри определенного проекта
@router.post("", response_model=schemas.DocumentRead)
async def load_document(project_id: int,
                  document_type: str = Form(...),  # вызов формы в docs FastAPI
                  file: UploadFile = File(...), # вызов загрузки файла FastAPI
                  db: Session = Depends(get_db) # вызывается перед выполнением endpoint
                  ): 
    """Загрузка документа в проект

    Args:
        project_id (int): _description_
        document_type (str, optional): _description_. Defaults to Form(...).
    Returns:

    """
    # select * from projects pr where pr.id = project_id limit 1
    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # допустимые типы документов: требования, исходный код
    allowed_document_types = {"requirements", "source_code"}
    if document_type not in allowed_document_types:
        raise HTTPException(status_code=400, detail="Document_type must be requirements or source_code")
    
    # имя файла 
    filename = ''
    if file.filename is None:
        filename = 'unknown'
        raise HTTPException(status_code=400, detail="Filename not found")
    else:
        filename = file.filename
        
    # расширения принимаемых файлов
    allowed_extensions = {".md", ".txt", ".py", ".c"}
    if not any(filename.endswith(extension) for extension in allowed_extensions):
        raise HTTPException(status_code=400, detail=f"Extension should be in {allowed_extensions}")
    
    # ожидание получения сырого текста из файла
    raw = await file.read()
    try:
        content = raw.decode('utf-8')
    except UnicodeDecodeError as exc:
        raise HTTPException(status_code=400, detail="Unicode should be UTF-8")

    db_document = models.Document(project_id=project_id,
                                    filename=filename,
                                    document_type=document_type,
                                    content=content)

    # запись и коммит в БД
    db.add(db_document)
    db.commit() # тут присваивает id проекту и дату создания
    db.refresh(db_document)
    
    return db_document

# /project/{project_id}/documents - получить имеющиеся документы по проекту
@router.get("", response_model=list[schemas.DocumentRead])
def list_documents(project_id: int,
                  db: Session = Depends(get_db)):
    """Получение отсортированного документов внутри проекта из БД
    SELECT * 
    FROM documents doc
    ORDER BY pr.id DESC

    Args:
        project_id (int): Идентификатор проекта.
        db (Session, optional): Сессия БД от database.py.
    Returns:
        list_documents (list[schemas.DocumentRead]): список проектов в формате DocumentRead.
    """    
    # select * from projects pr where pr.id = project_id limit 1
    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")

    list_documents = db.query(models.Document).filter(models.Document.project_id == project_id).order_by(models.Document.id.desc()).all()
    return list_documents
    