# Development Log

## Session 1 — Project Setup & Schema Design

**Objectives:**
- Set up the development environment
- Explore the API
- Design the database schema

**Work done:**

### Environment Setup
Installed and configured all required tools: PostgreSQL 16, Python 3.11 via deadsnakes 
PPA, pgAdmin 4, and VS Code with the Thunder Client extension. Created the project 
structure and virtual environment, and installed all Python dependencies.

### API Exploration
First contact with a REST API. Used Thunder Client to manually call each endpoint from 
football-data.org and analyse the raw JSON responses — areas, competitions, seasons, 
teams, matches, persons, standings and scorers — before writing any code.

### Database Schema Design
Designed the full relational schema from scratch in draw.io by analysing each API 
response field by field. Key decisions made during this process:
- Identified arrays in the API responses as many-to-many relationships requiring 
junction tables (`matchreferee`, `personcompetition`)
- Chose to flatten the `score` object directly into the `match` table (denormalisation) 
since it is always 1-to-1
- Designed composite primary keys for `scorers` (`person_id`, `competition_id`, 
`season_id`) and `standings` (`team_id`, `competition_id`, `season_id`)
- Used a self-referencing foreign key in `area` for the parent area relationship
- Renamed `group` to `match_group` — reserved keyword in SQL

**Schema at end of session 1 — 11 tables:**

`area` · `team` · `person` · `season` · `referee` · `competition` · `scorers` · 
`match` · `standings` · `matchreferee` · `personcompetition`

![ER Diagram v1](er_diagram.png)

---

## Session 2 — Physical Implementation & Environment Setup

**Objectives:**
- Create the physical database
- Set up the `.env` file
- Clean up the repository

**Work done:**

### Physical Implementation
Executed the SQL schema in PostgreSQL via pgAdmin. While cross-referencing the API 
responses more carefully during implementation, found inconsistencies in the logical 
model that required corrections — 4 new tables were added to the schema.

### Schema Corrections
After revisiting the API responses in detail, the following tables were added:
- `squadplayer` — junction table between `team` and `person` for squad players
- `teamstaff` — junction table between `team` and `person` for staff members
- `coach` — separate entity for coach data (different structure from person in the API)
- `team_coach` — junction table between `team` and `coach`

### Environment Setup
Created the `.env` file with database credentials and API key. Understood its role in 
keeping sensitive data out of version control via `.gitignore`.

### Repository Cleanup
Removed an accidental `.Rhistory` file that had been committed in session 1.

**Schema at end of session 2 — 15 tables:**

`area` · `team` · `person` · `squadplayer` · `teamstaff` · `coach` · `team_coach` · 
`season` · `referee` · `competition` · `personcompetition` · `scorers` · `match` · 
`standings` · `matchreferee`

![ER Diagram v2](er_diagram_v2.png)

---

**Next session:** Connect the API to the database via Python — `settings.py` → 
`connection.py` → `extract.py`.