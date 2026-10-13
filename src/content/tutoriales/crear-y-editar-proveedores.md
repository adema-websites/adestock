---
id: "crear-y-editar-proveedores"
slug: "crear-y-editar-proveedores"
title: "Cómo crear y editar proveedores en ADEstock"
description: "Cargá proveedores en ADEstock con sus datos de contacto, CUIT y condición de pago. Consultá deudas, adelantos e historial de pagos desde el POS."
category: "compras"
priority: "P1"
roles: ["dueno","administrativo"]
surface: ["panel"]
status: "published"
tiempo: "2 minutos"
necesitas: "nada previo"
para_quien: "dueños y administrativos"
modulo: "agenda (Proveedor), venta (POS → Gestión de proveedores)"
permiso: "ninguno especial"
source_path: "01-manual-usuario/18-crear-y-editar-proveedores.md"
source_hash: "7e0691a7cfc33452023ae426fd9b740575b078d962e69e0420039890d097950f"
product_version: "3.0.0"
verified_at: "2026-10-12"
reviewed_at: "2026-10-13"
reviewed_by: "ademasistemas"
synonyms: ["alta de proveedor","proveedor nuevo"]
related: ["cargar-compra-manual","cargar-compras-con-foto-ia","pagar-proveedor"]
social_image: "/social/crear-y-editar-proveedores-v1.jpg"
---
## Para qué sirve

Los proveedores son la otra mitad del negocio: a quienes les comprás. Cargarlos sirve para **asociarles compras**, saber **cuánto les debés** y pagarles. Es un paso previo a cargar cualquier compra, y también a cargar sus [listas de precios](/tutoriales/cargar-listas-precios-proveedores/).

## Qué vas a lograr

Vas a **crear y editar proveedores en ADEstock** para asociarles compras y consultar cuánto les debés. Registrá sus datos de contacto, CUIT y plazo de pago para identificar cada proveedor y revisar vencimientos.

Desde la misma gestión podés abrir sus pagos, registrar un adelanto y descargar el estado de cuenta.

## Paso a paso

### 1. Abrí la gestión de proveedores

Menú rápido (**F8**) → **Gestión de proveedores**.

![Lista de proveedores](../../assets/tutoriales/18-proveedores/01-lista-de-proveedores.png)

| # | Elemento | Qué es |
|---|---|---|
| 1 | **Buscador** | Filtra por nombre, contacto o CUIT |
| 2 | **Nuevo Proveedor** | Abre el formulario de alta |
| 3 | **Deuda CC** | Lo que **le debés** al proveedor (en rojo). *Saldo a favor* es plata que le adelantaste |
| 4 | **Acciones** | Editar · Pagar deuda o registrar adelanto · Ver pagos realizados · Estado de cuenta en PDF |

### 2. Completá el formulario

Tocá **Nuevo Proveedor**.

![Formulario de proveedor](../../assets/tutoriales/18-proveedores/02-formulario-vacio.png)

| # | Campo | Qué poner |
|---|---|---|
| 1 | **Nombre o Empresa** *(obligatorio)* | Como lo conocés. Es lo que vas a buscar al comprar |
| - | Persona de contacto, Teléfono, WhatsApp, Email, Dirección, Localidad | Datos de contacto. Opcionales |
| 2 | **CUIT / Documento** | Sirve para identificarlo y para reconocerlo en las boletas |
| 3 | **Condición de pago (días)** | En cuántos días le pagás (30, por ejemplo). Con esto el sistema marca como **vencidas** las compras impagas |
| 4 | **Notas internas** | Acuerdos, días de visita, descuentos… |

![Formulario completo](../../assets/tutoriales/18-proveedores/03-formulario-completo.png)

### 3. Guardá

Tocá **Guardar Proveedor**. Aparece en la lista, sin deuda.

![Proveedor creado](../../assets/tutoriales/18-proveedores/04-proveedor-creado.png)

## Otras formas de crear un proveedor

- **Al cargar una compra con foto:** si el proveedor de la boleta es nuevo, lo creás ahí mismo (*＋ Nuevo proveedor*), con solo la empresa y el CUIT.
- **Al pagar a un proveedor:** el botón **Nuevo** de la pantalla de pagos.

## Editar un proveedor

En la lista, tocá el primer icono de **Acciones** (lápiz). Cambiás lo que necesites y **Guardar Proveedor**.

## Qué hace cada icono de Acciones

| Icono | Qué hace |
|---|---|
| ✏️ **Editar proveedor** | Modifica sus datos |
| 💵 **Pagar deuda o registrar adelanto** | Abre el pago de cuentas corrientes de ese proveedor (ver [Pagar a un proveedor](/tutoriales/pagar-proveedor/)) |
| 🕘 **Ver pagos realizados** | Historial de pagos hechos a ese proveedor |
| 📄 **Estado de cuenta PDF** | Descarga lo que le debés, compra por compra |

## Qué pasa por detrás

| Qué | Detalle |
|---|---|
| Deuda CC | Es la suma de lo que falta pagar de cada compra hecha a cuenta corriente |
| Saldo a favor | Plata que le pagaste de más o por adelantado y todavía no se aplicó |
| Vencimiento | Se calcula con la *Condición de pago (días)* desde la fecha de cada compra |
| Alias OCR | Cuando cargás compras con foto, el sistema guarda cómo figura el proveedor en sus boletas |

## Problemas frecuentes

| Si te pasa… | Es porque… | Qué hacer |
|---|---|---|
| No veo la deuda de un proveedor | La compra se pagó en efectivo, o todavía está pendiente de confirmar | Las compras a cuenta corriente suman deuda cuando se **confirman** |
| El proveedor no aparece al cargar la compra | Está mal escrito o creado dos veces | Buscalo por CUIT; editá el nombre si hace falta |
| No encuentro cómo borrar un proveedor | Desde el POS no hay botón para borrarlos | Dejá de usarlo; el historial de compras y pagos se conserva |

## Cómo comprobar que salió bien

Buscá al proveedor por nombre o CUIT y revisá que sus datos y plazo de pago estén correctos. Un proveedor recién creado aparece sin deuda. Las compras a cuenta corriente empiezan a sumar deuda cuando se confirman.

## Siguiente paso

- [cargar una compra manual en ADEstock](/tutoriales/cargar-compra-manual/)
- [cargar compras con foto e IA en ADEstock](/tutoriales/cargar-compras-con-foto-ia/)
- [pagar a proveedores y registrar adelantos en ADEstock](/tutoriales/pagar-proveedor/)
