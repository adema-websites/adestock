# Importación/Exportación masiva de Recetas (Excel)

## Objetivo
Permitir que un usuario cargue **recetas** e **ingredientes** de forma masiva y segura, con un Excel que además **calcule costos** (costo total de receta y costo por porción). El flujo debe ser simple, con validaciones para evitar errores en claves foráneas.

---

## Cómo funciona hoy el costo de recetas (lógica actual del sistema)
Estas son las piezas clave que ya existen y vamos a respetar:

- **Producto.costo_unitario()**: si el producto no es receta, calcula costo unitario con `costo / cantidad`. Si el producto usa una receta (`fabricacion_propia`), el costo unitario es `receta.costo_porcion()`.
- **receta.costo_receta()**:
  - Suma **insumos** (tabla `productoReceta`) con conversiones entre unidades.
  - Suma **gastos adicionales** de la receta.
  - Suma **subrecetas** (si existen).
- **receta.costo_porcion()**: divide el costo total por `Porciones`.

La conversión de unidades que se aplica en costo está en `cocina.models.receta.costo_receta()`:
- Si el insumo está en **Gramos/Mililitros** y el producto está en **Kilos/Litros**, divide por 1000.
- Si el insumo está en **Kilos/Litros** y el producto está en **Gramos/Mililitros**, multiplica por 1000.
- Si la unidad coincide, costo directo.

---

## Diseño del Excel
El Excel tendrá **2 hojas**:

### 1) Hoja “Inventario” (Referencia)
**Objetivo**: mostrar todos los productos con su costo unitario para facilitar la elección de insumos y permitir fórmulas en la hoja de recetas.

Columnas:
- `producto_id` (ID real de Producto)
- `codigo`
- `nombre`
- `unidad_medida`
- `costo_unitario` (calculado en backend con `Producto.costo_unitario()`)

> Esta hoja es de referencia y NO se importa.

---

### 2) Hoja “Recetas” (Carga masiva)
La hoja tendrá **dos tablas**: **RECETAS** e **INGREDIENTES**. Ambas con headers claros y ayudas.

#### Tabla A: RECETAS (arranca en fila 6)
Columnas de entrada:
- `receta_id` (opcional): si existe, se **actualiza**.
- `receta_ref` (obligatorio si es nueva): texto corto único dentro del Excel, para asociar ingredientes.
- `nombre`
- `descripcion`
- `porciones`
- `categoria_id` o `categoria_nombre`
- `comentarios`

Columnas de cálculo (solo lectura):
- `costo_total` (suma de ingredientes + adicionales + subrecetas si existieran)
- `costo_porcion` (costo_total / porciones)

#### Tabla B: INGREDIENTES (debajo de la tabla A)
Columnas de entrada:
- `receta_ref` o `receta_id` (uno de los dos, para vincular)
- `producto_id` (FK a Inventario)
- `cantidad`
- `medida_uso` (lista: Unidades, Kilos, Gramos, Litros, Mililitros, Mt2s)

Columnas de cálculo (solo lectura):
- `producto_nombre` (busca por `producto_id`)
- `unidad_producto` (busca por `producto_id`)
- `costo_unitario_producto` (busca en Inventario)
- `costo_ingrediente` (costo_unitario ajustado por conversión * cantidad)

> En Excel, las columnas de cálculo se llenan con **fórmulas**. La importación solo lee columnas de entrada.

---

## Reglas de validación (para evitar errores)
1. **receta_id**: si está, la receta debe existir.
2. **receta_ref**: es obligatorio si se crea una receta nueva.
3. **producto_id** debe existir en Inventario.
4. **medida_uso** debe ser compatible con la unidad del producto (mismas reglas que `productoReceta.clean`).
5. Un producto **no puede ser insumo de su propia receta** si está asociado por `fabricacion_propia` (se valida al importar).

---

## Flujo de Importación (propuesto)
1. **Exportar plantilla** desde un nuevo botón en el Admin (similar a Inventario Inicial).
2. Usuario completa hoja **Recetas** (tablas de Recetas e Ingredientes).
3. **Subir Excel** → el sistema analiza y muestra resumen (recetas nuevas/actualizadas, errores).
4. **Confirmar** → se ejecuta importación en una transacción:
   - Si `receta_id` existe: actualiza campos y **reemplaza ingredientes**.
   - Si receta nueva: crea receta usando `receta_ref` y luego carga ingredientes.
   - Se validan FK y unidades.

---

## Exportación (propuesta)
- Exporta **Inventario** con costo unitario real.
- Exporta **Recetas** existentes con `receta_id` + ingredientes actuales.
- Se agregan fórmulas de cálculo de costos para guía visual del usuario.

---

## UI en Admin (propuesta)
- Nuevo botón en Admin Override: **“Recetas masivas (Excel)”**.
- Vista similar a Inventario Inicial:
  - Descargar plantilla.
  - Subir archivo.
  - Previsualización + confirmación.

---

## Notas
- Las fórmulas en Excel son solo guía. El costo real siempre se calcula en backend.
- Si un producto tiene receta (`fabricacion_propia`), su costo unitario sale de esa receta automáticamente.

---

## Próximos pasos
1. Implementar exportador Excel (2 hojas + fórmulas).
2. Implementar importador + preview/resumen.
3. Agregar ruta y vista en Admin Override con botón nuevo.
