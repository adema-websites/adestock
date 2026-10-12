---
id: "configurar-negocio"
slug: "configurar-negocio"
title: "Cómo configurar tu negocio en ADEstock la primera vez"
description: "Al terminar este asistente, ADEstock queda listo para vender: con el nombre de tu negocio, tus depósitos y cajas, las billeteras, los medios de cobro, los…"
category: "empezar"
priority: "P0"
roles: ["dueno"]
surface: ["panel"]
status: "draft"
tiempo: "3 minutos"
necesitas: "el usuario y la contraseña que te dio ADEMA Sistemas"
para_quien: "el dueño, la primera vez que entra al sistema"
modulo: "agenda (onboarding), billetera, venta, producto"
permiso: "ser el primer usuario que entra (superusuario)"
source_path: "01-manual-usuario/02-onboarding-configuracion-inicial.md"
source_hash: "3cda58410aa5244acfd1052bdab61e1758f9880ac22900f812768729d3e7d0ec"
product_version: "pendiente-verificar"
verified_at: "2026-10-12"
reviewed_at: null
synonyms: ["onboarding","primeros pasos","empezar","configuración inicial"]
related: []
social_image: null
---
## Qué vas a lograr

Al terminar este asistente, ADEstock queda **listo para vender**: con el nombre de tu negocio, tus depósitos y cajas, las billeteras, los medios de cobro, los usuarios y un catálogo de ejemplo de tu rubro.

El asistente aparece **una sola vez**. Cuando termina, si volvés a entrar a `/onboarding/` el sistema te lleva directo al POS.

## Paso a paso

### 1. Ingresá al sistema

Escribí tu usuario (1), tu contraseña (2) y presioná **Identificarse** (3).

![Pantalla de ingreso](../../assets/tutoriales/02-onboarding/01-login.png)

### 2. Pantalla de bienvenida

Es solo una presentación. Abajo tenés los contactos de soporte de ADEMA Sistemas. Presioná **Siguiente**.

![Bienvenida](../../assets/tutoriales/02-onboarding/02-bienvenida.png)

### 3. Paso 1: el nombre de tu negocio

Escribí el nombre de tu empresa o negocio. **Aparece en los tickets y en los reportes**, así que escribilo como querés que lo vean tus clientes.

![Nombre del negocio](../../assets/tutoriales/02-onboarding/03-paso1-nombre.png)

### 4. Paso 2: inventarios (depósitos)

Elegí cuántos lugares físicos donde guardás mercadería tenés.

- **Un solo inventario**: tenés un local o un depósito. Es lo más común, y lo que te recomendamos si dudás.

![Un solo inventario](../../assets/tutoriales/02-onboarding/04-paso2-inventarios-uno.png)

- **Múltiples inventarios**: tenés varios depósitos o locales. Indicá cuántos (de 2 a 20). El sistema crea **un punto de venta (caja) por cada depósito**.

![Varios inventarios](../../assets/tutoriales/02-onboarding/05-paso2-inventarios-varios.png)

> Más adelante podés agregar o cambiar depósitos y cajas desde el engranaje del POS (⚙).

### 5. Paso 3: billeteras y medios de cobro

Acá definís **dónde está tu plata** y **cómo te pagan**.

![Medios de pago](../../assets/tutoriales/02-onboarding/06-paso3-medios-pago.png)

**1. Billeteras.** Son las "cuentas" donde el sistema lleva el saldo.
- **Efectivo**: viene activada. Es el dinero de la caja.
- **Caja Fuerte**: para el dinero que guardás aparte.
- **Caja Chica**: para gastos menores.

**2. Medios de cobro.** Son las formas en que te pagan en el POS.
- **Efectivo**: siempre está (no se puede sacar).
- **Tarjetas** y **Transferencia**.
- **Cuenta Corriente (Fiado)**: permite vender y que el cliente pague después. Si fiás a algún cliente, dejala activada.

> El medio *Efectivo* queda vinculado a la billetera *Efectivo*. Así, cada venta en efectivo suma automáticamente a esa billetera.

### 6. Paso 4: usuarios

Indicá cuántas personas van a usar el sistema.

![Usuarios](../../assets/tutoriales/02-onboarding/07-paso4-usuarios.png)

1. **Cajeros**: solo acceden al punto de venta. No ven reportes ni configuración.
2. **Administrativos**: acceso completo (configuración, reportes, productos, compras).

El sistema crea los usuarios con contraseñas de arranque:

| Tipo | Usuarios que crea | Contraseña inicial |
|---|---|---|
| Cajeros | `cajero1`, `cajero2`, … | `Cajero123.` |
| Administrativos | `admin1`, `admin2`, … | `Admin123.` |

> ⚠️ **Cambiá esas contraseñas apenas termines.** Son iguales para todos los negocios. Mirá el tutorial de *Usuarios y permisos*.

Si tenés varios depósitos, los cajeros se reparten entre las cajas en orden (cajero1 → Caja Principal, cajero2 → Caja 2, …).

### 7. Paso 5: el rubro

Elegí el rubro que mejor describe tu negocio.

![Elegir rubro](../../assets/tutoriales/02-onboarding/08-paso5-rubro.png)

Al elegirlo, queda resaltado. Cuando tocás **Finalizar**, el sistema carga **productos, categorías, un proveedor y un cliente de ejemplo** de ese rubro, para que puedas probar el POS enseguida.

![Rubro elegido y Finalizar](../../assets/tutoriales/02-onboarding/09-paso5-rubro-elegido.png)

Rubros disponibles: Almacén, Verdulería, Ferretería, Kiosco, Química, Carnicería, Imprenta, Bazar, Mueblería, Pinturería, Cosmética / Nails y Dietética.

> Los datos de ejemplo se pueden borrar o reemplazar por los tuyos. Mirá *Cargar tus primeros productos*.

### 8. Listo: llegás al POS

Al finalizar, el sistema te lleva al **POS**. Lo primero que ves es la **Apertura de caja**: ingresá con cuánto efectivo empezás el turno (puede ser 0) y presioná **Abrir Turno**.

![POS con la apertura de caja](../../assets/tutoriales/02-onboarding/10-resultado.png)

## Qué pasa por detrás

Al presionar **Finalizar**, el sistema crea de una sola vez (si algo falla, no queda nada a medias):

| Qué | Detalle |
|---|---|
| Configuración | Nombre del negocio, moneda **$ (Pesos)**, precio de venta automático, **permite vender con stock negativo**, guías activadas |
| Grupos de seguridad | *Administrativos* y *Cajeros* |
| Billeteras | Las que tildaste (todas de tipo efectivo, saldo inicial 0) |
| Medios de cobro | Efectivo, y los que tildaste. Más los medios de **compra** (Efectivo, Transferencia, Cuenta Corriente Proveedor) |
| Depósitos y cajas | `Depósito Principal` / `Caja Principal`; si hay varios: `Depósito 2` / `Caja 2`, etc. Todos los medios de cobro quedan disponibles en todas las cajas |
| Estados de seguimiento | Pendiente, Confirmado, Entregado, Cancelado |
| Tu usuario | Pasa al grupo *Administrativos*, con la primera caja y **todos los permisos del POS** |
| Usuarios | Los cajeros y administrativos que pediste, con permisos básicos (los cajeros: solo el scanner de precios) |
| Datos del rubro | Se cargan en segundo plano; pueden tardar unos segundos en aparecer |

Detalle: si elegís **Ferretería**, los módulos de *Picking (armado de pedidos)* y *Cocina/fabricación* quedan **desactivados**. En el resto de los rubros quedan activados.

## Problemas frecuentes

| Si te pasa… | Es porque… | Qué hacer |
|---|---|---|
| Entro a `/onboarding/` y me manda al POS | El asistente ya se completó | Es lo esperado: ya está configurado. Cambiá cosas desde el engranaje del POS |
| No aparecen los productos de ejemplo apenas termino | La carga corre en segundo plano | Esperá unos segundos y actualizá el POS |
| No elegí rubro | Es opcional para el sistema, pero no se cargan datos de ejemplo | Cargá tus productos a mano |
| Quiero más cajas o depósitos | El asistente solo crea los iniciales | Engranaje ⚙ del POS → Puntos de venta |

## Siguiente paso

- Cargar tus primeros productos
- Crear usuarios y asignar permisos
- Recorrido por el POS
