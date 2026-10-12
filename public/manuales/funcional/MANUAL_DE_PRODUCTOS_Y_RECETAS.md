# Manual de Gestión de Productos, Costos y Recetas

Este documento detalla el funcionamiento del módulo de Productos y Cocina del sistema. Está diseñado para guiar al usuario en la creación de productos de reventa, materias primas y productos de elaboración propia (Recetas), explicando cómo el sistema calcula los costos y gestiona los precios de venta.

---

## 1. Conceptos Generales

El sistema diferencia dos tipos principales de productos:
1.  **Productos Simples / Insumos:** Productos que se compran y se venden tal cual (ej. una gaseosa) o materias primas para cocinar (ej. harina, huevos).
2.  **Productos de Fabricación Propia (Recetas):** Productos que resultan de un proceso de transformación de insumos (ej. una torta, un mueble, un sándwich).

---

## 2. Productos Simples (Compra y Reventa)

Son aquellos productos donde usted define manualmente el costo y la presentación.

### A. Definición del Costo Base
Al crear un producto simple, encontrará tres campos clave en la sección "Detalles del Producto":

*   **Unidad de Medida:** Es la unidad en la que usted gestiona el stock (Kilos, Litros, Unidades, etc.).
*   **Costo:** Es el precio que usted paga al proveedor por el "bulto" o "empaque" cerrado.
*   **Cantidad:** **(Importante)** Aquí debe colocar la cantidad que trae la presentación de compra.

> **Ejemplo Práctico:**
> *   Si compra una **bolsa de harina de 20 Kilos** que le cuesta $10.000:
>     *   Costo: $10.000
>     *   Cantidad: 20
>     *   Unidad: Kilos
>     *   *El sistema calculará internamente que el costo por Kilo es $500.*
>
> *   Si compra un **pack de 12 gaseosas** a $12.000:
>     *   Costo: $12.000
>     *   Cantidad: 12
>     *   Unidad: Unidades
>     *   *El sistema calculará que el costo unitario es $1.000.*

### B. Precios de Venta y Unidades Alternativas
El sistema permite flexibilidad en la venta. Usted puede comprar en una unidad y vender en otra, siempre que sean compatibles.

*   **Compatibilidad:**
    *   *Kilos* ↔ *Gramos*
    *   *Litros* ↔ *Mililitros*
    *   *Unidades* (Generalmente se venden por unidad).

En la pestaña de **Precios**, usted puede definir múltiples precios de venta.
*   Puede vender la Harina (que compró en Kilos) por paquetes de 500 Gramos.
*   El sistema calculará el costo proporcional automáticamente.

---

## 3. Productos de Fabricación Propia (Recetas)

Cuando un producto se elabora en casa (Cocina/Taller), el costo no lo define una factura de compra, sino la suma de sus ingredientes y gastos.

### A. El Módulo de Cocina (Recetas)
Antes de crear el producto final, debe existir la **Receta**.
Una receta se compone de:
1.  **Nombre y Descripción:** Qué estamos cocinando.
2.  **Porciones:** Cuántas unidades rinde esta preparación (ej. Una torta rinde 8 porciones, o 1 torta entera).
3.  **Insumos (Ingredientes):** Se seleccionan productos simples (harina, azúcar) y se indica la cantidad usada.
4.  **Gastos Adicionales:** Costos extra como gas, luz, packaging, mano de obra.
    *   **¿Cómo funcionan?** En el administrador de Recetas, verá una tabla para "Gastos Adicionales". Puede crear conceptos (ej. "Mano de Obra") y asignarles un valor fijo monetario a la receta.
    *   **Impacto:** Si agrega $500 de "Mano de Obra" a una receta que rinde 10 porciones, el sistema sumará $50 a cada porción automáticamente.
    *   **Importante:** Estos gastos son **fijos por receta**, no por kilo de ingrediente. Úselos para costos que no son materia prima pero que son necesarios para la fabricación.
5.  **Sub-Recetas:** Preparaciones previas (ej. una masa de tarta que se usa en varias recetas).

**El Cálculo Automático:**
El sistema suma todos los costos y los divide por la cantidad de **Porciones**.
> *Costo Total de la Receta / Cantidad de Porciones = Costo Unitario (Costo por Porción)*

**Exportar Receta:**
Dentro del módulo de cocina, cada receta tiene la opción de generar un **PDF**. Este documento sirve como guía de producción para el personal, detallando ingredientes y pasos sin mostrar necesariamente los costos sensibles.

### B. Asociación Producto - Receta (Lógica de Costo)
Este es el punto más importante de la integración. Cuando usted crea un Producto y le asigna una **Receta** en el campo "Fabricación Propia":

1.  **Bloqueo de Cantidad:** El sistema automáticamente establecerá la **Cantidad en 1** y bloqueará el campo.
2.  **Origen del Costo:** El sistema ignorará cualquier costo manual y tomará estrictamente el **Costo por Porción** calculado en la receta.

**¿Por qué funciona así?**
Anteriormente, existía el riesgo de error humano: si una receta de masa rendía 3000 gramos, el usuario podía poner "3000" en cantidad. El sistema multiplicaba *3000 x Costo por Gramo*, generando un costo millonario erróneo.

**Ahora:**
*   El sistema asume que este Producto representa **1 unidad de venta** resultante de la receta.
*   **Mensaje de Ayuda:** Verá un mensaje indicando: *"Este producto toma como base de costo 1 porción de la Receta 'Nombre'..."*.

---

## 4. Panel de Análisis de Precios

En la pestaña de precios del Producto (tanto simples como recetas), encontrará un nuevo panel informativo llamado **"Análisis de Costo y Precio"**.

Este panel le muestra en tiempo real:
1.  **Costo Base:** Cuánto le cuesta a usted esa unidad (ya sea comprada o cocinada).
    *   *Ej: $ 150.00 por Gramos* (Si es insumo).
    *   *Ej: $ 1,200.00 por Porción (Receta)* (Si es elaborado).
2.  **Precio Venta:** A cuánto lo está vendiendo según la rentabilidad o precio manual configurado.

Esto le permite verificar rápidamente si los números "cierran" sin tener que usar calculadora.

---

## Resumen de Flujo de Trabajo

1.  **Cargue sus Insumos:** Cree productos simples (Harina, Huevos) con sus costos de factura y presentaciones (bultos).
2.  **Arme sus Recetas:** Vaya a Cocina, cree la receta, agregue los insumos y defina cuántas porciones rinde.
3.  **Cree el Producto Final:**
    *   Vaya a Productos.
    *   Cree "Torta de Chocolate".
    *   En "Fabricación Propia", seleccione la receta "Torta Chocolate".
    *   El sistema ajustará la cantidad a 1 automáticamente.
    *   Vaya a la pestaña Precios y defina su precio de venta final.
