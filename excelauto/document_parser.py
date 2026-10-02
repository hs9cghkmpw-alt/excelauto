from __future__ import annotations

from io import BytesIO
import re

from pypdf import PdfReader

from .input_parser import parse_input


def parse_pdf(content: bytes) -> dict[str, str]:
    """Extract labelled values from a text PDF.

    This is intentionally conservative. Scanned PDFs need an OCR adapter, which
    will be added separately instead of silently returning unreliable values.
    """
    reader = PdfReader(BytesIO(content))
    text = "\n".join(page.extract_text() or "" for page in reader.pages)
    if not text.strip():
        raise ValueError("No selectable text found in this PDF. OCR is required for scanned documents.")
    # Table layout extractors often place a label and its adjacent value on
    # separate lines. Rejoin that reliable two-line form before parsing.
    normalised = re.sub(r"(?m)^([^\n:]+):\s*\n([^\n]+)$", r"\1: \2", text)
    return parse_input(normalised)
