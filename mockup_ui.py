import streamlit as st
import pandas as pd
from queries import find_devices
from devices import Device

st.set_page_config(page_title="Gerätemanagement", layout="wide")

st.write("# Gerätemanagement Müller/Vogel")

tab_overview, tab_edit = st.tabs(["Übersicht", "Verwaltung"])

# Fenster 1
with tab_overview:
    st.header("Aktuelle Geräteliste")
    all_devices = Device.find_all()
    
    if not all_devices:
        st.info("Es sind aktuell keine Geräte in der Datenbank.")
    else:
        data = [
            {
                "Gerätename": device.device_name, 
                "Verantwortlicher": device.managed_by_user_id,
                "Status": "Aktiv" if device.is_active else "Inaktiv"
            }
            for device in all_devices
        ]

        df = pd.DataFrame(data)

        st.dataframe(
            df, 
            width="stretch", 
            hide_index=True
        )

# Fenster 2
with tab_edit:
    col1, col2 = st.columns(2)
    
    # col1: Neues Gerät anlegen
    with col1:
        st.subheader("Neues Gerät anlegen")
        with st.container(border=True): 
            with st.form("add_device_form"):
                new_device_name = st.text_input(
                    "Gerätename", 
                    placeholder="z.B. iPhone 15 Pro Max 3000"
                )
                new_device_manager = st.text_input(
                    "Geräte-Verantwortlicher (E-Mail)", 
                    placeholder="Max.Mustermann@maexchen.com"
                )

                add_submitted = st.form_submit_button("Gerät hinzufügen", type="primary")

                if add_submitted:
                    if not new_device_name or not new_device_manager:
                        st.error("Bitte alle Felder ausfüllen.")
                    else:
                        existing = Device.find_by_attribute("device_name", new_device_name)
                        if existing:
                            st.error("Dieses Gerät existiert bereits.")
                        else:
                            new_device = Device(new_device_name, new_device_manager)
                            new_device.store_data()
                            st.success(f"Gerät '{new_device_name}' wurde angelegt.")
                            st.rerun()

    # col2: Bestehendes Gerät bearbeiten/löschen
    with col2:
        st.subheader("Gerät bearbeiten")
        with st.container(border=True): 
            
            devices_in_db = find_devices()
            if not devices_in_db:
                st.info("Keine Geräte zum Bearbeiten vorhanden.")
            else:
                current_device_name = st.selectbox(
                    "Gerät auswählen",
                    options=devices_in_db,
                    key="sbDevice"
                )

                loaded_device = Device.find_by_attribute("device_name", current_device_name)
                
                if loaded_device:
                    st.caption(f"Bearbeite: {loaded_device.device_name}")

                    # Geräte bearbeiten
                    with st.form("edit_device_form"):
                        text_input_val = st.text_input(
                            "Verantwortlichen ändern",
                            value=loaded_device.managed_by_user_id
                        )

                        save_submitted = st.form_submit_button("Änderungen speichern")

                        if save_submitted:
                            loaded_device.set_managed_by_user_id(text_input_val)
                            loaded_device.store_data()
                            st.success("Änderungen gespeichert.")
                            st.rerun()
                    
                    # Gerät löschen
                    st.divider()
                    st.write("**Geräte Entfernen**")
                    
                    confirm_key = f"confirm_delete_{loaded_device.device_name}"
                    
                    # Button löschen
                    if st.button("Gerät löschen", type="secondary", key=f"btn_del_{loaded_device.device_name}"):
                        st.session_state[confirm_key] = True
                        st.rerun()

                    # Wenn Löschen -> Bestätigung
                    if st.session_state.get(confirm_key):
                        st.warning(f"Möchten Sie '{loaded_device.device_name}' wirklich endgültig löschen?")
                        
                        # wirklich löschen
                        col_conf1, col_conf2 = st.columns(2)
                        with col_conf1:
                            if st.button("Ja, löschen", type="primary", key="yes_del"):
                                # Gerät entgültig löschen
                                loaded_device.delete()
                                st.success("Gerät wurde gelöscht.")
                                # State wieder entfernen
                                del st.session_state[confirm_key]
                                st.rerun()

                        # Dochnicht löschen       
                        with col_conf2:
                            if st.button("Abbrechen", key="no_del"):
                                del st.session_state[confirm_key]
                                st.rerun()