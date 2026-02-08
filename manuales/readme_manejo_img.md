# Manejo y Optimización de Imágenes en Django

Este documento detalla la implementación utilizada para optimizar, redimensionar y asegurar el almacenamiento de imágenes de usuario en el sistema. 

El objetivo principal es reducir drásticamente el espacio en disco, estandarizar los formatos y evitar conflictos de nombres de archivo.

## Características Principales

1.  **Conversión a WebP**: Todas las imágenes se convierten automáticamente al formato moderno WebP, que ofrece una compresión superior con mínima pérdida de calidad.
2.  **Redimensionado Automático**: Las imágenes que superan un ancho máximo (ej. 1200px) son redimensionadas proporcionalmente.
3.  **Renombrado Seguro**: Se descarta el nombre de archivo original y se genera uno nuevo usando un UUID (identificador único universal) para evitar problemas de codificación de caracteres, espacios o duplicados.
4.  **Procesamiento Inteligente**: La optimización solo ocurre cuando se sube una nueva imagen o se cambia una existente, evitando re-procesamientos innecesarios.

## Requisitos Previos

Asegúrate de tener instalada la librería `Pillow` en tu entorno virtual:

```bash
pip install Pillow
```

## Implementación

### 1. Función de Utilidad (`utils.py`)

Crea un archivo de utilidad (por ejemplo en `conf/utils.py` o `core/utils.py`) con la siguiente función lógica. Esta función encapsula toda la magia de procesamiento.

```python
import uuid
import sys
from io import BytesIO
from PIL import Image, ImageOps
from django.core.files.base import ContentFile

def compress_and_rename_image(image_file, max_width=1200, quality=85):
    """
    Recibe un archivo de imagen (FieldFile o InMemoryUploadedFile),
    lo redimensiona, lo convierte a WebP y le asigna un nombre UUID seguro.
    Retorna un ContentFile listo para ser asignado al campo.
    """
    if not image_file:
        return None

    try:
        # 1. Abrir la imagen con Pillow
        img = Image.open(image_file)
        
        # 2. Corregir orientación EXIF (evita que fotos de celular salgan rotadas)
        img = ImageOps.exif_transpose(img)

        # 3. Convertir a RGB si es necesario (Pillow no guarda RGBA/P en WebP/JPEG directamente a veces sin conflictos)
        # Para WebP con transparencia, RGBA es válido, pero para máxima compatibilidad o si se fuera a JPG, usar RGB.
        # En este caso, si quieres conservar transparencia en WebP, puedes quitar 'RGBA' de esta lista,
        # pero asegurar que el formato de salida soporte transparencia.
        if img.mode in ('P',): 
             img = img.convert('RGB')
        # Si la imagen es RGBA (tiene transparencia) y queremos fondo blanco (opcional):
        # if img.mode == 'RGBA':
        #     background = Image.new('RGB', img.size, (255, 255, 255))
        #     background.paste(img, mask=img.split()[3])
        #     img = background

        # 4. Redimensionar si es muy grande (manteniendo aspecto)
        if img.width > max_width:
            ratio = max_width / img.width
            new_height = int(img.height * ratio)
            img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)

        # 5. Guardar en memoria (BytesIO)
        output = BytesIO()
        # Se guarda forzando formato WEBP
        img.save(output, format='WEBP', quality=quality)
        output.seek(0)

        # 6. Generar nuevo nombre seguro
        new_filename = f"{uuid.uuid4()}.webp"

        # 7. Retornar objeto ContentFile de Django
        return ContentFile(output.read(), name=new_filename)

    except Exception as e:
        # En caso de error, loguear y devolver la imagen original sin tocar
        print(f"Error comprimiendo imagen: {e}")
        return image_file
```

### 2. Integración en el Modelo (`models.py`)

En cualquier modelo donde tengas un `ImageField`, debes sobrescribir el método `save()`.

```python
from django.db import models
from .utils import compress_and_rename_image # Importa tu función

class MiModelo(models.Model):
    nombre = models.CharField(max_length=100)
    imagen = models.ImageField(upload_to='carpeta_destino/', blank=True, null=True)

    def save(self, *args, **kwargs):
        # Lógica para detectar si la imagen ha cambiado o es nueva
        process_image = False
        
        if self.imagen:
            if not self.pk:
                # Es un objeto nuevo con imagen
                process_image = True
            else:
                # Es una edición, verificamos si la imagen cambió
                try:
                    old_obj = MiModelo.objects.get(pk=self.pk)
                    if old_obj.imagen != self.imagen:
                        process_image = True
                except MiModelo.DoesNotExist:
                    process_image = True
        
        # Si se requiere procesar
        if process_image:
            new_image = compress_and_rename_image(self.imagen)
            if new_image:
                self.imagen = new_image
        
        # Llamar al save del padre
        super().save(*args, **kwargs)
```

## Configuración Opcional

Si tienes un servidor web (Nginx/Apache), asegúrate de que sirva correctamente los tipos MIME para `.webp`, aunque hoy en día es estándar.

El valor `max_width=1200` y `quality=85` en la función de utilidad se pueden ajustar según las necesidades del proyecto (e.g., e-commerce vs blog).

---

Implementado originalmente en **Labisol** para optimización de almacenamiento.
