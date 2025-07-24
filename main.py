import streamlit as st
from ui.menu import menu_sidebar
from ui.views.consulta import mostrar as mostrar_consulta
from ui.views.evolucao import mostrar as mostrar_evolucao


st.set_page_config(page_title="PokéDex", layout="wide")

pagina, lang = menu_sidebar()

if pagina == "consulta":
    mostrar_consulta(lang)
elif pagina == "evolucao":
    mostrar_evolucao(lang)