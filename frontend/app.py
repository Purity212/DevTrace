import streamlit as st

from api_client import DEFAULT_API_BASE, check_health


st.set_page_config(page_title="DevTrace", page_icon="DT", layout="wide")

if "api_base" not in st.session_state:
    st.session_state.api_base = DEFAULT_API_BASE

st.title("DevTrace: матрица верификации")
st.markdown(
    """
    DevTrace — учебный инструмент для инженера по верификации, QA-инженера и разработчика,
    которому нужно быстро связать требования с исходным кодом и получить первичную
    матрицу верификации.

    **Что уже можно показать**
    - создание проекта;
    - загрузка документа требований и исходного кода;
    - запуск анализа;
    - просмотр матрицы верификации.

    **TODO**
    - полноценная авторизация пока не реализована;
    - текущий экран входа заменен на техническую стартовую страницу.
    """
)

with st.sidebar:
    st.subheader("Подключение к API")
    st.text_input("Адрес FastAPI", key="api_base")

    if st.button("Проверить API", use_container_width=True):
        try:
            payload = check_health()
        except Exception as exc:
            st.error(f"API недоступен: {exc}")
        else:
            st.success(f"API отвечает: {payload}")

    st.caption("Запуск API: `uvicorn backend.app.main:app --reload`")

st.markdown(
    """
    **Сценарий демо**

    1. Открыть страницу проектов (`Projects`) и создать или выбрать проект.
    2. Открыть страницу документов (`Documents`) и загрузить требования и исходный код.
    3. Открыть страницу анализа (`Analysis`) и запустить анализ для показа матрицы верификации.
    """
)

selected_project_id = st.session_state.get("selected_project_id")
selected_project_label = st.session_state.get("selected_project_label")

if selected_project_id:
    st.info(f"Текущий проект: {selected_project_label}")
else:
    st.warning("Текущий проект не выбран.")
