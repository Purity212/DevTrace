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
                            similarity_score: (float) - Степень смысловой схожести
                            system_status: (str) - candidate_found / ambiguous / no_candidate_found
    """
    requirement_key: str
    requirement_text: str
    code_chunk_name: str | None
    similarity_score: float
    system_status: str


def find_candidates(analyze_data : AnalyzeData) -> list[CandidateData]:
    """
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
    res = []
    for vec_req in X_req:
        similarity_to_req = []
        for vec_code in X_code:
            #https://numpy.org/doc/stable/reference/generated/numpy.ravel.html
            req_part = vec_req.toarray().ravel()
            code_part = vec_code.toarray().ravel()

            score = cosine_similarity(req_part, code_part)
            similarity_to_req.append(score)
        res.append(similarity_to_req)


    #similarity_matrix = cosine_similarity(X_req, X_code)
    #print(similarity_matrix)

    result = {
        "names": names.tolist(),
        "shape": list(X.shape),
        "res" : res
    }
    return result 

def set_candidate_status():
    pass

