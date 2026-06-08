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

def fetch_topscorers(competition_id):
    URL = f"{BASE_URL}competitions/{competition_id}/scorers"
    response = requests.get(URL, headers=headers)
    return response.json()

def fetch_standings(competition_id):
    URL = f"{BASE_URL}competitions/{competition_id}/standings"
    response = requests.get(URL, headers=headers)
    return response.json()

def fetch_matches(competition_id):
    URL = f"{BASE_URL}competitions/{competition_id}/matches"
    response = requests.get(URL, headers=headers)
    return response.json()

def fetch_person(person_id):
    URL = f"{BASE_URL}persons/{person_id}"
    response = requests.get(URL, headers=headers)
    return response.json()


# we go and get all the things from the api some dont need to have a unique like a person because they are include in
# the other ones, like persons is in teams