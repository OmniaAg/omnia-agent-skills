# Despliegue en plataformas gestionadas

**Cargar cuando:** el destino es Vercel, Netlify, Cloudflare Pages/Workers o GitHub Pages. Consultar además la guía oficial específica el día del cambio.

## Vercel

- Una salida estática de Astro no necesita configuración extra ni adaptador por defecto.
- Para renderizado bajo demanda, usar el adaptador oficial de Vercel y revisar opciones vigentes.
- Confirmar build, output, dominio, variables, previews, redirecciones y cabeceras.
- No añadir `vercel.json` salvo que exista un requisito que la configuración automática no cubra.

Fuente: [deploy en Vercel](https://docs.astro.build/en/guides/deploy/vercel/).

## Netlify

- Para una landing estática, validar comando de build y publicación de la salida generada.
- El renderizado bajo demanda y funciones requieren la integración/adaptador oficial correspondiente.
- Formularios y redirecciones de Netlify son capacidades propietarias: aislarlas y documentar portabilidad.
- Revisar versión de Node, variables, previews, cabeceras y manejo de rutas.

Fuente: [deploy en Netlify](https://docs.astro.build/en/guides/deploy/netlify/).

## Cloudflare

- Distinguir claramente Pages estático de Workers/runtime dinámico; no copiar una configuración entre ambos.
- Para on-demand usar el adaptador oficial y revisar compatibilidad de APIs de runtime, bindings y assets.
- Confirmar comando, directorio, variables/bindings, compatibilidad Node y configuración de rutas.
- No introducir APIs específicas de Workers en componentes estáticos compartidos.

Fuente: [deploy en Cloudflare](https://docs.astro.build/en/guides/deploy/cloudflare/).

## GitHub Pages

- Es hosting estático: no ofrece runtime Astro bajo demanda.
- Configurar `site` y, para sitios de proyecto, `base` según la URL del repositorio; comprobar enlaces y canonical.
- Preferir la Action oficial vigente de Astro en lugar de inventar un workflow que reinstale/configure de forma insegura.
- Definir permisos mínimos y disparador/entorno de Pages; no almacenar secretos en el workflow.

Fuente: [deploy en GitHub Pages](https://docs.astro.build/en/guides/deploy/github/).

## Reglas comunes

- No ejecutar CLI globales: usar integración Git o herramientas locales/efímeras aprobadas.
- No aceptar configuración autodetectada sin revisar modo estático, directorio y base.
- Los previews no deben emitir canonical/indexación de producción por accidente.
- Registrar configuración propietaria y alternativa de migración.
- Antes de desplegar, completar [checklist](17-validation-and-release.md).

