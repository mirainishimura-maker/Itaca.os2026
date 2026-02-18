"""
⚓ Ítaca OS 2.0
Plataforma Integral de Gestión y Desarrollo Humano
"""
import streamlit as st
import sys
import os

# Esto asegura que Streamlit encuentre tus carpetas 'components' y 'pages'
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import APP_NAME, APP_ICON, GLOBAL_CSS
import database as db

# Add project root to path
sys.path.insert(0, os.path.dirname(__file__))

from config import APP_NAME, APP_ICON, GLOBAL_CSS
import database as db

# ── PAGE CONFIG ──
st.set_page_config(
    page_title=f"{APP_ICON} {APP_NAME}",
    page_icon="⚓",
    layout="centered",
    initial_sidebar_state="expanded",
)

# ── GLOBAL CSS ──
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

# ── INIT DB ──
db.init_db()

# ── SIDEBAR ──
from components.sidebar import render_sidebar
render_sidebar()

# ── ROUTER ──
page = st.session_state.get("current_page", "Inicio")

if page == "Inicio":
    from pages.home import render
    render()
elif page == "Mi Esencia":
    from pages.mi_esencia import render
    render()
elif page == "Mi Estrategia":
    from pages.mi_estrategia import render
    render()
elif page == "Mi Hexágono":
    from pages.hexagono import render
    render()
elif page == "Cultura Ítaca":
    from pages.cultura import render
    render()
elif page == "Mi Brújula":
    from pages.brujula import render
    render()
elif page == "Mis Logros":
    from pages.logros import render
    render()
elif page == "Notificaciones":
    from pages.notificaciones import render
    render()
elif page == "Admin Dashboard":
    from pages.admin import render
    render()
else:
    st.error(f"Página no encontrada: {page}")
