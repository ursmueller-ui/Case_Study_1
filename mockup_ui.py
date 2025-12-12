import streamlit as st

# --- 1. Simulierte Device Klasse und Datenhaltung ---

class Device:
    """Simulierte Klasse zur Darstellung eines Geräts."""
    
    def __init__(self, device_name, managed_by_user_id, device_id):
        self.device_name = device_name
        self._managed_by_user_id = managed_by_user_id
        self.device_id = device_id

    def __str__(self):
        return f"Gerät(ID: {self.device_id}, Name: {self.device_name}, Verantwortlicher: {self._managed_by_user_id})"

    # Getter
    @property
    def managed_by_user_id(self):
        return self._managed_by_user_id
    
    # Setter
    def set_managed_by_user_id(self, new_id):
        self._managed_by_user_id = new_id

    def store_data(self):
        """Simuliert das Speichern in der Datenbank."""
        # Aktualisiere den Session State (die simulierte DB)
        st.session_state.device_db[self.device_name] = self
        print(f"DEBUG: Gerät '{self.device_name}' gespeichert. Neuer Verantwortlicher: {self._managed_by_user_id}")

# --- 2. Simulierte Datenbankfunktionen ---

def find_devices():
    """Simuliert das Abrufen aller Gerätenamen aus der DB."""
    return list(st.session_state.device_db.keys())

def find_device_by_name(device_name):
    """Simuliert das Laden eines spezifischen Device-Objekts."""
    return st.session_state.device_db.get(device_name)

# --- 3. Initialisiere Session State (Simulierte Datenbank) ---

if 'device_db' not in st.session_state:
    st.session_state.device_db = {
        "Laser Cutter X": Device("Laser Cutter X", "LeoMaus", 1),
        "3D-Drucker A": Device("3D-Drucker A", "Vollteil_Jan", 2),
        "CNC-Fräse Z": Device("CNC-Fräse Z", "Drehpeter", 3),
        "Schweißgerät": Device("Schweißgerät", "Funken_Kevin", 4)
    }

# Setze das Default-Gerät für die erste Auswahl
if 'current_device_name' not in st.session_state:
    st.session_state.current_device_name = find_devices()[0] if find_devices() else None

# --- 4. Streamlit UI Aufbau ---

st.title("⚙️ Geräteverwaltung (Mockup mit simuliertem CRUD)")
st.markdown("---")

devices_in_db = find_devices()

if devices_in_db:
    # 1. Selectbox zur Auswahl des Geräts
    # Die Option options=devices_in_db nutzt find_devices()
    current_device_name = st.selectbox(
        'Gerät auswählen',
        options=devices_in_db,
        key="sbDevice",
        # Setzt den Standardwert beim Start der App
        index=devices_in_db.index(st.session_state.current_device_name) if st.session_state.current_device_name else 0 
    )

    # 2. Logik zum Laden des ausgewählten Geräts
    loaded_device = find_device_by_name(current_device_name)

    if loaded_device:
        st.info(f"Loaded Device: {loaded_device}") # Nutzt die __str__ Methode
        st.markdown("---")

        # 3. Formular zur Bearbeitung
        with st.form("Device_Form"):
            
            # Zeigt den Gerätenamen (nicht editierbar im Formular)
            st.subheader(f"Gerät bearbeiten: {loaded_device.device_name}")

            # 4. Text-Input mit dem aktuellen Wert
            # Das value-Argument initialisiert das Textfeld
            text_input_val = st.text_input(
                "Geräte-Verantwortlicher", 
                value=loaded_device.managed_by_user_id
            )
            
            # Wichtig: Die Setter-Methode MUSS nach dem Ausführen des Formulars
            # aber VOR dem Speichern aufgerufen werden, um den neuen Wert zu übernehmen.
            # Da Streamlit das gesamte Skript neu ausführt, muss dies in der Submit-Logik geschehen.
            
            # 5. Submit Button
            submitted = st.form_submit_button("Änderungen speichern")
            
            if submitted:
                # 6. Logik beim Absenden des Formulars
                
                # Zuerst den neuen Wert in das Objekt schreiben
                loaded_device.set_managed_by_user_id(text_input_val) 
                
                # Dann das Objekt in der simulierten DB speichern
                loaded_device.store_data()
                
                # Speichert den aktuell ausgewählten Namen, falls dieser sich nicht ändert
                st.session_state.current_device_name = current_device_name 
                
                st.success("Daten erfolgreich gespeichert! Seite wird aktualisiert.")
                st.rerun() # Notwendig, um den aktualisierten Wert anzuzeigen

    else:
        st.error("Gerät nicht in der Datenbank gefunden.")

else:
    st.warning("Keine Geräte in der simulierten Datenbank vorhanden.")