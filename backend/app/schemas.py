from pydantic import BaseModel

# TODO: дописать Docstrings для классов

"""API для получения/отправки данных"""

class ProjectCreate(BaseModel):
    """
    API при создании проекта
    """
    name: str
    description: str | None = None
    
class ProjectRead(BaseModel):
    """
    API при получении данных о проекте
    """
    id: int
    name: str
    description: str | None = None
    
    class Config:
        from_attributes = True # работа с sqlalchemy объектами в json
  
  
"""Только чтение"""     
class DocumentRead(BaseModel):
    """
    API данных о документе, загруженном пользователем
    """
    id: int
    project_id: int
    filename: str
    document_type: str
    
    class Config:
        from_attributes = True # работа с sqlalchemy объектами в json
    
class RequirementRead(BaseModel):
    """
    API данных об извлеченном требовании
    """
    id: int
    project_id: int
    requirement_key: str
    text: str

    class Config:
        from_attributes = True # работа с sqlalchemy объектами в json
    
class CodeChunkRead(BaseModel):
    """
    API данных об извлеченном фрагменте кода
    """
    id: int
    project_id: int
    filename: str
    function_name: str
    content: str
    start_line: int | None = None
    end_line: int | None = None

    class Config:
        from_attributes = True # работа с sqlalchemy объектами в json
    
"""Создание - чтение - обновление"""
class TestCaseCreate(BaseModel):
    """
    При создании тест-кейса
    """
    title: str
    preconditions: str | None = None
    steps: str | None = None
    expected_result: str | None = None

class TestCaseRead(BaseModel):
    """
    Для чтения тест-кейса
    """
    id: int
    requirement_id: int
    title: str
    preconditions: str | None = None
    steps: str | None = None
    expected_result: str | None = None
    
    class Config:
        from_attributes = True # работа с sqlalchemy объектами в json

class TestCaseUpdate(BaseModel):
    """
    Для изменений тест-кейса
    """
    title: str | None = None
    preconditions: str | None = None
    steps: str | None = None
    expected_result: str | None = None
    
# "Единица трассировки"
class VerificationItemRead(BaseModel):
    """
    Строка матрицы трассировки, возвращаемая через API
    """

    id: int
    project_id: int
    requirement_id: int
    code_chunk_id: int | None = None
    similarity_score: float | None = None
    candidate_status: str
    verifier_status: str | None = None
    verifier_comment: str | None = None

    class Config:
        from_attributes = True # работа с sqlalchemy объектами в json