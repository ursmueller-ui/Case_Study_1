class Device:
    counter = 0  # Klassenattribut für die Anzahl der Instanzen

    def __init__(self, name, farbe):
        self.name = name
        self.farbe = farbe
        Device.counter += 1  # Erhöhe den Zähler bei jeder Instanzerstellung

    @classmethod
    def von_typ(cls, typ):  # Alternativer Konstruktor
        if typ == "Laptop":
            return cls("Standard-Laptop", "Silber")
        elif typ == "Tablet":
            return cls("Standard-Tablet", "Schwarz")
        else:
            return cls("Unbekanntes Gerät", "Weiß")

# Test
device1 = Device.von_typ("Laptop")
print(device1.name, device1.farbe)  # Ausgabe: "Standard-Laptop Silber"

device2 = Device.von_typ("Tablet")
print(device2.name, device2.farbe)  # Ausgabe: "Standard-Tablet Schwarz"

device3 = Device.von_typ("Kamera")
print(device3.name, device3.farbe)  # Ausgabe: "Unbekanntes Gerät Weiß"

print("Erstellte Geräte:", Device.counter)  # Ausgabe: 3
