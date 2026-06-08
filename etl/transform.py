def safe_get(obj, *keys, default=None):
    for key in keys:
        if obj is None:
            return default
        obj = obj.get(key) if isinstance(obj, dict) else None
    return obj if obj is not None else default


def transform_areas(data):
    return [
        {
            "id": area['id'],
            "name": str(area['name']),
            "code": str(area['countryCode']),
            "flag": str(safe_get(area, 'flag')) if safe_get(area, 'flag') else None,
            "parentArea_id": safe_get(area, 'parentAreaId'),
        }
        for area in data['areas']
    ]


def transform_teams(data):
    return [
        {
            "id": team['id'],
            "area_id": team['area']['id'],
            "name": str(team['name']),
            "shortName": str(team['shortName']),
            "tla": str(team['tla']),
            "crest": str(team['crest']),
            "address": str(safe_get(team, 'address')) if safe_get(team, 'address') else None,
            "website": str(safe_get(team, 'website')) if safe_get(team, 'website') else None,
            "founded": safe_get(team, 'founded'),
            "clubColors": str(safe_get(team, 'clubColors')) if safe_get(team, 'clubColors') else None,
            "venue": str(safe_get(team, 'venue')) if safe_get(team, 'venue') else None,
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
            "lastName": str(safe_get(data, 'lastName')) if safe_get(data, 'lastName') else None,
            "dateOfBirth": safe_get(data, 'dateOfBirth'),
            "nationality": str(data['nationality']),
            "section": str(data['section']),
            "position": str(safe_get(data, 'position')) if safe_get(data, 'position') else None,
            "shirtNumber": safe_get(data, 'shirtNumber'),
            "lastUpdated": data['lastUpdated'],
            "contractStart": safe_get(data, 'currentTeam', 'contract', 'start'),
            "contractUntil": safe_get(data, 'currentTeam', 'contract', 'until'),
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
            "id": team['coach']['id'],
            "firstName": str(safe_get(team, 'coach', 'firstName')) if safe_get(team, 'coach', 'firstName') else None,
            "lastName": str(safe_get(team, 'coach', 'lastName')) if safe_get(team, 'coach', 'lastName') else None,
            "name": str(safe_get(team, 'coach', 'name')) if safe_get(team, 'coach', 'name') else None,
            "dateOfBirth": safe_get(team, 'coach', 'dateOfBirth'),
            "nationality": str(safe_get(team, 'coach', 'nationality')) if safe_get(team, 'coach', 'nationality') else None,
            "contractStart": safe_get(team, 'coach', 'contract', 'start'),
            "contractUntil": safe_get(team, 'coach', 'contract', 'until'),
        }
        for team in data['teams']
        if safe_get(team, 'coach') and safe_get(team, 'coach', 'id')
    ]


def transform_teamcoach(data):
    return [
        {
            "team_id": team['id'],
            "coach_id": team['coach']['id'],
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
            "winner_id": safe_get(competition, 'currentSeason', 'winner'),
        }
        for competition in data['competitions']
        if safe_get(competition, 'currentSeason')
    ]




def transform_referee(data):
    return [
        {
            "id": referee['id'],
            "name": str(referee['name']),
            "type": str(referee['type']),
            "nationality": str(referee['nationality']),
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
            "type": str(safe_get(competition, 'type')) if safe_get(competition, 'type') else None,
            "emblem": str(safe_get(competition, 'emblem')) if safe_get(competition, 'emblem') else None,
            "plan": str(safe_get(competition, 'plan')) if safe_get(competition, 'plan') else None,
            "currentSeason": competition['currentSeason']['id'],
            "numberOfAvailableSeasons": competition['numberOfAvailableSeasons'],
            "lastUpdated": competition['lastUpdated'],
        }
        for competition in data['competitions']
        if safe_get(competition, 'currentSeason')
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
            "area_id": match['area']['id'],
            "competition_id": match['competition']['id'],
            "season_id": match['season']['id'],
            "utcDate": match['utcDate'],
            "status": str(safe_get(match, 'status')) if safe_get(match, 'status') else None,
            "matchday": match['matchday'],
            "stage": str(safe_get(match, 'stage')) if safe_get(match, 'stage') else None,
            "match_group": str(safe_get(match, 'group')) if safe_get(match, 'group') else None,
            "lastUpdated": match['lastUpdated'],
            "homeTeam": match['homeTeam']['id'],
            "awayTeam": match['awayTeam']['id'],
            "scoreWinner": str(safe_get(match, 'score', 'winner')) if safe_get(match, 'score', 'winner') else None,
            "scoreDuration": str(safe_get(match, 'score', 'duration')) if safe_get(match, 'score', 'duration') else None,
            "scoreFullTime": str(safe_get(match, 'score', 'fullTime')) if safe_get(match, 'score', 'fullTime') else None,
            "scoreHalfTime": str(safe_get(match, 'score', 'halfTime')) if safe_get(match, 'score', 'halfTime') else None,
        }
        for match in data['matches']
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


def transform_personcompetition(data):
    return [
        {
            "person_id": data['id'],
            "competition_id": competition['id'],
        }
        for competition in (safe_get(data, 'currentTeam', 'runningCompetitions') or [])
    ]