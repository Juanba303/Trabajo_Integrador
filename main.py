from fastapi import FastAPI, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import OperationalError
from models import Team, Player, Game
import seed

app = FastAPI()

#Initialize tables and seed without duplicating data after rebooting
seed.init_db()

@app.get("/equipos")
#This endpoint shows all teams in the league
def get_teams():
    try:
        with seed.get_session() as s:
            teams = s.scalars(select(Team)).all()
            return [team.to_dict() for team in teams]
    except OperationalError:
        raise HTTPException(status_code=500, detail="Error al consultar la base de datos")

@app.get("/equipos/{id}/jugadores")
#This endpoint shows every player on a team based on it's ID
def get_players_by_team_id(id: int):
    try:
        with seed.get_session() as s:
            players = s.scalars(select(Player).where(Player.equipo_id == id)).all()
            return [player.to_dict() for player in players]
    except OperationalError:
        raise HTTPException(status_code=500, detail="Error al consultar la base de datos")

@app.get("/partidos")
#This endpoint shows all the games already played
def get_games():
    try:
        with seed.get_session() as s:
            games = s.scalars(select(Game)).all()
            return [game.to_dict() for game in games]
    except OperationalError:
        raise HTTPException(status_code=500, detail="Error al consultar la base de datos")


#@app.get("/tabla")


#@app.get("/goleadores")


#@app.post("/partidos")