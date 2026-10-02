from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Spacer, Table, TableStyle, Paragraph


def build(path: str) -> None:
    styles = getSampleStyleSheet()
    document = SimpleDocTemplate(path, pagesize=A4, rightMargin=18 * mm, leftMargin=18 * mm, topMargin=18 * mm, bottomMargin=18 * mm)
    story = [Paragraph("Website renewal: weekly work plan", styles["Title"]), Spacer(1, 8 * mm)]
    details = [
        ["Employee:", "Alex Morgan"],
        ["Week of:", "2026-10-05"],
        ["Project:", "Website renewal"],
        ["Manager:", "Jamie Lee"],
    ]
    detail_table = Table(details, colWidths=[38 * mm, 120 * mm])
    detail_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#1F4E78")),
        ("TEXTCOLOR", (0, 0), (0, -1), colors.white),
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#B7C9D6")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.extend([detail_table, Spacer(1, 10 * mm)])
    work = [["Date", "Task", "Planned hours", "Actual hours", "Status", "Notes"],
            ["2026-10-05", "Requirements review", "2.0", "", "Planned", "Kickoff meeting"],
            ["2026-10-06", "Wireframes", "4.0", "", "Planned", "Home/contact"],
            ["2026-10-07", "Copy review", "3.0", "", "Planned", ""],
            ["2026-10-08", "Stakeholder review", "1.5", "", "Planned", ""],
            ["2026-10-09", "Revision plan", "2.5", "", "Planned", ""],]
    work_table = Table(work, colWidths=[28 * mm, 42 * mm, 27 * mm, 27 * mm, 25 * mm, 35 * mm], repeatRows=1)
    work_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1F4E78")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#B7C9D6")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(work_table)
    document.build(story)


if __name__ == "__main__":
    import sys
    build(sys.argv[1])
