# Interactividad con HTML y JavaScript nativo

**Cargar cuando:** se añaden menús, acordeones, modales, tabs, validación progresiva u otro comportamiento pequeño.

## Elección obligatoria

1. Usar el elemento HTML nativo apropiado (`button`, `details`, enlace, formulario, `dialog` cuando sea compatible con el requisito).
2. Resolver presentación y estados simples con CSS.
3. Añadir JavaScript nativo únicamente para el comportamiento que falta.
4. Considerar una isla de framework solo si estado, ecosistema o complejidad la justifican; cargar [islas](09-islands-and-ui-frameworks.md).

Un menú móvil, acordeón, modal o tabs sencillos no justifican por sí mismos instalar React, Vue o Svelte.

## Contrato de un script

- Seleccionar dentro de una raíz del componente mediante `data-*`; evitar selectores globales frágiles.
- Ser idempotente: marcar inicialización o retirar listeners de forma explícita.
- Funcionar con cero, una o varias instancias.
- Usar `addEventListener`; no sobrescribir handlers globales.
- Preservar estado ARIA, foco, Escape, retorno de foco y scroll según el patrón.
- No inyectar documentos HTML ni usar `innerHTML` con contenido no confiable.
- No depender de orden incidental de scripts.
- Usar delegación de eventos solo si reduce listeners sin volver opaco el alcance.

## Scripts en Astro

- Preferir scripts locales procesados por Astro/Vite para módulos, TypeScript y deduplicación cuando corresponda.
- Usar `is:inline` o atributos que cambien el procesamiento solo por una necesidad concreta y después de consultar la guía oficial vigente.
- No cargar un bundle global para una interacción presente en una sola ruta.
- `document` y `window` solo existen en el navegador: no usarlos durante frontmatter/renderizado del servidor.
- Si se habilita navegación de cliente, validar el ciclo de vida oficial y reinicialización; no asumir una única carga de documento.

## Patrones mínimos

- **Menú:** botón real, `aria-expanded`, objetivo identificado, cierre por Escape y manejo de foco razonable.
- **Acordeón:** preferir `details/summary` si satisface diseño y semántica.
- **Modal:** nombre accesible, foco inicial, contención cuando aplique, Escape y retorno de foco.
- **Tabs:** roles/teclado completos o una presentación sin tabs; no simular el patrón parcialmente.
- **Formulario:** validación nativa como base, errores asociados y respuesta de servidor/servicio como autoridad.

## Verificación

Probar sin JavaScript, con teclado, varias instancias, reinicialización, resize y reduced motion. Medir el JavaScript emitido y revisar [accesibilidad](13-accessibility.md).

Fuente oficial: [scripts y manejo de eventos](https://docs.astro.build/en/guides/client-side-scripts/).

