"""
⚓ Ítaca OS 2.0
Plataforma Integral de Gestión y Desarrollo Humano
"""
import streamlit as st
import sys
import os
import importlib

# ── CRITICAL: Ensure project root is in Python path ──
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

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

# ═══════════════════════════════════════════════════════
# 🪪 BLOQUEO DE PASAPORTE: Si no tiene DISC → forzar test
# ═══════════════════════════════════════════════════════
def _check_pasaporte():
    """
    Retorna True si el usuario necesita completar el Pasaporte.
    Condición: tiene email seleccionado pero NO tiene arquetipo_disc.
    """
    email = st.session_state.get("current_user")
    if not email:
        return False  # No hay usuario seleccionado aún
    ident = db.get_identidad(email)
    if not ident:
        return False
    # Si no tiene arquetipo → necesita Pasaporte
    return not ident.get("arquetipo_disc")

# ── SIDEBAR (siempre renderizar para seleccionar usuario) ──
from components.sidebar import render_sidebar
render_sidebar()

# ── VERIFICAR PASAPORTE ──
necesita_pasaporte = _check_pasaporte()

if necesita_pasaporte:
    # ══════════════════════════════════════════
    # MODO PASAPORTE: Solo mostrar el test DISC
    # El sidebar ya se renderizó (para que seleccione usuario)
    # pero forzamos la vista al Pasaporte
    # ══════════════════════════════════════════
    try:
        from pages.pasaporte import render as render_pasaporte
        render_pasaporte()
    except Exception as e:
        st.error(f"Error cargando Pasaporte: {e}")
        import traceback
        st.code(traceback.format_exc())

else:
    # ══════════════════════════════════════════
    # MODO NORMAL: Navegación completa
    # ══════════════════════════════════════════
    PAGE_MAP = {
        "Inicio": "pages.home",
        "Mi Esencia": "pages.mi_esencia",
        "Mi Estrategia": "pages.mi_estrategia",
        "Mi Hexágono": "pages.hexagono",
        "Cultura Ítaca": "pages.cultura",
        "Mi Brújula": "pages.brujula",
        "Mis Logros": "pages.logros",
        "Notificaciones": "pages.notificaciones",
        "Admin Dashboard": "pages.admin",
    }

    page = st.session_state.get("current_page", "Inicio")
    module_name = PAGE_MAP.get(page)

    if module_name:
        try:
            mod = importlib.import_module(module_name)
            mod.render()
        except Exception as e:
            st.error(f"Error cargando '{page}': {e}")
            import traceback
            st.code(traceback.format_exc())
    else:
        st.error(f"Página no encontrada: {page}")
