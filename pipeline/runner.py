import logging
import os
from datetime import datetime

os.makedirs("logs", exist_ok=True)
log_filename = f"logs/pipeline_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s:%(name)s:%(message)s",
    handlers=[
        logging.FileHandler(log_filename),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# this code above works so i can register the logs of everything i run so when i leave the api running for 
# exemple overnight in the morning i can check i up
# we put it first so we dont get any problems 
from etl.extract import *
from etl.transform import *
from etl.load import *

def run_etl(fetch_func, transform_func, load_func):
    data = fetch_func()
    transformed = transform_func(data)
    load_func(transformed)

competitions_data = fetch_competitions()

# seasons are inserted without winner_id because teams don't exist yet so we skip the problem
run_etl(fetch_areas, transform_areas, load_areas)
run_etl(fetch_competitions, transform_seasons, load_seasons)
run_etl(fetch_competitions, transform_competitions, load_competitions)

for competition in competitions_data['competitions']:
    competition_code = competition['code']
    teams_data = fetch_teams(competition_code)
    load_teams(transform_teams(teams_data))
    load_teamstaff(transform_teamstaff(teams_data))
    load_coach(transform_coach(teams_data))
    load_teamcoach(transform_teamcoach(teams_data))

    # so here i make the part of the engine decision making if there is someting new to check or not 
    # so i can save time in the execution 
    for team in teams_data['teams']:
        for player in team['squad']:
            db_last_updated = get_person_last_updated(player['id'])
            api_last_updated = player.get('lastUpdated')

            if db_last_updated is None:
                # if this person doen´t have a last update it doesn't exist so i have to check to create it 
                logger.info(f"New person {player['id']} - fetching")
                person_data = fetch_persons(player['id'])
                load_persons(transform_persons(person_data))
                load_personcompetition(transform_personcompetition(person_data))
            elif api_last_updated and str(db_last_updated) != api_last_updated:
                # this person is created but i have something new in the api
                logger.info(f"Updated person {player['id']} - fetching")
                person_data = fetch_persons(player['id'])
                load_persons(transform_persons(person_data))
                load_personcompetition(transform_personcompetition(person_data))
            else:
                # this person hasn´t got new info so i skip
                logger.info(f"Skipping person {player['id']} - already up to date")

    # only after persons are inserted we can insert squad relations
    load_squadplayers(transform_squadplayers(teams_data))

for competition in competitions_data['competitions']:
    competition_code = competition['code']
    matches_data = fetch_matches(competition_code)
    load_matches(transform_matches(matches_data))
    load_referees(transform_referee(matches_data))
    load_matchreferee(transform_matchreferee(matches_data))
    scorers_data = fetch_topscorers(competition_code)
    load_scorers(transform_scorers(scorers_data))
    standings_data = fetch_standings(competition_code)
    load_standings(transform_standings(standings_data))

# now that the teams are inserted we can update the seasons with the winner
run_etl(fetch_competitions, transform_seasons_winner, load_seasons_winner)