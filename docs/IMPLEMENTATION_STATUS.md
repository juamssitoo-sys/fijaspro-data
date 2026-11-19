# Estado de implementación — 2026-11-19

## Repositorio inspeccionado
- Repositorio: juamssitoo-sys/fijaspro-data
- Rama: main
- Visibilidad: public
- Repositorio confirmado y archivos leídos de vuelta desde GitHub.

## Implementado
- Catálogo inicial de 12 competiciones de fútbol y NBA, extraído de la configuración del backend FijasPro.
- Modelo de datos normalizado para partidos, temporadas, fases, equipos, jugadores y estadísticas.
- JSON Schema para registros de partidos.
- Política de fuentes/licencias y trazabilidad.
- Script de auditoría del catálogo NBA (solo metadatos; no replica registros deportivos).
- Validador básico de JSON y archivos sensibles.
- GitHub Actions para validar cambios en main y pull requests.

## Fuentes auditadas
### NBA
El repositorio llimllib/nba_data documenta datasets de stats.nba.com desde 2009-10 y ESPN Analytics desde 2018-19; incluye logs, box scores, temporadas, eventos y schedule. Su README documenta los prefijos de partido:
- 001 pretemporada
- 002 temporada regular
- 003 All-Star
- 004 playoffs
- 005 Play-In
- 006 final NBA Cup

No se encontró un archivo LICENSE en la raíz durante esta inspección. El README identifica fuentes subyacentes NBA y ESPN. Por tanto, no se han copiado sus Parquet ni sus datos de jugador/partido a este repositorio. La auditoría de cobertura está preparada para leer solo metadatos.

### Fútbol
open-matchday documenta 75 competiciones y archivos CSV para la temporada 2026/27, pero no representa por sí mismo el histórico completo 2025/26. Su DISCLAIMER limita el uso a fines informativos no comerciales, exige atribución y deja vigentes las condiciones de los proveedores upstream (incluidos ESPN y football-data.co.uk). Estadísticas de tiros/faltas/tarjetas/corners aparecen solo para una fracción de partidos. No se han copiado CSV ni datos de proveedores.

## Importación inicial realizada — 2026-11-19
- Se importaron 5 archivos JSON de OpenFootball para la temporada 2025/26: Premier League (380), LaLiga (380), Bundesliga (306), Ligue 1 (306) y Serie A (380).
- Total importado: 1,752 registros de partidos en formato fuente, sin normalización ni enriquecimiento.
- Archivos en `data/raw/openfootball/2025-26/`; manifiesto en `data/metadata/openfootball_import_2025-26.json`.
- Los archivos se leyeron de vuelta desde GitHub y se parsearon como JSON correctamente.
- Fuente declara CC0-1.0 para su esquema, datos y scripts: https://github.com/openfootball/football.json

## No realizado todavía
- No hay estadísticas de jugadores descargadas en `data/`.
- No se ha validado un recuento histórico de partidos por liga/temporada.
- No se ha conectado esta base al backend de producción FijasPro.
- No se ha confirmado la cobertura de Liga 1 Perú, Libertadores, Sudamericana y Nations League con una fuente que permita almacenamiento/redistribución.

## Criterio para declarar completo
Solo se marcará una competición/temporada como completa después de:
1. verificar derechos de almacenamiento y uso;
2. importar datos con identificadores de proveedor;
3. validar cobertura de fechas, partidos, equipos y jugadores;
4. medir duplicados y nulos;
5. publicar un manifiesto de cobertura y fuente.


## Importaciones adicionales — 2026-11-19
- Brasileirão Série A 2025: importado desde `openfootball/south-america`, archivo `brazil/2025_br1.txt`; encabezado de fuente: 380 partidos.
- Argentina Primera División 2025: importado desde `openfootball/south-america`, archivo `argentina/2025_ar1.txt`; encabezado de fuente: 240 partidos, solo etapa `1° Semestre`. No se declara temporada completa.
- UEFA Champions League 2025/26: importado desde `openfootball/champions-league`, archivo `2025-26/cl.txt`; encabezado de fuente: 189 partidos.
- Los tres archivos se guardaron sin alterar en `data/raw/openfootball/south-america/` y `data/raw/openfootball/champions-league/`. Manifiesto: `data/metadata/openfootball_additional_import_2026-11-19.json`.
- Las fuentes upstream declaran dedicación al dominio público / CC0. Se conserva la atribución de origen y no se atribuyen estadísticas de jugadores a estos archivos.

## Competiciones del catálogo todavía sin importación confirmada
- Liga 1 Perú.
- Copa Libertadores.
- Copa Sudamericana.
- UEFA Europa League.
- UEFA Conference League.
- UEFA Nations League.

No se encontraron archivos verificables para esas competiciones en las rutas consultadas; no se han creado registros sustitutos ni se han copiado datos de fuentes con condiciones no verificadas.
