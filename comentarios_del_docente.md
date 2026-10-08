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
- Datos en **SQLite** usando **SQLAlchemy** (ORM): las tablas se definen como clases de Python y las consultas se hacen con métodos, sin escribir SQL a mano. **No se usa Pydantic**: las validaciones se hacen a mano en Python. Guía con ejemplo completo: [guias/sqlalchemy_orm.md](guias/sqlalchemy_orm.md).
- Repositorio en GitHub con commits de **todos** los integrantes.
- API desplegada **en producción con Gunicorn** en Render, con URL pública y `/docs` funcionando (ver abajo).

### Nombres en el código (criterio acordado con la cátedra de Inglés)

> **Actualizado el 08/10:** ahora va **todo en inglés**, también tablas, columnas y rutas. Reemplaza el criterio del 24/09.

- **Variables, funciones y clases en inglés**: `list_students`, `get_session`, `class Student(Base)`.
- **Tablas, columnas, rutas y query params también en inglés**. Ejemplo: `class Student(Base)` con `__tablename__ = "students"`, columna `career_id` y ruta `GET /students`.
- El alcance de cada grupo lista las tablas y los endpoints en español **solo como referencia**: tradúzcanlos al inglés y usen **el mismo nombre en todos los archivos** (`db.py`, `seed.py`, `main.py`, `validation.py`).
- **Documentación en inglés**: `README.md`, docstrings y los mensajes que devuelve la API.
- **Comentarios**: pueden estar en español mientras desarrollan, pero para la **entrega final** tienen que estar en inglés.

### Despliegue a producción (Render + Gunicorn)

En tu compu desarrollás con `uvicorn main:app --reload`. En producción corre **Gunicorn** como administrador de procesos, con workers de Uvicorn adentro.

> Gunicorn **no funciona en Windows**. Localmente seguí usando `uvicorn`; Gunicorn corre en el servidor (Linux).

`requirements.txt` debe incluir:
```
fastapi
uvicorn
uvicorn-worker
gunicorn
sqlalchemy
```

En Render → **New → Web Service** → conectás el repo, y configurás:

| Campo | Valor |
|---|---|
| Build Command | `pip install -r requirements.txt` |
| Start Command | `python seed.py && gunicorn main:app -k uvicorn_worker.UvicornWorker -w 2 -b 0.0.0.0:$PORT` |

La clave viaja en el código, así que no hay que configurar nada más en Render.

- El seed corre **una sola vez antes** de levantar Gunicorn. Si lo pusieras adentro de `main.py`, cada worker lo ejecutaría por su cuenta y podrían cargar los datos duplicados.
- El plan gratis se duerme tras ~15 min sin uso (la primera visita tarda ~1 min) y su disco se borra al reiniciar: por eso el seed.

### Base de datos
- **3 tablas**, cada una con clave primaria (`id`).
- Al menos **1 relación** entre tablas (clave foránea, ej. `equipo_id`).
- Unos **10 registros de ejemplo** por tabla. Siempre **datos ficticios**.
- Un script de carga inicial `seed.py` que crea las tablas (`create_all`) y carga los datos **si la base está vacía** (ver sección 9 de la guía). Se ejecuta antes de levantar el servidor. En Render el disco se borra al reiniciar: así la API siempre arranca con datos.
- El archivo `.db` **no se sube** a GitHub (agregalo al `.gitignore`); se genera solo.

### Seguridad: TODOS los endpoints van protegidos
- Todos los endpoints piden la API key en el encabezado `X-API-Key`.
- La clave se define como una constante al principio de `main.py`. Más adelante en la carrera van a ver cómo sacarla del código con variables de entorno; por ahora, así.
- Como la clave está a la vista en el repo, **los datos son todos ficticios** y no se usa esta API para nada real.
- Sin clave o con clave incorrecta → **401**.

Se protege toda la app de una vez:

```python
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import APIKeyHeader

CLAVE = "clave-de-prueba-2026"   # clave del grupo
header = APIKeyHeader(name="X-API-Key")

def verificar(clave: str = Depends(header)):
    if clave != CLAVE:
        raise HTTPException(status_code=401, detail="API key invalida")

app = FastAPI(dependencies=[Depends(verificar)])
```

En `/docs` usá el botón **Authorize** para cargar la clave y probar.

---

## Nivel A — obligatorio (igual para todos)

Cada grupo implementa **exactamente estos 6 endpoints**, adaptados a su tema (ver *Alcance de este grupo*):

| # | Tipo | Ejemplo genérico | Qué practica |
|---|---|---|---|
| 1 | Listado con filtro | `GET /cosas?campo=valor` | Query param, `select(...).where(...)` |
| 2 | Detalle | `GET /cosas/{id}` | Path param, **404** si no existe |
| 3 | Relación | `GET /cosas/{id}/otras` | Cruzar dos tablas por la clave foránea (`relationship` o filtro por FK) |
| 4 | Segundo listado con filtro | `GET /otras?campo=valor` | Query param sobre otra tabla |
| 5 | Calculado | `GET /resumen` | Contar, sumar o agrupar (en Python o con `func` de SQLAlchemy) |
| 6 | Alta | `POST /cosas` | Recibir el cuerpo como `dict`, **validar a mano** (400 si está mal) e insertar con la sesión |

Además, en Nivel A:
- **Errores:** 401 (sin clave), 404 (no existe), y la API no se cae si la base no está o falla una consulta (`try/except`).
- **Filtros opcionales:** si no se manda el query param, devuelve todo.
- **Deploy:** URL pública en Render con `/docs` operativo.
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
2. URL pública en Render con `/docs` funcionando.
3. Video demo (máx. 5 min): endpoints funcionando con clave, y un pedido **sin** clave mostrando el 401.
4. Defensa oral: demo en vivo desde `/docs` y preguntas sobre el código.

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
