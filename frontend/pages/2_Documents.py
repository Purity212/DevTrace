from datetime import datetime

import pandas as pd
import requests
import streamlit as st

from api_client import extract_error_message, get_documents, upload_document


def format_document_type(document_type: str) -> str:
    mapping = {
        "requirements": "Требования",
        "source_code": "Исходный код",
    }
    return mapping.get(document_type, document_type)


def format_created_at(value: str | None) -> str:
    if not value:
        return ""

    try:
        dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return value

    return dt.strftime("%d.%m.%Y %H:%M:%S")


st.title("Документы")
st.write("Загрузка документов требований и исходного кода в активный проект.")

selected_project_id = st.session_state.get("selected_project_id")
selected_project_label = st.session_state.get("selected_project_label")

if not selected_project_id:
    st.warning("Сначала выберите проект на странице «Проекты».")
    st.stop()

st.info(f"Активный проект: {selected_project_label}")

requirements_file = st.file_uploader(
    "Документ требований",
    type=["md", "txt"],
    key="requirements_file",
)

if st.button("Загрузить требования", use_container_width=True):
    if requirements_file is None:
        st.warning("Выберите файл требований.")
    else:
        try:
            uploaded = upload_document(
                project_id=selected_project_id,
                document_type="requirements",
                uploaded_file=requirements_file,
            )
        except requests.HTTPError as exc:
            st.error(extract_error_message(exc.response))
        except requests.RequestException as exc:
            st.error(f"Ошибка загрузки документа требований: {exc}")
        else:
            st.success(f"Загружен файл: {uploaded['filename']}")
            st.rerun()

source_code_file = st.file_uploader(
    "Документ исходного кода",
    type=["py"],
    key="source_code_file",
)

st.caption("Для MVP принимаются только Python-файлы `.py`.")

if st.button("Загрузить исходный код", use_container_width=True):
    if source_code_file is None:
        st.warning("Выберите файл исходного кода.")
    else:
        try:
            uploaded = upload_document(
                project_id=selected_project_id,
                document_type="source_code",
                uploaded_file=source_code_file,
            )
        except requests.HTTPError as exc:
            st.error(extract_error_message(exc.response))
        except requests.RequestException as exc:
            st.error(f"Ошибка загрузки исходного кода: {exc}")
        else:
            st.success(f"Загружен файл: {uploaded['filename']}")
            st.rerun()

st.subheader("Документы проекта")
try:
    documents = get_documents(selected_project_id)
except requests.HTTPError as exc:
    st.error(extract_error_message(exc.response))
except requests.RequestException as exc:
    st.error(f"Не удалось получить документы проекта: {exc}")
else:
    if documents:
        documents_df = pd.DataFrame(documents)
        documents_df["document_type"] = documents_df["document_type"].map(format_document_type)
        if "created_at" in documents_df.columns:
            documents_df["created_at"] = documents_df["created_at"].apply(format_created_at)

        documents_df = documents_df.rename(
            columns={
                "id": "ID",
                "project_id": "ID проекта",
                "filename": "Файл",
                "document_type": "Тип документа",
                "created_at": "Дата загрузки",
            }
        )

        visible_columns = ["ID", "Файл", "Тип документа", "Дата загрузки"]
        visible_columns = [column for column in visible_columns if column in documents_df.columns]

        st.data_editor(
            documents_df[visible_columns],
            use_container_width=True,
            hide_index=True,
            disabled=True,
            column_config={
                "ID": st.column_config.NumberColumn("ID", width="small"),
                "Файл": st.column_config.TextColumn("Файл", width="large"),
                "Тип документа": st.column_config.TextColumn("Тип документа", width="medium"),
                "Дата загрузки": st.column_config.TextColumn("Дата загрузки", width="medium"),
            },
        )
    else:
        st.info("Документы для проекта пока не загружены.")
