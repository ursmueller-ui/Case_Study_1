import streamlit as st

# ---------- TAB 1 ----------
def run_tab1():
    st.header("Tab 1")
    st.session_state.ti_tab1_name = st.text_input(
        "Name Tab 1",
        value=st.session_state.ti_tab1_name,
        key="ti_tab1_name_input"
    )

def update_name_tab_1():
    st.session_state.ti_tab1_name = ""


# ---------- TAB 2 ----------
def run_tab2():
    st.header("Tab 2")
    st.session_state.ti_tab2_name = st.text_input(
        "Name Tab 2",
        value=st.session_state.ti_tab2_name,
        key="ti_tab2_name_input"
    )

def update_name_tab_2():
    st.session_state.ti_tab2_name = ""


# Damit modular.py dieselben Namen wie vorher importieren kann:
class tab1:
    run = staticmethod(run_tab1)
    update_name_tab_1 = staticmethod(update_name_tab_1)

class tab2:
    run = staticmethod(run_tab2)
    update_name_tab_2 = staticmethod(update_name_tab_2)
