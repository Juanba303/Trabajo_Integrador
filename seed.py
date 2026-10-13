from sqlalchemy import select
from db import Game, Player, Team, create_tables, get_session

create_tables()

def init_db():
    with get_session() as s:
        if s.scalars(select(Team)).first() is None:
            boca = Team(name="Boca Juniors", city="Buenos Aires")
            river = Team(name="River Plate", city="Buenos Aires")
            estudiantes = Team(name="Estudiantes RC", city="Río Cuarto")
            talleres = Team(name="Talleres", city="Córdoba")
            belgrano = Team(name="Belgrano", city="Córdoba")
            barcelona = Team(name="Barcelona", city="Barcelona")
            real_madrid = Team(name="Real Madrid", city="Madrid")
            ac_milan = Team(name="AC Milan", city="Milan")
            inter_milan = Team(name="Inter Milan", city="Milan")
            atletico_madrid = Team(name="Atlético Madrid", city="Madrid")

            s.add_all([boca, river, estudiantes, talleres, belgrano, barcelona, real_madrid, ac_milan, inter_milan, atletico_madrid])
            s.commit()

            s.add_all([
                Player(name="Juan Ibarra", team_id=boca.id, position="Extremo Derecho", goals=5),
                Player(name="Lucas Benítez", team_id=boca.id, position="Defensor Central", goals=2),
                Player(name="Enzo Radamel", team_id=river.id, position="Mediocampista", goals=6),
                Player(name="Mateo Quintero", team_id=river.id, position="Delantero", goals=9),
                Player(name="Pedro Gonzales", team_id=estudiantes.id, position="Delantero", goals=14),
                Player(name="Ignacio Cabrera", team_id=estudiantes.id, position="Arquero", goals=0),
                Player(name="Ruben Galoppo", team_id=talleres.id, position="Mediocampista", goals=3),
                Player(name="Facundo Valoyes", team_id=talleres.id, position="Lateral Izquierdo", goals=1),
                Player(name="Rodrigo Giménez", team_id=belgrano.id, position="Delantero", goals=15),
                Player(name="Tomás Longo", team_id=belgrano.id, position="Mediocampista Defensivo", goals=4),
                Player(name="Xavi Rodriguez", team_id=barcelona.id, position="Mediocampista", goals=8),
                Player(name="Lamine Puig", team_id=barcelona.id, position="Extremo Izquierdo", goals=11),
                Player(name="Mesut Ramos", team_id=real_madrid.id, position="Extremo Izquierdo", goals=7),
                Player(name="Federico Carvajal", team_id=real_madrid.id, position="Defensor Central", goals=3),
                Player(name="Rafael Inzaghi", team_id=ac_milan.id, position="Delantero", goals=6),
                Player(name="Gianluigi Tonali", team_id=ac_milan.id, position="Mediocampista", goals=2),
                Player(name="Mauro Giuseppe", team_id=inter_milan.id, position="Delantero", goals=10),
                Player(name="Nicolò Barella", team_id=inter_milan.id, position="Lateral Derecho", goals=1),
                Player(name="José Álvarez", team_id=atletico_madrid.id, position="Mediocampista", goals=4),
                Player(name="Diego Savic", team_id=atletico_madrid.id, position="Delantero", goals=8)
            ])

            s.add_all([
                Game(home_id=boca.id, away_id=river.id, home_goals=2, away_goals=1, matchday=1),
                Game(home_id=talleres.id, away_id=belgrano.id, home_goals=1, away_goals=1, matchday=1),
                Game(home_id=estudiantes.id, away_id=barcelona.id, home_goals=0, away_goals=2, matchday=1),
                Game(home_id=real_madrid.id, away_id=atletico_madrid.id, home_goals=2, away_goals=1, matchday=1),
                Game(home_id=ac_milan.id, away_id=inter_milan.id, home_goals=0, away_goals=1, matchday=1),
                Game(home_id=river.id, away_id=talleres.id, home_goals=2, away_goals=0, matchday=2),
                Game(home_id=belgrano.id, away_id=estudiantes.id, home_goals=3, away_goals=1, matchday=2),
                Game(home_id=barcelona.id, away_id=real_madrid.id, home_goals=3, away_goals=2, matchday=2),
                Game(home_id=atletico_madrid.id, away_id=ac_milan.id, home_goals=1, away_goals=0, matchday=2),
                Game(home_id=inter_milan.id, away_id=boca.id, home_goals=2, away_goals=2, matchday=2),
                Game(home_id=boca.id, away_id=estudiantes.id, home_goals=2, away_goals=0, matchday=3),
                Game(home_id=river.id, away_id=belgrano.id, home_goals=1, away_goals=0, matchday=3),
                Game(home_id=talleres.id, away_id=barcelona.id, home_goals=1, away_goals=3, matchday=3),
                Game(home_id=real_madrid.id, away_id=ac_milan.id, home_goals=2, away_goals=0, matchday=3),
                Game(home_id=inter_milan.id, away_id=atletico_madrid.id, home_goals=1, away_goals=1, matchday=3)
            ])
            s.commit()
            print("Objetos cargados")
        else:
            print("Ya hay objetos cargados")

if __name__ == "__main__":
    init_db()