import ast #встроенный парсер синтаксиса python

from typing import TypedDict

class CodeChunkData(TypedDict):
    """
    Класс фрагмента кода.

    Args: dict (TypeDict): словарь с однозначным заданием фрагмента кода следующего содержания: 
                            name: Название функции.
                            content: Содержание функции.
                            start_line: Номер строки начала фрагмента кода.
                            end_line: Номер строки конца фрагмента кода.
    """
    name: str
    content: str
    start_line: int
    end_line: int

def extract_code_chunks(text: str) -> list[CodeChunkData]:

    lines = text.splitlines() # для определения номеров строк кода
    code_chunks: list[CodeChunkData] = []

    # проверка на пустой файл
    if not text.strip():
        # return []
        raise Exception("Document is empty")
    
    # парсинг кода
    try:
        tree = ast.parse(text)
    except SyntaxError as exc:
        raise ValueError(f"Invalid python code: {exc.msg}")
    
    # проход по нодам в дереве кода
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)): # если часть исходника является функцией
            if node.end_lineno is None:
                raise ValueError("Can`t define bounds of function")

            code_chunks.append(
                {
                    "name": node.name,
                    "content" : "\n".join(lines[node.lineno - 1: node.end_linelo]), # всё содержэание от строки начала до строки конца
                    "start_line": node.lineno,
                    "end_line": node.end_lineno
                }
            )
    
    return code_chunks