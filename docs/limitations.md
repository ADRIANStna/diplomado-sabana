# Limitaciones

El sistema se despliega en **staging**, no en producción. Este documento crece con cada clase y se cierra en la clase 18.

## Fuera de alcance

- SLA contractual.
- Alta disponibilidad.
- Recuperación ante desastres multirregión.
- Operación 24/7.
- Certificaciones de seguridad.
- OAuth2/OIDC completo con proveedor externo.
- Escalado horizontal del servicio de ejecución.

## Limitaciones conocidas por clase

| Clase | Limitación |
|---|---|
| 7 | Almacenamiento en memoria: los datos se pierden al reiniciar el backend (se reemplaza en la clase 8). |
| 7 | Identidad temporal por cabecera `X-User-Id`; no es un control de seguridad (se reemplaza en la clase 10). |
