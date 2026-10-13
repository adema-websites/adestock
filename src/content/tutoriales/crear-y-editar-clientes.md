---
id: "crear-y-editar-clientes"
slug: "crear-y-editar-clientes"
title: "Cómo crear y editar clientes en ADEstock"
description: "Registrá clientes en ADEstock, editá sus datos y habilitá la cuenta corriente. Creá un cliente desde una venta y consultá su estado de cuenta."
category: "clientes"
priority: "P1"
roles: ["cajero","dueno","administrativo"]
surface: ["pos","panel"]
status: "published"
tiempo: "1 minuto por cliente"
necesitas: "nada especial"
para_quien: "cajeros y dueños"
modulo: "agenda (Cliente), venta (POS)"
permiso: "ninguno para crear un cliente rápido desde la venta; el listado de gestión está en el Menú rápido"
source_path: "01-manual-usuario/15-crear-y-editar-clientes.md"
source_hash: "d4634e8feceeddbab88bf4c83d133e681507c23981b62e4da289db390b08c30e"
product_version: "3.0.0"
verified_at: "2026-10-12"
reviewed_at: "2026-10-13"
reviewed_by: "ademasistemas"
synonyms: ["alta de cliente","cliente nuevo"]
related: ["hacer-una-venta","vender-fiado-cuenta-corriente","consultar-cuenta-corriente-cliente"]
social_image: "/social/crear-y-editar-clientes-v1.jpg"
---
## Para qué sirve

Un cliente registrado permite lo que el cliente anónimo no: asignarle ventas, **venderle fiado** y llevar su historial y su saldo. Esta guía sirve para darlo de alta (y editarlo) cuando lo necesitás. Si no hace falta nada de eso, se vende a **Consumidor Final** y no tenés que registrar a nadie.

## Qué vas a lograr

Vas a **crear y editar clientes en ADEstock** para asociarles ventas y consultar su historial. Si les vendés fiado, también vas a aprender a habilitar la cuenta corriente y acceder a sus estados de cuenta.

Podés dar de alta al cliente desde Gestión de clientes o mientras atendés una venta, sin perder el carrito.

> Si el cliente no necesita nada de eso, no hace falta registrarlo: se vende a **Consumidor Final** (es el cliente por defecto de cada venta).

## Paso a paso

### 1. Abrí la gestión de clientes

Menú rápido (**F8**) → **Gestión de clientes**.

![Gestión de clientes](../../assets/tutoriales/15-clientes/01-gestion-de-clientes.png)

1. **Nuevo Cliente**: abre el formulario de alta.
2. **Buscador**: encontrá un cliente por nombre o documento.

La tabla muestra el **documento**, el **nombre**, el **saldo de cuenta corriente** y las acciones de cada cliente. Un cliente sin cuenta corriente aparece como *Sin CC*.

### 2. Completá el formulario

Tocá **Nuevo Cliente**.

![Formulario de cliente](../../assets/tutoriales/15-clientes/02-formulario-vacio.png)

| # | Campo | Qué poner |
|---|---|---|
| 1 | **Nombre** *(obligatorio)* | Nombre o razón social con el que vas a identificar al cliente |
| 2 | **Documento (DNI/CUIT)** | Sirve para identificarlo y para facturar. Es lo que podés usar para buscarlo |
| - | Teléfono, Email, Dirección | Datos de contacto. Opcionales |
| 3 | **Categoría IVA** *(obligatorio)* | *Consumidor Final*, *Monotributista*, *Responsable Inscripto* o *Exento*. Se usa para **discriminar el IVA** en tickets y facturas A4 |
| 4 | **Habilitar Cuenta Corriente** | Activalo si le vas a vender "fiado". Si está apagado, el POS no te deja cobrarle con cuenta corriente |

### 3. Habilitá la cuenta corriente (si corresponde)

Para un cliente de confianza, tildá **Habilitar Cuenta Corriente**.

![Cliente con cuenta corriente habilitada](../../assets/tutoriales/15-clientes/03-con-cuenta-corriente.png)

> Habilitarla **no genera deuda**: solo permite que el cliente pueda quedar debiendo. La deuda aparece cuando le hacés una venta a cuenta corriente (ver [Vender a cuenta corriente](/tutoriales/vender-fiado-cuenta-corriente/)).

### 4. Guardá

Tocá **Guardar Cliente**. Aparece en la lista, con saldo $0,00.

![Cliente guardado](../../assets/tutoriales/15-clientes/04-cliente-guardado.png)

## Crear un cliente en plena venta

No hace falta ir al menú: en la pantalla de venta, el botón **Cambiar** del cliente (**F9**) abre el selector, y desde ahí podés crear un cliente nuevo y asignárselo a la venta sin perder el carrito.

## Editar un cliente

En la lista, tocá el primer icono de acciones (lápiz). Se abre el mismo formulario con los datos cargados; cambiás lo que necesites y tocás **Guardar Cambios**.

## Los iconos de acciones

| Icono | Qué hace |
|---|---|
| ✏️ Editar | Modifica los datos del cliente |
| 🖨️ Estado de cuenta (ticket) | Imprime en la ticketera su estado de cuenta |
| 📄 Estado de cuenta (PDF A4) | Descarga el estado de cuenta en PDF |
| 📊 Estado de cuenta (Excel) | Descarga el estado de cuenta en Excel |

Los iconos de **estado de cuenta** están deshabilitados para *Cliente Mostrador* (el cliente genérico) y para los clientes sin cuenta corriente. Cómo se lee ese estado de cuenta está en el tutorial [Revisar la cuenta corriente de un cliente](/tutoriales/consultar-cuenta-corriente-cliente/).

## Qué pasa por detrás

| Qué | Detalle |
|---|---|
| Cliente | Se crea en la agenda del sistema, visible para todas las cajas |
| Cuenta corriente | El cliente queda habilitado para recibir ventas con el medio de cobro *Cuenta Corriente* |
| Consumidor Final | Es un cliente genérico que ya viene creado: no necesita datos |

## Problemas frecuentes

| Si te pasa… | Es porque… | Qué hacer |
|---|---|---|
| El botón de cuenta corriente aparece apagado al cobrar | El cliente de la venta no tiene la cuenta corriente habilitada, o la venta es a Consumidor Final | Cambiá el cliente (F9) y habilitale la cuenta corriente desde *Editar* |
| No encuentro a un cliente | Lo buscás por un dato que no cargaste | Probá con nombre o documento |
| Los iconos de estado de cuenta están apagados | El cliente no tiene cuenta corriente | Habilitala desde *Editar* |

## Cómo comprobar que salió bien

Buscá al cliente por nombre o documento en **Gestión de clientes**. Revisá sus datos y, si vas a venderle fiado, confirmá que tenga habilitada la cuenta corriente. Crear el cliente o habilitar esa opción no genera deuda: la deuda surge al registrar una venta fiada.

## Siguiente paso

- [hacer una venta y cobrar en efectivo en ADEstock](/tutoriales/hacer-una-venta/)
- [vender fiado a cuenta corriente en ADEstock](/tutoriales/vender-fiado-cuenta-corriente/)
- [consultar saldos y cuentas corrientes en ADEstock](/tutoriales/consultar-cuenta-corriente-cliente/)
