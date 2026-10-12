# Manual de Onboarding (Configuración Inicial)

Este documento explica la configuración inicial (onboarding) y lo que deja listo el sistema después de completarla.

---

## ¿Cuándo aparece?
El onboarding se muestra automáticamente la primera vez que entrás al sistema, antes de usar el punto de venta o módulos administrativos.

---

## Preguntas del onboarding (5 pasos)

### 1) Nombre del negocio
**Pregunta:** “Dime el nombre de tu negocio”.

**¿Para qué sirve?**
- Se guarda en la configuración general.
- Aparece en tickets y reportes.

---

### 2) Inventarios
**Pregunta:** “¿Tenés 1 o más inventarios?”
- **Un solo inventario**: todo el stock en un solo lugar.
- **Múltiples inventarios**: varios depósitos o locales.

Si elegís múltiples, el sistema pide: **cantidad de inventarios** (mín. 2, máx. 20).

**Resultado:**
- Se crean los depósitos necesarios.
- Se crea **1 caja/punto de venta por cada depósito**.

---

### 3) Medios de pago y billeteras
**Pregunta:** “Configurá tus cuentas y medios de cobro”.

**Billeteras a crear (opcional):**
- Efectivo (recomendado y seleccionado por defecto)
- Caja Fuerte
- Caja Chica

**Medios de cobro (seleccionables):**
- Efectivo (siempre activo)
- Tarjetas
- Cuenta Corriente (Fiado)
- Transferencia

**Resultado:**
- Se crean billeteras según lo elegido.
- Se crean medios de pago y se vinculan automáticamente con las billeteras.

---

### 4) Usuarios
**Pregunta:** “¿Cuántos cajeros y cuántos administrativos usarán el sistema?”

**Resultado:**
- Se crean usuarios de tipo **Cajero** y **Administrativo**.
- Los cajeros quedan asignados a cajas (distribución automática).
- Los administrativos quedan con permisos completos.

> Nota: se generan usuarios con contraseñas por defecto (ver sección “Qué deja listo”).

---

### 5) Rubro del negocio
**Pregunta:** “Seleccioná el rubro que mejor describe tu negocio”.

**Resultado:**
- Se cargan **datos de ejemplo** (categorías, productos, precios, etc.) según el rubro elegido.

---

## Qué deja listo el onboarding (configuración general)

Al finalizar, el sistema queda listo con la siguiente configuración:

### Configuración base
- **Moneda principal y secundaria:** Pesos ($).
- **Precio de venta automático:** activado.
- **Venta con stock negativo:** permitida.
- **Guías maestras:** activadas.
- **Generación automática de códigos:** desactivada.
- **Rentabilidad sobre venta:** activada.

### Seguridad y usuarios
- Crea grupos de seguridad: **Administrativos** y **Cajeros**.
- El usuario que realizó el onboarding queda:
  - En el grupo **Administrativos**.
  - Con permisos completos.
  - Asignado a la **Caja Principal**.

**Usuarios creados automáticamente:**
- Cajeros: `cajero1`, `cajero2`, ...
  - Contraseña: `Cajero123.`
- Administrativos: `admin1`, `admin2`, ...
  - Contraseña: `Admin123.`

> Recomendación: cambiar contraseñas después del primer ingreso.

### Cajas y depósitos
- Se crean depósitos (inventarios) según la cantidad indicada.
- Se crea **1 caja por depósito** (Caja Principal, Caja 2, Caja 3, etc.).
- Todos los medios de pago quedan disponibles en todas las cajas.

### Billeteras y medios
- Billeteras (según selección): Efectivo, Caja Fuerte, Caja Chica.
- Medios de pago creados: Efectivo (obligatorio), Tarjetas, Cuenta Corriente, Transferencia.
- Medios de compra creados: Efectivo, Transferencia, Cuenta Corriente Proveedor.

### Estados de seguimiento (ventas / pedidos)
Se crean estados básicos para seguimiento:
- Pendiente
- Confirmado
- Entregado
- Cancelado

---

## Qué deja listo según el tipo de negocio (rubro)

Al elegir un rubro, el sistema ejecuta una carga automática de datos de ejemplo (productos, categorías y precios) adaptada a ese negocio. Esto te permite empezar a operar de inmediato y luego ajustar lo que necesites.

**Rubros disponibles y lo que carga cada uno:**

- **Almacén**
  - Categorías y productos típicos de almacén.
  - Proveedor y cliente de ejemplo.
  - Precios de venta iniciales.

- **Ferretería**
  - Categorías y productos frecuentes de ferretería.
  - Proveedor y cliente de ejemplo.
  - Precios de venta iniciales.

- **Kiosco**
  - Categorías y productos habituales (golosinas, bebidas, etc.).
  - Proveedor y cliente de ejemplo.
  - Precios de venta iniciales.

- **Carnicería**
  - Categorías por tipo de carne.
  - Productos por kilo y cortes habituales.
  - Proveedor y cliente de ejemplo.
  - Precios de venta iniciales.

- **Imprenta**
  - Categorías para papelería, impresión y diseño.
  - Productos y servicios típicos.
  - Proveedor y cliente de ejemplo.
  - Precios de venta iniciales.

- **Bazar**
  - Categorías y productos típicos de bazar.
  - Proveedor y cliente de ejemplo.
  - Precios de venta iniciales.

- **Mueblería**
  - Categorías y productos de muebles y accesorios.
  - Proveedor y cliente de ejemplo.
  - Precios de venta iniciales.

- **Pinturería**
  - Categorías de pinturas, accesorios y herramientas.
  - Productos típicos del rubro.
  - Proveedor y cliente de ejemplo.
  - Precios de venta iniciales (con escalas por litro/volumen en algunos casos).

- **Cosmética / Nails**
  - Categorías y productos de insumos de uñas.
  - Precios con escalas (unidad, pack, etc.).
  - Proveedor y cliente de ejemplo.
  - **Incluye una receta/combo** con insumos asociados.

> Estos datos son de ejemplo y pueden editarse o eliminarse luego.

---

## Siguiente paso recomendado
Una vez finalizado el onboarding:
1. Revisá **productos y precios**.
2. Ajustá **usuarios y permisos**.
3. Configurá **moneda secundaria** y **tipo de cambio** si corresponde.
4. Empezá a operar desde el punto de venta.
