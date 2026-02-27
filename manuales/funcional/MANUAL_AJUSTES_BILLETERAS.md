# 📝 Manual de Ajustes de Billeteras

## Descripción

El módulo de **Ajustes de Billeteras** permite registrar ingresos y egresos manuales en las cuentas, útil para:
- Correcciones de saldo
- Ajustes iniciales
- Ingresos/egresos externos al sistema
- Comisiones bancarias
- Intereses bancarios

## Acceso

**Admin → Billeteras y Cuentas → Ajustes de Billeteras**

## Cómo Crear un Ajuste

### Paso 1: Crear el Ajuste

1. Click en **"Agregar Ajuste de Billetera"**
2. Completar los campos:
   - **Billetera**: Seleccionar la cuenta a ajustar
   - **Tipo**: 
     - `Ingreso` ⬆: Suma dinero a la cuenta
     - `Egreso` ⬇: Resta dinero de la cuenta
   - **Motivo**: Seleccionar el motivo del ajuste
     - Ajuste de Saldo Inicial
     - Corrección de Saldo
     - Ingreso Externo
     - Egreso Externo
     - Comisión Bancaria
     - Interés Bancario
     - Otro
   - **Monto**: Cantidad a ajustar (siempre positivo)
   - **Descripción**: Explicación detallada del ajuste

3. Click en **"Guardar"**

⚠️ **IMPORTANTE**: Al guardar, el ajuste queda en estado **"Pendiente"** y NO impacta aún en el saldo.

### Paso 2: Confirmar el Ajuste

1. Volver a la lista de **Ajustes de Billeteras**
2. Seleccionar el/los ajuste(s) pendiente(s) con el checkbox
3. En el menú de acciones, elegir **"✓ Confirmar ajustes seleccionados"**
4. Click en **"Ir"**

✅ El sistema:
- Crea automáticamente el MovimientoBilletera
- Actualiza el saldo de la cuenta
- Marca el ajuste como confirmado
- Registra fecha y usuario que confirmó
- No permite modificar ni eliminar el ajuste confirmado

## Estados de un Ajuste

| Estado | Icono | Descripción |
|--------|-------|-------------|
| **Pendiente** | ⏳ | Creado pero no confirmado. No impacta en saldos. |
| **Confirmado** | ✓ | Confirmado. Ya impactó en el saldo. No se puede modificar. |

## Validaciones

El sistema valida automáticamente:

✅ **Para Egresos**:
- Que haya saldo suficiente en la cuenta
- Si la configuración permite saldos negativos, se permite el egreso

✅ **Para Todos**:
- Que el monto sea mayor a 0
- Que la billetera esté activa
- No se puede confirmar un ajuste ya confirmado

## Ejemplos de Uso

### Ejemplo 1: Ajuste de Saldo Inicial
```
Situación: Al implementar el sistema, la cuenta bancaria tiene $50,000

1. Crear ajuste:
   - Billetera: Banco Santander
   - Tipo: Ingreso
   - Motivo: Ajuste de Saldo Inicial
   - Monto: 50000
   - Descripción: "Saldo al 01/01/2026 según extracto bancario"

2. Confirmar el ajuste
3. La cuenta ahora tiene $50,000
```

### Ejemplo 2: Comisión Bancaria
```
Situación: El banco cobró $250 de mantenimiento

1. Crear ajuste:
   - Billetera: Banco Santander
   - Tipo: Egreso
   - Motivo: Comisión Bancaria
   - Monto: 250
   - Descripción: "Comisión de mantenimiento - Enero 2026"

2. Confirmar el ajuste
3. Se descuentan $250 del saldo
```

### Ejemplo 3: Ingreso Externo
```
Situación: Se recibió un depósito externo al sistema

1. Crear ajuste:
   - Billetera: MercadoPago
   - Tipo: Ingreso
   - Motivo: Ingreso Externo
   - Monto: 15000
   - Descripción: "Depósito de socio - Aporte de capital"

2. Confirmar el ajuste
3. Se suman $15,000 al saldo
```

### Ejemplo 4: Corrección de Saldo
```
Situación: Se detectó un error en el registro de movimientos

1. Crear ajuste:
   - Billetera: Efectivo Principal
   - Tipo: Ingreso (o Egreso según corresponda)
   - Motivo: Corrección de Saldo
   - Monto: 500
   - Descripción: "Corrección por venta no registrada del 15/01/2026"

2. Confirmar el ajuste
3. El saldo se corrige
```

## Vistas en el Admin

### Lista de Ajustes
Muestra:
- Fecha de creación
- Billetera
- Tipo (Ingreso/Egreso) con color
- Motivo
- Monto con signo y color
- Estado (Pendiente/Confirmado)
- Usuario que confirmó
- Fecha de confirmación

### Filtros Disponibles
- Por estado (Confirmado/Pendiente)
- Por tipo (Ingreso/Egreso)
- Por motivo
- Por billetera
- Por fecha de creación

### Búsqueda
Permite buscar por:
- Descripción del ajuste
- Nombre de la billetera

## Integración con Movimientos

Cuando se confirma un ajuste:
- Se crea un `MovimientoBilletera` con origen **"AJUSTE"**
- La descripción incluye el motivo y la descripción del ajuste
- Se puede navegar desde el ajuste al movimiento y viceversa
- Aparece en el reporte de billeteras

## Permisos y Seguridad

- ✅ Solo usuarios con permisos de admin pueden crear ajustes
- ✅ Los ajustes confirmados NO se pueden modificar
- ✅ Los ajustes confirmados NO se pueden eliminar
- ✅ Se registra qué usuario confirmó cada ajuste
- ✅ Validación de saldo para prevenir errores

## Auditoría

Cada ajuste registra:
- 📅 Fecha de creación
- 👤 Usuario que confirmó
- 🕐 Fecha de confirmación
- 🔗 Vínculo al movimiento generado
- 📝 Descripción completa del motivo

## Recomendaciones

✅ **Usar descripciones claras**: Facilita la auditoría posterior
✅ **Confirmar solo cuando esté seguro**: No se puede deshacer
✅ **Revisar el saldo antes de confirmar egresos**: Evita errores
✅ **Usar el motivo correcto**: Mejora la trazabilidad
✅ **Documentar bien los ajustes iniciales**: Importante para contabilidad

---

**Implementado**: Enero 2026  
**Versión**: 1.0
