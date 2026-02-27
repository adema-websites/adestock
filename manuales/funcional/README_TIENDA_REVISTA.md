# Módulo Tienda Online / Revista Digital (ADEstock)

## Objetivo

Implementar una vitrina online desacoplada del POS/Admin, accesible desde `/revista/`, con:

- Branding configurable por negocio.
- Catálogo real del sistema.
- UX mobile-first.
- Control de visibilidad de precios por autenticación.
- Escalabilidad para miles de productos.

---

## Resumen funcional

La mejora agrega una nueva app Django: `tienda`.

### Qué permite

1. Publicar la revista online en URL pública:
   - `/revista/`

2. Consumir datos por API interna desacoplada:
   - `/api/tienda/v1/revista/`
   - `/api/tienda/v1/config/`

3. Tomar datos reales del sistema:
   - Empresa y moneda desde `agenda.Configuracion`.
   - Categorías desde `producto.Categoria`.
   - Productos desde `producto.Producto`.
   - Precios por variantes desde `producto.ProductoPrecio`.

4. Respetar reglas de negocio definidas:
   - Solo productos con `habilitar_venta=True`.
   - Precios ocultos para público.
   - Precios visibles al iniciar sesión.

---

## Arquitectura implementada

## 1) Nueva app `tienda`

Archivos principales:

- `tienda/models.py`
- `tienda/views.py`
- `tienda/urls.py`
- `tienda/admin.py`
- `tienda/templates/tienda/revista.html`
- `tienda/static/tienda/revista.css`
- `tienda/static/tienda/revista.js`
- `tienda/migrations/0001_initial.py`

Integraciones globales:

- `adestock/settings.py`: app agregada en `INSTALLED_APPS`.
- `adestock/urls.py`: include de rutas de tienda.
- `adestock/custom_admin_registry.py`: registro para admin custom.

---

## 2) Modelos de configuración

## `TiendaConfiguracion`

Define parámetros visuales y de layout:

- `nombre_tienda`
- `slogan`
- `vigencia_texto`
- `color_primario`
- `color_secundario`
- `color_fondo`
- `color_texto`
- `fuente_principal`
- `productos_por_fila_movil`
- `productos_por_fila_tablet`
- `productos_por_fila_desktop`
- `mostrar_stock`
- `mostrar_descripcion`
- `mostrar_solo_categorias_configuradas`
- `activa`

## `TiendaCategoriaConfig`

Permite elegir categorías visibles y orden en la revista:

- Relación con `producto.Categoria`
- `visible`
- `orden`

---

## 3) API desacoplada

## Endpoint de datos completos

`GET /api/tienda/v1/revista/`

Retorna:

- `empresa` (nombre/logo/moneda)
- `tienda` (config visual y layout)
- `categorias` con productos agrupados

## Endpoint de configuración

`GET /api/tienda/v1/config/`

Retorna:

- Datos de empresa
- Configuración de tienda
- Cantidad de categorías

## Búsqueda incorporada por query string

`GET /api/tienda/v1/revista/?q=texto`

Filtra productos por:

- nombre
- descripción
- código de barras
- marca
- categoría

---

## 4) Reglas de visibilidad de precios

- Usuario NO autenticado:
  - Ve catálogo y detalle de producto.
  - No ve importes.

- Usuario autenticado:
  - Ve precios y variantes por producto.

La lógica se resuelve en backend (`request.user.is_authenticated`) y se refleja en frontend.

---

## 5) UX implementada en la revista

## Mobile-first

- Grid con mínimo 2 cards por fila en móvil.
- Cantidad de cards configurable por admin para móvil/tablet/desktop.

## Modal de producto (click en card)

Al hacer click en una card se abre modal con:

- nombre
- descripción
- unidad de medida
- todas las variantes de precio (cantidad + unidad + importe)

## Navegación por categorías

- Tabs horizontales sticky.
- Scroll suave hacia cada sección.

## Buscador integrado

- Input en cabecera de navegación.
- Debounce (320ms).
- Botón limpiar.
- Recarga de resultados por API.

---

## 6) Rendimiento para catálogos grandes

Se aplicaron dos mecanismos:

1. Lazy rendering por lotes (frontend)
   - Render inicial parcial por categoría.
   - Carga incremental al scroll con `IntersectionObserver`.

2. Lazy loading de imágenes
   - `loading="lazy"`
   - `decoding="async"`

Resultado: menor costo de render inicial y mejor respuesta con grandes volúmenes.

---

## Administración

Desde Admin (custom site) se puede gestionar:

- Configuración visual de tienda.
- Orden/visibilidad de categorías.

Modelos registrados:

- `TiendaConfiguracion`
- `TiendaCategoriaConfig`

---

## Migraciones y validación

Migración creada y aplicada:

- `tienda.0001_initial`

Validación técnica ejecutada:

- `python manage.py check` (sin errores)

---

## Flujo operativo recomendado

1. Ingresar al admin y configurar `TiendaConfiguracion`.
2. Definir categorías visibles y orden.
3. Confirmar productos con `habilitar_venta=True`.
4. Probar `/revista/` como público (sin login).
5. Probar `/revista/` autenticado para validar precios.
6. Probar búsquedas (`q`) y scroll con alto volumen de productos.

---

## Notas de compatibilidad

- No rompe POS ni módulos existentes.
- Reutiliza modelos actuales de productos/categorías/precios.
- Mantiene separación vista/API para facilitar futura tienda externa.

---

## Próximas mejoras sugeridas

- Paginación server-side opcional en API.
- Cache por query para búsquedas frecuentes.
- Filtros avanzados (rango de precio, marca, stock).
- Slug SEO por categoría/producto para front público web.
- Endpoint público firmado para consumir desde un frontend externo (SPA).
