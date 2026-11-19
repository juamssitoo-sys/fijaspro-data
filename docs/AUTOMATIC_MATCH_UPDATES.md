# Actualización automática al finalizar cada partido

## Requisito funcional obligatorio

FijasPro debe actualizar automáticamente los datos de cada partido cuando termine. No debe requerir una solicitud manual ni depender de una carga diaria. Se actualizarán, según lo que publique el proveedor autorizado: estado final, marcador, medio tiempo, prórroga, penales y estadísticas disponibles de equipos y jugadores.

Un partido no se considera terminado solo porque haya pasado su hora programada.

## Flujo operativo

1. Importar el calendario y conservar el ID estable de cada partido en el proveedor.
2. Seguir los partidos próximos y en curso mediante webhooks oficiales, si el proveedor los ofrece, o polling dentro de los límites contractuales.
3. Detectar estados como programado, en juego, descanso, aplazado, suspendido, abandonado y finalizado, solo si el proveedor los expone.
4. Al detectar el estado final, solicitar el detalle completo del partido, no solo el marcador del listado.
5. Validar ID, equipos, competición, fecha, estado y coherencia de los resultados.
6. Guardar mediante upsert idempotente por proveedor e ID de partido. Eventos repetidos no deben crear duplicados.
7. Recalcular tablas, forma reciente, promedios y métricas que dependan del encuentro.
8. Reconciliar partidos finalizados durante una ventana configurable de 24–72 horas para captar correcciones de resultados o estadísticas.
9. Registrar última consulta, última actualización exitosa, errores, reintentos y antigüedad del dato. Alertar ante partidos que no se actualicen dentro del margen esperado.

## Cadencia y resiliencia

- No fijar un intervalo universal hasta confirmar proveedor, plan y rate limits.
- Fixtures lejanos: consultas poco frecuentes; partidos próximos/en vivo: consultas más frecuentes; al finalizar: recuperar detalle inmediatamente y reconciliar después.
- Respetar rate limits, Retry-After, backoff exponencial y términos de caché/almacenamiento.
- Verificar la firma de webhooks cuando existan.
- Ejecutar la ingesta en backend/worker programado; nunca depender de que el usuario mantenga abierta la web.
- Si falla el proveedor, conservar el último dato válido y marcarlo como potencialmente desactualizado.

## Campos recomendados

En partidos: proveedor, ID externo, estado deportivo, hora programada/inicio/finalización, marcador final, marcador de medio tiempo, indicadores de prórroga/penales, marcador de penales, fecha de actualización del proveedor, última sincronización, captura, estado/error de sincronización.

En estadísticas: clave única por proveedor, partido y entidad (equipo/jugador), fecha de actualización/captura y versión o hash del payload cuando esté disponible.

Los campos ausentes permanecen null. El estado de sincronización es distinto del estado deportivo.

## Criterios de aceptación

- El resultado final se persiste sin intervención manual.
- Los endpoints y la interfaz reflejan el dato después de la ingesta.
- Las estadísticas se actualizan cuando el proveedor las publica, incluso si llegan después del pitazo final.
- Reintentos y eventos repetidos no duplican datos.
- Correcciones posteriores se aplican y conservan trazabilidad.
- Se puede consultar cuándo se sincronizó por última vez cada partido.

## Estado actual

Requisito documentado; automatización aún no desplegada. El repositorio de datos todavía no está conectado al backend. La implementación requiere un feed autorizado que permita consultas frecuentes, almacenamiento histórico y redistribución de los datos correspondientes.
