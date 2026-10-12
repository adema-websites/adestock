# Cambios implementados: Adelantos y cobro parcial en Cuenta Corriente

Fecha: 2026-02-25

## Objetivo
Permitir:
1. Registrar adelantos múltiples de un cliente (saldo a favor).
2. Cancelar deuda usando adelantos previos + pagos nuevos.
3. Ver faltante en tiempo real en el POS.
4. Mantener cambios de bajo impacto sobre el flujo existente.

---

## Archivos modificados

### 1) `venta/models.py`
Se agregó el nuevo modelo:
- `AplicacionPagoCliente`
  - `pago_cliente` (FK a `PagosClientes`)
  - `pago_venta` (FK a `PagosVentas`)
  - `monto_aplicado` (Decimal)
  - `fecha`

**Propósito:** registrar cuánto de cada cobro/adelanto se aplicó a cada deuda.

---

### 2) `venta/migrations/0003_aplicacionpagocliente.py`
Nueva migración que crea la tabla `AplicacionPagoCliente`.

---

### 3) `venta/views.py`
Se implementaron utilidades internas:
- `_decimal_or_zero(valor)`
- `_saldo_a_favor_cliente(cliente)`
- `_pagos_disponibles_cliente(cliente)`
- `_restante_deuda_pago_venta(pago_venta)`

#### Endpoint actualizado: `pos_obtener_deudas_cliente`
Cambios:
- Ahora devuelve montos **restantes reales** por deuda (no solo total original).
- Calcula montos actualizados proporcionales al restante.
- Agrega al JSON:
  - `saldo_a_favor`
  - `total_deuda`
  - `faltante_neto`

#### Endpoint actualizado: `pos_cobrar_deuda`
Cambios:
- Ya no exige igualdad estricta entre pago nuevo y deuda total.
- Permite cobrar usando:
  - pagos nuevos,
  - y/o saldo a favor preexistente.
- Si no alcanza, devuelve error con faltante exacto.
- Aplica montos a deudas seleccionadas en orden (fecha/id) creando registros en `AplicacionPagoCliente`.
- Marca `PagosVentas.cancelado=True` solo cuando la deuda queda totalmente cubierta.
- Mantiene compatibilidad de historial vinculando deudas canceladas al primer `PagosClientes` nuevo cuando existe.

#### Nuevo endpoint: `pos_registrar_adelanto`
- Ruta POST para registrar adelantos sin seleccionar deudas.
- Crea uno o varios `PagosClientes` confirmados (`estado=True`) y deja saldo a favor.
- Devuelve saldo a favor actualizado.

#### Endpoint actualizado: `obtener_saldo_cliente`
- Ahora calcula saldo con lógica neta real:
  - `saldo = deuda_pendiente - saldo_a_favor`
- Devuelve:
  - `total_deuda_pendiente`
  - `saldo_a_favor`

---

### 4) `venta/urls.py`
Se agregó ruta:
- `pos/registrar-adelanto/` -> `views.pos_registrar_adelanto`

---

### 5) `venta/templates/venta/pos.html`
En el modal de cobro de cuentas corrientes:

#### UI
- Se agregó botón `Adelanto` junto a `Buscar Deudas`.
- Se agregó indicador visual:
  - `Saldo a Favor`.
- Se actualizó leyenda de cálculo:
  - `Restante = Total Seleccionado - (Saldo a Favor + Pagos nuevos)`.

#### Lógica JS
- Nueva variable global: `saldoFavorCobro`.
- Al buscar deudas, carga también saldo a favor desde backend.
- `actualizarTotalesCobro()` ahora considera saldo a favor + pagos nuevos.
- El botón de confirmar cobro se habilita cuando el disponible cubre la deuda seleccionada.
- Se eliminó la validación obligatoria de “debe haber pagos nuevos” para permitir cancelar con adelantos existentes.
- Nuevo handler `#btn-registrar-adelanto`:
  - registra adelanto vía AJAX,
  - limpia pagos ingresados,
  - refresca deudas/saldo.

---

### 6) `agenda/models.py`
Método actualizado: `Cliente.cuenta_corriente()`
- Ahora contempla:
  - deuda restante real por aplicación,
  - saldo a favor no aplicado.
- Retorna saldo neto de cuenta corriente.

---

## Comportamiento final

### Caso 1: adelantos semanales
- Cliente adelanta 200k varias veces.
- El sistema acumula ese importe como saldo a favor.

### Caso 2: ponerse al día
- Seleccionás deudas en POS.
- El sistema descuenta saldo a favor automáticamente.
- Muestra faltante real.
- Podés pagar solo la diferencia.

### Caso 3: cancelar con saldo ya existente
- Si el saldo a favor cubre la deuda seleccionada, se puede confirmar cobro sin cargar nuevos medios.

### Caso 4: historial y comprobante de adelanto
- Los movimientos sin deudas asociadas ni aplicaciones se muestran como **Adelanto** (ya no como Cobro Deuda).
- Al registrar adelanto desde POS se imprime automáticamente un **comprobante de adelanto**.
- En reimpresión, si el pago no tiene deudas asociadas, el encabezado también se imprime como **Recibo de Adelanto**.

---

## Ajustes adicionales (26/02/2026)

### `venta/views.py`
- `pos_registrar_adelanto`:
  - ahora intenta imprimir comprobante de adelanto al guardar;
  - devuelve mensaje de impresión en la respuesta.
- `pos_obtener_pagos_clientes`:
  - clasifica cada `PagosClientes` como:
    - `adelanto` si no tiene deudas asociadas ni aplicaciones,
    - `cobro_deuda` en caso contrario.
- `pos_detalle_pago_cliente`:
  - acepta `tipo=adelanto`;
  - devuelve `total_aplicado` y `saldo_disponible` para el detalle.

### `venta/templates/venta/pos.html`
- Historial de pagos:
  - muestra badge **Adelanto** cuando `tipo === 'adelanto'`.
- Reimpresión:
  - habilitada para `cobro_deuda` y `adelanto`.
- Modal detalle:
  - para adelanto muestra total, aplicado y saldo disponible.

### `venta/printer_manager.py`
- `imprimir_recibo_cobro_escpos`:
  - nuevo parámetro `tipo_comprobante` (`'cobro_deuda'` o `'adelanto'`);
  - imprime encabezado y detalle según el tipo;
  - muestra saldo neto actualizado (deuda pendiente vs saldo a favor).
- `reimprimir_recibo_cobro_escpos`:
  - detecta adelanto si no hay deudas asociadas y ajusta textos del comprobante.
- `reimprimir_recibo_cobro_red`:
  - corrige firma para aceptar `caja_config`;
  - también adapta el texto a adelanto cuando corresponde.

---

## Validación ejecutada
Se ejecutó:
- `manage.py check` ✅ sin errores.
- `showmigrations venta` ✅ detecta `0003_aplicacionpagocliente`.

---

## Pendiente de despliegue
En el entorno que uses para producción, ejecutar:

```bash
python manage.py migrate venta
```

(En tu entorno local con venv actual: `c:/Users/kevin/OneDrive/Escritorio/adestock/venv/Scripts/python.exe manage.py migrate venta`)
