# Problemas críticos al trabajar con Astro

**Cargar cuando:** se analiza, migra, depura o audita un proyecto.

## Render y navegador

- El frontmatter se ejecuta durante renderizado, no en el navegador. `window`, `document`, storage y APIs DOM allí provocan fallos o supuestos incorrectos.
- Un `<script>` de cliente tiene otro ciclo de vida. No compartir estado implícito entre render y navegador.
- Si existe navegación de cliente, una inicialización basada solo en `DOMContentLoaded` puede no cubrir navegaciones posteriores; consultar eventos oficiales vigentes.

## Componentes e islas

- Un `.astro` no necesita hidratación para renderizar HTML. No añadir frameworks para “activar” contenido estático.
- `client:*` implica una decisión de hidratación para componentes de UI compatibles, no una optimización gratuita.
- `client:load` en cada componente transforma una landing ligera en múltiples cargas tempranas.
- Wrappers y componentes no reenvían automáticamente atributos/slots/semántica que no se hayan diseñado.

## Assets y rutas

- `src/assets/` requiere imports para el pipeline; no se referencia como URL pública `/src/assets/...`.
- `public/` se sirve sin procesamiento. No importarlo como si fuera un módulo del pipeline.
- Las rutas absolutas, `site` y `base` deben reflejar el destino; no arreglar subrutas con reemplazos globales de strings.
- Imports relativos heredados pueden romperse al mover HTML a componentes.

## Estilos y scripts

- El CSS local de Astro tiene alcance; estilos globales requieren intención explícita. No depender accidentalmente de que una sección alcance a otra.
- Atributos o directivas de un script pueden cambiar cómo Astro lo procesa; verificar la guía de la versión antes de asumir bundle/deduplicación.
- Scripts inline repetidos pueden inicializar varias veces o escapar al pipeline.

## Configuración y datos

- No asumir que `astro.config.mjs` siempre existe: son posibles extensiones compatibles, pero cualquier API debe validarse.
- No añadir adaptador a una salida estática solo por el proveedor.
- Variables públicas no son un almacén de secretos. Cualquier dato enviado al cliente es observable.
- Importar módulos exclusivos de servidor desde código hidratado puede romper build o filtrar arquitectura.
- Colecciones de contenido e integraciones cambian con versiones: consultar documentación, no copiar configuración antigua.

## Migración desde HTML

- No conservar un único `index.html` como arquitectura si Astro debe gestionar la ruta.
- No duplicar header/footer/metadatos ni pegar documentos completos en componentes.
- No inyectar secciones con `innerHTML` ni manipular globalmente el DOM para componer la página.
- No cargar todos los scripts y librerías en todas las rutas.

## Diagnóstico

Relacionar cada error con fase: configuración, render, bundle, cliente o despliegue. Ejecutar el verificador, type checking y build; después inspeccionar salida y consola. Revisar [migración](23-legacy-html-migration.md) para casos heredados.

