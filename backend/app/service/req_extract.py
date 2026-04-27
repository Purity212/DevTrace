import re

"""Модуль предназначен для описания логики извлечения требований из сырого текста в utf-8"""

# На первоначальном этапе - извлечение с помощью регулярных выражений с поиском следующего паттерна:
# REQ-...
# REQ-...-...
# REQ-...-...-...

REQUIREMENT_PATTERN = re.compile(
    r"^\s*(REQ(?:-[A-Z]+)*-\d+)\s*:\s*(.+?)\s*$",
    re.MULTILINE,
)

def extract_reqs(text: str) -> list[dict[str, str]]:
    """Извлекает требования из сырого текста
    Формат: 
    REQ-...
    REQ-...-...
    REQ-...-...-...

    Args:
        text (str): текст документа требований

    Returns:
        list[dict[str, str]]: список из словарей, где каждый словарь - это соответствие: "идентификатор требования" - "текст требования" 
    """
    reqs = []
    
    for match in REQUIREMENT_PATTERN.finditer(text):
        requirement_key = match.group(1).strip()
        requirement_text = match.group(2).strip()
        
        reqs.append(
            {
                "requirement_key": requirement_key,
                "text": requirement_text,
            }
        )

    return reqs