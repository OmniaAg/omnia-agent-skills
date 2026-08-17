# Selector y runtime de tema OMNIA

## Contenido

1. [Referencia práctica vigente](#referencia-práctica-vigente)
2. [Frontera de responsabilidades](#frontera-de-responsabilidades)
3. [Contrato de estado](#contrato-de-estado)
4. [Resolución inicial por hora local](#resolución-inicial-por-hora-local)
5. [Prioridad y persistencia](#prioridad-y-persistencia)
6. [Aplicación antes del primer paint](#aplicación-antes-del-primer-paint)
7. [Selector visual OMNIA](#selector-visual-omnia)
8. [Iconos canónicos](#iconos-canónicos)
9. [Icon registry y consumo](#icon-registry-y-consumo)
10. [Implementación portable](#implementación-portable)
11. [Ciclo de vida y robustez](#ciclo-de-vida-y-robustez)
12. [Accesibilidad](#accesibilidad)
13. [Validación](#validación)
14. [Anti-patterns](#anti-patterns)

## Referencia práctica vigente

Usar primero el sistema que ya funciona en el proyecto receptor. No crear un segundo store, otro atributo global ni un componente paralelo si existe un contrato correcto. En la tarjeta digital OMNIA que originó esta referencia, las responsabilidades están repartidas así:

| Pieza | Responsabilidad actual |
|---|---|
| `src/layouts/BaseLayout.astro` | Declarar el fallback del documento y ejecutar un bootstrap inline en `<head>` antes del primer paint. |
| `src/scripts/main.js` | Resolver, aplicar y persistir el tema; actualizar el selector; programar los cambios horarios y sincronizar pestañas. |
| `src/pages/index.astro` | Montar el componente una sola vez dentro de la página. |
| `src/components/ThemeToggle.astro` | Renderizar el grupo icon-only con dos botones reales: Moon y Sun. |
| `src/components/BrandHeader.astro` | Consumir el tema resuelto para mostrar la variante de marca compatible, sin participar en su decisión. |
| `src/data/socialIcons.ts` | Actuar como registry existente y única fuente de los SVG `dark` y `light`. |
| `src/styles/legacy.css` | Conservar geometría, responsive e interacción visual del selector. |
| `src/styles/omnia-dark.css` y `src/styles/omnia-light.css` | Entregar los tokens cromáticos del selector y del resto de cada tema. |
| `src/styles/migration.css` | Hacer que los SVG consuman `currentColor` sin duplicar geometría. |

El contrato operativo actual es:

- `localStorage['omnia-theme-mode']` guarda el override manual `dark` o `light`.
- La ausencia de un valor válido equivale internamente a `auto`.
- `new Date().getHours()` usa la hora local del navegador.
- Light rige desde las `06:00` inclusive hasta las `18:00` exclusive; Dark rige de `18:00` a `05:59`.
- `data-theme="dark|light"` en `<html>` expone el tema resuelto a CSS.
- `data-theme-mode="auto|dark|light"` conserva el modo interno.
- `data-theme-source="automatic|manual"` hace explícito el origen de la decisión.
- `style.colorScheme` y `<meta name="theme-color">` se sincronizan con el tema resuelto.
- El selector expone `data-mode`, `data-resolved-theme` y `aria-pressed` en sus botones.
- Mientras el modo sea automático, un timeout recalcula en la siguiente frontera de las `06:00` o `18:00`; al recuperar foco también vuelve a resolver.
- Un evento `storage` aplica cambios manuales realizados en otra pestaña.

Visualmente, la referencia vigente coloca una cápsula flotante abajo a la izquierda respetando safe areas. El control usa dos celdas de `3rem`, borde de `1px`, radio pill y blur localizado; cada opción mantiene target de `3rem × 3rem`, sube `1px` en hover y escala a `.96` en active. En Dark, Moon recibe fondo Blanco cálido y foreground Negro OMNIA mientras Sun queda transparente y muted; en Light ocurre lo inverso, con Sun sobre Negro OMNIA. Mobile compacta inset, gap, padding e icono sin reducir el target. Tratar todo este párrafo como descripción del caso actual, no como geometría obligatoria para otros proyectos.

Tratar estos nombres y archivos como referencia concreta, no como requisitos universales. Si otro proyecto ya usa una clase, un atributo, un store o un registry equivalentes, conservar su convención y portar el comportamiento.

## Frontera de responsabilidades

Mantener esta separación:

| `omnia-aesthetic` | `omnia-light-mode` |
|---|---|
| Geometría y anatomía del control | Transformación cromática y tokens light |
| Tipografía, spacing y layout | Resolución automática inicial |
| Posición, responsive y lenguaje visual | Override manual y persistencia |
| Estilo general de componentes y motion | Aplicación pre-paint y estado del tema |
| Dirección visual de hover, active y focus | Restricciones del selector e iconos Moon/Sun |

Adaptar el selector al sistema visual que `omnia-aesthetic` y el proyecto ya definan. No copiar obligatoriamente su posición flotante, medidas, blur o forma desde la tarjeta digital. Sí conservar el contrato Dark/Light, la iconografía, la accesibilidad y un estado activo inequívoco.

## Contrato de estado

Separar conceptualmente:

- **Tema resuelto:** `dark` o `light`; es el valor que consume la UI.
- **Preferencia manual:** `dark`, `light` o ausencia; solo existe después de una elección del usuario.
- **Modo automático interno:** fallback basado en hora local cuando no hay preferencia manual. No es una tercera opción visible.

Representar `auto` como modo interno es válido, como hace el proyecto actual, pero no renderizar un botón, label, item de menú ni posición adicional para él.

Mantener esta prioridad sin excepciones silenciosas:

```text
PAGE LOAD
   ↓
saved manual preference?
   ├─ YES → use saved theme
   │
   └─ NO
        ↓
      local hour
        ↓
   Light / Dark
```

Después de una interacción:

```text
USER CLICKS MOON OR SUN
        ↓
apply selected theme
        ↓
save manual preference
        ↓
manual preference becomes authoritative
```

No volver a automatización horaria durante esa sesión ni en cargas futuras mientras exista la preferencia manual. Si el producto ofrece una acción explícita de reset en otro contexto, eliminar la preferencia guardada; no convertir ese reset en una tercera opción visible del selector.

## Resolución inicial por hora local

Reutilizar exactamente los umbrales vigentes:

```ts
type Theme = 'dark' | 'light';

function getAutoTheme(date = new Date()): Theme {
  const hour = date.getHours();
  return hour >= 6 && hour < 18 ? 'light' : 'dark';
}
```

Validar las fronteras:

| Hora local | Tema automático |
|---:|---|
| `05:59` | Dark |
| `06:00` | Light |
| `17:59` | Light |
| `18:00` | Dark |

Obtener la hora únicamente en cliente mediante el reloj del dispositivo. No depender de timezone hardcodeada, hora del servidor, geolocalización, IP ni API externa. No sustituir esta regla por `prefers-color-scheme`: una preferencia del sistema puede ser una señal distinta, pero no forma parte del contrato horario OMNIA.

Mientras no exista override manual, recalcular al cruzar una frontera horaria. El proyecto actual programa la siguiente frontera y vuelve a comprobar al recuperar foco; replicar esa conducta cuando una página pueda permanecer abierta durante horas. Cancelar cualquier actualización automática al aplicar una preferencia manual.

## Prioridad y persistencia

Preferir `localStorage`, como la implementación vigente, cuando el entorno lo permita:

```text
no stored manual preference
        ↓
use local time
        ↓
apply resolved theme

manual selection
        ↓
store dark or light
        ↓
apply selected theme

future visit
        ↓
stored manual preference exists?
        ├─ yes → use it
        └─ no  → use local time
```

Aplicar estas reglas:

- Reutilizar la key existente si el proyecto ya tiene una; en la tarjeta actual es `omnia-theme-mode`.
- Guardar solo valores conocidos. Tratar datos inválidos como ausencia de preferencia.
- Considerar `auto` un detalle interno o un valor legacy equivalente a ausencia, nunca un override manual.
- Capturar errores de lectura/escritura. Si storage está bloqueado, resolver por hora local y mantener funcional el selector durante la sesión aunque no pueda persistir.
- No usar cookies, backend o una dependencia nueva cuando `localStorage` ya resuelve el alcance.
- Sincronizar otras pestañas con el evento `storage` cuando el proyecto pueda abrirse simultáneamente.

## Aplicación antes del primer paint

Evitar obligatoriamente white flash, dark flash, flicker y layout shift. Resolver y aplicar el tema antes de que se pinte la interfaz dependiente del tema.

En la implementación Astro actual, un script inline, síncrono y pequeño dentro de `<head>`:

1. lee `localStorage` de forma protegida;
2. resuelve la preferencia manual o la hora local;
3. escribe los atributos del tema sobre `<html>`;
4. sincroniza `color-scheme` y `theme-color`;
5. deja el resultado disponible para el runtime principal.

En otro framework, escoger el mecanismo pre-paint equivalente: script inline de bootstrap, inicializador temprano del documento, plantilla SSR con bootstrap cliente o API nativa del framework. Mantener estos invariantes:

- No esperar hydration, mount, `DOMContentLoaded`, un import dinámico ni una petición de red para decidir el primer tema.
- Mantener el bootstrap sin dependencias y con trabajo mínimo.
- Aplicar el selector global que ya consume el CSS: atributo, clase o mecanismo equivalente.
- Usar un fallback HTML válido, pero no confiar en él como decisión final cuando el cliente puede resolver antes del paint.
- Mantener idénticos los umbrales y la validación de storage entre bootstrap y runtime. Si deben estar duplicados por limitaciones del framework, proteger su paridad con tests.
- No ocultar el body ni introducir medidas distintas entre temas para encubrir el problema.

## Selector visual OMNIA

Renderizar únicamente:

```text
[ moon | sun ]
```

Usar la correspondencia canónica:

- Moon → Dark
- Sun → Light

No mostrar texto visible `Auto`, `Claro`, `Oscuro`, `Dark` o `Light`. La automatización permanece interna.

La tarjeta actual usa dos botones dentro de un grupo accesible. Cada botón declara `data-theme-choice="dark|light"`; el activo recibe `aria-pressed="true"` y un tratamiento visual contrastante entregado por tokens del tema. Sus targets son de `3rem` y la variante móvil conserva la misma función con iconos ligeramente más compactos.

Reutilizar esa anatomía si encaja con el proyecto. Si existe un control equivalente correcto, conservarlo y alinear únicamente iconos, estados y conducta. Hacer evidente el tema activo mediante superficie, foreground, borde u otro recurso compatible con `omnia-aesthetic`; no depender de una animación ni del color del icono como única señal.

## Iconos canónicos

Copiar estos SVG literalmente. No modificar paths, `viewBox`, atributos ni semántica; no recrearlos ni sustituirlos por Lucide, Font Awesome, Heroicons u otra librería.

### DARK — Moon

Nombre recomendado en el registry: `dark`.

```svg
<svg
  xmlns="http://www.w3.org/2000/svg"
  viewBox="0 0 16 16"
  fill="currentColor"
  aria-hidden="true"
  focusable="false"
>
  <path d="M6 .278a.77.77 0 0 1 .08.858 7.2 7.2 0 0 0-.878 3.46c0 4.021 3.278 7.277 7.318 7.277q.792-.001 1.533-.16a.79.79 0 0 1 .81.316.73.73 0 0 1-.031.893A8.35 8.35 0 0 1 8.344 16C3.734 16 0 12.286 0 7.71 0 4.266 2.114 1.312 5.124.06A.75.75 0 0 1 6 .278M4.858 1.311A7.27 7.27 0 0 0 1.025 7.71c0 4.02 3.279 7.276 7.319 7.276a7.32 7.32 0 0 0 5.205-2.162q-.506.063-1.029.063c-4.61 0-8.343-3.714-8.343-8.29 0-1.167.242-2.278.681-3.286"/>
</svg>
```

### LIGHT — Sun

Nombre recomendado en el registry: `light`.

```svg
<svg
  xmlns="http://www.w3.org/2000/svg"
  viewBox="0 0 16 16"
  fill="currentColor"
  aria-hidden="true"
  focusable="false"
>
  <path d="M8 11a3 3 0 1 1 0-6 3 3 0 0 1 0 6m0 1a4 4 0 1 0 0-8 4 4 0 0 0 0 8M8 0a.5.5 0 0 1 .5.5v2a.5.5 0 0 1-1 0v-2A.5.5 0 0 1 8 0m0 13a.5.5 0 0 1 .5.5v2a.5.5 0 0 1-1 0v-2A.5.5 0 0 1 8 13m8-5a.5.5 0 0 1-.5.5h-2a.5.5 0 0 1 0-1h2a.5.5 0 0 1 .5.5M3 8a.5.5 0 0 1-.5.5h-2a.5.5 0 0 1 0-1h2A.5.5 0 0 1 3 8m10.657-5.657a.5.5 0 0 1 0 .707l-1.414 1.415a.5.5 0 1 1-.707-.708l1.414-1.414a.5.5 0 0 1 .707 0m-9.193 9.193a.5.5 0 0 1 0 .707L3.05 13.657a.5.5 0 0 1-.707-.707l1.414-1.414a.5.5 0 0 1 .707 0m9.193 2.121a.5.5 0 0 1-.707 0l-1.414-1.414a.5.5 0 0 1 .707-.707l1.414 1.414a.5.5 0 0 1 0 .707M4.464 4.465a.5.5 0 0 1-.707 0L2.343 3.05a.5.5 0 1 1 .707-.707l1.414 1.414a.5.5 0 0 1 0 .708"/>
</svg>
```

## Icon registry y consumo

Copiar ambos SVG al icon registry que el proyecto ya utilice: `icons.ts`, `uiIcons.ts`, `iconRegistry.ts`, `socialIcons.ts` u otra convención local. No exigir un nombre de archivo específico ni crear un segundo registry.

Registrar conceptualmente:

```ts
dark: {
  name: 'dark',
  label: 'Modo oscuro',
  svg: `<!-- SVG Moon canónico completo -->`,
},

light: {
  name: 'light',
  label: 'Modo claro',
  svg: `<!-- SVG Sun canónico completo -->`,
},
```

Reemplazar los comentarios por los SVG literales de la sección anterior. Mantener las labels como metadata accesible o de desarrollo; no renderizarlas como texto visible del selector.

Consumir después los entries desde el componente mediante la API existente del registry. No pegar nuevamente el SVG dentro de Astro, JSX, templates HTML ni cada botón. Conservar `currentColor` para que los tokens del selector gobiernen el foreground.

## Implementación portable

Usar este pseudocódigo TypeScript como contrato, no como arquitectura paralela:

```ts
type Theme = 'dark' | 'light';

const manualTheme = readValidStoredTheme(); // Theme | null
const initialTheme = manualTheme ?? getAutoTheme(new Date());
applyResolvedTheme(initialTheme, manualTheme ? 'manual' : 'automatic');

function selectTheme(theme: Theme) {
  storeManualTheme(theme);
  cancelAutomaticBoundaryUpdate();
  applyResolvedTheme(theme, 'manual');
}
```

En proyectos que ya modelen `auto|dark|light`, mantener ese modelo. En proyectos que representen auto como `null`, mantener `null`. En ambos casos, la semántica debe ser la misma: solo la ausencia de override manual consulta la hora.

Centralizar la aplicación para que una sola operación sincronice, según existan en el proyecto:

- selector global de CSS (`data-theme`, clase o store);
- `color-scheme`;
- `meta[name="theme-color"]`;
- UI y `aria-pressed` del selector;
- assets temáticos que ya formen parte del sistema;
- programación o cancelación de la siguiente frontera automática.

No atar el contrato a Astro. Traducir el bootstrap y el lifecycle a React, Next.js, HTML/CSS/JS u otro framework sin cambiar prioridad, horarios, iconos ni experiencia visible.

## Ciclo de vida y robustez

- Inicializar los listeners una sola vez; con navegación cliente, usar el hook del framework sin duplicarlos.
- Programar la siguiente frontera solo en modo automático y recalcular con una `Date` nueva al ejecutarse.
- Recalcular al recuperar foco o visibilidad si la pestaña pudo atravesar una frontera suspendida.
- Cancelar timeouts automáticos al seleccionar Moon o Sun.
- Escuchar `storage` si se requiere consistencia entre pestañas.
- Actualizar primero el estado global y después la UI derivada para evitar estados contradictorios.
- No lanzar errores si falta el control en una página que comparte el layout; aplicar el tema global aunque el selector no esté montado.
- Mantener efectos cromáticos y transiciones incapaces de provocar cambio de medidas o layout shift.

## Accesibilidad

Cumplir como mínimo:

- Usar `<button type="button">` para cada elección cuando la UI tenga dos acciones.
- Agruparlos con un nombre accesible, por ejemplo `role="group" aria-label="Seleccionar tema"`, o semántica equivalente.
- Proporcionar `aria-label="Activar modo oscuro"` y `aria-label="Activar modo claro"`.
- Exponer el estado con `aria-pressed`, `aria-current` o un patrón equivalente coherente; en la referencia vigente se usa `aria-pressed`.
- Conservar navegación nativa por teclado y orden de foco lógico.
- Mostrar `:focus-visible` con contraste suficiente y sin recorte.
- Mantener targets táctiles apropiados; la referencia usa `3rem × 3rem`.
- Hacer inequívoco el estado activo con contraste suficiente y una señal que no dependa solo del hue.
- Mantener los SVG decorativos con `aria-hidden="true"` y `focusable="false"`; colocar el nombre accesible en el botón, no en el SVG.
- No añadir texto visible para resolver accesibilidad: usar nombres y estados accesibles.

## Validación

Antes de entregar, comprobar:

### Carga inicial

- Sin storage a `05:59` → Dark.
- Sin storage a `06:00` → Light.
- Sin storage a `17:59` → Light.
- Sin storage a `18:00` → Dark.
- Con `dark` guardado a las `14:00` → Dark.
- Con `light` guardado a las `22:00` → Light.
- Con storage inválido o inaccesible → fallback horario sin romper la página.
- Cold load y reload → ningún flash de la polaridad incorrecta ni layout shift.

### Interacción y persistencia

- Click en Moon → `data-theme` o estado equivalente pasa a Dark, Moon queda activo y `dark` se guarda.
- Click en Sun → pasa a Light, Sun queda activo y `light` se guarda.
- Reload → el override manual sigue siendo authoritative.
- Una preferencia manual cancela la actualización automática programada.
- Cambio en otra pestaña → se sincroniza si el producto soporta ese caso.
- No existe opción visible `Auto` ni labels visibles Dark/Light.

### UI, iconos y accesibilidad

- El componente consume `dark` y `light` desde el registry existente.
- Los dos SVG coinciden literalmente con los canónicos y conservan `currentColor`, `aria-hidden` y `focusable="false"`.
- Solo el botón activo expone `aria-pressed="true"`.
- Tab, Enter y Space funcionan mediante controles nativos.
- Focus, contraste y touch targets funcionan en dark, light, desktop y mobile.
- La estética y posición pertenecen al proyecto; no se rediseñó el selector existente.

### Integración cromática

- El tema resuelto activa los tokens light o dark existentes; el runtime no contiene una segunda paleta.
- `omnia-light-mode` no cambia geometría, tipografía, spacing, layout ni motion del sistema.
- `omnia-aesthetic` permanece intacta.

## Anti-patterns

Rechazar o corregir:

- selector con tres opciones visibles Dark/Light/Auto;
- labels visibles `Auto`, `Claro`, `Oscuro`, `Dark` o `Light`;
- `prefers-color-scheme`, hora del servidor o API externa sustituyendo la hora local acordada;
- automatización que pisa una preferencia manual;
- storage escrito en cada carga automática como si fuera elección del usuario;
- decisión de tema después de hydration o mount que causa flash;
- SVG duplicados dentro de componentes o reemplazados por icon libraries;
- iconos sin nombre accesible en el control;
- estado activo comunicado solo mediante una transición o un color ambiguo;
- nueva arquitectura de theming cuando el proyecto ya posee una funcional;
- estilos universales del botón que contradicen `omnia-aesthetic` o rediseñan el proyecto receptor.
