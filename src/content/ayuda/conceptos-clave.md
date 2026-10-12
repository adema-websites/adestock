---
id: "conceptos-clave"
slug: "conceptos-clave"
title: "Conceptos clave: stock, precios, cuentas corrientes y turnos de caja"
description: "Cuatro ideas explican casi todo lo que hace el sistema. Cada una remite al tutorial donde se usa."
orden: 2
status: "draft"
source_path: "03-conceptos/README.md"
source_hash: "621fefb91de3f1df881c1d3f515817fccfce8624666fd4e6a9c288da70fb8ea6"
product_version: "3.0.0"
verified_at: "2026-10-12"
reviewed_at: null
reviewed_by: null
synonyms: ["conceptos","de dónde sale el stock","costo","rentabilidad","fiado","arqueo","turno"]
social_image: null
---
Cuatro ideas explican casi todo lo que hace el sistema. Cada una remite al tutorial donde se usa.

## 1. Stock: de dónde sale el número

El stock de un producto **no es un número guardado**: se **calcula** cada vez, sumando y restando movimientos.

| Suma | Resta |
|---|---|
| Compras confirmadas | Ventas |
| Ajustes de inventario a favor (incluye el conteo) | Mermas |
| Fabricación (producto elaborado) | Consumo de ingredientes en fabricación |
| Transferencias que **entran** al depósito | Transferencias que **salen** |
| **Notas de crédito aplicadas** (mercadería no entregada) | Notas de débito aplicadas |

Ideas para no confundirse:

- **Por depósito.** El stock se calcula por depósito. Cada caja vende desde el depósito que tiene asignado.
- **Disponible vs. físico.** Con el ajuste *Seguimiento de entregas* (viene activado), lo vendido deja de estar **disponible** al instante, pero el **físico** baja recién cuando la venta se marca como **entregada**. Mientras tanto figura como *comprometido*. El **conteo** compara contra el físico, para no generar sobrantes falsos.
- **Corregir el stock** se hace con un **ajuste de inventario** (o un conteo), nunca «pisando» el número: así queda quién, cuándo y por qué.

→ Tutoriales: [23 Conteo](/tutoriales/contar-stock/), [24 Ajustes, mermas y transferencias](/tutoriales/ajustar-stock-mermas-transferencias/), [35 Notas de crédito](/tutoriales/notas-de-credito-y-debito/).

## 2. Precios, costo y rentabilidad

- Cada producto tiene un **costo** y una o más **presentaciones** (unidad, pack…), cada una con su **precio**.
- La **rentabilidad** es el margen. Por defecto se calcula **sobre el precio de venta**: `precio = costo ÷ (1 − rentabilidad)`. Una rentabilidad del 30 % significa que de cada $100 cobrados, $30 son ganancia. Se puede configurar sobre el costo (`costo × (1 + rentabilidad)`).
- Podés escribir el **precio** y el sistema calcula la rentabilidad, o al revés.
- Los **precios masivos** cambian solo el **precio**, no el costo, guardan los valores anteriores y se pueden **revertir**.
- Una **oferta** no mueve stock ni toca el precio de lista: solo cambia el precio al que se cobra. Si hay varias sobre el mismo producto, gana **la más barata**.
- Con *Congelar precio de venta al actualizar costo*, una compra más cara **no sube** el precio de venta (tu margen baja).

→ Tutoriales: [03 Productos](/tutoriales/cargar-productos/), [25 Precios masivos](/tutoriales/actualizar-precios-y-rentabilidad/), [26 Ofertas](/tutoriales/crear-ofertas-y-promociones/).

## 3. Cuentas corrientes (fiado)

- Vender **a cuenta corriente** crea una **deuda** del cliente. **No entra plata** a la caja: no cuenta en el arqueo de efectivo.
- La deuda guarda el precio de la venta. Hay dos saldos: el **normal** (lo que falta cobrar) y el **actualizado**, que se calcula **al consultar** con los precios de hoy y no se guarda.
- Los **adelantos** son saldo a favor del cliente y se descuentan al cobrar.
- Las deudas **solo se cancelan cobrando** desde el POS. Ese cobro entra al arqueo del turno y a la billetera del medio elegido. Un cobro mal cargado no se borra: se **anula** desde el panel y las deudas se restauran.
- Con los **proveedores** pasa lo mismo, a la inversa: una compra a cuenta corriente es deuda **tuya**, y se paga desde el POS.

→ Tutoriales: [09](/tutoriales/vender-fiado-cuenta-corriente/), [16](/tutoriales/consultar-cuenta-corriente-cliente/), [17](/tutoriales/cobrar-deuda-cliente/), [21](/tutoriales/pagar-proveedor/).

## 4. Turnos de caja y arqueo

- Un **turno** empieza cuando el cajero abre la caja con su efectivo inicial y termina cuando la cierra contando el efectivo.
- **Todo pago, gasto, retiro y pago a proveedor guarda el turno al que pertenece.** El cierre calcula lo que **debería haber** (inicial + cobros en efectivo − gastos − retiros − pagos en efectivo) y lo compara con lo **contado**: la diferencia es el faltante o sobrante.
- Un turno **cerrado no se modifica**: su PDF muestra siempre los mismos números.
- Para cerrar, las **compras pagadas en el turno tienen que estar confirmadas**.
- Los pagos, cobros, gastos y retiros **se cargan solo desde el POS**, no desde el panel.
- Las **notas de crédito** aplicadas durante el turno **restan** del medio elegido, y las de débito **suman**.

→ Tutoriales: [12 Turno](/tutoriales/abrir-y-cerrar-caja/), [13 Gastos y retiros](/tutoriales/registrar-gastos-y-retiros/), [32 Controlar turnos](/tutoriales/controlar-turnos-caja-panel/).

## Qué pasa cuando vendés (resumen)

| Qué | Efecto |
|---|---|
| Stock disponible | Baja al instante, en el depósito de tu caja |
| Stock físico | Baja al marcar la venta como entregada (con *Seguimiento de entregas*) o al vender (sin él) |
| Caja | Cada pago queda en tu turno |
| Billeteras | Cada pago mueve la billetera vinculada al medio |
| Cuenta corriente | La parte a CC queda como deuda |
| Ticket | Se imprime o se abre en pantalla según la configuración |

El sistema protege la venta contra el **doble clic**: si se confirma dos veces, el pago no se duplica.
