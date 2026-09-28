# Football League API

Made with FastAPI and SQLalchemy, this API will help you to organize your own football league and consult it's data, here are the endpoints:

### GET /equipos
Shows a list of all the teams in the league.

### GET /equipos/{id}/jugadores
Shows a list of all the players of a specific team.

### GET /partidos
Shows the already played matches

### GET /tabla	
Shows the league's table and the performance of the teams (pts, PJ, PG, PE, PP).

### GET /goleadores
Shows a list of the best goalscorers.

### POST /partidos	
Loads a match's result into the database.

# Running process
    - Clone the repository with git clone <repository-url> then cd <repository-name>
    - Activate the virtual enviroment in the terminal with source venv/bin/activate
    - Install all the dependencies with pip install -r requirements.txt
    - Initialize database with python seed.py
    - Start command: python seed.py && gunicorn main:app -k uvicorn_worker.UvicornWorker -w 2 -b 0.0.0.0:$PORT