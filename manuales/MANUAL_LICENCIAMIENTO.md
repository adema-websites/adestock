# Sistema de Licenciamiento Offline - Adestock

## 📋 Tabla de Contenidos
1. [Descripción General](#descripción-general)
2. [Características](#características)
3. [Arquitectura del Sistema](#arquitectura-del-sistema)
4. [Instalación y Configuración](#instalación-y-configuración)
5. [Uso para el Desarrollador](#uso-para-el-desarrollador)
6. [Uso para el Cliente](#uso-para-el-cliente)
7. [Seguridad](#seguridad)
8. [Solución de Problemas](#solución-de-problemas)

---

## 📖 Descripción General

Sistema de licenciamiento **Freemium** para Adestock que permite:
- **Versión Gratuita**: Funcionalidad completa pero con límites diarios y de capacidad
- **Versión Pro**: Sin restricciones al activar con licencia válida

El sistema vincula cada licencia al hardware específico del cliente (HWID), imposibilitando el uso de una misma licencia en múltiples computadoras.

---

## ✨ Características

### Seguridad
- ✅ Licencias vinculadas al hardware (Motherboard UUID + Disk Serial)
- ✅ Criptografía HMAC-SHA256 para firmar licencias
- ✅ Solo el desarrollador puede generar licencias válidas
- ✅ Protección contra timing attacks
- ✅ Validación automática sin conexión a internet

### Modelo Freemium

#### Versión Gratuita - Límites
- ✅ **5 ventas diarias**
- ✅ **Máximo 30 productos en inventario**
- ✅ **3 consultas diarias a OpenFoodFacts** (autocompletado de productos)
- ✅ Todas las funcionalidades disponibles, pero con restricciones

#### Versión Pro - Sin Límites
- ✅ **Ventas ilimitadas**
- ✅ **Productos ilimitados**
- ✅ **Consultas ilimitadas a OpenFoodFacts**
- ✅ **Soporte prioritario**
- ✅ **Actualizaciones gratuitas**
- ✅ **Sin vencimiento**

### Facilidad de Uso
- ✅ Interfaz web para activación de licencias
- ✅ Copiar/pegar Machine ID y Licencia
- ✅ Script interactivo para el desarrollador
- ✅ Validación automática con caché
- ✅ Indicadores visuales de límites en el POS

---

## 🏗️ Arquitectura del Sistema

### Componentes Principales

```
adestock/
├── utils/
│   ├── license_manager.py          # Núcleo del sistema
│   └── license_restrictions.py     # Decoradores y validaciones
│
├── views_license.py                 # Vistas de gestión
│
├── urls.py                          # Rutas configuradas
│
admin_keygen.py                      # Generador de licencias (NO DISTRIBUIR)
│
templates/
└── license/
    └── license_status.html          # Interfaz de activación
│
license.key                          # Archivo de licencia (generado por cliente)
```

### Flujo de Trabajo

```
┌─────────────┐         ┌──────────────┐         ┌─────────────┐
│   Cliente   │────────>│  Adestock    │────────>│ Desarrollador│
│             │ Machine │  (Obtener    │ Machine │              │
│             │   ID    │   HWID)      │   ID    │              │
└─────────────┘         └──────────────┘         └─────────────┘
      ▲                                                   │
      │                                                   │
      │                  Licencia                         │
      │                  Generada                         │
      └───────────────────────────────────────────────────┘
                    (admin_keygen.py)
```

---

## 🔧 Instalación y Configuración

### 1. Archivos Ya Creados

El sistema ha sido instalado con los siguientes archivos:

- ✅ `adestock/utils/license_manager.py` - Gestión de licencias
- ✅ `adestock/utils/license_restrictions.py` - Decoradores
- ✅ `adestock/views_license.py` - Vistas web
- ✅ `admin_keygen.py` - Generador (solo para ti)
- ✅ `templates/license/license_status.html` - Interfaz web

### 2. URLs Configuradas

Las siguientes rutas ya están agregadas a `adestock/urls.py`:

```python
# URLs de gestión de licencias
path('license/', license_status, name='license_status'),
path('license/activate/', activate_license, name='activate_license'),
path('license/deactivate/', deactivate_license, name='deactivate_license'),
path('api/license/machine-id/', get_machine_id_json, name='get_machine_id_json'),
path('api/license/status/', check_license_status_json, name='check_license_status'),
```

### 3. Ejemplo de Uso Implementado

Ya se aplicó el decorador a `pos_cerrar_venta` en `venta/views.py`:

```python
@login_required(login_url='/admin/login/')
@require_pro_or_limit_sales(max_free_sales=3)  # ← Limitación aplicada
def pos_cerrar_venta(request):
    # ... tu código de venta
```

### 4. Configuración Opcional

#### Agregar contexto global de licencia a todos los templates

Edita `adestock/settings.py`:

```python
TEMPLATES = [
    {
        'OPTIONS': {
            'context_processors': [
                # ... otros context processors
                'adestock.views_license.license_context_processor',  # ← Agregar
            ],
        },
    }
]
```

Esto hace disponible `is_pro_license` y `license_type` en todos tus templates.

---

## 👨‍💻 Uso para el Desarrollador

### Generar Licencias

#### Modo Interactivo (Recomendado)

```bash
cd C:\Users\kevin\OneDrive\Escritorio\adestock-desktop
python admin_keygen.py
```

**Proceso:**
1. El script te pedirá el Machine ID del cliente
2. Generará automáticamente su licencia
3. Opcionalmente la guardará en un archivo `.txt`

#### Modo Prueba (Testing)

```bash
python admin_keygen.py test
```

Esto:
- Obtiene el Machine ID de tu propia PC
- Genera una licencia de prueba
- Verifica que el sistema funciona correctamente

#### Modo Batch (Múltiples Licencias)

```bash
python admin_keygen.py batch
```

Para generar múltiples licencias desde un archivo de texto con Machine IDs.

### Ejemplo de Sesión Interactiva

```
======================================================================
  GENERADOR DE LICENCIAS ADESTOCK PRO
  Sistema de Licenciamiento Offline basado en HWID
======================================================================

INSTRUCCIONES:
----------------------------------------------------------------------
1. El cliente debe ir a 'Configuración > Licencia' en Adestock
2. Copiar su 'Machine ID' (64 caracteres) y enviártelo
3. Pegar el Machine ID aquí para generar su licencia
----------------------------------------------------------------------

Ingresa el Machine ID del cliente (o 'salir' para terminar): 
a7f3c2d1e5b9f8a6c3d2e1f0a9b8c7d6e5f4a3b2c1d0e9f8a7b6c5d4e3f2a1b0

======================================================================
✅  LICENCIA GENERADA EXITOSAMENTE
======================================================================

Machine ID del Cliente:
  a7f3c2d1e5b9f8a6c3d2e1f0a9b8c7d6e5f4a3b2c1d0e9f8a7b6c5d4e3f2a1b0

Clave de Licencia PRO:
----------------------------------------------------------------------
  mZxK3nP9qW2tY8jL5vC1bN4mA7sD0fG6hJ9kL2nM5pQ8rT1uV4wX7yZ0aB3cE6=
----------------------------------------------------------------------

INSTRUCCIONES PARA EL CLIENTE:
  1. Abrir Adestock
  2. Ir a 'Configuración > Licencia'
  3. Pegar la licencia en el campo correspondiente
  4. Hacer clic en 'Activar Licencia'
  5. ¡Listo! Ahora tiene versión PRO ilimitada
```

### Cambiar la Clave Secreta

**IMPORTANTE:** Antes de distribuir, cambia la `_SECRET_MASTER_KEY` en:

`adestock/utils/license_manager.py` (línea 41):

```python
_SECRET_MASTER_KEY = b'TU_CLAVE_SUPER_SECRETA_Y_UNICA_AQUI_2026'
```

⚠️ **NUNCA** compartas esta clave. Sin ella, nadie puede generar licencias falsas.

---

## 👥 Uso para el Cliente

### 1. Ver Estado de Licencia

El cliente puede acceder desde el menú de Adestock:

**Configuración > Licencia** o directamente en: `http://localhost:8000/license/`

### 2. Obtener Machine ID

1. Ir a la página de Licencia
2. Ver su **Machine ID** único (64 caracteres)
3. Hacer clic en **"Copiar"** para copiarlo al portapapeles
4. Enviártelo por WhatsApp/Email

### 3. Activar Licencia Pro

1. Recibir la licencia que tú le generaste
2. Ir a **Configuración > Licencia**
3. Pegar la licencia en el campo de texto
4. Hacer clic en **"Activar Licencia PRO"**
5. ✅ ¡Listo! Ahora tiene ventas ilimitadas

### 4. Limitaciones de Versión Gratuita

Cuando el cliente intenta realizar la **4ª venta del día** sin licencia Pro:

**En Vista Web:**
- Se muestra un mensaje: "🔒 Límite de Versión Gratuita Alcanzado"
- Se redirige a la página de activación de licencia

**En Petición AJAX (POS):**
```json
{
  "success": false,
  "error": "limit_reached",
  "message": "Has realizado 3 de 3 ventas permitidas hoy...",
  "ventas_hoy": 3,
  "limite": 3,
  "upgrade_url": "/license/"
}
```

---

## 🔒 Seguridad

### Fortalezas del Sistema

1. **Vinculación Hardware**: Cada licencia solo funciona en UN equipo específico
2. **Firma Criptográfica**: HMAC-SHA256 previene falsificación
3. **Offline**: No requiere internet, ni servidores
4. **Sin Fecha de Expiración**: Las licencias no caducan
5. **Protección Timing Attacks**: Usa `hmac.compare_digest()`

### Limitaciones

- ⚠️ Si el cliente cambia motherboard o disco, necesitará nueva licencia
- ⚠️ La `_SECRET_MASTER_KEY` está ofuscada pero no encriptada en el código
- ⚠️ Un atacante avanzado podría extraer la clave del código

### Mejoras de Seguridad Adicionales (Opcional)

Para producción seria, considera:

1. **Ofuscar código con PyArmor**:
```bash
pip install pyarmor
pyarmor obfuscate adestock/utils/license_manager.py
```

2. **Compilar con Cython**:
```bash
pip install cython
cythonize -i adestock/utils/license_manager.py
```

3. **Usar PyInstaller con cifrado**:
```bash
pyinstaller --key=MI_CLAVE_SECRETA adestock_secure.spec
```

---

## 🛠️ Solución de Problemas

### Cliente: "No puedo obtener mi Machine ID"

**Posibles causas:**
- Sistema operativo no es Windows
- Comandos WMIC deshabilitados

**Solución:**
```python
# En caso de error, el sistema mostrará el mensaje específico
# Verifica que WMIC esté disponible en CMD:
wmic csproduct get uuid
```

### Cliente: "Licencia inválida"

**Posibles causas:**
1. Licencia copiada incorrectamente (espacios extra)
2. Machine ID incorrecto usado en generación
3. Clave secreta diferente entre versiones

**Solución:**
1. Volver a copiar la licencia SIN espacios adicionales
2. Verificar que el Machine ID sea el correcto
3. Regenerar la licencia con el Machine ID actual

### Desarrollador: "Error al importar license_manager"

**Solución:**
```bash
# Asegúrate de ejecutar desde la raíz del proyecto:
cd C:\Users\kevin\OneDrive\Escritorio\adestock-desktop
python admin_keygen.py
```

### El límite no se aplica

**Verificar:**
1. Que el decorador esté aplicado a la vista
2. Que la fecha/hora del sistema sea correcta
3. Que el modelo `Venta` tenga el campo `completo=True` para ventas finalizadas

**Debug:**
```python
from adestock.utils.license_restrictions import check_daily_sales_limit
limite_alcanzado, ventas_hoy, mensaje = check_daily_sales_limit(3)
print(f"Límite: {limite_alcanzado}, Ventas hoy: {ventas_hoy}")
```

---

## 📝 Aplicar el Decorador a Otras Vistas

Para limitar otras funcionalidades, simplemente agrega el decorador:

### Ejemplo 1: Limitar creación de productos

```python
from adestock.utils.license_restrictions import require_pro_or_limit_sales

@login_required
@require_pro_or_limit_sales(max_free_sales=3)
def crear_producto(request):
    # Tu código aquí
```

### Ejemplo 2: Limitar con diferentes límites

```python
# 10 compras diarias en versión gratuita
@require_pro_or_limit_sales(max_free_sales=10)
def crear_compra(request):
    # Tu código aquí
```

### Ejemplo 3: Verificación manual

```python
from adestock.utils.license_restrictions import check_daily_sales_limit

def mi_vista(request):
    limite_alcanzado, ventas_hoy, mensaje = check_daily_sales_limit(3)
    
    if limite_alcanzado:
        messages.error(request, mensaje)
        return redirect('license_status')
    
    # Continuar con tu lógica
```

---

## 🎯 Checklist de Implementación

### Para el Desarrollador

- [x] ✅ Archivos creados e integrados
- [ ] 🔴 Cambiar `_SECRET_MASTER_KEY` en `license_manager.py`
- [ ] 🔴 Probar generación de licencia: `python admin_keygen.py test`
- [ ] 🔴 Verificar que `admin_keygen.py` NO esté en el instalador
- [ ] 🔴 Agregar enlace "Licencia" en menú de configuración
- [ ] 🔴 Aplicar decorador a vistas adicionales según necesites
- [ ] 🔴 (Opcional) Ofuscar código con PyArmor

### Para el Cliente (Primera Vez)

1. Abrir Adestock
2. Ir a "Configuración > Licencia"
3. Copiar Machine ID
4. Enviarlo al desarrollador
5. Recibir licencia
6. Pegar y activar
7. ✅ ¡Disfrutar versión Pro!

---

## 📞 Contacto y Soporte

Si encuentras algún problema o necesitas ayuda:

1. Revisar la sección de [Solución de Problemas](#solución-de-problemas)
2. Verificar los logs en `logs/` del proyecto
3. Ejecutar `python admin_keygen.py test` para diagnóstico

---

## 📄 Licencia del Sistema

Este sistema de licenciamiento es parte de Adestock y es propiedad exclusiva del desarrollador.

**Derechos:**
- ✅ Usar en tu aplicación Adestock
- ✅ Modificar según tus necesidades
- ✅ Generar licencias ilimitadas para clientes

**Prohibido:**
- ❌ Distribuir el código del sistema sin autorización
- ❌ Compartir `admin_keygen.py` con terceros
- ❌ Revelar la `_SECRET_MASTER_KEY`

---

**Versión del Sistema:** 1.0  
**Fecha:** Febrero 2026  
**Desarrollador:** Kevin - Adestock Desktop
