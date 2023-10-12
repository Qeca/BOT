import requests
import json
from model.Vehicle import Vehicle
from model.VehicleAdd import VehicleAdd

def getVehiclesByCompany(companyId:str) -> Vehicle:
    url = f"http://localhost:8080/api/v1/vehicles/byCompany/{companyId}"
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("GET", url, headers=headers)
    loads = response.json()
    for i in loads:
        vehicles = Vehicle(**i)
        print(vehicles.transportNumber)
        print(vehicles.mark)
        print(vehicles.model)
        print(vehicles.driverId)
    # print(loads)
    return vehicles

def deleteVehicle(vehicleId:str):
    url = f"http://localhost:8080/api/v1/vehicles/delete/{vehicleId}"
    headers = {
        'Content-type': 'application/json', 'Accept': 'application/json'
    }
    response = requests.request("POST", url, headers=headers)
    return True

def postVehicle(newVehicle: VehicleAdd) -> bool:
    url = f"http://localhost:8080/api/v1/vehicles/add"
    headers = {
        'Content-type': 'application/json', 'Accept': 'application/json'
    }
    response = requests.post(url, data=json.dumps(newVehicle.__dict__), headers=headers)
    return True

#deleteVehicle('4444')
#getVehiclesByCompany("1a7ee719-571f-4f86-84e8-8bfda8dc8363")
print(postVehicle(VehicleAdd("new", "news", "new new", 55)))