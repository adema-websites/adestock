# 📦 Módulo de Ajustes de Inventario

## 🎯 Propósito

El módulo de **Ajustes de Inventario** permite realizar correcciones y actualizaciones masivas del stock de productos sin necesidad de crear compras o ventas ficticias. Es ideal para:

- ✅ **Carga inicial de inventario** al comenzar a usar el sistema
- ✅ **Correcciones por conteo físico** cuando se detectan diferencias
- ✅ **Registro de mermas** por productos dañados o vencidos
- ✅ **Devoluciones** que requieren ajustar el stock
- ✅ **Importación masiva** de productos y stock desde Excel

---

## 🏗️ Estructura del Módulo

### 1. Tipos de Ajuste

El sistema incluye 5 tipos predefinidos:

| Tipo | Descripción | Uso típico | Comportamiento |
|------|-------------|-----------|----------------|
| **Inventario Inicial** | Carga inicial al comenzar | Primera vez que cargas productos | Crea Compra Virtual |
| **Corrección por Conteo** | Ajuste por diferencias físicas | Auditorías e inventarios | Crea Compra Virtual |
| **Merma/Producto Dañado** | Reducción por pérdidas | Productos vencidos o rotos | ⚠️ Crea Mermas (solo negativos) |
| **Devolución** | Aumento por devoluciones | Clientes que devuelven productos | Crea Compra Virtual |
| **Otro** | Otros ajustes diversos | Casos especiales | Crea Compra Virtual |

### 2. Estados de Ajuste

- **🔵 Borrador**: En edición, permite modificar
- **🟢 Aplicado**: Ya procesado, actualiza el stock definitivamente
- **🔴 Anulado**: Cancelado, sin efecto en el stock

---

## ⚠️ Tipo Especial: Merma/Producto Dañado

El tipo **"Merma/Producto Dañado"** tiene un comportamiento especial:

### Características:
- ✅ **Crea registros de Merma** en lugar de Compras Virtuales
- ✅ Las mermas quedan registradas en **Admin → Producto → Mermas**
- ⚠️ **SOLO acepta cantidades NEGATIVAS** (reducción de stock)
- ❌ **NO permite cantidades positivas** (aumentos)

### ¿Por qué este comportamiento?

Las mermas son específicamente para registrar **pérdidas de productos**:
- Productos vencidos
- Productos dañados
- Productos rotos o deteriorados
- Pérdidas por mal almacenamiento

Si necesitas **aumentar** el stock, usa otro tipo de ajuste:
- **Corrección por Conteo** para diferencias en inventarios
- **Devolución** para productos devueltos
- **Inventario Inicial** para cargas iniciales

### Validación Automática:

Si intentas agregar una cantidad positiva en un ajuste tipo MERMA:
```
❌ Error: Los ajustes de tipo 'Merma/Producto Dañado' solo pueden tener 
cantidades negativas (reducción de stock). Use otro tipo de ajuste 
para aumentar el stock.
```

### Ejemplo de Uso Correcto:

**Situación**: Se rompieron 10 botellas

1. Crear ajuste tipo **"Merma/Producto Dañado"**
2. Agregar producto: Coca Cola 2L
3. Cantidad ajuste: **-10** ✅ (cantidad negativa)
4. Motivo: "Rotura en depósito"
5. Aplicar ajuste → Se crea 1 registro de Merma con cantidad 10

**Incorrecto**:
- Cantidad ajuste: **+10** ❌ (rechazado por el sistema)

---

## 📋 Cómo Usar el Módulo

### Opción 1: Ajuste Manual (Pocos Productos)

1. Ir a **Admin → Producto → Ajustes de Inventario**
2. Clic en **"Agregar Ajuste de Inventario"**
3. Completar:
   - **Tipo**: Inventario Inicial
   - **Fecha**: Fecha del ajuste
   - **Depósito**: Depósito afectado
   - **Observaciones**: Motivo del ajuste
4. En la sección **"Detalle de ajuste"**, agregar productos:
   - Buscar el producto
   - El sistema muestra el **Stock Anterior** automáticamente
   - Ingresar **Cantidad de Ajuste**:
     - **Positivo** (+10): Aumenta el stock
     - **Negativo** (-5): Reduce el stock
   - El **Stock Nuevo** se calcula automáticamente
5. **Guardar**
6. Usar la acción **"Aplicar ajustes seleccionados"** para confirmar

### Opción 2: Importación Masiva desde Excel (Muchos Productos)

#### Paso 1: Crear el Ajuste en Borrador

1. Ir a **Admin → Producto → Ajustes de Inventario**
2. Crear un nuevo ajuste en **Borrador**
3. Seleccionar tipo **"Inventario Inicial"** y depósito
4. **Guardar** (sin productos aún)

#### Paso 2: Descargar Plantilla Excel

1. Abrir el ajuste recién creado
2. En la sección **"Importar/Exportar Excel"**, clic en:
   - **📥 Descargar Plantilla Excel**
3. Se descarga un archivo con:
   - Todos los productos del sistema
   - Stock actual de cada producto
   - Columna **"Cantidad Ajuste"** vacía

#### Paso 3: Completar la Plantilla

En Excel:
- **No modificar** las columnas: ID, Código, Nombre, etc.
- **Sólo editar** la columna **"Cantidad Ajuste"**:
  - **Valores positivos**: Agregar stock
    - Ejemplo: `+100` = aumentar 100 unidades
  - **Valores negativos**: Reducir stock
    - Ejemplo: `-20` = reducir 20 unidades
  - **Dejar en 0**: No ajustar ese producto
- Opcionalmente, agregar un **Motivo** específico

**Ejemplo:**

| ID | Código | Nombre | Stock Actual | Cantidad Ajuste | Motivo |
|----|--------|--------|--------------|-----------------|--------|
| 1 | 001 | Coca Cola 2L | 0.00 | 50 | Carga inicial |
| 2 | 002 | Sprite 1.5L | 0.00 | 30 | Carga inicial |
| 3 | 003 | Fanta 2L | 15.00 | -5 | Productos dañados |

#### Paso 4: Importar Detalles (Actualmente Manual)

⚠️ **Nota**: La importación automática desde Excel estará disponible en una versión futura.

Por ahora, debe cargar los productos manualmente desde el admin usando los datos del Excel.

#### Paso 5: Aplicar el Ajuste

1. Verificar que todos los productos estén correctos
2. Revisar el **"Resumen de Totales"** en el formulario
3. Seleccionar el ajuste
4. Ejecutar la acción **"Aplicar ajustes seleccionados"**
5. ✅ El stock se actualiza automáticamente

---

## 🔍 Detalles Técnicos

### ¿Cómo Afecta el Stock?

El sistema utiliza **dos mecanismos diferentes** según el tipo de ajuste:

#### Para tipos: Inventario Inicial, Corrección, Devolución, Otro

Cuando se **aplica** un ajuste:
1. Se crea una **Compra Virtual** con `compra_inicial=True`
2. La referencia a esta compra se guarda en el campo `compra_generada`
3. Se generan detalles de compra con `precio=0` (sin costo)
4. El stock se actualiza automáticamente vía la compra
5. Permite cantidades **positivas** (aumentos) y **negativas** (reducciones)
6. No afecta reportes de compras reales
7. Es auditable y trazable

Cuando se **anula** un ajuste:
1. Se elimina la compra virtual referenciada en `compra_generada`
2. El stock se revierte automáticamente (efecto cascada)
3. El campo `compra_generada` se vuelve null
4. El estado cambia a **ANULADO**
5. Se mantiene el registro para auditoría

#### Para tipo: Merma/Producto Dañado ⚠️

Cuando se **aplica** un ajuste de merma:
1. Se crean registros de **Merma** (uno por cada producto)
2. Las referencias se guardan en el campo `mermas_generadas`
3. Las mermas quedan visibles en **Admin → Producto → Mermas**
4. El stock se reduce automáticamente (las mermas se restan en el cálculo de stock)
5. **SOLO acepta cantidades negativas** (reducción de stock)
6. Las mermas tienen su propio sistema de auditoría
7. Se registra fecha, motivo, depósito y usuario

Cuando se **anula** un ajuste de merma:
1. Se eliminan todas las mermas referenciadas en `mermas_generadas`
2. El stock se revierte automáticamente
3. El campo `mermas_generadas` queda vacío
4. El estado cambia a **ANULADO**
5. Se mantiene el registro del ajuste para auditoría

### Validaciones

- ✅ No permite stock negativo final
- ✅ No permite modificar ajustes aplicados
- ✅ Calcula automáticamente el stock anterior
- ✅ Valida que haya al menos un producto
- ✅ Previene aplicar un ajuste dos veces
- ⚠️ **Ajustes tipo MERMA solo aceptan cantidades negativas**
- ✅ No permite cantidades de ajuste = 0

### Permisos

Los ajustes quedan registrados con:
- **Usuario** que lo creó
- **Fecha de creación**
- **Fecha de aplicación**

---

## 📊 Reportes y Auditoría

### Ver Ajustes Aplicados

1. Ir a **Admin → Producto → Ajustes de Inventario**
2. Filtrar por **Estado = Aplicado**
3. Ver fecha, usuario, depósito y productos afectados

### Exportar Ajuste a Excel

1. Abrir un ajuste aplicado
2. Clic en **📤 Exportar Ajuste Actual**
3. Se descarga un Excel con todos los detalles

### Trazabilidad

- Cada ajuste genera una compra con `compra_inicial=True`
- Se puede ver en **Admin → Compra → Compras**
- Filtrar por `compra_inicial=True` para ver ajustes

---

## 🚀 Casos de Uso Comunes

### Caso 1: Primera Carga de Inventario

**Situación**: Cliente nuevo que empieza a usar el sistema

1. Crear ajuste tipo **"Inventario Inicial"**
2. Descargar plantilla Excel
3. Completar columna "Cantidad Ajuste" con el stock real
4. Importar (actualmente manual, pronto automático)
5. Aplicar ajuste
6. ✅ Sistema listo con stock inicial

### Caso 2: Corrección por Inventario Físico

**Situación**: Se hizo un conteo y hay diferencias

1. Crear ajuste tipo **"Corrección por Conteo"**
2. Descargar plantilla (muestra el stock del sistema)
3. Comparar con conteo físico
4. Agregar ajustes positivos o negativos según diferencias
5. Aplicar ajuste
6. ✅ Stock corregido

### Caso 3: Productos Dañados ⚠️

**Situación**: Se rompieron 10 botellas de gaseosa

1. Crear ajuste tipo **"Merma/Producto Dañado"**
2. Agregar manualmente el producto (Coca Cola 2L)
3. Ingresar cantidad ajuste: **`-10`** (negativo obligatorio)
4. Motivo: "Rotura en depósito"
5. Aplicar ajuste
6. ✅ Se crea 1 registro de **Merma** con cantidad 10
7. ✅ El stock se reduce automáticamente en 10 unidades
8. ✅ La merma queda registrada en **Admin → Producto → Mermas**

**Importante**: 
- Si intentas poner cantidad positiva (+10), el sistema lo rechazará
- Las mermas se pueden ver y auditar en su propia sección del admin
- Al anular, se elimina la merma y el stock se restaura

---

## ↩️ Anulación de Ajustes

### ¿Cuándo Anular un Ajuste?

Un ajuste aplicado puede ser anulado en los siguientes casos:
- Se aplicó por error
- Los datos eran incorrectos
- Se necesita revertir el cambio en el inventario
- Se detectó un error después de aplicar

⚠️ **Importante**: La anulación **revierte completamente** los cambios en el stock.

### Cómo Anular un Ajuste

1. Ir a **Admin → Producto → Ajustes de Inventario**
2. Filtrar por **Estado = Aplicado**
3. Seleccionar el ajuste que desea anular
4. Ejecutar la acción **"Anular ajustes seleccionados"**
5. ✅ El sistema automáticamente:
   - Elimina la compra virtual asociada
   - Revierte todos los cambios en el stock
   - Marca el ajuste como **ANULADO**

### ¿Qué Sucede al Anular?

**Antes de anular:**
```
Producto X: Stock = 100 unidades
Ajuste aplicado: +50 unidades
Stock después del ajuste: 150 unidades
```

**Después de anular:**
```
Ajuste anulado
Compra virtual eliminada
Stock restaurado: 100 unidades ✅
```

### Restricciones

- ❌ No se puede anular un ajuste en **BORRADOR** (usar Eliminar)
- ❌ No se puede anular un ajuste ya **ANULADO**
- ✅ Solo se pueden anular ajustes **APLICADOS**

### Trazabilidad

El sistema mantiene registro completo:
- **compra_generada**: Referencia a la compra virtual (null después de anular)
- **fecha_aplicacion**: Fecha original de aplicación
- **estado**: Cambia a ANULADO
- **observaciones**: Se mantienen para auditoría

### Campos de Trazabilidad

En la sección **"Información del Sistema"** del admin, se pueden ver:

**Compra Generada** (para tipos: Inicial, Corrección, Devolución, Otro):
- Link a la compra virtual creada (mientras esté aplicado)
- Este campo se vuelve vacío después de anular
- Permite verificar qué compra se creó para el ajuste

**Mermas Generadas** (para tipo: Merma/Producto Dañado):
- Links a las mermas creadas (mientras esté aplicado)
- Este campo se vuelve vacío después de anular
- Permite acceder directamente a los registros de merma
- Las mermas también quedan en **Admin → Producto → Mermas**

---

## ⚡ Consejos y Mejores Prácticas

### ✅ Recomendaciones

- **Siempre usar tipo de ajuste correcto** para reportes claros
- **Usar tipo MERMA solo para pérdidas** (productos dañados, vencidos, rotos)
- **Agregar observaciones detalladas** para auditorías
- **Revisar el resumen** antes de aplicar
- **No aplicar dos veces** el mismo ajuste
- **Hacer backup** antes de ajustes masivos

### ❌ Evitar

- No usar para registrar compras reales (usar módulo Compras)
- No usar para registrar ventas (usar módulo Ventas)
- No aplicar sin revisar el resumen de totales
- No modificar productos una vez aplicado (crear otro ajuste)

---

## 🔮 Futuras Mejoras

### En Desarrollo

- ✨ **Importación automática desde Excel** (próximamente)
- ✨ **Validación de rangos** en Excel antes de importar
- ✨ **Historial de cambios** por producto
- ✨ **Reportes de ajustes** con gráficos
- ✨ **Notificaciones** al aplicar ajustes grandes

---

## 🆘 Soporte

Si tienes dudas o problemas:
1. Revisa esta documentación
2. Verifica los logs del sistema
3. Contacta al administrador del sistema

---

## 📅 Versión

- **Versión**: 1.2.0
- **Fecha**: Febrero 2026
- **Autor**: Sistema AdeStock
- **Última actualización**: 23/02/2026

### Changelog

**v1.2.0** (23/02/2026)
- ✅ **Nuevo**: Ajustes tipo MERMA ahora crean registros de Merma en lugar de Compras
- ✅ **Validación**: Tipo MERMA solo acepta cantidades negativas
- ✅ Agregado campo `mermas_generadas` para trazabilidad de mermas
- ✅ Las mermas quedan registradas en Admin → Producto → Mermas
- ✅ Anulación de ajustes tipo MERMA elimina las mermas automáticamente
- ✅ Mejor auditoría y separación entre ajustes normales y mermas

**v1.1.0** (23/02/2026)
- ✅ Agregado sistema de anulación completa de ajustes
- ✅ Agregado campo `compra_generada` para trazabilidad
- ✅ La anulación ahora revierte cambios en inventario automáticamente
- ✅ Eliminación de validación de stock negativo para correcciones
- ✅ Corrección de TypeError en cálculos Decimal/float

**v1.0.0** (Inicial)
- ✅ Creación del módulo de ajustes
- ✅ Importación/exportación Excel
- ✅ Tipos de ajuste predefinidos
- ✅ Estados: Borrador, Aplicado, Anulado
