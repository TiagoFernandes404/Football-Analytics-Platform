from database.connection import engine
from sqlalchemy import text
import logging

logger = logging.getLogger(__name__)


# lets create a simple fuc to serve as a teste in all load fuction so we dont code the same thing over and over again
def load_to_db(data, query, func_name):
    if not data:
        logger.warning(f"{func_name} | No data to load")
        return

    with engine.connect() as conn:
        try:
            conn.execute(text("SET CONSTRAINTS ALL DEFERRED"))
            conn.execute(query, data)
            conn.commit()
            logger.info(f"{func_name}  | {len(data)} records loaded")
        except Exception as e:
            conn.rollback()
            logger.error(f"{func_name}  | Error: {e}")

# because we created the load_to_db now we just have to write the INSERT script
# we use ON CONFLICT because imagine the case we have the same id came twice we could ignore or rewrite
# in my opinion the right mode is to rewrite because it can be updated data

def load_areas(data):
    query = text("""INSERT INTO area(id,name,code,flag,parentArea_id)
                 VALUES(:id, :name, :code, :flag, :parentArea_id)
                 ON CONFLICT (id) DO UPDATE SET
                    name=EXCLUDED.name,
                    code = EXCLUDED.code,
                    flag = EXCLUDED.flag,
                    parentArea_id = EXCLUDED.parentArea_id
    """)
    load_to_db(data,query,"load_areas")

def load_teams(data):
    query = text("""INSERT INTO team(id,area_id,name,shortName,tla,crest,address,website,founded,clubColors,venue,lastUpdated)
                 VALUES(:id,:area_id,:name,:shortName,:tla,:crest,:address,:website,:founded,:clubColors,:venue,:lastUpdated)
                 ON CONFLICT (id) DO UPDATE SET
                    area_id = EXCLUDED.area_id,
                    name=EXCLUDED.name,
                    shortName=EXCLUDED.shortName,
                    tla=EXCLUDED.tla,
                    crest=EXCLUDED.crest,
                    address=EXCLUDED.address,
                    website=EXCLUDED.website,
                    founded=EXCLUDED.founded,
                    clubColors=EXCLUDED.clubColors,
                    venue=EXCLUDED.venue,
                    lastUpdated=EXCLUDED.lastUpdated
    """)
    load_to_db(data,query,"load_teams")

def load_persons(data):
    query = text("""
        INSERT INTO person (id, name, firstName, lastName, dateOfBirth, nationality, section, position, shirtNumber, lastUpdated, contractStart, contractUntil)
        VALUES (:id, :name, :firstName, :lastName, :dateOfBirth, :nationality, :section, :position, :shirtNumber, :lastUpdated, :contractStart, :contractUntil)
        ON CONFLICT (id) DO UPDATE SET
            name = EXCLUDED.name,
            firstName = EXCLUDED.firstName,
            lastName = EXCLUDED.lastName,
            dateOfBirth = EXCLUDED.dateOfBirth,
            nationality = EXCLUDED.nationality,
            section = EXCLUDED.section,
            position = EXCLUDED.position,
            shirtNumber = EXCLUDED.shirtNumber,
            lastUpdated = EXCLUDED.lastUpdated,
            contractStart = EXCLUDED.contractStart,
            contractUntil = EXCLUDED.contractUntil
    """)
    load_to_db(data, query, "load_persons")


def load_seasons(data):
    query = text("""
        INSERT INTO season (id, startDate, endDate, currentMatchday, winner_id)
        VALUES (:id, :startDate, :endDate, :currentMatchday, :winner_id)
        ON CONFLICT (id) DO UPDATE SET
            startDate = EXCLUDED.startDate,
            endDate = EXCLUDED.endDate,
            currentMatchday = EXCLUDED.currentMatchday,
            winner_id = EXCLUDED.winner_id
    """)
    load_to_db(data, query, "load_seasons")


def load_competitions(data):
    query = text("""
        INSERT INTO competition (id, area_id, name, code, type, emblem, plan, currentSeason, numberOfAvailableSeasons, lastUpdated)
        VALUES (:id, :area_id, :name, :code, :type, :emblem, :plan, :currentSeason, :numberOfAvailableSeasons, :lastUpdated)
        ON CONFLICT (id) DO UPDATE SET
            area_id = EXCLUDED.area_id,
            name = EXCLUDED.name,
            code = EXCLUDED.code,
            type = EXCLUDED.type,
            emblem = EXCLUDED.emblem,
            plan = EXCLUDED.plan,
            currentSeason = EXCLUDED.currentSeason,
            numberOfAvailableSeasons = EXCLUDED.numberOfAvailableSeasons,
            lastUpdated = EXCLUDED.lastUpdated
    """)
    load_to_db(data, query, "load_competitions")


def load_matches(data):
    query = text("""
        INSERT INTO match (id, area_id, competition_id, season_id, utcDate, status, matchday, stage, match_group, lastUpdated, homeTeam, awayTeam, scoreWinner, scoreDuration, scoreFullTime, scoreHalfTime)
        VALUES (:id, :area_id, :competition_id, :season_id, :utcDate, :status, :matchday, :stage, :match_group, :lastUpdated, :homeTeam, :awayTeam, :scoreWinner, :scoreDuration, :scoreFullTime, :scoreHalfTime)
        ON CONFLICT (id) DO UPDATE SET
            status = EXCLUDED.status,
            matchday = EXCLUDED.matchday,
            lastUpdated = EXCLUDED.lastUpdated,
            scoreWinner = EXCLUDED.scoreWinner,
            scoreDuration = EXCLUDED.scoreDuration,
            scoreFullTime = EXCLUDED.scoreFullTime,
            scoreHalfTime = EXCLUDED.scoreHalfTime
    """)
    load_to_db(data, query, "load_matches")


def load_scorers(data):
    query = text("""
        INSERT INTO scorers (person_id, competition_id, season_id, team_id, playedMatches, goals, assists, penalties)
        VALUES (:person_id, :competition_id, :season_id, :team_id, :playedMatches, :goals, :assists, :penalties)
        ON CONFLICT (person_id, competition_id, season_id) DO UPDATE SET
            team_id = EXCLUDED.team_id,
            playedMatches = EXCLUDED.playedMatches,
            goals = EXCLUDED.goals,
            assists = EXCLUDED.assists,
            penalties = EXCLUDED.penalties
    """)
    load_to_db(data, query, "load_scorers")


def load_standings(data):
    query = text("""
        INSERT INTO standings (team_id, competition_id, season_id, stage, position, playedGames, form, won, draw, lost, points, goalsFor, goalsAgainst, goalDifference)
        VALUES (:team_id, :competition_id, :season_id, :stage, :position, :playedGames, :form, :won, :draw, :lost, :points, :goalsFor, :goalsAgainst, :goalDifference)
        ON CONFLICT (team_id, competition_id, season_id) DO UPDATE SET
            stage = EXCLUDED.stage,
            position = EXCLUDED.position,
            playedGames = EXCLUDED.playedGames,
            form = EXCLUDED.form,
            won = EXCLUDED.won,
            draw = EXCLUDED.draw,
            lost = EXCLUDED.lost,
            points = EXCLUDED.points,
            goalsFor = EXCLUDED.goalsFor,
            goalsAgainst = EXCLUDED.goalsAgainst,
            goalDifference = EXCLUDED.goalDifference
    """)
    load_to_db(data, query, "load_standings")


def load_referees(data):
    query = text("""
        INSERT INTO referee (id, name, type, nationality)
        VALUES (:id, :name, :type, :nationality)
        ON CONFLICT (id) DO UPDATE SET
            name = EXCLUDED.name,
            type = EXCLUDED.type,
            nationality = EXCLUDED.nationality
    """)
    load_to_db(data, query, "load_referees")

# i had to switch it because tthey were treing to put plasyers i ddinot have the matches for mabye matrch premium or somtehing
def load_squadplayers(data):
    query = text("""
        INSERT INTO squadplayer (team_id, person_id)
        SELECT :team_id, :person_id
        WHERE EXISTS (SELECT 1 FROM person WHERE id = :person_id)
        ON CONFLICT (team_id, person_id) DO NOTHING
    """)
    load_to_db(data, query, "load_squadplayers")


def load_teamstaff(data):
    query = text("""
        INSERT INTO teamstaff (team_id, person_id)
        VALUES (:team_id, :person_id)
        ON CONFLICT (team_id, person_id) DO NOTHING
    """)
    load_to_db(data, query, "load_teamstaff")


def load_coach(data):
    query = text("""
        INSERT INTO coach (id, firstName, lastName, name, dateOfBirth, nationality, contractStart, contractUntil)
        VALUES (:id, :firstName, :lastName, :name, :dateOfBirth, :nationality, :contractStart, :contractUntil)
        ON CONFLICT (id) DO UPDATE SET
            firstName = EXCLUDED.firstName,
            lastName = EXCLUDED.lastName,
            name = EXCLUDED.name,
            dateOfBirth = EXCLUDED.dateOfBirth,
            nationality = EXCLUDED.nationality,
            contractStart = EXCLUDED.contractStart,
            contractUntil = EXCLUDED.contractUntil
    """)
    load_to_db(data, query, "load_coach")


def load_teamcoach(data):
    query = text("""
        INSERT INTO team_coach (team_id, coach_id)
        VALUES (:team_id, :coach_id)
        ON CONFLICT (team_id) DO UPDATE SET
            coach_id = EXCLUDED.coach_id
    """)
    load_to_db(data, query, "load_teamcoach")


def load_matchreferee(data):
    query = text("""
        INSERT INTO matchreferee (match_id, referee_id)
        VALUES (:match_id, :referee_id)
        ON CONFLICT (match_id, referee_id) DO NOTHING
    """)
    load_to_db(data, query, "load_matchreferee")


def load_personcompetition(data):
    query = text("""
        INSERT INTO personcompetition (person_id, competition_id)
        VALUES (:person_id, :competition_id)
        ON CONFLICT (person_id, competition_id) DO NOTHING
    """)
    load_to_db(data, query, "load_personcompetition")


# so i decide to create this fuc to try and help with the time the progm runs as iḿ limited to 6 per min
# so where i get the time the lsat update hhappen so i can compare in the runner and decide if i check that person
# or pass it because ther is not anyhting new
def get_person_last_updated(person_id):
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT lastUpdated FROM person WHERE id = :id"),
            {"id": person_id}
        ).fetchone()
        return result[0] if result else None
    

# so because the winner comes from teams if i introduce the winner after the teams are introduced i can solve the problem
def load_seasons_winner(data):
    query = text("""
        UPDATE season SET winner_id = :winner_id
        WHERE id = :id AND :winner_id IS NOT NULL
    """)
    load_to_db(data, query, "load_seasons_winner")