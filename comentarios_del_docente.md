# Comentarios de la cátedra

Informática (TDS05) · Proyecto Integrador · UM Río Cuarto

Acá va la devolución de cada revisión semanal. Léelo antes de seguir programando.
El alcance completo del grupo está en el documento de alcances.

**Grupo:** Juan Ficco
**Tema:** Liga de fútbol

---

## 23/09

**Lo que hay:** el repo recién creado, con un README de una línea. Llegó tarde respecto del resto de los grupos, así que hay que arrancar ya.

**A corregir**
- El repo está en **privado**. Ponelo en público (Settings → General → Change visibility) para que se pueda corregir sin invitaciones.
- El README tiene que explicar qué hace la API, la lista de endpoints y cómo correrla.

**Próximos pasos**
1. `main.py` con FastAPI levantando y `/docs` abriendo.
2. `seed.py` con las 3 tablas: `equipos`, `jugadores` (con `equipo_id`) y `partidos` (con `local_id` y `visitante_id`).
3. Cargá unos 10 registros por tabla: con 4 o 5 equipos y varios partidos ya se arma una tabla de posiciones interesante.

**Lo importante de tu tema:** la tabla de posiciones **no se guarda**, se calcula recorriendo los partidos y contando 3 puntos por ganado y 1 por empatado. Ese es el endpoint que más se va a mirar en la defensa.

**Endpoints a entregar (Nivel A)**
- [ ] `GET /partidos?equipo_id=2`
- [ ] `GET /equipos/{id}` (404 si no existe)
- [ ] `GET /equipos/{id}/jugadores`
- [ ] `GET /jugadores?posicion=delantero`
- [ ] `GET /tabla` (Pts, PJ, PG, PE, PP, calculada desde los partidos)
- [ ] `POST /partidos`
- [ ] Todos protegidos con `X-API-Key` (clave como constante en `main.py`)
