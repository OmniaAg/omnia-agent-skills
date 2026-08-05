# Despliegue: decisión general

**Cargar cuando:** se elige hosting, se configura `site`/`base`, se prepara producción o se considera un adaptador.

## Primera decisión: estático o bajo demanda

### Estático por defecto

Una landing que puede generarse durante build no necesita adaptador. El flujo habitual produce `dist/`, que puede servirse como archivos estáticos en múltiples proveedores.

Ventajas: menor superficie operativa, caché sencilla, portabilidad y menos ejecución de servidor.

### Bajo demanda

Usarlo solo para rutas con necesidad por petición. Requiere un adaptador compatible con el runtime/proveedor y revisión de secretos, caché, región, logs, límites y rollback. Consultar [Node y on-demand](21-deploy-node-on-demand.md).

## Matriz

| Destino | Estático | Bajo demanda |
|---|---|---|
| Vercel/Netlify/Cloudflare | Generalmente sin adaptador para archivos estáticos | Adaptador oficial del proveedor según guía vigente |
| GitHub Pages | Sí | No como runtime de servidor |
| Hosting estático/Hostinger | Sí, subir salida | Depende de un producto/runtime separado; no asumir |
| Apache | Sí, servir salida; `.htaccess` opcional | Astro no se convierte en PHP/Apache por una regla de rewrite |
| Servidor Node | Puede servir archivos, pero suele ser innecesario | Adaptador Node y proceso gestionado |

## Configuración portable

- Mantener UI, contenido y rutas libres de APIs propietarias cuando no sean necesarias.
- Definir `site` con URL de producción confirmada.
- Definir `base` para subruta real (por ejemplo, ciertos GitHub Pages); probar enlaces, assets y canonical.
- Gestionar redirecciones, cabeceras y caché en un módulo/configuración del destino, no dentro de componentes.
- Mantener variables por entorno en el proveedor; nunca versionar secretos.
- Documentar directorio de salida, versión de Node, comando de build y gestor/lockfile.

## Formularios

- Un servicio gestionado puede conservar la landing estática.
- Funciones/Actions/endpoints requieren destino compatible, adaptación y validación oficial.
- No asumir que formularios especiales de un proveedor funcionan en otro.

## Validación previa

1. Ejecutar type checking y build con dependencias ya instaladas.
2. Inspeccionar salida: rutas, base, canonical, OG, sitemap, robots y assets.
3. Servir la salida como lo hará el destino y probar 404/refresh/rutas profundas.
4. Confirmar variables, redirecciones, cabeceras, caché, formularios y límites.
5. Probar preview; desplegar producción solo con autorización.

Fuente oficial: [despliegue de Astro](https://docs.astro.build/en/guides/deploy/), [renderizado bajo demanda](https://docs.astro.build/en/guides/on-demand-rendering/).

