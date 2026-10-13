---
id: "notas-de-credito-y-debito"
slug: "notas-de-credito-y-debito"
title: "Cómo aplicar y anular notas de crédito y débito en ADEstock"
description: "Revisá y aplicá notas de crédito por faltantes de pedidos en ADEstock. Consultá su efecto en stock y caja y cómo anularlas con una nota inversa."
category: "vender"
priority: "P2"
roles: ["dueno","administrativo"]
surface: ["panel"]
status: "published"
tiempo: "5 minutos"
necesitas: "una nota generada desde el picking (ver Armado de pedidos)"
para_quien: "el dueño y administrativos"
modulo: "venta (Notas de Ajuste), armado"
permiso: "acceso al panel de administración"
source_path: "01-manual-usuario/35-notas-de-credito-y-debito.md"
source_hash: "da733fcc447491665acf8ac5a0e90f8fa09d54562daada7ab447dde8bb9ba741"
product_version: "3.0.0"
verified_at: "2026-10-12"
reviewed_at: "2026-10-13"
reviewed_by: "ademasistemas"
synonyms: ["nota de crédito","nota de débito","diferencia de armado","ajuste de venta"]
related: ["armar-pedidos-picking","controlar-turnos-caja-panel","billeteras-y-cuentas"]
social_image: "/social/notas-de-credito-y-debito-v1.jpg"
---
## Para qué sirve

Si cobraste algo que finalmente no se pudo entregar, la venta tiene que corregirse. Las notas sirven para eso: la **nota de crédito** devuelve al stock la mercadería no entregada y resta ese dinero de la caja, y la **nota de débito** deshace una nota de crédito. Nacen del [armado de pedidos](/tutoriales/armar-pedidos-picking/), así que esta guía es para entender y aplicar lo que el sistema ya generó.

## Qué vas a lograr

Vas a **revisar, aplicar y anular notas de crédito y débito en ADEstock** para ajustar una venta con faltantes en el armado del pedido. La guía explica qué revisar en cada línea y cómo elegir el medio de pago de la devolución.

Una nota en borrador todavía no afecta stock ni caja. Al aplicarla se registran sus efectos; si necesitás anularla, el sistema conserva el historial mediante una nota inversa.

| Nota | Cuándo | Qué hace |
|---|---|---|
| **Nota de crédito** (`NC-000001`) | Faltó mercadería al armar el pedido | **Devuelve** esa mercadería al stock y **resta** el dinero de la caja del medio elegido |
| **Nota de débito** (`ND-000001`) | Se anuló una nota de crédito | Hace lo **inverso**: vuelve a sacar la mercadería del stock y a sumar el dinero |

Las notas **no se cargan desde el POS**: nacen del armado de pedidos y se **aplican en el panel**.

## Cómo nace una nota

1. Se arma un pedido y falta mercadería (ver [Preparar pedidos con picking móvil](/tutoriales/armar-pedidos-picking/)).
2. En el celular, **Generar Nota de Crédito** → se crea en estado **Borrador**.
3. El dueño o administrativo la **revisa y la aplica** en el panel.

Una nota en **borrador no mueve nada**: ni stock ni caja. Recién al **aplicarla** surte efecto.

## Paso a paso

### 1. Ubicá la nota

En el panel: **Venta → Notas de Ajuste**.

![Lista de notas](../../assets/tutoriales/35-notas-de-credito-y-debito/02-lista-de-notas.png)

| # | Columna | Qué es |
|---|---|---|
| 1 | **Estado** | *Borrador* (sin efecto), *Aplicada* o *Anulada* |
| 2 | **Aplicar** | Botón que aplica la nota (solo en borradores) |
| - | **Codigo / Tipo** | `NC-…` crédito (verde) o `ND-…` débito (rojo) |
| - | **Venta original** y **Armado pedido** | De qué venta y de qué armado viene |
| - | **Medio de pago** | Con qué medio se devuelve (o cobra) el dinero |
| - | **Movimiento financiero aplicado** | Tilde verde cuando el dinero ya impactó en la billetera |
| - | **Total** | Valor de lo que faltó, a precio de venta |

Desde la lista de **ventas**, la columna **Nota Crédito** muestra el botón **NC PDF** cuando la venta tiene una nota de crédito aplicada, para imprimir el comprobante.

![Columnas Armado y Nota Crédito de las ventas](../../assets/tutoriales/35-notas-de-credito-y-debito/01-ventas-armado-y-nota.png)

### 2. Revisá el detalle

Tocá el código de la nota. En **Información Principal** ves la venta, el armado y el **medio de pago**; en la pestaña **Detalles de Nota de Ajuste**, los productos y cantidades:

![Líneas de la nota](../../assets/tutoriales/35-notas-de-credito-y-debito/03b-lineas-de-la-nota.png)

Cada línea muestra el producto, la **cantidad** que faltó, el **precio unitario** de la venta original y el **total**. Mientras la nota esté en borrador podés corregir el medio de pago o las líneas. Una vez aplicada, queda **solo de lectura**.

> **Ojo con el medio de pago:** determina **de qué medio se resta el dinero** en el cierre de caja. Si la venta se pagó con transferencia, elegí transferencia; si fue efectivo, efectivo. Una nota de crédito sin medio no se puede aplicar.

### 3. Aplicala

Tocá **Aplicar** en la fila de la nota (o tildala y usá la acción **Aplicar notas seleccionadas**). El sistema confirma: *«Nota NC-000001 aplicada exitosamente»*.

![Nota aplicada](../../assets/tutoriales/35-notas-de-credito-y-debito/04-nota-aplicada.png)

Ahora el estado es **Aplicada**, el botón desaparece y **Movimiento financiero aplicado** queda en verde.

### 4. Anular una nota aplicada

Si la nota estuvo mal, tildala y elegí la acción **Anular notas seleccionadas** → **Ejecutar**.

![Anular nota](../../assets/tutoriales/35-notas-de-credito-y-debito/05-anular-nota.png)

El sistema **no borra nada**: marca la nota original como **Anulada** y crea automáticamente una **nota inversa** (una *nota de débito* si anulás un crédito) ya aplicada, con las mismas líneas.

![Nota anulada con su débito](../../assets/tutoriales/35-notas-de-credito-y-debito/06-nota-anulada-con-debito.png)

Así queda el rastro completo: el crédito, su anulación y la nota que la compensa. Solo se pueden anular notas **aplicadas**.

### 5. Crear una nota a mano (si hace falta)

**Agregar Nota de Ajuste** permite crear una nota sin pasar por el celular. Elegí el **tipo**, la **venta original**, el **armado** (es obligatorio: toda nota cuelga de un armado) y el **medio de pago**; después cargá las líneas en la pestaña de detalles y aplicala. Usalo solo para corregir casos puntuales, por ejemplo cuando se finalizó un pedido **sin** generar la nota de crédito.

## Qué pasa por detrás

| Al aplicar una nota… | Crédito | Débito |
|---|---|---|
| **Stock** | **Suma** las cantidades al stock del depósito del armado | **Resta** |
| **Caja (cierre de turno)** | **Resta** el total del medio elegido, en el turno donde se aplicó | **Suma** |
| **Billetera** | Registra un **egreso** en la billetera del medio (si el medio tiene billetera y no es cuenta corriente) | Registra un **ingreso** |

Detalles útiles:

- El efecto en la **caja** cuenta en el turno **cuyo horario incluye el momento de la aplicación**, para la caja de la venta original. Aplicala con el turno de esa caja **abierto**: si en ese momento no hay turno abierto, la nota no entra en ningún cierre.
- El stock se calcula siempre sumando las notas **aplicadas**; por eso una nota anulada compensada con su débito deja el stock como estaba.
- La nota de crédito resta **a precio de venta**, no a costo.

## Problemas frecuentes

| Si te pasa… | Es porque… | Qué hacer |
|---|---|---|
| La nota existe pero el stock no cambió | Está en **borrador** | Aplicala |
| «La nota de crédito debe tener medio de pago…» | La nota no tiene medio y no se pudo deducir de la venta | Abrila (borrador), elegí el medio y aplicala |
| No puedo editar la nota | Ya está aplicada o anulada | Si está aplicada, anulala y creá una nueva si corresponde. Si ya está anulada, revisá su nota inversa antes de crear otra |
| Un pedido cerrado no tiene nota de crédito | Se finalizó sin generarla | Reabrilo en el celular y generá la nota, o creala a mano (paso 5) |
| La caja del día no cuadra por una nota | La nota se aplicó en un turno distinto al de la venta | Mirá el arqueo del turno: las notas aparecen como movimientos del medio (ver [Controlar un turno](/tutoriales/controlar-turnos-caja-panel/)) |

## Cómo comprobar que salió bien

Confirmá que la nota figure como **Aplicada** y corresponda a la venta, productos, cantidades y medio de pago correctos. Revisá el efecto en el depósito y en el turno de la aplicación. Si la anulaste, comprobá el estado **Anulada** de la original y la nota inversa generada.

## Siguiente paso

- [preparar pedidos con picking móvil en ADEstock](/tutoriales/armar-pedidos-picking/)
- [revisar turnos y cierres de caja en ADEstock](/tutoriales/controlar-turnos-caja-panel/)
- [controlar billeteras, cuentas y saldos en ADEstock](/tutoriales/billeteras-y-cuentas/)
