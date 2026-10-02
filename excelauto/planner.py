from __future__ import annotations

import re
from difflib import SequenceMatcher

from .models import InputPlan, PlannedChange, WorkbookAnalysis, WritableField


def _normalise(value: str) -> str:
    return re.sub(r"[\s　_\-()（）/・]", "", value).lower()


class InputPlanner:
    def __init__(self, analysis: WorkbookAnalysis) -> None:
        self.analysis = analysis

    def create_plan(self, values: dict[str, str]) -> InputPlan:
        fields = [field for sheet in self.analysis.sheets for field in sheet.writable_fields]
        changes: list[PlannedChange] = []
        used_cells: set[tuple[str, str]] = set()
        for input_label, value in values.items():
            candidate, confidence = self._best_field(input_label, fields, used_cells)
            if candidate is None or confidence < 0.6:
                continue
            used_cells.add((candidate.sheet, candidate.cell))
            exact = _normalise(input_label) == _normalise(candidate.label)
            changes.append(PlannedChange(f"{candidate.sheet}:{candidate.cell}", candidate.sheet, candidate.cell, candidate.label, value, confidence, "見出しが一致" if exact else "見出しが近似"))
        return InputPlan(changes=changes)

    @staticmethod
    def _best_field(label: str, fields: list[WritableField], used_cells: set[tuple[str, str]]):
        best: WritableField | None = None
        best_score = 0.0
        needle = _normalise(label)
        for field in fields:
            if (field.sheet, field.cell) in used_cells:
                continue
            haystack = _normalise(field.label)
            score = 1.0 if needle == haystack else SequenceMatcher(None, needle, haystack).ratio()
            if needle in haystack or haystack in needle:
                score = max(score, 0.85)
            if score > best_score:
                best, best_score = field, score
        return best, best_score
