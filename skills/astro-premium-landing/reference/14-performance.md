# Rendimiento y Core Web Vitals

**Cargar cuando:** se añaden assets, fuentes, scripts, islas, animaciones, integraciones o se prepara producción.

## Presupuesto antes de optimizar

Registrar objetivos del intake para:

- Peso y dimensiones de la imagen LCP.
- JavaScript inicial y total hidratado.
- Fuentes, pesos y subconjuntos.
- CSS y dependencias externas.
- LCP, INP y CLS en dispositivo/red de referencia.

Los valores de laboratorio son evidencia comparativa, no sustituyen datos de campo.

## Orden de decisión

1. Generar HTML estático y semántico.
2. Reducir trabajo y dependencias antes de minificar.
3. Optimizar la imagen LCP, dimensiones y orden de descubrimiento.
4. Eliminar hidratación y scripts que no aporten interacción.
5. Cargar tarde lo secundario con la estrategia más restrictiva.
6. Corregir fuentes, CSS, terceros y caché según medición.

## Guardrails obligatorios

- No hidratar contenido estático.
- No usar `client:load` si la interacción puede esperar.
- No cargar analítica, chat, mapas o videos pesados sin consentimiento/estrategia aprobada.
- Definir dimensiones o proporción de imágenes, embeds y elementos que aparecen tarde.
- Evitar preload indiscriminado; priorizar solo recursos críticos confirmados.
- No sacrificar accesibilidad o contenido por una puntuación.
- Medir build y ruta final, no solo servidor de desarrollo.

## Diagnóstico por señal

- **LCP:** origen y tamaño del recurso, prioridad, TTFB, CSS bloqueante, fuente y render tardío.
- **INP:** listeners, terceros, hidratación, tareas largas y trabajo síncrono durante interacción.
- **CLS:** imágenes/fuentes/embeds sin reserva, contenido inyectado y animación de layout.

## Terceros

Para cada tercero registrar propietario, propósito, momento de carga, consentimiento, dominios, bytes y fallback. Eliminar widgets que puedan ser enlace/imagen estática hasta interacción.

## Verificación

- Comparar tamaño de `dist/`, bundles y requests antes/después cuando las herramientas estén disponibles.
- Probar throttling razonable, caché fría/caliente, móvil y reduced motion.
- Inspeccionar errores de consola, tareas largas y layout shifts.
- Documentar límites: una auditoría local no confirma métricas de usuarios reales.

Fuentes oficiales relacionadas: [imágenes](https://docs.astro.build/en/guides/images/), [scripts](https://docs.astro.build/en/guides/client-side-scripts/), [frameworks](https://docs.astro.build/en/guides/framework-components/).

