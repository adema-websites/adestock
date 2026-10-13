---
id: "importar-productos-excel"
slug: "importar-productos-excel"
title: "Cómo importar productos y precios desde Excel en ADEstock"
description: "Importá productos y precios a ADEstock con una plantilla Excel. Conservá los códigos de barras, revisá los cambios y confirmá la carga del catálogo."
category: "empezar"
priority: "P0"
roles: ["dueno","administrativo"]
surface: ["panel"]
status: "published"
tiempo: "10 minutos"
necesitas: "ser el dueño o tener acceso al panel de administración, y un archivo con tus productos"
para_quien: "dueños y administrativos"
modulo: "Producto > Inventario Inicial (Excel)"
permiso: "acceso al panel de administración"
source_path: "docs/EXCEL-HALLAZGOS.md"
source_hash: "4aa75b7495be7d5a59ba111e704a956912d4756a2a025bf50e3ff4c8575398a6"
product_version: "3.0.1"
verified_at: "2026-10-12"
reviewed_at: "2026-10-13"
synonyms: ["subir productos de planilla","planilla","excel","importar catálogo","cargar catálogo","plantilla","cargar muchos productos"]
related: ["cargar-stock-inicial-excel","cargar-productos","hacer-una-venta"]
social_image: "/social/importar-productos-excel-v1.jpg"
---
## Para qué sirve

Sirve para cargar de una sola vez el catálogo que ya tenés en una planilla, en lugar de dar de alta producto por producto. Es lo más útil al **empezar a usar el sistema** o cuando recibís muchos productos nuevos o cambios de precio. Antes de confirmar ves cuáles productos son nuevos y cuáles se actualizan. Carga productos y precios, **no el stock**: para eso está [stock inicial desde Excel](/tutoriales/cargar-stock-inicial-excel/).

## Qué vas a lograr

Vas a **importar productos, costos y precios desde Excel a ADEstock** usando la plantilla del sistema. La vista previa te permite distinguir los productos nuevos de los que se actualizarán antes de confirmar.

Esta importación carga el catálogo y sus precios. Para cargar existencias por depósito, continuá con [stock inicial desde Excel](/tutoriales/cargar-stock-inicial-excel/).

> Esta herramienta carga **productos y precios**. **No carga cuánta mercadería tenés**: el stock se carga con un [ajuste de inventario desde Excel](/tutoriales/cargar-stock-inicial-excel/).

## Antes de empezar

- Tené a mano tus productos con **código de barras**, nombre, categoría, costo y precio de venta.
- Si ya tenés productos cargados, **descargá primero la plantilla**: trae tu catálogo actual y te permite comparar los datos antes de importar. También hacé una [copia de seguridad del sistema](/tutoriales/respaldos/): la plantilla no reemplaza ese respaldo.

## Paso a paso

### 1. Abrí la pantalla

En el panel, entrá a **Producto > Inventario Inicial (Excel)**.

![Pantalla Inventario Inicial (Excel)](../../assets/web-excel/01-pantalla.png)

### 2. Descargá la plantilla

Tocá **Descargar plantilla**. Se baja un Excel con tus productos actuales y las columnas que el sistema espera.

| Columna | Qué poner |
|---|---|
| **codigo** | El código de barras. Es lo que identifica al producto |
| **nombre**, **descripcion** | Cómo lo ves en el sistema |
| **categoria** | Si no existe, se crea |
| **cantidad** y **unidad_de_medida** | La presentación sobre la que está expresado el costo (por ejemplo, un bulto de 12). **No es el stock** |
| **costo** | Costo de esa presentación |
| **cantidad_precio_1**, **udm_precio_1**, **rentabilidad_precio_1**, **precio_venta_1** | Un precio de venta. Para más precios, repetí el grupo hacia la derecha (_2, _3…) |

### 3. Completá la planilla

- Cargá **un producto por fila** y **siempre el código**.
- Guardá el archivo como **.xlsx**.
- No cambies los nombres de las columnas.

### 4. Subí el archivo y revisá la vista previa

Elegí el archivo y tocá el botón para subirlo. Antes de aplicar nada, el sistema te muestra qué va a hacer con cada fila:

![Vista previa de cambios con acción crear, código, nombre y precios](../../assets/web-excel/03-vista-previa.png)

| Columna | Qué te dice |
|---|---|
| **Acción** | *crear* si el código es nuevo, o *actualizar* si ya existe |
| **Precios (Excel)** / **Precios (actual)** | Lo que vas a cargar contra lo que hay hoy |

Mirá que las filas y los precios sean los que esperás.

### 5. Confirmá

Si está todo bien, tocá **Confirmar importación**. Al terminar vas a ver un resumen con **productos creados, actualizados, precios y errores**.

## Antes de confirmar: qué datos reemplaza la importación

Estos puntos los comprobamos con el importador de ADEstock 2.5.3 en una base de prueba:

- **Los precios de venta de cada producto se reemplazan por los del archivo.** Si el archivo no trae columnas de precio, el producto queda **sin precios de venta**.
- **Una categoría vacía deja el producto sin categoría**, y un **costo vacío lo deja en 0**.
- **Si una fila no tiene código, se crea un producto nuevo cada vez que importás.** Importar dos veces el mismo archivo sin códigos te duplica todo.
- **El código tiene que ser el mismo texto.** Si en Excel guardás el código como número, pierde los ceros del principio (`0012345` pasa a `12345`) y el sistema lo toma como otro producto. Formateá la columna **codigo** como **Texto** antes de pegar los códigos.
- **No hay deshacer.** Conservá la plantilla original y un respaldo del sistema antes de confirmar.

## Cómo comprobar que salió bien

1. Abrí **Producto > Productos** y buscá un par de códigos del archivo.
2. Revisá que el **nombre**, la **categoría** y el **costo** sean los esperados.
3. Abrí uno y mirá que tenga sus **precios de venta**.
4. En el POS, buscá el producto: tiene que aparecer con su precio.

## Problemas frecuentes

| Si te pasa… | Es porque… | Qué hacer |
|---|---|---|
| "El archivo no tiene las columnas requeridas. Usá la plantilla." | Falta alguna columna obligatoria (codigo, nombre, descripcion, categoria, cantidad, unidad_de_medida, costo) o cambió su nombre | Volvé a descargar la plantilla y copiá tus datos ahí |
| "No se pudo leer el archivo" | No es un Excel válido (.xlsx) | Guardalo de nuevo como **.xlsx** |
| Se duplicaron los productos | Las filas no tenían código | Completá los códigos para evitar nuevos duplicados. Revisá los registros ya creados con el administrador antes de volver a importar |
| Productos sin precio | El archivo no tenía columnas de precio | Reimportá con los grupos de precio completos |
| El producto aparece como nuevo en vez de actualizado | El código cambió (por ejemplo, sin ceros iniciales) | Corregí el formato de la columna **codigo** a **Texto** |

## Siguiente paso

- [cargar el stock inicial desde Excel en ADEstock](/tutoriales/cargar-stock-inicial-excel/)
- [cargar productos, stock y precios en ADEstock](/tutoriales/cargar-productos/)
- [hacer una venta y cobrar en efectivo en ADEstock](/tutoriales/hacer-una-venta/)
