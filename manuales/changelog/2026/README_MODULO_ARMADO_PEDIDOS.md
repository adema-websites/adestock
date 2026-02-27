# Módulo: Armado de Pedido (Picking para Distribuidores)

Fecha: 2026-02-13  
Estado: Propuesta técnica completa (lista para implementación)

## 1) Objetivo de negocio

Construir un módulo nuevo de **Armado de Pedido** para operaciones con alto volumen, donde:

- cada pedido tenga una orden de armado asociada,
- exista un flujo de estados configurable,
- se pueda ejecutar picking real (esperado vs. escaneado/validado),
- se emita automáticamente un ajuste económico (tipo nota de crédito) por faltantes/sobrantes,
- el proceso pueda cerrarse y también reabrirse controladamente.

---

## 2) Diagnóstico del sistema actual (alineación)

Sí, la idea está **muy alineada** con la arquitectura actual:

1. **Estados configurables**
   - Ya existe patrón en `venta.EstadoSeguimiento`.
   - Ya existe patrón más robusto en `cocina.EstadoFabricacion` + avance por orden.

2. **Disparadores por configuración al cerrar venta**
   - Ya existe en `repositories/VentaRepository.py::finalizar()` el flag `Configuracion.generar_fabricacion_al_vender`.
   - Podemos replicar el mismo patrón con un flag para armado de pedido.

3. **Cierre desde POS**
   - El flujo de cierre en POS usa `venta.pagar() -> venta.finalizar() -> venta.save()`.
   - Es el mejor punto único para creación automática del armado.

4. **Reportes PDF**
   - Ya hay reportes PDF de venta/fabricación (ReportLab) reutilizables como base.

5. **Acciones de admin para operación masiva**
   - `VentaAdmin` ya tiene acciones/botones por fila y URLs custom.
   - Se puede agregar acción “Crear armado de pedido” para uno o varios pedidos.

Conclusión: **no hay que inventar un framework nuevo**, solo extender patrones existentes de forma consistente.

---

## 3) Decisiones de diseño (MVP robusto)

### 3.1 Nueva app

Crear app: `armado`.

### 3.2 Modelo de estados configurable

Crear `EstadoArmadoPedido` (similar a `EstadoFabricacion`):

- `nombre` (unique)
- `orden` (secuencia)
- `color`
- `es_final`
- `es_cancelado`
- `permite_edicion` (opcional, default True)
- `activo`

Uso: definir flujos como “Pendiente → En picking → Controlado → Cerrado” o variantes por negocio.

### 3.3 Cabecera de armado

Crear `ArmadoPedido`:

- `venta` (FK a `venta.Venta`)
- `codigo` (correlativo legible)
- `estado` (FK a `EstadoArmadoPedido`)
- `deposito` (FK a depósito origen para picking)
- `fecha_creacion`, `fecha_inicio`, `fecha_cierre`
- `usuario_creador`, `usuario_cierre`
- `origen` (`AUTO_POS` / `MANUAL_ADMIN`)
- `cerrado` (bool derivable por estado final, opcional)
- `bloqueado` (bool para hard-lock manual si se requiere)
- `observaciones`

**Regla anti-duplicado clave:**

- Restricción única: `UniqueConstraint(fields=['venta'], condition=Q(activo=True), name='uniq_armado_activo_por_venta')`.
- Resultado: no se puede crear dos veces el mismo armado para una venta activa.

> Si se decide permitir “rearmado histórico”, se puede cerrar/anular el anterior y crear uno nuevo, pero nunca 2 activos de la misma venta.

### 3.4 Detalle de picking

Crear `ArmadoPedidoItem`:

- `armado` (FK)
- `detalle_venta` (FK a `venta.DetalleVenta`, opcional si se desea snapshot)
- `producto` (FK)
- `variante_texto` (snapshot: medida, presentación, etc.)
- `codigo_producto` (snapshot)
- `descripcion_producto` (snapshot)
- `cantidad_pedida`
- `cantidad_pickeada`
- `cantidad_faltante` (calculada)
- `cantidad_sobrante` (calculada)
- `estado_item` (`PENDIENTE`, `OK`, `FALTANTE`, `SOBRANTE`, `AJUSTADO`)
- `ultimo_scan` (datetime)
- `usuario_ultima_validacion`

Recomendado: guardar snapshot de descripción/código/variante para preservar trazabilidad aunque el producto cambie luego.

### 3.5 Eventos de trazabilidad (recomendado)

Crear `ArmadoPedidoEvento`:

- `armado`
- `tipo_evento` (`CREADO`, `PICK`, `ESTADO`, `CIERRE`, `REAPERTURA`, `NC_EMITIDA`, etc.)
- `payload_json`
- `usuario`
- `fecha`

Sirve para auditoría completa y para la pantalla exclusiva futura.

---

## 4) Configuración de empresa (flag solicitado)

Hoy existe `agenda.Configuracion.entrega` y `entrega_ventas`.  
Para este módulo agregar:

- `gestionar_entrega` (BooleanField, default=False)
  - Help: “Si está activo, al cerrar un pedido desde POS se crea automáticamente un Armado de Pedido.”

### Comportamiento

1. **Si `gestionar_entrega=True`:**
   - Al cerrar venta en POS (`VentaRepository.finalizar`) crear `ArmadoPedido` automático.
2. **Si `gestionar_entrega=False`:**
   - No crear automático.
   - Habilitar acción manual en admin de ventas para crear armado uno o varios.

---

## 5) Integración con cierre de venta (automático)

## Punto técnico recomendado

Implementar en `repositories/VentaRepository.py::finalizar()` inmediatamente después de la lógica de fabricación automática, con guardas idempotentes.

### Servicio sugerido

Crear servicio nuevo: `armado/services.py`

- `crear_armado_desde_venta(venta, origen='AUTO_POS', usuario=None)`
  - valida venta finalizada,
  - usa `get_or_create` por venta,
  - clona detalle de venta a `ArmadoPedidoItem`,
  - asigna estado inicial activo de menor orden,
  - retorna armado + flag de creado/no creado.

### Idempotencia

Aunque `finalizar()` se dispare más de una vez, no debe duplicar armado por venta.

---

## 6) Acción manual en panel de pedidos (admin)

En `VentaAdmin` agregar acción:

- `crear_armado_pedido`

Reglas:

- Soporta selección múltiple.
- Solo procesa ventas válidas (idealmente finalizadas y no anuladas/canceladas).
- Si venta ya tiene armado activo: informar “omitida por duplicado”.
- Resultado de acción: resumen `creadas / omitidas / con error`.

Opcional UX:

- Botón por fila “Crear Armado” cuando no exista.

---

## 7) Picking (núcleo operativo)

### 7.1 Reglas de validación por item

Para cada `ArmadoPedidoItem`:

- `cantidad_pickeada == cantidad_pedida` → `OK`
- `cantidad_pickeada < cantidad_pedida` → `FALTANTE`
- `cantidad_pickeada > cantidad_pedida` → `SOBRANTE`

Al cerrar armado, consolidar diferencias por item.

### 7.2 API/servicio para pantalla exclusiva futura

Desde ahora definir backend desacoplado:

- endpoint o método de servicio `registrar_pick(armado_id, producto_id, delta, usuario)`
- actualización transaccional de cantidades
- respuesta con estado de item + progreso total

Esto permite luego conectar handheld, scanner o UI dedicada sin reescribir reglas.

---

## 8) Nota de crédito automática por diferencias

### 8.1 Criterio funcional

Al cerrar un armado con faltantes/sobrantes:

- generar documento de ajuste asociado al armado y a la venta origen,
- faltante: impacto negativo (nota de crédito a favor del cliente),
- sobrante: configurable (puede generar débito o solo observación según política comercial).

### 8.2 Diseño mínimo sugerido

Si aún no existe módulo formal de NC reutilizable, crear:

- `ArmadoAjuste` (cabecera)
  - `armado`, `venta`, `cliente`, `total_ajuste`, `tipo` (`NC`, `ND`, `MIXTO`), `estado`, `fecha`
- `ArmadoAjusteItem`
  - `producto`, `cantidad_diferencia`, `precio_unitario_base`, `subtotal`, `motivo`

Precio base recomendado: tomar de `DetalleVenta.precio` de la venta original para coherencia comercial.

### 8.3 Integridad

- Un ajuste por cierre de armado (`OneToOne` o unique por `armado`).
- Si se reabre y vuelve a cerrar, generar **re-liquidación controlada**:
  - opción A: anular ajuste anterior y emitir nuevo,
  - opción B: emitir ajuste incremental.

Para MVP: opción A (más simple y auditables).

---

## 9) Flujo de estados y reapertura

## Requisito solicitado

El pedido debe poder finalizarse pero también volver atrás para seguir modificando.

### Propuesta concreta

- Definir estados terminales (`es_final=True`) pero permitir transición administrativa de reapertura:
  - `CERRADO -> EN_PICKING` (solo con permiso especial)
- Al reaperturar:
  - desbloquear edición de items,
  - registrar evento de auditoría obligatorio con motivo,
  - si existía ajuste NC emitido: marcarlo “pendiente de re-liquidación”.

### Control de permisos

Permiso Django:

- `armado.reabrir_armado_pedido`

Solo supervisores/administradores.

---

## 10) PDF del armado de pedido

Crear reporte nuevo (ReportLab), por ejemplo en `armado/reporte_armado.py`.

### Estructura del PDF

Encabezado:

- Empresa, fecha, nro armado, nro venta, cliente, estado, usuario.

Tabla principal (como pediste):

- Código
- Descripción
- Variante
- Cantidad Pedida
- Cantidad Pickeada
- Faltante
- Sobrante

Pie:

- Totales,
- Observaciones,
- Firma/confirmación.

En admin: botón `PDF` similar a fabricación.

---

## 11) Reglas de negocio críticas

1. No duplicar armado activo por venta.
2. No cerrar armado sin items.
3. No cerrar armado si está en estado cancelado.
4. Cierre debe ser transaccional:
   - recalcular diferencias,
   - emitir ajuste,
   - mover a estado final,
   - registrar evento.
5. Reapertura solo con permiso y trazabilidad.

---

## 12) Seguridad y concurrencia

Para evitar inconsistencias en picking concurrente:

- usar `select_for_update()` sobre `ArmadoPedidoItem` al registrar picks,
- operaciones de cierre dentro de `transaction.atomic()`,
- control optimista opcional (`updated_at`) para UI futura.

---

## 13) Plan técnico de implementación por fases

## Fase 1 - Base de datos y admin mínimo

1. Crear app `armado`.
2. Modelos:
   - `EstadoArmadoPedido`
   - `ArmadoPedido`
   - `ArmadoPedidoItem`
   - `ArmadoPedidoEvento` (recomendado)
3. Migraciones + índices + constraints únicos.
4. Registrar en admin con listados y filtros.
5. Comando inicial para estados por defecto.

## Fase 2 - Generación automática/manual

1. Agregar `Configuracion.gestionar_entrega`.
2. Integrar en `VentaRepository.finalizar()` creación automática condicional.
3. Agregar acción `crear_armado_pedido` en `VentaAdmin`.
4. Validación anti-duplicado con mensajes claros.

## Fase 3 - Picking y cierre

1. Servicios de pick por item.
2. Cálculo de faltantes/sobrantes.
3. Cierre transaccional de armado.
4. Reapertura con permisos + auditoría.

## Fase 4 - Ajuste tipo nota de crédito

1. Crear modelos de ajuste (si no existe módulo reutilizable).
2. Emisión automática al cierre con diferencias.
3. Política de re-liquidación en reapertura.

## Fase 5 - PDF y UX operativa

1. Reporte PDF de armado.
2. Botones admin (PDF, avanzar, cerrar, reabrir).
3. Endpoint base para pantalla exclusiva futura.

---

## 14) Pruebas recomendadas (mínimas)

1. **Creación automática:** con `gestionar_entrega=True`, cerrar venta en POS crea 1 armado.
2. **No duplicado:** cerrar venta de nuevo o acción manual repetida no crea segundo armado.
3. **Acción masiva admin:** crea para múltiples ventas y omite ya existentes.
4. **Picking:** actualiza cantidades y estados por item correctamente.
5. **Cierre con faltantes:** emite ajuste tipo NC y bloquea edición.
6. **Reapertura:** requiere permiso y deja trazabilidad.
7. **PDF:** genera columnas requeridas y datos correctos.

---

## 15) Mapeo de archivos a tocar

- `agenda/models.py` (nuevo boolean `gestionar_entrega`)
- `agenda/admin.py` (exponer flag en Configuración)
- `repositories/VentaRepository.py` (hook de creación automática)
- `venta/admin.py` (acción manual crear armado)
- `armado/models.py` (nuevos modelos)
- `armado/admin.py` (operativa admin)
- `armado/services.py` (lógica de negocio)
- `armado/views.py` (endpoints futuros de picking)
- `armado/reporte_armado.py` (PDF)
- `adestock/settings.py` (registrar app)

---

## 16) Criterio de alineación final (respuesta directa)

Sí, estamos alineados.

Tu pedido encaja muy bien en la base actual porque el sistema ya tiene:

- estados configurables,
- hooks por configuración en cierre de venta,
- acciones admin para operación,
- reportes PDF,
- y patrón de flujo operativo similar en fabricación.

La clave para hacerlo bien será:

1. idempotencia (no duplicar armados),
2. cierre/reapertura auditables,
3. ajuste económico automático por diferencias,
4. dejar backend listo para la pantalla exclusiva de picking.

---

## 17) Recomendación de naming (para evitar confusión con "entrega")

Como ya existe `entrega`/`entrega_ventas`, recomiendo:

- Flag nuevo: `gestionar_armado_pedidos` (más explícito),

si querés mantener tu wording exacto, también se puede usar:

- `gestionar_entrega`.

Sugerencia técnica: usar el nombre explícito (`gestionar_armado_pedidos`) y, si necesitás compatibilidad, dejar alias temporal.
