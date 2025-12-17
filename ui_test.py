import streamlit as st
import ui_device  # Importiert Ihre bestehende UI-Logik

# Hauptüberschrift für das Mockup
st.set_page_config(page_title="Hochschul-Geräte Mockup")
st.title("Hochschul-Portal")

# Erstellung von Tabs für eine einfache Navigation
tab1, tab2 = st.tabs(["Dashboard", "Geräte-Verwaltung"])

with tab1:
    st.subheader("Willkommen!")
    st.write("Dies ist die Übersicht für Studierende und Forschende.")
    st.info("Wählen Sie den Reiter 'Geräte-Verwaltung', um Daten zu ändern.")

with tab2:
    # Hier binden wir einfach den Code aus Ihrer ui_device.py ein
    # Da der Code dort direkt auf Modulebene steht, wird er beim Import ausgeführt
    # Falls Sie ui_device.py nicht in eine Funktion gepackt haben, 
    # wird der Inhalt hier direkt angezeigt.
    st.markdown("---")
    # Der folgende Part triggert die Logik aus ui_device.py
    exec(open("ui_device.py").read())