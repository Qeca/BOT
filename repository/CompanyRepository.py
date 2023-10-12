import requests
import json

from charset_normalizer.md import List

from model.Company import Company
from model.CompanyPost import PostCompany
from model.Driver import Driver

def getVehiclesByCompany(companyId:str) -> Company:
    url = f"http://localhost:8080/api/v1/company/{companyId}"
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("GET", url, headers=headers)
    loads = response.json()
    company = Company(**loads)
    print(company.id)
    print(company.name)
    print(company.vehicles)
    print(company.drivers)
    print(company.managers)
    # print(loads)
    return company

def getDriversByCompany(companyId: str) -> List[Driver]:
    url = f"http://localhost:8080/api/v1/company/{companyId}/getDrivers"
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("GET", url, headers=headers)
    drivers: List[Driver] = []
    loads = response.json()
    for i in loads:
        driver = Driver(**i)
        drivers.append(driver)
        print(driver.id)
        print(driver.firstname)
        print(driver.lastname)
    # print(loads)
    return drivers

def postCompany(company: PostCompany, managerId:str) -> str:
    url = f"http://localhost:8080/api/v1/company/{managerId}/add"
    headers = {
        'Content-type': 'application/json', 'Accept': 'application/json'
    }
    response = requests.post(url, data=json.dumps(company.__dict__), headers=headers)
    return True


#print(postCompany(PostCompany("ggbb"), '43235'))
# print(getDriversByCompany("1a7ee719-571f-4f86-84e8-8bfda8dc8363"))

#getVehiclesByCompany("1a7ee719-571f-4f86-84e8-8bfda8dc8363")