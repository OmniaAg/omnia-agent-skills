# Islas y frameworks de interfaz

**Cargar cuando:** se propone instalar o usar React, Vue, Svelte, Preact, Solid u otro renderer; se añade `client:*`.

## Regla de admisión

Los componentes `.astro` son la primera opción y no envían un runtime de UI por sí mismos. Un componente de framework solo se admite si aporta una capacidad concreta que HTML, CSS, JavaScript nativo o un componente Astro del servidor no resuelven de forma mantenible.

No instalar un framework por defecto ni para menús, acordeones o modales simples.

## Registro obligatorio por isla

```text
Motivo:
Componente y ruta:
Estado/interacción requerida:
Alternativas evaluadas:
Framework/integración ya disponible o nueva:
Directiva client:*:
Cuándo hidrata:
JavaScript estimado/medido:
Impacto en mantenimiento:
Fallback sin hidratación:
```

## Selección de directiva

- Sin `client:*`: HTML estático del componente de framework, si no necesita interacción en cliente.
- `client:visible`: interacción puede esperar a proximidad del viewport.
- `client:idle`: funcionalidad secundaria puede esperar a que el navegador esté inactivo.
- `client:media`: solo es interactivo bajo una condición de media válida y justificada.
- `client:load`: únicamente interacción crítica disponible inmediatamente; nunca por comodidad.
- `client:only`: solo si el componente no puede renderizarse en servidor y existe un fallback deliberado; es la opción más costosa en resiliencia.

Confirmar semántica y opciones en la referencia oficial vigente antes de implementar. Elegir la estrategia más restrictiva que satisfaga el caso.

## Guardrails

- No mezclar varios runtimes sin una razón excepcional documentada.
- No convertir secciones estáticas en islas para reutilizar un componente existente.
- Mantener el límite de hidratación pequeño; pasar props serializables y evitar estado global por defecto.
- Cargar componentes de framework directamente; una directiva puesta sobre un wrapper Astro no convierte mágicamente su interior en una isla.
- Revisar dependencias transitivas, tree shaking, CSS del runtime y duplicación de librerías.
- Medir HTML, JavaScript, tareas largas e interacción antes y después.

## Criterio de aceptación

La isla tiene valor funcional verificable, fallback suficiente, directiva justificada y coste registrado. El build, interacción, SSR/prerender y reduced motion funcionan en el destino elegido.

Fuentes oficiales: [frameworks de interfaz](https://docs.astro.build/en/guides/framework-components/), [directivas de plantilla](https://docs.astro.build/en/reference/directives-reference/), [integraciones](https://docs.astro.build/en/guides/integrations/).

