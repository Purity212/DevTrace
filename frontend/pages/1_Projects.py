import streamlit as st


st.set_page_config(page_title="DevTrace | Projects", page_icon="DT", layout="wide")

# GET /api/projects
DEFAULT_PROJECTS = [  
    {"id": 2, "name": "X_eng", "description": "Y_eng"},
    {"id": 1, "name": "X", "description": "X"},
]


if "projects_demo_data" not in st.session_state:
    st.session_state.projects_demo_data = DEFAULT_PROJECTS.copy()


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
        created_project = {
            "id": next_project_id,
            "name": project_name.strip(),
            "description": project_description.strip(),
        }
        st.session_state.projects_demo_data.insert(0, created_project)
        st.success(f"Демо-проект создан. Присвоен id={next_project_id}.")
    else:
        st.warning("Введите название проекта.")

st.subheader("Список проектов")
st.dataframe(
    st.session_state.projects_demo_data,
    use_container_width=True,
    hide_index=True,
)

if st.button("Сбросить демо-проекты"):
    st.session_state.projects_demo_data = DEFAULT_PROJECTS.copy()
    st.info("Демо-список проектов восстановлен.")
