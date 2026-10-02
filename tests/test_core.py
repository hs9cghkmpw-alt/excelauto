from io import BytesIO

from openpyxl import Workbook

from excelauto.analyzer import WorkbookAnalyzer
from excelauto.input_parser import parse_input
from excelauto.planner import InputPlanner
from excelauto.writer import apply_changes


def make_workbook() -> bytes:
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Invoice"
    sheet["A1"] = "Customer"
    sheet["A2"] = "Invoice date"
    sheet["B3"] = "Amount"
    sheet["C3"] = "=SUM(C4:C6)"
    buffer = BytesIO()
    workbook.save(buffer)
    return buffer.getvalue()


def test_parser_understands_key_value_text():
    assert parse_input("Customer: Example Inc\nInvoice date: 2026-10-02") == {
        "Customer": "Example Inc",
        "Invoice date": "2026-10-02",
    }


def test_analyzer_and_writer_preserve_formula_cells():
    content = make_workbook()
    analysis = WorkbookAnalyzer.from_bytes(content).analyze()
    fields = {(field.label, field.cell) for field in analysis.sheets[0].writable_fields}
    assert ("Customer", "B1") in fields
    assert ("Invoice date", "B2") in fields
    plan = InputPlanner(analysis).create_plan({"Customer": "Example Inc"})
    result = apply_changes(content, plan.changes)
    updated = WorkbookAnalyzer.from_bytes(result).workbook
    assert updated["Invoice"]["B1"].value == "Example Inc"
    assert updated["Invoice"]["C3"].value == "=SUM(C4:C6)"
