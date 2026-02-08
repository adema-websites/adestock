"""
EJEMPLOS DE USO - Sistema de Licenciamiento Adestock
=====================================================

Este archivo contiene ejemplos prácticos de cómo usar el sistema de licencias
en diferentes partes de tu aplicación Django.
"""

# =============================================================================
# EJEMPLO 1: Limitar ventas diarias (Ya implementado en venta/views.py)
# =============================================================================

from django.contrib.auth.decorators import login_required
from adestock.utils.license_restrictions import require_pro_or_limit_sales

@login_required
@require_pro_or_limit_sales(max_free_sales=3)
def pos_cerrar_venta(request):
    """
    Esta vista está protegida por el sistema de licencias.
    
    - Versión Gratuita: Máximo 3 ventas por día
    - Versión Pro: Ventas ilimitadas
    
    Si el límite se alcanza:
    - Para AJAX: Retorna JSON con error 403
    - Para web: Redirige a página de activación de licencia
    """
    # Tu código de venta aquí
    pass


# =============================================================================
# EJEMPLO 2: Verificación manual en cualquier vista
# =============================================================================

from adestock.utils.license_restrictions import check_daily_sales_limit
from django.contrib import messages
from django.shortcuts import redirect

def mi_vista_personalizada(request):
    """
    Si necesitas lógica personalizada para manejar el límite.
    """
    # Verificar límite con configuración personalizada
    limite_alcanzado, ventas_hoy, mensaje = check_daily_sales_limit(max_sales=5)
    
    if limite_alcanzado:
        messages.error(request, mensaje)
        messages.info(request, '¡Actualiza a Pro para eliminar restricciones!')
        return redirect('license_status')
    
    # Continuar con tu lógica normal
    messages.info(request, f'Has realizado {ventas_hoy} ventas hoy. Todo bien!')
    # ... resto de tu código


# =============================================================================
# EJEMPLO 3: Verificar tipo de licencia para mostrar/ocultar funciones
# =============================================================================

from adestock.utils.license_manager import is_pro_license

def vista_con_funciones_premium(request):
    """
    Muestra diferentes opciones según el tipo de licencia.
    """
    es_pro = is_pro_license()
    
    context = {
        'is_pro': es_pro,
        'puede_exportar_excel': es_pro,  # Solo Pro exporta a Excel
        'puede_enviar_email': es_pro,    # Solo Pro envía emails
        'limite_productos': None if es_pro else 100,  # Pro = ilimitado
    }
    
    return render(request, 'mi_template.html', context)


# =============================================================================
# EJEMPLO 4: En un Template HTML - Mostrar badges según licencia
# =============================================================================

"""
En cualquier template Django (.html):

{% load static %}

<!-- Badge de tipo de licencia -->
<div class="alert alert-{% if is_pro_license %}success{% else %}warning{% endif %}">
    {% if is_pro_license %}
        <i class="fas fa-star"></i> Versión PRO Activa
    {% else %}
        <i class="fas fa-info-circle"></i> Versión Gratuita
        <a href="{% url 'license_status' %}">Actualizar a Pro</a>
    {% endif %}
</div>

<!-- Botón deshabilitado para funciones Pro -->
<button class="btn btn-primary" 
        {% if not is_pro_license %}disabled title="Solo disponible en versión Pro"{% endif %}>
    Exportar Reporte Avanzado
</button>
"""


# =============================================================================
# EJEMPLO 5: Limitar otras funcionalidades (no solo ventas)
# =============================================================================

from adestock.utils.license_manager import get_license_manager

def vista_crear_producto(request):
    """
    Limitar número de productos en versión gratuita.
    """
    manager = get_license_manager()
    
    if not manager.is_valid():
        # Versión gratuita: máximo 50 productos
        from producto.models import Producto
        count = Producto.objects.count()
        
        if count >= 50:
            messages.error(
                request,
                '🔒 Límite de 50 productos alcanzado en versión Gratuita. '
                'Actualiza a Pro para productos ilimitados.'
            )
            return redirect('license_status')
    
    # Continuar con creación de producto
    # ...


# =============================================================================
# EJEMPLO 6: API REST - Verificar licencia en endpoints
# =============================================================================

from django.http import JsonResponse
from adestock.utils.license_restrictions import check_daily_sales_limit

def api_crear_venta(request):
    """
    Endpoint API que verifica el límite antes de crear venta.
    """
    if request.method == 'POST':
        # Verificar límite
        limite_alcanzado, ventas_hoy, mensaje = check_daily_sales_limit(3)
        
        if limite_alcanzado:
            return JsonResponse({
                'success': False,
                'error': 'LIMIT_REACHED',
                'message': mensaje,
                'ventas_realizadas': ventas_hoy,
                'upgrade_url': '/license/'
            }, status=403)
        
        # Procesar venta
        # ...
        
        return JsonResponse({
            'success': True,
            'venta_id': 123,
            'ventas_restantes': 3 - ventas_hoy - 1
        })


# =============================================================================
# EJEMPLO 7: Middleware personalizado (avanzado)
# =============================================================================

"""
Si quieres aplicar restricciones globalmente, crea un middleware:

# En adestock/middleware.py

from django.shortcuts import redirect
from django.contrib import messages
from adestock.utils.license_restrictions import check_daily_sales_limit

class LicenseLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.protected_paths = ['/venta/', '/pos/']  # Paths a proteger
    
    def __call__(self, request):
        # Verificar si la ruta está protegida
        if any(request.path.startswith(path) for path in self.protected_paths):
            limite_alcanzado, _, mensaje = check_daily_sales_limit(3)
            
            if limite_alcanzado:
                messages.error(request, mensaje)
                return redirect('license_status')
        
        response = self.get_response(request)
        return response

# Agregar en settings.py:
MIDDLEWARE = [
    # ... otros middlewares
    'adestock.middleware.LicenseLimitMiddleware',
]
"""


# =============================================================================
# EJEMPLO 8: Context Processor - Datos de licencia en todos los templates
# =============================================================================

"""
Ya incluido en adestock/views_license.py

Para usarlo, agregar en settings.py:

TEMPLATES = [{
    'OPTIONS': {
        'context_processors': [
            # ... otros processors
            'adestock.views_license.license_context_processor',
        ],
    },
}]

Ahora en CUALQUIER template tienes disponible:
- {{ is_pro_license }}  → True/False
- {{ license_type }}    → 'PRO' o 'GRATUITA'
"""


# =============================================================================
# EJEMPLO 9: Signal para notificar cuando se activa licencia
# =============================================================================

"""
# En adestock/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver, Signal

# Signal personalizado
license_activated = Signal()

@receiver(license_activated)
def on_license_activated(sender, **kwargs):
    # Enviar email de bienvenida
    # Habilitar funciones premium
    # Registrar en logs
    print("¡Licencia Pro activada!")

# Para emitir el signal desde views_license.py:
from adestock.signals import license_activated

def activate_license(request):
    # ... después de guardar licencia exitosamente
    license_activated.send(sender=request.user.__class__, user=request.user)
"""


# =============================================================================
# EJEMPLO 10: Test unitario del sistema de licencias
# =============================================================================

"""
# En tests/test_licensing.py

from django.test import TestCase
from adestock.utils.license_manager import LicenseManager

class LicensingTestCase(TestCase):
    
    def test_machine_id_generation(self):
        manager = LicenseManager()
        machine_id = manager.get_machine_id()
        
        # Machine ID debe ser SHA-256 (64 caracteres hex)
        self.assertEqual(len(machine_id), 64)
        self.assertTrue(all(c in '0123456789abcdef' for c in machine_id))
    
    def test_license_validation(self):
        manager = LicenseManager()
        machine_id = manager.get_machine_id()
        
        # Generar licencia válida
        license_key = manager.generate_license_key(machine_id)
        
        # Debe ser válida
        self.assertTrue(manager.verify_license_key(license_key, machine_id))
        
        # Licencia falsa debe ser inválida
        self.assertFalse(manager.verify_license_key('FAKE_LICENSE', machine_id))
    
    def test_daily_limit(self):
        from adestock.utils.license_restrictions import check_daily_sales_limit
        
        # Sin licencia, debe verificar límite
        limite, ventas, msg = check_daily_sales_limit(3)
        self.assertIsInstance(limite, bool)
        self.assertIsInstance(ventas, int)
"""


# =============================================================================
# RESUMEN DE FUNCIONES PRINCIPALES
# =============================================================================

"""
MÓDULO: adestock.utils.license_manager
---------------------------------------
- get_license_manager()         → Obtener instancia del gestor
- is_pro_license()              → bool: ¿Es licencia Pro?
- get_machine_id()              → str: Machine ID del sistema
- get_license_status()          → dict: Info completa

MÓDULO: adestock.utils.license_restrictions
--------------------------------------------
- @require_pro_or_limit_sales(N)     → Decorador para limitar ventas
- check_daily_sales_limit(N)         → Verificación manual
- get_license_info_for_template()    → Info para templates

VISTAS: adestock.views_license
-------------------------------
- license_status            → Página de gestión de licencia
- activate_license          → Activar licencia (POST)
- deactivate_license        → Desactivar (solo admin)
- get_machine_id_json       → API: obtener Machine ID
- check_license_status_json → API: verificar estado

URLS DISPONIBLES:
-----------------
/license/                   → Página de gestión
/license/activate/          → Activar (POST)
/license/deactivate/        → Desactivar (POST)
/api/license/machine-id/    → JSON: Machine ID
/api/license/status/        → JSON: Estado
"""
