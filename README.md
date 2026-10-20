# Football League API

REST API to manage a football league, consult teams, players, matches, and standings. Built with FastAPI and SQLite for the Informática course (TDS05) at Universidad de Mendoza.

## Authors

- Juan Bautista Ficco Laiseca

## Requirements

- Python 3.11 or newer
- Git

## How to run it

1. Clone the repository and enter the folder:

   ```bash
   git clone https://github.com/Juanba303/Trabajo_Integrador
   cd Trabajo_Integrador
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

   On Windows: `venv\Scripts\activate`

3. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Set up your environment variables:

   Create a `.env` file in the root directory:

   ```env
   API_KEY=test-key-2026
   DB_FILE=league.db
   ```

5. Create the database and load the sample data:

   ```bash
   python seed.py
   ```

6. Start the server:

   ```bash
   uvicorn main:app --reload
   ```

7. Open http://127.0.0.1:8000/docs

## How to use it

Every endpoint requires the API key in the `X-API-Key` header.
In `/docs`, click **Authorize** and paste the key: `test-key-2026`.

| Method | Path | Description |
|--------|------|-------------|
| GET | /matches?team_id=1 | List matches, optionally filtered by team |
| GET | /teams/{id} | Get details of a specific team |
| GET | /teams/{id}/players | List all players of a specific team |
| GET | /players?position=Forward | List all players, optionally filtered by position |
| GET | /table | Get the current league table |
| POST | /matches | Load a new match result |

Example:

```bash
curl -H "X-API-Key: test-key-2026" http://127.0.0.1:8000/teams/1
```

```json
{"id": 1, "name": "Team Name"}
```

Errors: `401` without a valid key, `404` if the team or item does not exist, `400` if the data sent is invalid, `500` if a database error occurs.

## Deploy

Live at https://football-league-api-2iw7.onrender.com/docs

The free plan sleeps after 15 minutes without use, so the first request can take about a minute.

## Use of AI

We used AI to get solutions for data loading in seed.py and
organize the logic behind the table calculation and validation criteria.
All code was written and tested by me.