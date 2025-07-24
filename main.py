# main.py
import streamlit as st
from ui.menu import menu_sidebar
from views.consulta import mostrar as mostrar_consulta
from views.evolucao import mostrar as mostrar_evolucao

st.set_page_config(page_title="PokéDex", layout="wide")

pagina = menu_sidebar()

if pagina == "Consulta Pokémon":
    mostrar_consulta()
elif pagina == "Evolução":
    mostrar_evolucao()
