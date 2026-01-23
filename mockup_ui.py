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
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Neuen Nutzer anlegen")
        with st.container(border=True):
            with st.form("add_user_form", clear_on_submit=True):
                new_user_name = st.text_input("Nutzername", placeholder="z.B. Max Mustermann")
                new_user_email = st.text_input("Nutzer-Email", placeholder="z.B. max.mustermann@mci.edu")

                add_submitted = st.form_submit_button("Nutzer hinzufügen", type="primary")

                if add_submitted:
                    if not new_user_name or not new_user_email:
                        st.error("Bitte alle Felder ausfüllen.")
                    else:
                        # Prüfen, ob ID schon existiert
                        existing = User.find_by_attribute("id", new_user_email)
                        if existing:
                            st.error("Ein Nutzer mit dieser E-Mail existiert bereits.")
                        else:
                            new_user_obj = User(new_user_email, new_user_name)
                            new_user_obj.store_data()
                            st.success(f"Nutzer '{new_user_name}' wurde angelegt.")
                            st.rerun()

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

                all_devices = Device.find_all()
                managed_devices = [d.id for d in all_devices if d.managed_by_user_id == selected_user_id]
                
                if managed_devices:
                    st.warning(f"Dieser Nutzer ist verantwortlich für: {', '.join(managed_devices)}")

                st.divider()

                st.write("**Nutzer Entfernen**")
                
                if st.button("Nutzer löschen", type="secondary", key="btn_del_user"):
                    if managed_devices:
                        st.error(f"Löschen nicht möglich: Der Nutzer verwaltet noch {len(managed_devices)} Gerät(e). Bitte weise diese erst wem anders zu.")
                    else:
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


from datetime import datetime, time
from reservation_service import ReservationService
from reservations import Reservation

# Fenster 4: Reservierungssystem
with tab_reserve:
    st.header("Reservierungssystem")

    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("Neue Reservierung")
        with st.container(border=True):

            users = User.find_all()
            devices = Device.find_all()

            if not users or not devices:
                st.error("Bitte zuerst Nutzer und Geräte anlegen!")
            else:
                with st.form("new_reservation_form", clear_on_submit=True):

                    user_id = st.selectbox(
                        "Nutzer",
                        options=[u.id for u in users],
                        format_func=lambda x: next((f"{u.name}" for u in users if u.id == x), x)
                    )
                    
                    device_id = st.selectbox(
                        "Gerät",
                        options=[d.id for d in devices]
                    )

                    st.write("**Zeitraum wählen:**")

                    c_start_d, c_start_t = st.columns(2)
                    start_d = c_start_d.date_input("Start-Datum", value=datetime.today())
                    start_t = c_start_t.time_input("Start-Zeit", value=time(9, 0))

                    c_end_d, c_end_t = st.columns(2)
                    end_d = c_end_d.date_input("End-Datum", value=datetime.today())
                    end_t = c_end_t.time_input("End-Zeit", value=time(17, 0))

                    submitted = st.form_submit_button("Reservieren", type="primary")

                    if submitted:
                        start_dt = datetime.combine(start_d, start_t)
                        end_dt = datetime.combine(end_d, end_t)

                        if start_dt >= end_dt:
                            st.error("Fehler: Das Ende muss nach dem Start liegen.")
                        else:
                            try:
                                ReservationService.create_reservation(user_id, device_id, start_dt, end_dt)
                                st.success(f"Reservierung für {device_id} erfolgreich!")
                                st.rerun()
                            except ValueError as e:
                                st.error(f"Nicht möglich: {e}")

    with col2:
        st.subheader("Aktuelle Reservierungen")
        
        srv = ReservationService() 
        all_reservations = srv.find_all_reservations()

        if not all_reservations:
            st.info("Aktuell keine Reservierungen vorhanden.")
        else:
            res_data = []
            for r in all_reservations:
                u_name = next((u.name for u in users if u.id == r.user_id), r.user_id)
                res_data.append({
                    "Gerät": r.device_id,
                    "Nutzer": u_name,
                    "Von": r.start_date,
                    "Bis": r.end_date,
                    "ID": r.id
                })
            
            df_res = pd.DataFrame(res_data)
            st.dataframe(
                df_res, 
                use_container_width=True, 
                hide_index=True,
                column_config={
                    "Von": st.column_config.DatetimeColumn(format="D.M.Y HH:mm"),
                    "Bis": st.column_config.DatetimeColumn(format="D.M.Y HH:mm"),
                }
            )

            st.divider()
            st.write("**Reservierung stornieren**")
            
            col_del_sel, col_del_btn = st.columns([3, 1])
            
            with col_del_sel:
                delete_options = {r.id: f"{r.device_id} | {r.user_id} | {r.start_date}" for r in all_reservations}
                
                selected_res_id = st.selectbox(
                    "Welche Reservierung entfernen?",
                    options=list(delete_options.keys()),
                    format_func=lambda x: delete_options[x],
                    label_visibility="collapsed"
                )

            with col_del_btn:
                if st.button("Stornieren", type="secondary"):
                    res_to_delete = Reservation.find_by_attribute("id", selected_res_id)
                    if res_to_delete:
                        res_to_delete.delete()
                        st.success("Gelöscht.")
                        st.rerun()
                    else:
                        st.error("Fehler: Reservierung nicht gefunden.")


# Fenster 5: Wartungssystem
with tab_maintenance:
    st.header("Wartungssystem")
    st.info("Diese Funktionalität wird in zukünftigen Versionen implementiert.")