---
id: "preguntas-frecuentes"
slug: "preguntas-frecuentes"
title: "Preguntas frecuentes y problemas comunes de ADEstock"
description: "Esta página junta, por tema, los problemas que más aparecen. Cada fila indica qué te pasa, por qué y qué hacer, y el tutorial donde está explicado con capturas. Antes…"
orden: 3
status: "draft"
source_path: "05-faq/README.md"
source_hash: "92f43f8ce552be5d332dbc6ca372cec9845b48a44c62b525e12213b00589f3a4"
product_version: "3.0.0"
verified_at: "2026-10-12"
reviewed_at: null
reviewed_by: null
synonyms: ["faq","problemas","errores","qué hago si","no me deja","no funciona"]
social_image: null
---
Esta página junta, por tema, los problemas que más aparecen. Cada fila indica **qué te pasa**, **por qué** y **qué hacer**, y el tutorial donde está explicado con capturas.

> Antes de nada: **si algo salió mal con la plata, no borres ni «arregles» a mano.** Casi todo se corrige con un movimiento que deja rastro (anular, nota de crédito, ajuste).

## Primeros pasos

### Onboarding: la configuración inicial de tu negocio

| Si te pasa… | Es porque… | Qué hacer |
|---|---|---|
| Entro a `/onboarding/` y me manda al POS | El asistente ya se completó | Es lo esperado: ya está configurado. Cambiá cosas desde el engranaje del POS |
| No aparecen los productos de ejemplo apenas termino | La carga corre en segundo plano | Esperá unos segundos y actualizá el POS |
| No elegí rubro | Es opcional para el sistema, pero no se cargan datos de ejemplo | Cargá tus productos a mano |
| Quiero más cajas o depósitos | El asistente solo crea los iniciales | Engranaje ⚙ del POS → Puntos de venta |

→ [Ver el tutorial completo](/tutoriales/configurar-negocio/)

### Cargar tus primeros productos

| Si te pasa… | Es porque… | Qué hacer |
|---|---|---|
| No veo "Crear producto" en el menú | Tu usuario no tiene permiso | Pedile al dueño el permiso *Gestionar productos* |
| No veo el lápiz de stock | Te falta el permiso *Modificar stock* | Pedilo al dueño |
| El precio me da más alto de lo esperado | La rentabilidad es sobre el precio de venta, no sobre el costo | Es lo esperado: 30 % sobre venta ≠ 30 % sobre costo |
| El costo por unidad está mal | Cargaste el costo por unidad en vez del costo del bulto, o el pack | Revisá que el costo sea el del bulto cerrado y el pack las unidades que trae |
| "Cant. Variable" está deshabilitado | La cantidad de esa fila es mayor a 1 | Solo se usa con cantidad = 1 |

→ [Ver el tutorial completo](/tutoriales/cargar-productos/)

### Crear usuarios y asignar permisos

| Si te pasa… | Es porque… | Qué hacer |
|---|---|---|
| "Ya existe un usuario con ese nombre" | El usuario para ingresar está repetido (no distingue mayúsculas) | Elegí otro |
| Las contraseñas no coinciden | Escribiste distinto en los dos campos | Volvé a escribirlas |
| La contraseña es rechazada | Es muy corta, muy común o solo números | Usá una más larga y mezclada |
| El cajero entra pero dice que no tiene caja | No se le asignó punto de venta | Editá el usuario y elegí una caja |
| No puedo activar *Contar sin ver el stock* | El usuario no tiene *Puede modificar stock* | Activá primero ese permiso |
| Quiero eliminar a un empleado | Los usuarios no se borran | Desmarcá *Usuario activo* y guardá |

→ [Ver el tutorial completo](/tutoriales/usuarios-y-permisos/)

### La configuración del POS (el engranaje)

| Si te pasa… | Es porque… | Qué hacer |
|---|---|---|
| No veo "Tu negocio" | Tu usuario no es el dueño | Pedile al dueño que haga el cambio |
| No aparece el botón *Presupuestos* | *Generar presupuestos desde POS* está apagado | Activalo en Ventas y caja y guardá |
| El POS no me deja vender sin stock | *Permitir venta con stock negativo* está apagado | Activalo en Ventas y caja |
| No puedo seguir vendiendo, pide cerrar caja | El turno es de otro día y no se permite operar con él | Cerrá la caja del día anterior, o activá *Permitir operar con turno abierto de otro día* |
| Una opción del Menú rápido no aparece | El módulo está apagado en *Módulos y sistema* o falta un permiso | Revisalo en Módulos y en los permisos del usuario |
| Los tickets no salen | La caja no tiene credencial del agente de impresión | Impresora de tickets → *Crear credencial para esta caja* |

→ [Ver el tutorial completo](/tutoriales/configurar-punto-de-venta/)

## El POS día a día

### Recorrido por el POS: pantalla, atajos y Menú rápido

| Si te pasa… | Es porque… | Qué hacer |
|---|---|---|
| "Debes abrir el turno de caja antes de operar" | No abriste el turno | Ingresá el efectivo inicial y tocá *Abrir Turno* |
| "No tienes una caja asignada" | Tu usuario no tiene punto de venta | Pedile al dueño que te asigne una (Menú rápido → Usuarios) |
| "Has alcanzado el límite de 5 ventas simultáneas" | Tenés abiertas todas las pestañas permitidas | Terminá o vaciá una venta antes de abrir otra |
| No veo la opción *Ofertas* o *Conteo de stock* | Tu usuario no tiene ese permiso | Pedírselo al dueño |

→ [Ver el tutorial completo](/tutoriales/usar-punto-de-venta/)

### Hacer una venta

| Si te pasa… | Es porque… | Qué hacer |
|---|---|---|
| El botón *Cobrar* está apagado | El carrito está vacío | Agregá al menos un producto |
| "Debe abrir la caja para poder cobrar" | No abriste el turno | Ingresá el efectivo inicial y tocá *Abrir Turno* |
| El POS no me deja vender un producto sin stock | El ajuste *Permitir venta con stock negativo* está apagado | El dueño puede activarlo en Configuración → Ventas y caja |
| No puedo cambiar el precio | Tu usuario no tiene *Puede modificar precios* | Pedíselo al dueño |
| No puedo hacer descuento | Falta el permiso *Puede hacer descuentos* | Pedíselo al dueño |
| El botón de cuenta corriente está apagado | El cliente de la venta es *Consumidor Final* o no tiene cuenta corriente | Cambiá el cliente (F9) a uno con cuenta corriente habilitada |

→ [Ver el tutorial completo](/tutoriales/hacer-una-venta/)

### Cobrar con varios medios de pago y aplicar descuentos

| Si te pasa… | Es porque… | Qué hacer |
|---|---|---|
| *Confirmar y cerrar* está apagado | Todavía falta cobrar | Agregá otro pago hasta que el faltante sea $ 0 |
| El panel de descuento no deja escribir | Tu usuario no tiene *Puede hacer descuentos* | Pedíselo al dueño |
| El botón *Cuenta Corriente* está apagado | El cliente es Consumidor Final o no tiene cuenta corriente | Cambiá el cliente (ver *Vender a cuenta corriente*) |
| Cargué un pago por error | - | Quitalo con el tacho y cargalo de nuevo |
| El importe de tarjeta es mayor al total | El medio tiene recargo | Es lo esperado: el recargo se suma al importe de ese medio |

→ [Ver el tutorial completo](/tutoriales/cobrar-con-varios-medios-de-pago/)

### Vender a cuenta corriente (fiado)

| Si te pasa… | Es porque… | Qué hacer |
|---|---|---|
| El botón *Cuenta Corriente* está apagado | El cliente es Consumidor Final, o no tiene cuenta corriente habilitada | Asignale un cliente con CC (F9) o habilitala desde *Gestión de clientes → Editar* |
| No aparece la etiqueta CC en la lista | El cliente no la tiene habilitada | Editá el cliente y tildá *Habilitar Cuenta Corriente* |
| Necesito saber cuánto me debe | - | Ver *Revisar la cuenta corriente de un cliente* |
| El cliente quiere pagar su deuda | - | Ver *Cobrar la deuda de un cliente* |

→ [Ver el tutorial completo](/tutoriales/vender-fiado-cuenta-corriente/)

### Anular una venta y reimprimir tickets

| Si te pasa… | Es porque… | Qué hacer |
|---|---|---|
| "La venta no está en un estado válido para anular" | Está en carrito o ya anulada | Solo se anulan ventas cobradas |
| No veo "Anular Venta" | Tu usuario no tiene permisos sobre Ventas en el panel | Pedíselo al dueño |
| "Abrí un turno de caja para registrar la devolución" | No hay ningún turno abierto y la venta tenía cobros | Abrí un turno desde el POS y anulá de nuevo |
| La venta anulada sigue en el listado | Las ventas anuladas no se borran | Es lo esperado; el estado figura como *anulada* |

→ [Ver el tutorial completo](/tutoriales/anular-venta-y-reimprimir-ticket/)

### Hacer un presupuesto y convertirlo en venta

| Si te pasa… | Es porque… | Qué hacer |
|---|---|---|
| No veo los botones de presupuesto | La función está apagada | El dueño la activa en Configuración → Ventas y caja |
| No puedo cargar el presupuesto al POS | Está vencido o cancelado | Renovalo: se genera uno nuevo con precios actuales |
| El presupuesto salió con precios distintos | Se generó de nuevo al cambiar el carrito | Es lo esperado: toma los precios del momento |
| No encuentro un presupuesto de otro cajero | La opción *Cajeros ven presupuestos de todos* está apagada | El dueño puede activarla |

→ [Ver el tutorial completo](/tutoriales/hacer-presupuesto/)

### Turno de caja: apertura, retiros y cierre con arqueo

| Si te pasa… | Es porque… | Qué hacer |
|---|---|---|
| "No hay un turno de caja abierto para cerrar" | No abriste turno, o ya lo cerraste | Abrí un turno nuevo |
| Me da faltante y no sé por qué | Algún retiro, gasto o cobro no se registró | Revisá en *Ventas anteriores*, *Gastos* y *Retiro de caja* del turno |
| El cierre no imprime | No hay impresora o agente configurado | Menú rápido → Configuración → Impresora de tickets |
| "Hay compras pagadas sin confirmar" al cerrar | Cargaste compras pagadas con dinero u otro medio y nadie las confirmó | Pedile al dueño o a un administrativo que las confirme en el panel (*Compra → Compras → Confirmar compra*) |
| Cerré sin querer | - | Abrí un turno nuevo; el cierre anterior queda registrado |

→ [Ver el tutorial completo](/tutoriales/abrir-y-cerrar-caja/)

### Registrar un gasto y un retiro de caja

| Si te pasa… | Es porque… | Qué hacer |
|---|---|---|
| No veo la opción *Gastos* | Falta el permiso *Puede registrar gastos* | Pedíselo al dueño |
| La lista de categorías está vacía | Todavía no se creó ninguna | Tocá el engranaje y creá las que necesites |
| El medio de pago no aparece | No está habilitado para tu caja | El dueño lo habilita en Configuración → Medios de cobro |
| "El monto debe ser mayor a cero" | Importe vacío o cero | Escribí un monto válido |
| Quiero cargar un gasto o retiro desde el panel de administración | Ya no se puede: solo se registran desde el POS | Registralo desde el POS con el turno abierto |
| El retiro no se refleja en el cierre | Se registró con un medio que no es efectivo | Verificá que el medio sea *Efectivo* |

→ [Ver el tutorial completo](/tutoriales/registrar-gastos-y-retiros/)

### Fábrica: producir productos con receta desde el POS

| Si te pasa… | Es porque… | Qué hacer |
|---|---|---|
| No veo *Fábrica* en el menú | El módulo *Cocina y recetas* está apagado | Activalo en Configuración → Módulos y sistema |
| La receta no aparece | No existe o no está activa | Cargala desde el panel de administración |
| Dice "Stock insuficiente" | Falta algún insumo | Cargá una compra o ajustá el stock del insumo, o fabricá una cantidad menor |
| No encuentro una fabricación terminada | El filtro muestra solo las activas | Tildá *Mostrar fabricadas y canceladas* |

→ [Ver el tutorial completo](/tutoriales/fabricar-productos-con-recetas/)

## Clientes y cuentas corrientes

### Crear y editar clientes

| Si te pasa… | Es porque… | Qué hacer |
|---|---|---|
| El botón de cuenta corriente aparece apagado al cobrar | El cliente de la venta no tiene la cuenta corriente habilitada, o la venta es a Consumidor Final | Cambiá el cliente (F9) y habilitale la cuenta corriente desde *Editar* |
| No encuentro a un cliente | Lo buscás por un dato que no cargaste | Probá con nombre o documento |
| Los iconos de estado de cuenta están apagados | El cliente no tiene cuenta corriente | Habilitala desde *Editar* |

→ [Ver el tutorial completo](/tutoriales/crear-y-editar-clientes/)

### Revisar la cuenta corriente de un cliente

| Si te pasa… | Es porque… | Qué hacer |
|---|---|---|
| El saldo actualizado es igual al normal | Los precios no cambiaron, o bajaron | Es lo esperado: nunca queda por debajo del original |
| Los iconos de estado de cuenta están apagados | El cliente no tiene cuenta corriente habilitada | Habilitala en *Editar cliente* |
| Hay diferencia entre este saldo y el ticket | El ticket muestra el saldo normal (deuda real) | Para ver el actualizado, generá el PDF/Excel con *Ambas* |

→ [Ver el tutorial completo](/tutoriales/consultar-cuenta-corriente-cliente/)

### Cobrar la deuda de un cliente (cancelar la cuenta corriente)

| Si te pasa… | Es porque… | Qué hacer |
|---|---|---|
| No veo *Cobrar a un cliente* en el menú | Falta el permiso *Puede cobrar Cta. Cte.* | Pedíselo al dueño |
| "Buscar Deudas" no muestra nada | El cliente no tiene deudas pendientes | Verificá en *Gestión de clientes* su saldo |
| El botón *Cobrar e imprimir* está gris | El *Restante* no es $ 0 | Ajustá el monto del pago o las deudas elegidas |
| Me equivoqué en un cobro | - | Pedile al dueño que lo anule desde el panel de administración |

→ [Ver el tutorial completo](/tutoriales/cobrar-deuda-cliente/)

## Proveedores y compras

### Crear y editar proveedores

| Si te pasa… | Es porque… | Qué hacer |
|---|---|---|
| No veo la deuda de un proveedor | La compra se pagó en efectivo, o todavía está pendiente de confirmar | Las compras a cuenta corriente suman deuda cuando se **confirman** |
| El proveedor no aparece al cargar la compra | Está mal escrito o creado dos veces | Buscalo por CUIT; editá el nombre si hace falta |
| No encuentro cómo borrar un proveedor | Desde el POS no hay botón para borrarlos | Dejá de usarlo; el historial de compras y pagos se conserva |

→ [Ver el tutorial completo](/tutoriales/crear-y-editar-proveedores/)

### Cargar una compra manual (sin foto) y pagarla

| Si te pasa… | Es porque… | Qué hacer |
|---|---|---|
| No me deja crear la compra | Hay un renglón sin producto, o con cantidad 0 | Asigná el producto o quitá el renglón |
| La compra no suma stock | Quedó pendiente | Pedile al dueño o a un administrativo que la confirme en el panel de administración |
| No me deja cerrar la caja | Tenés compras pagadas sin confirmar | Pedí que las confirmen (o descartalas si estaban mal cargadas) |
| No veo *Cuenta Corriente Proveedor* | Tu usuario no tiene el permiso *Puede comprar en cuenta corriente* | Pedíselo al dueño (Menú rápido → Usuarios) |
| Quiero cargar o editar el pago desde el panel | Los pagos se registran solo desde el POS | Eliminá la compra pendiente y volvela a cargar desde el POS |
| Cargué mal un precio | - | Antes de confirmar: eliminá la compra pendiente y volvela a cargar |
| El proveedor no está | Es nuevo | **＋ Nuevo proveedor** en el paso 2 |

→ [Ver el tutorial completo](/tutoriales/cargar-compra-manual/)

### Cargar una compra con la foto de la boleta (OCR rápido)

| Si te pasa… | Es porque… | Qué hacer |
|---|---|---|
| No veo *Compras con foto* | El módulo está apagado | Configuración → Módulos y sistema → *Compras con foto (OCR)* |
| "La configuración OCR no tiene API key" | Falta cargar la clave | Panel admin → Configuraciones API OCR |
| Falla la lectura con error del proveedor de IA | El modelo configurado ya no existe, o la clave no tiene saldo | Cambiá el modelo o revisá tu cuenta del proveedor de IA |
| "Se alcanzó el límite diario" / "presupuesto mensual" | Llegaste al máximo configurado | Subí el límite o continuá con **carga manual** (se habilita sola) |
| El OCR leyó mal una cantidad o un precio | Foto poco clara | Corregilo a mano en el paso 4 (los campos son editables) |
| La *Diferencia* no es $ 0 | Un renglón mal leído, faltante o sin asignar | Compará con la boleta y corregí; usá *Agregar renglón manual* |
| Un producto se asocia mal siempre | El alias quedó mal aprendido | Corregí el producto en ese renglón y revisá los alias (ver *Dónde ver lo que aprendió el sistema*) |
| La compra no mueve el stock | Quedó **pendiente** | Confirmala en Panel admin → Compra → Compras → *Confirmar compra* (la hace el dueño o un administrativo) |
| No me deja cerrar la caja | Hay compras pagadas sin confirmar en tu turno | Pedí que las confirmen en el panel |
| Me equivoqué con el flete | - | Antes de confirmar, no hay efecto: eliminá la compra pendiente y volvela a cargar |

→ [Ver el tutorial completo](/tutoriales/cargar-compras-con-foto-ia/)

### Pagar a un proveedor y revisar su cuenta corriente

| Si te pasa… | Es porque… | Qué hacer |
|---|---|---|
| No aparecen deudas del proveedor | La compra se pagó en efectivo, o quedó **pendiente de confirmar** | Confirmala en el panel de administración (Compra → Compras → *Confirmar compra*) |
| El botón *Aplicar pago* está apagado | Falta cargar un pago, o no tildaste ninguna compra | Elegí medio y monto, y tocá **+** |
| Pagué de más | El pago superó la deuda tildada | Revisá el *Saldo real*: si es negativo, el excedente figura como **saldo a favor** |
| "No hay un turno abierto" al pagar | Los pagos a proveedores salen de la caja del turno abierto | Abrí un turno desde el POS y volvé a pagar. No se pueden cargar pagos desde el panel de administración |
| Me equivoqué en un pago | - | Pedile al dueño que lo revierta desde el panel de administración |

→ [Ver el tutorial completo](/tutoriales/pagar-proveedor/)

### Cargar listas de precios de proveedores y compararlos

| Si te pasa… | Es porque… | Qué hacer |
|---|---|---|
| No veo la pantalla | El módulo está apagado | Configuración → Módulos y sistema → *Listas de precios de proveedores* |
| Muchos renglones quedan en *Revisión* | Los nombres de la lista difieren de los tuyos | Asocialos uno a uno con **Buscar** (o ignoralos) antes de publicar |
| Me equivoqué al publicar | - | Cargá la lista correcta y publicá de nuevo |
| Quiero seguir mañana | - | **Guardar borrador** y reabrí desde *Listas guardadas* |
| El precio se leyó mal (PDF/foto) | Calidad de la imagen | Corregilo en **Costo nuevo** antes de publicar |

→ [Ver el tutorial completo](/tutoriales/cargar-listas-precios-proveedores/)

## Stock y precios

### Conteo de stock (y corrección con el lápiz)

| Si te pasa… | Es porque… | Qué hacer |
|---|---|---|
| No veo *Conteo de stock* | Falta el permiso *Puede modificar stock* | Pedíselo al dueño |
| No veo el lápiz | Falta ese permiso, o no abriste el producto en *Editar* | Verificá el permiso y el permiso de gestionar productos |
| Un producto no aparece | No es contable (servicio u horas) o está fusionado | Esos productos no se cuentan |
| Contó otra persona y no puedo ver su diferencia | Conteo a ciegas | El administrador la ve en *Ajustes de inventario* |
| Me equivoqué en un conteo | - | Anulá el ajuste desde el panel de administración |

→ [Ver el tutorial completo](/tutoriales/contar-stock/)

### Ajustes de inventario, mermas y transferencias entre depósitos

| Si te pasa… | Es porque… | Qué hacer |
|---|---|---|
| El desplegable *Estado* de la transferencia está vacío | No hay estados cargados | Creá los estados en *Producto → Estados de transferencia* |
| La transferencia no mueve stock | Está en un estado que no es final | Tocá **▶ Avanzar** hasta el estado final |
| "No se puede modificar una transferencia completada" | Ya movió el stock | Hacé una transferencia inversa |
| La merma no descontó | Quedó pendiente | Tildala y usá **Confirmar mermas** |
| Quiero corregir el stock de varios productos | - | Usá el **Conteo de stock** del POS |

→ [Ver el tutorial completo](/tutoriales/ajustar-stock-mermas-transferencias/)

### Actualizar precios en bloque (precios masivos) y rentabilidad

| Si te pasa… | Es porque… | Qué hacer |
|---|---|---|
| "No hay precios que coincidan con los filtros" | La categoría o el proveedor no tiene productos con precio | Probá con *Todas* / *Todos* |
| El precio quedó más alto de lo que esperaba | El redondeo sube al múltiplo siguiente | Usá *0.01*, o corregí el precio a mano en la tabla |
| Me equivoqué | - | **Revertir lote** (solo el último) |
| Quiero ver cuánto gano por producto | - | La columna **% Actual / % Nuevo** de la previsualización, o la app del dueño (Productos) |
| La categoría dice "sin %" | No tiene rentabilidad objetivo | Cargala en el panel de administración, o usá un % fijo |

→ [Ver el tutorial completo](/tutoriales/actualizar-precios-y-rentabilidad/)

## Marketing y tienda

### Crear ofertas y promociones (y sus variantes)

| Si te pasa… | Es porque… | Qué hacer |
|---|---|---|
| No veo *Ofertas* en el menú | Falta el permiso *Puede gestionar ofertas* | Pedíselo al dueño |
| La oferta no se cobra | Está en *Borrador* o *Pausada*, o fuera de vigencia (fecha, día u hora) | Activala y revisá la vigencia en el Calendario |
| Se cobra una oferta que no esperaba | Hay otra oferta vigente más barata para ese producto | Pausá o editá la otra oferta |
| La promoción da pérdida | La regla deja el precio bajo el costo | Mirá el aviso amarillo y corregí el valor |
| Un producto no aparece al buscar | Solo se pueden poner en oferta productos con precio de venta | Cargale un precio de venta |

→ [Ver el tutorial completo](/tutoriales/crear-ofertas-y-promociones/)

### Crear revistas y folletos con tus ofertas (y editar sus fotos)

| Si te pasa… | Es porque… | Qué hacer |
|---|---|---|
| No veo *Revistas y folletos* | Módulo apagado o falta el permiso | Configuración → Módulos y sistema · permisos del usuario |
| *Traer ofertas* no trae nada | No hay ofertas vigentes en esas fechas | Creá una oferta o cambiá el período |
| Salen productos "Sin foto" | El producto no tiene foto cargada | **Subir otra foto** desde el editor, o cargala en el producto |
| El precio no es el que esperaba | La oferta cambió o venció | Volvé a **Traer ofertas** para actualizar |
| La hoja quedó muy cargada | Muchos productos por página | Bajá columnas/filas o usá más hojas |

→ [Ver el tutorial completo](/tutoriales/crear-revista-ofertas/)

### Imprimir etiquetas de precio y código de barras

| Si te pasa… | Es porque… | Qué hacer |
|---|---|---|
| No veo *Imprimir etiquetas* | Falta el permiso *Puede imprimir etiquetas* | Pedíselo al dueño |
| Dice que no hay etiquetadora | La caja no tiene una configurada | Configuración → Etiquetadora |
| No puedo tildar productos | No hay etiquetadora configurada | Configurala primero |
| No sale nada | La caja no tiene credencial del agente de impresión, o el agente no está corriendo | Configuración → Impresora de tickets → *Agente de impresión* |
| La segunda etiqueta sale desalineada | Falta calibrar | En *Etiquetadora* usá **Guardar e imprimir 2 de prueba** y ajustá el corrimiento |
| La etiqueta sale sin código | El producto no tiene código de barras | Cargale uno en *Editar producto* |

→ [Ver el tutorial completo](/tutoriales/imprimir-etiquetas/)

### Tienda online: prenderla, diseñarla y recibir pedidos

| Si te pasa… | Es porque… | Qué hacer |
|---|---|---|
| `/revista/` no abre | La tienda está apagada | *Configuración → Módulos y sistema → Tienda online activa* |
| El cliente no ve los precios | No inició sesión | Que ingrese o se registre |
| Nadie puede registrarse | *Registro libre* apagado | Prendelo, o creá vos las cuentas |
| Cambié el diseño y no se ve | Quedó en **borrador** | Tocá **Publicar** |
| El cliente no puede confirmar | No hay caja para las ventas online | Elegí la **Caja de las ventas online** |
| No aparece la portada | Está en *Catálogo directo* | Elegí **Portada + catálogo** en *Contenido* |

→ [Ver el tutorial completo](/tutoriales/configurar-tienda-online/)

## App del dueño y panel

### La app del dueño en el celular

| Si te pasa… | Es porque… | Qué hacer |
|---|---|---|
| «Tu usuario no tiene acceso a esta app» | El usuario es cajero | Cambiale el rol a *Administrativo* |
| «Usuario o contraseña incorrectos» | Datos mal escritos | Revisá mayúsculas y probá de nuevo |
| Productos / Elaborados / Cuentas piden «generar una radiografía» | Todavía no hay ningún reporte guardado | Tocá **Generar mes actual** |
| Los números no incluyen lo vendido hoy | El reporte se calculó antes | Tocá **Recalcular con los datos de hoy** |
| No me deja instalar la app | La dirección es `http://` | Entrá por `https://` |
| Elaborados está en cero | Todavía no se vendió ningún producto con receta en ese período | Elegí otro período |
| No veo «Para reponer» productos | Los productos no tienen stock mínimo cargado | Cargá el mínimo en cada producto |

→ [Ver el tutorial completo](/tutoriales/usar-app-del-dueno/)

### Consultar, filtrar y exportar información en el panel de administración

| Si te pasa… | Es porque… | Qué hacer |
|---|---|---|
| No encuentro una venta | Está en estado *creada* (nunca se cobró) o el filtro de fecha no la incluye | Filtrá por *estado = creada* o quitá el filtro de fecha |
| Una venta aparece dos veces en *Ingresos Ventas* | Se cobró con dos medios de pago | Es lo esperado: una fila por medio |
| «Seleccione solo un pedido…» | Tildaste más de una venta | Tildá una sola para el reporte de costos |
| Una columna que usaba desapareció | Alguien la ocultó en **tu** usuario (o la guardaste vos) | Acción *Configurar columnas visibles* → **Restaurar por defecto** |
| El Excel tiene muchas columnas que no necesito | Se exportan todos los campos tildados | En la pantalla de exportación, destildá los campos que no quieras |

→ [Ver el tutorial completo](/tutoriales/consultar-reportes-y-exportar/)

### Controlar los turnos de caja desde el panel de administración

| Si te pasa… | Es porque… | Qué hacer |
|---|---|---|
| El turno tiene faltante y no sé por qué | Falta registrar un retiro, un gasto o un cobro; o hay un pago de compra o a proveedor en efectivo | Revisá las pestañas del turno (incluye *Pagos de compras* y *Pagos a proveedores*) |
| Un pago antiguo a un proveedor no figura en ningún turno | Es anterior a esta versión (entonces no se asociaba al turno) | En *Compras → Pagos Masivos a Prov.* filtrá por **Sin turno** para ver esos pagos históricos |
| Necesito corregir un turno cerrado | Los cerrados no se recalculan solos | Un superusuario puede usar la acción **Recalcular turno** (queda anotado en observaciones) |
| El turno aparece *Abierto* de un día anterior | El cajero no lo cerró | Pedile que lo cierre desde el POS (ver [Turno de caja](/tutoriales/abrir-y-cerrar-caja/)) |
| No puedo modificar los números de un turno | Los totales son de solo lectura | Es a propósito: se calculan solos |
| Veo una venta anulada entre los ingresos del turno | El cobro original queda en su turno; la devolución figura en el turno abierto que se eligió al anular | Revisá la venta en *Venta → Ventas* y la devolución en el turno que corresponda |
| No puedo anular una venta | No hay ningún turno de caja abierto para imputar la devolución | Abrí un turno desde el POS y volvé a intentar |
| No encuentro cómo agregar un turno o un pago desde el panel | Ya no se puede: se hace todo desde el POS | Abrí el turno o registrá el pago desde el POS |

→ [Ver el tutorial completo](/tutoriales/controlar-turnos-caja-panel/)

### Billeteras y cuentas: dónde está tu plata

| Si te pasa… | Es porque… | Qué hacer |
|---|---|---|
| Un cobro no aparece en el banco | El medio de pago no tiene billetera vinculada | Vinculalo (paso 3) |
| «Saldo insuficiente en …» al transferir | El origen no tiene saldo suficiente y el saldo negativo no está permitido | Revisá el saldo, registrá el ingreso que falta o activá *Permitir saldo negativo* |
| No puedo cambiar el saldo inicial | La billetera ya tiene movimientos | Usá un **ajuste** de tipo *Corrección de saldo* |
| La transferencia no movió plata | Quedó pendiente | Confirmala con la acción *Confirmar transferencias seleccionadas* |
| La billetera Efectivo está en negativo | Faltan ingresos o el saldo inicial | Cargá un ajuste de *Ajuste de saldo inicial* o revisá los movimientos |
| No puedo usar una billetera en una operación | Está inactiva | Marcá *Cuenta activa* |

→ [Ver el tutorial completo](/tutoriales/billeteras-y-cuentas/)

## Armado de pedidos y notas

### Armado de pedidos (picking) desde el celular

| Si te pasa… | Es porque… | Qué hacer |
|---|---|---|
| No veo *Picking* o dice «Permiso denegado» | Tu usuario no tiene el permiso de picking, o el módulo está desactivado | Pedile al dueño el permiso (tutorial 04) o activá el módulo en el engranaje |
| No aparece la acción *Crear armado de pedido* | La venta no está finalizada, el módulo está apagado, o el primer estado de seguimiento ya genera armados solo | Revisá las tres cosas; si el primer estado tiene la casilla tildada, los armados ya se crean automáticamente |
| «La venta ya tiene un armado activo» | Una venta admite un solo armado activo | Trabajá con el que existe |
| «Error: undefined» al tocar *Siguiente Estado: Listo* | La pantalla no maneja la confirmación del estado final | Usá **Finalizar Pedido** (queda anotado como requerimiento, ver `_requerimientos/REQ-004`) |
| «Este pedido no permite edición en su estado actual» | El estado tiene *Permite edición* apagado | Reabrí el pedido o cambialo a un estado que permita edición |
| El pedido cerró pero el cliente no recibió la devolución | Se finalizó sin generar la nota de crédito | Creá la nota a mano en el panel (ver tutorial 35) |
| «Hay N items sin procesar» | Quedan ítems en PENDIENTE | Marcá cada uno (Completar o cantidad real) |

→ [Ver el tutorial completo](/tutoriales/armar-pedidos-picking/)

### Notas de crédito y débito: aplicar, controlar y anular

| Si te pasa… | Es porque… | Qué hacer |
|---|---|---|
| La nota existe pero el stock no cambió | Está en **borrador** | Aplicala |
| «La nota de crédito debe tener medio de pago…» | La nota no tiene medio y no se pudo deducir de la venta | Abrila (borrador), elegí el medio y aplicala |
| No puedo editar la nota | Ya está aplicada o anulada | Anulala (genera su inversa) y creá una nueva si corresponde |
| Un pedido cerrado no tiene nota de crédito | Se finalizó sin generarla | Reabrilo en el celular y generá la nota, o creala a mano (paso 5) |
| La caja del día no cuadra por una nota | La nota se aplicó en un turno distinto al de la venta | Mirá el arqueo del turno: las notas aparecen como movimientos del medio (ver [Controlar un turno](/tutoriales/controlar-turnos-caja-panel/)) |

→ [Ver el tutorial completo](/tutoriales/notas-de-credito-y-debito/)

## Operación: licencia, respaldos e impresión

### La licencia de ADEstock: versión gratuita y Licencia Pro

| Si te pasa… | Es porque… | Qué hacer |
|---|---|---|
| «Licencia no válida para este equipo», «Licencia inválida» o «Formato de licencia corrupto» | La clave es de otra PC o se copió incompleta | Revisá que pegaste toda la clave; si cambiaste de PC, pedí una nueva con el *Machine ID* actual |
| Dice «Machine ID no disponible» (o «La licencia expiró el…» si la clave tenía fecha) | El sistema no pudo leer los datos de la PC | Reiniciá el sistema como administrador; si sigue, avisá al soporte |
| No puedo cobrar: «límite diario» | Estás en la versión gratuita y ya hiciste 5 ventas hoy | Activá la Licencia Pro, o esperá a mañana |
| La licencia Pro dejó de verse tras cambiar de computadora | La licencia está atada a la PC anterior | Pedí una nueva clave con el nuevo *Machine ID* |

→ [Ver el tutorial completo](/tutoriales/licencia/)

### Respaldos: copias de seguridad y restauración

| Si te pasa… | Es porque… | Qué hacer |
|---|---|---|
| «No se seleccionaron configuraciones activas» | La configuración está **inactiva** o no tildaste ninguna | Tildá una configuración con *Activo* |
| El respaldo da **Error** | Carpeta de salida inexistente o sin permisos, disco lleno o base bloqueada | Leé el mensaje en la ejecución; probá con la carpeta vacía (usa la de datos) |
| No sube a Drive | Falta vincular la cuenta o venció la autorización | Repetí **Vincular Drive por QR** |
| Restauré y no veo cambios | La aplicación sigue con la base anterior en memoria | Reiniciá el sistema |
| Se me llenó el disco de ZIP | Los respaldos se acumulan | Copiá los viejos afuera y borrá los que ya no necesitás |

→ [Ver el tutorial completo](/tutoriales/respaldos/)

### Instalar y conectar el agente de impresión (Agent Printer)

| Si te pasa… | Es porque… | Qué hacer |
|---|---|---|
| El POS dice «la caja todavía no tiene credencial» | Falta el paso 1 | **Crear credencial para esta caja** |
| El agente dice *Cloud: ERROR* o error 401/403 | La clave o la URL están mal, o la credencial se regeneró | Copiá de nuevo los datos del POS (paso 1) y guardalos |
| «Detené el agente antes de guardar cambios» | Está corriendo | **Detener agente** → guardar → **Iniciar agente** |
| El ticket no sale pero el agente figura OK | Nombre de impresora USB incorrecto o impresora apagada/sin papel | Revisá **Impresoras detectadas** y el nombre en el POS; probá de nuevo |
| Se filtró la clave | - | En el POS tocá **Generar clave nueva** y cargala en el agente: el viejo deja de imprimir |
| Dos PC imprimen lo mismo | Usan la misma credencial | Una credencial por caja |

→ [Ver el tutorial completo](/tutoriales/instalar-agente-de-impresion/)
