# 📜 MAKJI 서비스 기획 - 자동 로깅 시스템 안내 (Logging System)

본 디렉토리(`logs/`)는 MAKJI 브랜드 RFP 기반 서비스 기획 과정에서 이루어지는 **AI 협업 히스토리(AI Log)**와 **비즈니스·아키텍처 의사결정 기록(Decision Log / ADR)**을 체계적으로 누적 및 관리하는 공간입니다.

---

## 📂 디렉토리 구조

```text
logs/
├── README.md                      # 로깅 시스템 가이드 (본 문서)
├── ai-log/                        # AI 모델과의 세션별 기획/분석 기록
│   ├── 20260912_initial_restructuring.md
│   └── git-activity.log           # Git post-commit 훅에 의해 자동 기록되는 커밋 내역
└── decision-log/                  # 비즈니스/정책 아키텍처 의사결정 레코드 (ADR)
    ├── ADR-001_slogan_and_unboxing_flow.md
    ├── ADR-002_formula_weights_20_18_38.md
    ├── ADR-003_weekend_carryover_policy.md
    └── DECISION_INDEX.md          # 모든 ADR을 자동 수집해 갱신하는 누적 색인표
```

---

## 🛠️ 자동화 도구 및 사용법

### 1. `scripts/auto_log.py`
AI 작업 세션 기록 및 의사결정(ADR)을 터미널에서 즉시 표준 템플릿 형태로 생성하는 CLI 유틸리티입니다.

#### A. AI 작업 로그 생성
```bash
python scripts/auto_log.py ai \
  --model "Gemini 3.8 Flash" \
  --topic "할인율 산식 최적화" \
  --summary "환율 20% + 검색 18% = 38% 하드캡 확정 및 검증" \
  --details "경영진 검토 의견서 작성 및 파라미터 백테스팅" \
  --files "docs/02_pricing_engine/FORMULA_SPECIFICATION.md" "docs/03_product_spec/PRD.md"
```

#### B. 의사결정 레코드(ADR) 생성
새로운 ADR 파일이 생성되면 `scripts/sync_decision_index.py`가 자동으로 호출되어 `DECISION_INDEX.md`가 즉시 동기화됩니다.
```bash
python scripts/auto_log.py decision \
  --title "주말 외환시장 휴장 시 금요일 종가 이월 정책" \
  --decider "기획팀 & 경영진" \
  --status "Accepted" \
  --context "토/일요일 외환시장 미운영에 따른 환율 데이터 결손 대응 필요" \
  --decision "금요일 16:30 서울외환시장 종가를 주말 동안 유지하며 '주말 특가'로 리브랜딩" \
  --consequences "시스템 에러 방지 및 주말 방문 고객 신뢰 유지"
```

---

### 2. `scripts/sync_decision_index.py`
`logs/decision-log/ADR-*.md` 파일들의 YAML Frontmatter(`id`, `title`, `date`, `status`, `decider`)를 파싱하여 [`logs/decision-log/DECISION_INDEX.md`](./decision-log/DECISION_INDEX.md) 테이블을 최신 상태로 재작성합니다.

```bash
python scripts/sync_decision_index.py
```

---

### 3. Git Hooks 자동 연동 (`.git/hooks/post-commit`)
`scripts/install_hooks.ps1`을 실행하면 로컬 Git 저장소에 `post-commit` 훅이 등록됩니다.
* 커밋이 발생할 때마다 `sync_decision_index.py`를 자동 실행하여 인덱스를 최신화합니다.
* 커밋 해시와 메시지를 `logs/ai-log/git-activity.log`에 실시간 추가합니다.

---

### 4. GitHub Actions CI 검증 (`.github/workflows/auto-log-verification.yml`)
저장소에 Push되거나 Pull Request가 열릴 때 ADR 인덱스의 정합성을 검증합니다.
