from typing import TypedDict

from backend.app.service.req_extract import RequirementData, extract_reqs
from backend.app.service.code_extract import CodeChunkData, extract_code_chunks

"""Пайплан обработки входных данных и формирование результата"""

text_from_req_file = ''
text_from_code_file = ''

class AnalyzeData(TypedDict):
    """
    Класс кандидата (соответствие требование - искходный код).

    Args: dict (TypeDict): словарь с однозначным заданием кандидата следующего содержания: 
                            requirements (list[RequirementData]) - 
                            code_chunks (list[CodeChunkData]) -
                            # TODO 
                            
    """
    requirements : list[RequirementData]
    code_chunks : list[CodeChunkData] 
    ### TODO 

def analyze(text_from_req_file: str, text_from_code_file: str):
    return AnalyzeData(
            {
            "requirements" : extract_reqs(text_from_req_file),
            "code_chunks": extract_code_chunks(text_from_code_file)
        }
    )