---
id: "imprimir-etiquetas"
slug: "imprimir-etiquetas"
title: "Cómo imprimir etiquetas de precios y códigos en ADEstock"
description: "Imprimí etiquetas de precios y códigos de barras en ADEstock. Configurá la etiquetadora, seleccioná presentaciones y copias o filtrá productos en oferta."
category: "instalar"
priority: "P1"
roles: ["dueno","administrativo"]
surface: ["panel"]
status: "published"
tiempo: "2 minutos por tanda"
necesitas: "una etiquetadora configurada para tu caja y el permiso Puede imprimir etiquetas"
para_quien: "dueños y encargados"
modulo: "etiquetas (POS → Imprimir etiquetas), print_queue"
permiso: "Puede imprimir etiquetas · etiquetadora configurada para la caja"
source_path: "01-manual-usuario/28-imprimir-etiquetas.md"
source_hash: "b2a35ad1a5c0bfaa611bbc799fdcc18bf1f31fbb9cc6dc047ccf87441257e036"
product_version: "3.0.0"
verified_at: "2026-10-12"
reviewed_at: "2026-10-13"
reviewed_by: "ademasistemas"
synonyms: ["etiquetas","impresora de etiquetas","código de barras"]
related: ["instalar-agente-de-impresion","crear-ofertas-y-promociones","actualizar-precios-y-rentabilidad"]
social_image: "/social/imprimir-etiquetas-v1.jpg"
---
## Para qué sirve

La etiqueta con nombre, precio y código de barras le muestra el precio al cliente y le permite al cajero escanear rápido. Esta guía sirve para imprimirlas para tus productos (o solo para los que están en oferta), eligiendo cuántas copias de cada presentación. Se usa al cargar productos nuevos o cuando cambian los precios.

## Qué vas a lograr

Vas a **imprimir etiquetas de precios en ADEstock** con el nombre del producto y su código de barras, cuando lo tenga cargado. Elegí la presentación, la cantidad de copias y los productos que necesitás etiquetar.

También podés imprimir solo productos con ofertas vigentes. Antes de enviar una tanda, la etiquetadora y el agente de impresión deben estar configurados para tu caja.

## Antes de empezar: configurar la etiquetadora

Cada **caja** tiene su propia etiquetadora, independiente de la impresora de tickets. Si no está configurada, la pantalla te avisa:

![Pantalla sin etiquetadora](../../assets/tutoriales/28-etiquetas/01-pantalla-sin-etiquetadora.png)

> *Tu punto de venta no tiene una etiquetadora configurada. Mientras tanto podés armar la selección, pero no se puede imprimir.*

El dueño la configura en **Menú rápido → Configuración → Etiquetadora** (o en *Panel de administración → Etiquetas → Configuración de etiquetadoras*):

![Configuración de la etiquetadora](../../assets/tutoriales/28-etiquetas/04-config-etiquetadora.png)

| Dato | Qué es |
|---|---|
| **Conexión** | USB (nombre exacto de la impresora en Windows) o Red (IP) |
| **Etiqueta** | Ancho y alto en mm, y resolución (203 o 300 dpi) |
| **Calibración** | Corrimiento horizontal y ajuste de alto, si la etiqueta sale corrida |
| **Al terminar cada etiqueta** | Nada, avanzar a la próxima o avance fijo; y si corta al final de la tanda |
| **Etiqueta de prueba** | Imprime 2 de prueba para verificar el alineado |

> Como el sistema imprime a través del **agente de impresión** de la caja, la caja también necesita su credencial de agente (ver [La configuración del POS](/tutoriales/configurar-punto-de-venta/)).

## Paso a paso

### 1. Abrí Imprimir etiquetas

Menú rápido (**F8**) → **Imprimir etiquetas**.

### 2. Buscá los productos

![Búsqueda](../../assets/tutoriales/28-etiquetas/02-busqueda.png)

Escribí nombre, marca o código. Cada producto muestra **todas sus presentaciones** con su precio (por unidad, por pack de 6…), el precio de **oferta** si tiene (🔥) y su **código de barras**.

> Si un producto **no tiene código de barras**, la etiqueta sale **sin código** (con nombre y precio). Podés darle código desde *Editar producto*, o dejar que el sistema genere uno (*Configuración → Precios y productos → Códigos de barras*).

### 3. Elegí qué imprimir

![Selección](../../assets/tutoriales/28-etiquetas/03-seleccion.png)

| # | Elemento | Qué hace |
|---|---|---|
| 1 | **Buscador** | Por nombre, marca o código |
| 2 | **Solo en oferta** | Muestra únicamente los productos con oferta vigente |
| 3 | **Tildar todos** | Marca todos los resultados |
| 4 | **Copias** | Cuántas etiquetas de esa presentación |
| 5 | **Plantilla** | El diseño de la etiqueta (*Estándar*) |
| 6 | **Imprimir** | Manda la tanda a la etiquetadora |

También podés filtrar por **categoría** y por **proveedor**. **Nada viene tildado**: elegís vos qué imprimir, y abajo ves el total (*N etiqueta(s) · N producto(s)*).

### 4. Imprimí

Tocá **Imprimir**. La tanda se manda al **agente de impresión** de tu caja, que la imprime en la etiquetadora configurada.

## Etiquetas desde las ofertas

En **Ofertas**, cada oferta tiene un botón **Etiquetas** que arma la tanda con los productos de esa oferta (usando la **leyenda** que cargaste, por ejemplo *Hasta agotar stock*).

## Qué pasa por detrás

| Qué | Detalle |
|---|---|
| Cola de impresión | Cada tanda se encola y el agente local la toma y la imprime |
| Código por presentación | Si está activado *Código de barras por presentación*, cada presentación (500 g, 1 kg…) tiene su propio código y al escanearlo entra esa presentación |
| Etiquetadora | Es por caja; la impresora de tickets es otra configuración |
| Ofertas | La etiqueta muestra el precio de oferta y el anterior tachado |

## Problemas frecuentes

| Si te pasa… | Es porque… | Qué hacer |
|---|---|---|
| No veo *Imprimir etiquetas* | Falta el permiso *Puede imprimir etiquetas* | Pedíselo al dueño |
| Dice que no hay etiquetadora | La caja no tiene una configurada | Configuración → Etiquetadora |
| Puedo armar la selección, pero no imprimir | No hay etiquetadora configurada | Configurala antes de enviar la tanda |
| No sale nada | La caja no tiene credencial del agente de impresión, o el agente no está corriendo | Configuración → Impresora de tickets → *Agente de impresión* |
| La segunda etiqueta sale desalineada | Falta calibrar | En *Etiquetadora* usá **Guardar e imprimir 2 de prueba** y ajustá el corrimiento |
| La etiqueta sale sin código | El producto no tiene código de barras | Cargale uno en *Editar producto* |

## Cómo comprobar que salió bien

Revisá una etiqueta impresa antes de enviar una tanda grande: nombre, presentación, precio, código y alineación. Si tiene código de barras, probalo con el lector del POS. Para etiquetas de oferta, comprobá que el precio y la leyenda correspondan a la promoción vigente.

## Siguiente paso

- [instalar Agent Printer para imprimir desde ADEstock](/tutoriales/instalar-agente-de-impresion/)
- [crear ofertas, descuentos y promociones 3×2 en ADEstock](/tutoriales/crear-ofertas-y-promociones/)
- [actualizar precios masivos y márgenes en ADEstock](/tutoriales/actualizar-precios-y-rentabilidad/)
