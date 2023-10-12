import requests
import json
from model.User import User
from model.Driver import Driver
from model.Manager import Manager
from model.ResponseManager import ResponseManager
from model.ResponseDriver import ResponseDriver


def getUser(userId: str):
    url = f"http://localhost:8080/api/v1/user/{userId}"
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("GET", url, headers=headers)
    loads = response.json()
    user = User(**loads)
    return user


# print(getUser("5367"))


def addDriver(driver: Driver):
    url = "http://localhost:8080/api/v1/user/addDriver"
    headers = {
        'Content-type': 'application/json', 'Accept': 'application/json'
    }
    response = requests.post(url, data=json.dumps(driver.__dict__), headers=headers)
    loads = response.json()
    responseDriver = ResponseDriver(**loads)
    return responseDriver


# print(addDriver(Driver(73894, "Пися", "Камушкин", "3232")))

def addManager(manager: Manager) -> ResponseManager:
    url = "http://localhost:8080/api/v1/user/addManager"
    headers = {
        'Content-type': 'application/json', 'Accept': 'application/json'
    }
    response = requests.post(url, data=json.dumps(manager.__dict__), headers=headers)
    loads = response.json()
    manager = ResponseManager(**loads)
    return manager


# print(addManager(Manager(2281, "Череп", "Пашкович")))

def deleteDriver(driverId: str):
    url = f"http://localhost:8080/api/v1/user/deleteDriver/{driverId}"
    headers = {
        'Content-Type': 'application/json', 'Accept': 'application/json'
    }
    response = requests.request("DELETE", url, headers=headers)
    loads = response.json()
    responseDriver = ResponseDriver(**loads)
    return responseDriver


print(deleteDriver("9678"))

def editDriver(driver: Driver):
    url = f"http://localhost:8080/api/v1/user/editDriver/{driver.id}"
    headers = {
        'Content-Type': 'application/json', 'Accept': 'application/json'
    }
    response = requests.post(url, data=json.dumps(driver.__dict__), headers=headers)
    loads = response.json()
    responseDriver = ResponseDriver(**loads)
    return responseDriver

# print(editDriver(Driver(73894, "Сергей", "Джабан", "3232")))
