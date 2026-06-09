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
- ✅ Normalised relational schema designed from scratch
- ✅ ETL pipeline structure (extract / transform / load) — the backbone of the project, without which nothing else would be possible
- ✅ Execution logs and error handling
- ⏳ Automated pipeline with scheduled runs
- ⏳ Historical data tracking per season

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

## 🗄️ Database Schema

15 tables designed from scratch by analysing each API endpoint response.
For the full schema evolution and design decisions see [Development Log](docs/DEVELOPMENT_LOG.md).

![ER Diagram](docs/er_diagram_v2.png)

---

## 📡 Data Source

[football-data.org](https://www.football-data.org) — Free tier (TIER_ONE)

**Competitions covered:** Campeonato Brasileiro Série A, Championship, Premier League, UEFA Champions League, European Championship, Ligue 1, Bundesliga, Serie A, Eredivisie, Primeira Liga, Copa Libertadores, Primera Division, FIFA World Cup.

---

## 🚀 Getting Started

```bash
# Clone the repository
git clone https://github.com/TiagoFernandes404/Football-Analytics-Platform.git
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
DB_NAME=football_intelligence_platform
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
│   └── schema.sql           # SQL schema
├── etl/
│   ├── extract.py           # API extraction
│   ├── transform.py         # Data transformation
│   └── load.py              # Database loading
├── pipeline/
│   └── runner.py            # Pipeline orchestration
├── docs/
│   ├── DEVELOPMENT_LOG.md   # Session logs and design decisions
│   ├── er_diagram.png       # ER diagram v1
│   ├── er_diagram.xml       # Editable draw.io file v1
│   ├── er_diagram_v2.png    # ER diagram v2
│   └── er_diagram_v2.xml    # Editable draw.io file v2
├── logs/                    # Execution logs
├── .env                     # Environment variables (not committed)
├── requirements.txt
└── README.md
```