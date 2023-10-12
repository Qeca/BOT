import requests
import json

def getCode(managerId: str):
    url = f"http://localhost:8080/api/v1/invite/{managerId}/getCode"
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("GET", url, headers=headers)
    loads = response.json()
    code = loads
    return code['code']

#print(getCode("43235"))