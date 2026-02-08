# 📋 Nueva Hoja: Productos_Receta

## ✅ Implementación Completada

Se ha agregado exitosamente una **tercera hoja "Productos_Receta"** al Excel de recetas masivas, permitiendo crear y gestionar ingredientes de recetas de forma más clara y masiva.

---

## 📊 Estructura del Excel Actualizado

### **Hoja 1: Inventario** (Referencia)
- Contiene todos los productos disponibles
- Sirve como fuente de datos para las validaciones
- Incluye: ID, código, nombre, unidad, cantidad, costo

### **Hoja 2: Recetas**
- Crear/actualizar recetas masivamente
- Sección superior: Datos de recetas (nombre, porciones, categoría, etc.)
- Sección inferior: Ingredientes (OPCIONAL - ahora puedes usar la Hoja 3)

### **Hoja 3: Productos_Receta** ⭐ NUEVA
- **Dedicada exclusivamente** a crear ingredientes masivamente
- Más clara y fácil de usar que la sección de ingredientes en Hoja 2
- Permite vincular productos a recetas de forma masiva

---

## 🎯 Columnas de la Hoja "Productos_Receta"

| Columna | Descripción | Tipo | Ejemplo |
|---------|-------------|------|---------|
| **receta_ref** | Referencia temporal de receta | Texto | `REC001` |
| **receta_id** | ID de receta existente | Número (validación) | `15` |
| **producto_id** | ID del producto/insumo | Número (validación) | `234` |
| **producto_nombre** | Nombre del producto | Texto (validación) | `Harina 000` |
| **cantidad** | Cantidad a usar | Número | `250` |
| **unidad_medida** | Unidad de medida | Lista (validación) | `Gramos` |
| **costo_unitario** | Costo por unidad | Fórmula automática | `0.05` |
| **subtotal** | Costo total ingrediente | Fórmula automática | `12.50` |

---

## 🚀 Cómo Usar la Nueva Hoja

### **Opción A: Crear recetas nuevas**

1. **En Hoja "Recetas"**: Crear las recetas con `receta_ref` (ejemplo: `REC001`, `REC002`)
2. **En Hoja "Productos_Receta"**: 
   - Usar la misma `receta_ref` para vincular ingredientes
   - Seleccionar productos de la lista desplegable
   - Ingresar cantidades
   - Seleccionar unidades de medida

**Ejemplo:**

| receta_ref | producto_id | producto_nombre | cantidad | unidad_medida |
|------------|-------------|-----------------|----------|---------------|
| REC001 | 45 | Harina 000 | 500 | Gramos |
| REC001 | 78 | Azúcar | 200 | Gramos |
| REC001 | 12 | Huevos | 3 | Unidades |
| REC002 | 45 | Harina 000 | 300 | Gramos |

### **Opción B: Agregar ingredientes a recetas existentes**

1. **En Hoja "Productos_Receta"**: 
   - Colocar el `receta_id` de la receta existente
   - Seleccionar productos
   - Ingresar cantidades y unidades

**Ejemplo:**

| receta_id | producto_id | cantidad | unidad_medida |
|-----------|-------------|----------|---------------|
| 15 | 89 | 250 | Gramos |
| 15 | 102 | 1 | Litros |

---

## 🎨 Características Implementadas

### ✅ **Validaciones de Datos**
- **Listas desplegables** para:
  - `receta_id`: Solo IDs de recetas existentes
  - `producto_id`: Solo IDs de productos en inventario
  - `producto_nombre`: Solo nombres de productos existentes
  - `unidad_medida`: Solo unidades válidas (Kilos, Gramos, Litros, etc.)

### ✅ **Fórmulas Automáticas**
- **`costo_unitario`**: Busca automáticamente el costo desde el Inventario
- **`subtotal`**: Calcula el costo total considerando:
  - Conversiones Kilos ↔ Gramos
  - Conversiones Litros ↔ Mililitros
  - Validación de unidades compatibles

### ✅ **Diseño Profesional**
- Logo de la empresa
- Títulos con color verde Adema (#27ae60)
- Tabla con formato y bordes
- Columnas ajustadas automáticamente

---

## 📥 Proceso de Importación

Al importar el Excel, el sistema:

1. **Lee la Hoja "Recetas"** → Crea/actualiza recetas
2. **Lee los ingredientes en Hoja "Recetas"** → Los procesa (OPCIONAL)
3. **Lee la Hoja "Productos_Receta"** → Procesa ingredientes adicionales
4. **Valida compatibilidad** de unidades de medida
5. **Crea los registros** en la base de datos

### **Reglas de Validación:**

✅ **Producto con unidad "Kilos"** → Solo acepta: `Kilos`, `Gramos`
✅ **Producto con unidad "Litros"** → Solo acepta: `Litros`, `Mililitros`
✅ **Producto con unidad "Unidades"** → Solo acepta: `Unidades`
✅ **Producto con unidad "Mt2s"** → Solo acepta: `Mt2s`

---

## 💡 Ventajas de la Nueva Hoja

| Ventaja | Descripción |
|---------|-------------|
| 🎯 **Claridad** | Hoja dedicada exclusivamente a productos-receta |
| ⚡ **Rapidez** | Carga masiva de ingredientes sin mezclar con otras secciones |
| 📊 **Organización** | Separación clara entre recetas e ingredientes |
| 🔍 **Facilidad** | Listas desplegables para evitar errores |
| 🧮 **Automatización** | Fórmulas automáticas para costos y subtotales |

---

## 📝 Ejemplo Completo de Uso

### **Paso 1: Descargar plantilla**
```python
# En Django Admin o vista personalizada
wb = build_recetas_template(include_data=True)
wb.save("recetas_plantilla.xlsx")
```

### **Paso 2: Completar Excel**

**Hoja "Recetas":**
| receta_ref | nombre | porciones | categoria |
|------------|--------|-----------|-----------|
| REC001 | Pan Casero | 10 | Panadería |
| REC002 | Torta Chocolate | 8 | Repostería |

**Hoja "Productos_Receta":**
| receta_ref | producto_nombre | cantidad | unidad_medida |
|------------|-----------------|----------|---------------|
| REC001 | Harina 000 | 1000 | Gramos |
| REC001 | Levadura | 25 | Gramos |
| REC001 | Sal | 15 | Gramos |
| REC002 | Harina 0000 | 500 | Gramos |
| REC002 | Cacao | 100 | Gramos |

### **Paso 3: Importar**
```python
from cocina.recetas_excel import import_recetas_excel

creadas, actualizadas, ingredientes, errores = import_recetas_excel(archivo)
print(f"Recetas creadas: {creadas}")
print(f"Ingredientes: {ingredientes}")
```

---

## 🔧 Archivos Modificados

- ✅ `cocina/recetas_excel.py`
  - Función `build_recetas_template()` → Agrega hoja "Productos_Receta"
  - Función `import_recetas_excel()` → Lee e importa desde la nueva hoja

---

## 🎉 Resultado Final

El usuario ahora puede:

✅ Descargar un Excel con **3 hojas** (Inventario, Recetas, Productos_Receta)
✅ Crear recetas masivamente en la Hoja "Recetas"
✅ Asignar ingredientes masivamente en la Hoja "Productos_Receta"
✅ Usar listas desplegables para evitar errores
✅ Ver costos calculados automáticamente
✅ Importar TODO en una sola operación

---

## 📞 Soporte

Si necesitas modificaciones adicionales:
- Cambiar validaciones
- Agregar más columnas
- Personalizar fórmulas
- Ajustar el diseño

¡La estructura está lista para extenderse fácilmente! 🚀
