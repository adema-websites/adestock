# Mejora nivel X - Control de Turno Multidía + Reformulación de Cierre de Caja (14-02-2026)

## Objetivo
Implementar una política configurable para evitar ventas con turnos abiertos de días anteriores (cuando la empresa así lo defina), sin romper el flujo actual de turnos nocturnos, y mejorar la experiencia del modal de cierre de caja para que muestre información real del turno activo.

---

## Resumen funcional

Se implementaron dos mejoras principales:

1. Control de turnos abiertos multidía configurable por empresa.
2. Rediseño del modal de cierre de caja para operar sobre el turno activo con más contexto operativo.

---

## 1) Control de turnos abiertos multidía (configurable)

### Nueva configuración de empresa
Se agregó el campo booleano en Configuración:

- permitir_turno_abierto_multidia
- Nombre visible: Permitir operar con turno abierto de otro día

Comportamiento:

- En True: se mantiene el comportamiento libre actual.
- En False: si existe un turno abierto de un día anterior y ese turno tiene movimientos, se bloquean ventas hasta cerrar caja.

### Regla de bloqueo exacta
El bloqueo solo ocurre cuando se cumplen estas condiciones:

1. El turno está ABIERTO.
2. La fecha de apertura del turno es menor al día actual.
3. El turno tiene movimientos registrados.
4. La configuración permitir_turno_abierto_multidia está en False.

### Qué se considera movimiento
Para esta regla se toman como movimientos:

- pagos_ventas
- pagos_clientes no anulados
- retiros
- gastos confirmados

---

## 2) Modal de advertencia y acceso rápido a cierre

Cuando se detecta bloqueo por turno multidía:

- El backend responde con estado 403 y bandera bloqueo_turno_multidia.
- El POS muestra modal de advertencia (SweetAlert) con mensaje claro.
- El modal incluye acción directa Ir a cierre de caja.

Esto se aplica en:

- creación de carrito
- cierre de venta
- carga inicial de POS (si ya entra con turno pendiente)

---

## 3) Reformulación del modal de Cierre de Caja

Se mejoró el modal para enfocarlo en el turno activo real:

### Cambios UX

- Se eliminó selector de fecha.
- Se eliminó selector de cajero.
- Se agregó bloque informativo con:
  - Cajero
  - Caja
  - Número de turno
  - Estado del turno
  - Fecha y hora de apertura
- Se mantiene el campo Efectivo en Caja (Real) para arqueo.

### Resultado
El usuario ahora entiende qué turno está cerrando y evita errores por cierre sobre fechas/cajeros incorrectos.

---

## 4) Cambios técnicos por archivo

### agenda/models.py
- Nuevo campo en Configuracion:
  - permitir_turno_abierto_multidia = BooleanField(default=True)

### agenda/admin.py
- Se expone permitir_turno_abierto_multidia dentro de Configuración de Ventas.

### agenda/migrations/0005_configuracion_permitir_turno_abierto_multidia.py
- Migración para persistir el nuevo campo en base de datos.

### venta/turnos.py
- Se agregó helper interno para detectar movimientos de turno.
- Se agregó validar_turno_multidia_para_ventas(turno, configuracion) como regla central.

### venta/views.py
- Se aplicó validación en:
  - pos_crear_carrito
  - pos_view (para disparo de modal al abrir POS)
  - pos_cerrar_venta
- Se enviaron flags al template:
  - bloquear_turno_multidia
  - mensaje_bloqueo_turno_multidia

### venta/templates/venta/pos.html
- Se agregó función mostrarModalTurnoMultidiaPendiente.
- Se integra modal de advertencia en errores 403 por bloqueo_turno_multidia.
- Se reformuló modal de cierre de caja:
  - elimina fecha/cajero
  - muestra datos del turno activo
  - cierre contra /cierre-caja/ del turno actual

---

## 5) Compatibilidad y alcance

### Qué no se cambió
- No se forzó auto-cierre diario rígido.
- No se alteró la lógica principal de cálculo de cierre de caja.
- No se modificó el modelo de turnos para dividir automáticamente por fecha.

### Por qué esta solución es segura
- Mantiene compatibilidad con turnos nocturnos.
- Permite política flexible por empresa (activar o desactivar).
- Evita cierres incorrectos por selección manual de fecha/cajero en modal.

---

## 6) Activación operativa

1. Ir a Admin > Configuración.
2. En Configuración de Ventas:
   - activar o desactivar Permitir operar con turno abierto de otro día.

Interpretación:

- Activado: operación libre entre días (comportamiento histórico).
- Desactivado: obliga a cerrar turno anterior con movimientos para continuar ventas.

---

## 7) Escenarios de prueba recomendados

### Caso A - Config en True
- Abrir turno ayer con movimientos.
- Hoy operar POS.
- Resultado esperado: permite vender.

### Caso B - Config en False, turno anterior con movimientos
- Abrir turno ayer y registrar ventas/retiros/gastos.
- Hoy intentar crear carrito o cerrar venta.
- Resultado esperado: bloqueo + modal + acceso rápido a cierre.

### Caso C - Config en False, turno anterior sin movimientos
- Abrir turno ayer sin movimientos.
- Hoy operar POS.
- Resultado esperado: no bloquea.

### Caso D - Cierre desde modal reformulado
- Abrir modal cierre de caja.
- Verificar datos visibles del turno activo.
- Confirmar cierre.
- Resultado esperado: cierre correcto del turno activo, sin selección manual de fecha.

---

## 8) Estado de implementación

Implementación completada y migración aplicada correctamente.
