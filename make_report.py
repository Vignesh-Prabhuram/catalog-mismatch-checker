"""Runs the checker and writes a formatted Excel report."""
import pandas as pd
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter
from mismatch_checker import run

summary, by_type, by_cat, bad, m3, m1 = run()
out = "mismatch_report.xlsx"

with pd.ExcelWriter(out, engine="openpyxl") as xw:
    pd.DataFrame(list(summary.items()), columns=["Metric", "Value"]).to_excel(xw, sheet_name="Summary", index=False)
    by_type.to_excel(xw, sheet_name="By Mismatch Type", index=False)
    by_cat.to_excel(xw, sheet_name="By Category", index=False)
    bad.to_excel(xw, sheet_name="Mismatch Details", index=False)
    m3.to_excel(xw, sheet_name="Missing in 3P", index=False)
    m1.to_excel(xw, sheet_name="Not in 1P", index=False)

    for ws in xw.book.worksheets:
        for c in ws[1]:
            c.font = Font(name="Arial", bold=True, color="FFFFFF")
            c.fill = PatternFill("solid", fgColor="1F4E78")
            c.alignment = Alignment(horizontal="center")
        for row in ws.iter_rows(min_row=2):
            for c in row:
                c.font = Font(name="Arial")
        for i, col in enumerate(ws.columns, 1):
            width = max(len(str(c.value)) if c.value is not None else 0 for c in col)
            ws.column_dimensions[get_column_letter(i)].width = min(max(width + 3, 12), 50)
        ws.freeze_panes = "A2"
    xw.book["Summary"].column_dimensions["A"].width = 30
print("Saved", out)
