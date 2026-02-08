Este es el Prompt Maestro "Empaquetado 1.0".

Lo he diseñado para que sea modular. Cuando quieras usarlo para otro proyecto en el futuro, solo tendrás que cambiar la sección de "VARIABLES DEL PROYECTO" al principio.

Está estructurado para obligar a la IA a usar buenas prácticas: bucles para las carpetas, configuración centralizada y manejo estricto de rutas compartidas.

Copia y pega el siguiente bloque en Claude Sonnet:

PROMPT_EMPAQUETADO_1.0
Actúa como un Arquitecto de Software Senior experto en Python, DevOps y entornos Windows. Tu objetivo es generar los archivos de configuración y el punto de entrada para empaquetar una aplicación Django de escritorio profesionalmente.

Voy a darte las VARIABLES DEL PROYECTO actuales y luego las REGLAS DE ARQUITECTURA que debes seguir obligatoriamente.

1. VARIABLES DEL PROYECTO (ADESTOCK)
Nombre de la App: Adestock

Nombre del Proyecto Django: adestock (nombre de la carpeta que contiene settings.py)

Puerto del Servidor: 8250

Icono: static/icono.ico

Ruta de Datos Compartida: C:\Adestock_Data (Debe ser accesible por todos los usuarios de Windows).

Librerías Complejas (requieren collect_all): pandas, numpy, tablib, openpyxl.

Carpetas a incluir: templates, static, media, manuales, logs, data-demo.

Hidden Imports Manuales: jazzmin, django.contrib.admin, django.contrib.auth, django.contrib.contenttypes, django.contrib.sessions, django.contrib.messages, django.contrib.staticfiles, django.contrib.humanize, dbbackup, pystray, PIL.

2. REGLAS DE ARQUITECTURA (LO QUE DEBES GENERAR)
Necesito que generes el código completo para 3 archivos. No expliques cada paso, entrega el código listo para producción.

ARCHIVO 1: run_server.py (El cerebro de la App)
Este script debe ser robusto y manejar la ejecución en segundo plano.

Configuración: Define SHARED_DATA_DIR apuntando a la ruta de datos compartida definida arriba.

Logging: Configura logging para escribir en SHARED_DATA_DIR/debug.log. IMPORTANTE: Redirige sys.stdout y sys.stderr a este logger, ya que la app no tendrá consola visible.

Base de Datos: Al iniciar, verifica si existe db.sqlite3 en SHARED_DATA_DIR.

Si NO existe: Ejecuta migraciones o un comando de setup inicial (ej: adema).

Si SÍ existe: Procede normalmente.

Settings: Asegura que os.environ apunte al settings.py correcto y que Django sepa buscar la DB en la ruta compartida (asume que settings.py tiene lógica para leer una variable de entorno o usa la ruta compartida si existe).

Threading: Ejecuta el servidor Django (usando runserver --noreload) en un hilo secundario (Daemon).

System Tray: Usa pystray en el hilo principal. Menú: "Abrir [Nombre App]" (abre navegador) y "Salir" (mata el proceso limpiamente con os._exit).

ARCHIVO 2: [nombre_proyecto].spec (Configuración PyInstaller Modular)
No quiero código espagueti. Usa un enfoque basado en listas para facilitar el mantenimiento.

Estructura:

Define una lista COMPLEX_LIBS con las librerías complejas. Itera sobre ella usando collect_all para llenar datas, binaries y hiddenimports.

Define una lista DIRS_TO_INCLUDE con las carpetas. Itera sobre ella para añadir recursivamente a datas, verificando si existen con os.path.exists para evitar errores.

Define una lista MANUAL_HIDDEN_IMPORTS para las apps de Django.

Configuración EXE: Establece estrictamente console=False (Windowed mode).

Icono: Asegura la inclusión del archivo .ico.

ARCHIVO 3: installer.nsi (Script NSIS)
El instalador debe garantizar que la app funcione para cualquier usuario del PC.

Privilegios: RequestExecutionLevel admin.

Instalación: En $PROGRAMFILES64\[Nombre App].

Gestión de Datos (CRÍTICO):

Crea el directorio definido en "Ruta de Datos Compartida" (ej: C:\Adestock_Data).

Permisos: Usa AccessControl::Grant o ejecuta icacls para dar permisos de "Control Total" (Full Control) a "Todos" (Everyone) o "Usuarios" (Users) sobre esa carpeta. Esto es vital para evitar errores de "ReadOnly database".

Accesos Directos: Escritorio y Menú Inicio.

Desinstalador:

Borra la carpeta de la aplicación en Archivos de Programa.

Pregunta de Seguridad: Muestra un MessageBox preguntando al usuario si desea borrar también la base de datos y logs en C:\Adestock_Data. Solo bórrala si el usuario dice "Sí".

Genera los tres archivos (run_server.py, adestock.spec, installer.nsi) ahora, asegurando consistencia total en los nombres de rutas y variables entre ellos.