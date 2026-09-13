#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MAKJI Service Planning - Decision Index Synchronizer
Scans all ADR files in logs/decision-log/ and automatically generates DECISION_INDEX.md
"""

import os
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DECISION_DIR = BASE_DIR / "logs" / "decision-log"
INDEX_FILE = DECISION_DIR / "DECISION_INDEX.md"


def parse_frontmatter(content: str) -> dict:
    data = {}
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
    if not match:
        return data
    fm = match.group(1)
    for line in fm.splitlines():
        if ":" in line:
            key, val = line.split(":", 1)
            data[key.strip()] = val.strip().strip('"').strip("'")
    return data


def sync_index():
    DECISION_DIR.mkdir(parents=True, exist_ok=True)
    adr_files = sorted(DECISION_DIR.glob("ADR-*.md"))

    records = []
    for p in adr_files:
        content = p.read_text(encoding="utf-8")
        meta = parse_frontmatter(content)
        adr_id = meta.get("id") or p.name.split("_")[0]
        title = meta.get("title") or p.stem
        date = meta.get("date") or "-"
        status = meta.get("status") or "Accepted"
        decider = meta.get("decider") or "MAKJI Team"
        records.append({
            "id": adr_id,
            "title": title,
            "date": date,
            "status": status,
            "decider": decider,
            "filename": p.name
        })

    # Generate Markdown Table
    table_rows = []
    for r in records:
        badge = "🟢" if r["status"].lower() == "accepted" else ("🟡" if r["status"].lower() == "proposed" else "⚪")
        table_rows.append(
            f"| `{r['id']}` | [{r['title']}](./{r['filename']}) | {badge} **{r['status']}** | {r['date']} | {r['decider']} |"
        )

    if not table_rows:
        rows_str = "| - | 등록된 의사결정이 없습니다 | - | - | - |"
    else:
        rows_str = "\n".join(table_rows)

    content = f"""# 📋 MAKJI STOCK 기획 의사결정 인덱스 (Decision Index)

> 본 문서는 MAKJI 브랜드 RFP 기반 서비스 기획 과정에서 이루어진 **주요 정책, 비즈니스 룰, 아키텍처 의사결정(ADR)**의 공식 누적 색인표입니다.  
> `scripts/auto_log.py` 및 Git Hook에 의해 **자동 동기화**됩니다.

---

## 의사결정 목록 (총 {len(records)}건)

| ID | 의사결정 제목 | 상태 | 결정 일자 | 결정 주체 |
| :---: | :--- | :---: | :---: | :--- |
{rows_str}

---

## 📌 상태 가이드 (Status Guide)
* 🟢 **Accepted**: 공식 확정 및 프로토타입/PRD 반영 완료
* 🟡 **Proposed**: 검토 중 또는 기업/팀 협의 대기
* ⚪ **Superseded**: 상위 의사결정으로 대체됨
* 🔴 **Rejected**: 리스크 검토 후 반려됨

---
*마지막 동기화: {Path(__file__).name} 자동 생성*
"""

    INDEX_FILE.write_text(content, encoding="utf-8")
    print(f"[DECISION-INDEX] Synced {len(records)} ADR records into {INDEX_FILE.name}")


if __name__ == "__main__":
    sync_index()
