# Manual de Puntos de Venta, Cajeros e Impresoras

Este documento explica cómo configurar y operar los Puntos de Venta (Cajas) y el sistema de impresión de tickets.

> **IMPORTANTE:** Este sistema está diseñado para ejecutarse preferentemente de forma **LOCAL** (en la misma computadora donde están conectadas las impresoras) o en una red local controlada. Esto permite que el sistema se comunique directamente con el hardware (impresoras USB) sin necesidad de diálogos de impresión del navegador ni configuraciones complejas de drivers web.

---

## 1. Conceptos Básicos

Para entender cómo funciona la facturación y emisión de tickets, debemos distinguir tres elementos:

1.  **Punto de Venta (Caja):** Es la representación virtual del lugar físico de cobro. Define de qué depósito se descuenta la mercadería vendida.
2.  **Usuario (Cajero):** La persona que opera el sistema.
3.  **Asignación:** El vínculo que le dice al sistema: *"Cuando el usuario Juan inicie sesión, estará vendiendo desde la Caja 1"*.

---

## 2. Configuración Paso a Paso

### Paso 1: Crear el Punto de Venta (Caja)
1.  Ingrese al Panel de Administración.
2.  Vaya a la sección **Agenda** > **Puntos de venta**.
3.  Cree una nueva Caja (ej. "Caja Principal", "Barra", "Kiosco").
4.  Asigne el **Depósito** del cual se descontará el stock.

### Paso 2: Configurar la Impresora
Cada Caja tiene su propia configuración de impresora. Esto permite que la "Caja Barra" imprima en la cocina y la "Caja Entrada" imprima en la recepción.

Dentro de la configuración de la Caja, encontrará la sección **Configuración de Impresora**:

#### A. Impresoras USB (Recomendado)
Esta es la configuración más común y robusta para este sistema.
1.  Conecte su impresora térmica por USB a la computadora donde corre el sistema.
2.  Instale el driver de Windows correspondiente.
3.  Vaya al **Panel de Control > Dispositivos e Impresoras** y anote el **nombre exacto** de la impresora (ej. `POS-58`, `EPSON TM-T20`, `Generic Text Only`).
4.  En el sistema, seleccione **Tipo de impresora: USB**.
5.  En el campo **Nombre de impresora USB**, escriba el nombre **exactamente igual** al de Windows.

> **¿Por qué USB?** Al estar conectado directamente, el sistema envía los comandos de corte de papel, apertura de cajón de dinero y formato de texto directamente al puerto, garantizando velocidad y precisión.

#### B. Impresoras de RED (Ethernet/Wi-Fi)
Útil si la impresora está lejos de la computadora (ej. en la cocina) y conectada por cable de red al router.
1.  Seleccione **Tipo de impresora: Impresora de Red (IP)**.
2.  **IP de impresora:** Ingrese la dirección IP fija de la impresora (ej. `192.168.0.100`).
3.  **Puerto:** Generalmente es `9100`.

#### C. Tamaño de Papel
Configure el ancho correcto para evitar que el texto salga cortado:
*   **58mm (32 caracteres):** Tickets angostos, comunes en impresoras portátiles o económicas.
*   **80mm (48 caracteres):** Tickets anchos estándar de supermercado/restaurante.

### Paso 3: Asignar el Usuario a la Caja
Para que el sistema sepa dónde imprimir cuando un empleado cobra:
1.  Vaya a **Agenda** > **Asignacion**.
2.  Cree una nueva asignación.
3.  Seleccione el **Usuario** (ej. "cajero1").
4.  Seleccione el **Punto de venta** (ej. "Caja Principal").

---

## 3. Flujo de Trabajo Diario

Una vez configurado, el funcionamiento es transparente para el usuario:

1.  El empleado "Juan" inicia sesión en el sistema.
2.  El sistema detecta que "Juan" está asignado a "Caja Principal".
3.  Juan realiza una venta y presiona "Cobrar".
4.  El sistema busca la configuración de impresora de "Caja Principal".
5.  **Automáticamente** (sin abrir ventanas emergentes de PDF), el ticket sale impreso por la impresora configurada.

### Solución de Problemas Comunes

*   **No imprime nada (USB):** Verifique que el nombre en el admin sea idéntico al de Windows (mayúsculas, espacios, guiones). Pruebe imprimir una página de prueba desde Windows para descartar fallas de cable.
*   **Imprime caracteres raros:** Verifique que el ancho del papel (58mm/80mm) coincida con el físico.
*   **Error "No hay impresora configurada":** Asegúrese de que el usuario logueado tenga una **Asignación** activa a una Caja que tenga impresora configurada.
