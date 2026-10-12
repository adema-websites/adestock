---
id: "contar-stock"
slug: "contar-stock"
title: "Cómo contar el stock de un depósito"
description: "Contar la mercadería física, comparar con lo que dice el sistema y corregir las diferencias en un solo paso, con registro de quién, cuándo y cuánto."
category: "stock"
priority: "P0"
roles: ["dueno","administrativo"]
surface: ["panel"]
status: "draft"
tiempo: "10 minutos por sector"
necesitas: "el permiso *Puede modificar stock* (el dueño lo tiene siempre)"
para_quien: "dueños y encargados que controlan el inventario"
modulo: "producto (ConteoStock, AjusteInventario), venta (POS)"
permiso: "Puede modificar stock · opcional: Contar sin ver el stock"
source_path: "01-manual-usuario/23-conteo-de-stock.md"
source_hash: "78a70e6ed1520c87ebee08529f6801ce8ae12fbd17777d6f32b398c500e8654c"
product_version: "pendiente-verificar"
verified_at: "2026-10-12"
reviewed_at: null
synonyms: ["conteo","inventario","tengo 12 pero dice 9","diferencias"]
related: []
social_image: "/social/contar-stock-v1.jpg"
---
## Qué vas a lograr

Contar la mercadería física, **comparar con lo que dice el sistema** y **corregir las diferencias** en un solo paso, con registro de quién, cuándo y cuánto.

Hay dos herramientas, según lo que necesites:

| Herramienta | Cuándo usarla |
|---|---|
| **Conteo de stock** (Menú rápido) | Contar **muchos** productos, por categoría, proveedor o depósito |
| **Lápiz** en el producto | Corregir **un** producto al instante |

## Conteo de stock

### 1. Abrí la pantalla

Menú rápido (**F8**) → **Conteo de stock**. Funciona igual desde la PC o el celular.

![Pantalla de conteo](../../assets/tutoriales/23-conteo-stock/01-pantalla-de-conteo.png)

| # | Filtro | Para qué sirve |
|---|---|---|
| 1 | **Buscar** | Por nombre, marca o **código de barras** (podés escanear) |
| 2 | **Categoría** | Contá un sector a la vez: bebidas, limpieza… |
| 3 | **Proveedor** | Contá por proveedor |
| 4 | **Solo sin contar** / **Solo con diferencia** | Para ver qué te falta contar o qué difiere |

También filtrás por unidad de medida y ordenás por nombre, categoría o código.

> **Casillero vacío = no contado:** no se modifica. Podés contar **por partes**, un sector por vez. Para dejar un producto **en cero**, escribí **0**.

### 2. Cargá lo que contaste

Cada fila muestra el **stock del sistema** y un casillero para escribir lo **contado**.

![Cantidades cargadas](../../assets/tutoriales/23-conteo-stock/02-cantidades-cargadas.png)

| # | Elemento | Qué hace |
|---|---|---|
| 1 | **Contado** | Escribís lo que hay realmente |
| 2 | **=** | Atajo: "el sistema está bien" (copia el stock del sistema) |
| 3 | **Diferencia** | Aparece sola: `−2` falta, `+2` sobra, `ok` coincide |

Detalles útiles:

- Se cuenta en la **unidad del producto** (unidades sueltas, no bultos; kilos, litros…). Admite coma decimal.
- Donde dice `+2 comp.` hay mercadería **comprometida** (vendida pero todavía no entregada): sigue físicamente en la góndola, por eso se cuenta igual.
- Abajo ves cuántas **líneas cargadas** tenés. El conteo se guarda como borrador en tu navegador si cerrás sin confirmar.

### 3. Previsualizá

Tocá **Previsualizar**. El sistema te muestra **qué va a cambiar** antes de tocar nada:

![Previsualización](../../assets/tutoriales/23-conteo-stock/03-previsualizacion.png)

| Dato | Qué es |
|---|---|
| **Productos contados / con diferencia** | Cuántos cargaste y cuántos difieren |
| **Sobrante a costo / Faltante a costo** | Lo que valen las diferencias (a costo) |
| **Había / Contado / ± / Queda** | Por producto, el antes y el después |
| *Líneas que coinciden* | No generan movimiento |

Podés agregar **observaciones** (por ejemplo, *Conteo semanal de góndola*). Si algo no cierra, **Volver a contar**.

### 4. Confirmá

Tocá **Confirmar ajuste**.

![Conteo confirmado](../../assets/tutoriales/23-conteo-stock/04-conteo-confirmado.png)

Queda registrado el **conteo** (`CS000002`) y un **ajuste de inventario** por cada depósito con diferencias (`AJ…`), tipo *Corrección por conteo*, con tu usuario, fecha y hora.

## Corregir un producto con el lápiz

En **Explorar** (o *Editar producto*), el modal del producto muestra el **stock físico** del depósito de tu caja con un **lápiz**.

![Producto con lápiz](../../assets/tutoriales/23-conteo-stock/05-modal-producto-con-lapiz.png)

Tocá el lápiz, escribí **cuánto hay** y confirmá:

![Corrección con lápiz](../../assets/tutoriales/23-conteo-stock/06-corregir-con-lapiz.png)

Ves **Sistema / Diferencia / Queda** antes de guardar. La corrección se aplica **al instante** (no hace falta *Actualizar producto*) y queda registrada como *Corrección por conteo*, con un motivo opcional.

> Para otros depósitos o muchos productos a la vez, usá el **Conteo de stock**.

## Conteo a ciegas

Si al usuario se le activa **Contar sin ver el stock** (en *Configuración → Usuarios*), ve la pantalla así:

![Conteo a ciegas](../../assets/tutoriales/23-conteo-stock/07-conteo-a-ciegas.png)

- Aparece la etiqueta **Conteo a ciegas**.
- **No ve** el stock del sistema (ni en la lista, ni en la previsualización, ni con el lápiz), y no tiene el botón **=**.
- Solo escribe lo que contó. Las **diferencias las ve el administrador** en *Ajustes de inventario*.

Es la forma de evitar que el que cuenta "ajuste" lo que ve a lo que dice el sistema.

## Reglas importantes

| Regla | Qué significa |
|---|---|
| Se compara contra el **stock físico** | Lo vendido pero no entregado sigue contando como físico: así no aparecen sobrantes falsos |
| **Siempre corrección**, nunca merma | El conteo corrige; las roturas o vencimientos se registran como mermas aparte |
| Mientras contás se puede seguir vendiendo | El sistema toma una "foto" del stock al cargar la fila y aplica solo la diferencia sobre el stock del momento de confirmar. Si hubo movimientos, la previsualización lo marca |
| Se puede anular | Un ajuste de conteo no se borra: se **anula** desde el panel de administración y el stock vuelve a lo anterior |

## Qué pasa por detrás

| Qué | Detalle |
|---|---|
| Conteo | Se crea un registro con quién contó, cuándo y cuántas líneas |
| Ajuste | Por depósito con diferencias, un ajuste con impacto directo en stock (sin compras virtuales) |
| Producto nuevo | Si cargás stock con el lápiz al crear un producto, queda como stock inicial |
| Seguridad | La confirmación es atómica: o se aplican todas las diferencias o ninguna |

## Problemas frecuentes

| Si te pasa… | Es porque… | Qué hacer |
|---|---|---|
| No veo *Conteo de stock* | Falta el permiso *Puede modificar stock* | Pedíselo al dueño |
| No veo el lápiz | Falta ese permiso, o no abriste el producto en *Editar* | Verificá el permiso y el permiso de gestionar productos |
| Un producto no aparece | No es contable (servicio u horas) o está fusionado | Esos productos no se cuentan |
| Contó otra persona y no puedo ver su diferencia | Conteo a ciegas | El administrador la ve en *Ajustes de inventario* |
| Me equivoqué en un conteo | — | Anulá el ajuste desde el panel de administración |

## Siguiente paso

- Ajustes de inventario, mermas y transferencias entre depósitos
- Gestión de precios
