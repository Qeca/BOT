import requests
import json
from BOT.model.Achivment import Achivment

def addAchivment(userId: str, achivment: Achivment):
    url = f"http://localhost:8080/api/v1/user/student/{userId}/addAchievement"
    headers = {
        'Content-type': 'application/json', 'Accept': 'application/json'
    }
    response = requests.post(url, data=json.dumps(achivment.__dict__), headers=headers)
    return True

print(addAchivment(1, Achivment('fff', 'ffff', 'ffff', 'ffff', '1')))