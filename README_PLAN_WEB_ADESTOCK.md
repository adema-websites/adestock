# Plan maestro de renovación de la web de ADEstock

Fecha: 12 de octubre de 2026. Estado: plan de ejecución; no implica que los cambios ya estén implementados.

Sitio: https://adestock.com.ar/.
Proyecto web revisado: `C:\Users\kevin\OneDrive\Escritorio\web_adestock\adestock_landing_actual`.
Documentación copiada: `C:\Users\kevin\OneDrive\Escritorio\web_adestock\documentacion`.
Fuente funcional: `C:\Users\kevin\OneDrive\Escritorio\ESCRITORIO\adestock\documentacion` y código de la versión del producto que se publique.

## 1. Decisión de producto y objetivos

ADEstock debe presentarse como un sistema para vender, controlar mercadería y ahorrar trabajo en el comercio. La web debe demostrarlo con tareas reales y resultados visibles. El centro de tutoriales será parte central del producto comercial: permitirá evaluar el sistema antes de probarlo y resolver dudas después de instalarlo.

Prioridades, en este orden:

1. Que un comerciante encuentre cómo empezar con sus productos, Excel y stock.
2. Que pueda hacer una venta y comprobar qué pasó con el stock y la caja.
3. Que pueda corregir y contar mercadería sin confundir una existencia final con un movimiento de ajuste.
4. Que descubra cómo cargar una compra sacándole una foto a la boleta y revisando lo leído por IA.
5. Que descubra cómo crear una revista de ofertas, exportarla y compartirla.
6. Que Google pueda descubrir y procesar páginas individuales útiles.
7. Que cada enlace compartido tenga una vista previa coherente y que la adquisición se pueda medir.

La meta comercial es conseguir consultas calificadas, pruebas y clientes; la meta de ayuda es reducir el tiempo hasta resolver una tarea. Posiciones, tráfico e indexación se medirán: no se garantizan ni se inventan objetivos porcentuales sin una línea de base.

## 2. Evidencia y límites de la revisión

| Observación | Evidencia | Implicación |
|---|---|---|
| Hay 32 tutoriales actuales, numerados 02–33 | Markdown en `01-manual-usuario/` | Publicar a partir de esos flujos; el número de origen no será parte de la URL |
| Hay 266 imágenes dentro del manual | Inventario de `01-manual-usuario/imagenes/` | Existe una base de capturas; falta QA visual individual antes de publicar |
| Los 32 Markdown coinciden entre la copia y el origen | Comparación SHA-256 de los archivos homólogos | El texto copiado no presenta divergencias en esa comparación; las imágenes no se compararon por hash |
| Los tutoriales declaran verificación del 12/10/2026 | Encabezados de documentación | Esa declaración se conserva como dato de origen; no sustituye una validación editorial y visual nueva |
| La guía pública usa capítulos cargados con `fetch` | `tutoriales/render-tutorials.js`, manifiesto y JSON | El texto principal debe pasar a HTML generado y URLs propias |
| La extracción web de tutoriales mostró navegación e introducción, sin el cuerpo de los capítulos | Consulta pública de `tutoriales.html` | Señal de fragilidad para lectores sin JS; no prueba por sí sola cómo Google lo indexó |
| El manifiesto antiguo contiene 17 entradas: onboarding, configuración y temas 2–16 | `tutoriales/chapters.json` | La numeración visible no representa 32 guías actuales |
| Hay 42 HTML en el árbol revisado | Inventario, incluye 9 plantillas del panel `admin-temas` | No son 42 páginas comerciales públicas; el inventario de URLs debe excluir plantillas internas |
| GA4 está embebido en varias páginas | ID `G-W01VQ5GZND` | Se vio instalación, no se validó recepción de eventos ni configuración de la cuenta |
| Las traducciones cambian título y descripción en el navegador | `i18n.js` | El copy se administra en más de una capa; evitar que diccionarios antiguos sobrescriban la renovación |
| La home mezcla SoftwareApplication y Product con ofertas diferentes | `index.html` | Unificar entidades y precios reales; quitar datos artificiales |
| Hay API firmada de temas, OAuth y agente de impresión | Carpetas y README de temas | Son contratos del producto: no eliminarlos al limpiar marketing |
| Varias carpetas documentales anunciadas están vacías en la copia | `00-inicio`, `02-referencia`, `03-conceptos`, `04-operacion`, `05-faq`, `llm` | Son estructura prevista, no contenido terminado |

No se ha realizado un crawl completo, inspección de Search Console, auditoría de campañas, evaluación de Core Web Vitals de campo ni revisión visual de todas las capturas. Tampoco se ha leído exhaustivamente el histórico técnico. Las decisiones de este plan se basan en el inventario, encabezados de los 32 tutoriales, lectura de flujos prioritarios, código focalizado y consultas públicas. No atribuir problemas de tráfico a una causa sin datos.

## 3. Arquitectura técnica elegida

Usar Astro como generador estático, con contenido en Markdown, componentes compartidos y JavaScript limitado a búsqueda, filtros, ampliación de capturas y medición. Astro es una decisión de implementación para este proyecto; la propiedad esencial es que el HTML entregado ya contenga todo el tutorial, sus enlaces y sus metadatos.

Mantener el dominio y preservar las URLs existentes que tengan sentido. Verificar hosting real antes de definir redirecciones y despliegue: `CNAME` sugiere dominio propio, y `_headers` contiene reglas para proveedores específicos, pero esos archivos no demuestran qué plataforma sirve producción ni que aplique esas reglas.

Organización propuesta dentro del repositorio web:

```text
src/
  components/           # navegación, CTA, captura, aviso, búsqueda
  layouts/              # comercial, tutorial, artículo
  content/
    tutoriales/         # Markdown público revisado + metadatos
    blog/               # educación y captación
    funciones/          # propuestas comerciales por función
    rubros/             # usos verificables por tipo de comercio
  data/
    sinonimos.json
    rutas-aprendizaje.json
    migracion-urls.csv
    capturas.json       # origen, variante publicada, dimensiones, estado de revisión
  pages/                # rutas estáticas y endpoints de build
public/
  assets/tutoriales/    # derivados optimizados, no capturas temporales
  social/              # tarjetas JPG/PNG para compartir
  api/temas-revista/    # conservar rutas, bytes firmados y paquetes existentes
scripts/               # importación documental, índice de búsqueda y controles
docs/                  # plan y operación editorial; fuera del sitio publicado
```

Mover `admin-temas` a un área de herramientas no publicada, conservando su funcionamiento y referencias. Las rutas de OAuth, vinculación y descargas se migran con pruebas específicas. No copiar `_historico`, bases, scripts de captura ni documentos técnicos internos al directorio público.

La documentación del sistema sigue siendo la fuente de comportamiento. El Markdown web es una adaptación editorial con `source_path`, versión y huella del origen; un control de sincronización detecta cambios para revisión. No publicar automáticamente un cambio técnico sin revisar capturas, mensajes y consecuencias para el cliente.

## 4. Mapa público definitivo

Navegación principal: **Cómo funciona · Para tu negocio · Tutoriales · Precios · Contacto** y CTA **Probar ADEstock**. “Guías para tu comercio” y novedades estarán en recursos y pie de página.

| Ruta | Función | Decisión |
|---|---|---|
| `/` | Propuesta general, demostración y entrada a tareas | Reescribir y rediseñar |
| `/sistema-de-stock/` | Página comercial principal de categoría | Mantener URL, ampliar con evidencia |
| `/control-de-stock/` | Contar, ajustar, detectar diferencias | Mantener, enfoque diferente a categoría |
| `/funciones/compras-con-ia/` | Beneficio de cargar boletas con foto | Crear, enlazar al tutorial real |
| `/funciones/revistas-y-folletos/` | Crear piezas de ofertas desde productos | Crear, mostrar resultado real |
| `/funciones/punto-de-venta/` | Venta, cobro y ticket | Crear después de los pilares prioritarios |
| `/funciones/productos-y-excel/` | Migrar catálogo y controlar existencias | Crear con explicación de los dos flujos |
| `/funciones/cuentas-corrientes/` | Fiado, cobros y saldos | Segunda etapa |
| `/sistema-de-stock-para-kioscos/` | Caso por rubro | Mantener, ejemplo propio |
| `/sistema-de-stock-para-almacenes/` | Caso por rubro | Mantener, ejemplo propio |
| `/sistema-de-stock-para-minimarkets/` | Caso por rubro | Mantener, ejemplo propio |
| `/precios.html` | Condiciones y elección | Mantener URL; validar planes y alcance vigente |
| `/descargar-demo.html` | Acceso a prueba y requisitos | Mantener URL; verificar instalador y condiciones |
| `/contacto.html` | Soporte y consulta comercial claramente diferenciados | Mantener URL |
| `/tutoriales/` | Centro de ayuda y buscador | Nueva entrada canónica |
| `/tutoriales/empezar/` | Ruta rápida inicial | Crear con orden y requisitos |
| `/tutoriales/{slug}/` | Una tarea completa | Crear por cada guía revisada |
| `/tutoriales/categorias/{slug}/` | Índice curado con contexto | Crear solo para categorías con contenido |
| `/tutoriales/buscar/` | Resultados del buscador | `noindex`, fuera del sitemap |
| `/blog/` y artículos actuales | Educación, problemas del negocio | Conservar URLs útiles y actualizar |
| `/versiones.html` | Novedades orientadas al usuario | Mantener, depurar detalle técnico |
| `/agent-printer.html` | Descarga operativa de impresión | Mantener ruta y enlaces del producto |
| `/temas-revistas/` | Catálogo de temas | Integrar visualmente sin romper API |
| Legales existentes | Condiciones reales y privacidad | Mantener, revisar coherencia |

Priorizar español de Argentina. Publicar otros idiomas solo con URLs propias, contenido completo y revisión humana; entonces usar `hreflang` recíproco y canonical por idioma. Retirar gradualmente el cambio automático de idioma que altera una misma URL y puede mostrar copy desactualizado. Los nombres del producto y los botones reales se conservan.

## 5. Home: estructura y dirección de copy

H1 de trabajo: **Vendé y controlá el stock de tu comercio con ADEstock**.
Subtítulo: **Cargá tus productos, registrá ventas y compras, y revisá tu mercadería desde un mismo sistema. Seguí los tutoriales para empezar paso a paso.**

Orden de bloques:

1. Promesa clara, captura real del producto, CTA “Probar ADEstock” y secundario “Ver cómo se usa”.
2. “¿Qué querés hacer primero?” con cinco accesos: Excel, primera venta, corregir stock, compra con foto, revista de ofertas.
3. Circuito básico ilustrado: productos → venta → control del stock. Explicar la confirmación de compras cuando se mencione ingreso de mercadería.
4. Compras con IA: foto original ficticia → revisión de renglones → compra confirmada. Enlace al tutorial.
5. Revistas: productos y ofertas → diseño → PDF/imagen/enlace. Mostrar una pieza real terminada.
6. Usos por rubro, con enlaces a páginas específicas.
7. Prueba social verificable: casos autorizados y demostraciones. No inventar testimonios, cantidades de clientes ni ahorros.
8. Condiciones de prueba y acceso a precios.
9. Dudas previas a contratar: instalación, modalidad, permisos, soporte e IA; respuestas verificadas en versión comercial.
10. CTA final y contacto.

Voseo consistente: “cargá”, “elegí”, “revisá”. Una frase, una idea. Traducir jerga al primer uso: “lectura de boletas con IA (OCR)”. Evitar “trazabilidad absoluta”, “instantáneo”, “sin errores” o cifras de ahorro no medidas. No mostrar SQL, modelos de Django o estructura de backend en páginas comerciales.

Revisar afirmaciones sobre ARCA/AFIP, funcionamiento offline, nube, licencia y demo contra la versión comercial y sus módulos. El sitio público dice que no incluye facturación fiscal, mientras hay documentación técnica de integraciones: eso exige determinar alcance real, no cambiar la promesa por inferencia.

## 6. Centro de ayuda orientado a tareas

Encabezado: **¿Qué querés hacer con ADEstock?** Buscador visible con ejemplo “cargar productos desde Excel, hacer una venta, corregir stock…”.

La primera pantalla debe mostrar las cinco tareas prioritarias, la ruta “Empezar desde cero” y categorías con lenguaje cotidiano:

- Empezar y cargar productos.
- Vender y cobrar.
- Controlar stock y precios.
- Comprar y trabajar con proveedores.
- Clientes y cuentas corrientes.
- Crear ofertas, revistas y tienda online.
- Controlar caja y el negocio.
- Instalar, imprimir y resolver problemas.

Filtros secundarios por rol (dueño, cajero, administrativo) y superficie (POS, App, Panel). Las tarjetas dicen qué se logra, requisitos, tiempo orientativo y fecha de verificación; no exhiben rutas técnicas. El contenido completo debe funcionar sin iniciar sesión y sin JavaScript.

Ruta inicial propuesta:

1. Configurar el negocio.
2. Elegir cómo cargar productos: manual o Excel.
3. Cargar existencias iniciales según depósito.
4. Abrir turno y recorrer lo mínimo del POS.
5. Hacer la primera venta.
6. Verificar el stock y cerrar caja.

Permitir saltar directamente a una tarea si ya se cumplen sus requisitos. “Tutorial siguiente” depende de la ruta elegida; “Relacionado” depende de la tarea, no del número del archivo.

## 7. Cola editorial y mapa de los 32 tutoriales actuales

Prioridad P0: onboarding, Excel/productos, venta, stock, compra con IA, revista. P1: operación diaria restante. P2: administración avanzada y operación. La tabla define slugs bajo `/tutoriales/`; no publicar una ficha vacía para reservar una URL.

| Fuente | Slug propuesto | Tratamiento | Prioridad |
|---|---|---|---|
| 02 | `configurar-negocio` | Configuración inicial, explicada sin “onboarding” como palabra principal | P0 |
| 03 | `cargar-productos` | Alta manual, costo por bulto y precios; enlace a Excel | P0 |
| 04 | `usuarios-y-permisos` | Crear usuario y habilitar tareas con ejemplos | P1 |
| 05 | `configurar-punto-de-venta` | Equipo, negocio y módulos; distinguir permisos | P1 |
| 06 | `usar-punto-de-venta` | Recorrido y atajos; apoyo a primera venta | P0 |
| 07 | `hacer-una-venta` | Búsqueda, presentación, cobro y comprobación final | P0 |
| 08 | `cobrar-con-varios-medios-de-pago` | Pagos combinados, descuentos y recargos | P1 |
| 09 | `vender-fiado-cuenta-corriente` | Cliente, deuda y límites reales | P1 |
| 10 | `anular-venta-y-reimprimir-ticket` | Dos rutas claramente separadas dentro de la guía | P1 |
| 11 | `hacer-presupuesto` | Crear, recuperar y convertir; estados y vigencia | P1 |
| 12 | `abrir-y-cerrar-caja` | Apertura, arqueo, faltantes y sobrantes | P0 |
| 13 | `registrar-gastos-y-retiros` | Diferenciar gasto y retiro | P1 |
| 14 | `fabricar-productos-con-recetas` | Insumos, producción y destino | P2 |
| 15 | `crear-y-editar-clientes` | Alta en plena venta y permisos | P1 |
| 16 | `consultar-cuenta-corriente-cliente` | Saldo original/actualizado con números | P1 |
| 17 | `cobrar-deuda-cliente` | Parcial, total y saldo a favor | P1 |
| 18 | `crear-y-editar-proveedores` | Alta, modificación y uso en compras | P1 |
| 19 | `cargar-compra-manual` | Crear, revisar y confirmar | P1 |
| 20 | `cargar-compras-con-foto-ia` | Tutorial estrella; flujo completo y confirmación | P0 |
| 21 | `pagar-proveedor` | Deuda, pago, adelanto y estado de cuenta | P1 |
| 22 | `cargar-listas-precios-proveedores` | Formatos, asociación y comparación | P1 |
| 23 | `contar-stock` | Conteo por depósito y vista previa; lápiz como atajo | P0 |
| 24 | `ajustar-stock-mermas-transferencias` | Guía de referencia; entradas claras por intención | P0 |
| 25 | `actualizar-precios-y-rentabilidad` | Margen vs recargo, actualización y verificación | P1 |
| 26 | `crear-ofertas-y-promociones` | Requisito y complemento de revistas | P0 |
| 27 | `crear-revista-ofertas` | Tutorial estrella; resultado exportado y compartido | P0 |
| 28 | `imprimir-etiquetas` | Formato, impresora y prueba | P1 |
| 29 | `configurar-tienda-online` | Activación, catálogo y comprobación pública | P1 |
| 30 | `usar-app-del-dueno` | Acceso y tareas; capítulos anclados por función | P2 |
| 31 | `consultar-reportes-y-exportar` | Consultar, filtrar, costos y exportación | P2 |
| 32 | `controlar-turnos-caja-panel` | Supervisión del dueño | P2 |
| 33 | `billeteras-y-cuentas` | Saldos, transferencias y ajustes | P2 |

Guías nuevas obligatorias, aún sin tutorial equivalente completo en esos 32 archivos:

| Slug | Objetivo | Evidencia y trabajo pendiente |
|---|---|---|
| `importar-productos-excel` | Pasar catálogo, costos y precios de Excel al sistema | Existe importador; verificar pantalla, plantilla y efecto de actualizar registros |
| `cargar-stock-inicial-excel` | Cargar existencias por depósito | Existe importación de ajustes; validar si cantidades representan diferencia o existencia final |
| `modificar-stock-producto` | Resolver “tengo 12, figura 9” | Derivar de 23–24; ejemplo simple y enlace al conteo |
| `configurar-compras-con-ia` | Habilitar módulo, proveedor y límites | Extraer de 20; revisar condiciones de consumo y no publicar claves |
| `resolver-errores-compras-ia` | Totales, asociaciones y pendientes | Extraer problemas de 20, con pasos verificables |
| `compartir-revista-whatsapp-instagram` | Elegir formato y entregar pieza | Derivar de 27; distinguir compartir archivo, enlace y subida a red |
| `instalar-adestock` | Descargar e iniciar correctamente | Operación pendiente: verificar versión/instalador |
| `configurar-impresora-tickets` | PDF, agente local y prueba | Validar documentación de impresión vigente |
| `hacer-copia-de-seguridad` | Guardar y verificar recuperación | Capturas y procedimiento pendientes |

Las derivadas cortas solo tendrán URL propia si resuelven una intención completa y diferente. Si repiten casi todo, usar una sección con ancla en la guía principal. No multiplicar páginas cambiando sinónimos.

## 8. Excel: primera prioridad de aprendizaje

La pregunta “cómo cargar stock en Excel” puede significar preparar una planilla, importar productos, cargar existencias o exportar para contar. El buscador y la página `/funciones/productos-y-excel/` deben presentar esas opciones con ejemplos claros.

Hallazgo del código: `producto/inventario_excel.py:import_inventario_excel` importa productos, costo, cantidad base y precios. El fragmento revisado no demuestra carga de stock por depósito. La `cantidad` del producto se usa en costo/presentación; no llamarla “stock”. El importador busca producto por ID o código y elimina sus precios existentes antes de recrearlos. Hay análisis previo en `analyze_inventario_excel` y un flujo en `adestock/admin_override.py`; comprobar su comportamiento completo antes de enseñarlo.

Existe otra vía en `producto/admin.py`, ajustes de inventario con Excel y plantilla: revisar signos, unidades, depósito, estados y aplicación. La web debe mostrar **importar catálogo** y **cargar/corregir existencias** como tareas diferentes.

Capturas mínimas para publicar las guías de Excel:

1. Acceso real a descargar plantilla.
2. Planilla con tres productos ficticios y columnas reales.
3. Código de barras como texto, preservando ceros iniciales.
4. Diferencia entre unidades del bulto, costo del bulto y existencias.
5. Selección de archivo y análisis/vista previa real si existe.
6. Ejemplo de validación fallida y cómo corregirlo.
7. Confirmación de importación y resumen de cambios.
8. Catálogo y precios después de importar.
9. Para existencias: depósito, ajuste pendiente, aplicación y stock antes/después.

Ofrecer una plantilla vigente y ejemplo descargable, generado desde la estructura real. Explicar qué ocurre si se importa dos veces, cómo se identifica un producto existente y qué campos se reemplazan. No prometer una importación universal de cualquier Excel ni reversión automática si no existe.

## 9. Compras con foto e IA: demostración y tutorial estrella

Página comercial: “Cargá tus compras con una foto de la boleta”. Describir ayuda para leer renglones y asociar productos; siempre revisar antes de confirmar. No confundir con generación de fotos de productos.

Tutorial principal con respuesta inicial de dos o tres frases y pasos:

1. Verificar módulo, permisos y configuración de IA, con enlace a preparación.
2. Fotografiar la boleta completa, derecha y legible o elegir archivo admitido.
3. Subir y procesar; explicar progreso y precargas pendientes.
4. Elegir o crear proveedor y revisar alias.
5. Revisar IVA, pago y flete sin convertir la guía en asesoramiento fiscal.
6. Asociar productos, revisar sugerencias y crear los que faltan.
7. Comparar cantidades, precios y total con el documento original.
8. Crear la compra pendiente.
9. Confirmarla en el panel: destacar este paso en el resumen inicial y final.
10. Verificar stock, costo y pago/deuda.
11. Mostrar una segunda boleta y qué asociaciones recuerda por proveedor.

Orden visual: foto original ficticia → lectura → corrección → resumen → pendiente → confirmada → efecto. Reutilizar selectivamente las 29 imágenes disponibles del flujo; cada imagen debe explicar algo. Flete, alias y configuración avanzada tendrán secciones colapsables o guías complementarias, siempre presentes en HTML.

Mensajes y tips: “Revisá la cantidad y el precio antes de confirmar”, “Crear la compra todavía no aumenta el stock”, “Un alias incorrecto puede repetirse en próximas boletas”. Transcribir mensajes reales de la interfaz y explicar acción siguiente. No repetir costos orientativos de IA sin fecha, modelo y condiciones comprobadas; la documentación menciona API key propia, que debe contrastarse con la oferta comercial vigente.

## 10. Revistas de ofertas: segundo diferencial comercial

Página comercial: “Creá una revista de ofertas con tus productos y precios”. Mostrar A4 y una versión para redes con productos de demostración.

Tutorial principal:

1. Activar módulo y revisar permiso.
2. Abrir “Revistas y folletos” y crear publicación.
3. Elegir formato: A4 para impresión, cuadrado/vertical/historia para redes.
4. Elegir tema y cantidad de productos por página.
5. Seleccionar vigencia y traer ofertas o agregar del catálogo.
6. Revisar presentaciones, precios y leyendas de promoción.
7. Ajustar fotos, encuadre, fondo y tamaño de productos destacados.
8. Revisar logo, título, fechas y pie comercial.
9. Guardar y publicar; distinguir estado interno de disponibilidad online.
10. Exportar PDF/PNG o compartir enlace/archivo según el canal.
11. Verificar el archivo y el enlace desde celular.
12. Duplicar para la próxima semana y revisar fechas/precios.

Reutilizar las 10 capturas existentes cuando correspondan. Añadir capturas del archivo final, la pieza para redes y el resultado de compartir, si no están cubiertas. Aclarar que editar la foto en una publicación no modifica la foto del catálogo, según el flujo documentado. Verificar permisos y acceso público de “Online” antes de prometer un enlace sin autenticación.

El tutorial debe terminar con algo que el comerciante pueda mostrar: la revista terminada. No afirmar que el sistema publica automáticamente en Instagram si solo exporta o abre una opción para compartir.

## 11. Plantilla editorial de todos los tutoriales

1. Título como acción: “Cómo cargar productos desde Excel en ADEstock”.
2. Respuesta breve: qué se logra y por dónde empezar.
3. Rol, permiso, módulo, versión, fecha de verificación y tiempo orientativo.
4. Requisitos y enlaces de preparación.
5. Resumen rápido de 3–6 pasos; índice con anclas.
6. Paso a paso con botones reales, capturas y resultado esperado por paso.
7. “Antes de confirmar” para operaciones que cambian datos.
8. “Cómo comprobar que salió bien”, con stock/caja/deuda según corresponda.
9. Errores frecuentes: mensaje literal, causa probable y acción concreta.
10. Tips pertinentes: unidades, presentación, permisos y límites.
11. Ejemplo realista con datos ficticios.
12. Siguiente tarea y hasta tres relacionados.
13. “¿Te sirvió?” y acceso a ayuda que indique tutorial y versión.

Cada captura usa `figure`, texto alternativo descriptivo y pie; los números y flechas tienen equivalencia textual. La imagen se puede ampliar con teclado y móvil. El video es opcional, carga al hacer clic y tiene resumen/transcripción; el usuario puede completar la tarea leyendo.

Reglas de producción de capturas: ambiente demo, datos ficticios, sin claves ni documentos de clientes; estado consistente entre pasos; conservar original y anotación reproducible; verificar nitidez del texto a tamaño móvil; evitar depender solo de rojo/verde. No regenerar todas las capturas hasta revisar las existentes.

Metadatos obligatorios del contenido:

```yaml
id: compras-foto-ia
slug: cargar-compras-con-foto-ia
title: Cómo cargar una compra con foto e IA en ADEstock
description: Leé una boleta con IA, revisá productos y totales, y confirmá la compra para actualizar stock y costos.
category: compras-proveedores
roles: [dueno, administrativo]
surface: [pos, panel]
status: draft
source_path: 01-manual-usuario/20-comprar-con-foto-ocr.md
source_hash: pendiente
product_version: pendiente-verificar
verified_at: 2026-10-12
reviewed_at: null
synonyms: [boleta, factura proveedor, cargar compra, foto factura, OCR]
related: [cargar-compra-manual, pagar-proveedor]
social_image: /social/cargar-compras-con-foto-ia.jpg
```

El build debe rechazar contenido `published` sin requisitos, revisión, imágenes válidas, enlaces resueltos y versión comprobada. `verified_at` del origen no convierte automáticamente `reviewed_at` en aprobado.

## 12. Búsqueda tipo RAG sin IA generativa

Decisión: índice local por fragmentos de contenido generado durante el build, implementado inicialmente con MiniSearch y un diccionario editorial de sinónimos. Elegir dependencia/versionar al implementar; la búsqueda funciona en el navegador y devuelve extractos reales con enlaces al encabezado.

Experiencia:

- Escribir una pregunta: “cómo cargo una factura con la cámara”.
- Ver “Cargar una compra con foto e IA”, extracto corto y enlace al paso de la foto.
- Filtrar por tarea, rol o POS/Panel/App.
- Abrir el paso exacto; el enlace completo sigue siendo un tutorial indexable.
- Si hay ambigüedad, ofrecer opciones: “¿Querés importar productos o cargar existencias?”.
- Si no hay resultados, sugerir tareas cercanas y contacto. Nunca inventar una respuesta.

Modelo de fragmento: `id`, `tutorial_id`, `url`, `heading_id`, `title`, `heading`, `text`, `keywords`, `synonyms`, `role`, `surface`, `version`, `verified_at`. Dividir por H2/H3 en pasajes con sentido, aproximadamente 100–250 palabras; conservar listas completas y evitar separar mensaje de error de su solución. Deduplicar resultados del mismo tutorial y ofrecer hasta tres pasos relevantes.

Normalizar mayúsculas y tildes, tolerar errores moderados y priorizar coincidencia exacta antes de coincidencia difusa. Ponderación inicial configurable: título 6, encabezado 4, palabras clave 3, texto 1; coincidencia de frase exacta suma prioridad. No son valores universales: ajustar usando consultas de prueba.

| Consulta cotidiana | Expansión/intención | Destino esperado |
|---|---|---|
| “cargar stock excel” | Excel + existencias; también catálogo | Dos opciones explícitas, stock inicial primero |
| “subir productos de planilla” | importar catálogo Excel | Importar productos |
| “tengo 12 pero dice 9” | corregir existencias | Modificar stock / conteo |
| “me quedó mal el stock” | ajuste, conteo, depósito | Corregir stock |
| “foto de factura” | compra foto, boleta, OCR | Compras con IA |
| “la compra no sumó stock” | compra pendiente | Confirmar compra, ancla exacta |
| “hacer folleto ofertas” | revista, catálogo promocional | Crear revista |
| “mandar ofertas por wasap” | WhatsApp, revista, compartir | Compartir revista |
| “cobrar mitad efectivo mitad tarjeta” | pagos combinados | Varios medios de pago |
| “fiar / fiado” | cuenta corriente | Vender fiado |
| “no veo el lápiz” | permiso modificar stock | Requisitos de corrección de stock |
| “lista proveedor excel” | precios ofrecidos, no stock | Listas de proveedores |

La respuesta destacada, si se muestra, será un extracto editorial identificable: “En este tutorial”, con fuente, fecha y enlace. No presentar el buscador como un asesor que comprende cualquier pregunta. Mantener el catálogo navegable sin buscador y un índice de categorías en HTML.

Aceptación: preparar 30 consultas reales antes de implementar; ≥90% de consultas con respuesta existente deben mostrar el tutorial correcto entre los tres primeros; las diez consultas críticas deben acertar el primer resultado o mostrar desambiguación correcta. Medir cero resultados y retorno al buscador. Objetivo de interacción tras cargar el índice: respuesta visible <200 ms en equipo de gama media; medir antes de considerar logrado.

## 13. Mapa SEO: una intención por página

Estas son hipótesis de búsqueda y lenguaje de clientes, no volúmenes ni posiciones medidos. Validar con Search Console y, cuando esté disponible, Keyword Planner o una fuente de datos SEO. No elegir competidores ni oportunidades por cifras inventadas.

| Grupo | Frases de trabajo | Página principal | Apoyo |
|---|---|---|---|
| Categoría | sistema de stock, software de inventario para comercios | `/sistema-de-stock/` | Home y rubros |
| Control | control de stock, ajustar inventario, contar mercadería | `/control-de-stock/` | Tutoriales de conteo y ajustes |
| Excel | importar productos desde Excel, cargar stock inicial Excel | `/funciones/productos-y-excel/` | Dos tutoriales distintos |
| Ventas | punto de venta para comercio, cómo hacer una venta | `/funciones/punto-de-venta/` | Primera venta y cobro |
| IA | cargar compras con foto, leer boletas con IA, OCR facturas proveedor | `/funciones/compras-con-ia/` | Tutorial completo y errores |
| Revistas | crear revista de ofertas, folleto supermercado, catálogo ofertas WhatsApp | `/funciones/revistas-y-folletos/` | Crear y compartir revista |
| Rubros | sistema stock kiosco, almacén, minimarket | URL existente de cada rubro | Caso con productos y circuito propio |
| Marca | ADEstock tutoriales, precios ADEstock, demo ADEstock | Ayuda, precios y demo | Navegación coherente |

Una página comercial responde “para qué sirve y por qué elegirlo”; una guía responde “cómo hacerlo”; un artículo responde un problema general del negocio. Compartir términos es natural si la intención es diferente. Evitar varias landings idénticas para “inventario”, “stock” y “control” sin aporte real.

Enlaces internos: comercial → tutorial relacionado → función pertinente; tutorial → requisito → paso siguiente; blog → función y tutorial realmente útiles. Usar textos descriptivos. Todos los tutoriales publicados deben ser accesibles por enlaces HTML desde el centro o su categoría, además del buscador.

Primera investigación competitiva pendiente: tomar cinco competidores que aparezcan en búsquedas argentinas de categoría, comparar propuesta, planes, tutoriales y demos; registrar URL, fecha y evidencia. No crear páginas de comparación nominal sin verificación actual de sus funciones y precios.

## 14. SEO técnico y metadatos

- HTML completo con H1 único editorial, jerarquía H2/H3 lógica, contenido visible y enlaces `a href` reales.
- Título y descripción únicos alineados con la tarea. Longitudes orientativas, no reglas rígidas: título claro y conciso, descripción que explique el resultado; revisar presentación real.
- Canonical absoluto coherente con URL final, HTTPS y un único host; normalización de slash/HTML según la ruta existente.
- Respuestas 200 para contenido válido, 301/308 para migraciones y 404/410 para eliminado sin equivalente. Evitar devolver home con 200 para cualquier ruta.
- Sitemap generado con solo canónicas públicas, indexables y 200; `lastmod` de cambios significativos reales. Dividir por tipo solo si aporta gestión.
- Robots debe permitir HTML, CSS, JS e imágenes públicas. `robots.txt` no protege contenido privado y bloquear una ruta no equivale a desindexarla.
- Búsqueda, filtros, borradores, páginas de éxito y callbacks fuera de sitemap y con `noindex` cuando sean HTML públicos apropiados; probar callbacks antes de tocar headers o rutas.
- Sin parámetros que creen cientos de páginas indexables de filtros; UTM no cambia canonical ni contenido.
- Revisar enlaces rotos, anclas, textos alternativos, migas y paginación real.
- Mantener `llms.txt` como índice complementario actualizado; no usarlo como garantía de indexación ni de aparición en respuestas de IA.
- Evitar carga masiva de páginas delgadas, texto oculto para bots, keyword stuffing o backlinks comprados como estrategia.

Datos estructurados:

| Página | Marcado elegido | Regla |
|---|---|---|
| Sitio | Organization + WebSite con IDs estables | Identidad y datos reales |
| Producto | SoftwareApplication | Plataforma y oferta coherentes con lo visible |
| Precios | Offer cuando exista precio público real | Número, moneda y condiciones correctas; nunca `price: Consultar` |
| Tutorial | TechArticle + BreadcrumbList | Autor/revisor, fechas y versión comprobables |
| Blog | BlogPosting + BreadcrumbList | Autoría y fechas reales |
| Video propio publicado | VideoObject cuando tenga datos completos | Miniatura, título y fechas verificados |

No inventar reseñas ni puntuaciones para completar requisitos de rich results. Un precio 0 corresponde únicamente a una oferta realmente gratuita definida; una demo temporal no convierte al producto entero en gratis. FAQs y pasos existen por utilidad; no basar la estrategia en resultados enriquecidos FAQ/HowTo. Verificar soporte vigente en la documentación oficial al implementar y validar tipos admitidos.

## 15. Redes, WhatsApp y vistas previas

Cada página pública debe entregar metadatos en su HTML original: `og:title`, `og:description`, `og:type`, `og:url`, `og:image`, dimensiones, `og:image:alt`, `og:site_name` y `og:locale=es_AR`; tarjeta X con `twitter:card=summary_large_image` y campos coherentes. Usar tipo article cuando corresponda.

Crear tarjeta específica por tutorial prioritario: título corto, marca y captura/resultados legibles. Tamaño de diseño inicial 1200×630; comprobar recortes reales. Publicar JPG o PNG para las tarjetas sociales y WebP para la web; son usos diferentes.

La URL de imagen debe ser absoluta HTTPS, pública, estable, con Content-Type correcto y accesible sin cookies ni autenticación. Evitar metadatos insertados solo por JS. Probar home, Excel, venta, stock, IA y revista en depurador de Meta y compartiendo desde WhatsApp, Instagram y X cuando corresponda. Registrar qué se muestra realmente; ninguna etiqueta garantiza idéntica presentación en todas las redes.

Al cambiar una tarjeta, usar versión en el nombre del archivo y refrescar caché donde la plataforma lo permita. Botón “Copiar enlace a este paso” para soporte; al compartir ese enlace, la tarjeta corresponde al tutorial, no necesariamente a su ancla.

## 16. Imágenes y rendimiento

Conservar capturas PNG originales como fuente. Generar WebP sin pérdida para interfaces con texto; comparar tamaño y nitidez antes de adoptarlo. Si WebP no reduce peso, conservar PNG optimizado. Para fotos, probar WebP con pérdida moderada; AVIF es opcional si la mejora compensa procesamiento y compatibilidad.

Logos e iconos: SVG optimizado cuando corresponda; no convertirlos automáticamente a bitmap. Las capturas no necesitan duplicarse en PNG público solo por costumbre: usar fallback si el soporte requerido lo justifica. JPG/PNG se mantienen para social y entregables del cliente cuando sean el formato adecuado.

Generar variantes responsive sin reducir tanto que el texto sea ilegible; ejemplo de anchos iniciales 640, 960 y 1440, según la imagen. Declarar `width`, `height`, `srcset` y `sizes`; lazy loading bajo el primer pliegue. Imagen principal visible sin lazy, con prioridad solo cuando se identifique como LCP. Ampliación puede cargar la variante de mayor detalle a demanda.

El inventario encontró un GIF de aproximadamente 17,5 MiB en la web: verificar uso; si aparece, evaluar reemplazo por video liviano con poster o secuencia de capturas. No borrar sin rastrear referencias.

Presupuestos de trabajo: página comercial inicial <1 MiB transferido sin video ni descargas opcionales; JS propio inicial <100 KiB gzip; índice inicial de búsqueda objetivo <300 KiB gzip, cargar al interactuar y dividir por categoría si crece. Son presupuestos internos, no factores de ranking aislados.

Objetivos de campo al percentil 75: LCP ≤2,5 s, INP ≤200 ms, CLS ≤0,1. Medir móvil y desktop por separado; resultados de laboratorio ayudan a depurar y no sustituyen datos de usuarios. Cargar video al hacer clic, reducir fuentes y scripts externos y revisar contraste/tamaño de objetivos táctiles.

## 17. Métricas y conversiones

Conservar la propiedad GA4 identificada hasta confirmar titularidad y configuración. Elegir una sola vía de instrumentación (directa o gestor de etiquetas) y evitar duplicación. Revisar privacidad y configuración de consentimiento aplicable antes de activar etiquetas publicitarias; no copiar datos personales a eventos.

| Evento | Disparador | Parámetros útiles | Uso |
|---|---|---|---|
| `view_tutorial` | Tutorial cargado | tutorial_id, category, product_version | Consumo |
| `search` | Consulta enviada | search_term saneado/limitado | Búsquedas; no enviar texto libre sensible |
| `help_search_results` | Resultados mostrados | result_count, query_group | Cero resultados |
| `help_search_select` | Abre resultado | tutorial_id, rank, heading_id | Relevancia |
| `tutorial_step_view` | Paso clave realmente visible | tutorial_id, step_id | Diagnóstico de abandono |
| `tutorial_feedback` | Sí/no “¿Te sirvió?” | tutorial_id, helpful | Calidad percibida |
| `file_download` | Descarga de plantilla/instalador | file_name, file_type, tutorial_id | Microconversión; deduplicar medición automática |
| `click_whatsapp` | Clic hacia WhatsApp | placement, page_type, topic | Intención; no equivale a consulta recibida |
| `generate_lead` | Formulario aceptado realmente | form_id, lead_type | Conversión principal |
| `share` | Acción de compartir | method, content_type, item_id | Uso de recursos |
| `trial_start` | Alta real de prueba, si se integra | source, product_version | Conversión verificada; no inferir de descarga |

No llamar “tutorial completado” a llegar al final de la página; no conocemos si ejecutó la tarea. No enviar nombres, emails, CUIT, claves ni texto de boletas. En el buscador, preferir grupos de intención y consultas anonimizadas; si no se puede sanear bien, omitir término libre.

Panel mensual: impresiones y clics orgánicos no marcarios; CTR por consulta/página; canónicas indexadas frente a elegibles; contactos y pruebas por canal; costo por lead calificado en Ads; uso del buscador, tasa de cero resultados y feedback; problemas de CWV. Segmentar prospectos y usuarios de ayuda con señales voluntarias o contexto, sin asumir identidad.

Línea de base: obtener 28 días y 90 días cuando existan en Search Console/GA4. Registrar fecha de migración y comparar períodos equivalentes, estacionalidad y tráfico de marca. Metas de los primeros 30 días: instrumentación verificada, todos los tutoriales P0 accesibles, cero enlaces internos rotos y búsqueda evaluada. Metas de tráfico y leads se fijan tras conocer la base.

## 18. SEM: adquisición con intención comercial

Preparar campañas y landing pages después de comprobar conversiones; este plan no activa campañas ni fija gasto sin presupuesto.

Grupos iniciales: marca ADEstock; sistema de stock para comercios; rubros prioritarios; compras con IA; revistas/folletos para negocios como experimento aparte. Cada anuncio lleva a la página que demuestra esa promesa, con CTA y tutorial de apoyo.

Excel y “cómo hacer una venta” pueden atraer personas que solo necesitan aprender: atenderlas orgánicamente primero. Para Ads, probar consultas de intención comercial y concordancias controladas; revisar términos reales antes de ampliar. Negativas iniciales a evaluar: empleo, sueldo, crack, serial, bolsa/acciones; “gratis”, “Excel” y “tutorial” requieren criterio por campaña y no exclusión global automática.

Usar UTM estables para redes y campañas externas; en Google Ads conservar autoetiquetado cuando esté configurado. No poner UTM en enlaces internos. Diferenciar clic en WhatsApp de lead calificado; vincular información posterior de ventas solo con un proceso autorizado y comprobable. Probar dos propuestas por grupo y decidir por leads calificados, no solo CTR.

## 19. Migración y retiro de tutoriales viejos

Antes de editar: capturar inventario URL → estado → title → canonical → enlaces → destino → decisión. Exportar Search Console y métricas si hay acceso; si no, registrar la limitación y conservar las URLs con mayor cautela. Guardar snapshot Git/backup y una copia de los recursos operativos.

| Contenido actual | Decisión prevista |
|---|---|
| `/tutoriales.html` | Migrar a `/tutoriales/`; compatibilidad con anclas antiguas |
| Anclas `#t1-onboarding`, `#t7-ventas`, etc. | Un servidor no recibe fragmentos; conservar una página puente legible con enlaces y un mapeo JS opcional a nuevas URLs, sin depender de JS para encontrar la guía |
| JSON antiguo de capítulos | Archivar al completar reemplazos; quitar referencias y renderer viejo |
| `/control-de-inventarios/` | Candidata a consolidar en `/control-de-stock/` si no tiene intención/contenido distintivos; revisar métricas antes de redirigir |
| `/software-de-inventario-argentina/` | Evaluar consolidación en `/sistema-de-stock/` con evidencia de consultas |
| Casos de uso existentes | Conservar o integrar por equivalencia; distribuidora belleza requiere destino propio o mantener hasta tenerlo |
| Manuales funcionales públicos | Mapear a ayuda vigente y migrar por tema; no enviar todos a home |
| Changelog técnico público | Extraer novedades útiles; revisar enlaces externos antes de retirar |
| API temas, ZIP, firmas, callback OAuth, vinculaciones | Preservar contratos, rutas y funcionamiento |

Para anclas antiguas, opción concreta: mantener `/tutoriales.html` como puente `noindex` con enlaces completos a todos los destinos antiguos y mapeo de `location.hash`; canonical hacia el centro nuevo. La URL base puede migrarse más adelante con 301 cuando se acepte perder el salto específico de bookmarks. Documentar esa excepción: no prometer que una 301 puede distinguir fragmentos. Evitar bloquear la página puente en robots si necesita procesarse su `noindex`.

En hosting con soporte real, aplicar redirecciones permanentes de un salto para el resto de URLs renombradas. Si producción es GitHub Pages, verificar limitaciones de redirección HTTP y decidir conservar rutas o habilitar una capa que soporte redirecciones; no asumir que `_redirects` funciona allí. Mantener redirecciones al menos un año y preferiblemente indefinidas. Actualizar enlaces internos a destino final.

Archivar tutoriales antiguos en el repositorio, fuera del artefacto público, cuando exista cobertura vigente y mapeo. Un tema todavía no reemplazado se revisa y mantiene temporalmente o se retira honestamente; no publicar instrucciones obsoletas bajo una etiqueta “actual”. No reemplazar todo el centro por “próximamente”.

## 20. Ejecución por fases y condiciones de avance

| Fase | Trabajo y entregable | Condición de cierre |
|---|---|---|
| 0 · Inventario | Rutas, dependencias, hosting, fuentes, contratos, línea de base | Inventario y mapa de migración revisables; backup recuperable |
| 1 · Reorganización | Estructura del repo, pipeline estático, plantillas, manifiesto editorial | Build reproducible; fuentes internas fuera de público |
| 2 · Base SEO y ayuda | Centro, categorías, plantilla, canonical/schema/social y buscador piloto | Todo el contenido principal en HTML; enlaces y búsqueda funcionan |
| 3 · Circuito inicial | Configuración → productos/Excel → stock → venta → caja | Persona de prueba completa el circuito con datos demo |
| 4 · Diferenciales | Compras con foto/IA y revistas, páginas comerciales y capturas finales | Compra confirmada y revista exportada, resultados comprobados |
| 5 · Resto de guías | Publicar P1 y P2 una por una | Cada guía supera QA editorial, funcional, visual y SEO |
| 6 · Renovación comercial | Home, rubros, precios, demo, blog y navegación | Promesas coherentes con producto y rutas internas completas |
| 7 · Migración pública | Redirecciones, sitemap, previews, analítica y comprobación de despliegue | Sin errores críticos; checklist de publicación cumplido |
| 8 · Mejora continua | Consultas, búsquedas fallidas, leads y rendimiento | Revisión semanal inicial; luego mensual según volumen |

Orden de publicación de tutoriales: primero configurar negocio, importar/cargar productos, cargar stock inicial, hacer venta, corregir/contar stock y abrir/cerrar caja; después compra con IA y revista, sin relegarlas al final de los 32 manuales. Las dependencias mínimas de esos dos flujos se publican antes o junto a ellos. Producir y validar una guía a la vez.

No fijar fecha de lanzamiento sin verificar alcance de capturas y capacidad de revisión. La secuencia es vinculante; el calendario se define al cerrar inventario. Un cambio de hosting o configuración comercial pendiente debe quedar como dependencia explícita, no resolverse por suposición.

## 21. Checklist de aceptación de publicación

### Contenido y tutoriales

- [ ] Las cinco entradas prioritarias se encuentran desde home y centro de ayuda.
- [ ] Cada tutorial publicado tiene fuente, versión, revisión, capturas legibles y resultado comprobable.
- [ ] Excel separa catálogo/precios de existencias por depósito.
- [ ] IA distingue procesar, crear pendiente y confirmar compra.
- [ ] Revistas muestra pieza final y diferencia exportar de publicar en una red.
- [ ] No hay tutoriales vacíos, imágenes faltantes, pasos inventados ni instrucciones técnicas internas expuestas.
- [ ] Una persona que no conoce el sistema realiza los cinco flujos prioritarios; registrar dónde se trabó y corregir.

### Técnica, SEO y social

- [ ] HTML sin JS contiene texto, enlaces, metadata y JSON-LD coherente.
- [ ] Sitemap incluye únicamente canónicas 200 indexables; robots no bloquea recursos necesarios.
- [ ] URLs eliminadas o movidas tienen decisión y respuesta HTTP correcta; página puente de anclas comprobada.
- [ ] No se alteraron paquetes firmados/API, OAuth, agente ni enlaces de descarga necesarios.
- [ ] Metadatos y tarjetas de las seis páginas prioritarias se comprobaron con herramientas y compartidos reales.
- [ ] Navegación, foco, buscador, filtros y ampliación funcionan con teclado y a 360 px.
- [ ] Laboratorio de rendimiento revisado; datos de campo anotados como disponibles o pendientes.
- [ ] Search Console: verificar propiedad, enviar sitemap e inspeccionar home y páginas P0 tras publicar; registrar canónica elegida y errores. La selección final de indexación corresponde a Google.

### Búsqueda y medición

- [ ] Las 30 preguntas de evaluación tienen resultado esperado y resultado obtenido.
- [ ] Consultas críticas aciertan o desambiguan; se resuelven cero resultados con navegación útil.
- [ ] Eventos recibidos una sola vez y conversiones de formulario solo tras aceptación real.
- [ ] WhatsApp/descargas se presentan como señales de intención, no clientes confirmados.
- [ ] No se envían datos personales en consultas ni parámetros.
- [ ] Tablero muestra línea de base y fecha de migración; no se atribuye crecimiento sin evidencia.

## 22. Mantenimiento y entregables concretos

Entregables de implementación: inventario y CSV de migraciones; proyecto estático y componentes; manifiesto de 32 guías más nuevas; cinco flujos prioritarios completos; índice local y banco de 30 consultas; catálogo de capturas y derivados; tarjetas sociales; sitemap/robots/schema; plan de eventos con verificación; registro de QA y procedimiento de despliegue/rollback.

Responsabilidades: desarrollo verifica comportamiento y build; edición revisa lenguaje/capturas; responsable del negocio confirma planes, versión comercial y promesas; persona de prueba valida comprensión. Una persona puede asumir varios roles, pero las verificaciones quedan registradas.

Ante cada release: comparar huellas de fuentes; marcar guías afectadas; actualizar texto, capturas y búsqueda; revisar precios/promesas; publicar con fecha real; comprobar enlaces y flujos afectados. Revisar semanalmente consultas sin resultado al inicio; mensualmente rendimiento orgánico, leads y piezas compartidas. No actualizar fechas de todos los tutoriales si no fueron revisados.

## 23. Referencias oficiales consultadas

Consultadas el 12/10/2026. Revalidar al implementar, especialmente soporte de resultados enriquecidos y requisitos publicitarios.

- [Google: JavaScript SEO](https://developers.google.com/search/docs/crawling-indexing/javascript/javascript-seo-basics). Fundamenta HTML completo, enlaces rastreables y metadatos consistentes.
- [Google: migraciones de URLs](https://developers.google.com/search/docs/crawling-indexing/site-move-with-url-changes). Fundamenta mapa de destinos y seguimiento de migración.
- [Google: contenido útil](https://developers.google.com/search/docs/fundamentals/creating-helpful-content). Fundamenta tutoriales originales orientados a resolver tareas.
- [Google: SoftwareApplication](https://developers.google.com/search/docs/appearance/structured-data/software-app). Verificar requisitos de ofertas y elegibilidad sin inventar reseñas.
- [Google: novedades de documentación](https://developers.google.com/search/updates). Verificar cambios de soporte de rich results; la antigua URL de FAQ redirigió aquí en la consulta.
- [Open Graph](https://ogp.me/). Campos y objetos para vistas previas compartidas.
- [web.dev: WebP](https://web.dev/learn/images/webp). Opciones de compresión con y sin pérdida.
- [web.dev: Web Vitals](https://web.dev/articles/vitals). Métricas y umbrales de experiencia de usuarios.
- [Google Analytics: eventos recomendados](https://support.google.com/analytics/answer/9267735). Base de nomenclatura; los eventos propios se documentan aparte.

Este plan define una web que demuestra, enseña y convierte. La calidad se comprueba con tareas completadas, páginas técnicamente accesibles, búsquedas útiles y resultados comerciales medidos.
