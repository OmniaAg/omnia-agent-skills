---
name: omnia-light-mode
description: "Transforma semánticamente a light mode interfaces que ya siguen `omnia-aesthetic` y estandariza su runtime Dark/Light: selector OMNIA Moon/Sun sin texto visible, tema inicial por hora local, override manual, persistencia y prevención de flash. Conserva intactos layout, composición, tipografía, jerarquía, spacing, geometría, componentes, contenido y motion. Usa esta modifier junto con `omnia-aesthetic` siempre que se pida una versión clara, light theme, cambio de polaridad, selector de tema o adaptación cromática clara de una experiencia OMNIA existente. No usar para diseñar OMNIA desde cero, rediseñar una interfaz ni tematizar marcas ajenas."
---

# OMNIA Light Mode

## Propósito

Reinterpretar la expresión cromática dark de una interfaz OMNIA como su equivalente light y, en productos que ofrecen ambas polaridades, implementar el contrato funcional del selector Dark/Light. Esta skill es una **modifier de polaridad**, no una estética alternativa ni una copia de `omnia-aesthetic`.

> Light mode is not an inverted dark mode. It is the same visual system under a different luminance environment.

## Dependencia y autoridad

1. Carga primero [`omnia-aesthetic`](../omnia-aesthetic/SKILL.md) y las referencias que esa skill enrute para el formato actual.
2. Trátala como fuente de verdad estable e intocable. No edites, corrijas, refactorices ni amplíes sus archivos.
3. Deja que `omnia-aesthetic` gobierne layout, composición, tipo, jerarquía, spacing, sizing, anatomía, radios, ritmo, contenido, arquitectura de información, interacción y motion.
4. Esta modifier gobierna la adaptación contextual de color, superficies, contraste, bordes, sombras, highlights, glows, gradientes, overlays y assets dependientes del tema.
5. También gobierna exclusivamente el contrato funcional del selector: resolución inicial por hora local, override manual, persistencia, aplicación pre-paint, estado accesible e iconos canónicos Moon/Sun.
6. Deja que `omnia-aesthetic` determine la apariencia final y la colocación del control. Esta modifier define su comportamiento, iconografía, estados y restricciones; no impone una geometría universal.
7. Si una propiedad no cambiaría únicamente por variar el entorno de luminancia y no pertenece al contrato funcional anterior, queda fuera de alcance. Ante cualquier conflicto fuera de estas responsabilidades, gana `omnia-aesthetic`.

Si la dependencia no está disponible, no reconstruyas la identidad desde esta skill: informa que falta `omnia-aesthetic`.

## Flujo de trabajo

1. **Congela los invariantes.** Registra la estructura visual y conductual que no puede cambiar; conserva también contenido y estados.
2. **Inventaría el sistema dark.** Localiza tokens y declaraciones dependientes del tema, su consumidor, estado, fondo real y posible asset asociado.
3. **Clasifica por rol.** Decide si cada uso es canvas, superficie, texto, borde, acento, sombra, glow, gradiente, overlay o media. No conviertas hexadecimales aislados.
4. **Define los polos light.** Construye canvas, superficies y texto desde los anclajes OMNIA; preserva relaciones perceptuales, no distancias numéricas.
5. **Transforma por contexto.** Aplica las reglas del rol y divide localmente un token solo si un mismo valor cumple funciones incompatibles. No renombres variables solo para satisfacer la taxonomía.
6. **Adapta marca y media.** Conserva el hue de marca cuando sea viable; evalúa cada asset antes de filtrarlo, sustituirlo o dejarlo intacto.
7. **Añade escape hatches.** Resuelve localmente logos, artwork, glass, SVG complejos, canvas, video o 3D que no soporten la regla general.
8. **Implementa el contrato de tema.** Si la interfaz ofrece ambos temas, conserva primero el sistema existente y completa únicamente lo necesario para cumplir prioridad manual, automatización horaria, persistencia, aplicación pre-paint e iconografía canónica.
9. **Valida en pares.** Compara dark y light con el mismo contenido, viewport, estado y breakpoint. La diferencia importante debe ser cromática, salvo el estado propio del selector.

## Principios críticos

- Razona `rol visual semántico → equivalente light`, nunca `hex viejo → hex nuevo`.
- Permite que los neutrales cambien ampliamente; conserva hue, función y reconocimiento de los colores OMNIA siempre que el contraste lo permita.
- Preserva jerarquía, pertenencia, separación y énfasis aunque el mecanismo cambie de luminosidad a borde, tint, highlight o sombra tenue.
- No asumas que todo valor oscuro debe aclararse: texto, iconos, scrims y CTA oscuros pueden seguir siendo oscuros por su función.
- No inviertas automáticamente fotografías, logos, ilustraciones, videos, renders, gradientes rasterizados ni trabajo de clientes.
- Prefiere una excepción pequeña y documentada a degradar un elemento especial con una regla global.
- No introduzcas neumorfismo: `omnia-aesthetic` lo declara contrario al sistema. Expresa profundidad clara con contraste tonal, bordes y sombras de contacto contenidas.
- Mantén la automatización interna: ausencia de preferencia manual → hora local; preferencia manual guardada → esa preferencia gana hasta que se elimine explícitamente.
- Expón solo Moon → Dark y Sun → Light. No muestres `Auto`, `Claro`, `Oscuro`, `Dark` ni `Light` como labels visibles.
- Reutiliza literalmente los SVG canónicos desde el icon registry del proyecto; no los dupliques en componentes ni los sustituyas por una librería.

## Carga modular

- Lee siempre [foundations.md](references/foundations.md) para establecer roles, polos y relaciones.
- Lee [transformation-rules.md](references/transformation-rules.md) al definir tokens o adaptar superficies, componentes, estados y efectos.
- Lee [media-and-assets.md](references/media-and-assets.md) si existen logos, iconos, SVG, imágenes, texturas, artwork, video, canvas o 3D.
- Lee [theme-switching.md](references/theme-switching.md) siempre que la entrega sea una interfaz navegable con Dark/Light, incluya o audite el selector, o necesite resolver carga inicial y persistencia. Omítela solo en un artefacto estático o una auditoría exclusivamente cromática sin runtime.
- Lee siempre [validation.md](references/validation.md) antes de entregar una especificación, auditoría o implementación.

## Límites

- No rediseñes para “aprovechar” el light mode.
- No cambies el stack, la arquitectura CSS ni el naming del proyecto salvo que una separación contextual sea imprescindible.
- No generes una paleta complementaria ni copies los colores por defecto de Dark Reader.
- No conviertas esta guía en inversión automática, filtro global, extensión del navegador ni una tercera opción visual `Auto`.
- No impongas Astro, un componente universal ni una arquitectura de estado nueva: adapta el contrato al framework y a las convenciones existentes.
