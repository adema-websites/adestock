---
id: "abrir-y-cerrar-caja"
slug: "abrir-y-cerrar-caja"
title: "Cómo abrir, hacer el arqueo y cerrar caja en ADEstock"
description: "Abrí un turno de caja en ADEstock, registrá el efectivo inicial y hacé el arqueo al cerrar. Entendé cómo se calculan faltantes y sobrantes."
category: "caja"
priority: "P0"
roles: ["cajero","dueno"]
surface: ["pos"]
status: "published"
tiempo: "2 minutos para abrir, 3 para cerrar"
necesitas: "tener una caja asignada"
para_quien: "cajeros y dueños"
modulo: "venta (CierreCaja, POS)"
permiso: "ninguno (cada cajero cierra su propio turno)"
source_path: "01-manual-usuario/12-turno-de-caja-apertura-y-cierre.md"
source_hash: "05a72bf250013b185be6840ff0dbaa5371b30da89568a65f46b0e3821009a375"
product_version: "3.0.0"
verified_at: "2026-10-12"
reviewed_at: "2026-10-13"
reviewed_by: "ademasistemas"
synonyms: ["turno","arqueo","faltante","sobrante","cierre de caja"]
related: ["registrar-gastos-y-retiros","controlar-turnos-caja-panel","cargar-compra-manual"]
social_image: "/social/abrir-y-cerrar-caja-v1.jpg"
---
## Para qué sirve

El turno de caja es el período en que una persona trabaja con una caja: se abre con el efectivo con el que arrancás y se cierra contando lo que hay. Sirve para saber **cuánta plata debería haber y cuánta hay realmente**, y detectar al instante un faltante o un sobrante. Se abre al empezar la jornada y se cierra al terminarla.

## Qué vas a lograr

Vas a **abrir y cerrar un turno de caja en ADEstock**: declarar el efectivo inicial, registrar las salidas durante el turno y contar el dinero al finalizar. El arqueo compara el efectivo contado con el esperado para identificar faltantes o sobrantes.

La guía incluye un ejemplo del cálculo y explica por qué las compras pagadas deben estar confirmadas antes del cierre.

## Qué es un turno

Un **turno** es el período en el que trabajás con una caja: arranca cuando lo abrís y termina cuando hacés el cierre. Todo lo que cobrás, retirás o gastás mientras tanto queda **asociado a ese turno**. Por eso, al cerrar, el sistema sabe exactamente cuánta plata debería haber.

## 1. Abrir el turno

Al entrar al POS sin turno abierto, el sistema te muestra la ventana **Apertura de Caja**. Escribí el **efectivo inicial** (con cuánta plata arrancás, puede ser $ 0) y tocá **Abrir Turno**.

![Apertura de caja](../../assets/tutoriales/12-turno-de-caja/03-nuevo-turno.png)

Mientras no abras el turno, el POS no te deja cobrar. Desde esa misma ventana podés ir al **Panel Admin** o **Salir**.

## 2. Durante el turno

| Qué necesitás | Dónde |
|---|---|
| Sacar efectivo de la caja (por ejemplo, pasarlo a la caja fuerte) | Menú rápido → **Retiro de caja** |
| Registrar un gasto pagado de la caja | Menú rápido → **Gastos** |
| Pagar una compra o un adelanto a un proveedor con plata de la caja | [Cargar una compra](/tutoriales/cargar-compra-manual/) y [Pagar a un proveedor](/tutoriales/pagar-proveedor/) |

Los gastos y retiros se explican en [Registrar gastos y retiros de caja](/tutoriales/registrar-gastos-y-retiros/). Las compras y los pagos a proveedores tienen sus propias guías, enlazadas en la tabla.

> **Todos los pagos y cobros se hacen desde el POS**, con el turno abierto. No se cargan desde el panel de administración. Así cada movimiento queda siempre en el turno y la caja donde ocurrió, y **no se pasa a otro turno**.

## 3. Cerrar el turno (arqueo)

Menú rápido (**F8**) → **Cierre de caja**.

![Cierre de caja](../../assets/tutoriales/12-turno-de-caja/01-cierre-de-caja.png)

| # | Elemento | Qué es |
|---|---|---|
| 1 | **Datos del turno** | Quién cierra, qué caja, número de turno y hora de apertura |
| 2 | **Efectivo en caja (real)** | **Contá la plata que hay físicamente** y escribí el total |
| 3 | **Generar Cierre** | Cierra el turno y emite el comprobante |

Escribí lo que contaste y tocá **Generar Cierre**.

![Efectivo contado](../../assets/tutoriales/12-turno-de-caja/02-efectivo-contado.png)

Al generar el cierre:

1. El turno **queda cerrado**.
2. Se **manda a imprimir el ticket de cierre** (si hay impresora configurada) con el resumen y la diferencia.
3. El POS te pide **abrir un turno nuevo** para seguir vendiendo.

## Cómo se calcula lo que "debería haber"

El sistema solo cuenta el **efectivo**. Los pagos con tarjeta, transferencia o cuenta corriente no entran al arqueo.

```
Efectivo esperado  =  Efectivo inicial
                    + Ventas cobradas en efectivo
                    + Cobros de deudas en efectivo
                    ± Notas de crédito / débito en efectivo
                    − Retiros de caja en efectivo
                    − Gastos pagados en efectivo
                    − Pagos de compras confirmadas en efectivo
                    − Pagos y adelantos a proveedores en efectivo
Diferencia         =  Efectivo contado − Efectivo esperado
```

### Ejemplo

| Concepto | Importe |
|---|---|
| Efectivo inicial | $ 5.000,00 |
| + Ventas en efectivo | $ 22.457,14 |
| + Cobro de una deuda en efectivo | $ 3.000,00 |
| − Retiro de caja | $ 2.000,00 |
| − Gasto en efectivo | $ 1.200,00 |
| **= Efectivo esperado** | **$ 27.257,14** |
| Efectivo contado | $ 27.000,00 |
| **Diferencia** | **− $ 257,14 (faltante)** |

Una diferencia **negativa** es un **faltante** (hay menos plata de la que debería); una **positiva** es un **sobrante**.

## Antes de cerrar: las compras pagadas tienen que estar confirmadas

Si en tu turno **cargaste compras** y las **pagaste con dinero (o con otro medio que no sea cuenta corriente)**, esas compras tienen que estar **confirmadas** antes de cerrar. Una compra pendiente **no descuenta** plata del arqueo, y si se confirmara después de cerrar quedarían saldos descuadrados.

Si hay compras sin confirmar, el sistema **no te deja cerrar** y te muestra un aviso con cuáles son (número de compra, proveedor y total pagado):

![Cierre bloqueado por compras sin confirmar](../../assets/tutoriales/12-turno-de-caja/04-cierre-bloqueado-por-compras.png)

Tocá **Entendido**: el turno sigue abierto. Pedile al **dueño o a un administrativo** que las confirme desde el panel de administración (*Compra → Compras → Confirmar compra*; más adelante también desde la app del dueño). Cuando estén confirmadas, volvé a **Cierre de caja**.

| Caso | ¿Frena el cierre? |
|---|---|
| Compra pagada con efectivo, transferencia, tarjeta u otro medio, **sin confirmar** | **Sí** |
| Compra **solo a cuenta corriente** cargada por alguien con permiso para comprar a cuenta corriente | No |
| Compra ya **confirmada** | No |
| Compra pendiente que se **descarta** (se anula o se borra) | No |

## ¿Qué pasa si me olvido de cerrar?

Si dejás el turno abierto de un día para el otro, el comportamiento depende de un ajuste del dueño (*Configuración → Ventas y caja → Permitir operar con turno abierto de otro día*):

| Ajuste | Qué pasa al día siguiente |
|---|---|
| **Apagado** | El POS **te obliga a cerrar** la caja del día anterior antes de vender |
| **Encendido** | Podés seguir vendiendo con ese turno |

## Qué pasa por detrás

| Qué | Detalle |
|---|---|
| Cada pago, retiro y gasto | Guarda el turno al que pertenece |
| Cierre | Calcula los movimientos del turno, guarda el efectivo contado y la diferencia, y marca el turno como cerrado |
| Ticket | Se encola para la impresora de la caja; si falla, intenta imprimir directo |
| Pagos de compras y a proveedores | Cada pago queda asociado al turno en el que se registró, igual que los gastos y retiros |
| Resumen guardado | El detalle por medio de pago queda guardado con el turno. **Consultar o descargar el PDF no modifica un turno cerrado**: muestra los números guardados al cerrar. La acción especial de recálculo del superusuario se explica en [Revisar turnos de caja](/tutoriales/controlar-turnos-caja-panel/) |

## Problemas frecuentes

| Si te pasa… | Es porque… | Qué hacer |
|---|---|---|
| "No hay un turno de caja abierto para cerrar" | No abriste turno, o ya lo cerraste | Abrí un turno nuevo |
| Me da faltante y no sé por qué | Algún retiro, gasto o cobro no se registró | Revisá en *Ventas anteriores*, *Gastos* y *Retiro de caja* del turno |
| El cierre no imprime | No hay impresora o agente configurado | Menú rápido → Configuración → Impresora de tickets |
| "Hay compras pagadas sin confirmar" al cerrar | Cargaste compras pagadas con dinero u otro medio y nadie las confirmó | Pedile al dueño o a un administrativo que las confirme en el panel (*Compra → Compras → Confirmar compra*) |
| Cerré sin querer | - | Abrí un turno nuevo; el cierre anterior queda registrado |

## Cómo comprobar que salió bien

Al generar el cierre, verificá que el turno quede **cerrado** y revisá el comprobante: efectivo inicial, esperado, contado y diferencia. El POS debe pedirte abrir un turno nuevo para seguir vendiendo. Si hay diferencia, consultá los movimientos del turno antes de atribuirla a un faltante físico.

## Siguiente paso

- [registrar gastos y retiros de caja en ADEstock](/tutoriales/registrar-gastos-y-retiros/)
- [revisar turnos y cierres de caja en ADEstock](/tutoriales/controlar-turnos-caja-panel/)
- [cargar una compra manual en ADEstock](/tutoriales/cargar-compra-manual/)
