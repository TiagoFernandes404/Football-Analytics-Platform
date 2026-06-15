-- So i will implement that views i think they are usefull so here i go ahha
-- areas_with_most_teams
-- average_age_per_team
-- teams_distinct_nationalities
-- teams_best_goal_difference_for_competition
-- teams_most_home_wins
-- current_season_matches
-- current_matchday_matches
-- competition_winners
-- top_scorers
-- top_assisters
-- top_penalty_scorers
-- most_matches_played
-- current_matchday_per_competition
-- referees_per_competition
-- players_last_contract_year







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
GROUP BY t.name, compname , s.goalDifference
ORDER BY goalDifference DESC;

-- test of the view teams_best_goal_difference_for_competition 
--SELECT * FROM teams_best_goal_difference_for_competition;

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
WHERE s.endDate >= CURRENT_DATE
 
-- test of the view current_season_matches 
-- SELECT * FROM current_season_matches;
