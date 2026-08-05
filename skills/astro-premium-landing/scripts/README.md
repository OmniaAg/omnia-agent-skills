# Utilidades de la skill

Los scripts usan argumentos separados, rutas resueltas y salidas dentro del proyecto. No instalan dependencias, no despliegan y no deben ejecutarse con privilegios elevados.

## `verify_project.py`

Auditor no destructivo para estructura Astro, arquitectura, contenido pendiente, SEO, accesibilidad heurística, assets/rutas, JavaScript/islas y posibles secretos.

### Requisitos

- Python 3.9 o posterior; biblioteca estándar.
- Para `--build`: Node y el paquete local `node_modules/astro` ya instalados.

### Uso

```text
python verify_project.py RUTA
python verify_project.py RUTA --strict
python verify_project.py RUTA --json
python verify_project.py RUTA --build --timeout 180
```

Opciones de umbral: `--max-file-bytes`, `--max-image-bytes` y `--max-component-lines`. `--help` es la referencia completa.

### Códigos

| Código | Significado |
|---:|---|
| 0 | Sin errores; advertencias permitidas fuera de estricto. |
| 1 | Advertencias en `--strict`, sin errores. |
| 2 | Uno o más errores de validación. |
| 3 | Uso o ruta inválidos. |
| 4 | Validación externa solicitada no disponible, fallida o expirada. |

`--build` invoca directamente el CLI local de Astro con `check` y `build`; no ejecuta scripts arbitrarios de `package.json`. Esos comandos pueden crear los artefactos normales `.astro/` y `dist/`. La salida capturada se limita y redacta. Los chequeos HTML/CSS son heurísticos y no sustituyen navegador, lector de pantalla, validador SEO ni medición de campo.

## `openverse_fetch.py`

Obtiene imágenes opcionales desde la API pública de Openverse, filtra licencias permitidas, valida HTTPS/MIME/firma/tamaño y escribe un ledger para revisión humana.

### Requisitos

- Python 3.9 o posterior; biblioteca estándar.
- Acceso de red autorizado.
- Un JSON dentro del proyecto con esta forma:

```json
[
  {
    "id": "hero-workspace",
    "query": "accessible creative workspace",
    "alt": "Equipo colaborando alrededor de una mesa"
  }
]
```

### Uso

```text
python openverse_fetch.py --project RUTA --queries media-queries.json --dry-run
python openverse_fetch.py --project RUTA --queries media-queries.json --target src/assets/openverse
python openverse_fetch.py --project RUTA --inline-query hero=workspace --json
```

No accede a red en `--dry-run`, no permite salida fuera del proyecto o mediante symlinks y no sobrescribe sin `--overwrite`. Licencias admitidas: `cc0`, `pdm`, `by`, `by-sa`. El ledger no sustituye revisar página de origen, licencia, atribución, privacidad, modelo release ni texto alternativo.

Códigos: `0` éxito, `1` resultado parcial, `3` uso inválido, `4` fallo completo de red/descarga.

## `normalize_assets.py`

Convierte y redimensiona imágenes locales conservando originales. Excluye animaciones para evitar pérdida silenciosa y puede emitir manifest.

### Requisitos

- Python 3.9 o posterior.
- Pillow ya instalado en el entorno. AVIF/HEIC dependen además del soporte disponible en esa instalación; el script no añade plugins.

### Uso

```text
python normalize_assets.py --project RUTA --src media --dry-run --recursive
python normalize_assets.py --project RUTA --src media --dst src/assets/optimized --format webp --recursive
python normalize_assets.py --project RUTA --src hero.png --format jpeg --max-width 1600 --manifest asset-manifest.json
```

No sobrescribe sin `--overwrite`, limita píxeles, corrige orientación EXIF y escribe de forma atómica. JPEG compone transparencia sobre blanco; revisar que esa decisión visual sea apropiada.

Códigos: `0` éxito, `1` conversión parcial, `3` uso inválido, `4` Pillow ausente.
