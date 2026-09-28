from fastapi import FastAPI, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import OperationalError
import seed

app = FastAPI()

#Initialize tables and seed without duplicating data after rebooting
seed.init_db()

@app.get("/equipos")
def obtener_equipos():
    try:
        with seed.get_session() as s:
            teams = s.scalars(select(seed.Team)).all()
            return [team.to_dict() for team in teams]
    except OperationalError:
        raise HTTPException(status_code=500, detail="Error al consultar la base de datos")