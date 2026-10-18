from sqlalchemy import exists, or_
from sqlalchemy.orm import Session
from db import Team, Match


def validate_match(data: dict, partial: bool = False, db: Session = None) -> dict:
    clean = {}

    ## Validate home_id
    home_id = data.get("home_id")
    if not isinstance(home_id, int) or isinstance(home_id, bool):
        raise ValueError("home_id is obligatory and must be an integer")
    clean["home_id"] = home_id

    ## Validate away_id
    away_id = data.get("away_id")
    if not isinstance(away_id, int) or isinstance(away_id, bool):
        raise ValueError("away_id is obligatory and must be an integer")
    clean["away_id"] = away_id

    ## Validate that teams don't play against themselves
    home = clean.get("home_id")
    away = clean.get("away_id")
    if home is not None and away is not None:
        if home == away:
            raise ValueError("A team can't play against itself")

    ## Validate home_goals
    home_goals = data.get("home_goals")
    if not isinstance(home_goals, int) or isinstance(home_goals, bool):
        raise ValueError("home_goals is obligatory and must be an integer")
    if home_goals < 0:
        raise ValueError("home_goals can't be negative")
    clean["home_goals"] = home_goals

    ## Validate away_goals
    away_goals = data.get("away_goals")
    if not isinstance(away_goals, int) or isinstance(away_goals, bool):
        raise ValueError("away_goals is obligatory and must be an integer")
    if away_goals < 0:
        raise ValueError("away_goals can't be negative")
    clean["away_goals"] = away_goals

    ## Validate matchday
    matchday = data.get("matchday")
    if not isinstance(matchday, int) or isinstance(matchday, bool):
        raise ValueError("matchday is obligatory and must be an integer")
    if matchday < 1:
        raise ValueError("matchday must be greater than or equal to 1")

    ## Validate maximum matchday limit
    teams = db.query(Team).count()
    if teams > 0:
        max_matchdays = (teams * 2) - 2
        if matchday > max_matchdays:
            raise ValueError(
                f"Matchday {matchday} exceeds the maximum allowed ({max_matchdays})"
                )

    clean["matchday"] = matchday

    ## Check if any of the two teams already has a match scheduled on the matchday
    if "matchday" in clean and "home_id" in clean and "away_id" in clean:
        matchday_exists = db.query(exists().where(Match.matchday == clean["matchday"], or_(
            Match.home_id == clean["home_id"],
            Match.away_id == clean["home_id"],
            Match.home_id == clean["away_id"],
            Match.away_id == clean["away_id"],
            ),
            )
        ).scalar()
        if matchday_exists:
            raise ValueError(
                "One or both teams already have a match scheduled for this matchday"
            )

    ## From this part, I started using exists() method because it was easier to search for data in queries
    if db is not None:
        ## Check if home team exists
        if "home_id" in clean:
            home_exists = db.query(
                exists().where(Team.id == clean["home_id"])
            ).scalar()
            if not home_exists:
                raise ValueError(
                    f"Home team with ID {clean['home_id']} doesn't exist"
                )

        ## Check if away team exists
        if "away_id" in clean:
            away_exists = db.query(
                exists().where(Team.id == clean["away_id"])
            ).scalar()
            if not away_exists:
                raise ValueError(
                    f"Away team with ID {clean['away_id']} doesn't exist"
                )

        ## Check if the match already exists in this home/away order
        if "home_id" in clean and "away_id" in clean:
            match_exists = db.query(
                exists().where(
                    Match.home_id == clean["home_id"],
                    Match.away_id == clean["away_id"],
                )
            ).scalar()
            if match_exists:
                raise ValueError(
                    "A match between these two teams with this home/away order already exists"
                )

    return clean