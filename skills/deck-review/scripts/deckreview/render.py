"""Render a .pptx to PDF with LibreOffice (headless), then to one PNG per slide.

LibreOffice is optional: without it the review still inspects and checks the
deck, and prints how to install it. Nothing is ever installed automatically.
PNG output needs pypdfium2 and Pillow (pip install pypdfium2 pillow).
"""

from __future__ import annotations

import os
import shutil
import stat
import subprocess
import tempfile
from pathlib import Path

SOFFICE_CANDIDATES = [
    "/Applications/LibreOffice.app/Contents/MacOS/soffice",
    "/opt/homebrew/bin/soffice",
    "/usr/local/bin/soffice",
    "/usr/bin/soffice",
    "/usr/bin/libreoffice",
    "/snap/bin/libreoffice",
    r"C:\Program Files\LibreOffice\program\soffice.exe",
    r"C:\Program Files (x86)\LibreOffice\program\soffice.exe",
]


def install_hint() -> str:
    return (
        "LibreOffice renders the slides for visual review; inspection and checks run "
        "without it.\n"
        "Install it yourself, then re-run (or pass --soffice /path/to/soffice):\n"
        "  macOS:          brew install --cask libreoffice\n"
        "  Ubuntu/Debian:  sudo apt-get install -y libreoffice-impress\n"
        "  Fedora:         sudo dnf install -y libreoffice-impress\n"
        "  Windows:        winget install TheDocumentFoundation.LibreOffice\n"
        "  Or download it from libreoffice.org."
    )


def find_soffice(explicit: str | None = None) -> str | None:
    """Path to the soffice binary, or None. An explicit path must exist."""
    if explicit:
        return explicit if Path(explicit).is_file() else None
    for name in ("soffice", "libreoffice"):
        found = shutil.which(name)
        if found:
            return found
    for cand in SOFFICE_CANDIDATES:
        if Path(cand).is_file():
            return cand
    return None


def _stable_profile_name() -> str:
    uid = os.getuid() if hasattr(os, "getuid") else "user"
    return f"deck-review-lo-{uid}"


def lo_profile_dir(base=None) -> Path:
    """A LibreOffice profile folder that only the current user can write.

    Reused between runs (LibreOffice starts faster with a warm profile). If the
    usual path is unsafe (a symlink, another owner, or open permissions, e.g.
    planted in a shared /tmp), a fresh private folder is returned instead.
    """
    base = Path(base or tempfile.gettempdir())
    path = base / _stable_profile_name()
    uid = os.getuid() if hasattr(os, "getuid") else None
    try:
        if not os.path.lexists(path):
            path.mkdir(mode=0o700)
        st = os.lstat(path)
        private = stat.S_ISDIR(st.st_mode) and (
            uid is None or (st.st_uid == uid and stat.S_IMODE(st.st_mode) & 0o077 == 0))
        if private:
            return path
    except OSError:
        pass
    return Path(tempfile.mkdtemp(prefix="deck-review-lo-tmp-", dir=base))  # mode 0700


def convert_to_pdf(pptx: Path, out_dir: Path, soffice: str, timeout: int = 180) -> Path:
    """Run LibreOffice once with a fixed argument list. Returns the PDF path."""
    out_dir.mkdir(parents=True, exist_ok=True)
    profile = lo_profile_dir()
    try:
        return _convert(pptx, out_dir, soffice, profile, timeout)
    finally:
        if profile.name != _stable_profile_name():
            shutil.rmtree(profile, ignore_errors=True)


def _convert(pptx, out_dir, soffice, profile, timeout):
    with tempfile.TemporaryDirectory(prefix="deck-review-") as tmp:
        tmp = Path(tmp)
        src = tmp / ("deck" + pptx.suffix.lower())  # safe name: no spaces or leading '-'
        shutil.copyfile(pptx, src)
        cmd = [
            soffice, "--headless", "--invisible", "--nologo", "--norestore",
            "--nolockcheck", f"-env:UserInstallation={profile.as_uri()}",
            "--convert-to", "pdf", "--outdir", str(tmp), str(src),
        ]
        proc = subprocess.run(cmd, capture_output=True, timeout=timeout, check=False)
        produced = tmp / "deck.pdf"
        if not produced.exists():
            err = (proc.stderr or b"").decode("utf-8", "replace").strip()[-400:]
            raise RuntimeError(f"LibreOffice did not produce a PDF (exit {proc.returncode}). "
                               f"{err}")
        dest = out_dir / (pptx.stem + ".pdf")
        shutil.move(str(produced), dest)
    return dest


def pdf_to_pngs(pdf: Path, out_dir: Path, width_px: int = 1600) -> list[Path]:
    import pypdfium2 as pdfium  # optional dependency

    out_dir.mkdir(parents=True, exist_ok=True)
    pngs = []
    doc = pdfium.PdfDocument(str(pdf))
    try:
        for i in range(len(doc)):
            page = doc[i]
            scale = width_px / page.get_width()
            img = page.render(scale=scale).to_pil()
            if img.size[0] != width_px:
                img = img.resize((width_px, round(img.size[1] * width_px / img.size[0])))
            path = out_dir / f"slide-{i + 1:02d}.png"
            img.save(path)
            pngs.append(path)
            page.close()
    finally:
        doc.close()
    return pngs


def render_pptx(pptx, out_dir, soffice: str | None = None, width_px: int = 1600,
                timeout: int = 180) -> dict:
    """Render `pptx` into out_dir. Never raises for a missing tool.

    Returns {"pdf": Path|None, "pngs": [Path], "error": str|None}.
    PNGs are numbered by page; LibreOffice skips hidden slides.
    """
    pptx, out_dir = Path(pptx), Path(out_dir)
    result = {"pdf": None, "pngs": [], "error": None}
    exe = find_soffice(soffice)
    if not exe:
        result["error"] = "LibreOffice (soffice) was not found.\n" + install_hint()
        return result
    try:
        result["pdf"] = convert_to_pdf(pptx, out_dir, exe, timeout=timeout)
    except (RuntimeError, OSError, subprocess.TimeoutExpired) as exc:
        result["error"] = f"Rendering failed: {exc}"
        return result
    try:
        result["pngs"] = pdf_to_pngs(result["pdf"], out_dir, width_px)
    except ImportError:
        result["error"] = ("PDF written, but PNG export needs pypdfium2 and Pillow: "
                           "pip install pypdfium2 pillow")
    except Exception as exc:  # a broken PDF page should not stop the review
        result["error"] = f"PNG export failed: {exc}"
    return result
