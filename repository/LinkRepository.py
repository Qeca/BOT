import requests
import json
from model.Vehicle import Vehicle
from model.VehicleAdd import VehicleAdd

def linkVehicleAndDriver(vehicleId:str, driverId:str):
    url = f"http://localhost:8080/api/v1/vehicles/linkDriver?driverId={driverId}&vehicleId={vehicleId}"
    headers = {
        'Content-type': 'application/json', 'Accept': 'application/json'
    }
    response = requests.request("POST", url, headers=headers)
    return True


#deleteVehicle('4444')
#getVehiclesByCompany("1a7ee719-571f-4f86-84e8-8bfda8dc8363")
print(linkVehicleAndDriver('4231', '4325'))