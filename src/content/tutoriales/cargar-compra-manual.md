---
id: "cargar-compra-manual"
slug: "cargar-compra-manual"
title: "Cómo cargar una compra manual en ADEstock"
description: "Cargá compras de mercadería en ADEstock sin usar IA: elegí proveedor, productos, cantidades y pago. Confirmá la compra para actualizar stock y costos."
category: "compras"
priority: "P1"
roles: ["dueno","administrativo"]
surface: ["panel"]
status: "published"
tiempo: "3 minutos"
necesitas: "un turno de caja abierto y los datos del proveedor, productos, cantidades y precios del comprobante"
para_quien: "dueños y administrativos"
modulo: "compra (Compra simple), producto, agenda (Proveedor)"
permiso: "acceso al módulo de compras"
source_path: "01-manual-usuario/19-cargar-una-compra-manual.md"
source_hash: "7dab4f125653c00cfd3591b5568bc2aa6a3c1700942cda36dc7d5d47b9d6fb86"
product_version: "3.0.0"
verified_at: "2026-10-12"
reviewed_at: "2026-10-13"
reviewed_by: "ademasistemas"
synonyms: ["compra","ingreso de mercadería","remito"]
related: ["crear-y-editar-proveedores","cargar-compras-con-foto-ia","pagar-proveedor"]
social_image: "/social/cargar-compra-manual-v1.jpg"
---
## Para qué sirve

Cada compra que cargás hace tres cosas a la vez: **suma stock**, **actualiza el costo** de los productos y deja asentado si la pagaste o si **quedó debiendo** al proveedor. Esta guía es la forma manual, para cuando no tenés la boleta a mano o son pocos renglones. Si la boleta es larga, conviene la [compra con foto e IA](/tutoriales/cargar-compras-con-foto-ia/).

## Qué vas a lograr

Vas a **cargar una compra de mercadería manualmente en ADEstock**, escribiendo los productos, cantidades y precios del comprobante. Podés registrar el pago o dejar la compra a cuenta corriente con el proveedor.

La carga se hace desde el POS y queda pendiente. La confirmación desde el panel de administración es el paso que aplica sus efectos sobre stock y pagos; el costo se actualiza en los renglones con **Act. costo** marcado.

Es el mismo asistente de 4 pasos que usa la compra con foto, pero sin lectura automática. Sirve cuando:

- No tenés la boleta a mano, o es un remito escrito a mano.
- Querés cargar algo rápido de pocos renglones.
- No tenés configurada la IA, o se alcanzó el límite diario.

## Paso a paso

### 1. Elegí "Carga rápida manual"

Abrí **Menú rápido (F8) → Compras (carga rápida)** (dirección `/compras/simple/`) y tocá **Carga rápida manual (sin OCR)**.

![Carga manual](../../assets/tutoriales/19-compra-manual/01-carga-manual.png)

### 2. Elegí el proveedor

No hay boleta que lo detecte: lo elegís vos de la lista (o lo creás con **＋ Nuevo proveedor**).

![Elegir proveedor](../../assets/tutoriales/19-compra-manual/02-elegir-proveedor.png)

### 3. Revisá la forma de pago, el IVA y el flete

![Forma de pago y opciones de flete de la compra](../../assets/tutoriales/19-compra-manual/03-checks.png)

| # | Pregunta | Qué responder |
|---|---|---|
| 1 | **¿Cómo se paga?** | *Efectivo*, *Transferencia* o *Cuenta Corriente Proveedor* (queda como deuda). La opción de **cuenta corriente** solo la ven los usuarios con el permiso *Puede comprar en cuenta corriente* |
| 2 | **¿Hubo flete?** | Si tildás, elegís si es un gasto aparte, si se paga con la compra y si se prorratea. Está explicado en [Cargar una compra con la foto de la boleta](/tutoriales/cargar-compras-con-foto-ia/#el-flete-tres-formas-de-manejarlo) |

También podés indicar si **la factura discrimina IVA**.

### 4. Cargá los renglones

En el paso 4 la tabla empieza vacía. Cada renglón se agrega con **➕ Agregar renglón manual**.

![Renglones vacíos](../../assets/tutoriales/19-compra-manual/04-renglones-vacios.png)

En cada renglón:

1. Escribí parte del **nombre del producto** y elegí el correcto de la lista. Si es nuevo, tocá **＋ Crear producto**.
2. Completá **cantidad** y **precio unitario**. El **total** se calcula solo. Si tenés un descuento, ponelo en **Desc%**.

![Renglones cargados](../../assets/tutoriales/19-compra-manual/05-renglones-cargados.png)

| # | Qué ves | Para qué sirve |
|---|---|---|
| 1 | **Producto** y **Precio actual vs. último costo** | Te muestra si el precio de esta compra **subió o bajó** respecto del último costo registrado. Por ejemplo: `+15,38 %` indica que el arroz que costaba $ 1.300 ahora te lo cobran $ 1.500. Si es igual, dice *Sin cambio* |
| 2 | **Cant. · Precio unit. · Desc% · Total** | Los valores del renglón |

> **Act. costo:** cada renglón tiene un casillero para que el costo del producto se **actualice** con el precio de esta compra. Viene tildado.

### 5. Revisá los totales

![Totales](../../assets/tutoriales/19-compra-manual/06-totales.png)

Como no hay boleta, **Total OCR** dice *no detectado* y **Diferencia** dice *Sin referencia OCR*. Controlá vos que **Total actual** coincida con tu remito.

### 6. Resumen y creación

Tocá **Crear compra**. Aparece el resumen previo (renglones, unidades a ingresar, total y flete):

![Resumen](../../assets/tutoriales/19-compra-manual/07-resumen.png)

Tocá **Crear compra** otra vez para guardar.

### 7. Confirmala en el panel de administración

La compra queda **pendiente** y **la tiene que confirmar el dueño o un administrativo**. Para que mueva stock y plata, se confirma así:

**Panel de administración → Compra → Compras** → tildá la compra → acción **Confirmar compra** → *Ejecutar*.

![Compra confirmada](../../assets/tutoriales/19-compra-manual/08-compra-confirmada.png)

Pasa a **✓ Aprobada**. En el ejemplo: 20 × $ 1.500 + 30 × $ 850 = **$ 55.500**.

> **Los pagos de una compra se registran desde el POS** (paso 3), no desde el panel de administración: en el panel la compra se **consulta y se confirma**, pero sus pagos no se agregan ni se editan. Tampoco se crean compras desde el panel.

### Y el turno de caja

El pago de la compra queda asociado al **turno que tenías abierto** cuando la cargaste. Mientras la compra esté **pendiente**, ese pago **no descuenta** efectivo del arqueo. Si la pagaste con dinero u otro medio (no cuenta corriente), **tiene que estar confirmada antes de que cierres el turno**: si no, el cierre te avisa y no te deja cerrar (ver [Turno de caja](/tutoriales/abrir-y-cerrar-caja/#antes-de-cerrar-las-compras-pagadas-tienen-que-estar-confirmadas)). Las compras **solo a cuenta corriente** no frenan el cierre.

## ¿Y si la pagué a cuenta corriente?

Si en el paso 3 elegiste *Cuenta Corriente Proveedor*, la compra confirmada suma **deuda** con el proveedor. La saldás desde **Menú rápido → Pagar a un proveedor** (ver [Pagar a un proveedor](/tutoriales/pagar-proveedor/)).

Si la pagaste en efectivo o transferencia, ya queda **pagada** al confirmar.

## Qué pasa por detrás

| Qué | Detalle |
|---|---|
| Stock | Suma la cantidad comprada de cada producto, al confirmar |
| Costo | Con *Act. costo* tildado, el costo del producto pasa a ser el precio de esta compra |
| Pago | Se registra un pago con el medio elegido, asociado a tu turno abierto. Si es cuenta corriente, queda sin cancelar (deuda) |
| Caja | Al confirmar la compra, el pago en efectivo resta del efectivo esperado **del turno donde se pagó** |

## Problemas frecuentes

| Si te pasa… | Es porque… | Qué hacer |
|---|---|---|
| No me deja crear la compra | Hay un renglón sin producto, o con cantidad 0 | Asigná el producto o quitá el renglón |
| La compra no suma stock | Quedó pendiente | Pedile al dueño o a un administrativo que la confirme en el panel de administración |
| No me deja cerrar la caja | Tenés compras pagadas sin confirmar | Pedí que las confirmen (o descartalas si estaban mal cargadas) |
| No veo *Cuenta Corriente Proveedor* | Tu usuario no tiene el permiso *Puede comprar en cuenta corriente* | Pedíselo al dueño (Menú rápido → Usuarios) |
| Quiero cargar o editar el pago desde el panel | Los pagos se registran solo desde el POS | Eliminá la compra pendiente y volvela a cargar desde el POS |
| Cargué mal un precio | - | Antes de confirmar: eliminá la compra pendiente y volvela a cargar |
| El proveedor no está | Es nuevo | **＋ Nuevo proveedor** en el paso 2 |

## Cómo comprobar que salió bien

Verificá que la compra figure como **Aprobada** en el panel y compará sus cantidades y total con el comprobante. Revisá el stock ingresado y los costos de los renglones con **Act. costo** marcado. Si compraste a cuenta corriente, consultá la deuda del proveedor; si pagaste en efectivo, revisá el movimiento en el turno correspondiente.

## Siguiente paso

- [crear y editar proveedores en ADEstock](/tutoriales/crear-y-editar-proveedores/)
- [cargar compras con foto e IA en ADEstock](/tutoriales/cargar-compras-con-foto-ia/)
- [pagar a proveedores y registrar adelantos en ADEstock](/tutoriales/pagar-proveedor/)
