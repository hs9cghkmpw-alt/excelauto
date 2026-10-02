from __future__ import annotations

import csv
import json
from io import StringIO


def parse_input(raw: str) -> dict[str, str]:
    """Accept a small JSON object, a one-row CSV, or key: value lines."""
    raw = raw.strip()
    if raw.startswith("{"):
        decoded = json.loads(raw)
        if not isinstance(decoded, dict):
            raise ValueError("JSON input must be an object of labels and values.")
        return {str(key).strip(): str(value).strip() for key, value in decoded.items()}
    values: dict[str, str] = {}
    for line in raw.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        if key.strip() and value.strip():
            values[key.strip()] = value.strip()
    if values:
        return values
    rows = list(csv.DictReader(StringIO(raw)))
    if rows and rows[0]:
        return {str(key).strip(): str(value).strip() for key, value in rows[0].items() if value is not None}
    return {}
