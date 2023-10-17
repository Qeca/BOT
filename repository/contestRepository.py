import requests
import json
from model.Contest import Contest

def getContests():
    url = "http://localhost:8080/api/v1/all/contests"
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("GET", url, headers=headers)
    loads = response.json()
    finalLoads = []
    for i in loads:
        contest = Contest(**i)
        finalLoads.append(contest)
    return finalLoads

def getContestById(contestId: int) -> Contest:
    url = f"http://localhost:8080/api/v1/all/contests/{contestId}"
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("GET", url, headers=headers)
    loads = response.json()
    loads['students'] = []
    contest = Contest(**loads)
    return contest

#print(getContestById(6))

def getNotAppliedContests() -> Contest:
    url = "http://localhost:8080/api/v1/all/contests/withStatus"
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("GET", url, headers=headers)
    loads = response.json()
    finalLoads = []
    for i in loads:
        contest = Contest(**i)
        finalLoads.append(contest)
    return finalLoads

#print(getNotAppliedContests())

def addContest(contest: Contest):
    url = "http://localhost:8080/api/v1/all/addContest"
    headers = {
        'Content-type': 'application/json', 'Accept': 'application/json'
    }
    response = requests.post(url, data=json.dumps(contest.__dict__), headers=headers)
    return True

def applyContest(id: 'str'):
    url = f"http://localhost:8080/api/v1/all/contest/{id}/apply"
    headers = {
        'Content-type': 'application/json', 'Accept': 'application/json'
    }
    response = requests.post(url, data=json.dumps([]), headers=headers)
    return True

print(applyContest('18'))

#print(addContest(Contest(None, "111", "ANAL", "ANAL", "ANAL", "ANAL", "ANAL", "ANAL", "ANAL", "ANAL", "ANAL", "ANAL", [])))
