from serializable import Serializable
from database import DatabaseConnector
from datetime import datetime
from typing import Self

class Maintenance(Serializable):
    
    # Eigene Tabelle in der Datenbank
    db_connector = DatabaseConnector().get_table("maintenances")

    def __init__(self, device_id: str, maintenance_date: datetime, cost: float, note: str, 
                 creation_date: datetime = None, last_update: datetime = None, id: str = None) -> None:
        
        # ID generieren, falls nicht vorhanden
        if not id:
            id = f"{device_id}_{maintenance_date}_{cost}"

        super().__init__(id, creation_date, last_update)
        self.device_id = device_id
        self.maintenance_date = maintenance_date
        self.cost = float(cost) # Sicherstellen, dass es eine Zahl ist
        self.note = note

    @classmethod
    def instantiate_from_dict(cls, data: dict) -> Self:
        return cls(data['device_id'], data['maintenance_date'], data['cost'], data['note'], 
                   data['creation_date'], data['last_update'], data['id'])

    def __str__(self):
        return f"Wartung: {self.device_id} am {self.maintenance_date} ({self.cost}€)"