# Fundamentos de polaridad light OMNIA

## Modelo mental

La transformación correcta tiene tres etapas:

`expresión OMNIA dark → análisis de función y contexto → expresión OMNIA light`

El valor fuente es evidencia, no significado. Un mismo `#161616` puede ser canvas, texto, icono, botón o scrim; cada uso puede requerir una decisión diferente. Clasifica el consumidor y el fondo real antes de elegir el resultado.

## Frontera de autoridad

Usa esta pregunta para resolver alcance:

> ¿Esta decisión tendría que cambiar únicamente porque cambió la luminancia del entorno?

- Si la respuesta es **no**, congélala y sigue `omnia-aesthetic`.
- Si es **sí**, esta modifier puede cambiar solo las propiedades cromáticas necesarias.
- Si no está claro, conserva la decisión y trata el caso como excepción pendiente, no como permiso para rediseñar.

La adición de un borde, tint o sombra solo es válida cuando recupera una separación que se perdería en light mode y no cambia medidas, anatomía ni ritmo.

## Roles semánticos

Clasifica cada uso en una de estas familias:

| Familia | Roles frecuentes | Pregunta de diagnóstico |
|---|---|---|
| Superficie | canvas, primary, raised, soft, interactive | ¿Qué plano establece o separa? |
| Foreground | text-primary, secondary, muted, label, icon | ¿Qué jerarquía de lectura representa? |
| Estructura | border-subtle, default, strong, divider, focus | ¿Qué límite o estado hace visible? |
| Marca | accent-primary, strong, muted, surface-tint | ¿Qué identidad o énfasis conserva? |
| Profundidad | contact shadow, ambient shadow, highlight, glow | ¿Qué relación espacial comunica? |
| Compuesto | gradient, overlay, mask, glass | ¿Qué capas y roles contiene? |
| Media | logo, photo, illustration, texture, video, 3D | ¿Es contenido, identidad o superficie decorativa? |

La taxonomía es un modelo de análisis. No exige renombrar tokens existentes. Si un token ambiguo funciona en varios contextos, conserva su nombre y crea overrides locales solo cuando sus roles necesiten resultados distintos.

## Polos de luminancia OMNIA

Construye la escala clara alrededor de los neutrales ya definidos por `omnia-aesthetic`. Estos valores son anclajes iniciales, no una tabla universal de sustitución:

| Rol light | Anclaje OMNIA | Relación buscada |
|---|---:|---|
| `surface-canvas` | `#F7F6F8` | neutral suave que evita blanco total |
| `surface-primary` | `#FDFDFC` | blanco cálido de identidad |
| `surface-raised` | `#FFFFFF` o primary + borde/sombra | plano elevado sin card flotante exagerada |
| `surface-soft` | neutral suave o tint de marca bajo | agrupación secundaria, no protagonismo |
| `text-primary` | `#161616` | máxima autoridad y lectura |
| `text-secondary` | `#414141` | apoyo claramente subordinado |
| `text-muted` | `#666666` | metadata legible, no texto “lavado” |
| `border-subtle` | Negro OMNIA al `14%` | separación silenciosa |
| `border-default` | Negro OMNIA alrededor de `20–24%` | límite operativo |
| `border-strong` | Negro OMNIA hasta `28%` | corte o estado con énfasis |

No fuerces una diferencia de luminosidad en todos los niveles. Dos superficies casi iguales pueden separarse mediante borde, highlight local o sombra de contacto. Evalúa siempre la pareja real: superficie con canvas, card con sección, control con card.

## Preservación de relaciones

Conserva la función perceptual, no la aritmética del color:

- Si una superficie dark se distinguía del canvas, su equivalente light también debe distinguirse.
- Si un plano elevado dominaba sobre uno secundario, debe conservar esa prioridad aunque ambos se acerquen al blanco.
- Si un divisor organizaba sin encajonar, no lo conviertas en una card ni en una sombra pesada.
- Si un estado invertía la polaridad de forma intencional, puede usar Negro OMNIA y Blanco cálido en light mode; “light” no significa eliminar todo contraste oscuro.
- Si la jerarquía dependía de opacidad, revalídala sobre el nuevo fondo: una opacidad idéntica rara vez conserva el mismo resultado perceptual.

Preserva relaciones por pares antes de optimizar colores individuales. Una muestra aislada no demuestra que el sistema funciona.

## Neutrales y colores cromáticos

### Neutrales

Los neutrales pueden moverse ampliamente entre polos porque su trabajo es construir luminancia, lectura y profundidad. Mantén su temperatura OMNIA —negro suave y blancos cálidos— y evita tanto `#000000`/`#FFFFFF` como solución universal como una escala gris genérica sin relación con la marca.

### Marca

Parte de los colores oficiales sin invertirlos ni crear complementarios:

| Familia | Base de identidad | Tratamiento light |
|---|---:|---|
| Morado | `#56167D` | conservar hue; ajustar lightness/saturation solo para contraste o estados |
| Azul | `#005B85` | conservar autoridad y hue; revisar texto, iconos y bordes finos |
| Carmesí | `#C8003B` | conservar energía; moderar área u opacidad antes de cambiar identidad |
| Amarillo | `#FCBF4A` | mantener como foco/CTA; usar foreground oscuro y validar límites sobre blanco |

Deriva variantes `strong`, `default`, `muted` y `surface-tint` dentro de la misma familia. Para tints, baja la contribución cromática sobre Blanco cálido; para texto o icono, refuerza lightness o saturación solo lo necesario. La variante se define por su función y contraste, no por una fórmula fija.

## Filosofía visual light

La versión clara debe seguir siendo futurist-clean, premium, precisa y humana. Evita el resultado “white SaaS” mediante:

- blancos cálidos y neutrales suaves en vez de blanco puro en todas partes;
- jerarquía editorial sostenida por divisores, tintes y contraste local;
- una o dos familias de acento por región, como en la fuente dark;
- profundidad contenida, sin flatness estéril ni tarjetas flotantes repetitivas;
- firmas OMNIA preservadas: gradiente, Negro OMNIA, acentos oficiales y formas orgánicas cuando ya existan.

La dimensionalidad no autoriza neumorfismo. Si el original no tenía una sombra, no la añadas por estilo; si una superficie pierde separación, usa la intervención cromática mínima que la recupere.

