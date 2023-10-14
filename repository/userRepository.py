import requests
import json
from model.Student import Student
from model.Admin import Admin

def getStudents():
    url = "http://localhost:8080/api/v1/user/students"
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("GET", url, headers=headers)
    loads = response.json()
    finalLoads = []
    for i in loads:
        student = Student(**i)
        finalLoads.append(student)
    return finalLoads

#print(getStudents())

def getStudent(userId: str) -> Student:
    url = f"http://localhost:8080/api/v1/user/students/{userId}"
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("GET", url, headers=headers)
    loads = response.json()
    student = Student(**loads)
    return student

#print(getStudent("2222"))

def addStudent(student:Student):
    url = "http://localhost:8080/api/v1/user/addStudent"
    headers = {
        'Content-type': 'application/json', 'Accept': 'application/json'
    }
    response = requests.post(url, data=json.dumps(student.__dict__), headers=headers)
    return True

#print(addStudent(Student("3333", "333", "Bogdan",  "Chirik","Anat","4219",[], [])))

def addAdmin(admin:Admin):
    url = "http://localhost:8080/api/v1/user/addAdmin"
    headers = {
        'Content-type': 'application/json', 'Accept': 'application/json'
    }
    response = requests.post(url, data=json.dumps(admin.__dict__), headers=headers)
    return True

#print(addAdmin(Admin("1111", "111", "Yulia", "Antoxina", "Vycheslavovna")))




