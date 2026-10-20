from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.exc import OperationalError
from security import verify_api_key
import crud

app = FastAPI(dependencies=[Depends(verify_api_key)])

@app.get("/games")
def list_games(team_id: int | None = None):
    try:
        return crud.list_games(team_id)
    except OperationalError:
        raise HTTPException(status_code=500, detail="Error while consulting database")

@app.get("/teams/{id}")
def get_team_by_id(id: int):
    try:
        if crud.list_players_by_team_id(id) == []:
            raise HTTPException(status_code=404, detail="Team doesn't exist")
        return crud.get_team_by_id(id)
    except OperationalError:
        raise HTTPException(status_code=500, detail="Error while consulting database")

@app.get("/teams/{id}/players")
def list_players_by_team_id(id: int):
    try:
        if crud.list_players_by_team_id(id) == []:
            raise HTTPException(status_code=404, detail="Team doesn't exist")
        return crud.list_players_by_team_id(id)
    except OperationalError:
        raise HTTPException(status_code=500, detail="Error while consulting database")

@app.get("/players")
def list_players(position: str | None = None):
    try:
        return crud.list_players(position)
    except OperationalError:
        raise HTTPException(status_code=500, detail="Error while consulting database")

@app.get("/table")
def get_table():
    try:
        return crud.get_table()
    except OperationalError:
        raise HTTPException(status_code=500, detail="Error while consulting database")

@app.post("/matches", status_code=201)
def create(data: dict):
    try:
        return crud.create_match(data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))