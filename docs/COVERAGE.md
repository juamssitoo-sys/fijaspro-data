# Cobertura disponible — corte 2026-11-19

Este inventario separa **archivos fuente importados** de cobertura completa de una competición. Los conteos de Football.TXT proceden de los encabezados de OpenFootball y todavía no equivalen a filas normalizadas, partidos únicos ni validación de resultados. Los cinco JSON de primera división sí se volvieron a leer desde el repositorio destino y se parsearon correctamente.

## Inventario importado

| Competición | Temporada / alcance | Conteo declarado | Estado |
|---|---:|---:|---|
| Premier League | 2025/26 | 380 | JSON parseado; raw |
| LaLiga | 2025/26 | 380 | JSON parseado; raw |
| Bundesliga | 2025/26 | 306 | JSON parseado; raw |
| Ligue 1 | 2025/26 | 306 | JSON parseado; raw |
| Serie A | 2025/26 | 380 | JSON parseado; raw |
| Brasileirão Série A | 2025 | 380 | Football.TXT raw; conteo de encabezado |
| Primera División Argentina | 2025, solo 1.er semestre | 240 | Parcial; Football.TXT raw |
| UEFA Champions League | 2025/26 | 189 | Football.TXT raw; conteo de encabezado |
| Copa Libertadores | 2025 | 155 | Football.TXT raw; conteo de encabezado |
| Copa Sudamericana | 2025 | 121 | Football.TXT raw; conteo de encabezado |
| UEFA Nations League | 2024/25 | 158 | Football.TXT raw; conteo de encabezado |
| UEFA Europa League | 2025/26, solo clasificatorias | 82 | Parcial; Football.TXT raw |
| UEFA Conference League | 2025/26, solo clasificatorias | 256 | Parcial; Football.TXT raw |

**Total aritmético de conteos declarados: 3,333.** No debe presentarse como 3,333 partidos únicos verificados. No se ha normalizado, deduplicado ni validado fila por fila el conjunto completo.

## Fuera de cobertura / bloqueado

- **Liga 1 Perú:** no se importó. No se identificó una fuente con permiso/licencia verificable para almacenar y redistribuir resultados en el repositorio público.
- **Europa League y Conference League, fase principal 2025/26:** los archivos OpenFootball consultados solo contienen `elq.txt` y `confq.txt` para clasificatorias; no están `el.txt` ni `conf.txt`. Las páginas UEFA y exportaciones de terceros sirven para consulta, pero no se acreditó permiso de redistribución.
- **NBA:** no se copiaron registros de partidos/jugadores. La disponibilidad técnica de catálogos de terceros no resuelve los derechos de NBA/ESPN. La auditoría preparada es solo de metadatos y aún no se ha ejecutado.
- **Estadísticas de jugadores/equipos:** no hay importación confirmada de box scores ni estadísticas detalladas.

## Próximos hitos para declarar la base lista

1. Implementar y probar un parser Football.TXT y un normalizador JSON con pruebas de casos especiales (prórroga, penales, partidos aplazados, marcadores incompletos y fechas).
2. Normalizar los 13 archivos y generar informes por temporada/fase: filas, IDs, duplicados, nulos, equipos y rangos de fechas.
3. Obtener fuente o autorización redistribuible para Liga 1 y fases principales UEFA; resolver derechos de NBA antes de replicar sus registros.
4. Conectar el dataset validado al backend solo después de fijar el contrato API y pruebas de integración.
5. Mantener los archivos raw y manifiestos de procedencia separados de los datos normalizados.

## Manifiestos

- `data/metadata/openfootball_import_2025-26.json`
- `data/metadata/openfootball_additional_import_2026-11-19.json`
- `data/metadata/openfootball_cups_nations_import_2026-11-19.json`
- `data/metadata/openfootball_uefa_qualifiers_2025-26_2026-11-19.json`
