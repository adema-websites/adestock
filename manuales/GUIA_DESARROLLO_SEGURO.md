# 🛡️ Guía de Desarrollo Seguro y Ciclo de Vida

Este documento detalla el procedimiento correcto para trabajar con los módulos críticos del sistema de licencias, los cuales están protegidos mediante compilación nativa (Cython) para evitar la ingeniería inversa.

---

## 📂 Archivos Protegidos

Los siguientes archivos contienen lógica sensible y **NO existen como `.py`** en el entorno de producción/compilación final. Se convierten a binarios `.pyd` (Windows DLLs).

1. `adestock/utils/license_manager.py` (Lógica central y Keys)
2. `adestock/utils/license_restrictions.py` (Decoradores de validación)

---

## 🔄 Ciclo de Trabajo (Paso a Paso)

### 1️⃣ FASE DE DESARROLLO (Modo Editable)
Para corregir bugs, añadir funciones o cambiar la lógica de licencias, necesitas restaurar los archivos a su formato original Python.

**Pasos:**
1. Abre una terminal en la raíz del proyecto.
2. Ejecuta el script de restauración:
   ```powershell
   python toggle_dev_mode.py
   ```
3. **Verifica:** Verás que los archivos `.pyd` desaparecen y aparecen nuevamente `license_manager.py` y `license_restrictions.py`.
4. **Edita:** Realiza tus cambios en el código `.py` normalmente.
5. **Prueba:** Ejecuta el servidor (`python manage.py runserver`) para verificar que todo funciona.

> **Nota:** Django funciona perfectamente con los archivos `.py` restaurados.

---

### 2️⃣ FASE DE PRODUCCIÓN (Modo Blindado)
Antes de generar el instalador o distribuir una actualización, DEBES compilar de nuevo los módulos críticos.

**Pasos:**
1. Asegúrate de haber guardado todos tus cambios.
2. Detén cualquier servidor en ejecución.
3. Ejecuta el script de compilación:
   ```powershell
   python compile_core.py
   ```
   *Esto generará los archivos `.pyd` compilados y ocultará los `.py` renombrándolos a `.src`.*

4. **Verifica:** Asegúrate de recibir el mensaje `[SUCCESS] Compilación exitosa`.

---

### 3️⃣ FASE DE EMPAQUETADO (Build)
Una vez que el sistema está en "Modo Blindado", puedes generar el ejecutable.

**Pasos:**
1. Ejecuta PyInstaller con el spec seguro:
   ```powershell
   pyinstaller adestock_secure.spec --clean --noconfirm
   ```
2. El ejecutable resultante en `dist/Adestock/` contendrá la lógica de licencias compilada e ilegible para humanos.

---

## ⚠️ Resumen Rápido de Comandos

| Acción | Comando |
|--------|---------|
| **🔓 HABILITAR EDICIÓN** | `python toggle_dev_mode.py` |
| **🔒 BLINDAR CÓDIGO** | `python compile_core.py` |
| **📦 CREAR EXE** | `pyinstaller adestock_secure.spec --clean` |

---

## 🚫 Solución de Problemas

**Error: "ModuleNotFoundError: No module named 'adestock.utils.license_manager'"**
- **Causa:** Probablemente tienes los archivos en `.src` pero no se generaron los `.pyd` (falló la compilación) o borraste los `.pyd` sin restaurar los `.py`.
- **Solución:** Ejecuta `python toggle_dev_mode.py` para recuperar los originales.

**Error: "ImportError: dynamic module does not define module export function"**
- **Causa:** Incompatibilidad de versiones de Python/Cython.
- **Solución:** Borra la carpeta `build/` temporal y recompila con `python compile_core.py`.
