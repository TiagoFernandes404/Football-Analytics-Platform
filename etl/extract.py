import time
import logging
import requests
from config.settings import API_KEY, RATE_LIMIT_DELAY, MAX_RETRIES


logger = logging.getLogger(__name__)

headers = {"X-Auth-Token": API_KEY}
BASE_URL = "https://api.football-data.org/v4/"

def fetch_with_retry(url, max_retries=MAX_RETRIES):
    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            logger.info(f"Success | URL: {url}")
            time.sleep(RATE_LIMIT_DELAY)
            return response.json()
            
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP error: {e} | URL: {url}")
        except requests.exceptions.ConnectionError:
            logger.error(f"No wifi connection | URL: {url}")
        except requests.exceptions.Timeout:
            logger.error(f"Timeout | URL: {url}")
        except requests.exceptions.JSONDecodeError:
            logger.error(f"Answer is not a valid JSON | URL: {url}")
            
        if attempt < max_retries - 1:
            logger.info(f"Retrying in 10 sec...")
            time.sleep(10)
    
    logger.error(f"Failed after {max_retries} attempts | URL: {url}")
    return None

# created a fuction that works as a tester or error detector, like this i can be aware of what is happening within the api comms 
# so is easiar to fix a probl because we know were it is 


def fetch_areas():
    url = f"{BASE_URL}areas/"
    return fetch_with_retry(url)

def fetch_competitions():
    url = f"{BASE_URL}competitions/"
    return fetch_with_retry(url)

def fetch_teams(competition_id):
    url = f"{BASE_URL}competitions/{competition_id}/teams"
    return fetch_with_retry(url)

def fetch_topscorers(competition_id):
    url = f"{BASE_URL}competitions/{competition_id}/scorers"
    return fetch_with_retry(url)

def fetch_standings(competition_id):
    url = f"{BASE_URL}competitions/{competition_id}/standings"
    return fetch_with_retry(url)

def fetch_matches(competition_id):
    url = f"{BASE_URL}competitions/{competition_id}/matches"
    return fetch_with_retry(url)

def fetch_persons(person_id):
    url = f"{BASE_URL}persons/{person_id}"
    return fetch_with_retry(url)

# we go and get all the things from the api some dont need to have a unique like a person because they are include in
# the other ones, we go and get person because when it is in teams we dont have all the info for the DB