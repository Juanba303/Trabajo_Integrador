# Guía · Consultas que cruzan varias tablas

Informática (TDS05) · Universidad de Mendoza · Sede Río Cuarto

Esta guía es para tu proyecto. El problema: `GET /matches` devuelve `home_id: 1` y `away_id: 2`, y vos querés que además diga **"Boca Juniors"** y **"River Plate"**. Los nombres están en otra tabla (`teams`), así que hay que cruzarlas.

Hay dos formas de hacerlo con SQLAlchemy. La primera es la más simple y es la que te recomiendo.

> **Sobre los nombres.** Los ejemplos ya usan los nombres en inglés que te pedí en la devolución del 08/10. Equivalencias con lo que tenés hoy: `equipos` → `teams`, `partidos` → `matches`, `local_id` → `home_id`, `visitante_id` → `away_id`, `goles_local` → `home_goals`, `goles_visitante` → `away_goals`, `fecha` → `matchday`.

---

## 1. La idea: `relationship`

Una `relationship` es un atributo que te lleva de un objeto al objeto relacionado. No es una columna: no se guarda nada nuevo en la base. SQLAlchemy hace la consulta a la otra tabla cuando lo usás.

Ya tenés una en `Player`:

```python
class Player(Base):
    ...
    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"))

    team: Mapped["Team"] = relationship()
```

Con eso, `player.team` es el objeto `Team` completo, y `player.team.name` es el nombre del equipo.

## 2. Tu caso: dos claves foráneas a la misma tabla

Un partido apunta **dos veces** a `teams`: el local y el visitante. Si escribís `relationship()` a secas, SQLAlchemy no sabe cuál de las dos claves usar y falla con `AmbiguousForeignKeysError`.

La solución es decirle cuál, con `foreign_keys`:

```python
class Game(Base):
    __tablename__ = "matches"

    id: Mapped[int] = mapped_column(primary_key=True)
    matchday: Mapped[int]
    home_id: Mapped[int] = mapped_column(ForeignKey("teams.id"))
    away_id: Mapped[int] = mapped_column(ForeignKey("teams.id"))
    home_goals: Mapped[int]
    away_goals: Mapped[int]

    home_team: Mapped["Team"] = relationship(foreign_keys=[home_id])
    away_team: Mapped["Team"] = relationship(foreign_keys=[away_id])

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "matchday": self.matchday,
            "home_id": self.home_id,
            "home_team": self.home_team.name,
            "away_id": self.away_id,
            "away_team": self.away_team.name,
            "home_goals": self.home_goals,
            "away_goals": self.away_goals,
        }
```

Son dos líneas nuevas en la clase y dos en el `to_dict`. No hay que tocar la base ni el seed.

La consulta queda **igual que antes**:

```python
def list_games() -> list[dict]:
    with get_session() as s:
        games = s.scalars(select(Game).order_by(Game.matchday))
        return [game.to_dict() for game in games]
```

Y la respuesta ahora trae los nombres:

```json
{"id": 1, "matchday": 1, "home_id": 1, "home_team": "Boca Juniors",
 "away_id": 2, "away_team": "River Plate", "home_goals": 2, "away_goals": 1}
```

> **Cuidado:** el `to_dict()` tiene que llamarse **adentro** del `with`. Afuera la sesión ya está cerrada y `game.home_team` da `DetachedInstanceError`.

## 3. Filtrar por una condición **o** la otra

Tu endpoint 1 es `GET /matches?team_id=2`: los partidos de un equipo, jugando de local **o** de visitante. Dos `.where()` seguidos se combinan con *y*; para el *o* está `or_`:

```python
from sqlalchemy import select, or_


def list_games(team_id: int | None = None) -> list[dict]:
    with get_session() as s:
        query = select(Game).order_by(Game.matchday)
        if team_id is not None:
            query = query.where(or_(Game.home_id == team_id, Game.away_id == team_id))
        return [game.to_dict() for game in s.scalars(query)]
```

| Quiero... | Se escribe |
|---|---|
| A **y** B | `.where(A).where(B)` o `.where(A, B)` |
| A **o** B | `.where(or_(A, B))` |
| Ordenar | `.order_by(Game.matchday)` |
| Ordenar de mayor a menor | `.order_by(Player.goals.desc())` |
| Los primeros 5 | `.limit(5)` |

## 4. La otra forma: `join`

Un `join` trae los datos de las dos tablas en **una sola consulta**. Hace falta cuando querés **filtrar u ordenar por una columna de la otra tabla**, por ejemplo "los partidos donde el local es de Córdoba".

Como `teams` aparece dos veces, hay que darle un apodo a cada aparición con `aliased`:

```python
from sqlalchemy import select
from sqlalchemy.orm import aliased


def list_games_by_home_city(city: str) -> list[dict]:
    home = aliased(Team)
    with get_session() as s:
        query = (
            select(Game)
            .join(home, Game.home_id == home.id)
            .where(home.city == city)
        )
        return [game.to_dict() for game in s.scalars(query)]
```

Se lee así: "traé los partidos, pegándole a cada uno su equipo local, y quedate con los que tienen el local en esa ciudad".

También podés pedir columnas sueltas en vez del objeto entero. Ahí cada fila es una tupla y se recorre con `s.execute`:

```python
def list_games_with_names() -> list[dict]:
    home = aliased(Team)
    away = aliased(Team)
    query = (
        select(Game, home.name, away.name)
        .join(home, Game.home_id == home.id)
        .join(away, Game.away_id == away.id)
    )
    with get_session() as s:
        result = []
        for game, home_name, away_name in s.execute(query):
            result.append({
                "id": game.id,
                "home_team": home_name,
                "away_team": away_name,
                "home_goals": game.home_goals,
                "away_goals": game.away_goals,
            })
        return result
```

Da el mismo resultado que la sección 2, con más código. Por eso para mostrar los nombres te conviene la `relationship`.

## 5. ¿Cuál uso?

| Situación | Usá |
|---|---|
| Mostrar un dato de la tabla relacionada (el nombre del equipo) | `relationship` (sección 2) |
| Filtrar por una columna de la misma tabla (`home_id`, `matchday`) | `.where()` (sección 3) |
| Filtrar u ordenar por una columna de **otra** tabla (la ciudad del local) | `join` (sección 4) |

Para los seis endpoints del alcance alcanza con las secciones 2 y 3. `GET /standings` no necesita ningún `join`: recorre los partidos con un `for` y va sumando puntos en un diccionario.

---

## Errores comunes

- **`AmbiguousForeignKeysError`.** Hay dos claves a la misma tabla y falta `foreign_keys=[...]` en la `relationship`.
- **`DetachedInstanceError`.** Usaste `game.home_team` fuera del `with`. Convertí a dict adentro.
- **`ForeignKey("Team.id")`.** Va el nombre de la **tabla** (`"teams.id"`), no el de la clase.
- **`or` de Python en vez de `or_`.** `Game.home_id == 2 or Game.away_id == 2` no da error, pero filtra solo por la primera condición.
- **`join` sin `aliased` cuando la tabla aparece dos veces.** SQLAlchemy no sabe a cuál de las dos te referís.
- **`s.scalars()` con varias columnas.** `scalars` devuelve solo la primera. Si pedís `select(Game, home.name)`, recorré con `s.execute()`.
