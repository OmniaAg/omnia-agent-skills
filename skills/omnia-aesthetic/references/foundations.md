# Fundamentos visuales de OMNIA

## Contenido

1. [Cómo interpretar las reglas](#cómo-interpretar-las-reglas)
2. [Tesis visual](#tesis-visual)
3. [Color](#color)
4. [Tipografía](#tipografía)
5. [Espacio y retícula](#espacio-y-retícula)
6. [Geometría, bordes y profundidad](#geometría-bordes-y-profundidad)
7. [Assets y tratamiento de imagen](#assets-y-tratamiento-de-imagen)
8. [Qué no debe convertirse en regla](#qué-no-debe-convertirse-en-regla)

## Cómo interpretar las reglas

- **Núcleo:** identidad oficial; cambia solo si existe un manual posterior.
- **Patrón repetido:** decisión observada de forma consistente y reutilizable.
- **Contextual:** solución útil en una composición concreta, no una obligación de marca.

## Tesis visual

**Núcleo:** “Ingeniería Creativa para Humanos” se expresa como precisión + humanidad.

- Precisión: Lexend, retículas claras, numeración, divisores, contraste y procesos visibles.
- Humanidad: Quicksand, curvas orgánicas, espacio para respirar y movimiento fluido.
- Personalidad: minimalista, espaciosa, contemporánea, creativa, profesional y dinámica sin caos.
- Firma: tensión entre geometría ordenada y formas líquidas derivadas del isotipo.

## Color

### Paleta de identidad — núcleo

| Rol | Color | Uso principal |
|---|---:|---|
| Negro OMNIA | `#161616` | Fondos oscuros, texto y masa visual principal |
| Blanco cálido | `#FDFDFC` | Fondo claro y texto inverso |
| Morado | `#56167D` | Acento conceptual, primario y de autoridad |
| Azul | `#005B85` | Confianza, estructura y tecnología |
| Carmesí | `#C8003B` | Transformación, creatividad y energía |
| Amarillo | `#FCBF4A` | Claridad, foco, CTA y microacentos |

El balance es neutro primero. En cada sección elige uno o dos acentos; reserva la secuencia completa para transiciones, líneas de proceso o momentos de identidad explícita.

### Neutros de interfaz — patrón repetido

Usa estos apoyos sin tratarlos como nuevos colores de marca: blanco `#FFFFFF`, superficie suave `#F7F6F8`, oscuro elevado principal `#1D1D1D`, oscuro suave secundario `#242424`, texto suave `#414141`, texto secundario `#666666` y texto inverso secundario `#C8C8C8`. No intercambiar los dos oscuros sin una razón de jerarquía: el principal separa una superficie del canvas Negro OMNIA; el secundario crea un nivel anidado cuando realmente hace falta.

Los divisores se construyen por transparencia:

- sobre claro: Negro OMNIA al `14%`, hasta `28%` para mayor énfasis;
- sobre oscuro: Blanco cálido al `14–24%`, hasta `35%` en cortes importantes.

### Degradados — núcleo

```css
--gradient-omnia: linear-gradient(
  90deg,
  #005b85 0%,
  #56167d 32%,
  #c8003b 68%,
  #fcbf4a 100%
);

--gradient-omnia-dark: linear-gradient(
  135deg,
  #005b85 0%,
  #56167d 46%,
  #c8003b 100%
);
```

También son válidos gradientes binarios azul→morado, morado→carmesí y carmesí→amarillo. Usa tints o radiales con los mismos colores y baja opacidad. No emplees arcoíris genérico, degradado en texto corrido ni gradientes como fondo de todas las secciones.

## Tipografía

### Familias y función — núcleo

- **Lexend:** títulos, navegación, botones, etiquetas, números, métricas y elementos funcionales.
- **Quicksand:** párrafos, explicaciones, FAQ, testimonios y mensajes humanos.
- Autohospeda ambas familias. Si Quicksand `400` no existe, usa `500` para cuerpo; reserva `300` para tamaños amplios.

### Jerarquía — patrón repetido

```css
--font-size-xs: .75rem;
--font-size-sm: .875rem;
--font-size-base: 1rem;
--font-size-md: 1.125rem;
--font-size-xl: 1.5rem;
--font-size-2xl: clamp(1.75rem, 3vw, 2.5rem);
--font-size-3xl: clamp(2.25rem, 5vw, 4rem);
--font-size-4xl: clamp(3rem, 7vw, 6.5rem);
```

- H1: Lexend `600–800`, línea `0.98–1.05`, tracking aproximado `-0.035em`, longitud breve.
- H2: Lexend `500–700`, línea `1.05–1.15`, normalmente limitado a `15–16ch`.
- H3: Lexend `500–600`.
- Cuerpo: Quicksand `500`, `1rem–1.125rem`, línea aproximada `1.65`, medida cómoda de `36–45rem`.
- Eyebrows y etiquetas: Lexend `600–700`, `.75rem`, mayúsculas, tracking `.14em`, acompañadas a menudo por una línea corta.

Usa `text-wrap: balance` en títulos y `pretty` en párrafos cuando esté disponible. Evita bloques extensos centrados y pesos ligeros en tamaños pequeños.

## Espacio y retícula

### Escala — patrón repetido

Parte de una unidad de `.25rem` y usa saltos `1, 2, 3, 4, 5, 6, 8, 10, 12, 16, 20, 24, 32`.

```css
--page-padding: clamp(1rem, 4vw, 4rem);
--section-space: clamp(5rem, 10vw, 9rem);
--section-space-small: clamp(3.5rem, 7vw, 6rem);
--content-gap: clamp(1.5rem, 4vw, 3rem);
--grid-gap: clamp(1rem, 3vw, 2rem);
```

Anchos de referencia: contenedor `80rem`, ancho `90rem`, contenido `68rem`, texto `45rem`, texto estrecho `36rem`.

El espacio negativo es parte de la identidad, pero es una **relación**, no padding grande en todas partes. Abrir aire entre grupos y comprimir elementos de una misma familia —por ejemplo, filas de un índice— para hacer visible la jerarquía. No aplicar mecánicamente los tokens de sección a un micrositio compacto.

## Geometría, bordes y profundidad

### Núcleo y patrones repetidos

- Bordes: `1px` por defecto; `2px` para controles o énfasis.
- Radios: `.375rem`, `.625rem`, `1rem`, `1.5rem`, `2rem` y pill `999px`.
- Cards principales: radio usual `1.5rem`; llamadas o paneles destacados: `2rem`; controles: pill.
- Formas lava: radios elípticos asimétricos, contorno fino o relleno tenue, siempre con función compositiva.
- Profundidad: contraste de planos, transparencia y bordes. Las sombras son excepcionales y suaves.

**Neumorfismo: ausente y contrario al sistema.** No uses superficies extruidas, dobles sombras claras/oscuras ni controles que dependan de relieve.

La transparencia con desenfoque aparece solo en capas flotantes concretas, como navegación o chips sobre un hero. No conviertas el glassmorphism en lenguaje general.

## Assets y tratamiento de imagen

### Núcleo

- Usa únicamente logos oficiales y conserva proporción, zona libre, color y contraste.
- La identidad OMNIA combina un isotipo circular orgánico con degradado carmesí→morado→azul y versiones horizontal, vertical, isotipo y marca de agua.
- Los identificadores departamentales son glifos simples —plumín, caballo, código y obturador— con el mismo degradado familiar; funcionan como un sistema, no como marcas independientes.
- Prioriza proyectos, procesos, equipo y materiales reales autorizados. No sustituyas prueba real por stock genérico.
- Mantén los colores de cada cliente. Encapsula la variedad con marcos neutros, proporciones consistentes y suficiente espacio.

La marca de agua puede usar opacidad aproximada `15–30%` sobre claro y `40–50%` sobre oscuro. Puede recortarse parcialmente si sigue reconocible y no compite con el contenido.

## Qué no debe convertirse en regla

Estas decisiones son **contextuales**, aunque sean compatibles con la identidad:

- una órbita de cuatro departamentos en el hero;
- un grid técnico detrás del hero;
- texto sticky junto a galerías de casos;
- cards escalonadas exactamente `5rem`;
- un badge orgánico con las letras “IA”;
- la asignación fija morado/rojo/azul/amarillo a cada departamento;
- un índice lateral específico para FAQ;
- los tokens de sombra definidos pero no usados como sistema.

Reutiliza su principio —integración, ritmo, jerarquía— sin copiar obligatoriamente su forma.

