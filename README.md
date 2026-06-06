# ⚽ Football Intelligence Platform

A personal portfolio project built to demonstrate real-world data engineering skills using live football data. This project evolves across 3 phases over several months, going from a raw ETL pipeline to a full analytics platform.

---

## 👨‍💻 About

Recently graduated in Computer Science from Universidade do Minho. Background in MySQL, SQL, Java, Python, C, C++, Haskell and Erlang. Previously built a relational database project in MySQL at university covering sporting events.

This is my first independent project outside of university — built to learn PostgreSQL, REST APIs, ETL pipelines and data engineering tools from scratch, while understanding every decision well enough to explain it in a job interview.

**Goal:** Build a strong portfolio that demonstrates real data engineering skills, from database design to automated pipelines and analytics.

---

## 🗺️ Project Roadmap

### ✅ Phase 1 — ETL Data Pipeline *(in progress)*

Extract real football data from the [football-data.org](https://www.football-data.org) API (free tier), transform it and load it automatically into a PostgreSQL database.

**Objectives:**
- Automated pipeline with scheduled runs
- Execution logs and error handling
- Historical data tracking per season
- Normalised relational schema designed from scratch

**Technologies:** PostgreSQL 16, Python 3.11, SQLAlchemy, psycopg2, requests, python-dotenv

---

### 🔜 Phase 2 — Scouting System

Build a scouting system on top of the pipeline data, allowing filtering of players by position, age and performance metrics, with direct player comparison.

**Objectives:**
- Advanced SQL queries
- Views, stored procedures and index optimisation
- Player comparison engine

---

### 🔜 Phase 3 — Analytics & Visualisation

Analytical layer with advanced metrics calculated in SQL, interactive dashboard in Streamlit, and deployment to a free cloud platform (Railway or Supabase).

---

## 🛠️ Development Process

### Step 1 — Environment Setup
Installed and configured all the required tools: PostgreSQL 16, Python 3.11 via deadsnakes PPA, pgAdmin 4, and VS Code with the Thunder Client extension. Created the project structure and virtual environment, and installed all Python dependencies.

### Step 2 — API Exploration
First contact with a REST API. Used Thunder Client to manually call each endpoint from football-data.org and analyse the raw JSON responses — areas, competitions, seasons, teams, matches, persons, standings and scorers — before writing any code.

### Step 3 — Database Schema Design
Designed the full relational schema from scratch in draw.io by analysing each API response field by field. Key decisions made during this process:
- Identified arrays in the API responses as many-to-many relationships requiring junction tables (`match_referees`, `person_competitions`)
- Chose to flatten the `score` object directly into the `matches` table (denormalisation) since it is always 1-to-1
- Designed composite primary keys for `scorers` (`person_id`, `competition_id`, `season_id`) and `standings` (`team_id`, `competition_id`, `season_id`)
- Used a self-referencing foreign key in `areas` for the parent area relationship

The schema covers 11 tables and was fully designed before writing a single line of SQL.

---

## 🗄️ Database Schema

The relational schema was designed by analysing each API endpoint response before writing any code. It covers 11 tables:

`areas` · `competitions` · `seasons` · `teams` · `matches` · `referees` · `match_referees` · `persons` · `person_competitions` · `scorers` · `standings`

![ER Diagram](docs/er_diagram.png)

---

## 📡 Data Source

[football-data.org](https://www.football-data.org) — Free tier (TIER_ONE)

**Competitions covered:** Premier League, Bundesliga, Serie A, Ligue 1, Primeira Liga, Championship, Eredivisie, Champions League, European Championship, FIFA World Cup, Copa Libertadores, Brasileirão.

---

## 🚀 Getting Started

```bash
# Clone the repository
git clone https://github.com/your-username/football-analytics-platform.git
cd football-analytics-platform

# Create and activate virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env with your API key and database credentials
```

### Environment Variables

```
API_KEY=your_football_data_api_key
DB_HOST=localhost
DB_PORT=5432
DB_NAME=football_analytics
DB_USER=postgres
DB_PASSWORD=your_password
```

---

## 📁 Project Structure

```
football-analytics-platform/
├── config/
│   └── settings.py          # Configuration loader
├── database/
│   ├── connection.py        # Database connection
│   ├── models.py            # SQLAlchemy models
│   └── migrations/          # Schema migrations
├── etl/
│   ├── extract.py           # API extraction
│   ├── transform.py         # Data transformation
│   └── load.py              # Database loading
├── pipeline/
│   └── runner.py            # Pipeline orchestration
├── docs/
│   ├── er_diagram.png       # ER diagram
│   └── er_diagram.xml       # Editable draw.io file
├── logs/                    # Execution logs
├── .env                     # Environment variables (not committed)
├── requirements.txt
└── README.md
```

---

## 📋 Requirements

```
requests
psycopg2-binary
sqlalchemy
python-dotenv
```

---

*Built from scratch as a learning project — every design decision was made with understanding, not just copying.*
