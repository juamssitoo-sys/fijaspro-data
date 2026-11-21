# Referencia: oritzio/football-database

Fuente: https://github.com/oritzio/football-database (rama `master`).

El README describe una colección de equipos en JSON para la temporada 2026/2027. Cada fila observada usa `team_id`, `team_name`, `team_abbreviation` y `team_stadium`.

## Uso en FijasPro
- Utilizar como catálogo de referencia de equipos y estadios, no como proveedor de fixtures, marcadores ni estadísticas.
- Los IDs de esta fuente solo son IDs locales de la fuente. No equipararlos directamente con IDs ESPN/Sportmonks; guardar el mapeo entre proveedores por separado.
- No sobreescribir IDs existentes ni información de encuentros con este catálogo.
- Revisar cambios de temporada y altas/bajas de equipos antes de cada actualización.
- Registrar fuente, archivo, commit y fecha de captura en toda importación.

## Cobertura detectada en el árbol del repositorio
La fuente enumera ligas de Inglaterra (Premier League, Championship, League One, League Two), Francia, España, Italia, Alemania, Países Bajos, Portugal, Brasil, Bélgica, Dinamarca, Escocia, República Checa, Turquía, Suecia, Croacia, Grecia, Colombia, México, Israel y deportes/equipos de Estados Unidos (MLS, NBA, NFL, NHL y MLB).

## Licencia
No se encontró un archivo LICENSE ni una declaración de licencia en README. No redistribuir los datos como parte de un producto comercial hasta obtener autorización/licencia del titular.
