# Imágenes y assets

**Cargar cuando:** se añaden, descargan, convierten u optimizan imágenes, fuentes, iconos o archivos públicos.

## Decisión de ubicación

- `src/assets/`: recurso local importado que debe beneficiarse del pipeline, metadatos o componentes de imagen.
- `public/`: favicon, robots, archivos de descarga u otros recursos que deben conservar nombre y bytes sin procesamiento.
- Remoto: solo con origen, licencia, política de privacidad y configuración permitida confirmados.

No usar `/src/assets/...` en HTML. No importar `public/` desde código para forzar el pipeline.

## Pipeline obligatorio

1. Confirmar licencia, fuente, autor y atribución antes de descargar.
2. Nombrar por contenido/uso, no por `image1` o identificadores temporales.
3. Guardar originales solo si el proyecto lo requiere; conservar un registro de procedencia.
4. Recortar al encuadre real y producir dimensiones acordes al mayor render esperado.
5. Preferir formatos modernos compatibles; mantener SVG para vectores confiables y sanitizados.
6. Proporcionar `width` y `height` intrínsecos o usar el pipeline que los determine para evitar CLS.
7. Definir `alt` desde la función de la imagen: vacío solo para decoración redundante.
8. Cargar la imagen LCP con prioridad deliberada; lazy-load para contenido fuera del viewport.

## Astro

- Preferir componentes/imports oficiales de imagen para recursos procesados, después de validar API y opciones de la versión.
- Configurar orígenes o patrones remotos únicamente para hosts necesarios.
- No asumir que una imagen en `public/` será optimizada por Astro.
- Verificar el HTML generado, `srcset`, dimensiones, formato, URL con `base` y caché del proveedor.

## Herramientas de esta skill

- `scripts/normalize_assets.py`: conversión local no destructiva. Requiere Pillow disponible; no instala.
- `scripts/openverse_fetch.py`: obtención opcional con filtros de licencia y ledger; requiere red. Revisar licencia final manualmente.
- Ninguna herramienta sobrescribe sin `--overwrite`.

## Fuentes y otros recursos

- Autohospedar cuando licencia y presupuesto lo permitan; usar solo pesos/subconjuntos necesarios.
- No convertir automáticamente librerías de CDN en archivos locales sin revisar licencia, integridad y proceso de actualización.
- Tratar SVG externo como contenido potencialmente activo; no insertar markup no confiable.

## Verificación

- Imports y URLs existen; no quedan imágenes de prueba.
- Peso/dimensiones corresponden al uso y no desplazan layout.
- Alt, caption y atribución son correctos.
- Open Graph tiene URL absoluta y tamaño adecuado.

Fuente oficial: [imágenes en Astro](https://docs.astro.build/en/guides/images/).

