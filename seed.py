from sqlalchemy import create_engine, event, ForeignKey, String, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session

DB_FILE = "league.db"

engine = create_engine(f"sqlite:///{DB_FILE}")

@event.listens_for(engine, "connect")
def enable_foreign_keys(con, _):
    con.execute("PRAGMA foreign_keys = ON")

class Base(DeclarativeBase):
    pass

class Team(Base):
    __tablename__ = "equipos"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(30), unique=True)
    ciudad: Mapped[str] = mapped_column(String(30))

    def to_dict(self) -> dict:
        return {"id": self.id, "nombre": self.nombre, "ciudad": self.ciudad}

class Player(Base):
    __tablename__ = "jugadores"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(30), unique=True)
    equipo_id: Mapped[int] = mapped_column(ForeignKey("equipos.id"))
    posicion: Mapped[str] = mapped_column(String(30))
    goles: Mapped[int]

    team: Mapped["Team"] = relationship()

    def to_dict(self) -> dict:
        return {"id": self.id, "nombre": self.nombre, "equipo_id": self.equipo_id, "posicion": self.posicion, "goles": self.goles}

class Game(Base):
    __tablename__ = "partidos"

    id: Mapped[int] = mapped_column(primary_key=True)
    local_id: Mapped[int] = mapped_column(ForeignKey("equipos.id"))
    visitante_id: Mapped[int] = mapped_column(ForeignKey("equipos.id"))
    goles_local: Mapped[int]
    goles_visitante: Mapped[int]
    fecha: Mapped[int]

    def to_dict(self) -> dict:
        return {"id": self.id, "local_id": self.local_id, "visitante_id": self.visitante_id, "goles_local": self.goles_local, "goles_visitante": self.goles_visitante, "fecha": self.fecha}

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
                Player(nombre="Enzo Radamel", equipo_id=river.id, posicion="Mediocampista", goles=6),
                Player(nombre="Pedro Gonzales", equipo_id=estudiantes.id, posicion="Delantero", goles=14),
                Player(nombre="Ruben Galoppo", equipo_id=talleres.id, posicion="Mediocampista", goles=3),
                Player(nombre="Rodrigo Giménez", equipo_id=belgrano.id, posicion="Delantero", goles=15),
                Player(nombre="Xavi Rodriguez", equipo_id=barcelona.id, posicion="Mediocampista", goles=8),
                Player(nombre="Mesut Ramos", equipo_id=real_madrid.id, posicion="Extremo Izquierdo", goles=7),
                Player(nombre="Rafael Inzaghi", equipo_id=ac_milan.id, posicion="Delantero", goles=6),
                Player(nombre="Mauro Giuseppe", equipo_id=inter_milan.id, posicion="Delantero", goles=10),
                Player(nombre="José Álvarez", equipo_id=atletico_madrid.id, posicion="Mediocampista", goles=4)
            ])

            s.add_all([
                Game(local_id=boca.id, visitante_id=river.id, goles_local=2, goles_visitante=1, fecha=1),
                Game(local_id=talleres.id, visitante_id=belgrano.id, goles_local=1, goles_visitante=1, fecha=1),
                Game(local_id=estudiantes.id, visitante_id=boca.id, goles_local=0, goles_visitante=2, fecha=1),
                Game(local_id=barcelona.id, visitante_id=real_madrid.id, goles_local=3, goles_visitante=2, fecha=2),
                Game(local_id=ac_milan.id, visitante_id=inter_milan.id, goles_local=0, goles_visitante=1, fecha=2),
                Game(local_id=atletico_madrid.id, visitante_id=barcelona.id, goles_local=1, goles_visitante=1, fecha=2),
                Game(local_id=river.id, visitante_id=talleres.id, goles_local=2, goles_visitante=0, fecha=3),
                Game(local_id=real_madrid.id, visitante_id=atletico_madrid.id, goles_local=2, goles_visitante=1, fecha=3),
                Game(local_id=inter_milan.id, visitante_id=ac_milan.id, goles_local=2, goles_visitante=2, fecha=3),
                Game(local_id=belgrano.id, visitante_id=estudiantes.id, goles_local=3, goles_visitante=1, fecha=3)
            ])
            s.commit()