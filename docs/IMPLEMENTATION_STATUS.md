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


## Importaciones adicionales — actualización 2026-11-19 12:21 UTC
- Copa Libertadores 2025: importada desde `openfootball/south-america/copa-libertadores/2025_copal.txt`; encabezado de fuente: 155 partidos.
- Copa Sudamericana 2025: importada desde `openfootball/south-america/copa-libertadores/2025_copas.txt`; encabezado de fuente: 121 partidos.
- UEFA Nations League 2024/25: importada desde `openfootball/internationals/uefa_nations_league/2024_uefa_nations_league.txt`; encabezado de fuente: 158 partidos.
- Archivos copiados sin alterar en `data/raw/openfootball/`; manifiesto: `data/metadata/openfootball_cups_nations_import_2026-11-19.json`.
- Los repositorios upstream de OpenFootball declaran dedicación al dominio público para esquema/datos/scripts.

## Pendientes que requieren otra fuente o permiso
- Liga 1 Perú: no se encontró una fuente abierta con licencia clara que permita incorporar y redistribuir resultados de partidos. El dataset del IPD consultado contiene registro de ligas, no resultados. No se importó.
- UEFA Europa League y Conference League 2025/26: el repositorio OpenFootball consultado declara incluir estas competiciones, pero no se localizaron archivos de esa temporada en las rutas verificadas. Se encontró open-matchday para 2026/27; su propio aviso limita el uso a fines informativos no comerciales y deja vigentes los términos de los proveedores upstream (ESPN, football-data.co.uk, fixturedownload, Soccerway, etc.). No se copió al repositorio público sin autorización específica de esos proveedores.

## Cobertura pendiente tras esta actualización
- Liga 1 Perú.
- UEFA Europa League 2025/26.
- UEFA Conference League 2025/26.
- No se ha conectado todavía la base al backend de producción ni se han importado estadísticas de jugadores.


## Importación adicional — clasificatorias UEFA 2025/26 — 2026-11-19
- UEFA Europa League: importado `2025-26/elq.txt`, 82 partidos declarados en el encabezado de la fuente; corresponde solo a rondas clasificatorias.
- UEFA Conference League: importado `2025-26/confq.txt`, 256 partidos declarados en el encabezado de la fuente; corresponde solo a rondas clasificatorias.
- Ambos archivos se copiaron sin alterar desde `openfootball/champions-league`. Manifiesto: `data/metadata/openfootball_uefa_qualifiers_2025-26_2026-11-19.json`.
- El repositorio fuente declara CC0-1.0 en `LICENSE.md`. La licencia incluye una cláusula que no garantiza la liberación de derechos de terceros; se conserva la procedencia y no se asume que CC0 resuelva automáticamente todos los derechos subyacentes.
- La inspección del árbol completo de la temporada 2025/26 no encontró `el.txt` ni `conf.txt` de fase principal. Por tanto, las competiciones siguen incompletas en el catálogo: solo hay cobertura clasificatoria.

## Revisión de Liga 1 Perú — 2026-11-19
- No se encontró un dataset público con licencia clara para redistribuir resultados de Liga 1.
- El dataset del IPD en datosabiertos.gob.pe está bajo Open Data Commons Attribution, pero contiene el registro administrativo de ligas deportivas, no resultados/fixtures de partidos.
- Footiqo y FootyStats muestran resultados y exportaciones, pero no se verificó una licencia que autorice la copia y redistribución de esos datos en FijasPro. No se importaron.
- La búsqueda identificó proyectos comunitarios de resultados de la selección peruana, pero no corresponden a Liga 1. Liga 1 Perú queda pendiente de una fuente autorizada o permiso explícito.

## Estado de las competiciones pendientes
- Liga 1 Perú: sin fuente redistribuible verificada.
- UEFA Europa League 2025/26: solo clasificatorias importadas (82 según encabezado); fase principal no localizada.
- UEFA Conference League 2025/26: solo clasificatorias importadas (256 según encabezado); fase principal no localizada.
- Estos conteos son los declarados por los encabezados de los archivos fuente; aún no son conteos normalizados, deduplicados ni validados fila por fila.


## Búsqueda ampliada de fuentes — 2026-11-19 12:34 UTC
### UEFA Europa League y Conference League 2025/26
- Se inspeccionó el árbol completo de `openfootball/champions-league` en la rama `master`: la carpeta `2025-26` contiene `cl.txt`, `clq.txt`, `elq.txt` y `confq.txt`, pero no `el.txt` ni `conf.txt`. Las rutas de fase principal devuelven 404. Por ello, los 82 y 256 partidos importados siguen siendo únicamente clasificatorias.
- UEFA publica páginas oficiales con resultados de la temporada completa: Europa League (`https://www.uefa.com/uefaeuropaleague/news/029c-1e9ad67620f2-05c31d01f0f4-1000--2025-26-europa-league-fixtures-and-results-quarter-final/`) y Conference League (`https://es.uefa.com/uefaconferenceleague/news/029c-1e9b4aa1be84-fcdd372d089f-1000--calendario-y-resultados-de-la-conference-league-2025-26/`). Son fuentes de verificación y consulta, pero no se identificó una licencia abierta que permita copiar y redistribuir masivamente sus registros.
- FixtureDownload ofrece exportación CSV/XLSX/JSON para ambas temporadas (`https://fixturedownload.com/results/europa-league-2025`, `https://fixturedownload.com/results/conference-league-2025`). No se verificó una licencia de redistribución, por lo que no se importó.
- La documentación DeepWiki del repositorio OpenFootball describe convenciones de nombres `el.txt` y `conf.txt`, pero la inspección del árbol Git real prevalece: esos dos archivos no están presentes en la temporada 2025/26 consultada.
### Liga 1 Perú
- La web oficial `https://liga1.pe/` publica resultados/fixtures mediante widgets identificados como proporcionados por SofaScore. La LFPP anunció su web institucional con fixture, tablas y resultados por torneo (`https://liga1.pe/la-liga-de-futbol-profesional-peruana-estrena-web-institucional-con-informacion-de-sus-competencias/`). No se identificó licencia de datos que permita extracción y redistribución en FijasPro.
- El portal oficial de Liga 1 publica resultados por fecha (ejemplos: Clausura fecha 1 y fecha 19), útiles para verificación manual, no equivalen a una licencia de redistribución del conjunto completo.
- Se inspeccionó el proyecto comunitario `LordEnnard14/liga1-apertura-2025-Data-Analytics`. Su CSV contiene 171 filas de resultados del Apertura 2025, pero el repositorio no tiene archivo LICENSE. Su README declara que los datos fueron obtenidos de Meridianbet y que el proyecto es para fines educativos. No se importó porque no hay permiso/licencia de redistribución confirmada y solo cubre el Apertura.
- PeruFutbolStats declara que sus resultados Liga 1 se registran manualmente durante transmisiones de L1 Max y se revisan; no se encontró licencia abierta para reutilizar/redistribuir su base.
- Footiqo ofrece CSV/Excel descargables con resultados y estadísticas históricas, pero no se encontró permiso explícito de redistribución de sus datos.
- IPD/Plataforma Nacional de Datos Abiertos mantiene un dataset con licencia ODC Attribution, pero su contenido es el registro administrativo de ligas inscritas, no fixtures ni resultados.
### Decisión
No se importan fuentes sin licencia/permiso verificable, aunque permitan consultar o descargar datos. Próximas vías válidas: solicitar autorización al titular/proveedor, obtener un feed/API con derechos de almacenamiento y redistribución, o usar un dataset que declare expresamente licencia abierta para los datos subyacentes.


## Consolidación del inventario — 2026-11-19
- Se consolidó la cobertura en `docs/COVERAGE.md` y se corrigió el estado del README, que todavía describía la ingesta como pendiente.
- Inventario actual: 13 archivos raw de 13 alcances competición/temporada; total aritmético de encabezados fuente: 3,333. Este total no es un conteo normalizado ni deduplicado.
- Los cinco JSON de primera división 2025/26 fueron parseados desde el repositorio destino. Los ocho archivos Football.TXT permanecen en bruto; sus cantidades son declaraciones de encabezado.
- No se rellenaron Liga 1, fases principales UEFA ni NBA con datos sin derechos verificados.
- Pendientes técnicos reales: parser/normalizador, validación fila por fila, deduplicación, estadísticas de jugadores/equipos, auditoría NBA y conexión al backend. No se declara producción ni integración completada.
