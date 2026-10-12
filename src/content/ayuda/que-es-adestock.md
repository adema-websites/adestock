---
id: "que-es-adestock"
slug: "que-es-adestock"
title: "Qué es ADEstock y dónde se hace cada cosa"
description: "ADEstock es el sistema de gestión de un comercio: vende (POS), controla el stock, lleva las cuentas corrientes de clientes y proveedores, la caja, las compras y te…"
orden: 1
status: "draft"
source_path: "00-inicio/README.md"
source_hash: "5ad8802d217cbd264c7d8bd2ff23af312e0af390314b58e4996f2ab6cd223fa1"
product_version: "3.0.0"
verified_at: "2026-10-12"
reviewed_at: null
reviewed_by: null
synonyms: ["empezar","qué es adestock","glosario","roles","permisos","pos","panel","app del dueño"]
social_image: null
---
ADEstock es el sistema de gestión de un comercio: **vende** (POS), **controla el stock**, lleva las **cuentas corrientes** de clientes y proveedores, la **caja**, las **compras** y te muestra **cómo viene el negocio**.

Esta guía te ubica en cinco minutos. Después seguí con los tutoriales paso a paso.

## Las tres «puertas» del sistema

| Puerta | Para qué se usa | Quién la usa | Cómo se entra |
|---|---|---|---|
| **POS** (punto de venta) | Vender, cobrar, abrir y cerrar la caja, gastos, retiros, cuenta corriente de clientes, conteo de stock. **Lo del día a día.** | Cajeros, encargados y dueño | Navegador, dirección del sistema → `/pos/` |
| **App del dueño** | Ver **cómo viene el negocio** desde el celular: ventas, ganancia, deudas, productos, proveedores | Dueño y administrativos | `/app/` (ver [tutorial 30](/tutoriales/usar-app-del-dueno/)) |
| **Panel de administración** | Revisar y corregir: ventas, compras, turnos, billeteras, precios masivos, ofertas, revistas, respaldos | Dueño y administrativos | Menú rápido del POS → *Panel de administración* |

> **Regla práctica:** si es algo que pasa **mientras se atiende** → POS. Si querés **mirar el negocio** → App. Si hay que **corregir, configurar o auditar** → Panel.

## Quién puede hacer qué

| Rol | Qué es | Qué ve |
|---|---|---|
| **Dueño** (superusuario) | Tiene **todos** los permisos, siempre | Todo: POS, App, Panel, usuarios, configuración |
| **Administrativo** | Persona de administración con acceso a la gestión | POS según sus permisos + **App del dueño** |
| **Cajero** | Atiende en una caja | Solo lo que el dueño le habilitó en el POS. **No** entra a la App |

El dueño decide los permisos de cada uno en el POS (*Menú rápido → Usuarios*). Ver [Crear usuarios y asignar permisos](/tutoriales/usuarios-y-permisos/).

## Dónde se hace cada cosa

| Quiero… | Lo hago en… | Tutorial |
|---|---|---|
| Configurar el negocio por primera vez | Pantalla de inicio (onboarding) | [02](/tutoriales/configurar-negocio/) |
| Cargar productos | POS → Menú rápido → Crear producto (F6) | [03](/tutoriales/cargar-productos/) |
| Vender y cobrar | POS | [07](/tutoriales/hacer-una-venta/), [08](/tutoriales/cobrar-con-varios-medios-de-pago/) |
| Vender «fiado» | POS (cuenta corriente) | [09](/tutoriales/vender-fiado-cuenta-corriente/), [17](/tutoriales/cobrar-deuda-cliente/) |
| Abrir/cerrar la caja | POS | [12](/tutoriales/abrir-y-cerrar-caja/) |
| Cargar una compra | POS → Menú rápido → Compras (carga rápida); se confirma en el Panel | [19](/tutoriales/cargar-compra-manual/), [20](/tutoriales/cargar-compras-con-foto-ia/) |
| Contar el stock | POS → Conteo de stock | [23](/tutoriales/contar-stock/) |
| Subir precios en bloque | POS → Menú rápido → Precios masivos | [25](/tutoriales/actualizar-precios-y-rentabilidad/) |
| Hacer ofertas y revistas | POS → Menú rápido → Ofertas / Revistas y folletos | [26](/tutoriales/crear-ofertas-y-promociones/), [27](/tutoriales/crear-revista-ofertas/) |
| Ver cómo viene el negocio | App del dueño | [30](/tutoriales/usar-app-del-dueno/) |
| Controlar los turnos de caja | Panel | [32](/tutoriales/controlar-turnos-caja-panel/) |
| Armar pedidos para entregar | Celular → `/picking/` | [34](/tutoriales/armar-pedidos-picking/) |
| Hacer copias de seguridad | Panel → Respaldos | [37](/tutoriales/respaldos/) |
| Conectar la impresora | POS → engranaje → Impresora de tickets | [38](/tutoriales/instalar-agente-de-impresion/) |

## Glosario

| Palabra | Qué significa |
|---|---|
| **POS** | Punto de venta: la pantalla donde se cobra |
| **Caja / punto de venta** | Un puesto de cobro. Cada caja tiene su depósito, su impresora y sus medios de cobro |
| **Turno** | El período entre que el cajero **abre** y **cierra** la caja. Todo pago, gasto y retiro pertenece a un turno |
| **Arqueo** | Comparar el efectivo que **debería haber** con el que **se contó** |
| **Medio de pago / de cobro** | Efectivo, tarjeta, transferencia, cuenta corriente… |
| **Presentación** | Cada forma de vender un producto: unidad, pack de 6, caja… cada una con su precio |
| **Rentabilidad** | El margen que te queda sobre un precio |
| **Depósito** | Un lugar donde hay stock (local, salón, trastienda) |
| **Cuenta corriente (CC)** | Lo que un cliente te debe (fiado) o lo que vos le debés a un proveedor |
| **Stock disponible / físico** | Disponible = lo que se puede vender; físico = lo que realmente hay en el depósito |
| **Merma** | Pérdida de mercadería (vencido, roto…) |
| **Picking / armado** | Juntar la mercadería de un pedido |
| **Nota de crédito / débito** | Comprobante que corrige una venta cuando faltó mercadería (ver [35](/tutoriales/notas-de-credito-y-debito/)) |
| **OCR** | Cargar una compra sacándole una foto a la boleta |
| **Agente de impresión** | Programa en la PC de la caja que imprime lo que manda el sistema |

## Por dónde empezar

1. **Nuevo en el sistema:** [02 Onboarding](/tutoriales/configurar-negocio/) → [03 Productos](/tutoriales/cargar-productos/) → [04 Usuarios](/tutoriales/usuarios-y-permisos/) → [06 Recorrido del POS](/tutoriales/usar-punto-de-venta/).
2. **Cajero:** [06](/tutoriales/usar-punto-de-venta/) → [07](/tutoriales/hacer-una-venta/) → [08](/tutoriales/cobrar-con-varios-medios-de-pago/) → [12](/tutoriales/abrir-y-cerrar-caja/).
3. **Dueño:** [30 App del dueño](/tutoriales/usar-app-del-dueno/) → [32 Turnos](/tutoriales/controlar-turnos-caja-panel/) → [37 Respaldos](/tutoriales/respaldos/).

El índice completo de tutoriales está en el [README de la documentación](/tutoriales/). Si algo no funciona, mirá las [Preguntas frecuentes](/ayuda/preguntas-frecuentes/).
