---
id: "vender-fiado-cuenta-corriente"
slug: "vender-fiado-cuenta-corriente"
title: "Cómo vender fiado a cuenta corriente en ADEstock"
description: "Registrá una venta fiada en ADEstock: seleccioná un cliente con cuenta corriente, cargá el importe adeudado y combiná un pago parcial si corresponde."
category: "clientes"
priority: "P1"
roles: ["cajero","dueno"]
surface: ["pos"]
status: "published"
tiempo: "2 minutos"
necesitas: "un cliente registrado con la cuenta corriente habilitada (ver Crear y editar clientes)"
para_quien: "cajeros y dueños"
modulo: "venta (POS), agenda (Cliente)"
permiso: "ninguno; el cliente debe tener la cuenta corriente habilitada"
source_path: "01-manual-usuario/09-vender-a-cuenta-corriente.md"
source_hash: "27ea6829b9d66db736c571bd2d231499107903b0011160b86c720f9f2bd6130a"
product_version: "3.0.0"
verified_at: "2026-10-12"
reviewed_at: "2026-10-13"
reviewed_by: "ademasistemas"
synonyms: ["fiar","fiado","cuenta corriente","deuda"]
related: ["crear-y-editar-clientes","consultar-cuenta-corriente-cliente","cobrar-deuda-cliente"]
social_image: "/social/vender-fiado-cuenta-corriente-v1.jpg"
---
## Para qué sirve

Vender "fiado" es entregar la mercadería ahora y cobrar después. Esta guía sirve para que ese fiado **no quede anotado en un cuaderno**: la deuda queda en la cuenta del cliente, con su detalle, y la cobrás más adelante desde el sistema (ver [cobrar la deuda de un cliente](/tutoriales/cobrar-deuda-cliente/)). Para venderle así, el cliente tiene que estar registrado con la cuenta corriente habilitada.

## Qué vas a lograr

Vas a **registrar una venta fiada en ADEstock** para que el importe pendiente quede en la cuenta corriente del cliente. Podés dejar el total como deuda o cobrar una parte en el momento y financiar el resto.

Necesitás asignar la venta a un cliente registrado con cuenta corriente habilitada. El importe fiado no representa efectivo recibido en la caja.

## Antes de empezar

- El cliente tiene que estar creado y con **Habilitar Cuenta Corriente** tildado.
- La venta no puede ser a *Consumidor Final*: hay que asignarle el cliente.
- El medio de cobro **Cuenta Corriente** tiene que estar activo en tu caja (viene así desde el onboarding).

## Paso a paso

### 1. Armá el carrito

Cargá los productos como en cualquier venta (ver [Hacer una venta](/tutoriales/hacer-una-venta/)).

### 2. Asignale el cliente a la venta

Tocá **Cambiar** (o **F9**) junto al cliente.

![Botón para cambiar cliente](../../assets/tutoriales/09-cuenta-corriente-venta/01-cambiar-cliente.png)

Se abre la lista de clientes. Los que tienen cuenta corriente habilitada llevan la etiqueta **CC**. Buscá por nombre o documento y tocá el cliente.

![Seleccionar cliente](../../assets/tutoriales/09-cuenta-corriente-venta/02-seleccionar-cliente.png)

### 3. Mirá su cuenta antes de cobrar

Apenas elegís un cliente con cuenta corriente, el panel de la derecha muestra un **resumen de su cuenta**:

![Cliente asignado con su resumen](../../assets/tutoriales/09-cuenta-corriente-venta/03-cliente-asignado.png)

| Dato | Qué significa |
|---|---|
| **Deuda total** | Lo que el cliente debe hoy, tal como se le vendió |
| **Adelantos disp.** | Plata que dejó a favor (anticipos) y todavía no se aplicó |
| **Deuda real** | `Deuda total − Adelantos`. Es lo que realmente debe: *Debe $…*, *A favor $…* o *Al día* |

### 4. Cobrá con Cuenta Corriente

Tocá **COBRAR** (F4). Con un cliente con cuenta corriente, el botón **Cuenta Corriente** ahora está habilitado (con Consumidor Final aparece apagado).

![Cobro con cuenta corriente disponible](../../assets/tutoriales/09-cuenta-corriente-venta/04-cobro-cuenta-corriente-habilitada.png)

Elegí **Cuenta Corriente** y tocá **Exacto** para cargar todo el total. Después **Agregar pago**.

![Pago a cuenta corriente](../../assets/tutoriales/09-cuenta-corriente-venta/05-pago-a-cuenta-corriente.png)

> También podés **combinar**: una parte en efectivo y el resto a cuenta corriente. Se hace igual que en [Cobrar con varios medios de pago](/tutoriales/cobrar-con-varios-medios-de-pago/).

### 5. Confirmá y cerrá

Tocá **CONFIRMAR Y CERRAR**. La venta se cierra y el **importe cargado a cuenta corriente** queda como deuda del cliente. Si combinaste medios de pago, lo cobrado en el momento no se suma a esa deuda.

![Venta cerrada](../../assets/tutoriales/09-cuenta-corriente-venta/06-venta-cerrada.png)

## Qué pasa por detrás

| Qué | Detalle |
|---|---|
| Deuda | Se crea un pago "adeudado" por el monto a cuenta corriente, asociado a la venta y al cliente |
| Caja | Ese monto **no entra** al arqueo de efectivo (no se cobró plata) |
| Stock | Se mueve igual que en cualquier venta |
| Ticket | Si está activada la opción *Mostrar saldo de cuenta corriente en el ticket*, el ticket muestra saldo anterior, esta compra y total adeudado |
| Precios | La deuda guarda el precio de la venta; más adelante puede **actualizarse** si los precios suben (ver [Revisar la cuenta corriente de un cliente](/tutoriales/consultar-cuenta-corriente-cliente/)) |

## Problemas frecuentes

| Si te pasa… | Es porque… | Qué hacer |
|---|---|---|
| El botón *Cuenta Corriente* está apagado | El cliente es Consumidor Final, o no tiene cuenta corriente habilitada | Asignale un cliente con CC (F9) o habilitala desde *Gestión de clientes → Editar* |
| No aparece la etiqueta CC en la lista | El cliente no la tiene habilitada | Editá el cliente y tildá *Habilitar Cuenta Corriente* |
| Necesito saber cuánto me debe | - | Ver [Revisar la cuenta corriente de un cliente](/tutoriales/consultar-cuenta-corriente-cliente/) |
| El cliente quiere pagar su deuda | - | Ver [Cobrar la deuda de un cliente](/tutoriales/cobrar-deuda-cliente/) |

## Cómo comprobar que salió bien

Después de cerrar la venta, elegí nuevamente al cliente con **F9** y revisá el resumen de su cuenta. La deuda debe incluir el importe que cargaste a cuenta corriente; si combinaste medios, solo esa parte queda pendiente. Cuando el cliente pague, registrá el cobro desde **Cobrar a un cliente**.

## Siguiente paso

- [crear y editar clientes en ADEstock](/tutoriales/crear-y-editar-clientes/)
- [consultar saldos y cuentas corrientes en ADEstock](/tutoriales/consultar-cuenta-corriente-cliente/)
- [cobrar deudas de clientes en ADEstock](/tutoriales/cobrar-deuda-cliente/)
