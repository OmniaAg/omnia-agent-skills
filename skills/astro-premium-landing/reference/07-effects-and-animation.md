# Efectos y animaciones

**Cargar cuando:** el brief pide movimiento, scroll effects, transiciones o una firma visual animada.

## Jerarquía de solución

1. Sin movimiento si no mejora comprensión, orientación o marca.
2. CSS para estados, entradas simples y transiciones locales.
3. Web Animations API o JavaScript nativo para secuencias pequeñas controladas.
4. API nativa del navegador como `IntersectionObserver` para activar trabajo bajo demanda.
5. Librería solo para coordinación compleja demostrada; medir su coste y reutilización.

## Obligatorio

- Definir función del efecto: feedback, continuidad, jerarquía, demostración o firma de marca.
- Mantener contenido y CTA disponibles sin JavaScript y sin esperar la animación.
- Respetar `prefers-reduced-motion: reduce`; eliminar desplazamientos, parallax y bucles no esenciales, no solo acelerarlos.
- Animar preferentemente `transform` y `opacity`; medir cualquier propiedad que provoque layout o pintura costosa.
- Evitar bloquear interacción y lectura durante secuencias de entrada.
- Inicializar una sola vez o hacer la inicialización idempotente; liberar listeners/observers cuando el ciclo de navegación lo requiera.
- Probar teclado, zoom, móvil, dispositivo lento y navegación hacia anclas.

## Presupuesto de movimiento

- Una firma principal reconocible, pocos motivos secundarios y estados coherentes.
- No animar simultáneamente todas las secciones.
- No añadir scroll hijacking, cursor personalizado o autoplay con sonido.
- No ocultar inicialmente bloques críticos mediante CSS si un fallo de script los dejaría invisibles.

## Librerías

Antes de incorporar una:

- Documentar efecto imposible o desproporcionado con CSS/WAAPI.
- Confirmar tamaño, licencia, mantenimiento, compatibilidad SSR y estrategia de carga.
- Importar solo lo usado y solo en la ruta/componente que lo necesita.
- Comparar bundle y trabajo del hilo principal antes/después.

## Verificación

- La experiencia reducida conserva significado y estados.
- No hay layout shift por dimensiones desconocidas.
- No hay observers/listeners duplicados después de navegación o reinicialización.
- El efecto sigue estable con resize y contenido de longitud distinta.
- Ejecutar [rendimiento](14-performance.md) y [validación](17-validation-and-release.md).

Si se usa navegación de Astro o una API sensible a versión, consultar la documentación oficial vigente antes de elegir eventos o persistencia.

