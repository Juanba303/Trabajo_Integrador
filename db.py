from sqlalchemy import create_engine, event, ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session

DB_FILE = "league.db"

engine = create_engine(f"sqlite:///{DB_FILE}")

@event.listens_for(engine, "connect")
def enable_foreign_keys(con, _):
    """Lets you control Foraign Keys."""
    con.execute("PRAGMA foreign_keys = ON")

class Base(DeclarativeBase):
    """Class inherited by every table"""
    pass

class Team(Base):
    __tablename__ = "teams"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), unique=True)
    city: Mapped[str] = mapped_column(String(30))

    def to_dict(self) -> dict:
        return {"id": self.id, "name": self.name, "city": self.city}

class Player(Base):
    __tablename__ = "players"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), unique=True)
    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"))
    position: Mapped[str] = mapped_column(String(30))
    goals: Mapped[int]

    team: Mapped["Team"] = relationship()

    def to_dict(self) -> dict:
        return {"id": self.id, "name": self.name, "team_id": self.team_id, "position": self.position, "goals": self.goals}

class Game(Base):
    __tablename__ = "matches"

    id: Mapped[int] = mapped_column(primary_key=True)
    home_id: Mapped[int] = mapped_column(ForeignKey("teams.id"))
    away_id: Mapped[int] = mapped_column(ForeignKey("teams.id"))
    home_goals: Mapped[int]
    away_goals: Mapped[int]
    matchday: Mapped[int]

    home_team: Mapped["Team"] = relationship(foreign_keys=[home_id])
    away_team: Mapped["Team"] = relationship(foreign_keys=[away_id])

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "home_id": self.home_id,
            "home_team": self.home_team.name,
            "away_id": self.away_id,
            "away_team": self.away_team.name,
            "home_goals": self.home_goals,
            "away_goals": self.away_goals,
            "matchday": self.matchday,
        }

def create_tables():
    Base.metadata.create_all(engine)

def get_session() -> Session:
    return Session(engine)