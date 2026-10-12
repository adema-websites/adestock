# Excel: qué hace realmente el producto (base para las guías P0)

Fuente: código de ADEstock `version.py` = **2.5.3**, commit `1dd777d` (12/10/2026): `producto/inventario_excel.py`, `adestock/admin_override.py` (vista `inventario_inicial`) y `producto/admin.py` (ajustes de inventario por Excel). Es lectura de código; **no se ejecutó ningún import** con datos reales. Cada punto marcado ⚠ debe comprobarse en una instalación demo antes de publicar la guía.

## Son dos herramientas distintas

| | Importar catálogo (Inventario inicial) | Cargar/corregir existencias (Ajuste de inventario) |
|---|---|---|
| Dónde | Panel → *Inventario Inicial (Excel)* | Panel → Ajustes de inventario → Importar desde Excel |
| Qué carga | Productos, costo, presentación (`cantidad`), precios de venta | Cantidades a **sumar o restar** por producto |
| Toca el stock | **No** | Sí, pero recién al **aplicar** el ajuste |
| Crea productos | Sí | **No** (si no existe, la fila da error) |
| Vista previa | Sí: tabla "Preview de cambios" (crear/actualizar, precios Excel vs actual) y confirmación | Sin vista previa en el Excel; queda un borrador que se revisa y se aplica |

## Importar catálogo

- **Plantilla:** se descarga desde la misma pantalla (`?export=1`), hoja "Inventario", encabezados en la fila 6 (el importador busca los encabezados en las primeras 10 filas). Incluye los productos ya cargados y listas desplegables (unidad, categoría, marca, proveedor).
- **Columnas obligatorias:** `codigo`, `nombre`, `descripcion`, `categoria`, `cantidad`, `unidad_de_medida`, `costo`. **Opcionales:** `id`, `marca`, `proveedor`, `minimo_compra` y grupos de precio `cantidad_precio_N`, `udm_precio_N`, `rentabilidad_precio_N`, `precio_venta_N` (+ `listas_precio_N` si las listas de precios están activas).
- **`cantidad` no es stock:** es la cantidad de unidades de la presentación sobre la que se expresa el `costo` (p. ej. costo de un bulto de 12). No llamarla "stock" en ninguna guía.
- **Cómo reconoce un producto existente:** primero por `id`; si no, por `codigo` (código de barras). Si no encuentra ninguno, **crea uno nuevo**.
- **Se importa dos veces:** con código o `id`, la segunda vez actualiza (no duplica). **Sin código ni `id`, cada importación crea un producto nuevo** ⚠ → toda fila debe tener código.
- **Qué pisa al actualizar** ⚠ (por lectura de código):
  - `categoria` vacía **deja el producto sin categoría**.
  - `costo` vacío lo deja en **0**; `cantidad` vacía vuelve a 1.
  - `nombre`, `descripcion` y `marca` vacíos se conservan.
  - **Los precios de venta del producto se borran y se recrean desde el archivo, siempre.** Si el archivo no trae columnas de precio, el producto queda **sin precios**.
- **Proveedor:** si el nombre no existe, se **crea** y queda como proveedor principal del producto.
- **Errores:** todo ocurre en una transacción; las listas de precio inexistentes cuentan como error y se omite ese precio (pero los precios anteriores ya se borraron).
- **Resumen final:** "Productos creados, actualizados, precios, errores" (mensaje real de la pantalla).
- **No hay reversión automática** en lo leído. Recomendar descargar la plantilla (que exporta el catálogo actual) **antes** de importar como copia de seguridad.
- **Código de barras como texto:** `codigo` se lee como celda; si Excel lo guardó como número se pierden ceros iniciales ⚠ (comprobar en demo y mostrar cómo formatear la columna como texto).

## Cargar existencias

- Plantilla de ajuste: columnas `ID Producto`, `Código`, `Nombre`, `Cantidad Ajuste`, `Motivo` (los encabezados se buscan por texto, en la fila 1).
- **`Cantidad Ajuste` es una diferencia con signo**, no el stock final: +10 suma 10, −3 resta 3. Filas con 0 o vacío se omiten.
- Se identifica el producto por ID o por código; si no existe, la fila falla y se informa (se muestran hasta 5 errores).
- El **depósito** se elige en el ajuste, no en el Excel: un archivo por depósito.
- El ajuste queda en **borrador**; el stock cambia al **aplicarlo**. Anular existe como acción.
- Para **stock inicial** (productos recién importados, stock 0) la diferencia equivale al stock real. Para **corregir** un stock que ya tiene movimientos, la diferencia hay que calcularla; para eso es más seguro el **Conteo de stock** (guía `contar-stock`), que parte de lo contado.

## Qué implican para las guías

1. `importar-productos-excel`: advertir ANTES de importar sobre precios (se reemplazan), categoría/costo vacíos y filas sin código; explicar el resumen; recomendar copia previa.
2. `cargar-stock-inicial-excel`: secuencia obligatoria *importar catálogo → crear ajuste en el depósito → importar Excel → revisar → aplicar → verificar stock antes/después*.
3. Buscador y `/funciones/productos-y-excel/`: presentar las dos opciones por separado, como pide el plan.
4. No prometer importación de cualquier Excel: solo la plantilla del sistema.

## Para comprobar en una instalación demo (capturas incluidas)

- [ ] Descarga de la plantilla y primera fila de encabezados reales.
- [ ] Importar 3 productos ficticios: pantalla de análisis, confirmación y mensaje de resumen.
- [ ] Reimportar el mismo archivo: no duplica, precios idénticos.
- [ ] Fila sin código: crea duplicado en cada importación.
- [ ] Archivo sin columnas de precio: ¿borra precios?
- [ ] Código `0012345` guardado como número vs texto.
- [ ] Ajuste por Excel: borrador, aplicación, stock antes/después, producto inexistente.
- [ ] ¿La reimportación de un ajuste en borrador reemplaza o suma? (`update_or_create` por producto: reemplaza el detalle del mismo producto en ese ajuste).

## Verificado el 12/10/2026 (importador real, base de demo copiada, ADEstock 2.5.3)

Se ejecutó `import_inventario_excel` y `analyze_inventario_excel` con libros generados:

| Prueba | Resultado |
|---|---|
| Alta de 3 productos con código y precio | creados 3, precios 3, errores 0 |
| Reimportar el mismo archivo | creados 0, actualizados 3: **no duplica** |
| Código `12345` (número) cuando existe `0012345` (texto) | **crea un producto nuevo** (se pierden los ceros) |
| Fila sin código, importada 2 veces | **2 productos nuevos** con el mismo nombre |
| Categoría vacía y costo vacío sobre un producto existente | categoría **None**, costo **0**; el precio se actualiza |
| Archivo sin columnas de precio sobre un producto con precio | el producto queda **sin precios** |
| Vista previa (analyze) | informa filas, grupos de precio y filas con precio; la pantalla agrega la tabla de cambios |

### Ajuste de inventario por Excel (verificado por la interfaz, base copiada)

| Prueba | Resultado |
|---|---|
| Formulario del ajuste | Requiere **fecha** y **depósito**; tipo "Inventario Inicial"; estado Borrador |
| Excel con 2 filas válidas, 1 con cantidad 0 y 1 con código inexistente | "Se importaron 2…", "Se omitieron 1… cantidad de ajuste = 0", "Se encontraron 1 error(es): Fila 5: Producto no encontrado (ID: None, Código: NOEXISTE999)" |
| Stock antes de aplicar | Sin cambios (el ajuste está en Borrador) |
| Aplicar (acción "Aplicar ajustes seleccionados") | "Se aplicaron 1 ajuste(s) correctamente"; Yerba 76 → 86, Aceite 42 → 47; la fila con 0 no cambia |
| Semántica | La cantidad **se suma** al stock existente (no lo fija) |

Sin verificar: reimportar sobre un borrador ya cargado, anulación y ajustes con cantidades negativas.
