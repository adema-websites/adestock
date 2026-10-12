# Manual de Configuración Inicial

Este documento está dirigido al **Administrador del Sistema** o Dueño del negocio. Aquí se definen las reglas del juego: monedas, datos de la empresa y usuarios.

---

## 1. Datos de la Empresa

Antes de emitir cualquier comprobante, debe configurar la identidad de su negocio.

1.  Vaya a **Agenda** > **Configuración**.
2.  Complete los campos:
    *   **Nombre:** Nombre de fantasía del negocio.
    *   **Dirección y Teléfono:** Aparecerán en los tickets.
    *   **CUIT:** Identificación fiscal.
    *   **Logo:** Suba una imagen cuadrada (preferentemente 500x500px) para personalizar el sistema.

---

## 2. Configuración de Monedas

El sistema es multimoneda, permitiendo operar en un entorno de inflación o doble divisa.

1.  Vaya a **Agenda** > **Monedas**.
2.  Defina su **Moneda Principal** (ej. Pesos ARS). Esta es la moneda base para la contabilidad.
3.  Defina su **Moneda Secundaria** (ej. Dólar USD).
4.  **Tipo de Cambio:** En la configuración general, establezca el valor de conversión.
    *   *Importante:* Si actualiza el tipo de cambio aquí, puede recalcular automáticamente los precios de venta de productos importados.

---

## 3. Usuarios y Permisos

No todos los empleados deben tener acceso a todo.

1.  Vaya a **Usuarios** (o Administración de Django > Usuarios).
2.  **Crear Usuario:** Ingrese nombre de usuario y contraseña.
3.  **Asignar Roles:**
    *   **Superusuario:** Acceso total (borrar, crear, configurar). Solo para dueños.
    *   **Staff (Vendedor):** Acceso limitado a ventas y caja.
    *   **Cocina:** Acceso solo a recetas y pedidos de producción.

---

## 4. Parámetros de Venta

En **Agenda** > **Configuración**, encontrará interruptores clave para adaptar el sistema a su rubro:

*   **Ventas Mayoristas:** Habilita listas de precios diferenciadas por volumen.
*   **Entrega (Delivery):** Habilita módulos de choferes y hojas de ruta.
*   **Stock Negativo:**
    *   *Activado:* Permite vender aunque el sistema diga que hay 0 stock (útil si la carga de compras está atrasada).
    *   *Desactivado:* Bloquea la venta si no hay stock (control estricto).
*   **Precio Venta Automático:** Si se activa, el precio se calcula solo (Costo + Rentabilidad). Si se desactiva, usted escribe el precio final a mano.
