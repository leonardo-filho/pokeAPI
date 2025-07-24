import streamlit as st
from streamlit_option_menu import option_menu

def menu_sidebar():
    with st.sidebar:
        escolha = option_menu(
            menu_title="🔍 PokéDex",
            options=["Consulta Pokémon", "Evoluções"],
            icons=["search", "diagram-3"],
            menu_icon="cast",
            default_index=0,
            styles={
                "container": {
                    "padding": "5px",
                    "background-color": "#2a2a2a"
                },
                "icon": {"color": "yellow", "font-size": "18px"},
                "nav-link": {
                    "color": "white",
                    "font-size": "16px",
                    "text-align": "left",
                    "margin": "5px",
                    "border-radius": "5px"
                },
                "nav-link-selected": {
                    "background-color": "#3f51b5",  # tom azul
                    "color": "white"
                }
            }
        )
    return escolha
