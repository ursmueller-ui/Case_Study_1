import streamlit as st

if "sb_current_device" not in st.session_state:
    st.session_state.sb_current_device = ""

# Eine Überschrift der ersten Ebene
st.write("# Gerätemanagement")

# Eine Überschrift der zweiten Ebene
st.write("## Geräteauswahl")

# Eine Auswahlbox mit hard-gecoded Optionen, das Ergebnis

st.session_state.sb_current_device = st.selectbox(label='Gerät auswählen',
        options = ["Gerät_A", "Gerät_B"])

st.write(f"Das ausgewählte Gerät ist {st.session_state.sb_current_device}")
