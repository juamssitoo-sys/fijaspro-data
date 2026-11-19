# FijasPro Data

Repositorio independiente para el archivo histórico deportivo de FijasPro.

**Ventana inicial:** 2025-01-01 a 2026-11-19 (ampliable).  
**Deportes:** fútbol y NBA.  
**Estado al 2026-11-19:** 13 archivos fuente importados (3,333 conteos declarados; no normalizados). La cobertura por competición y los bloqueos de licencia están en [docs/COVERAGE.md](docs/COVERAGE.md).

## Objetivo

Conservar datos verificables y trazables de partidos, temporadas, competiciones, equipos y jugadores. No se completan estadísticas ausentes con ceros ni se generan valores ficticios.

## Cobertura de fútbol

Competiciones iniciales identificadas en la configuración del backend FijasPro:
- Premier League
- LaLiga
- Ligue 1
- Brasileirão
- Liga 1 Perú
- Primera División Argentina
- UEFA Champions League
- UEFA Europa League
- UEFA Europa Conference League
- Copa Libertadores
- Copa Sudamericana
- UEFA Nations League

Se ampliará el catálogo cuando la configuración del frontend/backend lo confirme. Las copas nacionales y otras competiciones se incorporarán cuando exista fuente verificable y cobertura suficiente.

## Cobertura NBA

Incluir, cuando estén disponibles:
- Pretemporada
- Temporada regular
- NBA Cup / In-Season Tournament
- Play-In
- Playoffs (todas las rondas)
- All-Star y exhibiciones, identificadas como tales

Se almacenarán partidos, box scores de equipo y jugador, estadísticas por temporada, plantillas/identificadores y metadatos de fase. La disponibilidad real se documentará por fuente y temporada.

## Modelo de datos

Ver [docs/DATA_MODEL.md](docs/DATA_MODEL.md) y [config/competitions.json](config/competitions.json).

Principios:
1. IDs externos conservados como texto.
2. Cada fila lleva fuente, URL/identificador de origen y fecha de captura.
3. Valores no disponibles = null, nunca cero por defecto.
4. Deduplicación por ID del proveedor y claves compuestas de respaldo.
5. Separar temporada, tipo de temporada y fase/round.
6. Mantener datos originales y normalizados separados cuando los términos lo permitan.

## Fuentes evaluadas

Ver [docs/SOURCES.md](docs/SOURCES.md) y [docs/COVERAGE.md](docs/COVERAGE.md). La presencia de un dato en Internet no concede automáticamente derechos para copiarlo, redistribuirlo o usarlo para entrenar modelos. Este repositorio no debe almacenar dumps de proveedores hasta revisar sus condiciones y licencias upstream.

## Estructura prevista

- `data/football/` — particiones por competición/temporada, solo datos autorizados.
- `data/nba/` — particiones por temporada y tipo de partido, solo datos autorizados.
- `config/` — catálogo de competiciones y proveedores.
- `schemas/` — contratos JSON/CSV.
- `scripts/` — ingesta, normalización, validación y reportes de cobertura.
- `docs/` — documentación, fuentes y decisiones.

## Actualización automática de resultados

Requisito funcional: al finalizar cada partido, FijasPro debe recuperar y guardar automáticamente el resultado y las estadísticas disponibles, sin depender de una actualización manual ni de que el usuario mantenga la web abierta. Se implementará mediante webhook oficial o worker de polling en backend, según el proveedor y sus límites. Incluye reintentos, upsert idempotente, reconciliación de correcciones y trazabilidad. Ver [docs/AUTOMATIC_MATCH_UPDATES.md](docs/AUTOMATIC_MATCH_UPDATES.md). Actualmente está documentado, todavía no desplegado.

## Validación antes de conectar FijasPro

No declarar la base completa hasta publicar recuentos por competición, temporada, fase, partidos, jugadores y campos estadísticos; además de duplicados, nulos y última fecha disponible.

## Licencia

El código de este repositorio y los datos deportivos tienen licencias distintas. No se concede una licencia general sobre datos de terceros. Cada dataset deberá incluir su propia atribución y condiciones. No subir claves API, tokens ni credenciales.
