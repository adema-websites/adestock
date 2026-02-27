# Optimización del panel `/admin/` (13-02-2026)

## Objetivo
Reducir consultas lentas y mejorar tiempo de carga del dashboard admin personalizado (`CustomAdminSite.index -> calculate_metrics`).

---

## Cambios implementados

### 1) Instrumentación SQL del admin (diagnóstico)

**Archivo:** `adestock/middleware.py`
- Se agregó `AdminSQLProfilerMiddleware`.
- Perfilado activo solo para rutas `/admin/`.
- Activación por entorno (`ADMIN_SQL_PROFILER_ENABLED`).
- Loguea:
  - resumen por request (`ADMIN_SQL_PROFILE`)
  - top consultas lentas (`ADMIN_SQL_TOP`)

**Archivo:** `adestock/settings.py`
- Nuevas variables:
  - `ADMIN_SQL_PROFILER_ENABLED`
  - `ADMIN_SQL_PROFILER_MIN_MS`
  - `ADMIN_SQL_PROFILER_TOP_N`
  - `ADMIN_SQL_PROFILER_SQL_MAX_LEN`
- Se registró middleware: `adestock.middleware.AdminSQLProfilerMiddleware`.
- Logger dedicado `adestock.admin_sql_profiler`.
- Handler de archivo `logs/admin_sql.log`.

---

### 2) Optimización de consultas en dashboard admin

**Archivo:** `adestock/admin_override.py` (método `calculate_metrics`)

#### 2.1 Filtros de fecha en `Venta` sin cast por fecha
- Se reemplazaron filtros con `fecha__date__gte/lte` por rango datetime:
  - `fecha__gte=fecha_desde_dt`
  - `fecha__lt=fecha_hasta_exclusive_dt`
- Se usaron datetimes **aware** (`timezone.make_aware`) para evitar warnings de naive datetime.

Impacto: evita expresiones SQL tipo `django_datetime_cast_date(...)`, que suelen romper el uso eficiente de índices.

#### 2.2 Unificación de “ventas por seguimiento”
- Se eliminó el doble query (con seguimiento + sin seguimiento).
- Ahora se usa una sola agregación con `Coalesce`:
  - estado (`Sin Seguimiento` por defecto)
  - color (`#6c757d` por defecto)
  - orden (`999999` por defecto)

Impacto: menos scans sobre `venta_venta`.

#### 2.3 Reuso de queryset base de detalles de venta
- Se creó `ventas_detalle_base` para reutilizar en:
  - top productos
  - top clientes
  - total productos vendidos

Impacto: menor duplicación de lógica y simplificación de consultas.

#### 2.4 Optimización de “Top productos”
- Se pasó de agrupar por `producto__nombre` a agrupar por `producto_id`.
- Nombres se resuelven en una consulta separada (`Producto.objects.filter(id__in=...)`).

Impacto: agrupación más eficiente (clave numérica).

#### 2.5 Cache por bloques pesados (independientes de fecha)
- Nuevo cache de valuación de inventario:
  - key: `dashboard_inventory_valuation_v2`
  - TTL: 3600s
- Nuevo cache de reportes extra:
  - key: `dashboard_extra_reports_v2`
  - TTL: 3600s

Impacto: cuando cambia el rango de fechas, se evita recalcular bloques que no dependen de fecha.

---

### 3) Índices de base de datos

**Archivo:** `venta/models.py`

Se agregaron índices:
- `Venta`
  - `(estado, fecha)` -> `venta_estado_fecha_idx`
  - `(fecha, seguimiento)` -> `venta_fecha_seg_idx`
- `DetalleVenta`
  - `(fecha, venta)` -> `detven_fecha_venta_idx`
  - `(fecha, producto)` -> `detven_fecha_prod_idx`
  - `(venta, producto)` -> `detven_venta_prod_idx`

**Migración generada:**
- `venta/migrations/0002_detalleventa_detven_fecha_venta_idx_and_more.py`

---

## Comandos ejecutados

```bash
python manage.py check
python manage.py makemigrations venta
python manage.py migrate venta
```

Además se ejecutaron requests de benchmark contra `/admin/` con `Client()` autenticado.

---

## Resultados de benchmark (medidos)

### Antes de optimizar (medición previa)
- `/admin/`: ~20s
- Query top lenta: ~521-545 ms
- `sql_count` al límite de captura (`9000`)

### Después de optimizar
- Primer request frío (cache vacía):
  - `/admin/?fecha_desde=2026-02-01&fecha_hasta=2026-02-13`
  - **~23.4s** (sigue alto por bloques Python/N+1 de cálculo inicial)
  - consultas SQL lentas ya sin picos grandes (top ~84ms)
- Request con **otro rango de fechas** inmediatamente después:
  - `/admin/?fecha_desde=2026-01-01&fecha_hasta=2026-01-31`
  - **~1.84s**
- Request repetido del mismo rango:
  - **~25ms** (cache hit total)

Conclusión: se eliminaron los picos de SQL largo y se mejoró mucho el escenario real de uso con cambios de filtro y cache caliente.

---

## Pendiente recomendado (siguiente fase)

Para bajar también el **primer request frío**, el principal cuello actual es cálculo en Python por producto (`stock_actual()` en loop), que dispara muchas consultas chicas (patrón N+1). Se recomienda:

1. Reemplazar valuación por agregados por lote (compras/ventas/fabricación/mermas).
2. Evitar llamadas per-product a `stock_actual()` en dashboard.
3. Mantener coherencia funcional con la lógica de stock actual.

---

## Archivos modificados en esta tarea

- `adestock/middleware.py`
- `adestock/settings.py`
- `adestock/admin_override.py`
- `venta/models.py`
- `venta/migrations/0002_detalleventa_detven_fecha_venta_idx_and_more.py`
- `README_ADMIN_OPTIMIZACION_2026-02-13.md`

---

## Limpieza de pruebas

- Se creó usuario temporal `copilot_profiler` para benchmark.
- Se eliminó al finalizar (`deleted=1`).
