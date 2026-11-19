# Fuentes y evaluación inicial

Fecha de revisión: 2026-11-19.

## Fútbol: open-matchday

Repositorio: https://github.com/L1nu-X/open-matchday

- Publica resultados/fixtures CSV de 75 competiciones y actualiza diariamente.
- Incluye Premier League, LaLiga, Ligue 1, UEFA Champions/Europa/Conference, Brasileirão y Liga Profesional Argentina, entre otras.
- La cobertura estadística es desigual: la documentación indica que tiros/faltas/tarjetas y corners están disponibles solo para una fracción de partidos; no ofrece xG, alineaciones, lesiones, cuotas ni play-by-play.
- Sus condiciones declaran uso informativo no comercial, requieren atribución y advierten que los derechos de los proveedores upstream prevalecen.
- No redistribuir automáticamente sus CSV ni copiar datos de Football-Data.co.uk, ESPN, FotMob, Soccerway u otros upstream hasta verificar permiso para ese uso concreto.
- No se ha confirmado cobertura de Liga 1 Perú, Libertadores, Sudamericana o Nations League en el índice revisado. Se requieren fuentes adicionales.

## NBA: llimllib/nba_data

Repositorio: https://github.com/llimllib/nba_data  
Catálogo: https://basketball-data.billmill.org/nba/nba.duckdb

- Documenta game logs, estadísticas de temporada, lookup de equipos/jugadores y box scores.
- Estadísticas stats.nba.com: desde 2009-10; datos ESPN Analytics desde 2018-19.
- IDs de partidos permiten identificar pretemporada (001), temporada regular (002), All-Star (003), playoffs (004), Play-In (005) y final NBA Cup (006).
- La documentación identifica limitaciones: algunos juegos de exhibición All-Star pueden faltar y player game logs omiten jugadores DNP.
- La disponibilidad técnica no constituye por sí sola permiso para republicar datos NBA/ESPN. Usar como fuente de consulta/prototipo hasta revisar términos de origen y permiso de almacenamiento/distribución.

## NBA oficial / Sportradar

Sportradar documenta datos históricos desde 2013; Play-In desde 2019 y NBA Cup desde 2023, incluyendo PRE, REG, PST, PIT e IST. Es una alternativa de feed licenciado; verificar plan, límites y derechos de almacenamiento/redistribución antes de uso.

## Fuentes excluidas hasta obtener autorización

- Football-Data.co.uk: no usar para alimentar la base FijasPro ni sus modelos sin permiso expreso, por sus restricciones publicadas.
- Cualquier scraper de SofaScore/365Scores u otro sitio: no asumir que acceso público equivale a API autorizada o permiso de extracción y redistribución.

## Próximos pasos de investigación

1. Obtener inventario exacto de competiciones de la interfaz FijasPro.
2. Auditar cobertura 2025-01-01 a 2026-11-19 por competición y por campo.
3. Confirmar Liga 1 Perú, Libertadores, Sudamericana y Nations League con fuentes autorizadas.
4. Resolver licencia/ToS antes de descargar y almacenar datos masivamente.
5. Publicar un manifiesto por fuente con cobertura, fecha de corte, atribución y restricciones.
