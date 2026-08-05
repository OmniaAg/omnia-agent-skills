#!/usr/bin/env python3
"""Auditor estático y verificador opcional para landing pages con Astro.

Uso:
    python verify_project.py RUTA
    python verify_project.py RUTA --strict
    python verify_project.py RUTA --json
    python verify_project.py RUTA --build

El modo normal no modifica el proyecto. --build ejecuta el CLI local instalado de
Astro (`check` y `build`), que puede crear artefactos normales como `.astro/` y
`dist/`. Nunca instala dependencias ni ejecuta scripts arbitrarios de package.json.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable, Optional, Sequence
from urllib.parse import unquote, urlsplit


EXIT_OK = 0
EXIT_STRICT_WARNINGS = 1
EXIT_VALIDATION_ERRORS = 2
EXIT_USAGE = 3
EXIT_EXTERNAL_FAILURE = 4

SEVERITY_ORDER = {"ERROR": 0, "WARNING": 1, "INFO": 2}
CONFIG_NAMES = (
    "astro.config.mjs",
    "astro.config.js",
    "astro.config.ts",
    "astro.config.cjs",
)
PAGE_EXTENSIONS = {".astro", ".md", ".mdx", ".html"}
COMPONENT_EXTENSIONS = {".astro", ".tsx", ".jsx", ".vue", ".svelte"}
TEXT_EXTENSIONS = {
    ".astro",
    ".css",
    ".html",
    ".js",
    ".jsx",
    ".json",
    ".md",
    ".mdx",
    ".mjs",
    ".cjs",
    ".scss",
    ".svelte",
    ".ts",
    ".tsx",
    ".txt",
    ".vue",
    ".yaml",
    ".yml",
}
IMAGE_EXTENSIONS = {
    ".avif",
    ".bmp",
    ".gif",
    ".heic",
    ".heif",
    ".jpeg",
    ".jpg",
    ".png",
    ".svg",
    ".tif",
    ".tiff",
    ".webp",
}
ASSET_EXTENSIONS = IMAGE_EXTENSIONS | {
    ".css",
    ".eot",
    ".ico",
    ".js",
    ".json",
    ".mp3",
    ".mp4",
    ".ogg",
    ".pdf",
    ".ttf",
    ".wav",
    ".webm",
    ".woff",
    ".woff2",
}
SKIP_DIRECTORIES = {
    ".astro",
    ".git",
    ".hg",
    ".svn",
    ".vercel",
    ".netlify",
    "coverage",
    "dist",
    "node_modules",
}
FRAMEWORKS = {
    "react": ({"react", "react-dom", "@astrojs/react"}, {".jsx", ".tsx"}),
    "vue": ({"vue", "@astrojs/vue"}, {".vue"}),
    "svelte": ({"svelte", "@astrojs/svelte"}, {".svelte"}),
    "preact": ({"preact", "@astrojs/preact"}, {".jsx", ".tsx"}),
    "solid": ({"solid-js", "@astrojs/solid-js"}, {".jsx", ".tsx"}),
}


class Exit3ArgumentParser(argparse.ArgumentParser):
    """Argparse con código 3 para errores de uso, según el contrato del script."""

    def error(self, message: str) -> None:
        self.print_usage(sys.stderr)
        self.exit(EXIT_USAGE, f"{self.prog}: error: {message}\n")


@dataclass(frozen=True)
class Finding:
    severity: str
    code: str
    message: str
    path: Optional[str] = None
    line: Optional[int] = None


def build_parser() -> argparse.ArgumentParser:
    parser = Exit3ArgumentParser(
        description=(
            "Audita de forma no destructiva la estructura, contenido, SEO, "
            "accesibilidad, assets, islas y seguridad básica de un proyecto Astro."
        )
    )
    parser.add_argument("project", help="Ruta al proyecto Astro que se auditará.")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Devuelve 1 si hay advertencias y no hay errores.",
    )
    parser.add_argument(
        "--json",
        dest="json_output",
        action="store_true",
        help="Emite un único documento JSON, apto para automatización.",
    )
    parser.add_argument(
        "--build",
        action="store_true",
        help=(
            "Ejecuta `astro check` y `astro build` con el CLI local ya instalado. "
            "No instala dependencias."
        ),
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=120,
        metavar="SEGUNDOS",
        help="Timeout por comando externo; predeterminado: 120.",
    )
    parser.add_argument(
        "--max-file-bytes",
        type=int,
        default=750_000,
        metavar="BYTES",
        help="Umbral de advertencia para archivos de texto; predeterminado: 750000.",
    )
    parser.add_argument(
        "--max-image-bytes",
        type=int,
        default=1_500_000,
        metavar="BYTES",
        help="Umbral de advertencia para imágenes; predeterminado: 1500000.",
    )
    parser.add_argument(
        "--max-component-lines",
        type=int,
        default=500,
        metavar="LINEAS",
        help="Umbral heurístico de componente monolítico; predeterminado: 500.",
    )
    parser.add_argument("--version", action="version", version="%(prog)s 1.0.0")
    return parser


def is_within(path: Path, parent: Path) -> bool:
    try:
        path.resolve(strict=False).relative_to(parent.resolve(strict=False))
        return True
    except ValueError:
        return False


def relative_label(path: Path, root: Path) -> str:
    try:
        return path.resolve(strict=False).relative_to(root).as_posix()
    except ValueError:
        return str(path)


def line_number(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def strip_markup(value: str) -> str:
    value = re.sub(r"<[^>]+>", "", value)
    return re.sub(r"\s+", " ", value).strip()


def redact_output(value: str) -> str:
    patterns = (
        r"AKIA[0-9A-Z]{16}",
        r"gh[pousr]_[A-Za-z0-9]{20,}",
        r"(?:sk|pk)_(?:live|test)_[A-Za-z0-9_-]{12,}",
        r"sk-[A-Za-z0-9_-]{16,}",
        r"(?i)(authorization\s*:\s*(?:bearer|basic)\s+)[^\s]+",
    )
    redacted = value
    for pattern in patterns:
        redacted = re.sub(pattern, "[REDACTED]", redacted)
    return redacted[-6000:]


class Auditor:
    def __init__(self, root: Path, args: argparse.Namespace) -> None:
        self.root = root
        self.args = args
        self.findings: list[Finding] = []
        self.texts: dict[Path, str] = {}
        self.package: dict = {}
        self.dependencies: set[str] = set()
        self.pages: list[Path] = []
        self.config_path: Optional[Path] = None
        self.package_manager: Optional[str] = None
        self.external_failed = False

    def add(
        self,
        severity: str,
        code: str,
        message: str,
        path: Optional[Path] = None,
        line: Optional[int] = None,
    ) -> None:
        self.findings.append(
            Finding(
                severity=severity,
                code=code,
                message=message,
                path=relative_label(path, self.root) if path else None,
                line=line,
            )
        )

    def iter_files(self) -> Iterable[Path]:
        for path in self.root.rglob("*"):
            if not path.is_file():
                continue
            try:
                relative_parts = path.relative_to(self.root).parts
            except ValueError:
                continue
            if any(part in SKIP_DIRECTORIES for part in relative_parts[:-1]):
                continue
            yield path

    def read_text(self, path: Path) -> Optional[str]:
        if path in self.texts:
            return self.texts[path]
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            self.add("WARNING", "TEXT_ENCODING", "No se pudo leer como UTF-8.", path)
            return None
        except OSError as exc:
            self.add("ERROR", "FILE_READ", f"No se pudo leer el archivo: {exc}", path)
            return None
        self.texts[path] = text
        return text

    def run(self) -> None:
        self.check_project()
        self.collect_text_files()
        self.check_architecture()
        self.check_pending_content()
        self.check_duplicates()
        self.check_seo()
        self.check_accessibility()
        self.check_assets_and_routes()
        self.check_client_code()
        self.check_security()
        if self.args.build:
            self.run_external_checks()

    def check_project(self) -> None:
        package_path = self.root / "package.json"
        if not package_path.is_file():
            self.add("ERROR", "PROJECT_PACKAGE_MISSING", "Falta package.json.", package_path)
        else:
            try:
                self.package = json.loads(package_path.read_text(encoding="utf-8"))
            except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
                self.add("ERROR", "PROJECT_PACKAGE_INVALID", f"package.json no es válido: {exc}", package_path)
                self.package = {}

        for section in ("dependencies", "devDependencies", "peerDependencies"):
            values = self.package.get(section, {})
            if isinstance(values, dict):
                self.dependencies.update(str(key) for key in values)
        if "astro" not in self.dependencies:
            self.add("ERROR", "PROJECT_ASTRO_MISSING", "Astro no aparece en las dependencias declaradas.", package_path)
        else:
            self.add("INFO", "PROJECT_ASTRO_FOUND", "Se detectó Astro en las dependencias.", package_path)

        configs = [self.root / name for name in CONFIG_NAMES if (self.root / name).is_file()]
        if not configs:
            self.add("WARNING", "PROJECT_CONFIG_MISSING", "No se encontró astro.config.*; puede ser válido, pero debe confirmarse.")
        elif len(configs) > 1:
            self.add("ERROR", "PROJECT_CONFIG_MULTIPLE", "Existen varios archivos astro.config.*.")
            self.config_path = configs[0]
        else:
            self.config_path = configs[0]

        pages_dir = self.root / "src" / "pages"
        if not pages_dir.is_dir():
            self.add("ERROR", "PROJECT_PAGES_DIR_MISSING", "Falta src/pages/.", pages_dir)
        else:
            self.pages = [
                path
                for path in pages_dir.rglob("*")
                if path.is_file() and path.suffix.lower() in PAGE_EXTENSIONS
            ]
            if not self.pages:
                self.add("ERROR", "PROJECT_PAGE_MISSING", "No se encontró ninguna página renderizable.", pages_dir)
            else:
                self.add("INFO", "PROJECT_PAGES_FOUND", f"Se detectaron {len(self.pages)} página(s).", pages_dir)

        lockfile_managers = {
            "package-lock.json": "npm",
            "pnpm-lock.yaml": "pnpm",
            "yarn.lock": "yarn",
            "bun.lock": "bun",
            "bun.lockb": "bun",
        }
        lockfiles = [name for name in lockfile_managers if (self.root / name).is_file()]
        if len(lockfiles) > 1:
            self.add("WARNING", "PROJECT_MULTIPLE_LOCKFILES", f"Hay varios lockfiles: {', '.join(lockfiles)}.")
            self.package_manager = "ambiguous"
        elif not lockfiles:
            self.add("WARNING", "PROJECT_LOCKFILE_MISSING", "No se encontró lockfile.")
        else:
            self.package_manager = lockfile_managers[lockfiles[0]]
            self.add("INFO", "PROJECT_LOCKFILE", f"Lockfile detectado: {lockfiles[0]}.")
        declared_manager = self.package.get("packageManager")
        if isinstance(declared_manager, str) and declared_manager:
            manager_name = declared_manager.split("@", 1)[0]
            if self.package_manager is None:
                self.package_manager = manager_name
            elif self.package_manager not in {"ambiguous", manager_name}:
                self.add("WARNING", "PROJECT_MANAGER_CONFLICT", "packageManager no coincide con el lockfile detectado.", package_path)

    def collect_text_files(self) -> None:
        for path in self.iter_files():
            try:
                size = path.stat().st_size
            except OSError as exc:
                self.add("ERROR", "FILE_STAT", f"No se pudo inspeccionar: {exc}", path)
                continue
            if path.suffix.lower() in TEXT_EXTENSIONS:
                if size > self.args.max_file_bytes:
                    self.add(
                        "WARNING",
                        "ARCH_FILE_LARGE",
                        f"Archivo de texto grande ({size} bytes; umbral {self.args.max_file_bytes}).",
                        path,
                    )
                if size <= max(self.args.max_file_bytes * 4, 3_000_000):
                    self.read_text(path)

    def check_architecture(self) -> None:
        src = self.root / "src"
        if not src.is_dir():
            self.add("ERROR", "ARCH_SRC_MISSING", "Falta src/.", src)
            return
        directories = {
            "layouts": "Los layouts reutilizables no están presentes; confirmar si la landing necesita un layout principal.",
            "components": "No existe src/components/; una página mínima puede ser válida, pero revisar modularidad.",
            "styles": "No existe src/styles/; puede ser válido si todo el CSS compartido vive deliberadamente en componentes.",
            "assets": "No existe src/assets/; puede ser válido si no hay recursos procesados.",
        }
        for name, message in directories.items():
            path = src / name
            if not path.is_dir():
                severity = "WARNING" if name in {"layouts", "components"} else "INFO"
                self.add(severity, f"ARCH_{name.upper()}_MISSING", message, path)
        if not (self.root / "public").is_dir():
            self.add("INFO", "ARCH_PUBLIC_MISSING", "No existe public/; puede ser válido si no hay archivos sin procesar.")

        by_casefold: dict[str, list[Path]] = {}
        for path, text in self.texts.items():
            if path.suffix.lower() not in COMPONENT_EXTENSIONS:
                continue
            lines = text.count("\n") + 1
            if lines > self.args.max_component_lines:
                self.add(
                    "WARNING",
                    "ARCH_COMPONENT_MONOLITHIC",
                    f"Componente de {lines} líneas; revisar responsabilidades (umbral {self.args.max_component_lines}).",
                    path,
                )
            by_casefold.setdefault(path.name.casefold(), []).append(path)
        for name, paths in by_casefold.items():
            if len(paths) > 1:
                labels = ", ".join(relative_label(path, self.root) for path in paths)
                self.add("WARNING", "ARCH_CASE_COLLISION", f"Nombres que colisionan por mayúsculas/minúsculas ({name}): {labels}.")

    def check_pending_content(self) -> None:
        patterns = {
            "PENDING_TODO": r"\bTODO\b",
            "PENDING_FIXME": r"\bFIXME\b",
            "PENDING_SPANISH": r"\bPENDIENTE\b",
            "PENDING_LOREM": r"\bLOREM(?:\s+IPSUM)?\b",
            "PENDING_PLACEHOLDER": r"\bPLACEHOLDER\b",
            "PENDING_EXAMPLE_URL": r"https?://(?:www\.)?example\.(?:com|org|net)\b",
            "PENDING_DEMO_TEXT": r"\b(?:demo content|sample text|texto de prueba|contenido de prueba)\b",
        }
        for path, text in self.texts.items():
            for code, pattern in patterns.items():
                for match in re.finditer(pattern, text, flags=re.IGNORECASE):
                    self.add(
                        "WARNING",
                        code,
                        "Se detectó contenido pendiente o de demostración.",
                        path,
                        line_number(text, match.start()),
                    )

    def check_duplicates(self) -> None:
        hashes: dict[str, list[Path]] = {}
        for path, text in self.texts.items():
            if path.suffix.lower() not in COMPONENT_EXTENSIONS | {".css"}:
                continue
            normalized = re.sub(r"\s+", " ", text).strip()
            if len(normalized) < 200:
                continue
            digest = hashlib.sha256(normalized.encode("utf-8")).hexdigest()
            hashes.setdefault(digest, []).append(path)
        for paths in hashes.values():
            if len(paths) > 1:
                labels = ", ".join(relative_label(path, self.root) for path in paths)
                self.add("WARNING", "ARCH_DUPLICATE_FILE", f"Contenido sustancialmente idéntico: {labels}.")

    def check_seo(self) -> None:
        astro_texts = [text for path, text in self.texts.items() if path.suffix.lower() in {".astro", ".html"}]
        combined = "\n".join(astro_texts)
        if not re.search(r"<title\b", combined, re.IGNORECASE):
            self.add("ERROR", "SEO_TITLE_MISSING", "No se detectó ningún <title> en páginas/layouts.")
        if not re.search(r"<meta\b[^>]*\bname\s*=\s*['\"]description['\"]", combined, re.IGNORECASE):
            self.add("WARNING", "SEO_DESCRIPTION_MISSING", "No se detectó meta description.")
        if not re.search(r"<html\b[^>]*\blang\s*=", combined, re.IGNORECASE):
            self.add("ERROR", "SEO_LANG_MISSING", "No se detectó atributo lang en <html>.")
        if not re.search(r"<link\b[^>]*\brel\s*=\s*['\"][^'\"]*canonical", combined, re.IGNORECASE):
            config_text = self.read_text(self.config_path) if self.config_path else ""
            severity = "WARNING" if config_text and re.search(r"\bsite\s*:", config_text) else "INFO"
            self.add(severity, "SEO_CANONICAL_MISSING", "No se detectó canonical; confirmar si corresponde.")
        og_required = ("og:title", "og:description", "og:image")
        missing_og = [value for value in og_required if value.lower() not in combined.lower()]
        if missing_og:
            self.add("WARNING", "SEO_OG_INCOMPLETE", f"Open Graph incompleto; faltan: {', '.join(missing_og)}.")
        public_dir = self.root / "public"
        favicon_files = list(public_dir.glob("favicon.*")) if public_dir.is_dir() else []
        if not favicon_files and not re.search(r"<link\b[^>]*\brel\s*=\s*['\"][^'\"]*icon", combined, re.IGNORECASE):
            self.add("WARNING", "SEO_FAVICON_MISSING", "No se detectó favicon.")
        if not (public_dir / "robots.txt").is_file():
            self.add("INFO", "SEO_ROBOTS_MISSING", "No existe public/robots.txt; confirmar estrategia de indexación.")
        sitemap_present = "@astrojs/sitemap" in self.dependencies or (public_dir / "sitemap.xml").is_file()
        config_text = self.read_text(self.config_path) if self.config_path else ""
        if not sitemap_present and (len(self.pages) > 1 or (config_text and re.search(r"\bsite\s*:", config_text))):
            self.add("WARNING", "SEO_SITEMAP_MISSING", "No se detectó sitemap en un sitio que podría requerirlo.")

    def check_accessibility(self) -> None:
        all_style_text = "\n".join(
            text for path, text in self.texts.items() if path.suffix.lower() in {".astro", ".css", ".scss"}
        )
        has_motion = bool(re.search(r"@keyframes|\banimation\s*:|requestAnimationFrame|\bgsap\b|scroll-timeline", all_style_text, re.IGNORECASE))
        if has_motion and "prefers-reduced-motion" not in all_style_text:
            self.add("WARNING", "A11Y_REDUCED_MOTION_MISSING", "Hay animación, pero no se detectó prefers-reduced-motion.")

        total_h1 = 0
        for path, text in self.texts.items():
            if path.suffix.lower() not in {".astro", ".html", ".md", ".mdx"}:
                continue
            for match in re.finditer(r"<(?:img|Image|Picture)\b[^>]*>", text, re.IGNORECASE):
                if not re.search(r"\balt\s*=", match.group(0), re.IGNORECASE):
                    self.add("WARNING", "A11Y_IMAGE_ALT_MISSING", "Imagen sin atributo alt detectable.", path, line_number(text, match.start()))
            labels_for = {value for value in re.findall(r"<label\b[^>]*\bfor\s*=\s*['\"]([^'\"]+)['\"]", text, re.IGNORECASE)}
            for match in re.finditer(r"<input\b[^>]*>", text, re.IGNORECASE):
                tag = match.group(0)
                input_type = re.search(r"\btype\s*=\s*['\"]([^'\"]+)['\"]", tag, re.IGNORECASE)
                if input_type and input_type.group(1).lower() in {"hidden", "submit", "button", "reset", "image"}:
                    continue
                input_id = re.search(r"\bid\s*=\s*['\"]([^'\"]+)['\"]", tag, re.IGNORECASE)
                named = bool(re.search(r"\baria-(?:label|labelledby)\s*=", tag, re.IGNORECASE))
                if not named and (not input_id or input_id.group(1) not in labels_for):
                    self.add("WARNING", "A11Y_INPUT_LABEL_MISSING", "Input sin label asociado detectable.", path, line_number(text, match.start()))
            for match in re.finditer(r"<button\b([^>]*)>(.*?)</button\s*>", text, re.IGNORECASE | re.DOTALL):
                attrs, body = match.groups()
                if not strip_markup(body) and not re.search(r"\baria-(?:label|labelledby)\s*=|\btitle\s*=", attrs, re.IGNORECASE):
                    self.add("WARNING", "A11Y_BUTTON_NAME_MISSING", "Botón sin contenido o nombre accesible detectable.", path, line_number(text, match.start()))
            for match in re.finditer(r"<a\b([^>]*)>(.*?)</a\s*>", text, re.IGNORECASE | re.DOTALL):
                attrs, body = match.groups()
                if not strip_markup(body) and not re.search(r"\baria-(?:label|labelledby)\s*=|\btitle\s*=", attrs, re.IGNORECASE):
                    self.add("WARNING", "A11Y_LINK_NAME_MISSING", "Enlace vacío o sin nombre accesible detectable.", path, line_number(text, match.start()))
            headings = [int(value) for value in re.findall(r"<h([1-6])\b", text, re.IGNORECASE)]
            total_h1 += headings.count(1)
            for before, after in zip(headings, headings[1:]):
                if after > before + 1:
                    self.add("WARNING", "A11Y_HEADING_JUMP", f"Salto de encabezado h{before} a h{after}.", path)
        if total_h1 == 0:
            self.add("WARNING", "A11Y_H1_MISSING", "No se detectó ningún h1 en el contenido analizado.")
        elif total_h1 > len(self.pages) and self.pages:
            self.add("INFO", "A11Y_H1_REVIEW", f"Se detectaron {total_h1} h1 para {len(self.pages)} página(s); revisar composición por ruta.")

        self.check_simple_contrast(all_style_text)

    def check_simple_contrast(self, css: str) -> None:
        for rule in re.finditer(r"[^{}]+\{([^{}]+)\}", css, re.DOTALL):
            declarations = rule.group(1)
            foreground = re.search(r"(?<!-)\bcolor\s*:\s*(#[0-9a-fA-F]{3,6})\b", declarations)
            background = re.search(r"\bbackground(?:-color)?\s*:\s*(#[0-9a-fA-F]{3,6})\b", declarations)
            if not foreground or not background:
                continue
            ratio = contrast_ratio(foreground.group(1), background.group(1))
            if ratio is not None and ratio < 4.5:
                self.add("WARNING", "A11Y_CONTRAST_SIMPLE", f"Par explícito con contraste aproximado {ratio:.2f}:1; revisar contexto/tamaño.")

    def check_assets_and_routes(self) -> None:
        public_dir = (self.root / "public").resolve(strict=False)
        src_assets = (self.root / "src" / "assets").resolve(strict=False)
        routes = self.route_set()
        import_pattern = re.compile(r"(?:\bfrom\s*|\bimport\s*\(\s*|\bimport\s*)['\"]([^'\"]+)['\"]")

        for path, text in self.texts.items():
            for match in import_pattern.finditer(text):
                specifier = match.group(1).split("?", 1)[0]
                if not specifier.startswith("."):
                    continue
                candidate = (path.parent / specifier).resolve(strict=False)
                resolved = resolve_import(candidate)
                if resolved is None:
                    self.add("ERROR", "ASSET_IMPORT_BROKEN", f"Import local no resuelto: {specifier}.", path, line_number(text, match.start()))
                elif is_within(resolved, public_dir):
                    self.add("WARNING", "ASSET_PUBLIC_IMPORTED", "Se importa un archivo de public/; referirlo por URL o moverlo al pipeline.", path, line_number(text, match.start()))

            for match in re.finditer(r"\b(?:src|href|poster)\s*=\s*['\"]([^'\"{}]+)['\"]", text, re.IGNORECASE):
                value = match.group(1).strip()
                self.check_url_reference(path, text, match.start(), value, public_dir, routes)
            for match in re.finditer(r"url\(\s*['\"]?([^'\"){}]+)", text, re.IGNORECASE):
                value = match.group(1).strip()
                self.check_url_reference(path, text, match.start(), value, public_dir, routes)

            if re.search(r"(?:['\"]|url\()[^'\")]*?/src/assets/", text, re.IGNORECASE):
                self.add("ERROR", "ASSET_SRC_AS_PUBLIC", "Se referencia /src/assets/ como URL pública; debe importarse.", path)

        for path in self.iter_files():
            suffix = path.suffix.lower()
            if suffix not in IMAGE_EXTENSIONS:
                continue
            try:
                size = path.stat().st_size
            except OSError:
                continue
            if size > self.args.max_image_bytes:
                self.add("WARNING", "ASSET_IMAGE_LARGE", f"Imagen grande ({size} bytes; umbral {self.args.max_image_bytes}).", path)
            if suffix in {".bmp", ".tif", ".tiff", ".heic", ".heif"}:
                self.add("WARNING", "ASSET_FORMAT_REVIEW", f"Formato de imagen poco apto para entrega web ({suffix}).", path)

    def check_url_reference(
        self,
        source: Path,
        text: str,
        offset: int,
        value: str,
        public_dir: Path,
        routes: set[str],
    ) -> None:
        if not value or value.startswith(("#", "data:", "mailto:", "tel:", "javascript:")):
            return
        split = urlsplit(value)
        if split.scheme or split.netloc:
            return
        path_part = unquote(split.path)
        if "/src/assets/" in path_part.replace("\\", "/"):
            self.add("ERROR", "ASSET_SRC_AS_PUBLIC", "URL pública apunta a src/assets/.", source, line_number(text, offset))
            return
        if not path_part.startswith("/"):
            return
        suffix = Path(path_part).suffix.lower()
        if suffix in ASSET_EXTENSIONS:
            target = (public_dir / path_part.lstrip("/")).resolve(strict=False)
            if not is_within(target, public_dir) or not target.is_file():
                self.add("ERROR", "ASSET_PUBLIC_BROKEN", f"Recurso público inexistente: {path_part}.", source, line_number(text, offset))
        elif path_part not in routes and path_part.rstrip("/") not in {route.rstrip("/") for route in routes}:
            self.add("WARNING", "ROUTE_INTERNAL_UNKNOWN", f"Enlace interno no resuelto heurísticamente: {path_part}.", source, line_number(text, offset))

    def route_set(self) -> set[str]:
        routes: set[str] = set()
        pages_dir = self.root / "src" / "pages"
        for page in self.pages:
            relative = page.relative_to(pages_dir).with_suffix("")
            if any("[" in part for part in relative.parts):
                continue
            parts = list(relative.parts)
            if parts and parts[-1] == "index":
                parts.pop()
            route = "/" + "/".join(parts)
            routes.add(route or "/")
            routes.add((route.rstrip("/") + "/") if route != "/" else "/")
        return routes

    def check_client_code(self) -> None:
        directive_counts: dict[str, int] = {}
        framework_files = {path.suffix.lower() for path in self.texts}
        for path, text in self.texts.items():
            if path.suffix.lower() == ".astro":
                frontmatter = extract_frontmatter(text)
                match = re.search(r"\b(?:window|document)\b", frontmatter)
                if match:
                    self.add("ERROR", "CLIENT_DOM_IN_FRONTMATTER", "Uso de window/document en frontmatter (entorno de render).", path, line_number(text, match.start()))
                for match in re.finditer(r"\bclient:(load|idle|visible|media|only)\b", text):
                    directive = match.group(1)
                    directive_counts[directive] = directive_counts.get(directive, 0) + 1
                for match in re.finditer(r"<script\b[^>]*\bis:inline\b", text, re.IGNORECASE):
                    self.add("WARNING", "CLIENT_INLINE_SCRIPT", "Script inline: confirmar necesidad, alcance e inicialización.", path, line_number(text, match.start()))
                for script in extract_browser_scripts(text):
                    for match in re.finditer(r"import\.meta\.env\.([A-Z][A-Z0-9_]*)", script):
                        if not match.group(1).startswith("PUBLIC_"):
                            self.add("ERROR", "SEC_PRIVATE_ENV_CLIENT", "Variable privada referenciada desde script del navegador; nombre oculto.", path)
            elif path.suffix.lower() in {".jsx", ".tsx", ".vue", ".svelte"}:
                for match in re.finditer(r"import\.meta\.env\.([A-Z][A-Z0-9_]*)", text):
                    if not match.group(1).startswith("PUBLIC_"):
                        self.add("WARNING", "SEC_PRIVATE_ENV_FRAMEWORK", "Variable no pública en componente de framework; confirmar que nunca se hidrata.", path, line_number(text, match.start()))

        total_directives = sum(directive_counts.values())
        if total_directives:
            summary = ", ".join(f"client:{key}={value}" for key, value in sorted(directive_counts.items()))
            self.add("INFO", "CLIENT_ISLANDS_FOUND", f"Directivas de hidratación: {summary}.")
        if directive_counts.get("load", 0):
            severity = "WARNING"
            self.add(severity, "CLIENT_LOAD_REVIEW", f"Se detectaron {directive_counts['load']} uso(s) de client:load; justificar criticidad.")
        if directive_counts.get("only", 0):
            self.add("WARNING", "CLIENT_ONLY_REVIEW", "client:only omite render de servidor; revisar fallback y necesidad.")
        if total_directives > 5:
            self.add("WARNING", "CLIENT_ISLANDS_MANY", f"Hay {total_directives} islas hidratadas; revisar presupuesto de JavaScript.")

        installed: list[str] = []
        for name, (packages, extensions) in FRAMEWORKS.items():
            if self.dependencies.intersection(packages):
                installed.append(name)
                if not framework_files.intersection(extensions):
                    self.add("WARNING", "CLIENT_FRAMEWORK_UNUSED", f"Framework {name} declarado sin archivos detectables; revisar dependencia.")
        if installed:
            self.add("INFO", "CLIENT_FRAMEWORKS", f"Framework(s) de interfaz detectado(s): {', '.join(installed)}.")
        if len(installed) > 1:
            self.add("WARNING", "CLIENT_MULTIPLE_RUNTIMES", "Hay varios runtimes de interfaz; justificar cada uno.")

        public_scripts = [path for path in self.iter_files() if is_within(path, self.root / "public") and path.suffix.lower() in {".js", ".mjs"}]
        for path in public_scripts:
            self.add("INFO", "CLIENT_PUBLIC_SCRIPT", "Script en public/ se sirve sin procesamiento; confirmar que es deliberado.", path)

    def check_security(self) -> None:
        secret_patterns = (
            re.compile(r"AKIA[0-9A-Z]{16}"),
            re.compile(r"gh[pousr]_[A-Za-z0-9]{20,}"),
            re.compile(r"(?:sk|pk)_(?:live|test)_[A-Za-z0-9_-]{12,}"),
            re.compile(r"sk-[A-Za-z0-9_-]{16,}"),
            re.compile(r"(?i)\b(?:api[_-]?key|access[_-]?token|client[_-]?secret|password)\b\s*[:=]\s*['\"][^'\"]{12,}['\"]"),
        )
        for path, text in self.texts.items():
            for pattern in secret_patterns:
                match = pattern.search(text)
                if match:
                    self.add(
                        "ERROR",
                        "SEC_POSSIBLE_SECRET",
                        "Posible secreto detectado; el valor fue omitido.",
                        path,
                        line_number(text, match.start()),
                    )
                    break

        env_files = [path for path in self.root.glob(".env*") if path.is_file() and path.name not in {".env.example", ".env.sample"}]
        if env_files:
            gitignore_path = self.root / ".gitignore"
            gitignore = ""
            if gitignore_path.is_file():
                try:
                    gitignore = gitignore_path.read_text(encoding="utf-8")
                except OSError:
                    pass
            ignores_env = any(line.strip() in {".env", ".env*", ".env.*"} for line in gitignore.splitlines())
            for path in env_files:
                severity = "INFO" if ignores_env else "WARNING"
                self.add(severity, "SEC_ENV_FILE", "Existe un archivo de entorno; no se leyó su contenido y debe confirmarse que no esté versionado.", path)

    def local_astro_command(self) -> Optional[list[str]]:
        package_path = self.root / "node_modules" / "astro" / "package.json"
        if not package_path.is_file():
            return None
        node = shutil.which("node")
        if not node:
            return None
        try:
            package = json.loads(package_path.read_text(encoding="utf-8"))
            bin_value = package.get("bin")
            if isinstance(bin_value, dict):
                bin_value = bin_value.get("astro")
            if not isinstance(bin_value, str):
                return None
            entry = (package_path.parent / bin_value).resolve(strict=True)
        except (OSError, json.JSONDecodeError):
            return None
        if not is_within(entry, package_path.parent):
            return None
        return [node, str(entry)]

    def run_external_checks(self) -> None:
        command = self.local_astro_command()
        if command is None:
            self.external_failed = True
            self.add("ERROR", "EXTERNAL_ASTRO_UNAVAILABLE", "No está disponible el CLI local instalado de Astro; no se instaló nada.")
            return
        if self.package_manager == "ambiguous":
            self.external_failed = True
            self.add("ERROR", "EXTERNAL_MANAGER_AMBIGUOUS", "No se ejecutaron comandos porque hay varios lockfiles.")
            return
        self.add("INFO", "EXTERNAL_PACKAGE_MANAGER", f"Gestor detectado: {self.package_manager or 'sin lockfile/metadata'}.")

        actions: list[str] = []
        check_package = self.root / "node_modules" / "@astrojs" / "check" / "package.json"
        typescript_package = self.root / "node_modules" / "typescript" / "package.json"
        if "@astrojs/check" in self.dependencies and "typescript" in self.dependencies and check_package.is_file() and typescript_package.is_file():
            actions.append("check")
        else:
            self.external_failed = True
            self.add(
                "ERROR",
                "EXTERNAL_CHECK_UNAVAILABLE",
                "`astro check` no se ejecutó porque @astrojs/check/TypeScript no están declarados e instalados localmente; no se instaló nada.",
            )
        actions.append("build")

        for action in actions:
            full_command = [*command, action]
            try:
                completed = subprocess.run(
                    full_command,
                    cwd=self.root,
                    capture_output=True,
                    text=True,
                    encoding="utf-8",
                    errors="replace",
                    timeout=self.args.timeout,
                    shell=False,
                    check=False,
                )
            except subprocess.TimeoutExpired:
                self.external_failed = True
                self.add("ERROR", "EXTERNAL_TIMEOUT", f"`astro {action}` excedió {self.args.timeout} segundos.")
                continue
            except OSError as exc:
                self.external_failed = True
                self.add("ERROR", "EXTERNAL_EXECUTION", f"No se pudo ejecutar `astro {action}`: {exc}.")
                continue
            output = redact_output((completed.stdout or "") + "\n" + (completed.stderr or ""))
            if completed.returncode == 0:
                self.add("INFO", "EXTERNAL_OK", f"`astro {action}` finalizó con código 0.")
            else:
                self.external_failed = True
                message = f"`astro {action}` falló con código {completed.returncode}."
                if output.strip():
                    message += f" Salida redactada (máx. 6000 caracteres):\n{output.strip()}"
                self.add("ERROR", "EXTERNAL_FAILED", message)


def resolve_import(candidate: Path) -> Optional[Path]:
    if candidate.is_file():
        return candidate
    extensions = (".astro", ".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs", ".vue", ".svelte", ".css", ".json")
    if not candidate.suffix:
        for extension in extensions:
            option = candidate.with_suffix(extension)
            if option.is_file():
                return option
        if candidate.is_dir():
            for extension in extensions:
                option = candidate / f"index{extension}"
                if option.is_file():
                    return option
    return None


def extract_frontmatter(text: str) -> str:
    if not text.startswith("---"):
        return ""
    end = text.find("\n---", 3)
    return text[3:end] if end != -1 else text


def extract_browser_scripts(text: str) -> list[str]:
    result: list[str] = []
    for match in re.finditer(r"<script\b([^>]*)>(.*?)</script\s*>", text, re.IGNORECASE | re.DOTALL):
        attrs, body = match.groups()
        if re.search(r"\btype\s*=\s*['\"]application/(?:ld\+json|json)['\"]", attrs, re.IGNORECASE):
            continue
        result.append(body)
    return result


def parse_hex(value: str) -> Optional[tuple[int, int, int]]:
    raw = value.lstrip("#")
    if len(raw) == 3:
        raw = "".join(character * 2 for character in raw)
    if len(raw) != 6:
        return None
    try:
        return tuple(int(raw[index : index + 2], 16) for index in (0, 2, 4))  # type: ignore[return-value]
    except ValueError:
        return None


def contrast_ratio(foreground: str, background: str) -> Optional[float]:
    first = parse_hex(foreground)
    second = parse_hex(background)
    if first is None or second is None:
        return None

    def luminance(rgb: tuple[int, int, int]) -> float:
        channels = []
        for value in rgb:
            channel = value / 255
            channels.append(channel / 12.92 if channel <= 0.04045 else ((channel + 0.055) / 1.055) ** 2.4)
        return 0.2126 * channels[0] + 0.7152 * channels[1] + 0.0722 * channels[2]

    one, two = luminance(first), luminance(second)
    lighter, darker = max(one, two), min(one, two)
    return (lighter + 0.05) / (darker + 0.05)


def select_exit_code(auditor: Auditor, strict: bool) -> int:
    if auditor.external_failed:
        return EXIT_EXTERNAL_FAILURE
    if any(item.severity == "ERROR" for item in auditor.findings):
        return EXIT_VALIDATION_ERRORS
    if strict and any(item.severity == "WARNING" for item in auditor.findings):
        return EXIT_STRICT_WARNINGS
    return EXIT_OK


def emit_human(auditor: Auditor, exit_code: int) -> None:
    findings = sorted(
        auditor.findings,
        key=lambda item: (SEVERITY_ORDER[item.severity], item.path or "", item.line or 0, item.code),
    )
    print(f"Proyecto: {auditor.root}")
    for item in findings:
        location = ""
        if item.path:
            location = f" [{item.path}{':' + str(item.line) if item.line else ''}]"
        print(f"{item.severity:<7} {item.code}{location}: {item.message}")
    counts = {severity: sum(1 for item in findings if item.severity == severity) for severity in ("ERROR", "WARNING", "INFO")}
    print(f"Resumen: {counts['ERROR']} error(es), {counts['WARNING']} advertencia(s), {counts['INFO']} info. Código: {exit_code}.")


def emit_json(auditor: Auditor, exit_code: int) -> None:
    counts = {severity: sum(1 for item in auditor.findings if item.severity == severity) for severity in ("ERROR", "WARNING", "INFO")}
    payload = {
        "schema_version": 1,
        "project": str(auditor.root),
        "mode": {"strict": bool(auditor.args.strict), "build": bool(auditor.args.build)},
        "counts": counts,
        "exit_code": exit_code,
        "findings": [
            asdict(item)
            for item in sorted(
                auditor.findings,
                key=lambda value: (SEVERITY_ORDER[value.severity], value.path or "", value.line or 0, value.code),
            )
        ],
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.timeout < 1 or args.max_file_bytes < 1 or args.max_image_bytes < 1 or args.max_component_lines < 1:
        parser.error("los umbrales y el timeout deben ser enteros positivos")
    root = Path(args.project).expanduser().resolve(strict=False)
    if not root.exists():
        parser.error(f"la ruta no existe: {root}")
    if not root.is_dir():
        parser.error(f"la ruta no es un directorio: {root}")

    auditor = Auditor(root, args)
    auditor.run()
    exit_code = select_exit_code(auditor, args.strict)
    if args.json_output:
        emit_json(auditor, exit_code)
    else:
        emit_human(auditor, exit_code)
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
