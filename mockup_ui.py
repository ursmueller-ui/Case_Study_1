import streamlit as st

# --- KONSTANTE ---
ADMIN_PASSWORD = "letmein"

# --- 1. Simulierte Device Klasse und Datenhaltung ---

class Device:
    """Simulierte Klasse zur Darstellung eines Geräts."""
    
    def __init__(self, device_name, managed_by_user_id, device_id):
        self.device_name = device_name
        self._managed_by_user_id = managed_by_user_id
        self.device_id = device_id

    def __str__(self):
        # Zeigt nur die Basis-Infos, nicht den Verantwortlichen im __str__
        return f"Gerät(ID: {self.device_id}, Name: {self.device_name})"

    # Getter
    @property
    def managed_by_user_id(self):
        return self._managed_by_user_id
    
    # Setter
    def set_managed_by_user_id(self, new_id):
        self._managed_by_user_id = new_id

    def store_data(self):
        """Simuliert das Speichern in der Datenbank."""
        st.session_state.device_db[self.device_name] = self
        print(f"DEBUG: Gerät '{self.device_name}' gespeichert. Neuer Verantwortlicher: {self._managed_by_user_id}")

# --- 2. Simulierte Datenbankfunktionen ---

def find_devices():
    """Simuliert das Abrufen aller Gerätenamen aus der DB."""
    return list(st.session_state.device_db.keys())

def find_device_by_name(device_name):
    """Simuliert das Laden eines spezifischen Device-Objekts."""
    return st.session_state.device_db.get(device_name)

# --- 3. Initialisiere Session State (Simulierte Datenbank & Login-Status) ---

if 'device_db' not in st.session_state:
    st.session_state.device_db = {
        "Laser Cutter X": Device("Laser Cutter X", "LeoMaus", 1),
        "3D-Drucker A": Device("3D-Drucker A", "Vollteil_Jan", 2),
        "CNC-Fräse Z": Device("CNC-Fräse Z", "Drehpeter", 3),
        "Schweißgerät": Device("Schweißgerät", "Funken_Kevin", 4),
        "Lötstation": Device("Lötstation", "Heiß_Lutz", 5),
        "Bohrmaschine B": Device("Bohrmaschine B", "Friedrich Merz", 6),
        "Bandsäge Y": Device("Bandsäge Y", "Danny Run", 7)
    }

if 'current_device_name' not in st.session_state:
    st.session_state.current_device_name = find_devices()[0] if find_devices() else None

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False 


# --- 4. Login-Funktion (Seitenleiste) ---

def show_login_sidebar():
    """Zeigt die Passwortabfrage/Logout in der Seitenleiste."""
    st.sidebar.header("Admin-Zugang 🔑")
    
    if st.session_state.logged_in:
        st.sidebar.success("Angemeldet als Administrator.")
        if st.sidebar.button("Abmelden"):
            st.session_state.logged_in = False
            st.rerun()
    else:
        with st.sidebar.form("Login_Form"):
            password = st.text_input("Passwort zur Bearbeitung", type="password")
            submitted = st.form_submit_button("Login")

            if submitted:
                if password == ADMIN_PASSWORD:
                    st.session_state.logged_in = True
                    st.success("Login erfolgreich!")
                    st.rerun()
                else:
                    st.error("Falsches Passwort.")


# --- 5. Streamlit UI Aufbau ---

st.title("⚙️ Geräteverwaltung Müller GmbH")
st.markdown("---")

# Führt die Logik und die Anzeige für den Login aus
show_login_sidebar()

devices_in_db = find_devices()

if devices_in_db:
    # 1. Selectbox zur Auswahl des Geräts
    current_device_name = st.selectbox(
        'Gerät auswählen',
        options=devices_in_db,
        key="sbDevice",
        index=devices_in_db.index(st.session_state.current_device_name) if st.session_state.current_device_name else 0 
    )

    # 2. Logik zum Laden des ausgewählten Geräts
    loaded_device = find_device_by_name(current_device_name)

    if loaded_device:
        st.header(f"Details für {loaded_device.device_name}")
        st.markdown("---")

        # --- ANZEIGE DES VERANTWORTLICHEN (IMMER SICHTBAR) ---
        st.metric("Geräte-Verantwortlicher", loaded_device.managed_by_user_id)
        
        st.markdown("---")


        # 3. Formular zur Bearbeitung - NUR SICHTBAR NACH ERFOLGREICHEM LOGIN
        if st.session_state.logged_in:
            
            with st.form("Device_Edit_Form"):
                
                st.subheader(f"Geräte-Verantwortlichen ändern")
                st.warning("Achtung: Sie bearbeiten die Daten als Administrator.")

                # Text-Input mit dem aktuellen Wert zum ÄNDERN
                text_input_val = st.text_input(
                    "Neuer Verantwortlicher", 
                    value=loaded_device.managed_by_user_id, # Aktueller Wert zur Initialisierung
                    key="input_manager_id"
                )
                
                submitted = st.form_submit_button("Änderungen speichern")
                
                if submitted:
                    # Logik beim Absenden des Formulars
                    loaded_device.set_managed_by_user_id(text_input_val) 
                    loaded_device.store_data()
                    
                    st.session_state.current_device_name = current_device_name 
                    
                    st.success("Daten erfolgreich gespeichert! Seite wird aktualisiert.")
                    st.rerun()
        else:
            # Hinweis, wenn man nicht eingeloggt ist
            st.info("Melden Sie sich über die Seitenleiste an, um den Verantwortlichen zu bearbeiten.")

    else:
        st.error("Gerät nicht in der Datenbank gefunden.")

else:
    st.warning("Keine Geräte in der simulierten Datenbank vorhanden.")