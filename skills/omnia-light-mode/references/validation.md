# Validación de fidelidad light

## Criterio de éxito

Dark y light deben compartir la misma silueta, flujo, densidad, anatomía y comportamiento. La diferencia perceptual principal debe ser la polaridad y su adaptación cromática.

> Si desactivo mentalmente los colores y observo únicamente layout, geometría, jerarquía, componentes y motion, ¿sigue siendo exactamente el mismo sistema visual?

Si la respuesta es no, se modificó demasiado.

## Auditoría de alcance

Revisa el diff o la especificación antes de evaluar estética:

- Los cambios pertenecen a color, background, border color, shadow, highlight, glow, gradient, overlay o tratamiento de asset dependiente del tema.
- No cambiaron DOM, orden, copy, layout, grid, spacing, sizing, tipografía, radios, anatomía, breakpoints, interacciones ni timing de motion fuera del contrato Dark/Light solicitado. Si se incorpora el selector porque no existía, limitar su DOM y conducta a [theme-switching.md](theme-switching.md) y dejar que `omnia-aesthetic` gobierne su apariencia.
- Un asset swap conserva dimensiones, proporción, posición y función.
- Los tokens semánticos son un modelo mental; no se impuso un refactor de naming sin necesidad.
- `omnia-aesthetic` no tiene ningún cambio.

Una excepción solo pasa si recupera fidelidad cromática y está limitada al componente/asset afectado.

## Comparación pareada

Compara ambas polaridades con:

- el mismo viewport y zoom;
- el mismo contenido y datos;
- el mismo punto de scroll;
- los mismos estados default, hover, focus-visible, active, selected, disabled y error cuando existan;
- los mismos breakpoints de desktop y mobile;
- el mismo estado de movimiento reducido.

Superpone capturas o alterna rápidamente entre ellas. Busca desplazamientos, wraps, cambios de densidad o nuevas cajas: son señales de que la transformación excedió el color.

## Nueve controles obligatorios

### 1. Brand fidelity

- ¿Los acentos conservan hue, función y reconocimiento OMNIA?
- ¿Negro OMNIA, Blanco cálido y el gradiente siguen actuando como identidad, no como decoración genérica?
- ¿El resultado evita una plantilla SaaS blanca o una landing corporativa estéril?

### 2. Visual hierarchy

- ¿Primary, secondary y muted mantienen su orden de atención?
- ¿Los momentos de impacto siguen dominando sin recrearlos como masas dark arbitrarias?
- ¿Los acentos siguen siendo escasos y controlados?

### 3. Surface separation

- ¿Canvas, superficie primaria, raised, soft e interactive se distinguen en contexto?
- ¿La separación combina tono, borde y profundidad sin depender solo de sombra?
- ¿Las listas editoriales siguen siendo listas y las cards siguen perteneciendo a su familia?

### 4. Text readability

- ¿Texto normal alcanza al menos `4.5:1` y texto grande al menos `3:1` cuando aplica WCAG?
- ¿Texto secundario y muted son legibles sobre surfaces, tints, gradients y glass reales?
- ¿No se cambió tipografía para resolver un problema que era cromático?

### 5. Accent preservation

- ¿Morado, azul, carmesí y amarillo permanecen en su familia?
- ¿No aparecieron complementarios automáticos ni desaturación uniforme?
- ¿Tints, bordes y estados derivados siguen reconociéndose como el mismo acento?

### 6. Component state clarity

- ¿Hover, active, selected, disabled, focus, visited y validación se distinguen entre sí?
- ¿El foco amarillo es visible sobre blancos y superficies teñidas?
- ¿Color no es la única señal cuando el sistema original ya ofrecía otra?

### 7. Asset compatibility

- ¿Se utilizó la variante oficial correcta de logo?
- ¿Fotografías, clientes, ilustraciones, videos y 3D conservaron su contenido?
- ¿SVG, masks y glows se trataron por función, no mediante filtro global?

### 8. Desktop consistency

- ¿Se conservan retícula, proporciones, sticky, offsets, crops y ritmo?
- ¿Navegación, overlays y superficies translúcidas funcionan sobre todas las secciones?
- ¿No surgieron sombras, halos o bordes inconsistentes en componentes repetidos?

### 9. Mobile consistency

- ¿Se conserva el mismo flujo responsive sin nuevas cards ni agrupaciones?
- ¿Targets, foco, safe areas y contraste siguen claros en superficies pequeñas?
- ¿Los assets y gradientes mantienen crop y legibilidad en anchos extremos?

## Accesibilidad cromática

- Verifica contraste con el color compuesto final, no con el token aislado.
- Valida texto sobre gradientes en sus zonas más desfavorables.
- Mantén límites de controles y focus visible con al menos `3:1` frente a colores adyacentes cuando corresponda.
- No comuniques estado o categoría solo mediante hue.
- Revisa selección de texto, placeholders, autofill, scrollbars y controles nativos.
- Con `prefers-reduced-motion`, los cambios cromáticos deben seguir comunicando estado sin depender del desplazamiento eliminado.

## Anti-patterns de rechazo

Rechaza o corrige la transformación si aparece cualquiera de estas señales:

- sustitución global `dark hex → light hex` sin roles;
- inversión automática de imágenes o artwork;
- blanco puro en canvas, secciones, cards y controles a la vez;
- todos los elementos convertidos en cards flotantes;
- sombras copiadas del dark mode, blooms grises o doble sombra neumórfica;
- colores de marca invertidos, complementarios o recoloreados por cliente;
- opacidades dark reutilizadas sin validar composición;
- muted text demasiado tenue o disabled ilegible;
- gradientes con nuevos hues, dirección o stops sin razón cromática;
- modificación de layout, tipo, geometría, contenido o motion;
- excepciones globales nacidas de un único logo o hero.

## Cierre

Antes de entregar:

1. elimina reglas duplicadas o demasiado específicas;
2. consolida decisiones repetidas por rol semántico;
3. conserva solo excepciones justificadas;
4. registra assets oficiales faltantes sin inventarlos;
5. resume tokens light, tratamientos especiales y validaciones realizadas;
6. confirma explícitamente que `omnia-aesthetic` y el código no relacionado con el tema permanecen intactos.
