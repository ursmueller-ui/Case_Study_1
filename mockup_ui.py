import streamlit as st
from devices import Device
from queries import find_devices

# Konfiguration der Seite
st.set_page_config(page_title="Hochschul-Geräteverwaltung", layout="wide")

st.title("🎓 Hochschul-Geräteverwaltung")
st.markdown("Verwalten Sie hier Laser-Cutter, 3D-Drucker und andere Ressourcen.")

# --- Sidebar für Navigation ---
st.sidebar.header("Navigation")
page = st.sidebar.radio("Gehe zu:", ["Dashboard / Übersicht", "Gerät bearbeiten", "Neues Gerät anlegen"])

# --- DATEN LADEN ---
all_device_names = find_devices()

if page == "Dashboard / Übersicht":
    st.header("Aktuelle Geräteübersicht")
    
    # Metriken anzeigen
    col1, col2 = st.columns(2)
    col1.metric("Anzahl Geräte gesamt", len(all_device_names))
    col2.metric("Systemstatus", "Online")

    # Tabelle der Geräte (Mockup-Visualisierung)
    st.subheader("Geräteliste")
    devices_objects = Device.find_all()
    
    # Umwandlung für eine hübsche Tabelle
    device_data = []
    for d in devices_objects:
        device_data.append({
            "Gerätename": d.device_name,
            "Verantwortlicher": d.managed_by_user_id,
            "Status": "✅ Aktiv" if d.is_active else "❌ Inaktiv"
        })
    
    st.table(device_data)

elif page == "Gerät bearbeiten":
    st.header("Gerätedaten anpassen")
    
    if all_device_names:
        selected_name = st.selectbox("Wählen Sie ein Gerät aus:", all_device_names)
        loaded_device = Device.find_by_attribute("device_name", selected_name)
        
        if loaded_device:
            with st.form("edit_form"):
                st.info(f"Bearbeite: {loaded_device.device_name}")
                new_user = st.text_input("Verantwortlicher (E-Mail)", value=loaded_device.managed_by_user_id)
                
                submitted = st.form_submit_button("Änderungen speichern")
                if submitted:
                    loaded_device.set_managed_by_user_id(new_user)
                    loaded_device.store_data()
                    st.success("Daten erfolgreich aktualisiert!")
    else:
        st.warning("Keine Geräte in der Datenbank gefunden.")

elif page == "Neues Gerät anlegen":
    st.header("Neuzugang registrieren")
    
    with st.form("add_form"):
        new_name = st.text_input("Name des Geräts (z.B. 3D-Drucker 01)")
        new_manager = st.text_input("Verantwortlicher (E-Mail)")
        
        add_submitted = st.form_submit_button("Gerät registrieren")
        if add_submitted:
            if new_name and new_manager:
                new_device = Device(new_name, new_manager)
                new_device.store_data()
                st.success(f"Gerät '{new_name}' wurde erfolgreich angelegt!")
                st.balloons()
            else:
                st.error("Bitte alle Felder ausfüllen.")
        