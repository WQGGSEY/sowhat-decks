"""Render .pptx -> .pdf (LibreOffice, if installed) -> preview PNGs (pypdfium2, if installed).

Nothing is installed or downloaded here. When a tool is missing the result says
so and the build still succeeds with the .pptx alone.
"""
from __future__ import annotations

import os
import pathlib
import shutil
import subprocess
import tempfile
from dataclasses import dataclass, field

_CANDIDATES = (
    "/Applications/LibreOffice.app/Contents/MacOS/soffice",
    "/usr/bin/soffice", "/usr/local/bin/soffice", "/opt/homebrew/bin/soffice", "/snap/bin/libreoffice",
    r"C:\Program Files\LibreOffice\program\soffice.exe",
    r"C:\Program Files (x86)\LibreOffice\program\soffice.exe",
)
INSTALL_HINT = ("LibreOffice not found, so no PDF/PNG preview was made (the .pptx is fine). "
                "Install it from https://www.libreoffice.org/download/ or set SOFFICE=/path/to/soffice.")


@dataclass
class RenderResult:
    pdf: pathlib.Path | None = None
    pngs: list[pathlib.Path] = field(default_factory=list)
    message: str = ""


def find_soffice() -> str | None:
    env = os.environ.get("SOFFICE")
    if env and pathlib.Path(env).is_file():
        return env
    for name in ("soffice", "libreoffice"):
        found = shutil.which(name)
        if found:
            return found
    return next((c for c in _CANDIDATES if pathlib.Path(c).is_file()), None)


def to_pdf(pptx: pathlib.Path, out_dir: pathlib.Path, soffice: str, timeout: int = 240) -> pathlib.Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    # a throwaway LibreOffice profile, so the user's own profile and open windows are never touched
    # (mkdtemp + rmtree rather than TemporaryDirectory(ignore_cleanup_errors=...), which needs Python 3.10)
    profile = pathlib.Path(tempfile.mkdtemp(prefix="sowhat-lo-"))
    try:
        cmd = [soffice, f"-env:UserInstallation={profile.as_uri()}", "--headless", "--norestore",
               "--convert-to", "pdf", "--outdir", str(out_dir), str(pptx)]
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, check=False)
    finally:
        shutil.rmtree(profile, ignore_errors=True)
    pdf = out_dir / (pptx.stem + ".pdf")
    if not pdf.is_file():
        raise RuntimeError(f"LibreOffice did not produce {pdf.name}: {proc.stderr.strip() or proc.stdout.strip()}")
    return pdf


def to_pngs(pdf: pathlib.Path, out_dir: pathlib.Path, width: int = 1600) -> list[pathlib.Path]:
    import pypdfium2 as pdfium  # optional dependency, imported only when rendering

    out_dir.mkdir(parents=True, exist_ok=True)
    for old in out_dir.glob("slide-*.png"):
        old.unlink()
    doc = pdfium.PdfDocument(str(pdf))
    paths = []
    try:
        for i in range(len(doc)):
            page = doc[i]
            scale = width / page.get_width()
            image = page.render(scale=scale).to_pil()
            path = out_dir / f"slide-{i + 1:02d}.png"
            image.save(path)
            paths.append(path)
    finally:
        doc.close()
    return paths


def render(pptx: str | pathlib.Path, out_dir: str | pathlib.Path, *, width: int = 1600) -> RenderResult:
    """deck.pdf in out_dir and out_dir/preview/slide-NN.png, as far as the installed tools allow."""
    pptx, out_dir = pathlib.Path(pptx), pathlib.Path(out_dir)
    soffice = find_soffice()
    if not soffice:
        return RenderResult(message=INSTALL_HINT)
    pdf = to_pdf(pptx, out_dir, soffice)
    try:
        pngs = to_pngs(pdf, out_dir / "preview", width)
    except ImportError:
        return RenderResult(pdf=pdf, message="pypdfium2 not installed, so PNG previews were skipped "
                                             "(pip install pypdfium2). The PDF is ready.")
    return RenderResult(pdf=pdf, pngs=pngs, message=f"rendered {len(pngs)} slide(s)")
