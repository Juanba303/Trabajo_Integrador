from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.exc import OperationalError
from fastapi.security import APIKeyHeader
import crud

CLAVE = "clave-de-prueba-2026"
header = APIKeyHeader(name="X-API-Key")

def verificar(clave: str = Depends(header)):
    if clave != CLAVE:
        raise HTTPException(status_code=401, detail="API key invalida")

app = FastAPI(dependencies=[Depends(verificar)])

@app.get("/games")
def list_games(team_id: int | None = None):
    try:
        return crud.list_games(team_id)
    except OperationalError:
        raise HTTPException(status_code=500, detail="Error al consultar la base de datos")

@app.get("/teams/{id}")
def get_team_by_id(id: int):
    team = crud.get_team_by_id(id)
    if team is None:
        raise HTTPException(status_code=404, detail="El equipo no existe") 
    return team

@app.get("/teams/{id}/players")
def list_players_by_team_id(id: int):
    players = crud.list_players_by_team_id(id)
    if players is None:
        raise HTTPException(status_code=404, detail="El equipo no existe")
    return players

@app.get("/players")
def list_players(position: str | None = None):
    try:
        return crud.list_players(position)
    except OperationalError:
        raise HTTPException(status_code=500, detail="Error al consultar la base de datos")

@app.get("/table")
def get_table():
    try:
        return crud.get_table()
    except OperationalError:
        raise HTTPException(status_code=500, detail="Error al consultar la base de datos")

@app.post("/games", status_code=201)
def create(data: dict):
    try:
        return crud.create_game(data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))