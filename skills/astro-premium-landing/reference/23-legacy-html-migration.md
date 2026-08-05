# Migración desde HTML/CSS/JavaScript tradicional

**Cargar cuando:** el origen es un sitio estático, una plantilla Hostinger/Apache o un documento HTML monolítico.

## Inventario previo

- Páginas, rutas, canonical y redirecciones existentes.
- Header/footer, secciones repetidas y contenido estructurable.
- Hojas globales, especificidad, variables, media queries y fuentes.
- Scripts, selectores, estado, eventos globales, librerías/CDN y orden de carga.
- Assets, rutas relativas, licencias y configuración de servidor.
- Formularios, analítica, integraciones y comportamiento sin JavaScript.

## Mapeo

| Legado | Astro |
|---|---|
| `index.html` y otras páginas | Archivos de ruta en `src/pages/` |
| Documento repetido | Layout en `src/layouts/` |
| Header/footer/secciones | Componentes `.astro` |
| Datos repetidos en markup | Arrays/objetos tipados o colección justificada |
| CSS del sitio | Tokens/global estrecho + estilos locales graduales |
| JS IIFE global | Script nativo acotado o isla justificada |
| Carpeta pública | Clasificar entre `src/assets/` y `public/` |
| `.htaccess` | Configuración opcional de Apache, separada del proyecto Astro |

## Orden seguro

1. Preservar contenido, rutas y apariencia de referencia antes de abstraer.
2. Crear layout/documento y primera ruta.
3. Extraer secciones con responsabilidad clara y props tipadas.
4. Clasificar assets y corregir imports/URLs.
5. Migrar estilos sin reescritura total: tokens, base global y scopes locales.
6. Reimplementar cada interacción con HTML/CSS/JS mínimo; retirar inicializaciones duplicadas.
7. Migrar SEO, formularios, analítica y redirecciones explícitamente.
8. Comparar build y comportamiento; retirar archivos legacy solo dentro del alcance y con recuperación.

## Prohibido trasladar literalmente

- Documentos completos dentro de componentes, header/footer duplicados o HTML inyectado por JavaScript.
- Manipulación global del DOM, scripts en todas las rutas o dependencia incidental del orden.
- `document`/`window` en frontmatter.
- Rutas `../` frágiles, URLs `/src/assets/` o imports desde `public/`.
- CDNs sin revisión, `.htaccess` obligatorio, configuración Hostinger universal.
- React/Tailwind/hidratación como sustitución automática del legado.

## Compatibilidad temporal

No mantener dos inicializadores activos para la misma interacción. Si existe una migración gradual, definir propiedad por ruta/componente y una fecha/criterio de retirada.

## Criterio de aceptación

Paridad de contenido/rutas acordada, arquitectura Astro real, CSS y JS acotados, SEO y formularios conservados, assets clasificados y legacy restante documentado.

Revisar [gotchas](10-critical-astro-gotchas.md), [interactividad](08-native-interactivity.md) y [Apache opcional](20-deploy-static-apache-hostinger.md).

