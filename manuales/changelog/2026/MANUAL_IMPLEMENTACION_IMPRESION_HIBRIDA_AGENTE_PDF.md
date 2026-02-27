# Manual de Implementación: Impresión Híbrida (PDF Web + Agente Local)

Este documento resume la implementación completa que quedó funcionando para alternar entre:

- Modo PDF (navegador web)
- Modo Agente Local (cola cloud print_queue + app local AGENTE_PRINTER)

La solución permite operar en nube sin depender de CUPS/impresoras locales en el servidor.

---

## 1. Objetivo funcional

Se implementó un esquema híbrido para tickets de venta:

- Si Configuración > "Usar Comandera" está desactivado:
  - el sistema devuelve/abre ticket en PDF (comportamiento web clásico).

- Si "Usar Comandera" está activado:
  - el backend NO imprime localmente,
  - encola un PrintJob en print_queue,
  - el agente instalado en la PC local consume e imprime.

Resultado: se evita el error típico en cloud Linux: failed to connect to server (CUPS/socket local).

---

## 2. Arquitectura final

### 2.1 Backend cloud

- App print_queue expone API de cola:
  - POST /api/print/v1/agents/heartbeat
  - POST /api/print/v1/jobs/next
  - POST /api/print/v1/jobs/<job_id>/start
  - POST /api/print/v1/jobs/<job_id>/result

- Cada job se enruta por credencial store_id + pos_id.
- El backend guarda inventario de impresoras reportado por agente.

### 2.2 Agente local (AGENTE_PRINTER)

- Corre en Windows en la PC que tiene impresora.
- Hace heartbeat y polling de jobs.
- Imprime USB (win32print) o LAN (TCP 9100).
- Reporta SUCCESS/FAILED al backend.

### 2.3 Admin / Diagnóstico

- En admin print_queue/printagent:
  - acción para testear conexión + listar inventario,
  - columna Diagnóstico con acceso rápido,
  - endpoint seguro de diagnóstico staff-only.

---

## 3. Cambios aplicados en backend

### 3.1 print_queue: acciones y diagnóstico seguro

Se incorporó:

1) Acción admin en PrintAgent:
- Testea online/offline según last_seen_at.
- Sincroniza status ONLINE/OFFLINE.
- Muestra inventario USB/LAN detectado.

2) Ingesta robusta de inventario en heartbeat:
- Acepta printers tradicional.
- Acepta también usb_printers/lan_printers en raíz.

3) Snapshot seguro de heartbeat:
- Nuevos campos en PrintAgent:
  - last_heartbeat_snapshot
  - last_heartbeat_snapshot_at
- Guarda resumen saneado (sin exponer secretos).

4) Endpoint staff-only de diagnóstico:
- GET /api/print/v1/admin/agents/<agent_id>/heartbeat-diagnostic/
- Incluye cache-control no-store.

Migración asociada:
- print_queue/migrations/0007_printagent_heartbeat_snapshot_fields.py

### 3.2 Venta: switch real PDF vs Agente

Se cambió el flujo para usar el toggle existente Configuracion.tiket_comandera:

- tiket_comandera = False:
  - mantiene modo PDF.

- tiket_comandera = True:
  - encola ticket a print_queue (no impresión local del servidor).

Se implementó helper en venta/views.py para:

- construir payload ESC/POS base64,
- resolver destino printer_target (USB/LAN) según ConfiguracionImpresora de caja,
- obtener credencial activa PrintAgentCredential de esa caja,
- crear PrintJob con idempotency_key.

Flujos impactados:

- imprimir_ticket
- cierre de venta POS (autoimpresión)
- pos_reimprimir_ultimo_ticket
- imprimir_ticket_admin

---

## 4. Cambios aplicados en AGENTE_PRINTER (app instalable local)

Ruta de proyecto:
- AGENTE_PRINTER/

### 4.1 api_client.py

- heartbeat ahora acepta inventario opcional:
  - heartbeat(printers=...)
- Si se pasa inventario, envía payload con printers.

### 4.2 worker.py

Se agregó gestión de inventario en runtime:

- detección periódica de impresoras Windows,
- cache interno de inventario,
- envío de inventario junto al heartbeat,
- request_inventory_refresh para forzar refresh inmediato,
- evento inventory_updated para UI/log.

### 4.3 ui.py

Botón Actualizar impresoras quedó integrado a cloud:

- detecta impresoras localmente,
- si el worker está corriendo, solicita refresh inmediato al worker,
- acelera envío al backend (sin esperar ciclo largo).

Resultado observado:
- en admin ya aparecen USB detectadas correctamente.

---

## 5. Seguridad aplicada

1) API con Bearer token por credencial activa (PrintAgentCredential).
2) Validación store_id/pos_id contra credencial.
3) Endpoint diagnóstico restringido a staff.
4) Snapshot de heartbeat saneado (sin volcar secretos).
5) Respuesta diagnóstico con no-store.

Recomendaciones de producción:
- HTTPS obligatorio.
- Rotación periódica de API keys por caja.
- Desactivar credenciales no usadas (is_active=False).

---

## 6. Cómo operar (día a día)

### 6.1 Elegir modo de impresión

En Admin > Agenda > Configuración:

- Usar Comandera OFF -> PDF en web.
- Usar Comandera ON -> cola + agente local.

### 6.2 Requisitos para modo agente

1) Caja con ConfiguracionImpresora válida:
- USB: nombre_impresora (o inventario USB del agente).
- RED: ip_impresora y puerto.

2) Credencial activa en Print queue > Print agent credentials:
- vinculada a la caja,
- con store_id y pos_id correctos.

3) Agente local corriendo con misma identidad store_id + pos_id.

### 6.3 Verificación rápida

1) En monitor del agente: Iniciar agente + Actualizar impresoras.
2) En admin PrintAgent: acción testear conexión.
3) Revisar Diagnóstico por fila para snapshot heartbeat.
4) Imprimir ticket desde POS/admin y validar job consumido.

---

## 7. Troubleshooting

### Caso A: agente ONLINE pero USB/LAN en 0

- Verificar que agente actualizado incluya envío de printers.
- Presionar Actualizar impresoras con worker activo.
- Consultar endpoint de diagnóstico del agente.

### Caso B: Unauthorized en /agents/heartbeat

- api_key incorrecta o desactivada.
- store_id/pos_id no coincide con credencial.

### Caso C: no imprime y antes aparecía failed to connect to server

- Confirmar que Usar Comandera está ON para usar agente.
- Si está OFF, comportamiento esperado es PDF (no impresión directa).

### Caso D: job queda en cola

- Revisar agente local activo.
- Validar coincidencia store_id + pos_id en credencial y config del agente.
- Revisar logs de agente y estado job en admin.

---

## 8. Despliegue y actualización

### Backend

1) Aplicar migraciones:
- python manage.py migrate

2) Reiniciar servicio web.

### Agente local

1) Reempaquetar versión AGENTE_PRINTER actualizada.
2) Instalar en PC de caja.
3) Verificar config.yaml (cloud_base_url, api_key, store_id, pos_id, agent_name).
4) Ejecutar UI y confirmar heartbeat + inventario.

---

## 9. Estado final

La implementación quedó operativa y validada en pruebas:

- Alternancia PDF vs Agente funcional.
- Inventario de impresoras subiendo correctamente al backend.
- Diagnóstico seguro disponible en admin.
- Flujo de impresión cloud desacoplado de CUPS/impresora local del servidor.
