import pandas as pd
import requests
import streamlit as st

from api_client import extract_error_message, run_analysis


def format_system_status(value: str | None) -> str:
    mapping = {
        "candidate_found": "Кандидат найден",
        "ambiguous": "Неоднозначно",
        "no_candidate_found": "Кандидат не найден",
    }
    return mapping.get(value or "", value or "")


def format_verifier_status(value: str | None) -> str:
    mapping = {
        "todo": "Требует проверки",
        "?": "Требует проверки",
        "approved": "Подтверждено",
        "rejected": "Отклонено",
    }
    return mapping.get(value or "", value or "")


def build_verification_matrix_df(verification_matrix: list[dict]) -> pd.DataFrame:
    matrix_df = pd.DataFrame(verification_matrix)
    if matrix_df.empty:
        return matrix_df

    matrix_df = matrix_df.rename(
        columns={
            "requirement_key": "ID требования",
            "requirement_text": "Текст требования",
            "candidate_code": "Кандидат в коде",
            "similarity_score": "Оценка схожести",
            "system_status": "Статус системы",
            "test_cases_count": "Кол-во тест-кейсов",
            "verifier_status": "Статус верификатора",
            "verifier_comment": "Комментарий верификатора",
        }
    )

    if "Статус системы" in matrix_df.columns:
        matrix_df["Статус системы"] = matrix_df["Статус системы"].apply(format_system_status)

    if "Статус верификатора" in matrix_df.columns:
        matrix_df["Статус верификатора"] = matrix_df["Статус верификатора"].apply(format_verifier_status)

    return matrix_df


def build_requirements_df(requirements: list[dict]) -> pd.DataFrame:
    requirements_df = pd.DataFrame(requirements)
    if requirements_df.empty:
        return requirements_df

    return requirements_df.rename(
        columns={
            "id": "ID",
            "project_id": "ID проекта",
            "requirement_key": "ID требования",
            "text": "Текст требования",
        }
    )


def build_code_chunks_df(code_chunks: list[dict]) -> pd.DataFrame:
    code_chunks_df = pd.DataFrame(code_chunks)
    if code_chunks_df.empty:
        return code_chunks_df

    return code_chunks_df.rename(
        columns={
            "id": "ID",
            "project_id": "ID проекта",
            "filename": "Файл",
            "function_name": "Функция",
            "name": "Функция",
            "content": "Содержимое",
            "start_line": "Начальная строка",
            "end_line": "Конечная строка",
        }
    )


def build_candidates_df(candidates: list[dict]) -> pd.DataFrame:
    candidates_df = pd.DataFrame(candidates)
    if candidates_df.empty:
        return candidates_df

    candidates_df = candidates_df.rename(
        columns={
            "requirement_key": "ID требования",
            "requirement_text": "Текст требования",
            "code_chunk_name": "Кандидат в коде",
            "code_chunk_content": "Фрагмент кода",
            "similarity_score": "Оценка схожести",
            "candidate_status": "Статус системы",
        }
    )

    if "Статус системы" in candidates_df.columns:
        candidates_df["Статус системы"] = candidates_df["Статус системы"].apply(format_system_status)

    return candidates_df


st.title("Анализ и матрица верификации")
st.write("Запуск анализа по документам проекта и просмотр матрицы верификации.")

selected_project_id = st.session_state.get("selected_project_id")
selected_project_label = st.session_state.get("selected_project_label")

if not selected_project_id:
    st.warning("Сначала выберите проект на странице «Проекты».")
    st.stop()

st.info(f"Активный проект: {selected_project_label}")

if st.button("Запустить анализ", type="primary", use_container_width=True):
    try:
        analysis_result = run_analysis(selected_project_id)
    except requests.HTTPError as exc:
        st.error(extract_error_message(exc.response))
    except requests.RequestException as exc:
        st.error(f"Ошибка запуска анализа: {exc}")
    else:
        st.session_state.analysis_result = analysis_result
        st.success("Анализ завершен.")

analysis_result = st.session_state.get("analysis_result")

if not analysis_result:
    st.info("Результатов анализа пока нет. Нажмите «Запустить анализ».")
    st.stop()

requirements = analysis_result.get("requirements", [])
code_chunks = analysis_result.get("code_chunks", [])
candidates = analysis_result.get("candidates", [])
verification_matrix = analysis_result.get("verification_matrix", [])

st.subheader("Сводка")
metric_col_1, metric_col_2, metric_col_3, metric_col_4 = st.columns(4)

metric_col_1.metric("Требования", len(requirements))
metric_col_2.metric("Фрагменты кода", len(code_chunks))
metric_col_3.metric(
    "Кандидаты найдены",
    sum(1 for row in verification_matrix if row.get("system_status") == "candidate_found"),
)
metric_col_4.metric(
    "Неоднозначно",
    sum(1 for row in verification_matrix if row.get("system_status") == "ambiguous"),
)

st.subheader("Матрица верификации")
if verification_matrix:
    matrix_df = build_verification_matrix_df(verification_matrix)

    status_options = sorted(matrix_df["Статус системы"].dropna().unique().tolist())
    selected_statuses = st.multiselect(
        "Фильтр по статусу",
        options=status_options,
        default=status_options,
    )
    min_similarity = st.slider(
        "Минимальная оценка схожести",
        min_value=0.0,
        max_value=1.0,
        value=0.0,
        step=0.01,
    )
    search_text = st.text_input(
        "Поиск по требованию или кандидату в коде",
        placeholder="Например: FR-001 или parse_request",
    ).strip().lower()

    filtered_df = matrix_df.copy()
    if selected_statuses:
        filtered_df = filtered_df[filtered_df["Статус системы"].isin(selected_statuses)]
    filtered_df = filtered_df[filtered_df["Оценка схожести"] >= min_similarity]
    if search_text:
        requirement_mask = (
            filtered_df["Текст требования"].fillna("").str.lower().str.contains(search_text, regex=False)
        )
        candidate_mask = (
            filtered_df["Кандидат в коде"].fillna("").str.lower().str.contains(search_text, regex=False)
        )
        requirement_id_mask = (
            filtered_df["ID требования"].fillna("").astype(str).str.lower().str.contains(search_text, regex=False)
        )
        filtered_df = filtered_df[requirement_mask | candidate_mask | requirement_id_mask]

    st.caption(f"Строк в таблице: {len(filtered_df)}")

    st.data_editor(
        filtered_df,
        use_container_width=True,
        hide_index=True,
        disabled=True,
        column_config={
            "ID требования": st.column_config.TextColumn("ID требования", width="medium"),
            "Текст требования": st.column_config.TextColumn("Текст требования", width="large"),
            "Кандидат в коде": st.column_config.TextColumn("Кандидат в коде", width="medium"),
            "Оценка схожести": st.column_config.NumberColumn(
                "Оценка схожести", min_value=0.0, max_value=1.0, format="%.5f"
            ),
            "Статус системы": st.column_config.TextColumn("Статус системы", width="medium"),
            "Кол-во тест-кейсов": st.column_config.NumberColumn("Кол-во тест-кейсов", width="small"),
            "Статус верификатора": st.column_config.TextColumn("Статус верификатора", width="medium"),
            "Комментарий верификатора": st.column_config.TextColumn("Комментарий верификатора", width="medium"),
        },
    )
else:
    st.warning("Матрица верификации пуста.")

tab_requirements, tab_chunks, tab_candidates, tab_raw = st.tabs(
    ["Требования", "Фрагменты кода", "Кандидаты", "Сырые данные"]
)

with tab_requirements:
    st.data_editor(
        build_requirements_df(requirements),
        use_container_width=True,
        hide_index=True,
        disabled=True,
    )

with tab_chunks:
    st.data_editor(
        build_code_chunks_df(code_chunks),
        use_container_width=True,
        hide_index=True,
        disabled=True,
    )

with tab_candidates:
    st.data_editor(
        build_candidates_df(candidates),
        use_container_width=True,
        hide_index=True,
        disabled=True,
    )

with tab_raw:
    st.json(analysis_result)
