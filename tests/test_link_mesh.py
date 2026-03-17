#!/usr/bin/env python3
"""
Link Mesh Validator — Elktron Hackathon
========================================
Scans all HTML and Markdown files for asset references (src, href, url(),
GLTFLoader, markdown images/links) and verifies every local path resolves
to a real file. Optionally checks external URLs are reachable.

Usage:
    python tests/test_link_mesh.py              # local refs only (fast)
    python tests/test_link_mesh.py --check-urls # also probe external URLs
    python -m pytest tests/test_link_mesh.py -v # via pytest
"""

import os
import re
import sys
import urllib.request
import urllib.error
from pathlib import Path
from dataclasses import dataclass, field

# ── Config ──────────────────────────────────────────────────────────────────

REPO_ROOT = Path(__file__).resolve().parent.parent

# Directories to skip entirely
SKIP_DIRS = {
    ".git", "node_modules", ".venv", "__pycache__",
    "elktron-app/.venv", ".DS_Store",
}

# Known external URL prefixes (not local file refs)
EXTERNAL_PREFIXES = ("http://", "https://", "mailto:", "tel:", "data:", "blob:", "javascript:")

# URL patterns we don't check (CDN, badges, etc.)
SKIP_URL_PATTERNS = [
    r"img\.shields\.io",
    r"cdn\.jsdelivr\.net",
    r"unpkg\.com",
    r"fonts\.googleapis\.com",
    r"fonts\.gstatic\.com",
    r"ga\.jspm\.io",
    r"raw\.githubusercontent\.com",
    r"three\.module",
]

# File extensions that count as "asset references" worth checking
ASSET_EXTENSIONS = {
    ".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg", ".ico",
    ".pdf", ".glb", ".gltf", ".obj", ".mtl", ".blend",
    ".mp4", ".webm", ".mp3", ".wav",
    ".css", ".js", ".json", ".woff", ".woff2", ".ttf",
}

# ── Data ────────────────────────────────────────────────────────────────────

@dataclass
class LinkRef:
    source_file: str      # file containing the reference
    target_raw: str       # the raw path/URL as written
    target_resolved: str  # resolved absolute path (for local) or URL
    line_number: int
    ref_type: str         # "src", "href", "url()", "md-image", "md-link", "js-load"
    is_external: bool = False
    exists: bool = False
    status_code: int = 0
    error: str = ""


# ── Extraction ──────────────────────────────────────────────────────────────

def should_skip(path: Path) -> bool:
    parts = path.relative_to(REPO_ROOT).parts
    return any(skip in parts for skip in SKIP_DIRS)


def extract_html_refs(filepath: Path) -> list[LinkRef]:
    """Extract src=, href=, url(), and JS loader references from HTML."""
    refs = []
    try:
        content = filepath.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return refs

    lines = content.split("\n")

    # src="..." and href="..."
    attr_re = re.compile(r'''(?:src|href|poster|data-src|action)\s*=\s*["']([^"'#?]+?)["']''', re.IGNORECASE)
    # url(...) in inline CSS
    url_re = re.compile(r'''url\(\s*["']?([^"')#?]+?)["']?\s*\)''', re.IGNORECASE)
    # GLTFLoader.load / TextureLoader.load / etc
    js_load_re = re.compile(r'''\.load\(\s*["'`]([^"'`#?]+?)["'`]''')
    # fetch("...") for JSON/assets
    fetch_re = re.compile(r'''fetch\(\s*["'`]([^"'`#?]+?)["'`]''')

    for i, line in enumerate(lines, 1):
        for m in attr_re.finditer(line):
            val = m.group(1).strip()
            if not _is_template(val):
                refs.append(_make_ref(filepath, val, i, "attr"))
        for m in url_re.finditer(line):
            val = m.group(1).strip()
            if not _is_template(val):
                refs.append(_make_ref(filepath, val, i, "url()"))
        for m in js_load_re.finditer(line):
            val = m.group(1).strip()
            if not _is_template(val):
                refs.append(_make_ref(filepath, val, i, "js-load"))
        for m in fetch_re.finditer(line):
            val = m.group(1).strip()
            if not _is_template(val) and not val.startswith("/api"):
                refs.append(_make_ref(filepath, val, i, "fetch"))

    return refs


def extract_md_refs(filepath: Path) -> list[LinkRef]:
    """Extract image and link references from Markdown."""
    refs = []
    try:
        content = filepath.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return refs

    lines = content.split("\n")

    # ![alt](path) — markdown images
    img_re = re.compile(r'!\[[^\]]*\]\(([^)#?]+)\)')
    # [text](path) — markdown links
    link_re = re.compile(r'(?<!!)\[[^\]]*\]\(([^)#?]+)\)')
    # HTML in markdown: src="..." href="..."
    attr_re = re.compile(r'''(?:src|href)\s*=\s*["']([^"'#?]+?)["']''', re.IGNORECASE)

    for i, line in enumerate(lines, 1):
        for m in img_re.finditer(line):
            refs.append(_make_ref(filepath, m.group(1).strip(), i, "md-image"))
        for m in link_re.finditer(line):
            refs.append(_make_ref(filepath, m.group(1).strip(), i, "md-link"))
        for m in attr_re.finditer(line):
            refs.append(_make_ref(filepath, m.group(1).strip(), i, "attr"))

    return refs


def _is_template(val: str) -> bool:
    """Skip JS template literals, regex backrefs, and dynamic values."""
    return bool(re.search(r'[\$\{]', val)) or val.startswith("$")


def _make_ref(source: Path, target_raw: str, line: int, ref_type: str) -> LinkRef:
    """Create a LinkRef, resolving local paths relative to the source file."""
    is_ext = any(target_raw.startswith(p) for p in EXTERNAL_PREFIXES)

    if target_raw.startswith("file:///"):
        # file:/// URLs are local absolute paths — treat as local refs
        resolved = target_raw[7:]  # strip "file:///"
        resolved = "/" + resolved if not resolved.startswith("/") else resolved
        is_ext = False
    elif is_ext:
        resolved = target_raw
    else:
        # Resolve relative to the source file's directory
        source_dir = source.parent
        resolved = str((source_dir / target_raw).resolve())

    return LinkRef(
        source_file=str(source.relative_to(REPO_ROOT)),
        target_raw=target_raw,
        target_resolved=resolved,
        line_number=line,
        ref_type=ref_type,
        is_external=is_ext,
    )


# ── Validation ──────────────────────────────────────────────────────────────

def validate_local(ref: LinkRef) -> LinkRef:
    """Check if a local file reference exists on disk."""
    target = Path(ref.target_resolved)
    # Also check as directory (for href="docs/" style links)
    if target.exists() or target.is_dir():
        ref.exists = True
    elif (target.parent / target.name).exists():
        ref.exists = True
    else:
        ref.exists = False
        ref.error = "File not found"
    return ref


def validate_url(ref: LinkRef, timeout: int = 10) -> LinkRef:
    """Check if an external URL is reachable (HEAD request)."""
    # Skip CDN/badge URLs
    for pattern in SKIP_URL_PATTERNS:
        if re.search(pattern, ref.target_raw):
            ref.exists = True
            ref.status_code = 0
            ref.error = "skipped (CDN/badge)"
            return ref

    try:
        req = urllib.request.Request(ref.target_raw, method="HEAD",
                                     headers={"User-Agent": "ElktronLinkChecker/1.0"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            ref.status_code = resp.status
            ref.exists = ref.status_code < 400
            if not ref.exists:
                ref.error = f"HTTP {ref.status_code}"
    except urllib.error.HTTPError as e:
        # Some servers reject HEAD, try GET
        if e.code == 405:
            try:
                req = urllib.request.Request(ref.target_raw,
                                             headers={"User-Agent": "ElktronLinkChecker/1.0"})
                with urllib.request.urlopen(req, timeout=timeout) as resp:
                    ref.status_code = resp.status
                    ref.exists = ref.status_code < 400
            except Exception as e2:
                ref.status_code = 0
                ref.exists = False
                ref.error = str(e2)[:80]
        else:
            ref.status_code = e.code
            ref.exists = e.code < 400
            if not ref.exists:
                ref.error = f"HTTP {e.code}"
    except Exception as e:
        ref.status_code = 0
        ref.exists = False
        ref.error = str(e)[:80]

    return ref


# ── Scanner ─────────────────────────────────────────────────────────────────

def scan_repo(check_urls: bool = False) -> tuple[list[LinkRef], list[LinkRef]]:
    """Scan all HTML/MD files, return (all_refs, broken_refs)."""
    all_refs: list[LinkRef] = []

    for root, dirs, files in os.walk(REPO_ROOT):
        root_path = Path(root)
        if should_skip(root_path):
            dirs.clear()
            continue
        # Prune skip dirs from traversal
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]

        for fname in files:
            fpath = root_path / fname
            if fpath.suffix.lower() in (".html", ".htm"):
                all_refs.extend(extract_html_refs(fpath))
            elif fpath.suffix.lower() in (".md", ".markdown"):
                all_refs.extend(extract_md_refs(fpath))

    # Validate
    for ref in all_refs:
        if ref.is_external:
            if check_urls:
                validate_url(ref)
            else:
                ref.exists = True  # skip external by default
                ref.error = "skipped"
        else:
            validate_local(ref)

    broken = [r for r in all_refs if not r.exists]
    return all_refs, broken


# ── Report ──────────────────────────────────────────────────────────────────

def print_report(all_refs: list[LinkRef], broken: list[LinkRef], check_urls: bool):
    local_refs = [r for r in all_refs if not r.is_external]
    ext_refs = [r for r in all_refs if r.is_external]
    local_broken = [r for r in broken if not r.is_external]
    ext_broken = [r for r in broken if r.is_external]

    print(f"\n{'='*70}")
    print(f"  LINK MESH REPORT — Elktron Hackathon")
    print(f"{'='*70}")
    print(f"  Scanned:  {len(set(r.source_file for r in all_refs))} files")
    print(f"  Local refs:    {len(local_refs):>4}  ({len(local_broken)} broken)")
    print(f"  External refs: {len(ext_refs):>4}  ({len(ext_broken)} broken)" +
          ("" if check_urls else "  [skipped — use --check-urls]"))
    print(f"{'='*70}\n")

    if local_broken:
        print("BROKEN LOCAL REFERENCES:")
        print("-" * 70)
        for ref in sorted(local_broken, key=lambda r: (r.source_file, r.line_number)):
            print(f"  {ref.source_file}:{ref.line_number}")
            print(f"    {ref.ref_type}: {ref.target_raw}")
            print(f"    resolved: {ref.target_resolved}")
            print(f"    error: {ref.error}")
            print()

    if ext_broken:
        print("BROKEN EXTERNAL URLs:")
        print("-" * 70)
        for ref in sorted(ext_broken, key=lambda r: (r.source_file, r.line_number)):
            print(f"  {ref.source_file}:{ref.line_number}")
            print(f"    {ref.target_raw}")
            print(f"    error: {ref.error}")
            print()

    if not broken:
        print("ALL LINKS VALID")

    return len(broken)


# ── Pytest integration ──────────────────────────────────────────────────────

def test_local_references():
    """All local file references in HTML/MD must resolve to existing files."""
    all_refs, broken = scan_repo(check_urls=False)
    local_broken = [r for r in broken if not r.is_external]

    if local_broken:
        msg_lines = [f"\n{len(local_broken)} broken local reference(s):\n"]
        for ref in local_broken:
            msg_lines.append(f"  {ref.source_file}:{ref.line_number} -> {ref.target_raw}")
        raise AssertionError("\n".join(msg_lines))


def test_no_orphan_active_images():
    """Every file in img/ (non-CLAUDE.md) should be referenced somewhere."""
    img_dir = REPO_ROOT / "img"
    if not img_dir.exists():
        return

    all_refs, _ = scan_repo(check_urls=False)
    referenced_targets = set()
    for ref in all_refs:
        if not ref.is_external:
            referenced_targets.add(Path(ref.target_resolved).resolve())

    orphans = []
    for f in img_dir.iterdir():
        if f.is_dir() or f.name in ("CLAUDE.md", ".DS_Store"):
            continue
        if f.resolve() not in referenced_targets:
            orphans.append(str(f.relative_to(REPO_ROOT)))

    if orphans:
        msg = f"\n{len(orphans)} orphan file(s) in img/ (not referenced by any HTML/MD):\n"
        msg += "\n".join(f"  {o}" for o in orphans)
        raise AssertionError(msg)


def test_glb_models_referenced():
    """Every GLB in glb/ should be loaded by at least one HTML file."""
    glb_dir = REPO_ROOT / "glb"
    if not glb_dir.exists():
        return

    all_refs, _ = scan_repo(check_urls=False)
    referenced_targets = set()
    for ref in all_refs:
        if not ref.is_external:
            referenced_targets.add(Path(ref.target_resolved).resolve())

    orphans = []
    for f in glb_dir.glob("*.glb"):
        if f.resolve() not in referenced_targets:
            orphans.append(str(f.relative_to(REPO_ROOT)))

    if orphans:
        msg = f"\n{len(orphans)} orphan GLB model(s) in glb/ (not loaded by any HTML):\n"
        msg += "\n".join(f"  {o}" for o in orphans)
        raise AssertionError(msg)


def test_progression_images_referenced():
    """Every file in progression/ (non-README) should be referenced somewhere."""
    prog_dir = REPO_ROOT / "progression"
    if not prog_dir.exists():
        return

    all_refs, _ = scan_repo(check_urls=False)
    referenced_targets = set()
    for ref in all_refs:
        if not ref.is_external:
            referenced_targets.add(Path(ref.target_resolved).resolve())

    orphans = []
    for f in prog_dir.iterdir():
        if f.is_dir() or f.name in ("README.md", ".DS_Store"):
            continue
        if f.resolve() not in referenced_targets:
            orphans.append(str(f.relative_to(REPO_ROOT)))

    if orphans:
        msg = f"\n{len(orphans)} orphan file(s) in progression/ (not referenced by any HTML/MD):\n"
        msg += "\n".join(f"  {o}" for o in orphans)
        raise AssertionError(msg)


# ── CLI ─────────────────────────────────────────────────────────────────────

def main():
    check_urls = "--check-urls" in sys.argv
    all_refs, broken = scan_repo(check_urls=check_urls)
    count = print_report(all_refs, broken, check_urls)
    sys.exit(1 if count > 0 else 0)


if __name__ == "__main__":
    main()
