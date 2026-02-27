# 🚀 ADEstock

Sistema Integral de Gestión, Punto de Venta (POS) y Control de Inventario.

ADEstock es una plataforma de gestión comercial diseñada para escalar. Desarrollada con arquitectura híbrida (Cloud + Desktop), permite operar de manera ágil en el mostrador mientras mantiene una sincronización y control financiero estricto en el backend.

## ✨ Funcionalidades Clave

### 🛒 1. Punto de Venta (POS) y Gestión de Caja
- **Operación Ágil:** Búsqueda ultrarrápida de productos por nombre o código de barras, ajuste dinámico de cantidades y asociación a clientes en tiempo real.
- **Control de Turnos Avanzado:** Sistema de turnos diarios con políticas configurables (ej. `permitir_turno_abierto_multidia`). Bloquea ventas si existen turnos abiertos de días anteriores con movimientos, forzando un cierre de caja ordenado.
- **Cierre de Caja Inteligente:** El modal de cierre detecta automáticamente el turno activo, mostrando el cajero, fechas y el total teórico esperado, permitiendo al usuario ingresar el conteo físico para un arqueo preciso.
- **Impresión Híbrida:** Soporte para comprobantes clásicos en PDF vía web, o impresión silenciosa y directa a comandas/impresoras térmicas (USB/Red) mediante una cola de impresión (`print_queue`) y un agente local en Windows.

### 📦 2. Inventario y Catálogo de Productos
- **Trazabilidad Absoluta:** Automatización de stock donde las compras suman y las ventas descuentan de forma instantánea.
- **Sistema de Variantes:** Soporte nativo para productos "padre" (ej. Remera) y "variantes" (ej. Talle M, Color Negro). El stock, precios y códigos de barras se manejan a nivel variante, con un modal intuitivo de selección en el POS.
- **Onboarding Rápido:** Comandos de inicialización (ej. `datos_dietetica`) para poblar rápidamente el sistema con catálogos base, proveedores y escalas de venta.

### 👥 3. Clientes y Cuentas Corrientes
- **Gestión de Saldos y Adelantos:** Registro de cobros parciales o acumulación de dinero como "Saldo a favor".
- **Cobro Inteligente:** Integración del saldo a favor directamente en el POS para cancelar deudas pendientes, calculando el "faltante neto" al instante.
- **Comprobantes Detallados:** Generación automática de recibos de cobro y "Comprobantes de Adelanto".

### 💳 4. Billeteras y Cuentas Financieras
- **Multi-billetera:** Gestión unificada de Banco, Efectivo, MercadoPago, PayPal, Crypto, etc.
- **Automatización Financiera:** Generación automática de ingresos/egresos vinculados a ventas, compras, gastos operativos o pagos a proveedores.
- **Control y Transferencias:** Cálculo de saldos en tiempo real, prevención de saldos negativos (configurable) y transferencias interbancarias/caja con validación estricta.

### 🍳 5. Producción, Recetas y Costos
- **Importación Masiva (Excel):** Carga rápida de recetas mediante archivos de 3 hojas (`Inventario`, `Recetas`, `Productos_Receta`).
- **Conversiones Automáticas:** El motor de costos calcula automáticamente el valor por porción o receta, aplicando conversiones lógicas (ej. compra en Kilos, consumo en Gramos).
- **Integridad de Datos:** Restricciones lógicas de arquitectura (un producto con variantes no puede tener receta propia y viceversa).

### 🚚 6. Armado de Pedidos (Picking Mayorista)
- **Generación Automática:** Creación de órdenes de "Armado de Pedido" al cerrar ventas, optimizado para distribuidoras.
- **Flujo de Estados:** Transiciones configurables (`Pendiente` ➔ `En picking` ➔ `Cerrado`).
- **Control de Diferencias:** Comparación de cantidades pedidas vs. enviadas, con generación automática de Notas de Crédito por mercadería faltante.
- **Reportes Logísticos:** Generación de hojas de ruta en PDF con códigos, descripciones y cantidades.

### 📊 7. Reportes y Panel Administrador
- **Exportaciones Gerenciales:** Descarga de reportes financieros consolidados en Excel (`export-caja-excel`, `export-dashboard-excel`) cruzando compras, ventas, mermas y gastos.
- **Vistas Personalizadas:** Sistema de mixins que guarda las preferencias de cada usuario sobre qué columnas ver/ocultar en las tablas de administración.
- **Dashboard Ultra-Optimizado:** Panel principal con índices de base de datos, caché en bloques pesados (valuación de inventario) y profiling de SQL para tiempos de carga instantáneos.

### ⚙️ 8. Arquitectura, Seguridad y Soporte
- **Backups Automatizados (Google Drive):** Integración nativa OAuth2 que genera snapshots seguros de la base de datos (eludiendo bloqueos de SO) y archivos multimedia, comprimiéndolos en ZIP y subiéndolos directamente a la nube del cliente.
- **Sistema de Licenciamiento (Freemium/Pro):** Validador offline integrado. La versión gratuita limita el volumen operativo, mientras que la versión PRO se vincula criptográficamente al hardware (Machine ID).
- **Despliegue Híbrido:** Preparado para funcionar en la nube (VPS) o empaquetado como un ejecutable `.exe` nativo para Windows, sirviendo archivos estáticos localmente sin dependencias externas.
- **Soporte Integrado:** Vistas de error amigables (400, 404, 500) con integración directa a WhatsApp para reportes de fallos al equipo de desarrollo.

## 🔗 Enlaces útiles
- [Sitio principal de ademasistemas.com](https://ademasistemas.com)
- [Descargar demo](descargar-demo.html)
- [Tutoriales](tutoriales.html)
- [Política de privacidad](politica-privacidad.html)
- [Términos y condiciones](terminos-condiciones.html)
- [Contacto](contacto.html)