# Solución: TypeError "args or kwargs must be provided" en format_html()

## 🔴 El Error

Al trabajar con Django 6.0+ y Python 3.13, aparece este error al usar `format_html()`:

```python
TypeError: args or kwargs must be provided.
```

### Stack trace típico:
```
File "django/utils/html.py", line 137, in format_html
    raise TypeError("args or kwargs must be provided.")
```

---

## 📋 ¿Por qué ocurre?

Django's `format_html()` **requiere placeholders `{}` con argumentos** para escapar el HTML de forma segura.

### ❌ Código que FALLA:

```python
def mi_metodo(self, obj):
    return format_html(
        '''
        <div style="color: red;">
            <h3>Título</h3>
            <p>Contenido fijo sin placeholders</p>
        </div>
        '''
    )
```

**Error:** No hay placeholders `{}` ni argumentos después del string.

---

## ✅ Soluciones

### **Opción 1: Usar `mark_safe()` (Recomendado para HTML estático)**

Si el HTML **NO** contiene datos dinámicos del usuario, usa `mark_safe()`:

```python
from django.utils.safestring import mark_safe

def mi_metodo(self, obj):
    return mark_safe(
        '''
        <div style="color: red;">
            <h3>Título</h3>
            <p>Contenido fijo sin placeholders</p>
        </div>
        '''
    )
```

✅ **Cuándo usar:** HTML completamente estático (guías, ayudas, formateo fijo).

---

### **Opción 2: Usar `format_html()` correctamente (con placeholders)**

Si necesitas **insertar datos dinámicos**, usa placeholders `{}`:

```python
from django.utils.html import format_html

def mi_metodo(self, obj):
    nombre = obj.nombre
    precio = obj.precio
    
    return format_html(
        '''
        <div style="color: red;">
            <h3>Producto: {}</h3>
            <p>Precio: $ {:,.2f}</p>
        </div>
        ''',
        nombre,
        precio
    )
```

✅ **Cuándo usar:** Cuando insertas variables que pueden venir de la base de datos o entrada del usuario.

---

## 🔧 Casos Corregidos en este Proyecto

### Archivos modificados:

1. **producto/admin.py**
   - `guia_mermas()` → `mark_safe()`
   - `guia_carga_productos()` → `mark_safe()`

2. **venta/admin.py**
   - `guia_retiros()` → `mark_safe()`

3. **compra/admin.py**
   - `guia_maestra()` → `mark_safe()`
   - Variación de costo 0% → `mark_safe()`

4. **cocina/admin.py**
   - `guia_recetas()` → `mark_safe()`

5. **agenda/admin.py**
   - `guia_caja()` → `mark_safe()`
   - `guia_clientes()` → `mark_safe()`
   - `guia_asignacion()` → `mark_safe()`
   - `guia_monedas()` → `mark_safe()`
   - `guia_gastos()` → `mark_safe()`
   - `guia_depositos()` → `mark_safe()`
   - `guia_medios()` (2 instancias) → `mark_safe()`

---

## 🔍 Cómo Detectar el Problema

### Buscar en todo el proyecto:

```bash
# En terminal PowerShell
Get-ChildItem -Recurse -Filter "*.py" | Select-String "format_html\(\s*['\"]" -Context 0,3
```

### Patrón a buscar:

```python
# ❌ MAL - Sin placeholders ni argumentos
format_html('<div>...</div>')
format_html('''<div>...</div>''')

# ✅ BIEN - Con placeholders
format_html('<div>{}</div>', valor)
format_html('<span style="color: {};">{}</span>', color, texto)

# ✅ BIEN - HTML estático con mark_safe
mark_safe('<div>HTML fijo</div>')
```

---

## 📚 Referencia Rápida

| Situación | Solución | Ejemplo |
|-----------|----------|---------|
| HTML completamente estático | `mark_safe()` | Guías de ayuda, banners informativos |
| HTML con datos de BD/usuario | `format_html()` + `{}` | Mostrar nombre, precio, fecha del modelo |
| String sin placeholders pero necesita escape | `escape()` + `mark_safe()` | Texto con caracteres especiales |

---

## ⚠️ Seguridad

### `mark_safe()` - Usar con PRECAUCIÓN

```python
# ❌ PELIGRO - XSS vulnerability
def mostrar(self, obj):
    return mark_safe(f'<div>{obj.comentario_usuario}</div>')
    # Si comentario_usuario = "<script>alert('hack')</script>" → ejecuta el script
```

```python
# ✅ SEGURO - Escapa datos de usuario
def mostrar(self, obj):
    from django.utils.html import escape
    return mark_safe(f'<div>{escape(obj.comentario_usuario)}</div>')
```

**Regla de oro:** 
- `mark_safe()` = Solo para HTML que escribes tú (código fuente)
- `format_html()` = Para HTML con datos dinámicos (escapa automáticamente)

---

## 🛠️ Solución Aplicada en Proyecto

Todos los métodos de tipo "guía maestra" fueron migrados de:

```python
def guia_xxx(self, obj):
    return format_html('''<div>...</div>''')
```

A:

```python
def guia_xxx(self, obj):
    from django.utils.safestring import mark_safe
    return mark_safe('''<div>...</div>''')
```

Esto porque las guías son HTML estático sin datos del usuario.

---

## 📝 Notas Adicionales

- Este cambio es necesario desde **Django 4.2+** donde se hizo más estricta la validación.
- Python 3.13 también mejoró la detección de estos errores.
- El error aparece en **runtime**, no en startup, por eso se descubre al navegar al admin.

---

## ✅ Verificación

Después de aplicar los cambios:

1. Reinicia el servidor Django
2. Navega a cada sección del admin
3. Verifica que las guías maestras se muestren correctamente
4. No deberían aparecer más errores `TypeError: args or kwargs must be provided`

---

**Fecha de resolución:** 20 de Enero, 2026  
**Versiones:** Django 6.0.1, Python 3.13
