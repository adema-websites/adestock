# 💳 MANUAL DE BILLETERAS Y CUENTAS

## 📋 Descripción General

El módulo de **Billeteras y Cuentas** permite llevar un registro completo y automático de todos los movimientos de dinero de la empresa en sus diferentes cuentas bancarias, billeteras digitales y fondos de efectivo.

---

## ✨ Características Principales

### 🔄 **Registro Automático**
- Todos los movimientos se registran **automáticamente** al realizar operaciones
- No requiere doble carga de datos
- Se vincula con medios de pago y compra existentes

### 💰 **Control de Saldo**
- Saldo actualizado en tiempo real
- Validación de saldo disponible antes de transferencias/egresos
- Opción configurable para permitir o no saldos negativos

### 📊 **Trazabilidad Completa**
- Cada movimiento está vinculado al registro que lo originó
- Historial completo de movimientos
- Saldos anteriores y nuevos en cada operación

---

## 🚀 Configuración Inicial

### **1. Configurar el Sistema**

Ve a **Agenda → Configuración** y ajusta:

- **"Permitir saldo negativo en billeteras"**: 
  - ✅ **Activado**: Permite realizar transferencias y egresos sin validar saldo
  - ❌ **Desactivado**: Valida que haya saldo suficiente antes de cada egreso

> 💡 **Recomendación**: Mantenerlo desactivado para control estricto de caja

---

### **2. Crear Billeteras**

Ve a **Billeteras y Cuentas → Billeteras/Cuenta** y crea tus cuentas:

**Ejemplo:**
- **Nombre**: Banco Santander - Cuenta Corriente 1234
- **Tipo**: Cuenta Bancaria
- **Número de cuenta**: 1234567890123456789012
- **Titular**: Empresa ADEMA SRL
- **Banco**: Banco Santander
- **Saldo inicial**: $50,000.00 (el saldo con el que empieza esta cuenta)
- **Activa**: ✅ Sí

**Tipos disponibles:**
- 🏦 Cuenta Bancaria
- 💵 Efectivo
- 📱 MercadoPago
- 💳 PayPal
- ₿ Criptomonedas
- 📦 Otro

---

### **3. Asociar Medios de Pago/Compra**

Ve a **Agenda → Medios de pago** o **Medios de compra**:

**Para cada medio, asigna la billetera correspondiente:**

| Medio de Pago | Billetera Asociada |
|---------------|-------------------|
| Efectivo | Caja Efectivo |
| MercadoPago | Cuenta MercadoPago Principal |
| Transferencia Banco | Banco Santander Cta. 1234 |
| Débito/Crédito | Cuenta Terminal POS |

> ⚠️ **Importante**: Solo se registran movimientos para medios que **NO sean cuenta corriente** (las cuentas corrientes no mueven dinero real hasta que se cobran/pagan)

---

## 📖 Uso del Sistema

### **Flujo Automático de Registro**

#### **1. VENTA** 
```
Cliente paga con MercadoPago → $5,000
```
✅ Se crea automáticamente:
- **MovimientoBilletera**
  - Billetera: Cuenta MercadoPago Principal
  - Tipo: INGRESO (+)
  - Monto: $5,000
  - Origen: Venta #12345

#### **2. COMPRA**
```
Pago a proveedor con Transferencia → $15,000
```
✅ Se crea automáticamente:
- **MovimientoBilletera**
  - Billetera: Banco Santander Cta. 1234
  - Tipo: EGRESO (-)
  - Monto: $15,000
  - Origen: Compra #789

#### **3. GASTO**
```
Gasto de servicios pagado en efectivo → $2,500
```
✅ Se crea automáticamente:
- **MovimientoBilletera**
  - Billetera: Caja Efectivo
  - Tipo: EGRESO (-)
  - Monto: $2,500
  - Origen: Gasto - Servicios

#### **4. RETIRO DE CAJA**
```
Retiro para banco → $10,000
```
✅ Se crea automáticamente:
- **MovimientoBilletera**
  - Billetera: (según medio seleccionado)
  - Tipo: EGRESO (-)
  - Monto: $10,000
  - Origen: Retiro de Caja

#### **5. COBRO DE DEUDA**
```
Cliente paga deuda en efectivo → $3,000
```
✅ Se crea automáticamente:
- **MovimientoBilletera**
  - Billetera: Caja Efectivo
  - Tipo: INGRESO (+)
  - Monto: $3,000
  - Origen: Cobro de Deuda

---

## 🔄 Transferencias Entre Billeteras

### **Cómo hacer una transferencia:**

1. Ve a **Billeteras y Cuentas → Transferencias entre Billeteras**
2. Haz clic en **"Agregar transferencia"**
3. Completa los datos:
   - **Billetera origen**: Caja Efectivo
   - **Billetera destino**: Banco Santander Cta. 1234
   - **Monto**: $20,000
   - **Concepto**: Depósito diario
4. Guarda la transferencia (queda PENDIENTE)
5. Para confirmarla:
   - **Opción A**: Selecciona la transferencia → Acciones → "Confirmar transferencias seleccionadas"
   - **Opción B**: Entra a editar la transferencia y márcala como confirmada

### **¿Qué pasa al confirmar?**

✅ Se crean automáticamente DOS movimientos:

1. **Egreso en origen** (Caja Efectivo)
   - Tipo: EGRESO (-)
   - Monto: $20,000
   - Origen: TRANSFERENCIA_SALIDA

2. **Ingreso en destino** (Banco Santander)
   - Tipo: INGRESO (+)
   - Monto: $20,000
   - Origen: TRANSFERENCIA_ENTRADA

> ⚠️ **Validación**: Si tienes desactivado "Permitir saldo negativo", el sistema validará que la billetera origen tenga saldo suficiente antes de confirmar.

---

## 📊 Consultas y Reportes

### **Ver Saldo de una Billetera**

1. Ve a **Billeteras y Cuentas → Billeteras/Cuenta**
2. Selecciona la billetera que quieres ver
3. En la parte inferior verás:
   - 💵 Saldo Inicial
   - ✅ Total Ingresos
   - ❌ Total Egresos
   - **💰 Saldo Actual** (calculado automáticamente)

### **Ver Movimientos**

1. Ve a **Billeteras y Cuentas → Movimientos de Billeteras**
2. Filtra por:
   - Billetera
   - Tipo (Ingreso/Egreso)
   - Origen (Venta, Compra, Gasto, etc.)
   - Fecha

3. Cada movimiento muestra:
   - ⬆️ Ingreso (verde) / ⬇️ Egreso (rojo)
   - Monto con signo
   - Saldo anterior y nuevo
   - Descripción
   - Vínculo al registro origen

---

## 🎯 Casos de Uso Comunes

### **1. Control Diario de Efectivo**

**Billetera**: "Caja Efectivo Principal"

**Al final del día:**
1. Consulta el saldo actual
2. Compara con el efectivo físico
3. Si difiere, investiga los movimientos del día
4. Puedes filtrar por fecha para ver solo movimientos de hoy

---

### **2. Conciliación Bancaria**

**Billetera**: "Banco Santander Cta. 1234"

**Al recibir el resumen bancario:**
1. Compara el saldo del sistema con el saldo del banco
2. Revisa los movimientos registrados
3. Identifica diferencias (comisiones, intereses no registrados)
4. Puedes crear ajustes manuales si es necesario

---

### **3. Control de MercadoPago/Billeteras Digitales**

**Billetera**: "MercadoPago Principal"

**Para control:**
1. Cada venta con MercadoPago se registra automáticamente
2. Puedes ver exactamente cuánto dinero tienes en MP
3. Cuando retires a banco, registra una transferencia:
   - Origen: MercadoPago Principal
   - Destino: Banco Santander
   - Monto: Lo que retires

---

## ⚙️ Configuraciones Avanzadas

### **Permitir Saldo Negativo**

**Cuándo activarlo:**
- Si usas sobregiros bancarios
- Si quieres registrar primero y controlar después
- Para movimientos de ajuste/corrección

**Cuándo desactivarlo:**
- Para control estricto de caja
- Para evitar errores de registro
- En billeteras de efectivo (no puede haber negativo físicamente)

---

### **Billeteras Inactivas**

Si una cuenta se cierra o ya no se usa:
1. Edita la billetera
2. Desmarca "Cuenta activa"
3. La billetera seguirá existiendo con su historial
4. No podrás usarla en nuevas operaciones

---

## 🔍 Preguntas Frecuentes

### **¿Puedo editar un movimiento?**
❌ No. Los movimientos se crean automáticamente y son de solo lectura para mantener la integridad del sistema.

### **¿Qué pasa si borro una venta/compra?**
Los movimientos quedan registrados. El sistema no elimina movimientos automáticamente para mantener trazabilidad.

### **¿Puedo tener varias billeteras del mismo tipo?**
✅ Sí. Puedes tener múltiples cuentas bancarias, cajas de efectivo, etc.

### **¿Cómo corrijo un error en el saldo?**
Puedes ajustar el "Saldo inicial" de la billetera si recién estás comenzando. Si ya tiene movimientos, ese campo se bloquea para evitar inconsistencias.

### **¿Se puede exportar los movimientos?**
Sí, desde la lista de movimientos puedes usar las funciones de exportación del admin de Django.

---

## 🎓 Ejemplo Completo de Flujo Diario

**Inicio del día:**
- Caja Efectivo: $10,000

**Operaciones:**
1. Venta #1 - Efectivo: $3,500 → Caja Efectivo: $13,500
2. Venta #2 - MercadoPago: $2,000 → MercadoPago: $2,000
3. Compra a proveedor - Transferencia: $8,000 → Banco: -$8,000
4. Gasto luz - Efectivo: $1,200 → Caja Efectivo: $12,300
5. Retiro de caja para banco - Efectivo: $10,000 → Caja Efectivo: $2,300

**Transferencia:**
6. Depósito en banco del retiro: 
   - Origen: Retiros (virtual)
   - Destino: Banco Santander
   - Monto: $10,000

**Fin del día:**
- Caja Efectivo: $2,300
- MercadoPago: $2,000
- Banco Santander: $2,000 ($10,000 dep - $8,000 compra)

---

## 📞 Soporte

Si tienes dudas o encuentras algún problema, revisa:
1. Este manual
2. Los mensajes de validación del sistema
3. El historial de movimientos

El sistema está diseñado para ser **automático y confiable**. ¡Disfruta del control total de tus cuentas! 💪
