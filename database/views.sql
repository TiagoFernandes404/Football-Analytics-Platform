-- So in this file the commnet is under the view idk why just started like that i will leave it like that
-- for the vibes i think haha

CREATE OR REPLACE VIEW areas_with_most_teams AS
SELECT a.name, COUNT(t.id) AS totalperarea
FROM area a 
JOIN team t ON a.id = t.area_id
GROUP BY a.name
ORDER BY totalperarea DESC;

-- test of the view areas_with_most_teams 
-- SELECT * FROM areas_with_most_teams;

CREATE OR REPLACE VIEW average_age_per_team AS
SELECT t.name , ROUND(AVG(EXTRACT(YEAR FROM AGE(p.dateOfBirth))),1) AS media
FROM team t
JOIN squadplayer sp ON t.id = sp.team_id
JOIN person p ON sp.person_id = p.id
GROUP BY t.name 
ORDER BY media DESC;

-- test of the view average_age_per_team 
-- SELECT * FROM average_age_per_team;

CREATE OR REPLACE VIEW teams_distinct_nationalities AS
SELECT t.name, COUNT(DISTINCT p.nationality) AS total_nationalities
FROM person p
JOIN squadplayer sp ON sp.person_id = p.id
JOIN team t ON sp.team_id = t.id
GROUP BY t.name
ORDER BY total_nationalities DESC;

-- test of the view teams_distinct_nationalities 
-- SELECT * FROM teams_distinct_nationalities;

CREATE OR REPLACE VIEW teams_best_goal_difference_for_competition AS
SELECT t.name, c.name AS compname,s.goalDifference
FROM team t
JOIN standings s ON t.id = s.team_id
JOIN competition c ON s.competition_id = c.id
ORDER BY goalDifference DESC;

-- test of the view teams_best_goal_difference_for_competition 
-- SELECT * FROM teams_best_goal_difference_for_competition;

CREATE OR REPLACE VIEW teams_most_home_wins AS
SELECT t.name ,COUNT (*) AS home_wins
FROM team t
JOIN match m ON t.id = m.homeTeam
WHERE m.status = 'FINISHED'
AND  m.scoreWinner = 'HOME_TEAM'
GROUP BY t.name
ORDER BY home_wins DESC;

-- test of the view teams_most_home_wins 
-- SELECT * FROM teams_most_home_wins;

CREATE OR REPLACE VIEW current_season_matches AS
SELECT m.*
FROM match m
JOIN season s ON s.id = m.season_id
WHERE s.endDate >= CURRENT_DATE;
 
-- test of the view current_season_matches 
-- SELECT * FROM current_season_matches;


CREATE OR REPLACE VIEW current_matchday_matches AS
SELECT m.*
FROM match m
JOIN season s ON s.id = m.season_id
WHERE s.endDate >= CURRENT_DATE
AND s.startDate < CURRENT_DATE
AND m.matchday = s.currentMatchday;

-- test of the view current_matchday_matches 
-- SELECT * FROM current_matchday_matches;
	
CREATE OR REPLACE VIEW competition_winners AS
SELECT DISTINCT c.name AS competition, t.name AS winner
FROM season s
JOIN team t   ON t.id  = s.winner_id
JOIN match m  ON m.season_id = s.id
JOIN competition c ON c.id = m.competition_id
WHERE s.winner_id IS NOT NULL;

-- test of the view competition_winners 
-- SELECT * FROM competition_winners;

CREATE OR REPLACE VIEW top_scorers AS
SELECT DISTINCT ON (s.season_id, s.competition_id)s.season_id,s.competition_id,p.name,s.goals
FROM scorers s
JOIN person p ON p.id = s.person_id
ORDER BY s.season_id, s.competition_id, s.goals DESC;

-- test of the view top_scorers
-- SELECT * FROM top_scorers;

CREATE OR REPLACE VIEW top_assisters AS
SELECT DISTINCT ON (s.season_id, s.competition_id)s.season_id,s.competition_id,p.name,s.assists
FROM scorers s
JOIN person p ON p.id = s.person_id
ORDER BY s.season_id, s.competition_id, s.assists DESC;

-- test of the view top_assisters
-- SELECT * FROM top_assisters;

CREATE OR REPLACE VIEW top_penalty_scorers AS
SELECT DISTINCT ON (s.season_id, s.competition_id)s.season_id,s.competition_id,p.name,s.penalties
FROM scorers s
JOIN person p ON p.id = s.person_id
ORDER BY s.season_id, s.competition_id, s.penalties DESC;

-- test of the view top_penalty_scorers
-- SELECT * FROM top_penalty_scorers;

CREATE OR REPLACE VIEW most_matches_played AS
SELECT c.name AS competition, p.name AS pessoa, COUNT(DISTINCT m.id) AS total_matches
FROM person p
JOIN squadplayer sp ON sp.person_id = p.id
JOIN match m ON (m.homeTeam = sp.team_id OR m.awayTeam = sp.team_id)
JOIN competition c ON c.id = m.competition_id
WHERE m.status = 'FINISHED'
GROUP BY c.name, p.name
ORDER BY total_matches DESC;

-- in this one is the only i got strange results like one player with 120 i cannot fixe it maybe is because of 
-- he get transfer from the team and has the only way i get players is from teams i can mixed both teams he plays 
-- for but as i am poor i only have the free api
-- test of the view most_matches_played
-- SELECT * FROM most_matches_played;

CREATE OR REPLACE VIEW current_matchday_per_competition AS
SELECT s.currentMatchday, c.name
FROM competition c
JOIN season s ON c.currentSeason = s.id;


-- test of the view current_matchday_per_competition
-- SELECT * FROM current_matchday_per_competition;

CREATE OR REPLACE VIEW referees_per_competition AS
SELECT c.name, COUNT( DISTINCT r.id) AS totalreferee
FROM referee r
JOIN matchreferee mr ON mr.referee_id = r.id
JOIN match m ON m.id = mr.match_id
JOIN competition c ON c.id = m.competition_id
GROUP BY (c.name)
ORDER BY totalreferee DESC;

-- test of the view referees_per_competition
-- SELECT * FROM referees_per_competition;

CREATE OR REPLACE VIEW players_last_contract_year AS
SELECT p.name, EXTRACT(YEAR FROM p.contractUntil) AS contract_year
FROM person p 
JOIN squadplayer sp ON sp.person_id = p.id
WHERE p.contractUntil IS NOT NULL
AND EXTRACT(YEAR FROM p.contractUntil) <= EXTRACT(YEAR FROM CURRENT_DATE) + 1
ORDER BY contract_year;

-- test of the view players_last_contract_year
-- SELECT * FROM players_last_contract_year;