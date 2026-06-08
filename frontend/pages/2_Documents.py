import requests
import streamlit as st


st.set_page_config(page_title="DevTrace | Documents", page_icon="DT", layout="wide")

API_BASE = "http://127.0.0.1:8000" # для общения с fastapi

def get_documents():
    response = requests.get(f"{API_BASE}/documents", timeout=10)
    response.raise_for_status()
    return response.json()

def create_document(document_type: str, file):
    input = {"document_type": document_type, "file": file}
    response = requests.post(f"{API_BASE}/documents", json=input, timeout=10)
    return response.json()


# DEFAULT_PROJECTS = [
#     {"id": 2, "name": "X_eng", "description": "Y_eng"},
#     {"id": 1, "name": "X", "description": "X"},
# ]

# GET /api/projects/{project_id}/documents
# DEFAULT_DOCUMENTS = [
#     {
#         "id": 2,
#         "project_id": 2,
#         "filename": "flight_requirements_v1.docx",
#         "document_type": "requirement",
#     },
#     {
#         "id": 1,
#         "project_id": 2,
#         "filename": "autopilot_controller.cpp",
#         "document_type": "source_code",
#     },
# ]


# if "projects_demo_data" not in st.session_state:
#     st.session_state.projects_demo_data = DEFAULT_PROJECTS.copy()

# if "documents_demo_data" not in st.session_state:
#     st.session_state.documents_demo_data = DEFAULT_DOCUMENTS.copy()


st.title("Documents")
st.write("Болванка страницы документов без привязки к API.")

projects = st.session_state.projects_demo_data
#documents = st.session_state.documents_demo_data

if not projects:
    st.warning("Сначала создайте проект на вкладке Projects.")
    st.stop()

project_options = {
    f"{project['id']} - {project['name']}": project["id"] for project in projects
}

selected_project_label = st.selectbox("Проект", list(project_options.keys()))
selected_project_id = project_options[selected_project_label]

# POST /api/projects/{project_id}/documents
st.subheader("Загрузить документ")
with st.form("upload_document_form", clear_on_submit=True):
    document_type = st.selectbox(
        "Тип документа",
        ["requirement", "source_code"],
        format_func=lambda value: "Требование" if value == "requirement" else "Исходный код",
    )
    uploaded_file = st.file_uploader("Документ")
    upload_clicked = st.form_submit_button("Загрузить документ")

if upload_clicked:
    if uploaded_file is None:
        st.warning("Выберите файл.")
    else:
        next_document_id = (
            max((document["id"] for document in st.session_state.documents_demo_data), default=0) + 1
        )
        created_document = {
            "id": next_document_id,
            "project_id": selected_project_id,
            "filename": uploaded_file.name,
            "document_type": document_type,
        }
        st.session_state.documents_demo_data.insert(0, created_document)
        st.success(
            f"Демо-документ добавлен в проект id={selected_project_id}. "
            f"Присвоен id={next_document_id}."
        )

project_documents = [
    document
    for document in st.session_state.documents_demo_data
    if document["project_id"] == selected_project_id
]

st.subheader("Список документов проекта")
st.dataframe(
    project_documents,
    use_container_width=True,
    hide_index=True,
)

# if st.button("Сбросить демо-документы"):
#     st.session_state.documents_demo_data = DEFAULT_DOCUMENTS.copy()
#     st.info("Демо-список документов восстановлен.")
