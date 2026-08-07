# Patrones de interfaz OMNIA

## Composición general

### Patrón repetido

Alterna capítulos claros y oscuros para crear ritmo editorial. Una secuencia fiel puede ser:

1. hero oscuro de alto impacto;
2. franja clara de prueba o clientes;
3. explicación clara y espaciosa;
4. proceso oscuro y lineal;
5. trabajo real sobre fondo claro;
6. bloque de impacto con degradado oscuro;
7. servicios y FAQ claros;
8. CTA y footer oscuros.

Adapta la secuencia al contenido; conserva el contraste narrativo, no el orden literal.

Las composiciones combinan grids, columnas desiguales, elementos alternos y alguna ruptura controlada. En escritorio se permite sticky, escalonamiento o alternancia izquierda/derecha; en móvil todo vuelve a un flujo lineal legible.

## Encabezados de sección

Usa un bloque con:

- eyebrow Lexend en mayúsculas y línea corta;
- H2 grande, corto y balanceado;
- párrafo Quicksand de apoyo;
- margen inferior fluido de aproximadamente `2.75–5.5rem`.

En anchos amplios, separa título y explicación en una retícula aproximada `1.25fr / .75fr`; en móvil apílalos. No repitas exactamente la misma alineación en cada sección.

## Navegación

### Patrón repetido

- Header fijo, fondo Negro OMNIA al `90%`, blur cercano a `18px` y borde inferior blanco al `14%`.
- Altura mínima aproximada `5.25rem` y logo horizontal oficial.
- Links Lexend medianos con subrayado amarillo animado desde un extremo.
- CTA amarillo, texto oscuro, forma pill.
- En móvil, menú desplegable oscuro a ancho completo, filas de al menos `3.75rem`, cierre con Escape y retorno de foco.

El blur es contextual al header flotante; no lo extiendas a todas las superficies.

## Botones y enlaces de acción

### Sistema primario

- Forma pill, altura mínima `3.25rem`, padding aproximado `.85rem 1.35rem`.
- Lexend `600`, tamaño cercano a `.875rem`.
- Borde de `2px`; úsalo visible en variantes secundarias.
- Hover: elevación corta de `-2px`; active: retorno de `1px`.
- Focus: outline amarillo de `3px`, offset `4px`.

Variantes fieles:

- blanco sobre oscuro, hover amarillo;
- negro sobre claro, hover morado;
- transparente con borde blanco sobre oscuro;
- amarillo con texto negro para CTA de navegación.

En móvil estrecho los botones principales ocupan el ancho disponible. Las flechas diagonales `↗` funcionan como microfirma en acciones externas o de contacto, pero no son obligatorias.

## Cards y superficies

No existe una card universal. Selecciona la familia según la función.

### Servicios

- Cards altas, blancas, borde negro al `14%`, radio `1.5rem`, padding fluido `1.5–3rem`.
- Número e identificador arriba, nombre grande, explicación y lista, CTA separado por un divisor.
- Acento departamental en un círculo de fondo muy tenue y bullets.
- En escritorio, retícula de dos columnas con escalonamiento; en móvil, una columna sin offsets.

### Impacto o métricas

- Superficie oscura translúcida sobre degradado.
- Borde blanco al `24%`, radio `1.5rem` y número Lexend de escala extrema.
- El número domina; explicación breve al pie.

### Testimonios y FAQ

- Evita cajas flotantes. Usa estructura editorial con bordes superiores/inferiores.
- Testimonios: columnas separadas por líneas, mucho padding, logo contenido y cita Quicksand.
- FAQ: filas `<details>` de al menos `5rem`, pregunta Quicksand bold y control circular simple.

### Casos de estudio

- La imagen manda; usa borde `12–14%`, radio `1.5rem`, fondo neutral y proporciones explícitas.
- Alterna composición de medios y texto en escritorio; apila en móvil.
- Mantén zoom hover en torno a `1.015`, no una transformación dramática.
- Conserva cada identidad de cliente; OMNIA aparece en el marco y la narrativa, no recoloreando el trabajo.

## Fondos y motivos

### Patrones repetidos

- Base clara: Blanco cálido con tints verticales de morado o azul al `5–16%`.
- Base oscura: Negro OMNIA con radiales azules, morados o carmesíes de baja opacidad.
- Bloques destacados: degradado oscuro azul→morado→carmesí.
- Decoración: una forma lava grande de contorno fino, un isotipo como marca de agua o una línea multicolor de proceso.

Limita cada sección a una firma dominante. Una forma orgánica, un grid técnico o una marca de agua bastan; no los apiles por defecto.

## Jerarquía y ritmo

- Hero y CTA final: títulos de `2.75–7rem`, línea cercana a `.98`, medida `15ch`.
- Títulos de sección: `2.25–4rem`; títulos de cards: `1.35–3.6rem` según función.
- Los números `01`, `02` y etiquetas en mayúsculas refuerzan proceso, transparencia y orientación.
- Los divisores crean orden sin añadir cajas.
- Las secciones admiten densidades distintas: aire en narrativa, compacidad en índices, escala en impacto.

## Responsive

### Principio

Diseña desde el contenido con `clamp()`, grid/flex y queries donde la composición realmente se rompe. Los umbrales observados —aproximadamente `40`, `48`, `52`, `56`, `60`, `62` y `64rem`— son referencias, no breakpoints por dispositivo.

### Comportamientos repetidos

- Por debajo de `40rem`: CTA a ancho completo, ocultar señales secundarias, apilar galerías y reducir decoraciones.
- Entre `48–60rem`: activar encabezados partidos, timelines centrales o retículas de dos columnas cuando el contenido cabe.
- En torno a `62–64rem`: navegación completa, hero en dos columnas, casos alternos y texto sticky.
- Elimina offsets y sticky antes de que causen solapamiento.
- Preserva `1rem` mínimo de margen lateral y evita overflow horizontal.

## Movimiento

### Tokens repetidos

```css
--duration-fast: 160ms;
--duration-normal: 280ms;
--duration-slow: 600ms;
--duration-fluid: 900ms;
--ease-standard: cubic-bezier(.2, 0, 0, 1);
--ease-omnia: cubic-bezier(.22, 1, .36, 1);
--ease-in-out: cubic-bezier(.65, 0, .35, 1);
```

Usa:

- hover corto en botones, flechas y enlaces;
- revelado de opacidad + `translateY` de hasta `1.75rem`;
- zoom de imagen casi imperceptible;
- morfología lava lenta de `10–15s`, alternada y solo en uno o dos puntos clave;
- transición de menú cercana a `280ms`.

Evita scroll hijacking, parallax agresivo, glitches, partículas, loops rápidos o animar todas las secciones.

Con movimiento reducido, elimina desplazamientos, loops y smooth scroll. El contenido y los CTA deben ser visibles y utilizables sin esperar animaciones ni ejecutar JavaScript.

## Accesibilidad visual

- Mantén contraste suficiente sobre gradientes y transparencias.
- No comuniques categoría o estado solo mediante color; añade texto, posición, número o icono.
- Usa foco amarillo visible y no lo recortes con `overflow`.
- Conserva tamaños táctiles de `3rem` o más en controles principales.
- No dependas de hover para revelar contenido esencial.
- Mantén texto narrativo en superficies simples, no sobre decoración compleja.

## Señales de deriva estética

Corrige la dirección si aparecen tres o más de estas señales:

- cuatro acentos saturados dentro de cada componente;
- cards idénticas en todas las secciones;
- sombras profundas o neumorfismo;
- glassmorphism como lenguaje general;
- fondos oscuros/degradados sin pausas claras;
- tipografía geométrica también en todo el cuerpo;
- blobs aleatorios sin relación con contenido;
- estética de “IA” basada en neón, partículas o circuitos;
- logos modificados o trabajo de cliente recoloreado;
- movimiento constante que compite con lectura y rendimiento.

