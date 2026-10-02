from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class WritableField:
    sheet: str
    cell: str
    label: str
    kind: str

    def as_dict(self) -> dict[str, str]:
        return {"シート": self.sheet, "セル": self.cell, "項目": self.label, "種類": self.kind}


@dataclass(frozen=True)
class SheetAnalysis:
    name: str
    writable_fields: list[WritableField] = field(default_factory=list)
    protected_cells: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class WorkbookAnalysis:
    sheets: list[SheetAnalysis]


@dataclass(frozen=True)
class PlannedChange:
    id: str
    sheet: str
    cell: str
    label: str
    value: str
    confidence: float
    reason: str


@dataclass(frozen=True)
class InputPlan:
    changes: list[PlannedChange]
