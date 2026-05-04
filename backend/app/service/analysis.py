from typing import TypedDict

from backend.app.service.req_extract import RequirementData, extract_reqs
from backend.app.service.code_extract import CodeChunkData, extract_code_chunks
from backend.app.service.candidate_find import CandidateData, find_candidates
# import test cases module
# import verification matrix module

"""Пайплан обработки входных данных и формирование результата"""

text_from_req_file = ''
text_from_code_file = ''

class AnalyzeData(TypedDict):
    """
    Класс кандидата (соответствие требование - искходный код).

    Args: dict (TypeDict): словарь с однозначным заданием общих даннных анализаследующего содержания: 
                        requirements (list[RequirementData]) - 
                        code_chunks (list[CodeChunkData]) -
                        candidates (list[CandidateData]) -
                        test_cases (List[TestCaseData]) - 
                        verificatioN_matrix (List[VerifMatrixData]) - 
                                            
    """
    requirements : list[RequirementData]
    code_chunks : list[CodeChunkData] 
    candidates: list[CandidateData]
    # test_cases
    # verification_matrix


def analyze(text_from_req_file: str, text_from_code_file: str):

    # извлечение требований из документа
    requirements = extract_reqs(text_from_req_file)
    # извлечение фрагментов кода из документа
    code_chunks = extract_code_chunks(text_from_code_file)
    # поиск схожих кандидатов
    candidates = find_candidates(requirements=requirements, code_chunks=code_chunks)
    # TODO
    # test_cases =
    # TODO
    # verification_matrix = 

    return AnalyzeData(
        {
            "requirements": requirements,
            "code_chunks": code_chunks,
            "candidates": candidates
        }
        )