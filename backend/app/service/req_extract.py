import re

from typing import TypedDict

"""Модуль предназначен для описания логики извлечения требований из сырого текста в utf-8"""

# На первоначальном этапе - извлечение с помощью регулярных выражений с поиском следующего паттерна:
# REQ-...
# REQ-...-...
# REQ-...-...-...

REQUIREMENT_PATTERN = re.compile(
    r"^\s*(REQ(?:-[A-Z]+)*-\d+)\s*:\s*(.+?)\s*$",
    re.MULTILINE,
)

class RequirementData(TypedDict):
    """
    Класс требования.

    Args: dict (TypeDict): словарь с однозначным заданием требования следующего содержания: 
                            requirement_key: Идентификатор требования.
                            text: Текст требования.
    """
    requirement_key: str
    text: str

def extract_reqs(text: str) -> list[RequirementData]:
    """Извлекает требования из сырого текста
    Формат: 
    REQ-...
    REQ-...-...
    REQ-...-...-...

    Args:
        text (str): текст документа требований

    Returns:
        list[RequirementData]: список из RequirementData
    """
    reqs = []
    
    for match in REQUIREMENT_PATTERN.finditer(text):
        requirement_key = match.group(1).strip()
        requirement_text = match.group(2).strip()
        
        reqs.append(
            RequirementData(
                {
                    "requirement_key": requirement_key,
                    "text": requirement_text,
                }
            )
        )

    if not reqs: 
        raise ValueError("Requirements no found in document")

    return reqs