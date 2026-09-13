#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MAKJI Service Planning - Automatic Logging Utility
Supports automatic recording of:
1. AI Interaction Logs (logs/ai-log/)
2. Product & Architecture Decision Records (logs/decision-log/)
"""

import argparse
import datetime
import json
import os
import re
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
LOGS_DIR = BASE_DIR / "logs"
AI_LOG_DIR = LOGS_DIR / "ai-log"
DECISION_LOG_DIR = LOGS_DIR / "decision-log"

AI_LOG_DIR.mkdir(parents=True, exist_ok=True)
DECISION_LOG_DIR.mkdir(parents=True, exist_ok=True)


def slugify(text: str) -> str:
    text = re.sub(r"[^\w\s-]", "", text.lower())
    return re.sub(r"[-\s]+", "_", text).strip("_")


def record_ai_log(model: str, topic: str, summary: str, details: str = "", impacted_files: list = None):
    now = datetime.datetime.now()
    timestamp_str = now.strftime("%Y%m%d_%H%M%S")
    iso_str = now.strftime("%Y-%m-%dT%H:%M:%S+09:00")
    slug = slugify(topic)[:35]
    filename = f"{timestamp_str}_{slug}.md"
    file_path = AI_LOG_DIR / filename

    impacted_str = "\n".join([f"  - {f}" for f in (impacted_files or [])])
    if not impacted_str:
        impacted_str = "  - (지정된 변경 파일 없음)"

    content = f"""---
session_id: "{timestamp_str}"
date: "{iso_str}"
model: "{model}"
topic: "{topic}"
status: "Completed"
impacted_files:
{impacted_str}
---

# 🤖 AI 작업 기록: {topic}

> **작성 일시:** {now.strftime("%Y년 %m월 %d일 %H:%M:%S")}  
> **협업 모델:** `{model}`  
> **프로젝트:** MAKJI 브랜드 RFP 기반 서비스 기획 (MAKJI STOCK)

---

## 1. 세션 목표 및 프롬프트 요약
{summary}

## 2. 주요 도출 결과 및 기획 내용
{details or summary}

## 3. 영향받은 산출물 (Impacted Artifacts)
{impacted_str}

---
*본 문서는 `scripts/auto_log.py`를 통해 자동으로 생성 및 기록되었습니다.*
"""

    file_path.write_text(content, encoding="utf-8")
    print(f"[AI-LOG] Recorded: logs/ai-log/{filename}")
    return file_path


def get_next_adr_id() -> str:
    existing = list(DECISION_LOG_DIR.glob("ADR-*.md"))
    max_num = 0
    for p in existing:
        match = re.search(r"ADR-(\d+)", p.name)
        if match:
            max_num = max(max_num, int(match.group(1)))
    return f"ADR-{max_num + 1:03d}"


def record_decision(title: str, decider: str, status: str, context: str, decision: str, consequences: str):
    now = datetime.datetime.now()
    adr_id = get_next_adr_id()
    slug = slugify(title)[:35]
    filename = f"{adr_id}_{slug}.md"
    file_path = DECISION_LOG_DIR / filename

    content = f"""---
id: "{adr_id}"
title: "{title}"
date: "{now.strftime("%Y-%m-%d")}"
status: "{status}"
decider: "{decider}"
---

# [{adr_id}] {title}

| 메타데이터 | 내용 |
| :--- | :--- |
| **의사결정 ID** | `{adr_id}` |
| **결정 일자** | {now.strftime("%Y년 %m월 %d일")} |
| **상태** | **{status}** (Proposed / Accepted / Rejected / Superseded) |
| **결정 주체** | {decider} |
| **프로젝트** | MAKJI STOCK (브랜드 RFP 연계 서비스 기획) |

---

## 1. 배경 및 문제 정의 (Context)
{context}

---

## 2. 의사결정 사항 (Decision)
{decision}

---

## 3. 기대 효과 및 결과 (Consequences)
{consequences}

---
*본 문서는 `scripts/auto_log.py`에 의해 작성되었습니다.*
"""

    file_path.write_text(content, encoding="utf-8")
    print(f"[DECISION-LOG] Recorded: logs/decision-log/{filename}")

    # Auto sync decision index
    from sync_decision_index import sync_index
    sync_index()
    return file_path


def main():
    parser = argparse.ArgumentParser(description="MAKJI 자동 로깅 도구")
    subparsers = parser.add_subparsers(dest="subcommand", help="로깅 유형 선택")

    # AI log parser
    ai_parser = subparsers.add_parser("ai", help="AI 협업 로그 기록")
    ai_parser.add_argument("--model", default="Gemini 3.8 Flash", help="사용된 AI 모델명")
    ai_parser.add_argument("--topic", required=True, help="작업 주제")
    ai_parser.add_argument("--summary", required=True, help="작업 요약")
    ai_parser.add_argument("--details", default="", help="상세 내용")
    ai_parser.add_argument("--files", nargs="*", default=[], help="영향받은 파일 경로 목록")

    # Decision log parser
    dec_parser = subparsers.add_parser("decision", help="의사결정 기록 (ADR) 생성")
    dec_parser.add_argument("--title", required=True, help="의사결정 제목")
    dec_parser.add_argument("--decider", default="MAKJI 기획팀 & AI", help="결정자")
    dec_parser.add_argument("--status", default="Accepted", help="결정 상태 (Accepted, Proposed 등)")
    dec_parser.add_argument("--context", required=True, help="배경 및 문제 상황")
    dec_parser.add_argument("--decision", required=True, help="결정 내용")
    dec_parser.add_argument("--consequences", required=True, help="결과 및 기대 효과")

    args = parser.parse_args()

    if args.subcommand == "ai":
        record_ai_log(args.model, args.topic, args.summary, args.details, args.files)
    elif args.subcommand == "decision":
        record_decision(args.title, args.decider, args.status, args.context, args.decision, args.consequences)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
