from pathlib import Path

from excelauto.analyzer import WorkbookAnalyzer
from excelauto.document_parser import parse_pdf
from excelauto.planner import InputPlanner


FIXTURES = Path(__file__).resolve().parents[1] / "fixtures"


def test_project_plan_pdf_maps_to_demo_timesheet_fields():
    values = parse_pdf((FIXTURES / "demo_work_plan.pdf").read_bytes())
    assert values["Employee"] == "Alex Morgan"
    assert values["Week of"] == "2026-10-05"
    assert values["Project"] == "Website renewal"
    assert values["Manager"] == "Jamie Lee"

    analysis = WorkbookAnalyzer.from_bytes((FIXTURES / "demo_timesheet.xlsx").read_bytes()).analyze()
    plan = InputPlanner(analysis).create_plan(values)
    mapped = {(change.label, change.value) for change in plan.changes}
    assert ("Employee", "Alex Morgan") in mapped
    assert ("Week of", "2026-10-05") in mapped
    assert ("Project", "Website renewal") in mapped
    assert ("Manager", "Jamie Lee") in mapped
