# Modelo de datos normalizado

## Entidades

### competitions
`competition_id`, `sport`, `name`, `country`, `provider_ids`, `gender`, `is_cup`.

### seasons
`season_id`, `competition_id`, `label`, `start_date`, `end_date`, `season_year`.

### matches
`match_id`, `sport`, `competition_id`, `season_id`, `season_type`, `stage`, `round`, `scheduled_at_utc`, `status`, `home_team_id`, `away_team_id`, `home_score`, `away_score`, `venue`, `neutral_site`, `provider`, `provider_match_id`, `source_url`, `captured_at`.

### teams / players
IDs externos como strings; nombres históricos, abreviaturas y vigencia por temporada. No usar nombres como claves primarias.

### team_match_stats / player_match_stats
Una fila por equipo o jugador y partido. Métricas tipadas (puntos/goles, tiros, rebotes, asistencias, pérdidas, faltas, tarjetas, corners, etc.); métricas no disponibles quedan null. Añadir `provider`, `provider_record_id`, `captured_at`.

### player_season_stats / team_season_stats
Estadísticas agregadas de temporada con `season_type` y proveedor explícitos.

## Tipos de temporada y fases

Fútbol: `league`, `cup`, `international`, `friendly`, más fase específica (group, qualifying, round_of_16, quarter_final, semi_final, final, etc.).

NBA `season_type`: `preseason`, `regular_season`, `in_season_tournament`, `play_in`, `playoffs`, `all_star`, `exhibition`.

## Reglas de calidad

- Nunca convertir null en 0.
- Mantener la fecha original y UTC normalizada.
- Registrar prórroga y penales por separado si el proveedor los expone.
- Distinguir marcador al final del tiempo reglamentario y marcador final.
- Para NBA conservar periodo/cuarto y overtime si están disponibles.
- No mezclar estadísticas de temporada regular con playoffs.
- Claves únicas recomendadas: (provider, provider_match_id), y para stats (provider, provider_match_id, provider_entity_id).
- Registrar los campos realmente soportados por cada proveedor en el catálogo de cobertura.


## Sincronización automática de partidos

Ver [docs/AUTOMATIC_MATCH_UPDATES.md](AUTOMATIC_MATCH_UPDATES.md). El modelo debe distinguir estado deportivo de estado de sincronización, conservar IDs de proveedor y marcas de tiempo, y permitir reconciliar correcciones posteriores sin perder auditoría. Los partidos finalizados deben actualizar resultados y estadísticas automáticamente desde un feed autorizado.
