import streamlit as st
import pandas as pd
from devices_inheritance import Device
from users_inheritance import User

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
                new_device_manager = st.selectbox(
                    "Verantwortlicher Nutzer", 
                    options=[user.id for user in User.find_all()],
                    key="sbManager"
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
    
    # Layout wie bei Geräteverwaltung: 2 Spalten
    col1, col2 = st.columns(2)

    # ---------------------------------------------------------
    # SPALTE 1: Neuen Nutzer anlegen
    # ---------------------------------------------------------
    with col1:
        st.subheader("Neuen Nutzer anlegen")
        with st.container(border=True):
            # HIER IST DIE ÄNDERUNG: clear_on_submit=True
            with st.form("add_user_form", clear_on_submit=True):
                new_user_name = st.text_input("Nutzername", placeholder="z.B. Max Mustermann")
                new_user_email = st.text_input("Nutzer-Email", placeholder="z.B. max.mustermann@mci.edu")

                add_submitted = st.form_submit_button("Nutzer hinzufügen", type="primary")

                if add_submitted:
                    if not new_user_name or not new_user_email:
                        st.error("Bitte alle Felder ausfüllen.")
                    else:
                        # Prüfen, ob ID (Email) schon existiert
                        existing = User.find_by_attribute("id", new_user_email)
                        if existing:
                            st.error("Ein Nutzer mit dieser E-Mail existiert bereits.")
                        else:
                            new_user_obj = User(new_user_email, new_user_name)
                            new_user_obj.store_data()
                            st.success(f"Nutzer '{new_user_name}' wurde angelegt.")
                            # st.rerun() ist hier optional, da clear_on_submit das Formular eh leert,
                            # aber st.rerun() aktualisiert sofort die Listen in der rechten Spalte.
                            st.rerun()

    # ---------------------------------------------------------
    # SPALTE 2: Nutzer verwalten & Löschen
    # ---------------------------------------------------------
    with col2:
        st.subheader("Nutzer verwalten")
        
        all_users = User.find_all()
        
        with st.container(border=True):
            if not all_users:
                st.info("Keine Nutzer vorhanden.")
            else:
                # Auswahlbox für den Nutzer
                selected_user_id = st.selectbox(
                    "Nutzer auswählen",
                    options=[u.id for u in all_users],
                    format_func=lambda x: next((f"{u.name} ({u.id})" for u in all_users if u.id == x), x),
                    key="sb_user_manage"
                )

                # --- NEU: Verantwortlichkeiten anzeigen ---
                # Wir suchen alle Geräte, bei denen dieser Nutzer eingetragen ist
                all_devices = Device.find_all()
                managed_devices = [d.id for d in all_devices if d.managed_by_user_id == selected_user_id]
                
                if managed_devices:
                    st.warning(f"Dieser Nutzer ist verantwortlich für: {', '.join(managed_devices)}")


                st.divider()

                # Lösch-Logik
                st.write("**Nutzer Entfernen**")
                
                # Button deaktivieren oder Warnung anzeigen ist Geschmackssache. 
                # Hier lassen wir ihn klickbar, fangen aber den Fehler ab (sicherer).
                if st.button("Nutzer löschen", type="secondary", key="btn_del_user"):
                    if managed_devices:
                        st.error(f"Löschen nicht möglich: Der Nutzer verwaltet noch {len(managed_devices)} Gerät(e). Bitte weise diese erst wem anders zu.")
                    else:
                        # Löschen durchführen
                        user_to_delete = User.find_by_attribute("id", selected_user_id)
                        if user_to_delete:
                            user_to_delete.delete()
                            st.success(f"Nutzer {selected_user_id} wurde gelöscht.")
                            st.rerun()

    st.divider()
    with st.container(border=True):
        st.subheader("Alle Nutzer in der Datenbank")
        if all_users:
            user_data = [{"Name": u.name, "Email (ID)": u.id} for u in all_users]
            st.dataframe(pd.DataFrame(user_data), use_container_width=True, hide_index=True)
        else:
            st.write("Keine Daten.")



# Fenster 4: Gerät reservieren und Warteschlange
with tab_reserve:
    st.header("Gerät reservieren & Warteschlange")
    
    devices_in_db = [device.id for device in Device.find_all()]
    
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
                
                device_obj = Device.find_by_attribute("id", selected_dev_name)
                
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