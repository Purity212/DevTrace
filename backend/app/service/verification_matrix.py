from typing import TypedDict

from backend.app.service.req_extract import RequirementData
from backend.app.service.candidate_find import CandidateData
from backend.app.service.test_case_generate import TestCaseData

class VerificationMatrixRowData(TypedDict):
    """
    Класс каждой отдельно взятой строки матрицы верификации.
    """
    requirement_key: str
    requirement_text: str
    candidate_code: str | None
    similarity_score: float
    system_status: str
    test_cases_count: int
    verifier_status: str
    verifier_comment: str

def build_verification_matrix(requirements: list[RequirementData], 
                              candidates: list[CandidateData], 
                              test_cases: list[TestCaseData]) -> list[VerificationMatrixRowData]:
    
    verification_matrix : list[VerificationMatrixRowData] = []

    req_candidate = {row["requirement_key"]: row for row in candidates} # словарь: кандидат по айди требования

    # объяевление словаря тест_кейс - id
    req_test_case : dict[str, int] = {}
    # заполнение с авто-увеличением айди
    for t_c in test_cases:
        key = t_c["requirement_key"]
        req_test_case[key] = req_test_case.get(key, 0) + 1 # автоинкремент айди

    # формирование матрицы с группировкой по требованиям
    for req in requirements:
        key = req['requirement_key']
        candidate = req_candidate.get(key)

        verification_matrix.append(
            VerificationMatrixRowData(
                {
                    "requirement_key": key, 
                    "requirement_text": req["text"],
                    "candidate_code": candidate["code_chunk_name"],
                    "similarity_score": candidate["similarity_score"],
                    "system_status" : candidate["candidate_status"],
                    "test_cases_count" : req_test_case.get(key, 0),
                    "verifier_status" : "?",
                    "verifier_comment" : "?"
                }
            )
        )

    return verification_matrix