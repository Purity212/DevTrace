from backend.app.service.req_extract import RequirementData, extract_reqs
from backend.app.service.code_extract import CodeChunkData, extract_code_chunks

"""Пайплан обработки входных данных и формирование результата"""

text_from_req_file = ''
text_from_code_file = ''

def analyze(text_from_req_file: str, text_from_code_file: str):

    requirements : list[RequirementData] = extract_reqs(text_from_req_file)
    code_chunks : list[CodeChunkData] = extract_code_chunks(text_from_code_file)

    return {
        "reqs": requirements,
        "code_chunks": code_chunks
    }