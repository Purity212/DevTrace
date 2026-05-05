from typing import TypedDict

from backend.app.service.req_extract import RequirementData, extract_reqs
from backend.app.service.code_extract import CodeChunkData, extract_code_chunks
from backend.app.service.candidate_find import CandidateData, find_candidates
from backend.app.service.test_case_generate import TestCaseData, generate_draft_test_cases
from backend.app.service.verification_matrix import VerificationMatrixRowData, build_verification_matrix

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
    test_cases: list[TestCaseData]
    verification_matrix: list[VerificationMatrixRowData]


def analyze(text_from_req_file: str, text_from_code_file: str):
    """
    Функция анализирует текста, извлеченные из документов, по ним находит кандидатов на соответствие требования - фрагмента исходного кода,
    формирует базовые тест-кейсы для фрагмента, матрицу верификации.

    Args:
        text_from_req_file (str): Извлеченный текст из документа требований.
        text_from_code_file (str):  Извлеченный текст из документа исходного кода.

    Returns:
        Объект анализа (AnalyzeData), из которого можно получать, данные об анализе, обращаясь по следующим ключам:
        1. requirements (list[RequirementData]): Извлеченные требования.
        2. code_chunks (list[CodeChunkData]): Извлеченный ИК.
        3. candidates (list[CandidateData]): Перечень кандидатов.
        4. test_cases (list[TestCaseData]): Перечень тест-кейсов.
        5. verification_matrix (list[VerificationMatrixRowData]): Перечень строк матрицы верификации.
    """

    # извлечение требований из документа
    requirements = extract_reqs(text_from_req_file)
    # извлечение фрагментов кода из документа
    code_chunks = extract_code_chunks(text_from_code_file)
    # поиск схожих кандидатов
    candidates = find_candidates(requirements=requirements, code_chunks=code_chunks)
    # формирование базовых тест-кейсов
    test_cases = generate_draft_test_cases(requirements=requirements)
    # формирование матрицы трассируемости
    verification_matrix = build_verification_matrix(requirements=requirements, candidates=candidates, test_cases=test_cases)

    return AnalyzeData(
        {
            "requirements": requirements,
            "code_chunks": code_chunks,
            "candidates": candidates,
            "test_cases": test_cases,
            "verification_matrix" : verification_matrix
        }
        )
