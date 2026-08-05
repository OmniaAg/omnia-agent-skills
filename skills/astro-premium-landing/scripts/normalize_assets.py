#!/usr/bin/env python3
"""Normaliza imágenes locales sin modificar originales.

Requiere Pillow ya instalado. No descarga ni instala dependencias. Las salidas y el
manifest opcional deben permanecer dentro del proyecto; no sobrescribe sin
--overwrite.
"""

from __future__ import annotations

import argparse
import json
import os
import tempfile
from pathlib import Path
from typing import Optional, Sequence


EXIT_OK = 0
EXIT_PARTIAL = 1
EXIT_USAGE = 3
EXIT_DEPENDENCY = 4
INPUT_EXTENSIONS = {".avif", ".bmp", ".heic", ".heif", ".jpeg", ".jpg", ".png", ".tif", ".tiff", ".webp"}
OUTPUT_EXTENSIONS = {"webp": ".webp", "avif": ".avif", "jpeg": ".jpg"}


class Exit3Parser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        self.print_usage()
        self.exit(EXIT_USAGE, f"{self.prog}: error: {message}\n")


def parser() -> argparse.ArgumentParser:
    result = Exit3Parser(description="Convierte y redimensiona imágenes de forma no destructiva.")
    result.add_argument("--project", required=True, help="Raíz del proyecto Astro.")
    result.add_argument("--src", required=True, help="Archivo o directorio de entrada dentro del proyecto.")
    result.add_argument("--dst", default="src/assets/optimized", help="Directorio de salida dentro del proyecto.")
    result.add_argument("--format", choices=sorted(OUTPUT_EXTENSIONS), default="webp", help="Formato de salida.")
    result.add_argument("--quality", type=int, default=82, help="Calidad 1-100; predeterminado: 82.")
    result.add_argument("--max-width", type=int, default=2400, help="Ancho máximo; predeterminado: 2400 px.")
    result.add_argument("--max-pixels", type=int, default=40_000_000, help="Límite de píxeles de entrada; predeterminado: 40000000.")
    result.add_argument("--recursive", action="store_true", help="Recorre subdirectorios del origen.")
    result.add_argument("--overwrite", action="store_true", help="Permite reemplazar salidas existentes.")
    result.add_argument("--dry-run", action="store_true", help="Muestra el plan sin crear directorios ni archivos.")
    result.add_argument("--manifest", help="JSON opcional de resultados, relativo al proyecto.")
    result.add_argument("--json", dest="json_output", action="store_true", help="Emite salida JSON.")
    return result


def within(path: Path, root: Path) -> bool:
    try:
        path.resolve(strict=False).relative_to(root.resolve(strict=True))
        return True
    except (OSError, ValueError):
        return False


def project_path(root: Path, value: str, must_exist: bool = False) -> Path:
    raw = Path(value).expanduser()
    candidate = raw.resolve(strict=False) if raw.is_absolute() else (root / raw).resolve(strict=False)
    if not within(candidate, root):
        raise ValueError(f"la ruta sale del proyecto: {value}")
    cursor = root
    for part in candidate.relative_to(root).parts:
        cursor = cursor / part
        if cursor.exists() and cursor.is_symlink():
            raise ValueError(f"no se permiten enlaces simbólicos en la ruta: {value}")
    if must_exist and not candidate.exists():
        raise ValueError(f"la ruta no existe: {value}")
    return candidate


def input_files(source: Path, recursive: bool) -> list[Path]:
    if source.is_file():
        return [source] if source.suffix.lower() in INPUT_EXTENSIONS else []
    iterator = source.rglob("*") if recursive else source.glob("*")
    return sorted(path for path in iterator if path.is_file() and not path.is_symlink() and path.suffix.lower() in INPUT_EXTENSIONS)


def atomic_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=".asset-manifest-", suffix=".json", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
            json.dump(payload, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = parser().parse_args(argv)
    if not 1 <= args.quality <= 100 or args.max_width < 1 or args.max_pixels < 1:
        parser().error("quality debe ser 1-100 y los límites deben ser positivos")
    root = Path(args.project).expanduser().resolve(strict=False)
    if not root.is_dir():
        print(f"ERROR: el proyecto no existe o no es directorio: {root}")
        return EXIT_USAGE
    try:
        source = project_path(root, args.src, must_exist=True)
        destination_root = project_path(root, args.dst)
        manifest_path = project_path(root, args.manifest) if args.manifest else None
    except ValueError as exc:
        print(f"ERROR: {exc}")
        return EXIT_USAGE
    if not source.is_file() and not source.is_dir():
        print("ERROR: --src debe ser archivo o directorio.")
        return EXIT_USAGE

    files = input_files(source, args.recursive)
    if not files:
        print("ERROR: no se encontraron imágenes compatibles.")
        return EXIT_USAGE
    source_base = source.parent if source.is_file() else source
    extension = OUTPUT_EXTENSIONS[args.format]

    planned = []
    for image_path in files:
        relative_parent = image_path.parent.relative_to(source_base) if source_base in image_path.parents or image_path.parent == source_base else Path()
        output_path = destination_root / relative_parent / f"{image_path.stem}{extension}"
        planned.append({"source": image_path.relative_to(root).as_posix(), "output": output_path.relative_to(root).as_posix()})
    if args.dry_run:
        payload = {"dry_run": True, "format": args.format, "files": planned, "files_written": False}
        print(json.dumps(payload, ensure_ascii=False, indent=2) if args.json_output else "\n".join(f"DRY RUN: {item['source']} -> {item['output']}" for item in planned))
        return EXIT_OK

    try:
        from PIL import Image, ImageOps, UnidentifiedImageError
    except ImportError:
        print("ERROR: Pillow no está disponible. Instálalo solo si el usuario autoriza esa dependencia.")
        return EXIT_DEPENDENCY

    Image.MAX_IMAGE_PIXELS = args.max_pixels
    converted: list[dict] = []
    failures: list[dict] = []
    for item, image_path in zip(planned, files):
        output_path = root / item["output"]
        temporary_path: Optional[Path] = None
        try:
            if output_path.exists() and not args.overwrite:
                raise FileExistsError("la salida ya existe; usa --overwrite")
            output_path.parent.mkdir(parents=True, exist_ok=True)
            if output_path.parent.is_symlink():
                raise RuntimeError("el destino es un enlace simbólico")
            with Image.open(image_path) as opened:
                if getattr(opened, "is_animated", False):
                    raise RuntimeError("imagen animada no admitida; convertirla requiere una decisión explícita")
                width, height = opened.size
                if width * height > args.max_pixels:
                    raise RuntimeError(f"excede el límite de {args.max_pixels} píxeles")
                image = ImageOps.exif_transpose(opened)
                if image.width > args.max_width:
                    new_height = max(1, round(image.height * args.max_width / image.width))
                    image = image.resize((args.max_width, new_height), Image.Resampling.LANCZOS)
                if args.format == "jpeg":
                    if image.mode in {"RGBA", "LA"} or (image.mode == "P" and "transparency" in image.info):
                        rgba = image.convert("RGBA")
                        background = Image.new("RGB", rgba.size, "white")
                        background.paste(rgba, mask=rgba.getchannel("A"))
                        image = background
                    else:
                        image = image.convert("RGB")
                elif image.mode not in {"RGB", "RGBA"}:
                    image = image.convert("RGBA" if "transparency" in image.info else "RGB")

                fd, temporary = tempfile.mkstemp(prefix=".asset-", suffix=extension, dir=output_path.parent)
                os.close(fd)
                temporary_path = Path(temporary)
                save_format = {"webp": "WEBP", "avif": "AVIF", "jpeg": "JPEG"}[args.format]
                save_options = {"format": save_format, "quality": args.quality}
                if args.format in {"webp", "jpeg"}:
                    save_options["optimize"] = True
                image.save(temporary_path, **save_options)
            os.replace(temporary_path, output_path)
            temporary_path = None
            converted.append(
                {
                    **item,
                    "input_bytes": image_path.stat().st_size,
                    "output_bytes": output_path.stat().st_size,
                    "width": image.width,
                    "height": image.height,
                    "format": args.format,
                }
            )
        except (OSError, RuntimeError, ValueError, UnidentifiedImageError, Image.DecompressionBombError) as exc:
            failures.append({"source": item["source"], "error": str(exc)})
        finally:
            if temporary_path is not None and temporary_path.exists():
                temporary_path.unlink()

    payload = {"converted": converted, "failures": failures}
    if manifest_path:
        try:
            atomic_json(manifest_path, payload)
        except OSError as exc:
            failures.append({"source": "manifest", "error": str(exc)})
    if args.json_output:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        for item in converted:
            print(f"OK: {item['source']} -> {item['output']} ({item['output_bytes']} bytes)")
        for item in failures:
            print(f"ERROR: {item['source']}: {item['error']}")
    return EXIT_PARTIAL if failures else EXIT_OK


if __name__ == "__main__":
    raise SystemExit(main())

