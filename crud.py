from sqlalchemy import select, or_
from db import Game, Player, Team, get_session

def list_games(team_id: int | None = None) -> list[dict]:
    with get_session() as s:
        query = select(Game).order_by(Game.matchday)
        if team_id is not None:
            query = query.where(or_(Game.home_id == team_id, Game.away_id == team_id))
        return [g.to_dict() for g in s.scalars(query)]

def get_team_by_id(team_id: int) -> dict | None:
    with get_session() as s:
        team = s.get(Team, team_id)
        return team.to_dict() if team else None

def list_players_by_team_id(team_id: int) -> list[dict] | None:
    with get_session() as s:
        team = s.get(Team, team_id)
        query = select(Player).where(Player.team_id == team_id)
        return [p.to_dict() for p in s.scalars(query)]

def list_players(position: str | None = None) -> list[dict]:
    with get_session() as s:
        query = select(Player)
        if position is not None:
            query = query.where(Player.position == position)
        return [p.to_dict() for p in s.scalars(query)]

def get_table():
    with get_session() as s:
        teams = s.scalars(select(Team)).all()
        games = s.scalars(select(Game)).all()

        standings = {}

        for team in teams:
            standings[team.id] = {
                "team": team.name,
                "points": 0,
                "played": 0,
                "won": 0,
                "drawn": 0,
                "lost": 0,
                "goals_for": 0,
                "goals_against": 0,
                "goal_difference": 0
            }

        for game in games:
            if game.home_id in standings and game.away_id in standings:
                home = standings[game.home_id]
                away = standings[game.away_id]

            home["played"] += 1
            away["played"] += 1            

            home["goals_for"] += game.home_goals
            home["goals_against"] += game.away_goals
            away["goals_for"] += game.away_goals
            away["goals_against"] += game.home_goals

            if game.home_goals > game.away_goals:
                home["won"] += 1
                home["points"] += 3
                away["lost"] += 1
            elif game.home_goals < game.away_goals:
                away["won"] += 1
                away["points"] += 3
                home["lost"] += 1
            else:
                home["drawn"] += 1
                home["points"] += 1
                away["drawn"] += 1
                away["points"] += 1

        table = []
        for team_id, data in standings.items():
            data["goal_difference"] = data["goals_for"] - data["goals_against"]
            table.append(data)
    
        table.sort(key=lambda x: (x["points"], x["goal_difference"], x["goals_for"]), reverse=True)
        
        return table

def create_game(data: dict) -> dict:
    with get_session() as s:
        game = Game(**data)            
        s.add(game)
        s.commit()
        return game.to_dict()