# Comentarios de la cátedra

Informática (TDS05) · Proyecto Integrador · UM Río Cuarto

Acá va la devolución de cada revisión semanal. Léelo antes de seguir programando.
Primero está el alcance completo del proyecto; al final, la devolución de cada semana.

**Grupo:** Juan Ficco
**Tema:** Liga de fútbol

---

# Alcances de este proyecto

Esto es lo que hay que entregar. Lo que no está acá, no se pide.

## Reglas comunes a todos los grupos

### Stack
- Python + **FastAPI** + Uvicorn.
- Datos en **SQLite**. Pueden usar **SQLAlchemy** (ORM, con la guía [guias/sqlalchemy_orm.md](guias/sqlalchemy_orm.md)) o **`sqlite3` con SQL directo**: las dos formas valen. **Pydantic es opcional**: el cuerpo del `POST` se puede validar con un modelo de Pydantic (`class StudentIn(BaseModel)`) o a mano en `validation.py`. Las dos formas valen.
- Repositorio en GitHub con commits de **todos** los integrantes.
- **Demo local:** la API se corre en la notebook de cada grupo con `uvicorn`. No hace falta desplegarla en la web (ver *Demo local*, abajo).

### Nombres en el código (criterio acordado con la cátedra de Inglés)

> **Actualizado el 15/10:** los nombres de tablas, columnas y rutas en inglés pasan a ser una **recomendación**. Si quedan en español, no es un error.

- **Variables, funciones y clases en inglés**: `list_students`, `get_session`, `class Student(Base)`.
- **Tablas, columnas, rutas y query params:** se recomienda que también vayan en inglés (`__tablename__ = "students"`, columna `career_id`, ruta `GET /students`), pero pueden quedar en español, como figuran en el alcance.
- Lo que sí es obligatorio: usar **el mismo nombre en todos los archivos** (`models.py`, `seed.py`, `crud.py`, `main.py`, `validation.py`). Si la tabla se llama `estudiantes` en el seed, se llama `estudiantes` en todos lados.
- **Documentación en inglés**: `README.md`, docstrings y los mensajes que devuelve la API.
- **Comentarios**: pueden estar en español mientras desarrollan, pero para la **entrega final** tienen que estar en inglés.

### Demo local (sin despliegue)

> **Actualizado el 15/10:** no se despliega a producción. La defensa es **local**, en la notebook del grupo.

`requirements.txt` debe incluir:
```
fastapi
uvicorn
python-dotenv
```
y `sqlalchemy` si lo usan.

Para levantar el proyecto desde cero (lo mismo tiene que estar en el README):
```
python -m venv venv
venv\Scripts\activate          (en Linux/Mac: source venv/bin/activate)
pip install -r requirements.txt
python seed.py
uvicorn main:app --reload
```
Y abrir http://127.0.0.1:8000/docs.

- El seed se corre **una vez, antes** de levantar el servidor. No va adentro de `main.py`.
- Antes de la defensa, prueben todo esto en la notebook con la que van a presentar.

### Base de datos
- **3 tablas**, cada una con clave primaria (`id`).
- Al menos **1 relación** entre tablas (clave foránea, ej. `equipo_id`).
- **Algunos datos de ejemplo** en cada tabla, los suficientes para ver funcionar los endpoints. No hay mínimo ni máximo. Siempre **datos ficticios**.
- Recomendación: que los datos permitan ver los filtros en acción, por ejemplo productos de varias categorías, para que `?category=` devuelva algo distinto de la lista completa.
- Un script de carga inicial `seed.py` que crea las tablas (con `create_all` o con `CREATE TABLE IF NOT EXISTS`) y carga los datos **solo si la base está vacía**. Se ejecuta antes de levantar el servidor y, si se corre dos veces, no duplica nada.
- El archivo `.db` **puede estar en el repo**. Si lo suben, que esté actualizado (el que genera el seed actual).

### Seguridad: TODOS los endpoints van protegidos

> **Actualizado el 15/10:** se **recomienda** guardar la clave en una variable de entorno en lugar de escribirla en el código. No es obligatorio; en la defensa se puede preguntar por qué conviene hacerlo.

- Todos los endpoints piden la API key en el encabezado `X-API-Key`.
- Sin clave o con clave incorrecta → **401**. Con la clave correcta → **200** y los datos.
- **Recomendado:** guardar la clave en un archivo **`.env`** que **no se sube** (va en el `.gitignore`) y leerla con `python-dotenv`. Al repo se sube un **`.env.example`** con el nombre de la variable y sin el valor. Paso a paso en [guias/variables_de_entorno.md](guias/variables_de_entorno.md). Si la dejan como constante en `security.py`, también vale.
- Los datos son todos **ficticios**: esta API no se usa para nada real.

`security.py` con la clave en el `.env` (la forma recomendada):

```python
import os

from dotenv import load_dotenv
from fastapi import Depends, HTTPException
from fastapi.security import APIKeyHeader

load_dotenv()
API_KEY = os.getenv("API_KEY")
header = APIKeyHeader(name="X-API-Key")


def verify_api_key(key: str = Depends(header)):
    if API_KEY is None or key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
```

Y en `main.py` se protege toda la app de una vez:

```python
app = FastAPI(dependencies=[Depends(verify_api_key)])
```

En `/docs` usá el botón **Authorize** para cargar la clave y probar.
---

## Nivel A — obligatorio (igual para todos)

Cada grupo implementa **exactamente estos 6 endpoints**, adaptados a su tema (ver *Alcance de este grupo*):

| # | Tipo | Ejemplo genérico | Qué practica |
|---|---|---|---|
| 1 | Listado con filtro | `GET /cosas?campo=valor` | Query param y filtro en la consulta |
| 2 | Detalle | `GET /cosas/{id}` | Path param, **404** si no existe |
| 3 | Relación | `GET /cosas/{id}/otras` | Cruzar dos tablas por la clave foránea |
| 4 | Segundo listado con filtro | `GET /otras?campo=valor` | Query param sobre otra tabla |
| 5 | Calculado | `GET /resumen` | Contar, sumar o agrupar (en Python o en la consulta) |
| 6 | Alta | `POST /cosas` | Recibir el cuerpo (con un modelo de Pydantic o como `dict` validado a mano), rechazar los datos inválidos con **400** o **422**, e insertar en la base |

Además, en Nivel A:
- **Errores:** 401 (sin clave), 404 (no existe), y la API no se cae si la base no está o falla una consulta (`try/except`).
- **Filtros opcionales:** si no se manda el query param, devuelve todo.
- **Seguridad (recomendado):** API key en variable de entorno (`.env`) en lugar de escrita en el código.
- **README:** qué hace la API, lista de endpoints, cómo usar la API key, cómo correrla localmente, y declaración de uso de IA si la usaron.

## Nivel B — opcional

Existe un Nivel B que suma hasta 1 punto sobre la nota final. **No se preocupen por eso todavía:** lo vemos en clase más adelante, cuando el Nivel A esté andando.

---

## Alcance de este grupo

### Grupo 5 · Liga de fútbol
**Integrantes:** Juan Ficco

**Tablas**
- `equipos`: id, nombre, ciudad
- `jugadores`: id, nombre, posicion, goles, equipo_id (FK)
- `partidos`: id, fecha, local_id (FK), visitante_id (FK), goles_local, goles_visitante

**Endpoints Nivel A**
1. `GET /partidos?equipo_id=2`
2. `GET /equipos/{id}`
3. `GET /equipos/{id}/jugadores`
4. `GET /jugadores?posicion=delantero`
5. `GET /tabla` → tabla de posiciones **calculada** a partir de los partidos (Pts, PJ, PG, PE, PP)
6. `POST /partidos`


---

## Fuera de alcance (para todos)

No se pide y **no suma**:
- Frontend o páginas web.
- Login de usuarios, registro, JWT.
- Bases de datos externas (PostgreSQL, MySQL, etc.).
- Docker.
- Integración con IA o con el chatbot (eso corresponde a Análisis de Sistemas).
- Pagos, facturación, envío de mails, hardware real.

## Entregables

1. Repositorio GitHub: `main.py`, script de seed, `requirements.txt`, `README.md`, commits de todos.
2. Video demo (máx. 5 min): endpoints funcionando con clave, y un pedido **sin** clave mostrando el 401.
3. Defensa oral el **miércoles 28/10**: demo en vivo desde `/docs`, en local, y preguntas sobre el código. El repositorio tiene que estar al día el **miércoles 21/10**.

---

# Devolución semanal

## 23/09

**📌 Novedad:** la base se maneja con **SQLAlchemy** (ORM) y **sin Pydantic**; las validaciones del `POST` van a mano. Hay una guía con ejemplo completo en [guias/sqlalchemy_orm.md](guias/sqlalchemy_orm.md) y el código en `guias/pokedex/`. Agreguen `sqlalchemy` a `requirements.txt`.

**Lo que hay:** el repo recién creado, con un README de una línea. Llegó tarde respecto del resto de los grupos, así que hay que arrancar ya.

**A corregir**
- El repo está en **privado**. Ponelo en público (Settings → General → Change visibility) para que se pueda corregir sin invitaciones.
- El README tiene que explicar qué hace la API, la lista de endpoints y cómo correrla.

**Próximos pasos**
1. `main.py` con FastAPI levantando y `/docs` abriendo.
2. `seed.py` con las 3 tablas: `equipos`, `jugadores` (con `equipo_id`) y `partidos` (con `local_id` y `visitante_id`).
3. Cargá unos 10 registros por tabla: con 4 o 5 equipos y varios partidos ya se arma una tabla de posiciones interesante.

**Lo importante de tu tema:** la tabla de posiciones **no se guarda**, se calcula recorriendo los partidos y contando 3 puntos por ganado y 1 por empatado. Ese es el endpoint que más se va a mirar en la defensa.

## 24/09

**📌 Criterio de nombres.** Variables, funciones y clases en **inglés**; tablas, columnas y rutas como en el alcance; comentarios en inglés para la entrega final. Está detallado arriba en *Reglas comunes* y la guía ya lo aplica.

**Lo que hay:** sin cambios. El repo sigue con un README de una línea.

Todos los demás grupos ya tienen código o base de datos. Estás quedando atrás y el calendario no espera: el 30/09 la meta son los endpoints 1 a 3.

**Próximos pasos (urgente)**
1. `main.py` con `app = FastAPI()` y un endpoint que devuelva JSON. Probalo con `uvicorn main:app --reload` y `/docs`.
2. `seed.py` con **SQLAlchemy** (ver [guias/sqlalchemy_orm.md](guias/sqlalchemy_orm.md)): `equipos`, `jugadores` (con `equipo_id`) y `partidos` (con `local_id` y `visitante_id`), ~10 registros por tabla.
3. `requirements.txt` con `fastapi`, `uvicorn`, `uvicorn-worker`, `gunicorn`, `sqlalchemy`.

## 08/10

**📌 Cambio de criterio: todo en inglés.** Ahora también las **tablas, columnas, rutas y query params** van en inglés, igual que el README, los docstrings y los mensajes de la API. Reemplaza lo dicho el 24/09; está detallado arriba en *Nombres en el código*. El alcance sigue listando los nombres en español solo como referencia.

**📌 Guía nueva (opcional):** [guias/variables_de_entorno.md](guias/variables_de_entorno.md), para sacar la clave del código con un `.env`.

**Lo que hay:** arrancaste y avanzaste bien. 👍 Probé la API: `GET /equipos`, `GET /equipos/{id}/jugadores` y `GET /partidos` funcionan. Usás SQLAlchemy con sesión, separaste los modelos en `models.py`, el seed carga 10 equipos, 20 jugadores y 15 partidos sin duplicar, atrapás el error de base con `try/except` y el README en inglés describe el proyecto. Bien también por dejar escrito que usaste IA en el seed: pasá esa declaración al README, que es donde se pide.

**⚠️ La API no tiene clave.** Todos los endpoints responden sin `X-API-Key`. Es obligatorio y es lo primero que se prueba en la defensa. El código está arriba en *Seguridad*: son 8 líneas y protege toda la app de una vez.

**Cómo estás contra los 6 endpoints del alcance**

| # | Alcance | Estado |
|---|---|---|
| 1 | `GET /partidos?equipo_id=2` | Está el listado, **falta el filtro**: con `?equipo_id=2` devuelve los 15 partidos. Tiene que traer los que jugó ese equipo, de local **o** de visitante |
| 2 | `GET /equipos/{id}` | Falta |
| 3 | `GET /equipos/{id}/jugadores` | ✅ Funciona |
| 4 | `GET /jugadores?posicion=delantero` | Falta |
| 5 | `GET /tabla` | Falta |
| 6 | `POST /partidos` | Falta |

`GET /equipos` y `GET /goleadores` no están en el alcance. Podés dejarlos, pero no cuentan: primero los seis de la tabla.

**A corregir en el código**
- `python seed.py` **no carga nada**: el archivo define `init_db()` pero nunca la llama. Hoy funciona porque `main.py` la ejecuta al importarse, y eso es justo lo que hay que evitar: en Render corren 2 workers y cada uno cargaría los datos. Sacá `seed.init_db()` de `main.py` y agregá al final de `seed.py`:
  ```python
  if __name__ == "__main__":
      init_db()
  ```
- En `models.py`, el `to_dict` de los partidos quedó adentro de `Base` en vez de adentro de `Game`. Anda de casualidad, porque `Game` lo hereda. Movelo a `Game`.
- `GET /equipos/999/jugadores` devuelve `[]`. Si el equipo no existe tiene que dar **404**.
- El `engine` y `get_session` están en `seed.py`. Van en `db.py` (o en `models.py`), así `main.py` no depende del seed.
- **Nombres en inglés** (criterio nuevo). Clases y funciones ya están bien; faltan tablas, columnas y rutas: `teams`, `players`, `matches`; `name`, `city`, `position`, `goals`, `team_id`, `home_id`, `away_id`, `home_goals`, `away_goals`; y `/teams`, `/players`, `/matches`, `/standings`. La columna `fecha` guarda el número de fecha del torneo: en inglés es `matchday`, no `date`.

**A corregir en el repo**
- No hay `.gitignore`: `league.db` y `__pycache__/` están subidos. Creá el archivo con `*.db` y `__pycache__/`, y sacalos con `git rm --cached league.db -r __pycache__`.
- El README lista `/goleadores` y le faltan `/equipos/{id}` y `/jugadores`. Que coincida con los seis del alcance.

**Sobre `GET /tabla`:** es el endpoint que más se va a mirar. No se guarda nada: recorrés los partidos y, por cada uno, sumás a cada equipo un partido jugado y 3, 1 o 0 puntos según el resultado. Un diccionario con el `id` del equipo como clave alcanza. Al final ordenás por puntos.

**Próximos pasos**
1. Agregar la API key y probar el 401 en `/docs`.
2. Arreglar el seed (`if __name__`) y el `to_dict` de `Game`.
3. Pasar tablas, columnas y rutas a inglés. Conviene hacerlo ahora, antes de escribir los endpoints que faltan.
4. Endpoints 1 (filtro), 2 y 4, que son los más simples. Después `/tabla` y el `POST`.

## 15/10

**📌 Cambios en las reglas** (están arriba, en *Reglas comunes*):
- **SQLAlchemy es opcional:** también vale `sqlite3` con SQL directo.
- **No hay que desplegar.** La defensa es **local**, en su notebook, el **miércoles 28/10**. El repo tiene que estar al día el **miércoles 21/10**.
- **Recomendado:** la API key en una variable de entorno (`.env`) en lugar de escrita en el código. No es obligatorio, pero en la defensa se puede preguntar dónde está la clave y por qué conviene sacarla del código.

**Lo que hay:** muy buen avance. 👍 Probé la API y funcionan `GET /games?team_id=` (trae los partidos de local **y** de visitante), `GET /teams/{id}` con 404, `GET /players?position=` y `GET /table`. Recalculé la tabla a mano y coincide en puntos, PJ, PG, PE, PP y en el orden. La clave anda (401 sin clave o con clave mala). El seed se corre con `python seed.py`, carga 10 + 20 + 15 y no duplica. Sacaste el venv del repo y todo está en inglés. Lo que te marqué el 08/10 del seed está resuelto.

**Lo que falta para la entrega del 21/10:**

1. **Validación del `POST /games`.** `validations.py` está vacío y el JSON va directo a `Game(**data)`. Probé y entran con 201:
   - goles negativos;
   - `true` como gol (se guarda como 1);
   - el mismo equipo de local y de visitante;
   - **goles en texto** (`"dos"`). Después de eso, **`GET /table` da 500** y la tabla queda rota.

   Escribí `validate_game(data)` en `validations.py`: campos obligatorios, enteros y no booleanos, goles >= 0, local distinto de visitante. Que lance `ValueError` con un mensaje claro, y `main.py` lo convierte en 400. Hoy los errores que devuelve el `POST` son el texto crudo de SQLAlchemy, con SQL adentro: eso no se le muestra al usuario.
2. **`GET /teams/999/players` devuelve `[]`.** Tiene que dar 404 si el equipo no existe.
3. **`try/except` en `/teams/{id}` y `/teams/{id}/players`.** Los otros endpoints lo tienen; estos dos dan 500 sin control si falta la base.
4. **README desactualizado.** Lista rutas en español que ya no existen (`/equipos`, `/partidos`, `/tabla`, `/goleadores`), no explica cómo usar la clave y los pasos para correrlo son los de Render. Tiene que tener las rutas reales, el header `X-API-Key`, los pasos con `uvicorn main:app --reload` y la declaración de uso de IA (en el seed dejaste escrito que la usaste).

**Recomendación:** pasar la clave a un `.env` (ver *Seguridad*, arriba, y [guias/variables_de_entorno.md](guias/variables_de_entorno.md)). No es obligatorio, pero en la defensa se puede preguntar dónde está la clave y por qué conviene sacarla del código.

**Más chico:**
- En `crud.py:50`, el `if` que controla que los dos equipos existan solo cubre las dos primeras líneas; el resto del cálculo quedó afuera por la indentación.
- La clase es `Game`, la tabla `matches` y la ruta `/games`. Elegí un nombre (por ejemplo, todo `matches`).
- Quedan en español `CLAVE`, `verificar`, los mensajes de error y los `print` del seed.
