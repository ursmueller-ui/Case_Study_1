import streamlit as st
from queries import find_devices
from devices import Device

st.write("# Gerätemanagement Müller/Vogel")

# Gerät hinzufügen
st.write("## Neues Gerät hinzufügen")

with st.form("add_device_form"):
    new_device_name = st.text_input("Gerätename")
    new_device_manager = st.text_input("Geräte-Verantwortlicher (E-Mail)")

    add_submitted = st.form_submit_button("Gerät hinzufügen")

    if add_submitted:
        if not new_device_name or not new_device_manager:
            st.error("Bitte alle Felder ausfüllen.")
        else:
            # Prüfen ob Gerät bereits existiert
            existing = Device.find_by_attribute("device_name", new_device_name)
            if existing:
                st.error("Dieses Gerät existiert bereits.")
            else:
                new_device = Device(new_device_name, new_device_manager)
                new_device.store_data()
                st.session_state.new_device_name = "Neuer Gerätename"
                st.session_state.new_device_manager = "Neuer Verantwortlicher"

                st.success(f"Gerät '{new_device_name}' wurde angelegt.")
                st.rerun()

st.divider()


st.write("## Geräteauswahl")

devices_in_db = find_devices()

if not devices_in_db:
    st.info("Noch keine Geräte vorhanden.")
    st.stop()

# Gerät mit einer Selectbox auswählen
current_device_name = st.selectbox(
    "Gerät auswählen",
    options=devices_in_db,
    key="sbDevice"
)

loaded_device = Device.find_by_attribute("device_name", current_device_name)

if not loaded_device:
    st.error("Device not found in the database.")
    st.stop()

st.write(f"**Aktuelles Gerät:** {loaded_device.device_name}")

#Geräte ändern
with st.form("edit_device_form"):
    text_input_val = st.text_input(
        "Geräte-Verantwortlicher",
        value=loaded_device.managed_by_user_id
    )

    save_submitted = st.form_submit_button("Änderungen speichern")

    if save_submitted:
        loaded_device.set_managed_by_user_id(text_input_val)
        loaded_device.store_data()
        st.success("Änderungen gespeichert.")
        st.rerun()

confirm_delete = st.checkbox(
    "Ich bestätige, dass dieses Gerät dauerhaft gelöscht werden soll."
)

if st.button("🗑️ Gerät löschen", disabled=not confirm_delete):
    loaded_device.delete()  # ← deine Delete-Methode
    st.success("Gerät wurde gelöscht.")
    st.rerun()

#with st.expander("Session State"):
    #st.write(st.session_state)
