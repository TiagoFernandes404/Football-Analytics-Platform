# function to protect the elements that can come back null
def safe_get(obj, *keys, default=None):
    for key in keys:
        if obj is None:
            return default
        obj = obj.get(key) if isinstance(obj, dict) else None
    return obj if obj is not None else default

# so the api returns the date in a YYYY-MM and the DB expects YY-MM-DD so the soluction i found was to make a function
# thats puts the days in 01 so i can skip this error and keep the DB DATE secure for the queries
# because is contract dates i think that the day beigng the first who´t matter much
def fix_date(value):
    if value and len(value) == 7:  # "YYYY-MM" -> "YYYY-MM-01"
        return value + "-01"
    return value


def transform_areas(data):
    return [
        {
            "id": area['id'],
            "name": str(area['name']),
            "code": str(area['countryCode']),
            "flag": safe_get(area, 'flag'),
            "parentArea_id": safe_get(area, 'parentAreaId'),
        }
        for area in data['areas']
    ]


def transform_teams(data):
    return [
        {
            "id": team['id'],
            "area_id": safe_get(team, 'area', 'id'),
            "name": str(team['name']),
            "shortName": str(team['shortName']),
            "tla": str(team['tla']),
            "crest": str(team['crest']),
            "address": safe_get(team, 'address'),
            "website": safe_get(team, 'website'),
            "founded": safe_get(team, 'founded'),
            "clubColors": safe_get(team, 'clubColors'),
            "venue": safe_get(team, 'venue'),
            "lastUpdated": team['lastUpdated'],
        }
        for team in data['teams']
    ]


def transform_persons(data):
    return [
        {
            "id": data['id'],
            "name": str(data['name']),
            "firstName": str(data['firstName']),
            "lastName": safe_get(data, 'lastName'),
            "dateOfBirth": safe_get(data, 'dateOfBirth'),
            "nationality": safe_get(data, 'nationality'),
            "section": safe_get(data, 'section'),
            "position": safe_get(data, 'position'),
            "shirtNumber": safe_get(data, 'shirtNumber'),
            "lastUpdated": data['lastUpdated'],
            "contractStart": fix_date(safe_get(data, 'currentTeam', 'contract', 'start')),
            "contractUntil": fix_date(safe_get(data, 'currentTeam', 'contract', 'until')),
        }
    ]


def transform_squadplayers(data):
    return [
        {
            "team_id": team['id'],
            "person_id": person['id'],
        }
        for team in data['teams']
        for person in (safe_get(team, 'squad') or [])
    ]


def transform_teamstaff(data):
    return [
        {
            "team_id": team['id'],
            "person_id": person['id'],
        }
        for team in data['teams']
        for person in (safe_get(team, 'staff') or [])
    ]


def transform_coach(data):
    return [
        {
            "id": safe_get(team, 'coach', 'id'),
            "firstName": safe_get(team, 'coach', 'firstName'),
            "lastName": safe_get(team, 'coach', 'lastName'),
            "name": safe_get(team, 'coach', 'name'),
            "dateOfBirth": safe_get(team, 'coach', 'dateOfBirth'),
            "nationality": safe_get(team, 'coach', 'nationality'),
            "contractStart": fix_date(safe_get(team, 'coach', 'contract', 'start')),
            "contractUntil": fix_date(safe_get(team, 'coach', 'contract', 'until')),
        }
        for team in data['teams']
        if safe_get(team, 'coach') and safe_get(team, 'coach', 'id')
    ]


def transform_teamcoach(data):
    return [
        {
            "team_id": team['id'],
            "coach_id": safe_get(team, 'coach', 'id'),
        }
        for team in data['teams']
        if safe_get(team, 'coach') and safe_get(team, 'coach', 'id')
    ]


def transform_seasons(data):
    return [
        {
            "id": competition['currentSeason']['id'],
            "startDate": competition['currentSeason']['startDate'],
            "endDate": safe_get(competition, 'currentSeason', 'endDate'),
            "currentMatchday": safe_get(competition, 'currentSeason', 'currentMatchday'),
            "winner_id": None,  # here insert as none and in the end we search for the winner 
        }
        for competition in data['competitions']
        if safe_get(competition, 'currentSeason')
    ]


def transform_referee(data):
    return [
        {
            "id": referee['id'],
            "name": str(referee['name']),
            "type": safe_get(referee, 'type'),
            "nationality": safe_get(referee, 'nationality'),
        }
        for match in data['matches']
        for referee in (safe_get(match, 'referees') or [])
    ]


def transform_competitions(data):
    return [
        {
            "id": competition['id'],
            "area_id": competition['area']['id'],
            "name": str(competition['name']),
            "code": str(competition['code']),
            "type": safe_get(competition, 'type'),
            "emblem": safe_get(competition, 'emblem'),
            "plan": safe_get(competition, 'plan'),
            "currentSeason": competition['currentSeason']['id'],
            "numberOfAvailableSeasons": competition['numberOfAvailableSeasons'],
            "lastUpdated": competition['lastUpdated'],
        }
        for competition in data['competitions']
        if safe_get(competition, 'currentSeason')
    ]


def transform_matchreferee(data):
    return [
        {
            "match_id": match['id'],
            "referee_id": referee['id'],
        }
        for match in data['matches']
        for referee in (safe_get(match, 'referees') or [])
    ]


def transform_scorers(data):
    return [
        {
            "person_id": scorer['player']['id'],
            "competition_id": data['competition']['id'],
            "season_id": data['season']['id'],
            "team_id": scorer['team']['id'],
            "playedMatches": scorer['playedMatches'],
            "goals": scorer['goals'],
            "assists": safe_get(scorer, 'assists') or 0,
            "penalties": safe_get(scorer, 'penalties') or 0,
        }
        for scorer in data['scorers']
        if safe_get(scorer, 'player', 'id') and safe_get(scorer, 'team', 'id')
    ]


def transform_matches(data):
    return [
        {
            "id": match['id'],
            "area_id": safe_get(match, 'area', 'id'),
            "competition_id": safe_get(match, 'competition', 'id'),
            "season_id": safe_get(match, 'season', 'id'),
            "utcDate": match['utcDate'],
            "status": safe_get(match, 'status'),
            "matchday": safe_get(match, 'matchday'),
            "stage": safe_get(match, 'stage'),
            "match_group": safe_get(match, 'group'),
            "lastUpdated": match['lastUpdated'],
            "homeTeam": safe_get(match, 'homeTeam', 'id'),
            "awayTeam": safe_get(match, 'awayTeam', 'id'),
            "scoreWinner": safe_get(match, 'score', 'winner'),
            "scoreDuration": safe_get(match, 'score', 'duration'),
            "scoreFullTime": str(safe_get(match, 'score', 'fullTime')) if safe_get(match, 'score', 'fullTime') else None,
            "scoreHalfTime": str(safe_get(match, 'score', 'halfTime')) if safe_get(match, 'score', 'halfTime') else None,
        }
        for match in data['matches']
    ]


def transform_standings(data):
    return [
        {
            "team_id": table['team']['id'],
            "competition_id": data['competition']['id'],
            "season_id": data['season']['id'],
            "stage": safe_get(standings, 'stage'),
            "position": table['position'],
            "playedGames": table['playedGames'],
            "form": safe_get(table, 'form'),
            "won": table['won'],
            "draw": table['draw'],
            "lost": table['lost'],
            "points": table['points'],
            "goalsFor": table['goalsFor'],
            "goalsAgainst": table['goalsAgainst'],
            "goalDifference": table['goalDifference'],
        }
        for standings in data['standings']
        for table in standings['table']
    ]


def transform_personcompetition(data):
    return [
        {
            "person_id": data['id'],
            "competition_id": competition['id'],
        }
        for competition in (safe_get(data, 'currentTeam', 'runningCompetitions') or [])
    ]

# so because the winner comes from teams if i introduce the winner after the teams are introduced i can solve the problem
# same as load 
def transform_seasons_winner(data):
    return [
        {
            "id": competition['currentSeason']['id'],
            "winner_id": safe_get(competition, 'currentSeason', 'winner', 'id'),
        }
        for competition in data['competitions']
        if safe_get(competition, 'currentSeason')
    ]