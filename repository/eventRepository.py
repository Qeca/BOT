import requests
import json
from model.Event import Event


def getEvents():
    url = "http://localhost:8080/api/v1/all/events"
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("GET", url, headers=headers)
    loads = response.json()
    finalLoads = []
    for i in loads:
        event = Event(**i)
        finalLoads.append(event)
    return finalLoads

def getEventById(eventId: int) -> Event:
    url = f"http://localhost:8080/api/v1/all/events/{eventId}"
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("GET", url, headers=headers)
    loads = response.json()
    loads['students'] = []
    contest = Event(**loads)
    return contest

#print(getEventById(3))

def linkStudent(eventId: int, studentId: str):
    url = f"http://localhost:8080/api/v1/all/events/{eventId}/{studentId}"
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers)
    print(response.json())

# print(linkStudent("384467654"))

def getEventsByStudent(studentId: str) -> Event:
    url = f"http://localhost:8080/api/v1/all/events/byStudent/{studentId}"
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("GET", url, headers=headers)
    loads = response.json()
    finalLoads = []
    # for i in loads:
    #     finalLoads.append(i["name"])
    # finalLoads.append("Хакатон Время IT")
    print(loads[0]['name'])
    return loads

# print(getEventsByStudent("384467654"))

def getEventByTag(tag: str) -> Event:
    url = f"http://localhost:8080/api/v1/all/events/byTag?tag={tag}"
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("GET", url, headers=headers)
    loads = response.json()
    finalLoads = []
    for i in loads:
        i['students'] = []
        event = Event(**i)
        finalLoads.append(event)
    return finalLoads

#print(getEventByTag('Soft Skills'))

def getNotAppliedEvents() -> Event:
    url = "http://localhost:8080/api/v1/all/events/withStatus"
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("GET", url, headers=headers)
    loads = response.json()
    finalLoads = []
    for i in loads:
        event = Event(**i)
        finalLoads.append(event)
    return finalLoads

#print(getNotAppliedEvents())

def addEvent(event: Event):
    url = "http://localhost:8080/api/v1/all/addEvent"
    headers = {
        'Content-type': 'application/json', 'Accept': 'application/json'
    }
    response = requests.post(url, data=json.dumps(event.__dict__), headers=headers)
    return True

#print(addEvent(Event(None, "222", "ANAL", "342", "ANAL", "111", "ANAL", "412", "ANAL", "412", "ANAL", "ANAL", [])))

def linkEventToUser(eventId: str, userId: str):
    url = f"http://localhost:8080/api/v1/all/events/{eventId}/{userId}"
    headers = {
        'Content-type': 'application/json', 'Accept': 'application/json'
    }
    response = requests.post(url, data={}, headers=headers)
    loads = response.json()
    return loads

#print(linkEventToUser("1", "860077602"))
