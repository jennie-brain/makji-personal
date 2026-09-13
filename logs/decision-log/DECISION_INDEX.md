# 📋 MAKJI STOCK 기획 의사결정 인덱스 (Decision Index)

> 본 문서는 MAKJI 브랜드 RFP 기반 서비스 기획 과정에서 이루어진 **주요 정책, 비즈니스 룰, 아키텍처 의사결정(ADR)**의 공식 누적 색인표입니다.  
> `scripts/auto_log.py` 및 Git Hook에 의해 **자동 동기화**됩니다.

---

## 의사결정 목록 (총 3건)

| ID | 의사결정 제목 | 상태 | 결정 일자 | 결정 주체 |
| :---: | :--- | :---: | :---: | :--- |
| `ADR-001` | [브랜드 슬로건 및 언박싱 감성 여정 정의 ('살 때는 주식처럼, 받을 때는 선물처럼')](./ADR-001_slogan_and_unboxing_flow.md) | 🟢 **Accepted** | 2026-09-11 | MAKJI 기획 총괄 & C-Level 경영진 |
| `ADR-002` | [할인율 산식 가중치 확정 (환율 20% + 검색 18% = 합산 38% 하드캡, KOSPI 이벤트 분리)](./ADR-002_formula_weights_20_18_38.md) | 🟢 **Accepted** | 2026-09-12 | MAKJI 서비스 기획팀, 재무 담당자, Gemini 3.8 Flash 검증 |
| `ADR-003` | [주말 및 공휴일 외환시장 휴장 시 금요일 종가 이월 및 '주말 장외 마켓' 브랜딩 정책](./ADR-003_weekend_carryover_policy.md) | 🟢 **Accepted** | 2026-09-12 | MAKJI 서비스 기획팀 & 플랫폼 개발팀 |

---

## 📌 상태 가이드 (Status Guide)
* 🟢 **Accepted**: 공식 확정 및 프로토타입/PRD 반영 완료
* 🟡 **Proposed**: 검토 중 또는 기업/팀 협의 대기
* ⚪ **Superseded**: 상위 의사결정으로 대체됨
* 🔴 **Rejected**: 리스크 검토 후 반려됨

---
*마지막 동기화: sync_decision_index.py 자동 생성*
