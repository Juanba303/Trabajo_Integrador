from sqlalchemy import select, or_
from db import Game, Player, Team, get_session

def list_games(team_id: int | None = None) -> list[dict]:
    with get_session() as s:
        query = select(Game).order_by(Game.matchday)
        if team_id is not None:
            query = query.where(or_(Game.home_id == team_id, Game.away_id == team_id))
        return [g.to_dict() for g in s.scalars(query)]

def list_teams(team_id: int) -> list[dict]:
    with get_session() as s:
        query = select(Team).order_by(Team.id)
        return [t.to_dict() for t in s.scalars(query)]

def get_team_by_id(team_id: int) -> dict | None:
    with get_session() as s:
        team = s.get(Team, team_id)
        return team.to_dict() if team else None

def list_players_by_team_id(team_id: int) -> list[dict]:
    with get_session() as s:
        query = query.where(Player.team == Team.id)
        return [p.to_dict() for p in s.scalars(query)]

def list_players(position: str | None = None) -> list[dict]:
    with get_session() as s:
        query = select(Player)
        if position is not None:
            query = query.where(Player.position == position)
        return [p.to_dict() for p in s.scalars(query)]

def get_table(team_id: int) -> dict | None:
    with get_session() as s:
        query = select(Team).order_by(Team.id)
        return [t.to_dict() for t in s.scalars(query)]