# Manual de Gestión de Depósitos y Transferencias

Este documento explica cómo administrar múltiples inventarios (depósitos) y cómo mover mercadería entre ellos de manera segura y controlada.

---

## 1. Conceptos Generales

El sistema permite gestionar el stock en diferentes ubicaciones físicas o lógicas. Por ejemplo:
*   **Depósito Central:** Donde se recibe la mercadería de proveedores.
*   **Sucursal 1 (Salón):** Donde se realiza la venta al público.
*   **Cocina:** Donde se materia prima para elaboración.

Cada producto tiene un stock independiente en cada depósito. "Coca Cola" puede tener 100 unidades en el Depósito Central y 20 en la Sucursal 1.

---

## 2. Gestión de Depósitos

Para crear o editar los lugares donde se guarda mercadería:

1.  Vaya a **Agenda** > **Depósitos**.
2.  **Nuevo Depósito:**
    *   **Nombre:** Identificador claro (ej. "Cámara de Frío", "Mostrador").
    *   **Dirección:** (Opcional) Ubicación física.
3.  **Guardar.**

> **Nota:** Al vender, la caja registradora suele estar asociada a un depósito específico, descontando stock automáticamente de allí.

---

## 3. Transferencias de Inventario (Movimiento de Stock)

Cuando usted lleva mercadería de un lugar a otro (ej. del Depósito al Salón para reponer góndolas), debe registrar una **Transferencia** para que el stock se descuente de uno y sume en el otro.

### A. Crear una Transferencia

1.  Vaya a **Producto** > **Transferencias**.
2.  Haga clic en **Nueva Transferencia**.
3.  **Cabecera:**
    *   **Fecha:** Día del movimiento.
    *   **Depósito de Salida:** ¿De dónde sacamos la mercadería? (El sistema verificará que haya stock aquí).
    *   **Depósito de Entrada:** ¿A dónde va la mercadería?
    *   **Chofer / Vehículo:** (Opcional) Si el traslado requiere transporte logístico.
4.  **Guardar Cabecera** para habilitar la carga de productos.

### B. Agregar Productos (Detalle)

1.  En la ficha de la transferencia, busque los productos a mover.
2.  Indique la **Cantidad**.
3.  El sistema validará si hay stock suficiente en el *Depósito de Salida*.
    *   *Si no hay stock, no le dejará agregar el producto para evitar stock negativo.*

### C. Estados de la Transferencia (Confirmación)

Las transferencias tienen estados para controlar el flujo (ej. "Pendiente", "En Tránsito", "Recibido").

*   Cuando crea la transferencia, el stock **NO se mueve inmediatamente**. Queda en estado "Pendiente" o "Borrador".
*   Para hacer efectivo el movimiento, debe cambiar el estado a un **Estado Final** (generalmente llamado "Finalizado" o "Recibido").
*   **Solo al pasar a Estado Final:**
    *   Se resta el stock del Depósito de Salida.
    *   Se suma el stock al Depósito de Entrada.

> **Importante:** Si la mercadería se pierde en el camino (roturas en el traslado), debe ajustar la cantidad en el destino o registrar una Merma posterior.

---

## 4. Visualización de Stock por Depósito

Para saber dónde está su mercadería:

1.  Vaya a **Producto** > **Lista de Productos**.
2.  Utilice los filtros de búsqueda para seleccionar **"Stock en Depósito: [Nombre]"**.
3.  La columna de stock mostrará la cantidad disponible solo en esa ubicación.

También puede ver la ficha individual de un producto para ver el desglose total:
*   Total Empresa: 150
    *   Depósito Central: 100
    *   Sucursal 1: 50
