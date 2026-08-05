#!/usr/bin/env python3
"""Descarga opcional de imágenes desde Openverse con licencia y ledger.

No almacena credenciales, solo acepta HTTPS, limita tamaño, valida tipo de archivo,
mantiene todas las salidas dentro del proyecto y no sobrescribe sin --overwrite.
La licencia y atribución deben revisarse manualmente antes de publicar.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Sequence
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urlsplit
from urllib.request import Request, urlopen


API_URL = "https://api.openverse.org/v1/images/"
ALLOWED_LICENSES = {"cc0", "pdm", "by", "by-sa"}
MIME_EXTENSIONS = {
    "image/avif": ".avif",
    "image/gif": ".gif",
    "image/jpeg": ".jpg",
    "image/png": ".png",
    "image/webp": ".webp",
}
EXIT_OK = 0
EXIT_PARTIAL = 1
EXIT_USAGE = 3
EXIT_NETWORK = 4


class Exit3Parser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        self.print_usage()
        self.exit(EXIT_USAGE, f"{self.prog}: error: {message}\n")


@dataclass(frozen=True)
class Query:
    asset_id: str
    query: str
    alt: str


def parser() -> argparse.ArgumentParser:
    result = Exit3Parser(description="Obtiene assets de Openverse de forma controlada y registra su procedencia.")
    result.add_argument("--project", required=True, help="Raíz del proyecto Astro.")
    source = result.add_mutually_exclusive_group(required=True)
    source.add_argument("--queries", help="JSON con una lista de {id, query, alt}.")
    source.add_argument(
        "--inline-query",
        action="append",
        metavar="ID=CONSULTA",
        help="Consulta individual; puede repetirse. El alt queda pendiente en el ledger.",
    )
    result.add_argument("--target", default="src/assets/openverse", help="Directorio de imágenes relativo al proyecto.")
    result.add_argument("--credits", default="openverse-credits.json", help="Ledger JSON relativo al proyecto.")
    result.add_argument(
        "--licenses",
        default="cc0,pdm,by,by-sa",
        help="Licencias permitidas separadas por coma: cc0,pdm,by,by-sa.",
    )
    result.add_argument("--max-bytes", type=int, default=8_000_000, help="Máximo por descarga; predeterminado: 8000000.")
    result.add_argument("--timeout", type=int, default=20, help="Timeout de red; predeterminado: 20 segundos.")
    result.add_argument("--throttle-ms", type=int, default=400, help="Pausa entre consultas; predeterminado: 400 ms.")
    result.add_argument("--overwrite", action="store_true", help="Permite reemplazar un asset con el mismo id.")
    result.add_argument("--dry-run", action="store_true", help="Valida y muestra el plan sin acceder a la red ni escribir.")
    result.add_argument("--json", dest="json_output", action="store_true", help="Salida JSON.")
    return result


def within(path: Path, root: Path) -> bool:
    try:
        path.resolve(strict=False).relative_to(root.resolve(strict=True))
        return True
    except (OSError, ValueError):
        return False


def safe_path(root: Path, value: str, must_exist: bool = False) -> Path:
    candidate = (root / value).resolve(strict=False) if not Path(value).is_absolute() else Path(value).resolve(strict=False)
    if not within(candidate, root):
        raise ValueError(f"la ruta sale del proyecto: {value}")
    relative = candidate.relative_to(root)
    cursor = root
    for part in relative.parts:
        cursor = cursor / part
        if cursor.exists() and cursor.is_symlink():
            raise ValueError(f"no se permiten enlaces simbólicos en la ruta de salida: {value}")
    if must_exist and not candidate.is_file():
        raise ValueError(f"no existe el archivo: {value}")
    return candidate


def load_queries(root: Path, args: argparse.Namespace) -> list[Query]:
    raw_items: list[dict[str, str]] = []
    if args.queries:
        path = safe_path(root, args.queries, must_exist=True)
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError(f"JSON de consultas inválido: {exc}") from exc
        if not isinstance(payload, list):
            raise ValueError("el JSON de consultas debe ser una lista")
        for item in payload:
            if not isinstance(item, dict):
                raise ValueError("cada consulta debe ser un objeto")
            raw_items.append({"id": str(item.get("id", "")), "query": str(item.get("query", "")), "alt": str(item.get("alt", ""))})
    else:
        for value in args.inline_query or []:
            if "=" not in value:
                raise ValueError("--inline-query debe usar ID=CONSULTA")
            asset_id, query = value.split("=", 1)
            raw_items.append({"id": asset_id, "query": query, "alt": ""})

    result: list[Query] = []
    seen: set[str] = set()
    for item in raw_items:
        asset_id = item["id"].strip().lower()
        query = item["query"].strip()
        alt = item["alt"].strip()
        if not re.fullmatch(r"[a-z0-9][a-z0-9-]{0,63}", asset_id):
            raise ValueError(f"id no seguro: {asset_id!r}")
        if asset_id in seen:
            raise ValueError(f"id duplicado: {asset_id}")
        if not query or len(query) > 200:
            raise ValueError(f"consulta vacía o demasiado larga para {asset_id}")
        seen.add(asset_id)
        result.append(Query(asset_id, query, alt))
    if not result:
        raise ValueError("no se proporcionaron consultas")
    return result


def https_url(value: str) -> bool:
    parsed = urlsplit(value)
    return parsed.scheme == "https" and bool(parsed.netloc) and parsed.username is None and parsed.password is None


def request_json(url: str, timeout: int, retries: int = 2) -> dict:
    if not https_url(url):
        raise ValueError("la URL de API no es HTTPS segura")
    last_error: Optional[Exception] = None
    for attempt in range(retries + 1):
        try:
            request = Request(url, headers={"User-Agent": "astro-premium-landing/1.0 (+asset-audit)"})
            with urlopen(request, timeout=timeout) as response:
                if not https_url(response.geturl()):
                    raise ValueError("la redirección de API abandonó HTTPS")
                if response.status != 200:
                    raise RuntimeError(f"HTTP {response.status}")
                data = response.read(2_000_001)
                if len(data) > 2_000_000:
                    raise RuntimeError("respuesta de API demasiado grande")
            payload = json.loads(data.decode("utf-8"))
            if not isinstance(payload, dict):
                raise RuntimeError("respuesta de API inesperada")
            return payload
        except HTTPError as exc:
            last_error = exc
            if exc.code not in {429, 500, 502, 503, 504} or attempt == retries:
                break
        except (URLError, OSError, RuntimeError, ValueError, json.JSONDecodeError, UnicodeDecodeError) as exc:
            last_error = exc
            if attempt == retries:
                break
        time.sleep(1.5 * (attempt + 1))
    raise RuntimeError(f"falló la consulta de Openverse: {type(last_error).__name__}")


def select_result(payload: dict, licenses: set[str]) -> dict:
    results = payload.get("results")
    if not isinstance(results, list):
        raise RuntimeError("Openverse no devolvió una lista de resultados")
    for item in results:
        if not isinstance(item, dict):
            continue
        license_id = str(item.get("license", "")).lower()
        url = str(item.get("url") or "")
        if license_id in licenses and https_url(url):
            return item
    raise RuntimeError("no se encontró un resultado HTTPS con licencia permitida")


def sniff_extension(data: bytes, content_type: str) -> Optional[str]:
    mime = content_type.split(";", 1)[0].strip().lower()
    extension = MIME_EXTENSIONS.get(mime)
    if extension == ".jpg" and data.startswith(b"\xff\xd8\xff"):
        return extension
    if extension == ".png" and data.startswith(b"\x89PNG\r\n\x1a\n"):
        return extension
    if extension == ".gif" and data.startswith((b"GIF87a", b"GIF89a")):
        return extension
    if extension == ".webp" and data[:4] == b"RIFF" and data[8:12] == b"WEBP":
        return extension
    if extension == ".avif" and len(data) >= 12 and data[4:8] == b"ftyp" and b"avif" in data[8:32]:
        return extension
    return None


def download(url: str, target_dir: Path, stem: str, max_bytes: int, timeout: int, overwrite: bool) -> tuple[Path, int, str]:
    if not https_url(url):
        raise RuntimeError("la URL del asset no es HTTPS segura")
    request = Request(url, headers={"User-Agent": "astro-premium-landing/1.0 (+asset-audit)"})
    temporary_path: Optional[Path] = None
    try:
        with urlopen(request, timeout=timeout) as response:
            if not https_url(response.geturl()):
                raise RuntimeError("la redirección del asset abandonó HTTPS")
            length = response.headers.get("Content-Length")
            if length and int(length) > max_bytes:
                raise RuntimeError("el asset excede --max-bytes")
            content_type = response.headers.get("Content-Type", "")
            with tempfile.NamedTemporaryFile(prefix=".openverse-", suffix=".part", dir=target_dir, delete=False) as handle:
                temporary_path = Path(handle.name)
                total = 0
                first = b""
                while True:
                    chunk = response.read(min(65_536, max_bytes + 1 - total))
                    if not chunk:
                        break
                    total += len(chunk)
                    if total > max_bytes:
                        raise RuntimeError("el asset excede --max-bytes")
                    if len(first) < 64:
                        first += chunk[: 64 - len(first)]
                    handle.write(chunk)
        extension = sniff_extension(first, content_type)
        if extension is None:
            raise RuntimeError("tipo MIME o firma de imagen no permitidos")
        destination = target_dir / f"{stem}{extension}"
        if destination.exists() and not overwrite:
            raise FileExistsError(f"ya existe {destination.name}; usa --overwrite")
        os.replace(temporary_path, destination)
        temporary_path = None
        return destination, total, content_type.split(";", 1)[0].lower()
    finally:
        if temporary_path is not None and temporary_path.exists():
            temporary_path.unlink()


def write_ledger(path: Path, entries: list[dict], overwrite: bool) -> None:
    existing: list[dict] = []
    if path.exists():
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
            if isinstance(payload, list):
                existing = [item for item in payload if isinstance(item, dict)]
        except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise RuntimeError(f"ledger existente inválido: {exc}") from exc
    by_id = {str(item.get("id")): item for item in existing}
    for entry in entries:
        if entry["id"] in by_id and not overwrite:
            raise RuntimeError(f"el ledger ya contiene {entry['id']}; usa --overwrite")
        by_id[entry["id"]] = entry
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=".openverse-ledger-", suffix=".json", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
            json.dump(list(by_id.values()), handle, ensure_ascii=False, indent=2)
            handle.write("\n")
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = parser().parse_args(argv)
    if args.max_bytes < 1 or args.timeout < 1 or args.throttle_ms < 0:
        raise SystemExit(EXIT_USAGE)
    root = Path(args.project).expanduser().resolve(strict=False)
    if not root.is_dir():
        print(f"ERROR: el proyecto no existe o no es un directorio: {root}")
        return EXIT_USAGE
    try:
        target_dir = safe_path(root, args.target)
        ledger_path = safe_path(root, args.credits)
        queries = load_queries(root, args)
        licenses = {value.strip().lower() for value in args.licenses.split(",") if value.strip()}
        if not licenses or not licenses.issubset(ALLOWED_LICENSES):
            raise ValueError(f"licencias permitidas: {', '.join(sorted(ALLOWED_LICENSES))}")
    except ValueError as exc:
        print(f"ERROR: {exc}")
        return EXIT_USAGE

    if args.dry_run:
        payload = {
            "dry_run": True,
            "project": str(root),
            "target": str(target_dir),
            "ledger": str(ledger_path),
            "licenses": sorted(licenses),
            "queries": [query.__dict__ for query in queries],
            "network_accessed": False,
            "files_written": False,
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2) if args.json_output else f"DRY RUN: {len(queries)} consulta(s); sin red ni escrituras.")
        return EXIT_OK

    target_dir.mkdir(parents=True, exist_ok=True)
    entries: list[dict] = []
    failures: list[dict] = []
    for index, query in enumerate(queries):
        try:
            params = urlencode({"q": query.query, "license": ",".join(sorted(licenses)), "page_size": 20})
            result = select_result(request_json(f"{API_URL}?{params}", args.timeout), licenses)
            destination, size, mime = download(str(result.get("url")), target_dir, query.asset_id, args.max_bytes, args.timeout, args.overwrite)
            entry = {
                "id": query.asset_id,
                "query": query.query,
                "alt": query.alt,
                "file": destination.relative_to(root).as_posix(),
                "bytes": size,
                "mime": mime,
                "title": str(result.get("title") or ""),
                "creator": str(result.get("creator") or ""),
                "creator_url": str(result.get("creator_url") or ""),
                "source": str(result.get("source") or ""),
                "foreign_landing_url": str(result.get("foreign_landing_url") or ""),
                "license": str(result.get("license") or "").lower(),
                "license_url": str(result.get("license_url") or ""),
                "openverse_id": str(result.get("id") or ""),
                "attribution_reviewed": False,
            }
            entries.append(entry)
        except (HTTPError, URLError, OSError, RuntimeError, ValueError) as exc:
            failures.append({"id": query.asset_id, "error": str(exc)})
        if index < len(queries) - 1 and args.throttle_ms:
            time.sleep(args.throttle_ms / 1000)

    try:
        if entries:
            write_ledger(ledger_path, entries, args.overwrite)
    except (OSError, RuntimeError) as exc:
        failures.append({"id": "ledger", "error": str(exc)})

    payload = {"downloaded": entries, "failures": failures, "ledger": str(ledger_path)}
    if args.json_output:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        for entry in entries:
            print(f"OK: {entry['id']} -> {entry['file']} ({entry['license']})")
        for failure in failures:
            print(f"ERROR: {failure['id']}: {failure['error']}")
        print("Revisa manualmente licencia, atribución y texto alternativo antes de publicar.")
    if failures:
        return EXIT_PARTIAL if entries else EXIT_NETWORK
    return EXIT_OK


if __name__ == "__main__":
    raise SystemExit(main())
