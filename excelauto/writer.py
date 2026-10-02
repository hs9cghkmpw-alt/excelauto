from __future__ import annotations

from io import BytesIO

from openpyxl import load_workbook

from .models import PlannedChange


def apply_changes(content: bytes, changes: list[PlannedChange]) -> bytes:
    """Apply pre-reviewed changes without replacing populated or formula cells."""
    workbook = load_workbook(BytesIO(content), data_only=False, keep_vba=False)
    for change in changes:
        sheet = workbook[change.sheet]
        cell = sheet[change.cell]
        if sheet.protection.sheet:
            raise ValueError(f"Protected sheet cannot be changed: {change.sheet}!{change.cell}")
        if cell.data_type == "f" or cell.value is not None:
            raise ValueError(f"Populated or formula cell cannot be changed: {change.sheet}!{change.cell}")
        cell.value = change.value
    output = BytesIO()
    workbook.save(output)
    return output.getvalue()
