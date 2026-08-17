# Media y assets en light mode

## Principio

No trates un asset como una bolsa de píxeles que debe invertirse. Determina primero su función, transparencia, luminancia dominante, escala de uso y si se comporta como contenido, marca, icono o superficie casi sólida.

La información visual del asset prevalece sobre una regla global. Preservar una fotografía o trabajo de cliente intacto suele ser más fiel que “armonizarlo” con el tema.

## Secuencia de análisis

1. **Identifica el tipo:** logo, icono, SVG, fotografía, ilustración, textura, background artwork, video, canvas o 3D.
2. **Identifica la función:** contenido, identidad, control, decoración, superficie o máscara.
3. **Inspecciona el contexto:** fondo real, tamaño renderizado, transparencia, contraste interno y estados.
4. **Busca una variante oficial:** prioriza el asset creado para fondos claros.
5. **Elige el tratamiento mínimo:** conservar, cambiar variante, adaptar tokens internos, ajustar contenedor o aplicar una excepción local.
6. **Valida fidelidad y responsive:** revisa desktop/mobile, recortes, poster frames, lazy states y densidad de píxel.

## Matriz por tipo

| Tipo | Tratamiento por defecto | Adaptación permitida | Evitar |
|---|---|---|---|
| Fotografía | conservar píxeles y color | ajustar marco, scrim de texto o superficie circundante | invertir, desaturar o recolorear automáticamente |
| Logo | usar variante oficial para fondo claro | cambiar `src`, `picture` o asset token sin alterar caja | filtros CSS, reconstrucción o recolor no autorizado |
| Icono monocromo | vincular fill/stroke al foreground semántico | cambiar color por estado y fondo | invertir el contenedor completo |
| Icono multicolor | conservar identidad | usar variante oficial si existe | reducirlo a monocromo por conveniencia |
| SVG UI | clasificar fill, stroke, stop-color y masks por rol | tematizar solo formas declaradas como UI | recolorear ilustración o logo como si fuera icono |
| Ilustración | conservar como contenido | variante light oficial o marco/tint contextual | inversión global o nueva paleta automática |
| Textura | evaluar si funciona como superficie | bajar opacidad, adaptar tono o sustituir por variante | aplicar el mismo filtro que a una fotografía |
| Background artwork | evaluar legibilidad y jerarquía | variant, overlay localizado o excepción | ocultarlo por sistema sin entender su función |
| Video | conservar contenido | poster/controles/letterbox temáticos o versión oficial | filtros de inversión o brillo global |
| 3D render | conservar materiales e iluminación | ajustar stage, environment o variante suministrada | recolorear el render desde CSS |
| Canvas/WebGL | tratar como subsistema | usar API/flag de tema ya disponible o excepción | asumir que sus píxeles heredan variables CSS |

## Logos

- Busca primero versiones oficiales dark-on-light, horizontales, verticales o isotipo según la misma anatomía usada en dark.
- Conserva proporción, zona libre, tamaño, alineación y lugar en la jerarquía.
- Cambiar de variante es una adaptación cromática válida; cambiar lockup, tamaño o ubicación no lo es.
- Si solo existe un logo para fondo oscuro, no lo filtres. Usa un contenedor inverso ya compatible con la composición o registra el asset light como pendiente.
- Los logos de clientes conservan sus colores y no se fuerzan a la paleta OMNIA.

## SVG, iconos y máscaras

- Inspecciona `fill`, `stroke`, `stop-color`, opacidades, `currentColor`, masks y filtros por separado.
- En iconos de UI, trata `fill`/`stroke` como foreground; en una máscara, el color visible puede venir del background del elemento y cumplir función de foreground.
- Conserva stroke width, geometría, viewBox, tamaño y motion.
- No sustituyas un SVG complejo por un icono genérico. Si mezcla marca, artwork y UI, tematiza únicamente las capas inequívocamente dependientes del tema.

## Fotografías e ilustraciones

- No alteres el contenido para “hacerlo light”. Adapta primero el encuadre neutral que lo contiene.
- Si texto se superpone, conserva la composición y usa scrim/overlay localizado con el mínimo cambio necesario.
- Distingue una ilustración plana casi sólida de una fotografía: la primera puede tener variante temática; la segunda normalmente se conserva.
- Mantén el tratamiento del trabajo de clientes. La identidad OMNIA vive en el marco y la narrativa, no en recolorearlo.

## Texturas, artwork y fondos

- Una textura pequeña, repetitiva y casi sólida puede actuar como superficie: permite adaptar tono y alpha si preserva frecuencia y escala.
- Un hero artwork, collage o gradiente rasterizado es contenido compuesto: usa una variante o excepción, no una transformación por píxel.
- Conserva background-size, position, repeat, crop y breakpoint. Esas decisiones pertenecen a composición.
- Si un fondo claro pierde una forma orgánica, prueba borde teñido, watermark de baja opacidad o tint local antes de cambiar la forma.

## Gradientes y glows

- Los gradientes CSS son propiedades compuestas: clasifica cada stop y conserva dirección, distribución y familia cromática.
- Los gradientes dentro de imágenes son artwork y siguen las reglas del asset.
- Transforma glows dark decorativos en tint, halo contenido o border tint. Conserva ubicación y escala de la firma; reduce bloom y opacidad sobre fondos claros.
- No añadas nuevos glows para compensar una adaptación débil.

## Video, 3D y contenido dinámico

- No filtres frames. Evalúa controles, posters, captions, overlays y stages por separado.
- Un render 3D puede necesitar un entorno light proporcionado por el sistema original; no alteres cámara, geometría, timing ni materiales para crear uno nuevo.
- Para canvas o visualizaciones, usa hooks de tema existentes. Si no existen, limita la entrega a una especificación de colores o registra la excepción; no construyas una arquitectura runtime fuera de alcance.

## Escape hatches

Usa reglas generales primero y una excepción cuando fallen. Documenta cada excepción con:

- componente/asset y contexto;
- rol visual que debía preservarse;
- por qué la transformación general falla;
- tratamiento local elegido;
- estados y breakpoints revisados;
- asset oficial pendiente, si aplica.

Excepciones habituales: logos, hero artwork, glass localizado, gradient meshes, SVG complejos, canvas, video, 3D y componentes de marca especiales. Mantenlas pequeñas, explícitas y reversibles; no permitas que una excepción se convierta en un segundo tema global.

