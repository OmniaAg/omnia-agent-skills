# Patrón Linktree y hubs compactos OMNIA

Aplicar este módulo a link-in-bio, directorios de enlaces, páginas de contacto y micrositios compactos cuya tarea principal sea llevar a pocas acciones oficiales. Conservar la lógica visual; no copiar contenido ni convertir este caso en plantilla universal.

## Contenido

1. [Criterio de patrón](#criterio-de-patrón)
2. [Anatomía](#anatomía)
3. [Shell y geometría](#shell-y-geometría)
4. [Composición desktop](#composición-desktop)
5. [Composición mobile](#composición-mobile)
6. [Identidad e introducción](#identidad-e-introducción)
7. [Navegación tipo índice](#navegación-tipo-índice)
8. [Bloque social y footer](#bloque-social-y-footer)
9. [Densidad y alineación](#densidad-y-alineación)
10. [Estados y accesibilidad](#estados-y-accesibilidad)
11. [Adaptación de contenido](#adaptación-de-contenido)
12. [Golden references](#golden-references)
13. [Validación](#validación)

## Criterio de patrón

Usar este patrón cuando el contenido pueda entenderse como **identidad breve + directorio de acciones + contacto social**. La navegación es el contenido, no el acceso a una narrativa más larga.

No usarlo por el simple hecho de que una página sea corta. Si necesita hero persuasivo, prueba, casos, explicación, varios CTA o capítulos de contenido, gobernarla con `interface-patterns.md`.

La firma de esta familia es:

- un canvas neutro oscuro y un único panel contenido;
- dos zonas complementarias en desktop y un flujo continuo en mobile;
- marca e introducción con aire, directorio compacto con ritmo lineal;
- jerarquía creada por alineación, divisores, numeración y contraste, no por una pila de cards;
- una sola intervención cromática dominante: una regla fina con el gradiente OMNIA.

## Anatomía

Ordenar la experiencia así:

1. shell de página centrado;
2. panel principal;
3. zona de identidad con logo, claim y descripción;
4. zona de directorio con etiqueta, lista primaria, bloque social y footer;
5. estados interactivos discretos y accesibles.

Mantener esta jerarquía aunque cambien las etiquetas, la cantidad de enlaces o el tipo de contacto. No insertar header global, hero adicional, menú hamburguesa ni CTA flotante si el directorio ya resuelve la navegación.

## Shell y geometría

Usar los fundamentos de color y tipografía sin redefinirlos. Para esta expresión compacta, tomar como referencia:

| Rol | Valor o relación observada |
|---|---|
| Canvas | token Negro OMNIA |
| Panel | token de oscuro elevado principal |
| Texto principal | token Blanco cálido |
| Texto secundario | token de texto inverso secundario |
| Borde | blanco cálido al `18%`; rango válido `14–24%` |
| Ancho máximo del panel | cerca de `68rem` |
| Padding exterior | `clamp(1rem, 4vw, 4rem)` más safe areas |
| Padding interior | `clamp(1.5rem, 5vw, 4rem)` |
| Radio del panel | `2rem`; bajar a `1.5rem` en anchos extremos |
| Regla superior | gradiente OMNIA, `2px`, inset de `1.25–1.5rem` |

- Centrar el panel en ambos ejes cuando su contenido cabe; permitir scroll natural y conservar padding vertical cuando no cabe.
- Mantener el panel plano: borde de `1px`, sin sombra visible ni glassmorphism.
- Colocar la regla cromática dentro del panel, cerca del borde superior. Tratarla como firma, no como barra de progreso ni decoración repetida.
- Reservar el resto del fondo para el silencio visual. No añadir blobs, grid técnico, watermark o radiales por defecto.

## Composición desktop

Activar la composición dividida cuando ambas zonas quepan con comodidad; la referencia lo hace alrededor de `48rem`.

- Usar dos columnas desiguales: identidad cercana a `.8fr` y directorio a `1.2fr`, con la primera nunca menor de unos `16rem`.
- Separar columnas con un gap fluido cercano a `2–4rem`.
- Añadir un divisor vertical de `1px` al inicio de la zona de directorio y un padding izquierdo cercano a `2–3rem`.
- Alinear logo, claim, descripción, etiquetas de grupo y redes a la izquierda.
- Mantener el footer dentro de la columna de directorio; no convertirlo en una franja de ancho completo.

La relación de columnas importa más que una coordenada exacta: la identidad debe sentirse estable y silenciosa; el directorio, más ancho y operativo.

## Composición mobile

- Apilar identidad y directorio dentro del mismo panel; no crear dos cards.
- Centrar logo, claim, descripción, redes y footer. Mantener la etiqueta y las filas del directorio alineadas para escaneo.
- Retirar el divisor vertical y cualquier padding que simule una segunda columna.
- Conservar un mínimo de `1rem` de margen exterior y evitar que el panel toque el viewport.
- En anchos cercanos o inferiores a `23.5rem`, reducir padding lateral del panel a unos `1.25rem`, ocultar la numeración si compromete el título y apilar el footer sin separador ornamental.

El mobile no es una versión “card stack” del desktop: es la misma secuencia editorial en flujo lineal.

## Identidad e introducción

- Usar el logotipo horizontal oficial claro sobre el panel oscuro. Conservar transparencia, proporción y zona libre; no reconstruirlo ni sustituirlo con texto.
- Dar al logo una anchura fluida aproximada de `14–22rem`, limitada siempre por su contenedor.
- Evitar un titular hero que compita con el logo. Mantener una estructura semántica accesible —por ejemplo, un `h1` visualmente oculto o un encabezado breve si el contenido lo exige— sin alterar la jerarquía visual.
- Colocar después un claim corto en Lexend `600`, alrededor de `.875rem`, mayúsculas, tracking cercano a `.08em`, color amarillo.
- Añadir una descripción breve en Quicksand `500`, alrededor de `1rem`, línea `1.65`, color secundario y medida máxima cercana a `31rem`.
- Usar aproximadamente `1.5rem` entre logo y bloque de copy, y `.75–1.25rem` dentro del copy.
- Alinear a la izquierda en desktop y centrar en mobile. No forzar centrado global en pantallas amplias.

El claim y el texto pueden cambiar; sus roles no. El claim nombra la promesa y la descripción explica en una o dos frases qué conecta la organización con los enlaces.

## Navegación tipo índice

Tratar la lista primaria como índice editorial, no como botones pill ni cards independientes.

- Introducir cada grupo con una etiqueta funcional corta —por ejemplo, “Explora” o “Conecta”— en Lexend `600`, `.75rem`, mayúsculas y tracking cercano a `.14em`.
- Usar una lista semántica dentro de `nav` cuando el conjunto sea navegación.
- Construir cada fila con tres zonas: número, título y señal de destino. Usar `01`, `02`, `03` solo cuando el orden facilite orientación; mantenerlo estable y secuencial.
- Mantener altura mínima cercana a `4.5rem`, padding contenido y borde superior de `1px`; cerrar la última fila con borde inferior.
- Usar título Lexend `500` alrededor de `1rem`, número Lexend `600` alrededor de `.75rem` y flecha externa simple de unos `24px` con trazo de `2px`.
- Mantener radios discretos, alrededor de `.625rem`, para permitir el estado de superficie sin convertir cada fila en cápsula.
- Identificar enlaces externos visualmente y con texto accesible. Usar `target="_blank"` solo cuando sea deliberado y acompañarlo de `rel="noopener noreferrer"`.

Para un estado real “próximamente”, retirar la acción, usar `aria-disabled="true"`, atenuar la fila y mostrar un status pill pequeño en amarillo. No inventar destinos futuros para llenar el layout.

## Bloque social y footer

- Separar el bloque social de la lista primaria con aire de grupo, cerca de `2rem`, no con otra card.
- Usar iconos sociales oficiales o SVG monocromos reconocibles dentro de objetivos circulares de `3.25–3.75rem`.
- Aplicar borde fino inverso, fondo transparente e icono de `1.25–1.5rem`.
- Mantener un gap fluido de `.75–1rem`; alinear a la izquierda en desktop y centrar en mobile.
- Incluir nombre de plataforma y aviso de nueva pestaña en el nombre accesible; no depender solo de la silueta del icono.
- Colocar el footer después de las redes, con tipografía secundaria de `.75rem`, bajo contraste y composición centrada dentro de la zona de directorio.
- Usar un punto amarillo pequeño para separar copyright y lema cuando quepan en una línea; retirarlo al apilar.

El lema, año y obligaciones legales se adaptan al proyecto. No copiar datos de OMNIA a una entidad distinta ni inventar redes ausentes.

## Densidad y alineación

Combinar dos densidades:

- **identidad:** aire amplio, pocos elementos, lectura pausada;
- **directorio:** filas compactas y repetibles, agrupadas por divisores;
- **entre grupos:** separación visible para que lista, redes y footer no formen una masa uniforme.

Usar el espacio para mostrar pertenencia. Los elementos dentro de una fila permanecen próximos; logo y copy respiran; lista y redes se separan. No aplicar el espaciado de secciones de una landing ni aumentar arbitrariamente todos los gaps para “hacerlo premium”.

## Estados y accesibilidad

Tomar como estado por defecto de la implementación de referencia:

- fila hover: superficie blanca, texto oscuro, número morado y flecha desplazada `2px` hacia arriba y derecha;
- fila active: escala cercana a `.99`;
- social hover: superficie y borde blancos, icono oscuro y elevación de `-2px`;
- social active: descenso de `1px` y escala cercana a `.98`;
- focus visible: outline amarillo de `3px` con offset de `4px`.

Mantener transiciones cortas cercanas a `160ms`. No usar glow, rebote, gradiente animado ni revelar información esencial solo en hover. Con `prefers-reduced-motion`, eliminar desplazamientos y escalas sin perder el cambio de contraste.

Preservar objetivos táctiles de al menos `3rem`, orden de foco coherente, skip link cuando corresponda y contraste suficiente. No imitar una omisión semántica de la referencia si puede corregirse sin cambiar su apariencia.

## Adaptación de contenido

Mantener invariantes: panel único, relación identidad/directorio, jerarquía tipográfica, organización por líneas, neutralidad dominante, acento cromático escaso y transformación responsive.

Adaptar según el contenido:

- número y nombres de enlaces;
- etiquetas de grupo;
- claim y descripción;
- plataformas sociales;
- presencia de estados deshabilitados;
- copy y obligaciones del footer;
- proporción de columnas dentro del rango observado cuando el contenido lo requiera.

No inventar: logo, iconos oficiales, enlaces, datos de contacto, estados, claims de marca o decoraciones para ocupar huecos. No reutilizar obligatoriamente el ancho, el copy ni la cantidad de enlaces del caso de referencia.

## Golden references

Usar las imágenes después de aplicar las reglas escritas, como validación adicional:

- [desktop](../visual-reference/linktree-desktop.png): silueta del shell, proporción de columnas, divisor, densidad y alineación;
- [mobile](../visual-reference/linktree-mobile.png): panel único, orden, centrado selectivo y márgenes;
- [recorte social](../visual-reference/linktree-link-hover.png): contiene el bloque social pese al nombre del archivo;
- [recorte de enlaces](../visual-reference/linktree-social-hover.png): contiene las filas primarias pese al nombre del archivo.

Los recortes de hover reflejan el comportamiento del CSS ejecutable actual. Usarlos junto con la sección [Estados y accesibilidad](#estados-y-accesibilidad) para validar geometría, jerarquía y contraste.

No depender de la interpretación de píxeles para reconstruir la interfaz ni copiar coordenadas del viewport de captura.

## Validación

Antes de entregar, comprobar:

- ¿Se reconoce un hub compacto, no una landing comprimida?
- ¿Existe un único panel y una sola firma cromática dominante?
- ¿La identidad respira mientras el directorio conserva densidad lineal?
- ¿Desktop usa dos zonas y mobile un flujo único sin cards añadidas?
- ¿Los enlaces se leen como índice numerado y no como botones genéricos?
- ¿Redes y footer ocupan su jerarquía secundaria?
- ¿No se inventaron assets, destinos, estados o contenido?
- ¿Hover, focus, teclado, safe areas, anchos extremos y movimiento reducido funcionan sin alterar la composición?
