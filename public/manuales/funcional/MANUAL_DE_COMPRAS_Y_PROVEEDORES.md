# Manual de Compras y Proveedores

La gestión eficiente comienza con una buena compra. Este módulo le permite registrar el ingreso de mercadería, actualizar costos y gestionar deudas con proveedores.

---

## 1. Gestión de Proveedores

Antes de comprar, debe decir a quién le compra.

1.  Vaya a **Agenda** > **Proveedores**.
2.  Haga clic en **Agregar Proveedor**.
3.  Complete los datos:
    *   **Empresa:** Nombre comercial (ej. "Distribuidora El Sol").
    *   **Contacto:** Nombre del vendedor.
    *   **Teléfono/Email:** Para reclamos o pedidos.

---

## 2. Registrar una Compra (Ingreso de Stock)

Cada vez que llega un camión o hace una compra en el mayorista, debe registrarla para que suba el stock.

1.  Vaya a **Compra**.
2.  Haga clic en **Nueva Compra**.
3.  **Cabecera:**
    *   Seleccione el **Proveedor**.
    *   **Seleccione el Depósito de Destino:** Indique a dónde ingresará físicamente la mercadería (ej. Depósito Central).
    *   Seleccione el **Medio de Compra** (Efectivo, Transferencia, Cuenta Corriente).
    *   Ingrese el número de factura (opcional, para control fiscal).
4.  **Detalle (Productos):**
    *   Busque el producto (ej. "Harina").
    *   Ingrese la **Cantidad** comprada.
    *   Ingrese el **Costo Unitario** (lo que dice la factura).
    *   *El sistema calculará el subtotal.*
5.  Repita para todos los productos de la factura.
6.  **Guardar:** Al confirmar, el stock de esos productos aumentará inmediatamente.

---

## 3. Actualización de Costos

El sistema es inteligente. Si usted compró Harina a $500 la semana pasada, y hoy carga una compra a $600:

1.  El sistema actualizará el **Costo Base** del producto a $600.
2.  Si tiene configurado "Precio Automático", el sistema sugerirá actualizar el precio de venta para mantener su rentabilidad.

---

## 4. Cuentas Corrientes (Deuda a Proveedores)

Si usted compra "fiado" a un proveedor:

1.  En la compra, seleccione Medio de Compra: **Cuenta Corriente**.
2.  La compra se guarda, el stock sube, pero el dinero no sale de su caja diaria.
3.  Se genera una deuda en la cuenta del proveedor.

**Para pagar esa deuda:**
1.  Vaya a **Compra** > **Pagos a Proveedores**.
2.  Seleccione el proveedor.
3.  Registre un pago (ej. "Pago a cuenta $50.000").
4.  El saldo deudor bajará.
