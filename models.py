from sqlalchemy import create_engine, event, ForeignKey, String, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session

class Base(DeclarativeBase):
    "Inherited class by every table"
    pass

    def to_dict(self) -> dict:
        return {"id": self.id, "local_id": self.local_id, "visitante_id": self.visitante_id, "goles_local": self.goles_local, "goles_visitante": self.goles_visitante, "fecha": self.fecha}

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