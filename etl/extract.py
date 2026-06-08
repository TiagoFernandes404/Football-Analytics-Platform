from config.settings import API_KEY
import requests

headers = {"X-Auth-Token": API_KEY}
BASE_URL = "https://api.football-data.org/v4/"

def fetch_areas():
    URL= f"{BASE_URL}areas/"
    response = requests.get(URL, headers=headers)
    return response.json()

def fetch_competitions():
    URL= f"{BASE_URL}competitions/"
    response = requests.get(URL, headers=headers)
    return response.json()

def fetch_teams(competition_id):
    URL = f"{BASE_URL}competitions/{competition_id}/teams"
    response = requests.get(URL, headers=headers)
    return response.json()
