import os

#from users import User

from tinydb import TinyDB, Query
from serializer import serializer
from devices import Device
from datetime import datetime

# A class that represents a reservation focused on the data
class Reservation():
    
    def __init__(self, name : str, start_date : datetime, end_date : datetime):
        self.name = name
        self.start_date = start_date
        self.end_date = end_date

    def to_dict(self):
        return self.__dict__
    
    def __str__(self):
        return f'Reservation {self.name} ({self.start_date} - {self.end_date})'
    
    def __repr__(self):
        return self.__str__()

# A class that helps in handling reservations based on the business logic
class ReservationService():
    def validate_reservation(self, reservation: Reservation) -> bool:
        return reservation.start_date < reservation.end_date

    def check_overlap(self, res1: Reservation, res2: Reservation) -> bool:
        return not (res1.end_date <= res2.start_date or res1.start_date >= res2.end_date)
    
class DeviceAggregate(Device):
    # Class variable that is shared between all instances of the class
    db_connector = TinyDB(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database.json'), storage=serializer).table('devices_with_subclass')

    # Constructor
    def __init__(self, device_name : str, managed_by_user_id : str, reservation : Reservation):
        super().__init__(device_name, managed_by_user_id)
        self.reservation = reservation

    def to_dict(self):
        device_dict = self.__dict__.copy()
        if isinstance(self.reservation, Reservation):
            device_dict['reservation'] = self.reservation.to_dict()
        return device_dict

    def store_data(self):
        print("Storing data...")
        # Check if the device already exists in the database
        DeviceQuery = Query()
        result = self.db_connector.search(DeviceQuery.device_name == self.device_name)


        if result:
            # Update the existing record with the current instance's data
            result = self.db_connector.update(self.to_dict(), doc_ids=[result[0].doc_id])
            print("Data updated.")
        else:
            # If the device doesn't exist, insert a new record
            self.db_connector.insert(self.to_dict())
            print("Data inserted.")
            

if __name__ == "__main__":
    # Create a device
    date1 = datetime.strptime("2021-01-01", "%Y-%m-%d")
    date2 = datetime.strptime("2021-01-02", "%Y-%m-%d")
    
    res1 = Reservation("res1", date1, date2)
    res_ser_1 = ReservationService()
    print("Is Reservation valid: ", res_ser_1.validate_reservation(res1))
    print("Is Reservation overlapping: ", res_ser_1.check_overlap(res1, res1))


    device1 = DeviceAggregate("Device1", "one@mci.edu",res1)
    print(res1.__dict__)
    device1.store_data()
    # Load the device from the database
    DeviceQuery = Query()
    result = device1.db_connector.search(DeviceQuery.device_name == "Device1")
    # make it an object
    result = DeviceAggregate(result[0]['device_name'], result[0]['managed_by_user_id'], Reservation(result[0]['reservation']['name'], result[0]['reservation']['start_date'], result[0]['reservation']['end_date']))
    print(result)
    print(result.reservation)


    