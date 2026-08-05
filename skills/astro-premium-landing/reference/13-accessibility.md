# Accesibilidad

**Cargar cuando:** se crea o revisa estructura, navegación, interacción, formularios, color, medios o movimiento.

## Base obligatoria

- Usar HTML semántico antes de ARIA: landmarks, botones, enlaces, formularios, listas y encabezados reales.
- Mantener un `main`, orden de lectura lógico, encabezado principal claro y jerarquía sin saltos arbitrarios.
- Incluir enlace de salto cuando existe navegación repetida relevante.
- Toda función debe operarse con teclado y mostrar foco visible.
- El nombre accesible de botones/enlaces debe expresar la acción; los iconos solos necesitan nombre.
- No usar enlace como botón ni `div` clicable como control.
- Asociar cada input con `label`; instrucciones y errores mediante relaciones accesibles.
- Mantener contraste suficiente y no comunicar estado solo por color.
- Usar `alt` funcional; `alt=""` únicamente para imágenes decorativas redundantes.
- Respetar zoom, reflow, orientación y tamaños táctiles razonables.

## Movimiento y medios

- Implementar una experiencia `prefers-reduced-motion` sin parallax, desplazamientos o bucles no esenciales.
- Evitar autoplay con sonido; ofrecer controles de pausa para movimiento persistente cuando aplique.
- Proveer captions/transcripción según el medio y el criterio acordado.
- No depender de hover para revelar información o controles esenciales.

## Patrones interactivos

- Gestionar estado ARIA, Escape y foco según el patrón, no de forma decorativa.
- Un modal debe tener nombre, foco inicial razonable, cierre accesible y retorno de foco.
- Mensajes dinámicos importantes necesitan anuncio apropiado, sin abusar de regiones live.
- La validación no debe borrar datos ni depender solo del color; mover foco/resumen según complejidad.

## Revisión mínima

1. Navegar toda la página con teclado y orden de tabulación.
2. Probar zoom/reflow y anchos pequeños sin scroll horizontal bidimensional inesperado.
3. Activar reduced motion y alto contraste/tema cuando esté en alcance.
4. Inspeccionar árbol semántico, nombres, estados y errores.
5. Ejecutar automatización accesible disponible.
6. Realizar revisión humana; el verificador de esta skill es heurístico y no certifica conformidad.

## Contraste automatizable

Solo marcar automáticamente pares de color de texto/fondo explícitos en una misma regla simple. Gradientes, imágenes, transparencia, estados y texto grande requieren inspección/render; no afirmar falsos positivos como hechos.

## Criterio de aceptación

La conversión completa funciona con teclado, el documento conserva significado sin CSS/JS, los controles tienen nombre/estado, el movimiento tiene alternativa y los problemas conocidos están registrados con severidad.

Relacionar con [formularios](16-forms-analytics-and-integrations.md), [efectos](07-effects-and-animation.md) y [validación](17-validation-and-release.md).

