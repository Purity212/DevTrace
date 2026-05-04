from typing import TypedDict

from backend.app.service.req_extract import RequirementData

class TestCaseData(TypedDict):
    """
    """
    requirement_key : str
    external_id: str
    title: str
    preconditions: str
    steps: str 
    expected_result: str
    test_type: str
    status: str

def make_test_case_id(requirement_key: str) -> str:
    """
    Для формирования идентификаторов тест-кейсов на основе идентификаторов требований.
    """
    if requirement_key.startswith("REQ-"):
        return "TC-" + requirement_key[4:] + "-001"
    return f"TC-{requirement_key}-001"


def generate_draft_test_cases(requirements: list[RequirementData]) -> list[TestCaseData]:
    """
    Релизует формирование базового тестового сценария (для MVP 1 без интеграции "умного анализатора" - например агента по chat gpt api) 

    Args:
        requirements (list[RequirementData])  - список извлеченных требований
    """
    test_cases: list[TestCaseData] = []

    for requirement in requirements:
        requirement_key = requirement["requirement_key"]
        requirement_text = requirement["text"]

        test_cases.append(
            TestCaseData(
                {
                    "requirement_key": requirement_key,
                    "external_id": make_test_case_id(requirement_key),
                    "title": f"Verify {requirement_key}",
                    "preconditions": "Project is created, documents are uploaded, system is ready for execution.",
                    "steps": f"1. Prepare the system state.\n2. Execute the scenario for {requirement_key}.\n3. Observe the system behavior.",
                    "expected_result": requirement_text,
                    "test_type": "positive",
                    "status": "draft",
                }
            )
        )

    return test_cases