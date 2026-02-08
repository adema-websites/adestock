PROMPT_EMPAQUETADO_2.0 (MODO EXPERTO)
Actúa como un Arquitecto de Software Senior y Experto en Seguridad Python. Necesito generar la configuración para empaquetar una aplicación Django ("Adestock") para Windows, corrigiendo errores críticos de concurrencia y seguridad de versiones anteriores.

1. VARIABLES DEL PROYECTO
App Name: Adestock

Django Project Name: adestock (carpeta que contiene settings.py)

Entry Point: run_server.py

Puerto: 8250

Ruta Compartida (Datos): C:\Adestock_Data

Librerías Complejas: pandas, numpy, tablib, openpyxl, reportlab.

Carpetas de Recursos: templates, static, media, manuales, data-demo.

Hidden Imports Críticos: jazzmin, django.contrib.*, dbbackup, pystray, PIL, django.core.management.

2. INSTRUCCIONES ESTRICTAS DE GENERACIÓN
Genera el código completo para los siguientes 3 archivos.

ARCHIVO 1: run_server.py (Entry Point Robusto)
Este script es CRÍTICO. Debe evitar el error de "Fork Bomb" (ventanas infinitas).

Multiprocessing: Debes incluir multiprocessing.freeze_support() al inicio del bloque if __name__ == "__main__":.

Ejecución Django (VITAL):

PROHIBIDO usar subprocess.call o subprocess.run para iniciar Django. Esto causa recursión infinita en el EXE.

OBLIGATORIO usar from django.core.management import execute_from_command_line.

Ejecuta el servidor en un hilo (Thread) pasando los argumentos como lista: ['manage.py', 'runserver', '0.0.0.0:8250', '--noreload'].

Logging: Configura el logging para escribir en C:\Adestock_Data\debug.log. Redirige sys.stdout y sys.stderr a este archivo inmediatamente, o la app fallará en silencio al no tener consola.

Inicialización: Verifica si existe la DB en la ruta compartida. Si no, ejecuta migraciones o comando de carga inicial (adema).

ARCHIVO 2: adestock.spec (PyInstaller Seguro)
Modo: Configura onedir=True (carpeta) en lugar de onefile. Esto acelera el inicio y permite depurar archivos estáticos.

Seguridad de Código:

Al recolectar datas, asegúrate de incluir templates y static, pero NO incluyas la carpeta raíz del proyecto completa que contenga los archivos .py.

El código Python debe ir empaquetado en los binarios, no suelto como archivos .py visibles y editables por el usuario.

Librerías: Usa un bucle para collect_all de las librerías complejas (pandas, etc.).

Consola: console=False (Windowed).

ARCHIVO 3: installer.nsi (NSIS Permissions)
Nivel: RequestExecutionLevel admin.

Directorio Instalación: $PROGRAMFILES64\Adestock.

Gestión de Datos (Permisos):

Crea el directorio C:\Adestock_Data.

Usa AccessControl::Grant (o ExecWait 'icacls ...') para otorgar control total (F) a "Todos" (Everyone) sobre esa carpeta. Esto es vital para que SQLite no de error de "ReadOnly".

Uninstaller:

Borra la carpeta de Program Files.

Muestra un MessageBox preguntando si se desea borrar los DATOS (C:\Adestock_Data). Si el usuario dice NO, consérvalos.

Genera el código de los 3 archivos ahora. Asegura que las rutas y nombres de variables coincidan perfectamente entre Python y NSIS.