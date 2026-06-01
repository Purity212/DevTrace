import requests
import streamlit as st

st.set_page_config(page_title="DevTrace | Projects", page_icon="DT", layout="wide")

API_BASE = "http://127.0.0.1:8000" # для общения с fastapi

def get_projects():
    response = requests.get(f"{API_BASE}/projects", timeout=10)
    response.raise_for_status()
    return response.json()

def create_project(name: str, desc: str):
    input = {"name": name, "description": desc}
    response = requests.post(f"{API_BASE}/projects", json=input, timeout=10)
    return response.json()



# GET /api/projects
st.session_state.projects_demo_data = get_projects()

st.title("Projects")
st.write("Болванка страницы проектов без привязки к API.")

# POST /api/projects
st.subheader("Создать проект") 
with st.form("create_project_form", clear_on_submit=True):
    project_name = st.text_input("Название проекта")
    project_description = st.text_area("Описание проекта")
    create_clicked = st.form_submit_button("Создать проект")

if create_clicked:
    if project_name.strip():
        next_project_id = (
            max((project["id"] for project in st.session_state.projects_demo_data), default=0) + 1
        )
        created_project = create_project(name=project_name, desc=project_description)
        st.session_state.projects_demo_data.insert(0, created_project)
        st.success(f"Демо-проект создан. Присвоен id={next_project_id}.")
    else:
        st.warning("Введите название проекта.")

if st.button("Архивировать проекты"):
    st.session_state.projects_demo_data = []
    st.info("Демо-список проектов восстановлен.")


st.subheader("Список проектов")
projects = st.session_state.projects_demo_data
st.dataframe(
    projects,
    use_container_width=True,
    hide_index=True,
)

