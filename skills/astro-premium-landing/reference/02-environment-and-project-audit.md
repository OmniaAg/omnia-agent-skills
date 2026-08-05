# Detección del entorno y auditoría inicial

**Cargar cuando:** se analiza un proyecto, se corrige un fallo de entorno o se decide qué módulos aplicar.

## Inventario obligatorio

- Sistema operativo, shell y política de ejecución.
- Versión disponible de Node, gestor de paquetes y lockfile efectivo.
- Versión de Astro declarada y configuración `astro.config.*`.
- Scripts reales de `package.json`; no asumir nombres.
- `output`, adaptador, `site`, `base`, integraciones y aliases configurados.
- Estructura bajo `src/` y `public/`, rutas existentes y directorio de salida.
- TypeScript, nivel de estrictitud y configuración heredada.
- Estrategia CSS, frameworks de interfaz e islas hidratadas.
- Variables de entorno por nombre, nunca por valor.
- Estado de control de versiones y cambios ajenos.
- Destino de despliegue y requisitos dinámicos confirmados.

## Procedimiento seguro

1. Leer `package.json`, lockfiles, `astro.config.*` y `tsconfig.json` antes de ejecutar comandos.
2. Elegir el gestor del lockfile; si hay varios, registrar conflicto y no regenerarlos.
3. Inspeccionar `src/pages/`, layouts, componentes, estilos y assets con búsqueda de archivos.
4. Localizar `client:*`, scripts, runtimes de UI, imports de entorno y endpoints.
5. Ejecutar `python scripts/verify_project.py RUTA` para una línea base no destructiva.
6. Consultar [problemas críticos](10-critical-astro-gotchas.md) y, en Windows, [troubleshooting](22-windows-troubleshooting.md).

## Señales de un proyecto estático

- La landing puede resolverse en build con contenido conocido.
- No requiere sesión, respuesta personalizada, secreto en cada petición ni escritura en servidor.
- Formularios y analítica pueden delegarse a un servicio explícito.

No confundir datos obtenidos durante el build con renderizado bajo demanda.

## Señales que requieren decisión

- `output` distinto del valor estático esperado o presencia de adaptador.
- Rutas con `prerender = false`, endpoints, middleware o acciones de servidor.
- Múltiples frameworks de UI o numerosas directivas `client:load`.
- Referencias `/src/assets/`, imports desde `public/` o rutas relativas heredadas.
- Más de un lockfile, scripts que instalan durante build o configuración del proveedor dentro de componentes.

## Salida de la auditoría

Registrar una tabla compacta: hallazgo, evidencia (archivo/ruta), impacto, decisión y módulo siguiente. No modificar hasta conocer alcance y criterio de aceptación.

Fuente oficial: [estructura de proyectos Astro](https://docs.astro.build/en/basics/project-structure/), [referencia de configuración](https://docs.astro.build/en/reference/configuration-reference/).

