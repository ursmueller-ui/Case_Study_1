import streamlit as st

from tabs import tab1, tab2

if "name" not in st.session_state:
    st.session_state.name = ""
if "ti_tab1_name" not in st.session_state:
    st.session_state.ti_tab1_name = ""
if "ti_tab2_name" not in st.session_state:
    st.session_state.ti_tab2_name = ""

def reset():
   st.session_state.name = ""
   st.session_state.ti_tab1_name = ""
   st.session_state.ti_tab2_name = ""
   # make the text_input widgets reset
   tab1.update_name_tab_1()
   tab2.update_name_tab_2()

st.write("Current Session State:")
st.session_state

tab_1, tab_2 = st.tabs(["Tab 1", "Tab 2"])

with tab_1:
   tab1.run()
with tab_2:
   tab2.run()

st.button("Reset Session State", on_click=reset)

