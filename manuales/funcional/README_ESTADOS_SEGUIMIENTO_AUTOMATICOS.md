# Estados de Seguimiento con Generación Automática

## 🎯 Descripción General

El sistema **ADESTOCK** ahora cuenta con **Estados de Seguimiento** inteligentes que pueden **generar automáticamente** procesos de **Armado de Pedidos** y **Fabricación** cuando una venta avanza por diferentes etapas del flujo operativo.

Esta funcionalidad permite automatizar la creación de tareas de producción y picking basándose en el estado actual del pedido, optimizando el flujo de trabajo sin intervención manual.

---

## 🏗️ Arquitectura del Sistema

### Modelos Principales

1. **`EstadoSeguimiento`** - Define los estados personalizables del flujo
2. **`Venta`** - Pedidos de los clientes con estado de seguimiento asignado  
3. **`ArmadoPedido`** - Proceso de picking/armado generado automáticamente
4. **`Fabricacion`** - Proceso de producción generado automáticamente

### Flujo de Datos
```
Venta → EstadoSeguimiento → [Generar Armado/Fabricación] → Procesos automáticos
```

---

## ⚙️ Configuración de Estados de Seguimiento

### Acceso al Administrador
1. Ir al **Admin de Django**
2. Buscar **"Estado de Seguimiento"** en la sección **VENTA**
3. Crear o editar estados según el flujo operativo

### Campos de Configuración

| Campo | Descripción | Ejemplo |
|-------|-------------|---------|
| **Nombre** | Nombre descriptivo del estado | "En Cocina", "Listo para Retirar" |
| **Orden** | Secuencia numérica del flujo (menor = primero) | 1, 2, 3, 4... |
| **Color** | Color hexadecimal para identificación visual | #28a745 (verde), #ffc107 (amarillo) |
| **Es Final** | Marca si es el último estado del flujo | ✅ Solo el estado final |
| **Generar Armado de Pedido** | ✅ Crea automáticamente armado al entrar | Estados de picking |
| **Generar Fabricación** | ✅ Crea automáticamente fabricación al entrar | Estados de producción |
| **Activo** | Estado habilitado para usar | ✅ Siempre activado |

---

## 🛠️ Configuración Recomendada

### Ejemplo de Flujo Completo

| Orden | Estado | Generar Armado | Generar Fabricación | Es Final |
|-------|--------|----------------|---------------------|----------|
| **0** | Pendiente | ❌ | ❌ | ❌ |
| **1** | Fabricando los insumos | ❌ | ✅ | ❌ |
| **2** | Armando el pedido | ✅ | ❌ | ❌ |
| **3** | Listo para entregar | ❌ | ❌ | ✅ |

### Colores Sugeridos
- **Pendiente**: `#fba94b` (Naranja) 
- **Fabricando**: `#78cea2` (Verde claro)
- **Armando**: `#976bff` (Morado)  
- **Listo**: `#28a745` (Verde)

---

## 🔄 Flujo Operativo

### 1. Creación de Pedido
```
Cliente realiza pedido → Venta creada → Estado: "Pendiente"
```

### 2. Avance Manual desde Admin
  
**Paso 1: Ir a Admin → Ventas**
- Buscar la venta deseada
- Ver columna **"Seg."** con estado actual
- Hacer clic en botón **"Avanzar"**

**Paso 2: "Pendiente" → "Fabricando los insumos"**
```
✅ Se generan automáticamente:
   - Fabricaciones para productos con receta
   - Lote: "VENTA-{id_venta}"
   - Estado inicial de fabricación  
   - Cantidades calculadas (cantidad × pack)
```

**Paso 3: "Fabricando" → "Armando el pedido"**
```
✅ Se genera automáticamente:
   - ArmadoPedido vinculado a la venta
   - ArmadoPedidoItems para cada producto  
   - Código: ARM-000XXX
   - Estado inicial de armado
```

**Paso 4: "Armando" → "Listo para entregar"**
```
Estado final - No genera nuevos procesos
```

---

## 🎮 Cómo Usar el Sistema

### Requisitos Previos
1. ✅ **Venta finalizada** (estado = FINALIZADA)
2. ✅ **Estados de seguimiento configurados** 
3. ✅ **Estados de armado** creados en el sistema
4. ✅ **Estados de fabricación** creados en el sistema

### Proceso Paso a Paso

#### 1️⃣ Configurar Estados
```bash
# Ir al Admin → Estado de Seguimiento
# Crear estados con la configuración deseada
# Asignar orden secuencial (0, 1, 2, 3...)
# Marcar checkboxes según necesidad:
#   - Generar Armado de Pedido  
#   - Generar Fabricación
```

#### 2️⃣ Procesar Pedidos
```bash
# Admin → Ventas → Buscar venta
# Columna "Seg." muestra estado actual
# Botón "Avanzar" lleva al siguiente estado
# Mensajes informativos confirman lo generado
```

#### 3️⃣ Monitorear Procesos
```bash
# Admin → Armado de Pedidos (ver pickings creados)
# Admin → Fabricación (ver producciones creadas)
# Columnas "Armado / Fab." en vista de Ventas
```

---

## 🔧 Detalles Técnicos

### Generación de Fabricación

**Condiciones:**
- Venta debe estar **FINALIZADA** 
- Estado de seguimiento con `generar_fabricacion = True`
- Productos deben tener **receta asociada** (`fabricacion_propia`)

**Proceso:**
1. Busca productos con receta en los detalles de venta
2. Calcula cantidad: `cantidad_venta × cantidad_pack`  
3. Determina depósito (de la venta → caja → primer depósito disponible)
4. Obtiene estado inicial de fabricación (menor orden)
5. Crea registro `Fabricacion` con datos calculados

### Generación de Armado

**Condiciones:**
- Venta debe estar **FINALIZADA**
- Estado de seguimiento con `generar_armado_pedido = True` 
- Debe existir al menos un **estado de armado** activo

**Proceso:**
1. Verifica que no exista armado activo para la venta (get_or_create)
2. Obtiene estado inicial de armado (menor orden)  
3. Crea registro `ArmadoPedido` vinculado a la venta
4. Genera `ArmadoPedidoItem` para cada detalle de venta
5. Calcula cantidades y maneja productos sin nombre
6. Registra evento de creación automática

### Idempotencia
- **No duplica procesos**: Si ya existe armado/fabricación no crea duplicados
- **Mensajes claros**: Informa si se creó nuevo o ya existía  
- **Transacciones atómicas**: Garantiza integridad de datos

---

## 🚨 Manejo de Errores

### Errores Comunes y Soluciones

#### Error: "No existe un Estado de Armado activo inicial"
**Causa:** No hay estados de armado configurados  
**Solución:** Crear estados en Admin → Armado → Estado Armado Pedido

#### Error: "NOT NULL constraint failed: descripcion_producto"  
**Causa:** Productos sin nombre en el sistema
**Solución:** ✅ **Automaticamente manejado** - sistema asigna "Producto #ID"

#### Error: "La venta ya tiene un armado activo"
**Causa:** Intento de crear armado duplicado
**Solución:** ✅ **Comportamiento esperado** - no crea duplicados

---

## 📊 Monitoreo y Reportes

### Vista de Ventas - Columnas Informativas

**"Armado / Fab."** - Muestra estado resumido:
```
Armado: En Proceso (1)
Fabricación: Finalizado (2) 
```

**"Estado armado de pedido"** - Detalle específico:
```
#8 - Pendiente
#12 - Listo  
```

**"Estado fabricación"** - Detalle específico:
```
#45 - En Producción
#46 - Horneado
```

### Filtros Disponibles
- Por **estado de seguimiento**
- Por **estado de venta** (finalizada, pagada, etc.)
- Por **cliente**
- Por **fecha**

---

## 🎯 Casos de Uso Recomendados

### Restaurante/Comida Rápida
```
1. Pendiente (sin procesos)
2. En Cocina (↪️ generar fabricación) 
3. Listo para Retirar (estado final)
```

### Distribuidora/Mayorista  
```
1. Confirmado (sin procesos)
2. Produciendo (↪️ generar fabricación)
3. Armando (↪️ generar armado) 
4. Despachado (estado final)
```

### Panadería/Pastelería
```
1. Pedido Recibido (sin procesos)  
2. Horneando (↪️ generar fabricación)
3. Decorando (sin procesos)
4. Empaquetando (↪️ generar armado)
5. Entregado (estado final)
```

---

## ⚡ Mejores Prácticas

### Configuración
- ✅ **Usar orden secuencial** (0, 1, 2, 3...) para flujo lógico
- ✅ **Solo un estado final** por flujo
- ✅ **Colores distintivos** para identificación rápida  
- ✅ **Nombres descriptivos** y claros para el equipo

### Operación  
- ✅ **Finalizar ventas antes** de avanzar estados
- ✅ **Avanzar estados en orden** - no saltar pasos
- ✅ **Revisar mensajes del sistema** para confirmar generaciones
- ✅ **Monitor procesos generados** en sus respectivos admins

### Mantenimiento
- ✅ **No eliminar estados con ventas asociadas** 
- ✅ **Desactivar estados** en lugar de eliminar
- ✅ **Probar cambios en ambiente desarrollo** antes de producción
- ✅ **Capacitar equipo** en el nuevo flujo

---

## 🔍 Troubleshooting

### Problema: No se generan procesos automáticamente
**Verificar:**
1. ¿Venta está FINALIZADA? 
2. ¿Estado tiene checkbox marcado?
3. ¿Existen estados de destino (armado/fabricación)?
4. ¿Hay productos con receta? (para fabricación)

### Problema: Botón "Avanzar" no aparece  
**Verificar:**
1. ¿Estado actual no es final?
2. ¿Existe siguiente estado configurado?
3. ¿Estado siguiente está activo?

### Problema: Productos aparecen como "Producto #ID"
**Causa:** Productos sin nombre en base de datos  
**Impacto:** ✅ **No afecta funcionamiento** - es comportamiento seguro

---

## 📈 Roadmap Futuro

### Posibles Mejoras
- 🔄 **API REST** para integración externa
- 📱 **Notificaciones push** al cambiar estados  
- 📊 **Dashboard temps real** de estados
- 🤖 **IA para sugerir** próximos pasos
- 🔗 **Integración con impresoras** para automizar etiquetas

---

## 👥 Soporte

### Documentación Relacionada
- `README_MODULO_ARMADO_PEDIDOS.md` - Detalles del módulo armado
- Documentación Django Admin - Configuración general  

### Contacto
- **Desarrollador:** Claude Sonnet 4
- **Fecha Implementación:** Febrero 2026  
- **Versión ADESTOCK:** Híbrida

---

*Este sistema de Estados de Seguimiento Automáticos transforma la gestión manual de pedidos en un flujo inteligente y automatizado, reduciendo errores y optimizando tiempos de operación.*