from sqlalchemy import create_engine, event, ForeignKey, String, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session
from models import Base, Team, Player, Game

DB_FILE = "league.db"

engine = create_engine(f"sqlite:///{DB_FILE}")

@event.listens_for(engine, "connect")
def enable_foreign_keys(con, _):
    "This lets you control foreign keys with SQLite with every execution"
    con.execute("PRAGMA foreign_keys = ON")

def create_tables():
    Base.metadata.create_all(engine)

def get_session() -> Session:
    return Session(engine)

def init_db():
    create_tables()
    with get_session() as s:
        #Important: I made this part with the help of AI, because I couldn't find a way to load data-
        #without having Server Errors
        #Basically, it asks if the first row is empty, if its not, its loads the data
        if s.scalars(select(Team)).first() is None:
            boca = Team(nombre="Boca Juniors", ciudad="Buenos Aires")
            river = Team(nombre="River Plate", ciudad="Buenos Aires")
            estudiantes = Team(nombre="Estudiantes RC", ciudad="Río Cuarto")
            talleres = Team(nombre="Talleres", ciudad="Córdoba")
            belgrano = Team(nombre="Belgrano", ciudad="Córdoba")
            barcelona = Team(nombre="Barcelona", ciudad="Barcelona")
            real_madrid = Team(nombre="Real Madrid", ciudad="Madrid")
            ac_milan = Team(nombre="AC Milan", ciudad="Milan")
            inter_milan = Team(nombre="Inter Milan", ciudad="Milan")
            atletico_madrid = Team(nombre="Atlético Madrid", ciudad="Madrid")

            s.add_all([boca, river, estudiantes, talleres, belgrano, barcelona, real_madrid, ac_milan, inter_milan, atletico_madrid])
            s.commit()

            s.add_all([
                Player(nombre="Juan Ibarra", equipo_id=boca.id, posicion="Extremo Derecho", goles=5),
                Player(nombre="Lucas Benítez", equipo_id=boca.id, posicion="Defensor Central", goles=2),
                Player(nombre="Enzo Radamel", equipo_id=river.id, posicion="Mediocampista", goles=6),
                Player(nombre="Mateo Quintero", equipo_id=river.id, posicion="Delantero", goles=9),
                Player(nombre="Pedro Gonzales", equipo_id=estudiantes.id, posicion="Delantero", goles=14),
                Player(nombre="Ignacio Cabrera", equipo_id=estudiantes.id, posicion="Arquero", goles=0),
                Player(nombre="Ruben Galoppo", equipo_id=talleres.id, posicion="Mediocampista", goles=3),
                Player(nombre="Facundo Valoyes", equipo_id=talleres.id, posicion="Lateral Izquierdo", goles=1),
                Player(nombre="Rodrigo Giménez", equipo_id=belgrano.id, posicion="Delantero", goles=15),
                Player(nombre="Tomás Longo", equipo_id=belgrano.id, posicion="Mediocampista Defensivo", goles=4),
                Player(nombre="Xavi Rodriguez", equipo_id=barcelona.id, posicion="Mediocampista", goles=8),
                Player(nombre="Lamine Puig", equipo_id=barcelona.id, posicion="Extremo Izquierdo", goles=11),
                Player(nombre="Mesut Ramos", equipo_id=real_madrid.id, posicion="Extremo Izquierdo", goles=7),
                Player(nombre="Federico Carvajal", equipo_id=real_madrid.id, posicion="Defensor Central", goles=3),
                Player(nombre="Rafael Inzaghi", equipo_id=ac_milan.id, posicion="Delantero", goles=6),
                Player(nombre="Gianluigi Tonali", equipo_id=ac_milan.id, posicion="Mediocampista", goles=2),
                Player(nombre="Mauro Giuseppe", equipo_id=inter_milan.id, posicion="Delantero", goles=10),
                Player(nombre="Nicolò Barella", equipo_id=inter_milan.id, posicion="Lateral Derecho", goles=1),
                Player(nombre="José Álvarez", equipo_id=atletico_madrid.id, posicion="Mediocampista", goles=4),
                Player(nombre="Diego Savic", equipo_id=atletico_madrid.id, posicion="Delantero", goles=8)
            ])

            s.add_all([
            Game(local_id=boca.id, visitante_id=river.id, goles_local=2, goles_visitante=1, fecha=1),
                Game(local_id=talleres.id, visitante_id=belgrano.id, goles_local=1, goles_visitante=1, fecha=1),
                Game(local_id=estudiantes.id, visitante_id=barcelona.id, goles_local=0, goles_visitante=2, fecha=1),
                Game(local_id=real_madrid.id, visitante_id=atletico_madrid.id, goles_local=2, goles_visitante=1, fecha=1),
                Game(local_id=ac_milan.id, visitante_id=inter_milan.id, goles_local=0, goles_visitante=1, fecha=1),
                Game(local_id=river.id, visitante_id=talleres.id, goles_local=2, goles_visitante=0, fecha=2),
                Game(local_id=belgrano.id, visitante_id=estudiantes.id, goles_local=3, goles_visitante=1, fecha=2),
                Game(local_id=barcelona.id, visitante_id=real_madrid.id, goles_local=3, goles_visitante=2, fecha=2),
                Game(local_id=atletico_madrid.id, visitante_id=ac_milan.id, goles_local=1, goles_visitante=0, fecha=2),
                Game(local_id=inter_milan.id, visitante_id=boca.id, goles_local=2, goles_visitante=2, fecha=2),
                Game(local_id=boca.id, visitante_id=estudiantes.id, goles_local=2, goles_visitante=0, fecha=3),
                Game(local_id=river.id, visitante_id=belgrano.id, goles_local=1, goles_visitante=0, fecha=3),
                Game(local_id=talleres.id, visitante_id=barcelona.id, goles_local=1, goles_visitante=3, fecha=3),
                Game(local_id=real_madrid.id, visitante_id=ac_milan.id, goles_local=2, goles_visitante=0, fecha=3),
                Game(local_id=inter_milan.id, visitante_id=atletico_madrid.id, goles_local=1, goles_visitante=1, fecha=3)
            ])
            s.commit()