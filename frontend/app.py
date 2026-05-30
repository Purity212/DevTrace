import streamlit as st


st.set_page_config(page_title="DevTrace", page_icon="DT", layout="wide")

st.title("Авторизация DevTrace")
st.write(
    "Страница входа для инженера-программиста, "
    "который проводит анализ кода и верификацию."
)

username = st.text_input("Логин")
password = st.text_input("Пароль", type="password")
workspace = st.selectbox(
    "Контур доступа", ["Анализ требований", 
     "Анализ исходного кода", 
     "Генерация матрицы трассируемости",
     "Генерация тест-кейсов",
     "Генерация отчетов"
     ]
)
remember = st.checkbox("Запомнить устройство")

if st.button("Войти"):
    if username and password:
        st.success(
            f"Демо-вход выполнен: {username}. "
            f"Выбран контур: {workspace}. "
            f"{'Устройство будет запомнено' if remember else 'Устройство не будет запомнено'}"
        )
    else:
        st.warning("Введите логин и пароль.")

st.divider()
st.markdown(
    """
    Функционал 
    - `Projects` — создание проекта и просмотр списка проектов.
    - `Documents` — загрузка документов в проект и просмотр списка документов.
    - `Analysis` — дальнейший анализ и верификация.
    """
)
