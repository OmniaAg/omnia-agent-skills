# Compatibilidad y troubleshooting en Windows

**Cargar cuando:** el desarrollo/CI usa Windows, hay rutas con espacios, políticas de PowerShell, diferencias de shell o binarios locales.

## Reglas obligatorias

- Usar `pathlib` en Python y APIs de rutas de Node; no concatenar `\\` o `/` manualmente.
- Pasar comandos como listas de argumentos y `shell=False` cuando sea posible.
- Citar rutas en comandos mostrados; una ruta puede contener espacios, caracteres Unicode o paréntesis.
- No asumir `bash`, `chmod`, symlinks, `/tmp`, utilidades GNU ni variables con sintaxis Unix.
- Usar el script del `package.json` y gestor detectado para invocar binarios locales; no depender de instalaciones globales.
- Tratar nombres de archivo sin sensibilidad a mayúsculas para detectar colisiones que fallarán en CI Linux.
- Preservar finales de línea/configuración del repositorio; no reescribir todo un archivo por CRLF/LF.

## PowerShell

- Comprobar versión y execution policy si un `.ps1` no inicia; no recomendar desactivar seguridad globalmente.
- Preferir `python`, `py -3` o el launcher disponible después de detectarlo.
- Evitar interpolar contenido no confiable en una cadena de comando.
- Para operaciones de archivos usar rutas literales y validar el destino resuelto antes de cualquier mutación.

## Node y gestores

- Si hay varios lockfiles, detener regeneración automática y decidir cuál es fuente de verdad.
- En Windows, binarios locales pueden terminar en `.cmd`; `scripts/verify_project.py --build` los localiza sin usar shell.
- Long paths, antivirus y archivos bloqueados pueden causar fallos intermitentes: registrar la ruta/error exactos; no reintentar con eliminación agresiva.
- OneDrive/carpetas sincronizadas pueden bloquear o cambiar timestamps; no asumir corrupción sin evidencia.

## Scripts de esta skill

- Los tres scripts Python usan biblioteca estándar para CLI/rutas; `normalize_assets.py` importa Pillow solo al ejecutarse.
- No se conservan wrappers `.sh`: duplicaban lógica y no ayudaban a Windows. La interfaz Python es la fuente única.
- Ningún script instala paquetes globales o construye comandos con `shell=True`.

## Diagnóstico

1. Capturar OS, shell, `python --version`, `node --version`, lockfile y comando exacto.
2. Resolver ruta absoluta y confirmar existencia/tipo.
3. Reproducir con el script local mínimo.
4. Comparar sensibilidad de mayúsculas, separadores, line endings y variables por nombre.
5. Si falla build, ejecutar comprobación estática antes de limpiar caches; no borrar sin autorización y objetivo validado.

