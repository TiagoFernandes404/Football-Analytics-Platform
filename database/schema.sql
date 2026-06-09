
-- IDs come directly from the API so no SERIAL or IDENTITY needed
-- TEXT for fields where max size is unpredictable (names, urls, etc)
-- VARCHAR(n) where size is logically limited (e.g. tla is always 3 chars)
-- NOT NULL only where I'm sure the API never sends null

CREATE TABLE area (
    id INTEGER,
    name VARCHAR(50) NOT NULL,
    code VARCHAR(3) NOT NULL,
    flag TEXT,
    parentArea_id INTEGER,
    PRIMARY KEY(id),
    FOREIGN KEY(parentArea_id) REFERENCES area(id)
);

CREATE TABLE team (
    id INTEGER,
    area_id INTEGER NOT NULL,
    name VARCHAR(50) NOT NULL,
    shortName VARCHAR(20) NOT NULL,
    tla VARCHAR(3) NOT NULL,
    crest TEXT NOT NULL,
    address TEXT,
    website TEXT,
    founded INTEGER,
    clubColors TEXT,
    venue TEXT,
    lastUpdated TIMESTAMP NOT NULL,
    PRIMARY KEY(id),
    FOREIGN KEY(area_id) REFERENCES area(id)
);

CREATE TABLE person (
    id INTEGER,
    name TEXT NOT NULL,
    firstName TEXT NOT NULL,
    lastName TEXT,
    dateOfBirth DATE,
    nationality VARCHAR(20) NOT NULL,
    section VARCHAR(50) NOT NULL,
    position VARCHAR(50),
    shirtNumber INTEGER,
    lastUpdated TIMESTAMP NOT NULL,
    contractStart DATE,
    contractUntil DATE,
    PRIMARY KEY(id)
);


CREATE TABLE squadplayer(
	team_id INTEGER,
	person_id INTEGER,
	PRIMARY KEY (team_id,person_id),
	FOREIGN KEY (team_id) REFERENCES team(id),
	FOREIGN KEY (person_id) REFERENCES person(id)
);

CREATE TABLE teamstaff(
	team_id INTEGER,
	person_id INTEGER,
	PRIMARY KEY (team_id,person_id),
	FOREIGN KEY (team_id) REFERENCES team(id),
	FOREIGN KEY (person_id) REFERENCES person(id)
);

CREATE TABLE coach(
	id INTEGER,
	firstName TEXT,
	lastName TEXT,
	name TEXT,
	dateOfBirth DATE,
	nationality VARCHAR(20),
	contractStart DATE,
	contractUntil DATE,
	PRIMARY KEY(id)
);

CREATE TABLE team_coach(
	team_id INTEGER,
	coach_id INTEGER,
	PRIMARY KEY (team_id),
	FOREIGN KEY (team_id) REFERENCES team(id),
	FOREIGN KEY (coach_id) REFERENCES coach(id)
);

CREATE TABLE season(
	id INTEGER,
	startDate DATE NOT NULL,
	endDate DATE,
	currentMatchday INTEGER,
	winner_id INTEGER,
	PRIMARY KEY(id),
	FOREIGN KEY(winner_id) REFERENCES team(id)
);

CREATE TABLE referee(
	id INTEGER,
	name TEXT NOT NULL,
	type TEXT NOT NULL,
	nationality TEXT NOT NULL,
	PRIMARY KEY(id)
);

CREATE TABLE competition(
	id INTEGER,
	area_id INTEGER NOT NULL,
 	name VARCHAR(50) NOT NULL,
	code VARCHAR(3) NOT NULL,
	type VARCHAR(20),
	emblem TEXT,
	plan TEXT,
	currentSeason INTEGER NOT NULL,
	numberOfAvailableSeasons INTEGER NOT NULL,
	lastUpdated TIMESTAMP NOT NULL,
	PRIMARY KEY (id),
	FOREIGN KEY(area_id) REFERENCES area(id),
	FOREIGN KEY(currentSeason) REFERENCES season(id)
);

CREATE TABLE personcompetition(
	person_id INTEGER,
	competition_id INTEGER,
	PRIMARY KEY(person_id,competition_id),
	FOREIGN KEY(person_id) REFERENCES person(id),
	FOREIGN KEY(competition_id) REFERENCES competition(id)
);

CREATE TABLE scorers(
	person_id INTEGER,
	competition_id INTEGER,
	season_id INTEGER,
	team_id INTEGER NOT NULL,
	playedMatches INTEGER NOT NULL,
	goals INTEGER NOT NULL,
	assists INTEGER NOT NULL,
	penalties INTEGER NOT NULL,
	PRIMARY KEY(person_id,competition_id,season_id),
	FOREIGN KEY(person_id) REFERENCES person(id),
	FOREIGN KEY(competition_id) REFERENCES competition(id),
	FOREIGN KEY(season_id) REFERENCES season(id)
);

 -- ERROR:  syntax error at or near "group"
 -- LINE 152:     group VARCHAR(50),
 --            ^ 
 --SQL state: 42601
 --Character: 3596

 -- In this Table group pops as an error because is a reserved word it's used in GROUP BY  
 -- so we have to switch it out (to match_group)
 
CREATE TABLE match(
    id INTEGER,
    area_id INTEGER NOT NULL,
    competition_id INTEGER NOT NULL,
    season_id INTEGER NOT NULL,
    utcDate TIMESTAMP NOT NULL,
    status VARCHAR(20),
    matchday INTEGER NOT NULL,
    stage VARCHAR(50),
    match_group VARCHAR(50),
    lastUpdated TIMESTAMP NOT NULL,
    homeTeam INTEGER NOT NULL,
    awayTeam INTEGER NOT NULL,
    scoreWinner VARCHAR(20),
    scoreDuration VARCHAR(20),
    scoreFullTime TEXT,
    scoreHalfTime TEXT,
    PRIMARY KEY(id),
    FOREIGN KEY(area_id) REFERENCES area(id),
    FOREIGN KEY(competition_id) REFERENCES competition(id),
    FOREIGN KEY(season_id) REFERENCES season(id),
    FOREIGN KEY(homeTeam) REFERENCES team(id),
    FOREIGN KEY(awayTeam) REFERENCES team(id)
);

CREATE TABLE standings(
    team_id INTEGER,
    competition_id INTEGER,
    season_id INTEGER,
    stage VARCHAR(50),
    position INTEGER,
    playedGames INTEGER NOT NULL,
    form VARCHAR(20),
    won INTEGER NOT NULL,
    draw INTEGER NOT NULL,
    lost INTEGER NOT NULL,
    points INTEGER NOT NULL,
    goalsFor INTEGER NOT NULL,
    goalsAgainst INTEGER NOT NULL,
    goalDifference INTEGER NOT NULL,
    PRIMARY KEY(team_id, competition_id, season_id),
    FOREIGN KEY(team_id) REFERENCES team(id),
    FOREIGN KEY(competition_id) REFERENCES competition(id),
    FOREIGN KEY(season_id) REFERENCES season(id)
);

CREATE TABLE matchreferee(
    match_id INTEGER,
    referee_id INTEGER,
    PRIMARY KEY (match_id, referee_id),
    FOREIGN KEY (match_id) REFERENCES match(id),
    FOREIGN KEY (referee_id) REFERENCES referee(id)
);

-- area references itself (parentArea_id) so when inserting all areas at once
-- the parent may not exist yet when the child is inserted
-- DEFERRABLE INITIALLY DEFERRED tells PostgreSQL to only check the FK at the end of the transaction
ALTER TABLE area DROP CONSTRAINT area_parentarea_id_fkey;
ALTER TABLE area ADD CONSTRAINT area_parentarea_id_fkey 
    FOREIGN KEY (parentArea_id) REFERENCES area(id) 
    DEFERRABLE INITIALLY DEFERRED;

-- competition references season but seasons winner_id is set to NULL on insert
-- so we only need to defer competition -> season, not season -> team
ALTER TABLE competition DROP CONSTRAINT competition_currentseason_fkey;
ALTER TABLE competition ADD CONSTRAINT competition_currentseason_fkey
    FOREIGN KEY (currentSeason) REFERENCES season(id)
    DEFERRABLE INITIALLY DEFERRED;


-- Because a use the free plan i can upload personcompetition because some came wiht the league i dont have acess
-- so if i take competition of FK that solves it i losse the verification but the competition i have on the BD 
-- are insert when i pass the competitions
ALTER TABLE personcompetition DROP CONSTRAINT personcompetition_competition_id_fkey;
