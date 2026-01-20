import streamlit as st
import pandas as pd
from devices_inheritance import Device

st.set_page_config(page_title="Gerätemanagement", layout="wide")

st.write("# Gerätemanagement Müller/Vogel")

tab_overview, tab_edit, tab_user, tab_reserve, tab_maintenance = st.tabs(["Übersicht", "Geräte-Verwaltung","Nutzer-Verwaltung", "Reservierungssystem", "Wartungssystem"])

# Fenster 1
with tab_overview:
    st.header("Aktuelle Geräteliste")
    all_devices = Device.find_all()
    
    if not all_devices:
        st.info("Es sind aktuell keine Geräte in der Datenbank.")
    else:
        data = [
            {
                "Gerätename": device.id, 
                "Verantwortlicher": device.managed_by_user_id,
                #"Status": "Aktiv" if device.is_active else "Inaktiv"
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
            
            devices_in_db = [device.id for device in Device.find_all()]
            if not devices_in_db:
                st.info("Keine Geräte zum Bearbeiten vorhanden.")
            else:
                current_device_name = st.selectbox(
                    "Gerät auswählen",
                    options=devices_in_db,
                    key="sbDevice"
                )

                loaded_device = Device.find_by_attribute("id", current_device_name)
                
                if loaded_device:
                    st.caption(f"Bearbeite: {loaded_device.id}")

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
                    
                    confirm_key = f"confirm_delete_{loaded_device.id}"
                    
                    # Button löschen
                    if st.button("Gerät löschen", type="secondary", key=f"btn_del_{loaded_device.id}"):
                        st.session_state[confirm_key] = True
                        st.rerun()

                    # Wenn Löschen -> Bestätigung
                    if st.session_state.get(confirm_key):
                        st.warning(f"Möchten Sie '{loaded_device.id}' wirklich endgültig löschen?")
                        
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

# Fenster 3: Nutzer-Verwaltung
with tab_user:
    st.header("Nutzer-Verwaltung")
    st.info("Diese Funktionalität wird in zukünftigen Versionen implementiert.")

# Fenster 4: Gerät reservieren und Warteschlange
with tab_reserve:
    st.header("Gerät reservieren & Warteschlange")
    
    devices_in_db = find_devices()
    
    if not devices_in_db:
        st.info("Keine Geräte vorhanden.")
    else:
        col_res1, col_res2 = st.columns([1, 2])
        
        # col1 Reservierungen eintragen
        with col_res1:
            with st.container(border=True):
                st.subheader("Bedarf anmelden")
                
                selected_dev_name = st.selectbox(
                    "Für welches Gerät?", 
                    options=devices_in_db,
                    key="sb_reserve"
                )
                
                device_obj = Device.find_by_attribute("device_name", selected_dev_name)
                
                if not hasattr(device_obj, 'reservation_queue'):
                    device_obj.reservation_queue = []

                reserver_name = st.text_input("Ihr Name und Zeitdauer der Nutzung",
                                              key="input_res_name",
                                              placeholder="Max Mustermann 2 Tage")
                
                if st.button("In Warteschlange eintragen", type="primary"):
                    if not reserver_name:
                        st.error("Bitte einen Namen eingeben.")
                    else:
                        device_obj.reservation_queue.append(reserver_name)
                        device_obj.store_data()
                        st.success(f"{reserver_name} wurde vorgemerkt.")
                        st.rerun()
# GEHT NOCH NICHT ZUM SPEICHERN UND ABRUFEN DER WARTESCHLANGE
                
                st.divider()
                if st.button("Nächsten Benutzer abfertigen (Löschen)"):
                    if len(device_obj.reservation_queue) > 0:
                        removed_user = device_obj.reservation_queue.pop(0)
                        device_obj.store_data()
                        st.success(f"{removed_user} wurde aus der Liste entfernt.")
                        st.rerun()
                    else:
                        st.warning("Die Warteschlange ist leer.")

        # col2: Warteschlange anzeigen
        with col_res2:
            st.subheader(f"Warteschlange für: {selected_dev_name}")
            
            queue = device_obj.reservation_queue
            
            if not queue:
                st.info("Aktuell keine Reservierungen.")
            else:
                # Schöne Darstellung als nummerierte Liste
                st.write("Folgende Personen warten (Reihenfolge):")
                for i, person in enumerate(queue, 1):
                    st.markdown(f"**{i}. {person}**")

# Fenster 5: Wartungssystem
with tab_maintenance:
    st.header("Wartungssystem")
    st.info("Diese Funktionalität wird in zukünftigen Versionen implementiert.")