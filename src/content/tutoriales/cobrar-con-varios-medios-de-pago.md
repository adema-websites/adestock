---
id: "cobrar-con-varios-medios-de-pago"
slug: "cobrar-con-varios-medios-de-pago"
title: "Cómo cobrar con varios medios de pago en ADEstock"
description: "Cobrá una venta con efectivo, tarjeta o transferencia en ADEstock. Combiná medios de pago, aplicá descuentos y revisá el faltante antes de cerrar."
category: "vender"
priority: "P1"
roles: ["cajero","dueno"]
surface: ["pos"]
status: "published"
tiempo: "2 minutos"
necesitas: "haber armado el carrito (ver Hacer una venta)"
para_quien: "cajeros y dueños"
modulo: "venta (POS → Cobro)"
permiso: "aplicar descuentos requiere \"Puede hacer descuentos\""
source_path: "01-manual-usuario/08-cobrar-con-varios-medios-de-pago.md"
source_hash: "fb6e6f5b22d1906202e7a93be7c3e2a280ea429e50bd1d84dc5641fa6086771a"
product_version: "3.0.0"
verified_at: "2026-10-12"
reviewed_at: "2026-10-13"
reviewed_by: "ademasistemas"
synonyms: ["pago mixto","mitad efectivo mitad tarjeta","descuento","recargo"]
related: ["hacer-una-venta","vender-fiado-cuenta-corriente","abrir-y-cerrar-caja"]
social_image: "/social/cobrar-con-varios-medios-de-pago-v1.jpg"
---
## Para qué sirve

No todos los clientes pagan de una sola forma: a veces una parte es en efectivo y el resto con tarjeta o transferencia. Esto sirve para que **cada importe quede asentado en su medio de pago** y el cierre de caja cierre bien, y para aplicar un descuento cuando lo acordás con el cliente.

## Qué vas a lograr

Vas a **cobrar una venta con varios medios de pago** en ADEstock, por ejemplo una parte en efectivo y el resto con tarjeta o transferencia. Cada pago queda separado para identificar cuánto se cobró con cada medio.

La guía también explica cómo aplicar un descuento antes de cargar los pagos y cómo revisar los recargos configurados en cada medio de cobro.

## Cómo funciona el cobro

El cobro no es "un medio y listo": podés **sumar pagos** hasta cubrir el total. Cada pago que agregás baja el *faltante*. La venta solo se puede cerrar cuando el faltante llega a cero.

![Total a cobrar](../../assets/tutoriales/08-varios-medios-de-pago/01-total-a-cobrar.png)

Los cuatro recuadros de arriba te acompañan todo el cobro:

| # | Recuadro | Qué muestra |
|---|---|---|
| - | **Cliente activo** | A quién se le vende. Con *Cambiar / Ver cliente* lo cambiás sin salir |
| 1 | **Total venta** | Lo que tiene que quedar cubierto para cerrar |
| - | **Total aplicado** | La suma de los pagos que ya cargaste |
| 2 | **Faltante** | Lo que falta cobrar. Cuando llega a cero cambia a *Completado*. Si el cliente entrega de más en efectivo, muestra el **vuelto** |

## Paso a paso

### 1. (Opcional) Aplicá un descuento

Si hay que hacer un descuento, hacelo **antes** de cargar los pagos. En el panel *Descuento (opcional)* elegí entre **%** (porcentaje) y **$** (monto fijo) y escribí el valor.

![Descuento aplicado](../../assets/tutoriales/08-varios-medios-de-pago/02-descuento.png)

El sistema te muestra qué aplicó (*Descuento aplicado: 10 % (−$ 1.735,00) · Total original: $ 17.350,00*) y el **Total venta** ya viene con el descuento. El botón **Quitar** lo elimina.

> Aplicar descuentos requiere el permiso **Puede hacer descuentos**. Sin él, el panel no te deja usarlo.

### 2. Cargá el primer pago

Elegí un medio (por ejemplo **Efectivo**), escribí el importe y tocá **Agregar pago**.

![Primer pago en efectivo](../../assets/tutoriales/08-varios-medios-de-pago/03-primer-pago-efectivo.png)

El pago aparece en **3. Pagos cargados** y el faltante baja.

### 3. Cargá el resto con otro medio

Elegí otro medio (por ejemplo **Tarjetas**). Para no calcular el importe a mano, usá los atajos de abajo del campo *Importe*:

![Resto con tarjeta](../../assets/tutoriales/08-varios-medios-de-pago/04-resto-con-tarjeta.png)

| Botón | Qué completa |
|---|---|
| **Exacto** | Todo lo que falta cobrar (incluye el recargo del medio, si tiene) |
| **50 %** | La mitad de lo que falta |
| **Limpiar** | Borra el importe |

Tocá **Agregar pago**.

### 4. Revisá y confirmá

Cuando el faltante llega a cero, el cuadro de aviso cambia a *Pago completo*. Revisá la lista y tocá **CONFIRMAR Y CERRAR**.

![Dos pagos cargados](../../assets/tutoriales/08-varios-medios-de-pago/05-dos-pagos-cargados.png)

Podés **quitar** un pago con el tacho (🗑) y volver a cargarlo si el cliente cambia de idea.

### 5. Listo

La venta se cierra y el POS abre una venta nueva.

![Venta cerrada](../../assets/tutoriales/08-varios-medios-de-pago/06-venta-cerrada.png)

## Medios con recargo o descuento

Algunos medios de cobro pueden tener un **recargo o descuento** configurado (por ejemplo, +5 % por pagar con tarjeta). Se configura en *Configuración → Medios de cobro* y se aplica solo: cuando elegís ese medio, el importe ya viene con el recargo y el botón del medio muestra una etiqueta con el porcentaje.

## Qué pasa por detrás

| Qué | Detalle |
|---|---|
| Un registro por pago | Cada pago cargado se guarda por separado, con su medio, su importe y su turno de caja |
| Caja y cierre | En el cierre de caja, el efectivo se cuenta aparte de los medios electrónicos |
| Billeteras | Cada pago alimenta la billetera vinculada a su medio de cobro |
| Descuento | Queda registrado en la venta (tipo y valor) junto con el total original |
| Protección | Si tocás *Confirmar* dos veces, los pagos no se duplican |

## Problemas frecuentes

| Si te pasa… | Es porque… | Qué hacer |
|---|---|---|
| *Confirmar y cerrar* está apagado | Todavía falta cobrar | Agregá otro pago hasta que el faltante sea $ 0 |
| El panel de descuento no deja escribir | Tu usuario no tiene *Puede hacer descuentos* | Pedíselo al dueño |
| El botón *Cuenta Corriente* está apagado | El cliente es Consumidor Final o no tiene cuenta corriente | Cambiá el cliente (ver [Vender a cuenta corriente](/tutoriales/vender-fiado-cuenta-corriente/)) |
| Cargué un pago por error | - | Quitalo con el tacho y cargalo de nuevo |
| El importe de tarjeta es mayor al total | El medio tiene recargo | Es lo esperado: el recargo se suma al importe de ese medio |

## Cómo comprobar que salió bien

Antes de confirmar, verificá que el **Faltante** sea $ 0 y que cada pago tenga el medio y el importe correctos. Si cargaste uno por error, quitá esa fila y agregala de nuevo. Revisá también el vuelto cuando el cliente entrega efectivo de más.

## Siguiente paso

- [hacer una venta y cobrar en efectivo en ADEstock](/tutoriales/hacer-una-venta/)
- [vender fiado a cuenta corriente en ADEstock](/tutoriales/vender-fiado-cuenta-corriente/)
- [abrir, hacer el arqueo y cerrar caja en ADEstock](/tutoriales/abrir-y-cerrar-caja/)
