---
id: "cargar-listas-precios-proveedores"
slug: "cargar-listas-precios-proveedores"
title: "Cómo cargar listas de precios de proveedores en ADEstock"
description: "Importá listas de precios de proveedores en ADEstock desde Excel, CSV, PDF o fotos. Asociá productos, compará valores y publicá los precios revisados."
category: "compras"
priority: "P1"
roles: ["dueno","administrativo"]
surface: ["panel"]
status: "published"
tiempo: "5 minutos por lista"
necesitas: "el módulo Listas de precios de proveedores activado y la lista del proveedor (Excel, CSV, PDF o foto)"
para_quien: "dueños y administrativos que quieren saber quién les vende más barato"
modulo: "compra (Listas de precios de proveedor), gerencia (Comparar proveedores)"
permiso: "módulo \"Listas de precios de proveedores\" activado"
source_path: "01-manual-usuario/22-listas-de-precios-de-proveedores.md"
source_hash: "eabd94142c1af1deeaf01d86a0300258a24aaa4af8ada11e7625e448f66e1699"
product_version: "3.0.0"
verified_at: "2026-10-12"
reviewed_at: "2026-10-13"
reviewed_by: "ademasistemas"
synonyms: ["lista de precios","lista proveedor excel","comparar precios"]
related: ["cargar-compras-con-foto-ia","usar-app-del-dueno","actualizar-precios-y-rentabilidad"]
social_image: "/social/cargar-listas-precios-proveedores-v1.jpg"
---
## Para qué sirve

Esta sección sirve para tener **la lista de precios de cada proveedor cargada en el sistema**, y así comparar cuánto sale cada producto en cada uno y decidir **dónde te conviene comprar**.

Cada proveedor tiene su propia lista, pero casi siempre la manda con el mismo formato: agrega artículos o cambia precios, no cambia la forma del archivo. Por eso el trabajo fuerte se hace **una sola vez por proveedor**: cargás la lista y asociás sus renglones con tus productos. Cuando llega una lista nueva, la subís de nuevo y el sistema, que ya sabe cómo escribe ese proveedor cada producto, reconoce casi todo solo. Solo revisás lo nuevo.

Para qué te sirve tener las listas cargadas:

- **Comparar:** ves cuánto cuesta un producto en cada proveedor y si el precio que te ofrecen es más barato o más caro que tu costo actual.
- **Comprar donde conviene:** la pantalla **Compra inteligente** del panel de administración arma la reposición de los productos con poco stock y, para cada uno, te sugiere el proveedor con el **precio vigente más bajo** entre las listas cargadas.
- **Tener los precios al día:** cada lista nueva reemplaza a la anterior como precio vigente, y la anterior queda como historial.

Para que la sugerencia sirva, mantené las listas actualizadas. Y ojo: el sistema compara el precio tal como figura en cada lista, sin convertir cajas a unidades; si dos proveedores listan distinto, revisalo antes de decidir.

## Qué vas a lograr

Vas a **cargar una lista de precios de proveedor en ADEstock**, asociar cada renglón a tu catálogo y comparar los valores ofrecidos con tu costo actual. Podés revisar la carga, guardarla como borrador y publicar los precios cuando estén correctos.

Publicar una lista guarda los precios de referencia del proveedor. El costo de tus productos se actualiza mediante las compras confirmadas con actualización de costo habilitada.

> **Importante:** publicar una lista **no cambia el costo de tus productos**. Guarda *el precio que ofrece ese proveedor*. Tu costo cambia recién cuando le **comprás** (ver [Cargar una compra](/tutoriales/cargar-compra-manual/)).

## Antes de empezar

El dueño activa el módulo en **Menú rápido → Configuración → Módulos y sistema → Listas de precios de proveedores**.

Formatos aceptados: **CSV, XLSX, DOCX, PDF** y **fotos** (JPG, PNG, WEBP). Con CSV y Excel el sistema lee las columnas directamente; con PDF y fotos usa lectura con IA (como en la compra con foto).

## Paso a paso

Abrí **Menú rápido (F8) → Listas de proveedores** (dirección `/compras/proveedores-ocr/`). Aparece cuando el módulo está activado.

### 1. Elegí el proveedor y el archivo

![Inicio](../../assets/tutoriales/22-listas-proveedores/01-inicio.png)

| # | Elemento | Qué es |
|---|---|---|
| 1 | **Desde archivo** | Subís la lista del proveedor |
| 2 | **Carga manual** | Cargás los precios a mano, producto por producto |
| 3 | **Proveedor base** | El proveedor de la lista. Si no lo elegís, el sistema trata de detectarlo |
| 4 | **Procesar lista** | Lee el archivo |

Elegí el proveedor, el archivo y tocá **Procesar lista**.

### 2. Revisá lo que leyó

![Lista procesada](../../assets/tutoriales/22-listas-proveedores/02-lista-procesada.png)

Arriba ves un resumen: **proveedor detectado**, **moneda** y **cantidad de renglones**. Abajo, la revisión:

| # | Botón | Qué hace |
|---|---|---|
| 1 | **Filtro** | Muestra todos, solo los asociados (*Matcheados*), los *No matcheados*, los *Actualizados* o los *Ignorados* |
| 2 | **Guardar borrador** | Guarda tu avance para seguir después (queda en *Listas guardadas*) |
| 3 | **Publicar precios** | Confirma y deja vigentes los precios de esta lista |

### 3. Controlá cada renglón

![Renglones](../../assets/tutoriales/22-listas-proveedores/03-renglones.png)

| # | Columna | Qué significa |
|---|---|---|
| 1 | **Producto OCR** | Lo que dice la lista del proveedor, con el precio leído |
| 2 | **Producto / match del sistema** | **Tu** producto asociado. Si está en verde (*Match*) ya lo reconoció |
| 3 | **Costo actual** | Lo que hoy te cuesta ese producto, con un indicador |
| 4 | **Costo nuevo** | El precio de la lista. Podés corregirlo |

**El indicador de costo** compara el precio del proveedor contra tu costo actual:

- 🟢 **OK**: el proveedor te lo ofrece al mismo precio o **más barato**.
- 🔴 **Más caro**: el proveedor te lo ofrece **más caro** que tu costo actual.

En el ejemplo, el aceite figura **Más caro** ($ 2.780 contra tu costo de $ 2.250), mientras que el arroz ($ 1.480 vs. $ 1.500) y los fideos ($ 840 vs. $ 850) están **OK**.

Cada renglón tiene sus propias acciones:

| Botón | Qué hace |
|---|---|
| **Buscar** | Si está *Sin asociar* (estado **Revisión**), buscás tu producto y lo asociás |
| **Guardar fila** | Guarda solo ese renglón |
| **Publicar fila** | Publica el precio de ese renglón sin esperar al resto |
| **Eliminar fila** | Lo saca de la carga |
| **Ignorar** | Lo marca para que no se publique (queda registrado como ignorado) |

También podés **agregar una fila manual** a la revisión con el buscador de arriba (*Agregar fila manual a esta revisión*).

### 4. Ignorá o asociá los renglones sin producto

El renglón que no encontró producto (*Sin asociar*) queda en **Revisión**. Asocialo con **Buscar**, o tocá **Ignorar** si no lo vendés.

![Renglón ignorado](../../assets/tutoriales/22-listas-proveedores/04-renglon-ignorado.png)

### 5. Publicá

Tocá **Publicar precios**. El sistema te pregunta cuántos precios va a cambiar:

![Confirmar publicación](../../assets/tutoriales/22-listas-proveedores/05-confirmar-publicacion.png)

> *Se cambiarán 5 precios vigentes de proveedor. Si no querés cambiar los precios ahora, usá Guardar borrador.*

Confirmá con **Publicar ahora**.

![Publicado](../../assets/tutoriales/22-listas-proveedores/06-publicado.png)

## Dónde quedan los precios

En el panel de administración, **Compra → Precios proveedores desde listas**: un renglón por proveedor y producto, con su precio, moneda y de qué carga viene.

![Precios por proveedor](../../assets/tutoriales/22-listas-proveedores/07-precios-por-proveedor-en-admin.png)

## Comparar proveedores

Hay dos formas de comparar, según lo que quieras saber:

| Quiero saber… | Dónde |
|---|---|
| **Si el precio de una lista es mejor o peor que mi costo** | En esta pantalla, columna *Costo actual* / *Costo nuevo* con el indicador **OK / Más caro** |
| **Qué proveedor me conviene para cada producto** | En el panel de administración, **Compra inteligente** (botón en el inicio del panel): para cada producto con poco stock sugiere el proveedor con el precio vigente más bajo de tus listas. Todos los precios cargados se ven en **Compra → Precios proveedores desde listas** |
| **A quién le compré más barato de verdad** (y cuánto pagué de más) | En la **app de la dueña** (`/app/`), pantallas **Proveedores** y **Comparar proveedores**. Esa comparación usa **tus compras reales confirmadas**, no las listas |

## Qué pasa por detrás

| Qué | Detalle |
|---|---|
| Lectura | CSV/Excel: se leen las columnas (código, descripción, precio). PDF/foto: lectura con IA |
| Asociación | Cada renglón se compara con tus productos por nombre; lo que no encuentra queda en *Revisión* y lo asociás vos |
| Publicar | Guarda el precio del proveedor para cada producto como **precio vigente** de esa lista |
| Costo del producto | **No cambia**: se actualiza solo cuando cargás una compra |
| Historial | Cada carga queda guardada (borrador, confirmada) y se puede reabrir desde *Listas guardadas* |

## Problemas frecuentes

| Si te pasa… | Es porque… | Qué hacer |
|---|---|---|
| No veo la pantalla | El módulo está apagado | Configuración → Módulos y sistema → *Listas de precios de proveedores* |
| Muchos renglones quedan en *Revisión* | Los nombres de la lista difieren de los tuyos | Asocialos uno a uno con **Buscar** (o ignoralos) antes de publicar |
| Me equivoqué al publicar | - | Cargá la lista correcta y publicá de nuevo |
| Quiero seguir mañana | - | **Guardar borrador** y reabrí desde *Listas guardadas* |
| El precio se leyó mal (PDF/foto) | Calidad de la imagen | Corregilo en **Costo nuevo** antes de publicar |

## Cómo comprobar que salió bien

Abrí **Compra → Precios proveedores desde listas** y verificá proveedor, producto, moneda y precio publicado. Los renglones que ignoraste deben quedar fuera de la publicación. Comprobá que el costo de tus productos conserve su valor: publicar la lista no registra una compra.

## Siguiente paso

- [cargar compras con foto e IA en ADEstock](/tutoriales/cargar-compras-con-foto-ia/)
- [consultar ventas y stock desde la app de ADEstock](/tutoriales/usar-app-del-dueno/)
- [actualizar precios masivos y márgenes en ADEstock](/tutoriales/actualizar-precios-y-rentabilidad/)
