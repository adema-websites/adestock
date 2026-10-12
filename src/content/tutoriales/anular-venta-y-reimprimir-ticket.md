---
id: "anular-venta-y-reimprimir-ticket"
slug: "anular-venta-y-reimprimir-ticket"
title: "Cómo anular una venta y reimprimir un ticket"
description: "- Reimprimir el ticket de una venta ya cerrada (esto lo hace cualquier cajero desde el POS). - Anular una venta hecha por error, para que deje de contar en…"
category: "vender"
priority: "P1"
roles: ["cajero","dueno"]
surface: ["pos","panel"]
status: "draft"
tiempo: "2 minutos"
necesitas: "saber el número de la venta"
para_quien: "el dueño (y quien tenga acceso al panel de administración)"
modulo: "venta (POS → Ventas anteriores; panel de administración → Ventas)"
permiso: "reimprimir: ninguno (cada cajero ve los tickets de su turno); anular: acceso al panel de administración"
source_path: "01-manual-usuario/10-anular-una-venta-y-reimprimir-tickets.md"
source_hash: "cdefb21d504be2f5b380eb29556b4b37083ee78b98aff235b8ff8fbcf93ddea8"
product_version: "pendiente-verificar"
verified_at: "2026-10-12"
reviewed_at: null
synonyms: ["anular","devolución","reimprimir","ticket"]
related: []
social_image: null
---
## Qué vas a lograr

- **Reimprimir** el ticket de una venta ya cerrada (esto lo hace cualquier cajero desde el POS).
- **Anular** una venta hecha por error, para que **deje de contar** en caja, stock y reportes.

> **Hoy la anulación de una venta se hace desde el panel de administración, no desde el POS.** Desde el POS solo se consultan y reimprimen las ventas.

## Reimprimir un ticket (desde el POS)

Menú rápido (**F8**) → **Ventas anteriores**.

![Ventas anteriores](../../assets/tutoriales/07-hacer-una-venta/09-ventas-anteriores.png)

Cada venta muestra su número, fecha y hora, cliente, caja y total. Con **Ticket** reimprimís el ticket y con **Hoja A4** la versión en A4.

- Un cajero ve solo las ventas de **su turno actual**. Con el permiso **Puede ver todos los tickets** ve las de todas las cajas y turnos.

## Anular una venta (desde el panel de administración)

### 1. Entrá al listado de ventas

Desde el POS: Menú rápido → **Panel de administración** → **Venta → Ventas**.

### 2. Elegí la venta y la acción

Tildá la casilla de la venta (o ventas) a anular. Arriba de la lista, en el desplegable de acciones, elegí **Anular Venta** y tocá **Ejecutar**.

![Acción Anular Venta](../../assets/tutoriales/10-anular-venta/02-accion-anular-venta.png)

En el listado ves por cada venta: número, fecha y estado, cajero, cliente, total, seguimiento, ticket, nota de crédito y el botón **Entregar**.

### 3. Verificá el resultado

El sistema muestra un aviso: *Venta N anulada correctamente*, y la venta pasa al estado **anulada**.

![Venta anulada](../../assets/tutoriales/10-anular-venta/03-venta-anulada.png)

## Qué se puede anular

Solo se anulan las ventas en estado **pagada, facturada o finalizada**. Una venta ya anulada, o una que todavía está en carrito (creada), no se puede anular.

## Qué pasa al anular

| Qué | Efecto |
|---|---|
| Venta | Pasa a estado **anulada**, con el motivo "Anulada desde admin" |
| Stock | Las ventas anuladas **dejan de descontar**: el stock de esos productos vuelve a estar disponible |
| Cierre de caja | Los pagos de una venta anulada **no se cuentan** en el arqueo |
| Cobros de deuda asociados | Si la venta fue a cuenta corriente y el cliente ya había pagado, esos pagos se **anulan** y las deudas se restauran |
| Registro | La venta **no se borra**: queda para auditoría |

> **Importante:** anular no devuelve plata en efectivo. Si ya le cobraste al cliente, la devolución es un movimiento aparte (retiro de caja).

## Cuándo usar otra herramienta

| Situación | Qué usar |
|---|---|
| El cliente devuelve **parte** de la mercadería | **Nota de crédito** (desde el panel de administración) |
| Se cobró de menos o de más en un **cobro de deuda** | Acción *Anular cobro* (solo superusuario), en el panel de administración |
| El carrito sigue abierto y quiero empezar de cero | **Vaciar** (F3) en el POS |

## Entregar una venta

En el listado de ventas, junto a cada una está el botón **Entregar**. Marca la venta como entregada y **descuenta el stock físico** si tenés activado *Seguimiento de entregas* (ver *La configuración del POS*). Con ese ajuste apagado, el stock se descuenta al cobrar y no hace falta.

## Problemas frecuentes

| Si te pasa… | Es porque… | Qué hacer |
|---|---|---|
| "La venta no está en un estado válido para anular" | Está en carrito o ya anulada | Solo se anulan ventas cobradas |
| No veo "Anular Venta" | Tu usuario no tiene permisos sobre Ventas en el panel | Pedíselo al dueño |
| La venta anulada sigue en el listado | Las ventas anuladas no se borran | Es lo esperado; el estado figura como *anulada* |

## Siguiente paso

- Turno de caja: apertura, retiros y cierre
- Cobrar la deuda de un cliente
