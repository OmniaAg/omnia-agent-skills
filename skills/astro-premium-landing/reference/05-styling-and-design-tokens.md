# Estilos, tokens y responsive

**Cargar cuando:** se define o modifica la estrategia CSS, se crea UI o se considera Tailwind.

## Decisión inicial

Detectar primero lo que ya usa el proyecto:

| Estrategia | Uso principal |
|---|---|
| CSS local de `.astro` | Estilos encapsulados de una sección/componente. Predeterminado práctico. |
| CSS global | Reset, fuentes, tokens, elementos base y utilidades deliberadas. |
| Variables CSS | Tokens de color, tipo, espacio, radio, sombra, capas y movimiento. |
| CSS Modules | Solo donde el tipo de componente/integración ya los justifique. |
| Tailwind | Únicamente si ya existe o fue solicitado; respetar la integración vigente. |

No migrar de estrategia por preferencia. Registrar una regla simple de propiedad: qué vive globalmente y qué vive con el componente.

## Obligatorio

- Definir tokens semánticos (`--color-text`, `--space-section`, `--radius-control`) en vez de valores de marca repetidos.
- Mantener globales estrechos: `:root`, reset, tipografía base, elementos y utilidades compartidas justificadas.
- Usar estilos locales para estructura/variantes de componentes.
- Diseñar fluidamente con `clamp()`, grid/flex, contenedores y media queries basadas en quiebres reales del contenido.
- Incluir estados `hover`, `focus-visible`, `active`, `disabled`, error y éxito cuando apliquen.
- Preservar foco visible y contraste; no comunicar estado solo con color.
- Implementar `prefers-reduced-motion` si existe movimiento no esencial.

## Evitar

- Selectores globales profundos, `!important` como sistema o especificidad creciente.
- Estilos inline estáticos; reservar `style` dinámico para valores realmente variables y seguros.
- Números mágicos duplicados, z-index arbitrarios o breakpoints por dispositivo nominal.
- Clases huérfanas, reglas duplicadas y utilidades de una sola ocurrencia sin valor.
- Mezclar Tailwind, CSS local, CSS Modules y librerías CSS sin límites documentados.
- Instalar Tailwind o una librería de animación para un efecto resoluble con CSS.

## Tailwind

Si está aprobado:

1. Detectar versión y método de integración existentes.
2. Consultar la guía oficial vigente antes de cambiar configuración; el mecanismo ha cambiado entre versiones.
3. Mantener tokens y patrones compartidos; no convertir cada decisión en una cadena opaca de utilidades.
4. No reescribir CSS estable únicamente para uniformar sintaxis.

## Tipografía

- Usar formatos y subconjuntos adecuados, declarar fallbacks y evitar pesos no utilizados.
- Preload solo para fuentes críticas confirmadas.
- Controlar medida de línea, altura, tamaño fluido y saltos del hero en idiomas previstos.

## Revisión

Buscar reglas globales nuevas, valores repetidos, `!important`, inline styles, overflow horizontal, foco invisible, motion sin alternativa y mezcla de estrategias. Revisar también [accesibilidad](13-accessibility.md) y [rendimiento](14-performance.md).

Fuentes oficiales: [estilos y CSS](https://docs.astro.build/en/guides/styling/), [integración Tailwind](https://docs.astro.build/en/guides/integrations-guide/tailwind/).

