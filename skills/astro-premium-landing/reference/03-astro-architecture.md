# Stack, convenciones y arquitectura Astro

**Cargar cuando:** se inicializa, reorganiza o migra una landing; se crean rutas; se decide renderizado.

## Convenciones obligatorias

| Ruta | Responsabilidad |
|---|---|
| `src/pages/` | Rutas basadas en archivos y endpoints necesarios. |
| `src/layouts/` | Shells reutilizables, estructura documental y metadatos consistentes. |
| `src/components/` | Secciones y piezas reutilizables sin crear rutas. |
| `src/styles/` | Tokens, reset y estilos compartidos cuando aportan valor. |
| `src/assets/` | Imágenes y recursos importados que Astro/Vite deben procesar. |
| `public/` | Archivos copiados sin procesamiento y referidos por URL desde la raíz/base. |

- Usar `.astro` como componente predeterminado y TypeScript en frontmatter.
- Mantener un único documento semántico por página: no pegar `<html>`, `<head>` o `<body>` dentro de secciones.
- Componer header, footer y SEO mediante layouts/componentes; no duplicarlos por ruta.
- Tipar `Props` y datos; validar contenido externo en el límite adecuado.
- Modelar listas repetidas con datos y `.map()`, con claves/identidad conceptual estable.
- Conservar la ruta como responsabilidad de la página y la presentación como responsabilidad de componentes.

## Renderizado

La salida estática es la decisión inicial para una landing. Solo elegir renderizado bajo demanda si existe al menos una necesidad que no puede resolverse en build o en un servicio externo apropiado: autenticación por petición, contenido personalizado, secreto de servidor en tiempo real o mutación controlada.

Antes de cambiar el modo:

1. Documentar necesidad, rutas afectadas, caché, coste y alternativa estática.
2. Consultar la guía oficial vigente de renderizado bajo demanda y del adaptador.
3. Seleccionar proveedor/runtime; después instalar únicamente su adaptador autorizado.
4. Mantener prerenderizadas las rutas que no necesitan servidor cuando la configuración vigente lo permita.

## Configuración

- Definir `site` cuando se necesitan URLs absolutas fiables, canonical o sitemap.
- Definir `base` solo si el sitio se sirve bajo subruta; construir enlaces con conocimiento de esa base, no con parches de reemplazo.
- No fijar un adaptador para una exportación estática que el proveedor pueda servir directamente.
- No añadir integraciones sin una función verificable.
- Consultar la referencia oficial antes de usar opciones sensibles a versión.

## Contenido y variables

- Usar colecciones solo cuando esquema, validación, consultas o muchas entradas lo justifiquen. Para una única landing, datos tipados locales suelen bastar.
- Acceder a secretos solo en contexto de servidor/build. Las variables expuestas al cliente deben seguir el prefijo público vigente y no contener información privada.
- Nunca interpolar una variable privada en markup, atributos, JSON serializado o scripts del navegador.

## Criterio de salida

Rutas, layout, componentes, assets, datos y modo de renderizado tienen una responsabilidad explícita; la arquitectura compila sin adaptaciones del proveedor incrustadas en la UI.

Fuentes oficiales: [estructura](https://docs.astro.build/en/basics/project-structure/), [rutas y páginas](https://docs.astro.build/en/basics/astro-pages/), [TypeScript](https://docs.astro.build/en/guides/typescript/), [variables de entorno](https://docs.astro.build/en/guides/environment-variables/), [renderizado bajo demanda](https://docs.astro.build/en/guides/on-demand-rendering/).

