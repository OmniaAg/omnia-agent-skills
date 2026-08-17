# Reglas de transformación cromática

## Método de decisión

Antes de editar, construye un inventario mínimo por uso:

| Campo | Contenido |
|---|---|
| Consumidor | componente, pseudo-elemento o asset |
| Contexto | fondo real, capa, estado y breakpoint |
| Fuente | token/declaración y valor dark |
| Rol | superficie, foreground, estructura, marca, profundidad o media |
| Destino | token/valor light y relación que preserva |
| Excepción | motivo y alcance, si aplica |

No deduzcas el rol solo por el nombre del token. Inspecciona dónde termina usándose, incluidas variables encadenadas. Si un valor alimenta texto y background, sepáralo por contexto sin exigir una migración global de nombres.

## Reglas generales

| Rol dark observado | Equivalente light | Invariante perceptual |
|---|---|---|
| Canvas Negro OMNIA | neutral claro suave, normalmente `surface-canvas` | silencio, marco y contraste con el contenido |
| Superficie oscura primaria | Blanco cálido `surface-primary` | plano principal y continuidad |
| Superficie oscura elevada | blanco o superficie primaria con keyline/contact shadow | elevación relativa, no “cardiness” |
| Superficie oscura secundaria | neutral o tint claro ligeramente más denso | anidación y pertenencia |
| Texto inverso primario | Negro OMNIA | máxima jerarquía |
| Texto inverso secundario | `text-secondary` | subordinación legible |
| Texto inverso tenue | `text-muted` validado en contexto | metadata sin desaparecer |
| Borde claro translúcido | Negro OMNIA translúcido | mismo grado de separación |
| Glow cromático | tint, halo corto o border tint | énfasis de marca sin bloom sucio |
| Gradiente dark | misma familia/orden con stops adaptados | dirección, ritmo e identidad |

No conviertas mecánicamente cada superficie oscura en blanco. Construye primero la escala `canvas → surface → raised/interactive` y verifica que las diferencias se sostengan en contexto.

## Canvas, secciones y superficies

- Usa `#F7F6F8` o un neutral suave compatible como canvas cuando el panel principal necesita emerger.
- Usa Blanco cálido `#FDFDFC` como base de contenido; reserva `#FFFFFF` para el nivel que realmente requiera máxima claridad.
- Reinterpreta capítulos dark como superficies claras tonales o tints de marca de baja contribución. Conserva el ritmo de capítulos sin mantener masas oscuras por inercia ni borrar sus límites.
- Conserva el número, orden, altura y anatomía de las secciones. Cambiar alternancia cromática no autoriza reordenarlas.
- Usa una combinación pequeña de luminancia, borde, tint y sombra. No hagas depender toda la jerarquía de `box-shadow`.
- Añade keylines sin alterar caja o medidas; aprovecha bordes existentes o técnicas inset cuando un borde nuevo modificaría layout.

## Cards y paneles

- Mantén exactamente grid, padding, radio, proporción y densidad definidos por `omnia-aesthetic`.
- Si dark separaba card y canvas por masa tonal, usa en light una superficie cálida con borde sutil; añade sombra de contacto solo si la separación sigue siendo insuficiente.
- Conserva las familias funcionales: una FAQ editorial no se convierte en card; una lista no se convierte en bento; un panel único no se fragmenta.
- Las superficies translúcidas sobre gradiente requieren una evaluación local de fondo, borde y texto. No reutilices el alpha dark sin comprobar el color compuesto.

## Navegación

- Transforma el fondo oscuro de una navegación dependiente del tema a una superficie clara opaca o translúcida equivalente; conserva posición, altura, blur, anatomía y comportamiento.
- Adapta el borde inferior a `border-subtle` y el texto a sus roles light.
- Conserva el CTA amarillo con texto oscuro cuando siga siendo legible y fiel.
- Si el blur era contextual a una capa flotante, mantenlo únicamente allí. Un tema claro no convierte glassmorphism en lenguaje global.
- Evalúa la navegación sobre cada sección y durante scroll; una transparencia válida sobre canvas puede fallar sobre artwork o gradientes.

## Texto, iconos y estructura

- No cambies familias, escala, weight, line-height, tracking, medida ni alineación.
- Mapea jerarquías a `text-primary`, `text-secondary` y `text-muted`; no uses un único gris para todo.
- Trata labels, metadata y placeholders como roles distintos aunque compartieran color dark.
- Usa el mismo rol de foreground para iconos monocromos y texto equivalente; conserva los iconos multicolor.
- Convierte bordes claros translúcidos a Negro OMNIA translúcido según su importancia, no con una inversión de porcentaje ciega.
- Mantén divisores como divisores. Refuerza opacidad solo hasta que organicen sin encajonar.

## Sombras, highlights y profundidad

- No traslades sombras dark literalmente. Reduce opacidad oscura, aumenta difusión y limita el desplazamiento visual.
- Usa sombra de contacto corta para anclar y sombra ambiental muy tenue solo cuando el componente ya expresaba elevación.
- Permite un highlight claro inset discreto sobre superficies elevadas si recupera volumen; no lo combines como doble sombra neumórfica.
- Una superficie sin elevación en dark debe seguir sin elevación artificial en light salvo que pierda una relación esencial.
- Evita sombras grises profundas, halos alrededor de todas las cards y relieves de baja accesibilidad.

## Glows y gradientes

- Convierte blooms luminosos dark en uno de estos recursos: tint de superficie, halo local de baja opacidad, borde teñido o acento ambiental restringido.
- Conserva familia, secuencia, dirección y posiciones de stops del gradiente OMNIA. Ajusta lightness, saturation y alpha por stop según su rol.
- No inventes complementarios ni uses el gradiente completo en cada región.
- Para gradientes que sostienen texto, decide primero si son superficie o artwork; después valida cada tramo crítico del foreground.
- Mantén el gradiente dark original solo cuando funcione como momento inverso intencional de marca, no por falta de adaptación.

## Botones y enlaces

- Conserva tamaño, radio pill, borde, tipografía, icono, movimiento y prioridad.
- Un botón Negro OMNIA con texto cálido puede permanecer oscuro: es un foreground interactivo, no el canvas.
- Mantén amarillo + texto oscuro para CTA cuando el límite siga siendo visible; añade borde neutral o separación local si se pierde sobre una superficie clara.
- Deriva hover/selected de la misma familia de acento. Cambia área, tint, borde o lightness antes de cambiar hue.
- Conserva desplazamiento y timing de hover/active; solo transforma las propiedades cromáticas.
- Los enlaces deben seguir distinguiéndose por algo más que color cuando así lo definía el patrón original.

## Inputs y controles

- Usa superficie primaria o soft, texto primario, placeholder diferenciado y borde default.
- Refuerza el borde en hover y usa acento/focus ring en focus; no cambies altura, padding ni anatomía.
- Trata autofill, selección, error, success y controles nativos como estados propios. No dejes que el navegador introduzca una polaridad incoherente.
- Mantén el amarillo como señal de foco OMNIA, pero añade una keyline oscura compañera si hace falta para distinguirlo sobre blancos. Conserva grosor, offset y forma del sistema de foco.
- No uses solo sombra inset para comunicar que un campo es editable.

## Estados interactivos

- **Hover:** conserva el salto de contraste del original mediante tint, foreground, borde o una inversión intencional; no añadas elevación arbitraria.
- **Active:** conserva transform/posición y hace visible el estado mediante una variación cromática pequeña pero inequívoca.
- **Selected/current:** combina superficie, borde y foreground cuando el color por sí solo no basta; mantiene el acento de la misma familia.
- **Disabled:** reduce énfasis por rol, no aplicando una opacidad global que vuelva ilegible contenido o bordes. Conserva la señal semántica existente.
- **Focus-visible:** debe superar fondos claros, tints y gradientes sin abandonar el amarillo de identidad.
- **Visited, checked, error y success:** conserva significado y contraste; no inventes una paleta de estados si el producto ya la define.

## Overlays, scrims y transparencia

- Un scrim puede seguir siendo oscuro porque su rol es reducir prominencia y aislar un modal; ajusta alpha según el fondo light.
- Mantén stacking, blur, área y comportamiento. Solo cambia color/opacidad necesarios para conservar aislamiento.
- Recalcula colores por su composición sobre el fondo real. El mismo `rgba()` produce otra jerarquía sobre Blanco cálido.
- En glass, coordina surface tint, alpha, borde, highlight y texto como un sistema local. Si el resultado se ensucia, usa una superficie más opaca antes de añadir efectos.

