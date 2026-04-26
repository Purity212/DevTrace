#from pydantic import BaseModel
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from backend.app.database import Base

"""Описание таблиц работы с данными по схеме бд из README.md"""

class Project(Base):
    """
    Таблица проектов 
    
    Поля:
    - id (PK): уникальный идентификатор проекта.
    - name: название проекта.
    - description: необязательное описание проекта.
    - created_at: дата и время создания проекта.
    """
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    documents = relationship("Document", back_populates="project")
    requirements = relationship("Requirement", back_populates="project")
    code_chunks = relationship("CodeChunk", back_populates="project")
    verification_items = relationship("VerificationItem", back_populates="project")


class Document(Base):
    """
    Талица загруженного документа.
    
    Поля:
    - id (PK): уникальный идентификатор документа.
    - project_id (FK): идентификатор проекта, которому принадлежит документ.
    - filename: исходное имя загруженного файла.
    - document_type: тип документа, например requirements (требования) или source_code (исходный код).
    - content: текстовое содержимое файла.
    - created_at: дата и время загрузки документа.
    """
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    filename = Column(String(255), nullable=False)
    document_type = Column(String(50), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    project = relationship("Project", back_populates="documents")


class Requirement(Base):
    """
    Таблица требования.
    
    Поля:
    - id (PK): уникальный идентификатор требования.
    - project_id (FK): идентификатор проекта, которому принадлежит требование.
    - requirement_key: внешний ключ требования из текста, например REQ-001 или REQ-CTRL-001.
    - text: текст требования без requirement_key.
    """
    __tablename__ = "requirements"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    requirement_key = Column(String(100), nullable=False)
    text = Column(Text, nullable=False)

    project = relationship("Project", back_populates="requirements")
    verification_items = relationship("VerificationItem", back_populates="requirement")
    test_cases = relationship("TestCase", back_populates="requirement")


class CodeChunk(Base):
    """
    Таблица фрагмента исходного кода.
    
    Поля:
    - id (PK): уникальный идентификатор фрагмента кода.
    - project_id (FK): идентификатор проекта, которому принадлежит фрагмент.
    - filename: имя файла, из которого извлечён фрагмент.
    - function_name: имя найденной функции.
    - content: полный текст фрагмента кода.
    - start_line: номер первой строки фрагмента в исходном файле.
    - end_line: номер последней строки фрагмента в исходном файле.
    """
    __tablename__ = "code_chunks"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    filename = Column(String(255), nullable=False)
    function_name = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    start_line = Column(Integer, nullable=True)
    end_line = Column(Integer, nullable=True)

    project = relationship("Project", back_populates="code_chunks")
    verification_items = relationship("VerificationItem", back_populates="code_chunk")


class VerificationItem(Base):
    """
    Элемент матрицы трассировки (однозначная свзяз: требование - фрагмент кода).
    
    Поля:
    - id (PK): уникальный идентификатор строки matrix.
    - project_id (FK): идентификатор проекта.
    - requirement_id (FK): идентификатор требования.
    - code_chunk_id (FK): идентификатор найденного фрагмента кода, если кандидат найден.
    - similarity_score: значение cosine similarity между требованием и фрагментом кода.
    - candidate_status: автоматический статус поиска кандидата:
      candidate_found, ambiguous или no_candidate_found.
    - verifier_status: статус, который вручную выставляет верификатор.
    - verifier_comment: комментарий верификатора.
    """
    __tablename__ = "verification_items"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    requirement_id = Column(Integer, ForeignKey("requirements.id"), nullable=False)
    code_chunk_id = Column(Integer, ForeignKey("code_chunks.id"), nullable=True)
    similarity_score = Column(Float, nullable=True)
    candidate_status = Column(String(50), nullable=False)
    verifier_status = Column(String(50), nullable=True)
    verifier_comment = Column(Text, nullable=True)

    project = relationship("Project", back_populates="verification_items")
    requirement = relationship("Requirement", back_populates="verification_items")
    code_chunk = relationship("CodeChunk", back_populates="verification_items")


class TestCase(Base):
    """
    Тест-кейс для требования
    
    Поля:
    - id (PK): уникальный идентификатор тест-кейса.
    - requirement_id (FK): идентификатор требования, которое проверяет тест-кейс.
    - title: название тест-кейса.
    - preconditions: предусловия выполнения теста.
    - steps: шаги теста.
    - expected_result: ожидаемый результат.
    """
    
    __tablename__ = "test_cases"

    id = Column(Integer, primary_key=True, index=True)
    requirement_id = Column(Integer, ForeignKey("requirements.id"), nullable=False)
    title = Column(String(255), nullable=False)
    preconditions = Column(Text, nullable=True)
    steps = Column(Text, nullable=True)
    expected_result = Column(Text, nullable=True)

    requirement = relationship("Requirement", back_populates="test_cases")
