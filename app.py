from __future__ import annotations

import streamlit as st

from excelauto.analyzer import WorkbookAnalyzer
from excelauto.input_parser import parse_input
from excelauto.planner import InputPlanner
from excelauto.writer import apply_changes


st.set_page_config(page_title="Excel Auto", page_icon="📊", layout="wide")
st.title("Excel Auto")
st.caption("初見のExcelに対しても、変更前に候補を確認してから安全に入力します。")

workbook_upload = st.file_uploader("1. Excelファイル (.xlsx)", type=["xlsx"])
source_text = st.text_area(
    "2. 入力データ（文章・CSV・JSON）",
    placeholder="例:\n請求先: 株式会社サンプル\n請求日: 2026/10/02",
    height=180,
)

if workbook_upload is not None:
    workbook_bytes = workbook_upload.getvalue()
    analysis = WorkbookAnalyzer.from_bytes(workbook_bytes).analyze()

    with st.expander("Excelの解析結果", expanded=False):
        for sheet in analysis.sheets:
            st.markdown(f"**{sheet.name}** — 入力候補 {len(sheet.writable_fields)}件 / 保護領域 {len(sheet.protected_cells)}件")
            if sheet.writable_fields:
                st.dataframe([field.as_dict() for field in sheet.writable_fields], use_container_width=True, hide_index=True)

    if source_text.strip():
        source_values = parse_input(source_text)
        plan = InputPlanner(analysis).create_plan(source_values)
        st.subheader("3. 入力候補")
        if not plan.changes:
            st.info("安全に対応付けられる候補がありません。見出しと入力データの項目名を近づけてください。")
        else:
            chosen_ids = []
            for change in plan.changes:
                label = f"{change.sheet}!{change.cell}: {change.label} → {change.value}（{change.reason} / {change.confidence:.0%}）"
                if st.checkbox(label, value=change.confidence >= 0.9, key=change.id):
                    chosen_ids.append(change.id)
            selected_changes = [change for change in plan.changes if change.id in chosen_ids]
            if selected_changes:
                output = apply_changes(workbook_bytes, selected_changes)
                st.download_button("4. 入力済みファイルを作成", data=output, file_name=f"{workbook_upload.name.removesuffix('.xlsx')}_入力済み.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            else:
                st.warning("反映する候補を1つ以上選んでください。")
else:
    st.info("まずExcelファイルを選択してください。元ファイルは変更しません。")
