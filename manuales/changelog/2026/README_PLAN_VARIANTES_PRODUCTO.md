# Plan de Implementación: Variantes de Producto (Escalable y Compatible)

## Objetivo

Implementar variantes (talle, color, etc.) sin romper el sistema actual de:

- stock,
- precios,
- ventas en `/pos/`,
- costos y recetas.

Con reglas de negocio clave:

1. Si un producto tiene variantes, **no puede tener receta**.
2. Debe permitir **usar código por variante** o **no usarlo**.
3. En `/pos/`, al seleccionar producto con variantes, abrir **modal para elegir variante**.

---

## Resumen de decisión arquitectónica

Se recomienda mantener `Producto` como entidad operativa (SKU vendible real) y agregar jerarquía padre/hijo dentro del mismo modelo para minimizar impacto.

### Enfoque elegido

- `Producto` padre = modelo comercial (ej. "Remera Básica").
- `Producto` hijo = variante vendible (ej. "Remera Básica - Negra - Talle M").
- La venta, stock y precio siempre operan sobre el **hijo** (variante).

Ventaja: el 90% del código actual (que ya depende de `DetalleVenta.producto`, `ProductoPrecio.producto`, `stock_actual()`) se mantiene con cambios incrementales.

---

## Fase 1 — Modelo de datos (aditivo y backward-compatible)

## 1.1 Cambios en `producto.models.Producto`

Agregar campos:

- `producto_padre = models.ForeignKey('self', null=True, blank=True, related_name='variantes', on_delete=models.CASCADE)`
- `es_producto_base = models.BooleanField(default=False)`
- `usa_variantes = models.BooleanField(default=False)`
- `atributos_variante = models.JSONField(default=dict, blank=True)`  
  Ejemplo: `{"color": "Negro", "talle": "M"}`
- `requiere_codigo_en_variantes = models.BooleanField(default=False)` (solo relevante en padre)

Notas:

- Producto sin variantes: `usa_variantes=False`, `producto_padre=None`.
- Producto padre: `usa_variantes=True`, `es_producto_base=True`, `producto_padre=None`.
- Variante: `producto_padre != None`, `es_producto_base=False`.

## 1.2 Restricciones e índices

Agregar validaciones/constraints:

- Un producto hijo **no puede tener hijos** (solo 1 nivel).
- Un hijo no puede apuntar a sí mismo.
- En padre con `usa_variantes=True`: impedir `fabricacion_propia`.
- Si existe al menos una variante activa, impedir asignar `fabricacion_propia` al padre.
- Unicidad recomendada de variante: `(producto_padre, atributos_variante)` (validación de aplicación; si se requiere fuerte en DB, usar hash de atributos normalizados).

Índices sugeridos:

- índice por `producto_padre`
- índice por `usa_variantes`
- índice por `es_producto_base`

## 1.3 Migración de datos inicial

Estrategia segura:

1. Crear campos nuevos nullable/default sin tocar lógica existente.
2. No convertir productos actuales automáticamente.
3. Mantener comportamiento actual para todos los productos existentes.

Resultado: despliegue sin corte.

---

## Fase 2 — Reglas de negocio (recetas y códigos)

## 2.1 Regla de receta

Regla obligatoria:

- Si `usa_variantes=True` o tiene `variantes.exists()`: `fabricacion_propia` debe ser `None`.
- Si `fabricacion_propia` está definida: no permitir activar `usa_variantes` ni crear variantes.

Puntos de validación:

- `Producto.clean()`
- formularios/admin (mensaje claro)
- endpoints AJAX de alta/edición de producto

Mensaje sugerido:

> "Un producto con variantes no puede tener receta asociada. Quite la receta o elimine variantes para continuar."

## 2.2 Regla de código de barras por variante (opcional)

Comportamiento:

- Si `requiere_codigo_en_variantes=True`: toda variante debe tener `codigo_barras`.
- Si `False`: `codigo_barras` en variantes es opcional.

Importante:

- Mantener `codigo_barras` único global cuando no es `null` (ya existe en el modelo).
- El padre puede tener o no código (según negocio), pero no se usa para descontar stock.

---

## Fase 3 — Precios, stock y costos

## 3.1 Precios

- `ProductoPrecio` permanece igual, asociado a `Producto` (variante).
- No crear precios en padre cuando `usa_variantes=True`.
- En UI/admin: ocultar o bloquear inline de precios en padre con variantes.

## 3.2 Stock

- Stock operativo solo en variantes.
- Para padre: mostrar stock agregado = suma de `stock_actual()` de variantes.
- Bloquear movimientos directos de stock del padre (mermas, transferencias, compras sobre padre).

## 3.3 Costos

- Costo por variante (permite diferencias por color/talle/proveedor).
- Reportes pueden mostrar:
  - detalle por variante,
  - agregado por producto padre.

---

## Fase 4 — Admin y ABM de productos

## 4.1 Admin de Producto

Agregar secciones:

- Datos del padre (`usa_variantes`, `requiere_codigo_en_variantes`).
- Inline de variantes (nombre, atributos, costo, código, habilitar_stock, habilitar_venta).

Reglas UI:

- Si es padre con variantes:
  - deshabilitar receta,
  - deshabilitar inline de precios del padre,
  - mostrar acción "Gestionar variantes".
- Si es variante:
  - bloquear edición de campos heredables opcionales (marca/categoría según decisión).

## 4.2 API/endpoint de producto

Extender payload para POS con:

- `usa_variantes`
- `variantes: [{id, nombre, atributos_variante, codigo_barras, stock_actual, precios...}]`

---

## Fase 5 — POS `/pos/`: modal de selección de variante

## 5.1 Flujo esperado

1. Usuario selecciona producto en grilla/buscador.
2. Si `usa_variantes=False`: comportamiento actual.
3. Si `usa_variantes=True`: abrir modal con variantes.
4. Usuario elige variante.
5. Se agrega al carrito la variante (`DetalleVenta.producto = variante`).

## 5.2 Requisitos del modal

Mostrar por variante:

- nombre/atributos (ej. Negro / M),
- precio principal,
- stock disponible (si aplica bloqueo por stock),
- código de barras (si existe).

Controles:

- buscador rápido por atributo/código,
- confirmación de selección,
- cerrar modal sin agregar ítem.

## 5.3 Compatibilidad con scanner

- Si escanean código de variante: agregar directo sin modal.
- Si escanean código de padre (si existe): abrir modal para elegir variante.

---

## Fase 6 — Ventas, notas de crédito/débito y reportes

## 6.1 Ventas y detalle

- No cambiar estructura principal: `DetalleVenta.producto` ya soporta SKU.
- Guardar siempre variante para máxima trazabilidad.

## 6.2 Notas de ajuste

- Ajustes de inventario y crédito/débito sobre la variante vendida.
- En impresión/reporte, mostrar nombre padre + atributos de variante.

## 6.3 Reportes

Agregar filtros opcionales:

- por padre,
- por variante,
- consolidado por padre.

---

## Fase 7 — Migraciones y despliegue por etapas

## 7.1 Orden recomendado

1. Migración de esquema (campos nuevos).
2. Deploy backend con validaciones suaves + logs.
3. Activar admin de variantes (sin POS aún).
4. Cargar primeros productos con variantes.
5. Activar modal en POS.
6. Ajustar reportes.

## 7.2 Feature flags sugeridos

- `activar_variantes_producto`
- `activar_modal_variantes_pos`

Permite rollback funcional sin revertir migraciones.

---

## Fase 8 — Plan de pruebas (mínimo obligatorio)

## 8.1 Unit tests

- Producto con variantes + receta => inválido.
- Producto con receta + intentar crear variante => inválido.
- `requiere_codigo_en_variantes=True` sin código => inválido.
- Stock padre = suma de variantes.

## 8.2 Integración POS

- Click en producto simple agrega directo.
- Click en producto con variantes abre modal.
- Elegir variante agrega ítem correcto al carrito.
- Scanner por código de variante agrega directo.

## 8.3 Regresión crítica

- Venta normal sin variantes.
- Devolución/anulación y notas de ajuste.
- Cálculo de costos y rentabilidad.
- Reportes diarios/cierre de caja.

---

## Riesgos y mitigaciones

1. **Riesgo:** mezcla de stock en padre e hijo.  
   **Mitigación:** bloquear movimientos en padre con `usa_variantes=True`.

2. **Riesgo:** duplicación de variantes por atributos en distinto orden JSON.  
   **Mitigación:** normalizar claves (`lower/trim/sort`) antes de guardar.

3. **Riesgo:** UX lenta en productos con muchas variantes.  
   **Mitigación:** paginar/buscar en modal y limitar payload inicial.

4. **Riesgo:** confusión operativa con códigos opcionales.  
   **Mitigación:** flag claro por padre y validación consistente en alta/edición.

---

## Checklist de aceptación funcional

- [ ] Un producto con variantes no acepta receta.
- [ ] Un producto con receta no acepta variantes.
- [ ] Se puede configurar si variantes requieren código o no.
- [ ] POS abre modal al seleccionar producto con variantes.
- [ ] Carrito guarda la variante elegida.
- [ ] Stock se descuenta de la variante.
- [ ] Reportes permiten ver agregado por padre y detalle por variante.

---

## Recomendación final

Implementar en 2 entregas:

1. **Entrega A (Backoffice):** modelo + validaciones + admin de variantes + stock/precio por variante.
2. **Entrega B (POS):** modal de selección + scanner + ajustes de reportes.

Así reduces riesgo operativo, mantienes compatibilidad con el sistema actual y habilitas escalabilidad real para distintos tipos de negocio.
