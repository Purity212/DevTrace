import pandas as pd
import requests
import streamlit as st

from api_client import create_project, extract_error_message, get_projects


st.title("Проекты")
st.write("Создание проекта, выбор активного проекта и локальная очистка списка в интерфейсе.")

if "projects_hidden" not in st.session_state:
    st.session_state.projects_hidden = False

try:
    projects = get_projects()
except requests.RequestException as exc:
    st.error(f"Не удалось получить список проектов: {exc}")
    st.stop()

st.subheader("Создать проект")
with st.form("create_project_form", clear_on_submit=True):
    project_name = st.text_input("Название проекта")
    project_description = st.text_area("Описание проекта")
    create_clicked = st.form_submit_button("Создать проект")

if create_clicked:
    if not project_name.strip():
        st.warning("Введите название проекта.")
    else:
        try:
            created_project = create_project(
                name=project_name.strip(),
                description=project_description.strip() or None,
            )
        except requests.HTTPError as exc:
            st.error(extract_error_message(exc.response))
        except requests.RequestException as exc:
            st.error(f"Ошибка создания проекта: {exc}")
        else:
            st.session_state.selected_project_id = created_project["id"]
            st.session_state.selected_project_label = (
                f"{created_project['id']} - {created_project['name']}"
            )
            st.session_state.projects_hidden = False
            st.success(
                f"Проект создан: id={created_project['id']}, name={created_project['name']}"
            )
            st.rerun()

st.subheader("Выбрать активный проект")
if not projects:
    st.info("Проектов пока нет.")
    st.stop()

project_options = {
    f"{project['id']} - {project['name']}": project["id"]
    for project in projects
}

default_index = 0
current_label = st.session_state.get("selected_project_label")
if current_label in project_options:
    default_index = list(project_options.keys()).index(current_label)

selected_project_label = st.selectbox(
    "Проект",
    options=list(project_options.keys()),
    index=default_index,
)
selected_project_id = project_options[selected_project_label]

st.session_state.selected_project_id = selected_project_id
st.session_state.selected_project_label = selected_project_label

controls_col_1, controls_col_2 = st.columns(2)
with controls_col_1:
    if st.button("Очистить список на экране", use_container_width=True):
        st.session_state.projects_hidden = True
        st.info("Список проектов скрыт только в Streamlit. Данные в API не удаляются.")

with controls_col_2:
    if st.button("Показать список снова", use_container_width=True):
        st.session_state.projects_hidden = False
        st.rerun()

st.success(f"Активный проект: {selected_project_label}")

st.subheader("Список проектов")
if st.session_state.projects_hidden:
    st.info("Список проектов скрыт локально.")
else:
    projects_df = pd.DataFrame(projects).rename(
        columns={
            "id": "ID",
            "name": "Название",
            "description": "Описание",
        }
    )
    st.data_editor(
        projects_df,
        use_container_width=True,
        hide_index=True,
        disabled=True,
        column_config={
            "ID": st.column_config.NumberColumn("ID", width="small"),
            "Название": st.column_config.TextColumn("Название", width="medium"),
            "Описание": st.column_config.TextColumn("Описание", width="large"),
        },
    )
