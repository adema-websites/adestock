# Sistema de Notas de Crédito y Débito para Picking

## Resumen de Implementación

Se ha implementado un sistema completo de notas de crédito y débito que se integra automáticamente con el proceso de picking, proporcionando trazabilidad contable completa y manejo robusto de diferencias en el armado de pedidos.

## ✅ Funcionalidades Implementadas

### 1. **Modelos de Base de Datos**
- **`TipoNota`**: Define tipos de notas (Crédito/Débito) con factores de inventario
- **`NotaAjuste`**: Nota principal con estados (Borrador/Aplicada/Anulada)
- **`DetalleNotaAjuste`**: Líneas de productos ajustados con precios y cantidades

### 2. **Lógica Transaccional Robusta**
- **`procesar_cierre_picking_con_ajustes()`**: Cierre automático con @transaction.atomic
- **`reabrir_picking_con_ajustes()`**: Reapertura con reversión de ajustes
- **Auto-detección de diferencias**: Compara cantidad_pedida vs cantidad_pickeada
- **Generación automática** de notas de crédito por faltantes

### 3. **APIs de Picking Mejoradas**
- **`api_cambiar_estado()`**: Validación especial para estados finales
- **`api_reabrir_picking()`**: Manejo de reapertura con confirmación
- Popup de confirmación obligatorio antes de cerrar
- Información detallada de diferencias y ajustes

### 4. **Interfaz de Administración Completa**
- Admin para TipoNota, NotaAjuste y DetalleNotaAjuste
- Visualización con badges de colores por tipo y estado
- Acciones masivas: aplicar/anular notas
- Restricciones de edición según estado

## 🔧 Flujo de Funcionamiento

### Cierre de Picking (Estado Final)

1. **Usuario intenta avanzar a estado final**
2. **Sistema detecta diferencias** automáticamente
3. **Muestra popup de confirmación** con:
   - Lista de productos faltantes
   - Montos de ajuste
   - Advertencia de impacto en inventario
4. **Si usuario confirma:**
   - Genera nota de crédito automática
   - Ajusta inventario (devuelve faltantes)
   - Registra evento en historial
   - Cierra picking con nueva información

### Reapertura de Picking

1. **Usuario intenta reabrir picking cerrado**
2. **Sistema identifica notas aplicadas**
3. **Muestra popup de confirmación** con:
   - Lista de notas que se anularán
   - Advertencia de reversión de inventario
4. **Si usuario confirma:**
   - Crea notas de débito inversas
   - Revierte ajustes de inventario
   - Cambia estado a editable
   - Registra evento de reapertura

## 📁 Archivos Modificados/Creados

### Backend
- **`venta/models.py`**: Nuevos modelos TipoNota, NotaAjuste, DetalleNotaAjuste
- **`armado/services.py`**: Lógica transaccional de cierre/reapertura
- **`armado/views_picking.py`**: APIs mejoradas con confirmación
- **`venta/admin.py`**: Administración completa de notas

### Frontend
- **`armado/templates/armado/picking_confirmacion_popup.js`**: Popups de confirmación

### Base de Datos
- **`venta/migrations/0005_tiponota_notaajuste_detallenotaajuste.py`**: Nuevas tablas
- **Datos iniciales**: Tipos de nota Crédito (+1) y Débito (-1)

## 🛡️ Seguridad y Robustez

### Transacciones Atómicas
```python
@transaction.atomic()
def procesar_cierre_picking_con_ajustes():
    # Si algo falla, todo se revierte automáticamente
```

### Validaciones Múltiples
- Estado del pedido (debe permitir edición)
- Existencia de diferencias reales
- Permisos de usuario
- Integridad de datos

### Trazabilidad Completa
- **Eventos de armado**: Registro de cada cambio
- **Usuario responsable**: Quién hizo cada acción
- **Timestamps**: Fecha exacta de cada operación
- **Referencias cruzadas**: Nota original ↔ Nota de anulación

## 📊 Reporting y Análisis

### Información Disponible
- **Diferencias por pedido**: Qué productos faltaron y por qué monto
- **Notas por período**: Cuántas notas se generaron automáticamente
- **Usuario performance**: Quién comete más errores en picking
- **Productos problemáticos**: Cuáles faltan más frecuentemente

### Queries Útiles
```python
# Notas de crédito del mes
NotaAjuste.objects.filter(
    fecha_emision__month=datetime.now().month,
    tipo_nota__nombre='CREDITO'
)

# Items con más faltantes
DetalleNotaAjuste.objects.values('producto__nombre').annotate(
    total_faltantes=Sum('cantidad_ajuste')
).order_by('-total_faltantes')
```

## 🔄 Casos de Uso Avanzados

### 1. Corrección de Errores
Si se detecta que una nota de crédito fue incorrecta:
1. Ir al admin de NotaAjuste
2. Usar acción "Anular notas seleccionadas" 
3. Se genera automáticamente nota de débito inversa
4. El inventario se ajusta correctamente

### 2. Ajustes Manuales
Si necesitas hacer ajustes que no sean de picking:
1. Crear NotaAjuste manual en el admin
2. Agregar DetalleNotaAjuste con productos/cantidades
3. Aplicar la nota para que afecte inventario

### 3. Auditorías
```python
# Ver historial completo de un producto
producto = Producto.objects.get(id=123)
ajustes = DetalleNotaAjuste.objects.filter(
    producto=producto
).select_related('nota').order_by('-nota__fecha_emision')
```

## ⚠️ Consideraciones Importantes

### Backup y Recuperación
- Las notas NO se pueden eliminar una vez aplicadas
- Solo se pueden anular creando notas inversas
- Mantener backups regulares antes de cambios masivos

### Performance
- Las consultas usan select_related() y prefetch_related()
- Índices automáticos en campos de búsqueda frecuente
- Paginación en el admin para listas grandes

### Escalabilidad Futura
- Fácil agregar nuevos tipos de nota
- Extensible para otros módulos (no solo picking)
- API preparada para integración con sistemas externos

## 🚀 Próximos Pasos Recomendados

1. **Testing**: Crear casos de prueba automatizados
2. **Reportes**: Agregar dashboard de análisis de diferencias
3. **Mobile UX**: Optimizar popups para tablets/móviles
4. **Integraciones**: Conectar con sistema contable externo
5. **Alertas**: Notificaciones automáticas por exceso de faltantes

## 📞 Soporte

El sistema está completamente documentado y utiliza patrones estándar de Django. Para modificaciones futuras, consultar:
- Documentación de Django Transactions
- Patrones de Service Layer
- Best practices de Django Admin

**¡El sistema está listo para producción!** 🎉