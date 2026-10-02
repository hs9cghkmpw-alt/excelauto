import fs from "node:fs/promises";
import { SpreadsheetFile, Workbook } from "@oai/artifact-tool";

const outputPath = process.argv[2];
if (!outputPath) throw new Error("Usage: node create_demo_workbook.mjs <output.xlsx>");

const workbook = Workbook.create();
const sheet = workbook.worksheets.add("Timesheet");
sheet.showGridLines = false;
sheet.getRange("A2:F2").values = [["Project timesheet", "", "", "", "", ""]];
sheet.getRange("A2:F2").format.font = { name: "Arial", size: 14, bold: true, color: "#1F2937" };
sheet.getRange("A3:F3").format.borders = { bottom: { style: "thin", color: "#94A3B8" } };
sheet.getRange("A5:B8").values = [
  ["Employee", null],
  ["Week of", null],
  ["Project", null],
  ["Manager", null],
];
sheet.getRange("A5:A8").format = {
  fill: "#1F4E78",
  font: { name: "Arial", size: 10, bold: true, color: "#FFFFFF" },
  verticalAlignment: "center",
};
sheet.getRange("B5:B8").format = { fill: "#FFF2CC", font: { name: "Arial", size: 10 }, verticalAlignment: "center" };
sheet.getRange("A10:F10").values = [["Date", "Task", "Planned hours", "Actual hours", "Status", "Notes"]];
sheet.getRange("A10:F10").format = {
  fill: "#1F4E78",
  font: { name: "Arial", size: 10, bold: true, color: "#FFFFFF" },
  horizontalAlignment: "center",
  verticalAlignment: "center",
};
sheet.getRange("A11:F15").format = { font: { name: "Arial", size: 10 }, verticalAlignment: "center" };
sheet.getRange("C11:C15").format.numberFormat = "0.0";
sheet.getRange("D11:D15").format.numberFormat = "0.0";
sheet.getRange("A17:C17").values = [["Totals", "Planned hours", "Actual hours"]];
sheet.getRange("A17:C17").format = { fill: "#D9EAF7", font: { name: "Arial", size: 10, bold: true }, horizontalAlignment: "center" };
sheet.getRange("B18").formulas = [["=SUM(C11:C15)"]];
sheet.getRange("C18").formulas = [["=SUM(D11:D15)"]];
sheet.getRange("B18:C18").format.numberFormat = "0.0";
sheet.getRange("A18:C18").format = { font: { name: "Arial", size: 10, bold: true }, fill: "#EAF2F8" };
sheet.getRange("A5:F18").format.borders = { preset: "outside", style: "thin", color: "#B7C9D6" };
sheet.getRange("A:A").format.columnWidth = 16;
sheet.getRange("B:B").format.columnWidth = 28;
sheet.getRange("C:D").format.columnWidth = 16;
sheet.getRange("E:E").format.columnWidth = 14;
sheet.getRange("F:F").format.columnWidth = 24;
sheet.freezePanes.freezeRows(10);

workbook.recalculate();
const check = await workbook.inspect({ kind: "table", range: "Timesheet!A2:F18", include: "values,formulas", tableMaxRows: 20, tableMaxCols: 6 });
if (!check.ndjson) throw new Error("Workbook inspection returned no result");
const errors = await workbook.inspect({ kind: "match", searchTerm: "#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A|#NUM!", options: { useRegex: true, maxResults: 30 } });
if (errors.ndjson.includes("#REF!") || errors.ndjson.includes("#DIV/0!")) throw new Error("Formula error found");
const preview = await workbook.render({ sheetName: "Timesheet", range: "A2:F18", scale: 1.5, format: "png" });
await fs.mkdir("tmp/demo", { recursive: true });
await fs.writeFile("tmp/demo/timesheet-preview.png", new Uint8Array(await preview.arrayBuffer()));
const xlsx = await SpreadsheetFile.exportXlsx(workbook);
await xlsx.save(outputPath);
