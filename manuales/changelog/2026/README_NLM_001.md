# README NLM 001 · Inicio rápido Dietética (storytelling + guía LLM)

## 1) Propósito de este documento

Este README está pensado para:

- mostrar un **recorrido inicial real** de ADEstock,
- explicar de forma simple **cómo funciona el negocio dentro del sistema**,
- servir como guía de referencia para un **LLM** que asista a usuarios en onboarding,
- enfocar el caso de uso en **`datos_dietetica`**.

> Escenario: abrimos una dietética nueva y en 1 jornada dejamos el sistema operativo para vender, comprar, mover stock, cerrar caja y analizar el Excel del admin override.

---

## 2) Contexto rápido para LLM (resumen operativo)

Si eres un asistente LLM, asume estas reglas de negocio para este flujo:

1. Una **compra** suma stock y actualiza costos.
2. Una **venta** descuenta stock y registra cobro (o cuenta corriente).
3. El **inventario se mueve** por compras, ventas y ajustes (mermas/traslados).
4. El **cierre de caja** compara lo teórico vs lo real del turno.
5. El **reporte Excel del admin override** consolida resultados (compras, ventas, NC/ND, gastos, depreciaciones, eléctricos, etc.).

---

## 3) Prerrequisitos mínimos

- Proyecto migrado y funcionando.
- Usuario con acceso al admin y módulos de venta/compra.
- Caja configurada.
- Depósito configurado.

Comandos base:

```bash
python manage.py migrate
python manage.py runserver
```

---

## 4) Capítulo 1 — “Abrimos la dietética en 10 minutos”

### Paso 1: cargar dataset inicial de dietética

Ejecutar:

```bash
python manage.py datos_dietetica
```

Este comando deja una base operativa con:

- categorías,
- proveedor de ejemplo,
- cliente de ejemplo,
- productos,
- precios por escala (kg/gramos/unidad según producto),
- recetas de fabricación propia.

Resultado esperado en consola: mensaje de proceso completado y “Dietética lista para usar”.

---

## 5) Capítulo 2 — “Primera compra: entra mercadería y sube stock”

Historia: llega reposición de frutos secos del proveedor.

### Flujo funcional

1. Ir a **Compra → Nueva Compra**.
2. Seleccionar proveedor.
3. Elegir **depósito de destino**.
4. Elegir medio de compra (efectivo/transferencia/CC).
5. Agregar productos con cantidad y costo.
6. Confirmar compra.

### Qué pasa internamente

- Se crean líneas de compra.
- El stock sube en el depósito elegido.
- El costo de producto puede actualizarse con el nuevo valor de reposición.
- Si la compra fue a cuenta corriente, queda saldo pendiente al proveedor.

---

## 6) Capítulo 3 — “Primera venta: baja stock y entra dinero”

Historia: una clienta compra 500g de granola y 250g de semillas.

### Flujo funcional

1. Abrir caja en POS (si aún no está abierta).
2. Buscar productos por nombre/código.
3. Ajustar cantidades.
4. Seleccionar cliente (opcional, por defecto consumidor final).
5. Cobrar con medio de pago.
6. Confirmar e imprimir ticket.

### Qué pasa internamente

- Se registra `Venta` y su detalle.
- El stock se descuenta automáticamente.
- Se guarda el medio de pago y su impacto de caja/CC.
- La operación queda disponible para reportes y cierre.

---

## 7) Capítulo 4 — “Mover inventario: cómo leerlo en la práctica”

En este recorrido inicial, el inventario se mueve así:

- **Compra**: movimiento de entrada (+).
- **Venta**: movimiento de salida (−).
- **Merma/ajustes/traslados** (si se usan): impacto adicional según tipo.

Recomendación para demo comercial:

1. Hacer 1 compra corta (2–3 productos).
2. Hacer 2 ventas cortas.
3. Ir al inventario y mostrar cómo cambiaron las existencias.

Con eso el cliente entiende el corazón del sistema: “todo lo que compro entra, todo lo que vendo sale”.

---

## 8) Capítulo 5 — “Cierre de caja del turno”

Historia: termina el turno de la tarde y necesitamos rendir caja.

### Flujo funcional

1. Ir a **Venta → Cerrar Caja**.
2. Revisar resumen teórico:
   - ventas por medio,
   - gastos/retiros,
   - total esperado en cajón.
3. Contar efectivo real.
4. Confirmar cierre.

### Qué obtiene el negocio

- Control de diferencias (sobrante/faltante).
- Trazabilidad por cajero/turno.
- Base para auditoría interna diaria.

---

## 9) Capítulo 6 — “Reporte de caja + Excel del Admin Override”

Historia: ahora el dueño quiere mirar el negocio completo en una planilla.

### 9.1 Reporte de caja (panel admin)

Ruta funcional del panel:

- **Admin Override → Reportes de Caja**
- filtrar fechas/cajero
- exportar PDF o Excel según necesidad

Endpoints implementados en el admin personalizado:

- `reportes-caja/`
- `export-caja-pdf/`
- `export-caja-excel/`
- `export-dashboard-excel/`

### 9.2 Qué incluye el Excel de `export-caja-excel`

Resumen de contenido (hojas):

1. Carátula / resumen general
2. Compras (cabecera, productos, pagos)
3. Ventas (cabecera, productos, cobros)
4. NC/ND
5. Gastos
6. Depreciación de bienes
7. Costos operativos
8. Mermas
9. Conceptos eléctricos

En términos comerciales, este Excel muestra el “estado operativo-financiero” del período en una sola descarga.

### 9.3 Qué incluye el Excel de `export-dashboard-excel`

- Estado de resultados
- Depreciación de bienes
- Top productos
- Top clientes

Ideal para lectura gerencial rápida.

---

## 10) Script de demo para vender el sistema (pitch corto)

Puedes contar el producto así:

1. “Cargo datos iniciales de dietética en minutos (`datos_dietetica`).”
2. “Registro una compra y el stock sube automáticamente.”
3. “Hago una venta en POS y el stock baja al instante.”
4. “Cierro caja y controlo diferencias de turno.”
5. “Descargo Excel desde admin override y veo compras, ventas, NC/ND, gastos y costos técnicos.”

Mensaje final para cliente:

> ADEstock no es solo facturar: es controlar flujo real del negocio con trazabilidad completa, desde mercadería hasta resultado económico.

---

## 11) Prompt recomendado para asistentes LLM internos

Usar como prompt base:

```text
Actúa como consultor funcional de ADEstock para una dietética.
Explica siempre en pasos numerados y con lenguaje simple.
Prioriza este flujo: cargar datos_dietetica, hacer compra, hacer venta, validar movimiento de stock, cerrar caja y exportar Excel desde admin override.
Si el usuario pide más detalle, ampliar con rutas de menú y qué valida cada paso.
```

---

## 12) Lecturas complementarias (enlaces)

- [README.md](README.md)
- [README_TECNICO.md](README_TECNICO.md)
- [manuales/MANUAL_DE_VENTAS_Y_CAJA.md](manuales/MANUAL_DE_VENTAS_Y_CAJA.md)
- [manuales/MANUAL_DE_COMPRAS_Y_PROVEEDORES.md](manuales/MANUAL_DE_COMPRAS_Y_PROVEEDORES.md)
- [manuales/MANUAL_DE_REPORTES_Y_ESTADISTICAS.md](manuales/MANUAL_DE_REPORTES_Y_ESTADISTICAS.md)
- [manuales/MANUAL_DE_CONFIGURACION_INICIAL.md](manuales/MANUAL_DE_CONFIGURACION_INICIAL.md)
- [manuales/MANUAL_GUIA_TUTORIALES.md](manuales/MANUAL_GUIA_TUTORIALES.md)
- [manuales/MANUAL_PICKING_MOVIL.md](manuales/MANUAL_PICKING_MOVIL.md)
- [SISTEMA_NOTAS_CREDITO_DEBITO_README.md](SISTEMA_NOTAS_CREDITO_DEBITO_README.md)

---

## 13) Checklist de éxito (onboarding dietética)

- [ ] Corrí `python manage.py datos_dietetica`
- [ ] Registré una compra completa
- [ ] Registré al menos una venta en POS
- [ ] Verifiqué cambio de stock
- [ ] Ejecuté cierre de caja
- [ ] Exporté y abrí `export-caja-excel`
- [ ] Expliqué al cliente el resultado operativo del período

Con este checklist completo, la implementación inicial queda lista para demostración comercial y arranque operativo.
