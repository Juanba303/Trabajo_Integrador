from sqlalchemy import select, or_
from db import Match, Player, Team, get_session
import validations

def list_matches(team_id: int | None = None) -> list[dict]:
    with get_session() as s:
        query = select(Match).order_by(Match.matchday)
        if team_id is not None:
            query = query.where(or_(Match.home_id == team_id, Match.away_id == team_id))
        return [m.to_dict() for m in s.scalars(query)]

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
        matches = s.scalars(select(Match)).all()

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

        for match in matches:
            if match.home_id in standings and match.away_id in standings:
                home = standings[match.home_id]
                away = standings[match.away_id]

                home["played"] += 1
                away["played"] += 1            

                home["goals_for"] += match.home_goals
                home["goals_against"] += match.away_goals
                away["goals_for"] += match.away_goals
                away["goals_against"] += match.home_goals

                if match.home_goals > match.away_goals:
                    home["won"] += 1
                    home["points"] += 3
                    away["lost"] += 1
                elif match.home_goals < match.away_goals:
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

def create_match(data: dict) -> dict:
    with get_session() as s:
        clean = validations.validate_match(data, db=s)
        match = Match(**clean)            
        s.add(match)
        s.commit()
        return match.to_dict()