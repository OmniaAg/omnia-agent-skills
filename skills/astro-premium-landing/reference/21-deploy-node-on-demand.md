# Servidor Node y renderizado bajo demanda

**Cargar cuando:** una ruta necesita ejecución por petición en Node o el proveedor exige el adaptador Node.

## Puerta de arquitectura

Antes de instalar adaptador:

- Necesidad dinámica concreta y rutas afectadas.
- Por qué build, servicio externo o endpoint aislado no bastan.
- Runtime/proveedor, versión de Node, proceso, proxy, región y escalado.
- Modelo de caché, secretos, logs, salud, timeout y rollback.
- Coste operativo y propietario.

Sin estas respuestas, conservar salida estática.

## Adaptador

- Consultar la guía oficial vigente de `@astrojs/node`; los modos y opciones son sensibles a versión.
- Elegir el modo soportado (por ejemplo, proceso autónomo o integración middleware) según la infraestructura real, no por defecto histórico.
- Instalar solo con autorización y usando el gestor/lockfile existente.
- No importar dependencias exclusivas de Node en código que deba ejecutarse en edge o navegador.
- Mantener prerenderizadas las páginas que no necesitan petición cuando la configuración vigente lo permita.

## Operación obligatoria

- Ejecutar detrás de HTTPS/proxy correctamente configurado y documentar headers confiables.
- Proveer variables privadas en el entorno del proceso, con mínimo privilegio.
- Definir arranque, puerto/host, señales de cierre, reinicio, health check y logs sin secretos.
- Configurar caché y cabeceras según contenido; no asumir que un servidor Node incluye CDN.
- Servir assets de salida correctamente y verificar URLs/base.
- Probar errores, timeouts y formularios sin mostrar trazas internas.

## Seguridad

- Validar y limitar entradas en servidor; añadir CSRF/rate limit/anti-spam donde el modelo lo requiera.
- No registrar cuerpos sensibles, tokens ni variables completas.
- Revisar dependencias y superficie de endpoints.
- Separar previews y producción; rotar credenciales fuera del repositorio.

## Criterio de aceptación

La necesidad dinámica está demostrada, el adaptador coincide con runtime, las rutas estáticas siguen siendo estáticas cuando procede, build/arranque/health/error fueron probados y existe runbook/rollback.

Fuentes oficiales: [adaptador Node](https://docs.astro.build/en/guides/integrations-guide/node/), [renderizado bajo demanda](https://docs.astro.build/en/guides/on-demand-rendering/).

