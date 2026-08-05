# Hosting estático, Apache y Hostinger

**Cargar cuando:** el destino confirmado recibe archivos estáticos, usa Apache o es Hostinger. Es un módulo opcional; no representa un requisito de Astro.

## Hosting estático tradicional

1. Mantener salida estática y construir con el gestor/lockfile del proyecto.
2. Verificar que el directorio de salida contiene HTML, assets y rutas esperadas.
3. Confirmar si el hosting sirve dominio raíz o subdirectorio; ajustar `site`/`base` antes del build.
4. Transferir el contenido de la salida, no el código fuente ni `node_modules`.
5. Verificar MIME, HTTPS, rutas profundas, 404, caché, compresión y permisos desde el servidor real.

## Hostinger

Hostinger es un destino posible, no la arquitectura de la skill. Seguir la guía oficial de Astro y la documentación vigente del plan de Hostinger elegido. No asumir que todos los planes ofrecen Node, CI, reglas Apache o el mismo panel.

Para salida estática, la guía vigente puede permitir integración Git/auto-deploy o carga de `dist/`; confirmar directorio público, comando de build y versión de Node. Para dinámica, confirmar primero que el producto soporta el runtime y adaptador requeridos.

Fuente: [deploy en Hostinger](https://docs.astro.build/en/guides/deploy/hostinger/).

## Apache

`templates/htaccess.template` es opcional y solo para servidores Apache compatibles que permiten overrides.

Antes de usarla:

- Confirmar `mod_rewrite`, `mod_headers`/`mod_expires` si se usan y política `AllowOverride`.
- Sustituir valores marcados de base/error documentadamente.
- No aplicar reglas SPA que devuelvan `index.html` para todas las URLs: una exportación Astro multipágina debe servir sus archivos y 404 reales.
- No cachear HTML indefinidamente; assets con hash pueden usar caché larga.
- Probar en staging. Un error de `.htaccess` puede provocar HTTP 500.

No usar esta plantilla en Vercel, Netlify, Cloudflare Pages, GitHub Pages o servidores que no sean Apache.

## Redirecciones y rutas

- Colocar redirecciones en la capa del proveedor/servidor y preservar query strings cuando corresponda.
- Evitar cadenas/bucles, redirecciones internas a dominio preview y reglas específicas de una marca dentro de la skill.
- Para un sitio bajo subruta, resolver `base` en Astro antes que reescribir cada asset en Apache.

## Caché y rollback

- Versionar/configurar reglas junto al proyecto solo si el servidor realmente las consume.
- Guardar copia de configuración activa y lista de archivos desplegados mediante el proceso del operador.
- Definir rollback recuperable antes de reemplazar producción.

