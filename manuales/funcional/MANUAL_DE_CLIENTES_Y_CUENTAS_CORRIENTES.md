# Manual de Clientes y Cuentas Corrientes

Este módulo permite gestionar la base de datos de clientes y ofrecer financiación propia (fiado/cuenta corriente).

---

## 1. Alta de Clientes

Para vender a alguien que no sea "Consumidor Final":

1.  Vaya a **Agenda** > **Clientes**.
2.  **Nuevo Cliente:**
    *   **Nombre:** Nombre completo.
    *   **Documento/CUIT:** Necesario para facturación electrónica.
    *   **Teléfono/Dirección:** Datos de contacto y delivery.
    *   **Habilitar Cuenta Corriente:** Marque esta casilla si desea permitirle comprar fiado.

---

## 2. Vender en Cuenta Corriente (Fiado)

1.  En la pantalla de **Venta**, cargue los productos.
2.  **Seleccione al Cliente:** Es obligatorio identificarlo.
3.  Al cobrar, seleccione el Medio de Pago: **Cuenta Corriente**.
4.  El sistema validará si el cliente tiene la cuenta habilitada.
5.  Se emite un ticket (comprobante de deuda) y el saldo del cliente aumenta.

---

## 3. Cobranza (Recibir Pagos)

Cuando el cliente viene a pagar su deuda:

1.  Vaya a **Venta** > **Cuentas Corrientes** (o Cobranzas).
2.  Busque al cliente. Verá su saldo deudor actual (ej. Debe $20.000).
3.  Haga clic en **Registrar Pago**.
4.  Ingrese el monto que entrega el cliente (ej. $10.000 a cuenta o el total).
5.  Seleccione cómo paga (Efectivo, Transferencia).
6.  El sistema emite un **Recibo de Cobro** y actualiza el saldo.

---

## 4. Consulta de Saldos

Puede ver el estado de cuenta en cualquier momento:

*   **Desde la Venta:** Al seleccionar al cliente, el sistema suele mostrar un aviso: *"Saldo Deudor: $XXXX"*.
*   **Reporte de Deudores:** En la sección de Reportes, puede sacar un listado de todos los clientes que deben dinero y cuánto, ideal para gestionar cobranzas a fin de mes.
