# REQUIREMENTS_DevTrace

## DevTrace Verification Assistant — MVP 1

---

## 1. Название проекта

**DevTrace Verification Assistant — MVP 1**

---

## 2. Цель MVP 1

Разработать учебный прототип инструмента поддержки верификатора инженерного ПО.

MVP 1 должен закрывать курсовое ТЗ:

| Требование курсовой | Реализация в MVP 1 |
|---|---|
| GitHub repository | Репозиторий проекта |
| Backend | FastAPI |
| 2+ endpoints | Несколько API endpoints |
| Frontend | Streamlit |
| БД | SQLite |
| ML / AI bonus | TF-IDF similarity для поиска связи требование → код |
| Docker/docker-compose bonus | Минимальный docker-compose |

---

## 3. Краткое описание продукта

**DevTrace** принимает файл с требованиями и файл с исходным кодом, автоматически извлекает требования, ищет возможные связанные фрагменты кода, генерирует черновики тест-кейсов и формирует verification matrix.

Главная идея MVP 1:

```text
requirements.md + source_code.py/.c
        ↓
extracted requirements
        ↓
candidate code links
        ↓
draft test cases
        ↓
verification matrix
        ↓
CSV export
```

---

## 4. Ограничение MVP 1

MVP 1 — это **не полноценный AI/RAG-продукт**.

В MVP 1 **не используются**:

```text
OpenAI API
Qdrant
PostgreSQL
LangChain
PDF/DOCX
авторизация
многопользовательский режим
```

MVP 1 использует простой и объяснимый ML-lite подход:

```text
TF-IDF + cosine similarity ???
```

---

## 5. Пользователь

Основной пользователь:

```text
верификатор / QA-инженер / инженер по тестированию инженерного ПО
```

Пользователь хочет быстро получить первичную матрицу:

```text
требование → возможная реализация в коде → черновик тест-кейса → статус проверки человеком
```

---

## 6. Стек MVP 1

| Слой | Технология |
|---|---|
| Backend | FastAPI |
| Frontend | Streamlit |
| Database | SQLite |
| ORM | SQLAlchemy |
| Validation | Pydantic |
| ML-lite | scikit-learn TF-IDF |
| Data export | pandas / csv |
| Tests | pytest, минимум |
| Containerization | Docker Compose |

---

## 7. Входные данные

### 7.1. Requirements file

Поддерживаемые форматы:

```text
.md
.txt
```

Пример:

```text
REQ-CTRL-001: При запуске система должна выполнить self-test памяти.
REQ-CTRL-002: Если self-test завершился ошибкой, система должна установить error_flag.
REQ-CTRL-003: При активном error_flag команда управления должна игнорироваться.
```

### 7.2. Source code file

Поддерживаемые форматы:

```text
.py
.c
.txt
```

Пример:

```python
def startup_self_test():
    return memory_check()

def init_system():
    result = startup_self_test()
    if result != 0:
        error_flag = True
```

---

## 8. Выходные данные

MVP 1 должен формировать:

```text
1. список извлечённых требований;
2. список фрагментов кода;
3. candidate links requirement → code;
4. draft test cases;
5. verification matrix;
6. CSV export.
```

---

## 9. Функциональные требования

### FR-001. Создание проекта

Система должна позволять создать проект анализа.

Минимальные поля проекта:

| Поле | Описание |
|---|---|
| name | название проекта |
| description | краткое описание |

Пример:

```text
Safety Monitor Demo
```

---

### FR-002. Загрузка requirements-файла

Пользователь должен иметь возможность загрузить файл с требованиями.

Поддерживаемые расширения:

```text
.md
.txt
```

После загрузки файл сохраняется в SQLite как документ типа:

```text
requirements
```

---

### FR-003. Загрузка source code файла

Пользователь должен иметь возможность загрузить файл с исходным кодом.

Поддерживаемые расширения:

```text
.py
.c
.txt
```

После загрузки файл сохраняется в SQLite как документ типа:

```text
code
```

---

### FR-004. Извлечение требований

Система должна извлекать требования из requirements-файла.

Основной поддерживаемый формат:

```text
REQ-CTRL-001: текст требования
REQ-001: текст требования
```

Минимальные поля требования:

| Поле | Описание |
|---|---|
| external_id | ID требования |
| text | текст требования |
| source_document_id | документ-источник |

Если ID не найден, система может создать ID вида:

```text
AUTO-REQ-001
```

---

### FR-005. Извлечение фрагментов кода

Система должна извлекать фрагменты кода.

Для Python:

```text
def function_name(...):
```

Для C:

```text
void function_name(...)
int function_name(...)
```

Минимальные поля code chunk:

| Поле | Описание |
|---|---|
| name | имя функции или блока |
| content | текст фрагмента |
| start_line | начальная строка |
| end_line | конечная строка |

---

### FR-006. Поиск candidate links

Система должна искать возможную связь между каждым требованием и фрагментом кода.

Алгоритм MVP 1:

```text
TF-IDF vectorization
cosine similarity
top-1 candidate code chunk
```

Для каждого требования система сохраняет:

| Поле | Описание |
|---|---|
| requirement_id | требование |
| code_chunk_id | найденный фрагмент кода |
| similarity_score | оценка похожести |
| system_status | статус системы |

Статусы:

| Условие | Статус |
|---|---|
| score >= 0.25 | candidate_found |
| 0.10 <= score < 0.25 | ambiguous |
| score < 0.10 | no_candidate_found |

---

### FR-007. Генерация draft test cases

Система должна автоматически создать минимум один черновик тест-кейса для каждого требования.

Поля тест-кейса:

| Поле | Описание |
|---|---|
| test_case_id | ID тест-кейса |
| title | название |
| preconditions | предусловия |
| steps | шаги |
| expected_result | ожидаемый результат |
| test_type | positive / negative |
| status | draft / approved / edited / rejected |

Шаблон ID:

```text
TC-CTRL-001-001
```

---

### FR-008. Verification Matrix

Система должна формировать таблицу verification matrix.

Обязательные колонки:

| Колонка | Описание |
|---|---|
| Requirement ID | ID требования |
| Requirement Text | текст требования |
| Candidate Code | найденный фрагмент кода |
| Similarity Score | оценка похожести |
| System Status | candidate_found / ambiguous / no_candidate_found |
| Test Cases | количество тест-кейсов |
| Verifier Status | pending / approved / rejected / needs_work |
| Verifier Comment | комментарий пользователя |

---

### FR-009. Human-in-the-loop review

Пользователь должен иметь возможность изменить решение по каждой строке verification matrix.

Доступные действия:

```text
approve
reject
needs_work
edit comment
```

Статусы верификатора:

```text
pending
approved
rejected
needs_work
```

---

### FR-010. Редактирование тест-кейсов

Пользователь должен иметь возможность открыть тест-кейс и изменить:

```text
title
preconditions
steps
expected_result
test_type
status
comment
```

---

### FR-011. Добавление тест-кейса вручную

Пользователь должен иметь возможность добавить новый тест-кейс к выбранному требованию.

---

### FR-012. Экспорт CSV

Пользователь должен иметь возможность экспортировать verification matrix в CSV.

Файл должен содержать:

```text
Requirement ID
Requirement Text
Candidate Code
Similarity Score
System Status
Verifier Status
Verifier Comment
Test Cases Count
```

---

## 10. Нефункциональные требования

### NFR-001. Локальный запуск

Проект должен запускаться локально.

Backend:

```bash
uvicorn backend.app.main:app --reload
```

Frontend:

```bash
streamlit run frontend/streamlit_app.py
```

---

### NFR-002. Docker Compose

Проект должен иметь минимальный `docker-compose.yml` для запуска:

```text
backend
frontend
```

SQLite может храниться в volume.

---

### NFR-003. Простота

MVP 1 должен быть реализован без лишней инфраструктуры.

Запрещено добавлять в MVP 1:

```text
Qdrant
OpenAI
PostgreSQL
авторизацию
сложные роли пользователей
```

---

### NFR-004. Объяснимость

Алгоритм поиска связей должен быть объяснимым:

```text
TF-IDF similarity score
```

Пользователь должен видеть similarity score в matrix.

---

### NFR-005. Расширяемость

Код должен быть структурирован так, чтобы позже можно было заменить:

| MVP 1 | Future |
|---|---|
| SQLite | PostgreSQL |
| TF-IDF | embeddings + Qdrant |
| шаблонные тест-кейсы | LLM-generated test cases |
| простой parser | AST/parser-based analysis |

---

## 11. Модель данных

### projects

| Поле | Тип |
|---|---|
| id | int |
| name | str |
| description | str |
| created_at | datetime |

---

### documents

| Поле | Тип |
|---|---|
| id | int |
| project_id | int |
| filename | str |
| document_type | str |
| content | text |
| created_at | datetime |

---

### requirements

| Поле | Тип |
|---|---|
| id | int |
| project_id | int |
| external_id | str |
| text | text |
| source_document_id | int |

---

### code_chunks

| Поле | Тип |
|---|---|
| id | int |
| project_id | int |
| name | str |
| content | text |
| source_document_id | int |
| start_line | int |
| end_line | int |

---

### verification_items

| Поле | Тип |
|---|---|
| id | int |
| requirement_id | int |
| code_chunk_id | int / null |
| similarity_score | float |
| system_status | str |
| verifier_status | str |
| verifier_comment | text |

---

### test_cases

| Поле | Тип |
|---|---|
| id | int |
| requirement_id | int |
| external_id | str |
| title | str |
| preconditions | text |
| steps | text |
| expected_result | text |
| test_type | str |
| status | str |
| verifier_comment | text |

---

## 12. API требования

### API-001. Создать проект

```http
POST /projects
```

Request:

```json
{
  "name": "Safety Monitor Demo",
  "description": "Demo project for MVP 1"
}
```

Response:

```json
{
  "id": 1,
  "name": "Safety Monitor Demo"
}
```

---

### API-002. Получить список проектов

```http
GET /projects
```

---

### API-003. Загрузить документ

```http
POST /projects/{project_id}/documents
```

Параметры:

```text
file
document_type: requirements | code
```

---

### API-004. Получить документы проекта

```http
GET /projects/{project_id}/documents
```

---

### API-005. Запустить анализ

```http
POST /projects/{project_id}/analyze
```

Действия:

```text
1. extract requirements
2. extract code chunks
3. calculate similarity
4. create verification items
5. generate draft test cases
```

---

### API-006. Получить verification matrix

```http
GET /projects/{project_id}/verification-matrix
```

---

### API-007. Обновить решение верификатора

```http
PATCH /verification-items/{item_id}
```

Request:

```json
{
  "verifier_status": "approved",
  "verifier_comment": "Связь подтверждена"
}
```

---

### API-008. Получить тест-кейсы требования

```http
GET /requirements/{requirement_id}/test-cases
```

---

### API-009. Обновить тест-кейс

```http
PATCH /test-cases/{test_case_id}
```

---

### API-010. Добавить тест-кейс вручную

```http
POST /requirements/{requirement_id}/test-cases
```

---

### API-011. Экспорт CSV

```http
GET /projects/{project_id}/export/csv
```

---

## 13. UI требования

### UI-001. Project Dashboard

Экран должен показывать:

```text
название проекта
количество документов
количество требований
количество найденных связей
количество ambiguous связей
количество no_candidate_found
количество тест-кейсов
```

---

### UI-002. Upload Documents

Экран должен позволять:

```text
выбрать проект
загрузить requirements-файл
загрузить code-файл
выбрать тип документа
запустить анализ
```

---

### UI-003. Verification Matrix

Главный экран MVP 1.

Таблица должна показывать:

```text
Requirement ID
Requirement Text
Candidate Code
Similarity Score
System Status
Verifier Status
Action
```

---

### UI-004. Review Requirement

Экран должен показывать:

```text
текст требования
найденный фрагмент кода
similarity score
system status
verifier status
verifier comment
```

Пользователь может изменить:

```text
verifier status
verifier comment
```

---

### UI-005. Test Case Editor

Экран должен позволять редактировать:

```text
title
preconditions
steps
expected_result
test_type
status
comment
```

---

### UI-006. Export

Экран должен позволять скачать:

```text
verification_matrix.csv
```

---

## 14. Структура репозитория

```text
devtrace-verification-assistant/
├── backend/
│   └── app/
│       ├── main.py
│       ├── database.py
│       ├── models.py
│       ├── schemas.py
│       ├── api/
│       │   ├── projects.py
│       │   ├── documents.py
│       │   ├── analysis.py
│       │   ├── verification.py
│       │   └── test_cases.py
│       └── services/
│           ├── requirement_extractor.py
│           ├── code_extractor.py
│           ├── similarity_service.py
│           ├── test_case_generator.py
│           └── export_service.py
│
├── frontend/
│   └── streamlit_app.py
│
├── data/
│   └── demo/
│       ├── requirements.md
│       └── source_code.py
│
├── tests/
│   ├── test_requirement_extractor.py
│   ├── test_code_extractor.py
│   └── test_similarity_service.py
│
├── docker-compose.yml
├── requirements.txt
├── README.md
└── .gitignore
```

---

## 15. Demo dataset

### requirements.md

```text
REQ-CTRL-001: При запуске система должна выполнить self-test памяти.
REQ-CTRL-002: Если self-test завершился ошибкой, система должна установить error_flag.
REQ-CTRL-003: При активном error_flag команда управления должна игнорироваться.
REQ-CTRL-004: При успешном self-test система должна перейти в normal mode.
```

### source_code.py

```python
error_flag = False
mode = "INIT"

def memory_self_test():
    return 0

def init_system():
    global error_flag, mode
    result = memory_self_test()

    if result != 0:
        error_flag = True
        mode = "SAFE"
    else:
        mode = "NORMAL"

def handle_command(command):
    if mode == "SAFE":
        return "ignored"

    return f"executed: {command}"
```

---

## 16. Критерии приёмки MVP 1

MVP 1 считается завершённым, если выполнены условия:

| № | Критерий |
|---:|---|
| 1 | Проект опубликован на GitHub |
| 2 | Backend запускается через FastAPI |
| 3 | Frontend запускается через Streamlit |
| 4 | Есть SQLite БД |
| 5 | Можно создать проект |
| 6 | Можно загрузить requirements-файл |
| 7 | Можно загрузить code-файл |
| 8 | Система извлекает требования |
| 9 | Система извлекает фрагменты кода |
| 10 | Система считает TF-IDF similarity |
| 11 | Система формирует verification matrix |
| 12 | Система генерирует draft test cases |
| 13 | Пользователь может изменить verifier status |
| 14 | Пользователь может редактировать test case |
| 15 | Можно экспортировать CSV |
| 16 | Есть README с инструкцией запуска |
| 17 | Есть docker-compose.yml |
| 18 | Есть минимум 3 pytest-теста для сервисного слоя |

---

## 17. Что не входит в MVP 1

```text
OpenAI API
Qdrant
PostgreSQL
LangChain
PDF parsing
DOCX parsing
Excel import
авторизация
роли пользователей
история версий матрицы
audit trail
сложный dashboard
production deployment
```

---

## 18. Итоговая формула MVP 1

```text
DevTrace MVP 1 = FastAPI + Streamlit + SQLite + TF-IDF + verification matrix + draft test cases + human review + CSV export
```
