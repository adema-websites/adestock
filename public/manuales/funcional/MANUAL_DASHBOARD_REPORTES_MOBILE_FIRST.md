# Manual de Dashboard y Reportes (Mobile First)

## Objetivo
Este manual define cómo usar `/dashboard/` como centro de control operativo y de análisis, con foco en visualización rápida desde celular y validación posterior en escritorio.

## Alcance
- Ruta principal: `/dashboard/` (panel administrativo personalizado)
- Público: supervisión, caja, dueños y responsables de operación
- Uso esperado: consulta diaria, detección de desvíos y decisión rápida

## Principios Mobile First
1. Ver primero los KPIs clave en una sola pantalla.
2. Reducir scroll horizontal y priorizar tarjetas verticales.
3. Mostrar filtros de fecha simples y visibles.
4. Mantener acciones críticas arriba (exportar, actualizar, filtrar).

## Flujo operativo recomendado
1. Abrir `/dashboard/` al inicio de turno.
2. Ajustar rango de fechas (`fecha_desde`, `fecha_hasta`).
3. Revisar métricas de ventas, caja y rentabilidad.
4. Entrar a reportes detallados cuando haya desvíos.
5. Exportar evidencia (PDF/Excel) para cierre y auditoría.

## Qué reportar diariamente desde `/dashboard/`
- Total vendido del período.
- Cantidad de comprobantes/ventas.
- Ticket promedio.
- Ingresos por medios de cobro.
- Egresos relevantes (gastos/retiros).
- Alertas de stock y productos críticos (si aplica en vista).

## Vista recomendada para celular
- Bloque 1: rango de fechas + botón actualizar.
- Bloque 2: 4 a 6 KPIs en tarjetas.
- Bloque 3: resumen de caja y medios.
- Bloque 4: accesos rápidos a reportes detallados.

## Buenas prácticas de gestión
- Validar siempre el mismo corte horario para comparar días.
- Separar lectura operativa (hoy) de lectura analítica (semanal/mensual).
- Si un KPI cae, abrir inmediatamente el reporte fuente y dejar nota.
- No tomar decisiones por un único dato aislado.

## Integración con reportes del sistema
Después del dashboard, profundizar en:
- Reportes de caja.
- Reportes de billeteras/cuentas.
- Inventario detallado.
- Trazabilidad y estados de pedidos (armado/fabricación).

## Checklist de cierre diario (mobile)
- [ ] Rango de fechas correcto.
- [ ] Ventas y ticket promedio dentro de rango esperado.
- [ ] Diferencias de caja justificadas.
- [ ] Egresos extraordinarios identificados.
- [ ] Exportación de respaldo generada.

## Notas técnicas
- El dashboard se sirve desde el admin personalizado (`CustomAdminSite`).
- Los filtros y exportaciones deben usarse como fuente oficial de auditoría.
- Si se detecta lentitud, revisar primero filtros de fecha y volumen de datos.
