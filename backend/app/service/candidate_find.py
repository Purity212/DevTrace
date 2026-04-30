from typing import TypedDict

from backend.app.service.req_extract import RequirementData
from backend.app.service.code_extract import CodeChunkData
from backend.app.service.analysis import AnalyzeData, analyze

from sklearn.feature_extraction.text import TfidfVectorizer

from backend.app.service.similarity_algs.cosine_similarity import cosine_similarity

class CandidateData(TypedDict):
    """
    Класс кандидата (соответствие требование - искходный код).

    Args: dict (TypeDict): словарь с однозначным заданием кандидата следующего содержания: 
                            requirement_key (str) - Идентификатор требования.
                            requirement_text: str) - Текст требования.
                            code_chunk_name: (str | None) - Название фрагмента кода (опционально)
                            code_chunk_content (str | None) - Содержание фрагмента кода (опционально)
                            similarity_score: (float) - Степень смысловой схожести
                            system_status: (str) - candidate_found / ambiguous / no_candidate_found
    """
    requirement_key: str
    requirement_text: str
    code_chunk_name: str | None
    code_chunk_content : str | None
    similarity_score: float
    candidate_status: str


def find_candidates(analyze_data : AnalyzeData) -> list[CandidateData]:
    """
    Реализует поиск кандидатов на соответствие среди требований и фрагментов кода, опираясь на оценку "схожести", кандидат - пара с высшей оценкой.

    1. Проверка на пустые списики
    2. Все текста для единого словаря: requirements_texts + code_texts
    3. Трэин для vectorizer + fit_transform (на одном пространстве признаков для требований и кодовых фрагментов)
    4. разделить matrix на req_matrix и code_matrix
    5. similarity_matrix = cosine_similarity(...) - применение метода для поиска похожих по смыслу
    6. пройти по каждому requirement
       - найти best score
       - найти best chunk
       - определить status
       - append в results
    7. return results

    Returns: Информацию о кандидате в формате CandidateData
    """
    requirements : list[RequirementData] = analyze_data['requirements']
    if len(requirements) < 1:
        raise ValueError("Requirements list is empty")

    code_chunks : list[CodeChunkData] = analyze_data['code_chunks']
    if len(code_chunks) < 1: 
        raise ValueError("Code chunks list is empty")
    
    # извлечение текстов
    requirement_texts = [req["text"] for req in requirements]
    
    # если идентификаторы требований значения в сиинтаксическом пространсве не имеют, 
    # то в случае с функциями важно учесть имя_функции + текст_функции
    code_texts = [f"{chunk['name']} {chunk['content']}" for chunk in code_chunks]
    # для построение единого словаря признаков в TF-IDF сложим все текста в один
    all_texts = requirement_texts + code_texts

    # https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(all_texts)
    names = vectorizer.get_feature_names_out()

    # разделение матрицы на требования и исх. код
    X_req = X[: len(requirements)]
    X_code = X[len(requirements):]

    # временно в двойном цикле, требует оптимизации 
    # подсчёт схожести каждого вектора требования с каждым вектором исходного кода
    req_code_score_list = []
    for vec_req in X_req:
        similarity_to_req = []
        for vec_code in X_code:
            #https://numpy.org/doc/stable/reference/generated/numpy.ravel.html
            req_part = vec_req.toarray().ravel()
            code_part = vec_code.toarray().ravel()

            score = cosine_similarity(req_part, code_part)
            similarity_to_req.append(score)
        req_code_score_list.append(similarity_to_req)

    all_candidates : list[CandidateData] = []

    # Найти best score
    for req_ind, code_scores in enumerate(req_code_score_list):
        req_best_score = max(code_scores)

        requirement = requirements[req_ind]

        chunk_ind = code_scores.index(req_best_score)
        code_chunk = code_chunks[chunk_ind]

        # определение статуса кандидата (временно грубая оценка по score)

        candidate = CandidateData(
    {"requirement_key": requirement["requirement_key"] if req_best_score > 0 else None,
            "requirement_text": requirement["text"] if req_best_score > 0 else None,
            "code_chunk_name": code_chunk['name'] if req_best_score > 0 else None,
            "code_chunk_content" : code_chunk['content'] if req_best_score > 0 else None,
            "similarity_score": req_best_score,
            "candidate_status": set_candidate_status(req_best_score)})

        all_candidates.append(candidate)
    


    #similarity_matrix = cosine_similarity(X_req, X_code)
    #print(similarity_matrix)

    result = {
        "names": names.tolist(),
        "shape": list(X.shape),
        "candidates_list" : all_candidates
    }
    return result 

def set_candidate_status(score: float) -> str: 
    """
    Опреляет статус кандидата по грубой оценке score
    """
    if score >= 0.2:
        return "candidate_found"
    if score >= 0.1:
        return "ambiguous"
    return "no_candidate"

