from fastapi import FastAPI, HTTPException
from sqlalchemy.exc import OperationalError
import crud

app = FastAPI()

@app.get("/games")
def list_games(team_id: int | None = None):
    try:
        return crud.list_games(team_id)
    except OperationalError:
        raise HTTPException(status_code=500, detail="Error al consultar la base de datos")

@app.get("/teams")
def list_teams():
    try:
        return crud.list_teams()
    except OperationalError:
        raise HTTPException(status_code=500, detail="Error al consultar la base de datos")

@app.get("/teams/{id}")
def get_team_by_id(id: int):
    team = crud.get_team_by_id(id)
    if team is None:
        raise HTTPException(status_code=404, detail="El equipo no existe") 

@app.get("/teams/{id}/players")
def get_players_by_team_id(id: int):
    players = crud.list_players_by_team_id(id)
    if players is None:
        raise HTTPException(status_code=404, detail="El equipo no existe")

@app.get("/players")
def list_players(position: str | None = None):
    try:
        return crud.list_players(position)
    except OperationalError:
        raise HTTPException(status_code=500, detail="Error al consultar la base de datos")