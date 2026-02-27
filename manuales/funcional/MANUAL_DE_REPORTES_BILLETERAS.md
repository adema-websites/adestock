# 📊 Manual de Reportes de Billeteras y Cuentas

## Descripción General

Este módulo permite visualizar y auditar todos los movimientos financieros de las billeteras/cuentas del sistema, proporcionando un control completo sobre el flujo de efectivo y movimientos bancarios.

## Acceso al Reporte

### Desde el Dashboard:
1. Ingresa al panel de administración
2. En la sección de accesos rápidos, haz clic en **"Reportes de Cuentas"** 💳

### URL Directa:
`/admin/reportes-billeteras/`

## Características Principales

### 🔍 Filtros Disponibles

1. **Rango de Fechas**: 
   - Fecha Desde / Fecha Hasta
   - Por defecto muestra el mes actual

2. **Billetera/Cuenta**:
   - Todas las billeteras (opción por defecto)
   - Seleccionar una billetera específica

3. **Tipo de Movimiento**:
   - Todos
   - Solo Ingresos
   - Solo Egresos

4. **Origen del Movimiento**:
   - Venta
   - Compra
   - Gasto
   - Retiro de Caja
   - Cobro de Deuda
   - Pago a Proveedor
   - Transferencia Entrada/Salida
   - Ajuste Manual

### 📊 Información Mostrada

#### Resumen Ejecutivo:
- **Saldo Total Inicio**: Suma de saldos de todas las cuentas al inicio del período
- **Total Ingresos**: Suma de todos los ingresos del período
- **Total Egresos**: Suma de todos los egresos del período
- **Movimiento Neto**: Diferencia entre ingresos y egresos
- **Saldo Total Final**: Saldo resultante al final del período

#### Resumen por Billetera:
Tabla detallada con:
- Nombre de la billetera
- Tipo (Banco, MercadoPago, Efectivo, etc.)
- Saldo al inicio del período
- Total de ingresos
- Total de egresos
- Movimiento neto
- Saldo final
- Cantidad de movimientos

#### Análisis por Tipo de Origen:
Cards con estadísticas agrupadas por:
- Ingresos por origen
- Egresos por origen
- Movimiento neto
- Cantidad de transacciones

#### Detalle de Movimientos:
Tabla con los últimos 200 movimientos mostrando:
- Fecha y hora
- Billetera
- Tipo (Ingreso/Egreso)
- Origen
- Monto
- Saldo anterior
- Saldo nuevo
- Descripción

### 📄 Exportación a PDF

El botón **"Exportar PDF"** genera un reporte profesional que incluye:

1. **Header con información de la empresa**
   - Logo y datos de configuración
   - Período del reporte
   - Filtros aplicados

2. **Resumen Ejecutivo por Billetera**
   - Tabla completa con todas las billeteras
   - Totales generales
   - Colores diferenciados

3. **Estadísticas por Origen**
   - Tabla agrupada por tipo de movimiento
   - Subtotales por cada origen

4. **Detalle de Movimientos**
   - Últimos 50 movimientos (en PDF)
   - Información completa de cada transacción

### 🎯 Casos de Uso

#### Control de Flujo de Caja:
```
1. Seleccionar período mensual
2. Ver resumen de todas las cuentas
3. Identificar ingresos y egresos principales
4. Exportar PDF para archivo
```

#### Auditoría de Cuenta Específica:
```
1. Filtrar por billetera específica
2. Seleccionar rango de fechas
3. Revisar todos los movimientos
4. Verificar orígenes y montos
```

#### Análisis de Ventas/Compras:
```
1. Filtrar por origen "Venta" o "Compra"
2. Ver solo ingresos o solo egresos
3. Analizar montos por período
4. Exportar reporte
```

#### Reconciliación Bancaria:
```
1. Seleccionar cuenta bancaria específica
2. Comparar saldo inicial vs final
3. Revisar detalle de movimientos
4. Contrastar con extracto bancario
```

## Integración con el Sistema

### Movimientos Automáticos:
Los movimientos se registran automáticamente cuando ocurren:

- ✅ **Ventas**: Ingreso en la billetera seleccionada
- ✅ **Compras**: Egreso en la cuenta de pago
- ✅ **Gastos**: Egreso de caja o cuenta
- ✅ **Retiros de Caja**: Egreso registrado
- ✅ **Cobros de Deuda**: Ingreso en cuenta
- ✅ **Pagos a Proveedores**: Egreso en cuenta
- ✅ **Transferencias**: Egreso en origen, ingreso en destino

### Trazabilidad:
Cada movimiento mantiene referencia al registro que lo originó, permitiendo navegar desde el reporte al documento fuente.

## Ventajas del Sistema

✅ **Visibilidad Completa**: Todos los movimientos en un solo lugar
✅ **Filtros Potentes**: Búsqueda precisa por múltiples criterios
✅ **Análisis Automático**: Cálculos y totales en tiempo real
✅ **Exportación Profesional**: PDFs listos para auditoría
✅ **Trazabilidad Total**: Cada movimiento vinculado a su origen
✅ **Múltiples Cuentas**: Control unificado de todas las billeteras

## Notas Importantes

⚠️ **Rendimiento**: La vista muestra hasta 200 movimientos. Para consultas mayores, use filtros o exporte a PDF.

⚠️ **Saldos**: Los saldos se calculan en tiempo real basándose en el saldo inicial + movimientos.

⚠️ **Permisos**: Solo usuarios con permisos de superusuario pueden acceder a estos reportes.

⚠️ **Actualización**: Los datos se actualizan automáticamente con cada nueva transacción.

## Soporte

Para dudas o problemas con el reporte de billeteras, contactar al administrador del sistema.

---

**Fecha de Implementación**: Enero 2026  
**Versión**: 1.0
