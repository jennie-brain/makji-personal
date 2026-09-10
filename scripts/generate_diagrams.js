/**
 * MAKJI Bread Market - Architecture & UML Diagram Generator
 * Uses Playwright to render pixel-perfect high-DPI architecture diagrams.
 */
const fs = require('fs');
const path = require('path');
const { chromium } = require('C:/Users/Administrator/workspace/cardfit/node_modules/playwright');

const OUTPUT_DIR = path.resolve(__dirname, '../docs/architecture');
const ARTIFACT_DIR = 'C:/Users/Administrator/.gemini/antigravity-cli/brain/21628af2-f691-4a6d-8ca5-9cec8e6da9f6';

if (!fs.existsSync(OUTPUT_DIR)) {
  fs.mkdirSync(OUTPUT_DIR, { recursive: true });
}
if (!fs.existsSync(ARTIFACT_DIR)) {
  fs.mkdirSync(ARTIFACT_DIR, { recursive: true });
}

// 1. SYSTEM ARCHITECTURE HTML
const architectureHtml = `<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<title>MAKJI Bread Market - System Architecture</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Pretendard", "Malgun Gothic", sans-serif;
    background: #090D16;
    color: #F1F5F9;
    padding: 36px;
    width: 1680px;
    height: 1180px;
    margin: 0 auto;
    display: flex;
    flex-direction: column;
    gap: 20px;
  }
  
  /* Header */
  .header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid rgba(255,255,255,0.12);
    padding-bottom: 18px;
  }
  .header-left {
    display: flex;
    align-items: center;
    gap: 16px;
  }
  .badge-logo {
    background: linear-gradient(135deg, #F59E0B, #EF4444);
    color: #FFF;
    font-weight: 800;
    font-size: 16px;
    padding: 8px 14px;
    border-radius: 8px;
    letter-spacing: 0.5px;
    box-shadow: 0 4px 12px rgba(245, 158, 11, 0.3);
  }
  .header-title h1 {
    font-size: 26px;
    font-weight: 700;
    color: #FFFFFF;
    letter-spacing: -0.5px;
  }
  .header-title p {
    font-size: 13px;
    color: #94A3B8;
    margin-top: 3px;
  }
  .header-meta {
    display: flex;
    gap: 10px;
  }
  .meta-tag {
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.12);
    padding: 6px 12px;
    border-radius: 6px;
    font-size: 12px;
    color: #CBD5E1;
  }

  /* Grid Layout */
  .main-grid {
    display: grid;
    grid-template-columns: 310px 280px 370px 310px 290px;
    gap: 16px;
    flex: 1;
  }

  /* Layer Box */
  .layer-col {
    background: rgba(15, 23, 42, 0.7);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 14px;
    padding: 16px;
    display: flex;
    flex-direction: column;
    gap: 12px;
    box-shadow: 0 8px 24px rgba(0,0,0,0.4);
    position: relative;
  }
  .layer-col::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    border-top-left-radius: 14px;
    border-top-right-radius: 14px;
  }
  .layer-client::before { background: #38BDF8; }
  .layer-gateway::before { background: #A855F7; }
  .layer-core::before { background: #10B981; }
  .layer-batch::before { background: #F59E0B; }
  .layer-cafe24::before { background: #F43F5E; }

  .layer-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding-bottom: 8px;
    border-bottom: 1px solid rgba(255,255,255,0.08);
  }
  .layer-title {
    font-size: 14px;
    font-weight: 700;
    display: flex;
    align-items: center;
    gap: 8px;
  }
  .layer-badge {
    font-size: 10px;
    padding: 2px 7px;
    border-radius: 4px;
    font-weight: 600;
  }

  /* Cards inside layers */
  .component-card {
    background: rgba(30, 41, 59, 0.6);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 10px;
    padding: 12px;
    display: flex;
    flex-direction: column;
    gap: 6px;
    transition: all 0.2s;
  }
  .card-title {
    font-size: 13px;
    font-weight: 700;
    color: #F8FAFC;
    display: flex;
    align-items: center;
    gap: 6px;
  }
  .card-desc {
    font-size: 11px;
    color: #94A3B8;
    line-height: 1.45;
  }
  .tag-list {
    display: flex;
    flex-wrap: wrap;
    gap: 4px;
    margin-top: 4px;
  }
  .sub-tag {
    font-size: 10px;
    padding: 2px 6px;
    border-radius: 4px;
    background: rgba(255,255,255,0.05);
    color: #94A3B8;
    border: 1px solid rgba(255,255,255,0.06);
  }

  /* Highlight colors */
  .c-blue { color: #38BDF8; }
  .c-purple { color: #C084FC; }
  .c-green { color: #34D399; }
  .c-amber { color: #FBBF24; }
  .c-rose { color: #FB7185; }

  .bg-blue-sub { background: rgba(56, 189, 248, 0.12); color: #38BDF8; border-color: rgba(56, 189, 248, 0.25); }
  .bg-purple-sub { background: rgba(168, 85, 247, 0.12); color: #C084FC; border-color: rgba(168, 85, 247, 0.25); }
  .bg-green-sub { background: rgba(16, 185, 129, 0.12); color: #34D399; border-color: rgba(16, 185, 129, 0.25); }
  .bg-amber-sub { background: rgba(245, 158, 11, 0.12); color: #FBBF24; border-color: rgba(245, 158, 11, 0.25); }
  .bg-rose-sub { background: rgba(244, 63, 94, 0.12); color: #FB7185; border-color: rgba(244, 63, 94, 0.25); }

  /* Bottom storage bar */
  .storage-layer {
    background: rgba(15, 23, 42, 0.85);
    border: 1px solid rgba(99, 102, 241, 0.3);
    border-radius: 12px;
    padding: 14px 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 16px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.3);
  }
  .storage-title-area {
    display: flex;
    align-items: center;
    gap: 12px;
    min-width: 240px;
  }
  .storage-cards {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 12px;
    flex: 1;
  }
  .storage-card {
    background: rgba(30, 41, 59, 0.8);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 8px;
    padding: 8px 12px;
  }

  /* Data flow arrows / connections banner */
  .flow-banner {
    display: flex;
    align-items: center;
    justify-content: space-around;
    background: rgba(255,255,255,0.03);
    border: 1px dashed rgba(255,255,255,0.12);
    border-radius: 8px;
    padding: 8px 16px;
    font-size: 11px;
    color: #94A3B8;
  }
  .flow-item {
    display: flex;
    align-items: center;
    gap: 6px;
  }
  .flow-arrow {
    color: #F59E0B;
    font-weight: 700;
  }
</style>
</head>
<body>

  <!-- Header -->
  <div class="header">
    <div class="header-left">
      <div class="badge-logo">MAKJI ARCH</div>
      <div class="header-title">
        <h1>MAKJI Bread Market 종합 시스템 아키텍처 (System Architecture)</h1>
        <p>실시간 시장 데이터(트렌드·환율·KOSPI) 연동 빵 시세 & Cafe24 커머스 통합 플랫폼</p>
      </div>
    </div>
    <div class="header-meta">
      <div class="meta-tag">스펙 버전: v11.0 MVP</div>
      <div class="meta-tag">기준: 2026.09 (9/9 합의안 반영)</div>
      <div class="meta-tag">백엔드: Cafe24 Admin API v2</div>
    </div>
  </div>

  <!-- Main Architecture 5-Column Grid -->
  <div class="main-grid">

    <!-- 1. Client Layer -->
    <div class="layer-col layer-client">
      <div class="layer-header">
        <div class="layer-title c-blue">
          <span>📱</span> 1. 클라이언트 계층
        </div>
        <div class="layer-badge bg-blue-sub">Mobile Web / SPA</div>
      </div>

      <div class="component-card">
        <div class="card-title">🏠 HOME 화면 뷰</div>
        <div class="card-desc">BREAD-DAQ 날씨/지수, "내일의 빵 예측 [A/B]", 모닝 빵뉴스 피드, 포춘쿠키 운세</div>
        <div class="tag-list">
          <span class="sub-tag">예측 투표</span>
          <span class="sub-tag">실시간 트렌드 뉴스</span>
          <span class="sub-tag">익명 ID</span>
        </div>
      </div>

      <div class="component-card">
        <div class="card-title">📈 Bread Market 뷰</div>
        <div class="card-desc">당일 변동폭 TOP 1 강조 카드, TOP 3/5 랭킹, 10종 빵 시세표 & 토스 멀티뷰 차트 바텀시트</div>
        <div class="tag-list">
          <span class="sub-tag">라인 차트</span>
          <span class="sub-tag">혜택 밴드</span>
          <span class="sub-tag">TOP 10 모달</span>
        </div>
      </div>

      <div class="component-card">
        <div class="card-title">🎮 이벤트 & 미니게임 뷰</div>
        <div class="card-desc">황금 식빵 자르기 게임 (1일 1회 500원 쿠폰 캡), 오븐 갓 구운 빵운세 인터랙션</div>
        <div class="tag-list">
          <span class="sub-tag">1일 1회 마진 방어</span>
          <span class="sub-tag">명예의 전당</span>
        </div>
      </div>

      <div class="component-card">
        <div class="card-title">🛒 장바구니 Direct Drawer</div>
        <div class="card-desc">쿠폰 코드 자동 주입, 투명 영수증, Cafe24 장바구니 슛팅 연계</div>
        <div class="tag-list">
          <span class="sub-tag">원클릭 슛팅</span>
          <span class="sub-tag">500원 할인</span>
        </div>
      </div>

      <div class="component-card">
        <div class="card-title">💾 Local Client Cache</div>
        <div class="card-desc">익명 유저 UUID 발급/보관, 금일 투표 상태 캐시, 게임 플레이 카운트 저장</div>
        <div class="tag-list">
          <span class="sub-tag">LocalStorage</span>
          <span class="sub-tag">SessionCookie</span>
        </div>
      </div>
    </div>

    <!-- 2. API Gateway & BFF Layer -->
    <div class="layer-col layer-gateway">
      <div class="layer-header">
        <div class="layer-title c-purple">
          <span>⚡</span> 2. API 게이트웨이 & BFF
        </div>
        <div class="layer-badge bg-purple-sub">Routing & Security</div>
      </div>

      <div class="component-card">
        <div class="card-title">🛡️ Security & Rate Limit</div>
        <div class="card-desc">DDoS/봇 방지, 투표 어뷰징 차단, 1일 1회 쿠폰 발급 엄격 제한 필터</div>
        <div class="tag-list">
          <span class="sub-tag">IP Limiter</span>
          <span class="sub-tag">UUID Guard</span>
        </div>
      </div>

      <div class="component-card">
        <div class="card-title">🧭 Reverse Proxy / Router</div>
        <div class="card-desc">SSL Termination, 정적 에셋 서빙, API 요청 라우팅 및 로드 밸런싱</div>
        <div class="tag-list">
          <span class="sub-tag">Nginx / Cloudflare</span>
          <span class="sub-tag">CORS</span>
        </div>
      </div>

      <div class="component-card">
        <div class="card-title">🎛️ BFF Controllers</div>
        <div class="card-desc">
          • <code>/api/market/*</code> : 시세 & 차트<br>
          • <code>/api/predict/*</code> : A/B 투표 & 판정<br>
          • <code>/api/event/*</code> : 미니게임 & 쿠폰<br>
          • <code>/api/news/*</code> : 모닝 브리핑 피드
        </div>
        <div class="tag-list">
          <span class="sub-tag">REST API</span>
          <span class="sub-tag">JSON Schema</span>
        </div>
      </div>

      <div class="component-card">
        <div class="card-title">🔑 Anonymous Auth Module</div>
        <div class="card-desc">비회원 브라우저 fingerprint 및 익명 세션 토큰 발행/인증 처리</div>
        <div class="tag-list">
          <span class="sub-tag">Anon UUID</span>
          <span class="sub-tag">JWT Handshake</span>
        </div>
      </div>
    </div>

    <!-- 3. Core Business & Rule Engine Layer -->
    <div class="layer-col layer-core">
      <div class="layer-header">
        <div class="layer-title c-green">
          <span>⚙️</span> 3. 핵심 도메인 & 룰 엔진
        </div>
        <div class="layer-badge bg-green-sub">Business Logic</div>
      </div>

      <div class="component-card" style="border: 1px solid rgba(16,185,129,0.3); background: rgba(16,185,129,0.06);">
        <div class="card-title c-green">🧮 MAKJI 오늘의 빵 시세 산출 엔진</div>
        <div class="card-desc">
          <strong>변동률 산출 공식 (9/9 합의안):</strong><br>
          <code>오늘 변동률 = (트렌드 60% + 코스피 25% + 환율 15%) × 5</code><br>
          • 전날 가격이 아닌 <strong>정가(기본가격) 기준 재계산</strong>
        </div>
        <div class="tag-list">
          <span class="sub-tag bg-green-sub">60:25:15 가중치</span>
          <span class="sub-tag bg-green-sub">×5배 증폭</span>
        </div>
      </div>

      <div class="component-card">
        <div class="card-title">🛡️ 가격대별 안전 캡 & 마진 방어</div>
        <div class="card-desc">
          • <strong>1만원 미만</strong>: 하루 최대 ±10%<br>
          • <strong>1만~2만원</strong>: 하루 최대 ±7%<br>
          • <strong>2만원 이상</strong>: 하루 최대 ±5%<br>
          • <strong>마진 방어선</strong>: 전 제품 마진율 55% 이상 유지
        </div>
        <div class="tag-list">
          <span class="sub-tag">3단계 Safety Cap</span>
          <span class="sub-tag">최저 마진율 방어</span>
        </div>
      </div>

      <div class="component-card">
        <div class="card-title">🎯 내일의 빵 판정기 (Prediction Engine)</div>
        <div class="card-desc">매일 10종 중 랜덤 1종 지정 ➔ 유저 A/B 투표 수합 ➔ 익일 실제 시세 변동과 대조 후 성공 시 500원 할인코드 발행</div>
        <div class="tag-list">
          <span class="sub-tag">랜덤 종목 추첨</span>
          <span class="sub-tag">성공 검증</span>
          <span class="sub-tag">보상 발행</span>
        </div>
      </div>

      <div class="component-card">
        <div class="card-title">📰 사전 승인 마케팅 템플릿 풀 (RFP 준수)</div>
        <div class="card-desc"><strong>AI 무작위 카피 생성 엄격 배제:</strong> 시장 지표 트리거에 따라 사전 승인된 문구 풀에서 템플릿을 선택하여 안전한 모닝 뉴스/운세 생성</div>
        <div class="tag-list">
          <span class="sub-tag">Template Pool</span>
          <span class="sub-tag">브랜드 가이드 준수</span>
        </div>
      </div>
    </div>

    <!-- 4. Batch & External Collector Layer -->
    <div class="layer-col layer-batch">
      <div class="layer-header">
        <div class="layer-title c-amber">
          <span>🔄</span> 4. 데이터 배치 & 수집 계층
        </div>
        <div class="layer-badge bg-amber-sub">Pipeline</div>
      </div>

      <div class="component-card">
        <div class="card-title">⏰ Daily Cron Scheduler</div>
        <div class="card-desc">
          • <strong>08:50</strong> : 기상청 날씨/강수확률 수집<br>
          • <strong>09:00</strong> : 트렌드/환율 수집 & 투표 개장<br>
          • <strong>15:30</strong> : KOSPI 마감 종가 수집 & 투표 마감<br>
          • <strong>00:00</strong> : 데일리 시세 확정 및 Cafe24 동기화
        </div>
        <div class="tag-list">
          <span class="sub-tag">Cron Task</span>
          <span class="sub-tag">타임존 KST</span>
        </div>
      </div>

      <div class="component-card">
        <div class="card-title">🌐 NAVER DataLab 수집기</div>
        <div class="card-desc">10개 빵 품목 키워드별 일간 검색 클릭 지수 수집 및 전일 대비 변동률 산출 (비중 60%)</div>
        <div class="tag-list">
          <span class="sub-tag">Naver API</span>
          <span class="sub-tag">키워드 10종</span>
        </div>
      </div>

      <div class="component-card">
        <div class="card-title">📊 금융위 KOSPI 수집기</div>
        <div class="card-desc">금융공공데이터 포털 KOSPI 종합주가지수 일일 종가 및 등락률 수집 (비중 25%)</div>
        <div class="tag-list">
          <span class="sub-tag">공공데이터 포털</span>
          <span class="sub-tag">KOSPI 지수</span>
        </div>
      </div>

      <div class="component-card">
        <div class="card-title">💱 수출입은행 환율 수집기</div>
        <div class="card-desc">USD/KRW 일일 고시 환율 및 변동폭 수집 (비중 15%)</div>
        <div class="tag-list">
          <span class="sub-tag">수출입은행 API</span>
          <span class="sub-tag">원달러 환율</span>
        </div>
      </div>

      <div class="component-card">
        <div class="card-title">🌧️ 기상청 단기예보 수집기</div>
        <div class="card-desc">서울/수도권 당일 강수 확률 및 날씨 코드 수집 ➔ 모닝 빵뉴스 및 빵운세 테마 연동</div>
        <div class="tag-list">
          <span class="sub-tag">기상청 API</span>
          <span class="sub-tag">날씨 테마</span>
        </div>
      </div>
    </div>

    <!-- 5. E-Commerce / Cafe24 Integration Layer -->
    <div class="layer-col layer-cafe24">
      <div class="layer-header">
        <div class="layer-title c-rose">
          <span>🛍️</span> 5. Cafe24 커머스 연동
        </div>
        <div class="layer-badge bg-rose-sub">Cafe24 Admin API</div>
      </div>

      <div class="component-card">
        <div class="card-title">🔐 Cafe24 OAuth 2.0 Auth</div>
        <div class="card-desc">자사몰(makji.kr) 앱 인증 토큰 갱신 및 Admin API 호출 권한 관리</div>
        <div class="tag-list">
          <span class="sub-tag">Client ID / Secret</span>
          <span class="sub-tag">Token Refresh</span>
        </div>
      </div>

      <div class="component-card">
        <div class="card-title">🏷️ 상품 가격/할인 자동 동기화</div>
        <div class="card-desc">
          <code>/api/v2/admin/products</code><br>
          매일 00:00 확정된 10종 빵 시세 및 할인가를 Cafe24 상품 정보에 배치 일괄 반영
        </div>
        <div class="tag-list">
          <span class="sub-tag">Product API</span>
          <span class="sub-tag">배치 업데이트</span>
        </div>
      </div>

      <div class="component-card">
        <div class="card-title">🎟️ 프로모션 쿠폰 동적 발행</div>
        <div class="card-desc">
          <code>/api/v2/admin/coupons</code><br>
          예측 성공 500원 할인코드 및 미니게임 승리 쿠폰을 실시간 Cafe24 쿠폰으로 생성/지급
        </div>
        <div class="tag-list">
          <span class="sub-tag">Coupon API</span>
          <span class="sub-tag">1일 1회 유효성</span>
        </div>
      </div>

      <div class="component-card">
        <div class="card-title">⚡ Cafe24 Cart Direct Injection</div>
        <div class="card-desc">빵마켓에서 선택한 상품 + 쿠폰 코드를 Cafe24 장바구니로 원클릭 슛팅하여 즉시 주문서 호출</div>
        <div class="tag-list">
          <span class="sub-tag">Cart Payload</span>
          <span class="sub-tag">다이렉트 주문</span>
        </div>
      </div>

      <div class="component-card">
        <div class="card-title">💳 makji.kr 본체 결제 & 주문</div>
        <div class="card-desc">네이버페이/카카오페이/토스페이/신용카드 결제 및 스마트 HACCP 시설 출고</div>
        <div class="tag-list">
          <span class="sub-tag">Cafe24 PG</span>
          <span class="sub-tag">배송 처리</span>
        </div>
      </div>
    </div>

  </div>

  <!-- Persistence Layer (Bottom Bar) -->
  <div class="storage-layer">
    <div class="storage-title-area">
      <span style="font-size:24px;">🗄️</span>
      <div>
        <div style="font-size:14px; font-weight:700; color:#818CF8;">6. 데이터 영속성 및 인메모리 캐시 계층 (Persistence & Cache Layer)</div>
        <div style="font-size:11px; color:#94A3B8;">실시간 고속 조회와 영구 데이터 보관을 분리한 듀얼 스토리지 아키텍처</div>
      </div>
    </div>
    <div class="storage-cards">
      <div class="storage-card">
        <div style="font-size:12px; font-weight:700; color:#F8FAFC;">⚡ Redis In-Memory Cache</div>
        <div style="font-size:11px; color:#94A3B8; margin-top:2px;">당일 빵 시세 캐시, TOP 1/5 랭킹, 실시간 A/B 투표수 카운터, 세션 세마포어</div>
      </div>
      <div class="storage-card">
        <div style="font-size:12px; font-weight:700; color:#F8FAFC;">🍞 Bread Master Database</div>
        <div style="font-size:11px; color:#94A3B8; margin-top:2px;">10종 상품 기본정가, 원가율, 영양성분, 제품 설명, 이미지 에셋 메타데이터</div>
      </div>
      <div class="storage-card">
        <div style="font-size:12px; font-weight:700; color:#F8FAFC;">📈 Market History Storage</div>
        <div style="font-size:11px; color:#94A3B8; margin-top:2px;">일자별 외부 지표(트렌드/주가/환율), 최종 산출 시세, 30일 가격 추이 로그</div>
      </div>
      <div class="storage-card">
        <div style="font-size:12px; font-weight:700; color:#F8FAFC;">📝 User Actions & Coupon Log</div>
        <div style="font-size:11px; color:#94A3B8; margin-top:2px;">익명 유저 예측 투표 로그, 미니게임 점수, 500원 쿠폰 발급/사용 검증 이력</div>
      </div>
    </div>
  </div>

  <!-- Flow Explanation Footer -->
  <div class="flow-banner">
    <div class="flow-item">
      <span>1️⃣ 외부 API 지표 수집 (09:00/15:30)</span>
      <span class="flow-arrow">➔</span>
    </div>
    <div class="flow-item">
      <span>2️⃣ 60:25:15 공식 및 안전 캡 적용 (00:00)</span>
      <span class="flow-arrow">➔</span>
    </div>
    <div class="flow-item">
      <span>3️⃣ 오늘의 빵 시세 DB/Redis 캐싱 & Cafe24 가격 동기화</span>
      <span class="flow-arrow">➔</span>
    </div>
    <div class="flow-item">
      <span>4️⃣ 유저 홈/마켓 탐색 & 내일의 빵 투표/게임</span>
      <span class="flow-arrow">➔</span>
    </div>
    <div class="flow-item">
      <span>5️⃣ 500원 보상 쿠폰 자동 발급 & Cafe24 장바구니 다이렉트 결제</span>
    </div>
  </div>

</body>
</html>
`;

// 2. USE CASE DIAGRAM HTML
const usecaseHtml = `<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<title>MAKJI Bread Market - Use Case Diagram</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Pretendard", "Malgun Gothic", sans-serif;
    background: #0B1120;
    color: #F1F5F9;
    padding: 36px;
    width: 1680px;
    height: 1100px;
    margin: 0 auto;
    display: flex;
    flex-direction: column;
    gap: 20px;
  }
  
  /* Header */
  .header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid rgba(255,255,255,0.12);
    padding-bottom: 16px;
  }
  .header-left {
    display: flex;
    align-items: center;
    gap: 16px;
  }
  .badge-logo {
    background: linear-gradient(135deg, #3B82F6, #10B981);
    color: #FFF;
    font-weight: 800;
    font-size: 15px;
    padding: 8px 14px;
    border-radius: 8px;
    letter-spacing: 0.5px;
  }
  .header-title h1 {
    font-size: 25px;
    font-weight: 700;
    color: #FFFFFF;
  }
  .header-title p {
    font-size: 13px;
    color: #94A3B8;
    margin-top: 3px;
  }

  /* Main Diagram Frame */
  .diagram-container {
    display: grid;
    grid-template-columns: 240px 1fr 240px;
    gap: 24px;
    flex: 1;
    position: relative;
  }

  /* Actor Columns */
  .actor-col {
    display: flex;
    flex-direction: column;
    justify-content: space-around;
    padding: 10px 0;
  }
  .actor-card {
    background: rgba(30, 41, 59, 0.7);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 12px;
    padding: 16px;
    text-align: center;
    box-shadow: 0 4px 16px rgba(0,0,0,0.3);
  }
  .actor-icon {
    font-size: 36px;
    margin-bottom: 8px;
  }
  .actor-name {
    font-size: 15px;
    font-weight: 700;
    color: #F8FAFC;
  }
  .actor-type {
    font-size: 11px;
    color: #94A3B8;
    margin-top: 4px;
  }

  /* System Boundary Box */
  .system-boundary {
    background: rgba(15, 23, 42, 0.65);
    border: 2px dashed rgba(56, 189, 248, 0.35);
    border-radius: 16px;
    padding: 24px 28px;
    display: flex;
    flex-direction: column;
    gap: 16px;
    position: relative;
  }
  .system-label {
    position: absolute;
    top: -14px;
    left: 30px;
    background: #0284C7;
    color: #FFF;
    padding: 4px 16px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 0.5px;
  }

  /* Use Case Groups */
  .uc-groups-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 16px;
    flex: 1;
  }
  .uc-group {
    background: rgba(30, 41, 59, 0.5);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 12px;
    padding: 14px;
    display: flex;
    flex-direction: column;
    gap: 10px;
  }
  .uc-group-title {
    font-size: 13px;
    font-weight: 700;
    color: #94A3B8;
    border-bottom: 1px solid rgba(255,255,255,0.06);
    padding-bottom: 6px;
    display: flex;
    align-items: center;
    gap: 6px;
  }
  .uc-pills {
    display: flex;
    flex-direction: column;
    gap: 8px;
    flex: 1;
  }
  .uc-pill {
    background: rgba(15, 23, 42, 0.8);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 30px;
    padding: 8px 14px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    transition: all 0.2s;
  }
  .uc-pill-left {
    display: flex;
    align-items: center;
    gap: 10px;
  }
  .uc-id {
    font-size: 11px;
    font-weight: 700;
    padding: 2px 7px;
    border-radius: 12px;
    background: rgba(255,255,255,0.08);
    color: #CBD5E1;
  }
  .uc-text {
    font-size: 13px;
    font-weight: 600;
    color: #F8FAFC;
  }
  .uc-rel {
    font-size: 10px;
    color: #94A3B8;
    background: rgba(255,255,255,0.04);
    padding: 2px 8px;
    border-radius: 10px;
    border: 1px solid rgba(255,255,255,0.06);
  }

  /* Specific Pill Accents */
  .pill-blue { border-color: rgba(56, 189, 248, 0.3); }
  .pill-blue .uc-id { background: rgba(56, 189, 248, 0.15); color: #38BDF8; }

  .pill-emerald { border-color: rgba(16, 185, 129, 0.3); }
  .pill-emerald .uc-id { background: rgba(16, 185, 129, 0.15); color: #34D399; }

  .pill-amber { border-color: rgba(245, 158, 11, 0.3); }
  .pill-amber .uc-id { background: rgba(245, 158, 11, 0.15); color: #FBBF24; }

  .pill-rose { border-color: rgba(244, 63, 94, 0.3); }
  .pill-rose .uc-id { background: rgba(244, 63, 94, 0.15); color: #FB7185; }

  /* Legend Footer */
  .footer-legend {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: rgba(15, 23, 42, 0.7);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 10px;
    padding: 10px 20px;
    font-size: 12px;
    color: #94A3B8;
  }
  .legend-items {
    display: flex;
    gap: 20px;
  }
  .legend-item {
    display: flex;
    align-items: center;
    gap: 8px;
  }
  .legend-dot {
    width: 10px;
    height: 10px;
    border-radius: 50%;
  }
</style>
</head>
<body>

  <!-- Header -->
  <div class="header">
    <div class="header-left">
      <div class="badge-logo">UML USE CASE</div>
      <div class="header-title">
        <h1>MAKJI Bread Market 시스템 유스케이스 다이어그램 (Use Case Diagram)</h1>
        <p>액터별 핵심 활동 및 E-Commerce(Cafe24) 전환 연결 흐름 명세</p>
      </div>
    </div>
    <div>
      <span style="font-size:12px; color:#94A3B8; background:rgba(255,255,255,0.06); padding:6px 12px; border-radius:6px;">표준 UML 2.5 명세</span>
    </div>
  </div>

  <!-- Main Diagram -->
  <div class="diagram-container">

    <!-- Left Actors: Users -->
    <div class="actor-col">
      <div class="actor-card" style="border-top: 3px solid #38BDF8;">
        <div class="actor-icon">👤</div>
        <div class="actor-name">일반 방문자</div>
        <div class="actor-type">Guest / Anonymous Session</div>
        <div style="font-size:11px; color:#64748B; margin-top:8px;">SNS 유입, 비회원, 데일리 루틴 탐색 고객</div>
      </div>

      <div class="actor-card" style="border-top: 3px solid #10B981;">
        <div class="actor-icon">🧑‍💻</div>
        <div class="actor-name">구매/단골 회원</div>
        <div class="actor-type">Registered Makji Customer</div>
        <div style="font-size:11px; color:#64748B; margin-top:8px;">자사몰 가입자, 배당 쿠폰 및 정기구독 이용자</div>
      </div>

      <div class="actor-card" style="border-top: 3px solid #C084FC;">
        <div class="actor-icon">👔</div>
        <div class="actor-name">마케팅 / 운영자</div>
        <div class="actor-type">MAKJI Internal Operator</div>
        <div style="font-size:11px; color:#64748B; margin-top:8px;">마진율 방어 감시, 템플릿 카피 풀 관리</div>
      </div>
    </div>

    <!-- Center: System Boundary -->
    <div class="system-boundary">
      <div class="system-label">System Boundary : MAKJI Bread Market Platform</div>

      <div class="uc-groups-grid">

        <!-- Group 1: Search & Market View -->
        <div class="uc-group">
          <div class="uc-group-title">
            <span style="color:#38BDF8;">●</span> [영역 1] 시세 탐색 & 시장 브리핑
          </div>
          <div class="uc-pills">
            <div class="uc-pill pill-blue">
              <div class="uc-pill-left">
                <span class="uc-id">UC-01</span>
                <span class="uc-text">오늘의 10종 빵 시세 및 BREAD-DAQ 지수 확인</span>
              </div>
              <span class="uc-rel">Primary</span>
            </div>
            <div class="uc-pill pill-blue">
              <div class="uc-pill-left">
                <span class="uc-id">UC-02</span>
                <span class="uc-text">당일 변동폭 TOP 1 메인 및 TOP 5 랭킹 조회</span>
              </div>
              <span class="uc-rel">&lt;&lt;extend&gt;&gt;</span>
            </div>
            <div class="uc-pill pill-blue">
              <div class="uc-pill-left">
                <span class="uc-id">UC-03</span>
                <span class="uc-text">토스형 차트(라인 / 정가 대비 혜택 밴드) 확인</span>
              </div>
              <span class="uc-rel">&lt;&lt;include&gt;&gt;</span>
            </div>
            <div class="uc-pill pill-blue">
              <div class="uc-pill-left">
                <span class="uc-id">UC-04</span>
                <span class="uc-text">실시간 모닝 빵뉴스 & 포춘쿠키 운세 열람</span>
              </div>
              <span class="uc-rel">Engagement</span>
            </div>
          </div>
        </div>

        <!-- Group 2: Gamification & Prediction -->
        <div class="uc-group">
          <div class="uc-group-title">
            <span style="color:#10B981;">●</span> [영역 2] 게이미피케이션 & 예측 참여
          </div>
          <div class="uc-pills">
            <div class="uc-pill pill-emerald">
              <div class="uc-pill-left">
                <span class="uc-id">UC-05</span>
                <span class="uc-text">🎯 '내일의 빵' 등락 [A 오른다 / B 내린다] 투표</span>
              </div>
              <span class="uc-rel">Daily Routine</span>
            </div>
            <div class="uc-pill pill-emerald">
              <div class="uc-pill-left">
                <span class="uc-id">UC-06</span>
                <span class="uc-text">익일 투표 성공 검증 및 500원 할인코드 수령</span>
              </div>
              <span class="uc-rel">&lt;&lt;extend&gt;&gt;</span>
            </div>
            <div class="uc-pill pill-emerald">
              <div class="uc-pill-left">
                <span class="uc-id">UC-07</span>
                <span class="uc-text">황금 식빵 자르기 게임 참여 (1일 1회 쿠폰 캡)</span>
              </div>
              <span class="uc-rel">500원 캡</span>
            </div>
            <div class="uc-pill pill-emerald">
              <div class="uc-pill-left">
                <span class="uc-id">UC-08</span>
                <span class="uc-text">오븐 갓 구운 빵운세 뽑기 및 T-처방 확인</span>
              </div>
              <span class="uc-rel">Daily 1회</span>
            </div>
          </div>
        </div>

        <!-- Group 3: Commerce Conversion -->
        <div class="uc-group">
          <div class="uc-group-title">
            <span style="color:#FB7185;">●</span> [영역 3] 커머스 전환 & 카페24 결제
          </div>
          <div class="uc-pills">
            <div class="uc-pill pill-rose">
              <div class="uc-pill-left">
                <span class="uc-id">UC-09</span>
                <span class="uc-text">획득 쿠폰(500원) 자동 바인딩 & 장바구니 슛팅</span>
              </div>
              <span class="uc-rel">&lt;&lt;include&gt;&gt;</span>
            </div>
            <div class="uc-pill pill-rose">
              <div class="uc-pill-left">
                <span class="uc-id">UC-10</span>
                <span class="uc-text">Cafe24 주문서 결제 완료 (네이버/카카오페이)</span>
              </div>
              <span class="uc-rel">Conversion</span>
            </div>
            <div class="uc-pill pill-rose">
              <div class="uc-pill-left">
                <span class="uc-id">UC-11</span>
                <span class="uc-text">구매 후 익일 시세 알림(재방문 트리거) 등록</span>
              </div>
              <span class="uc-rel">Retention</span>
            </div>
          </div>
        </div>

        <!-- Group 4: Automated Batch & System Ops -->
        <div class="uc-group">
          <div class="uc-group-title">
            <span style="color:#FBBF24;">●</span> [영역 4] 시세 산출 & Cafe24 자동 동기화
          </div>
          <div class="uc-pills">
            <div class="uc-pill pill-amber">
              <div class="uc-pill-left">
                <span class="uc-id">UC-12</span>
                <span class="uc-text">외부 4대 지표(트렌드/KOSPI/환율/날씨) 자동 수집</span>
              </div>
              <span class="uc-rel">09:00/15:30</span>
            </div>
            <div class="uc-pill pill-amber">
              <div class="uc-pill-left">
                <span class="uc-id">UC-13</span>
                <span class="uc-text">60:25:15 공식 및 가격대별 상한(±5~10%) 시세 산출</span>
              </div>
              <span class="uc-rel">00:00 Batch</span>
            </div>
            <div class="uc-pill pill-amber">
              <div class="uc-pill-left">
                <span class="uc-id">UC-14</span>
                <span class="uc-text">Cafe24 상품 할인가 & 프로모션 쿠폰 실시간 동기화</span>
              </div>
              <span class="uc-rel">Admin API</span>
            </div>
            <div class="uc-pill pill-amber">
              <div class="uc-pill-left">
                <span class="uc-id">UC-15</span>
                <span class="uc-text">마진율 55% 방어선 검증 및 이상치 Alert</span>
              </div>
              <span class="uc-rel">Safety Guard</span>
            </div>
          </div>
        </div>

      </div>
    </div>

    <!-- Right Actors: External Systems -->
    <div class="actor-col">
      <div class="actor-card" style="border-top: 3px solid #F59E0B;">
        <div class="actor-icon">⏱️</div>
        <div class="actor-name">시스템 스케줄러</div>
        <div class="actor-type">Daily Cron Batch Engine</div>
        <div style="font-size:11px; color:#64748B; margin-top:8px;">08:50 날씨, 09:00 환율, 15:30 주가, 00:00 시세 확정 배치 실행</div>
      </div>

      <div class="actor-card" style="border-top: 3px solid #F43F5E;">
        <div class="actor-icon">🛍️</div>
        <div class="actor-name">Cafe24 커머스</div>
        <div class="actor-type">External E-Commerce Platform</div>
        <div style="font-size:11px; color:#64748B; margin-top:8px;">자사몰 makji.kr 본체, 상품/쿠폰 API, 장바구니/PG 결제 처리</div>
      </div>

      <div class="actor-card" style="border-top: 3px solid #38BDF8;">
        <div class="actor-icon">🌐</div>
        <div class="actor-name">외부 공공 API</div>
        <div class="actor-type">External Data Providers</div>
        <div style="font-size:11px; color:#64748B; margin-top:8px;">네이버 데이터랩, 금융위 KOSPI, 한국수출입은행, 기상청</div>
      </div>
    </div>

  </div>

  <!-- Legend Footer -->
  <div class="footer-legend">
    <div class="legend-items">
      <div class="legend-item"><span class="legend-dot" style="background:#38BDF8;"></span> 시세 탐색 (UC-01~04)</div>
      <div class="legend-item"><span class="legend-dot" style="background:#10B981;"></span> 게이미피케이션 & 예측 (UC-05~08)</div>
      <div class="legend-item"><span class="legend-dot" style="background:#FB7185;"></span> 커머스 전환 (UC-09~11)</div>
      <div class="legend-item"><span class="legend-dot" style="background:#FBBF24;"></span> 자동 배치 & 안전 장치 (UC-12~15)</div>
    </div>
    <div>핵심 비즈니스 목표: <strong>자사몰 DAU 극대화 & 마진 55% 방어 기반 결제 전환</strong></div>
  </div>

</body>
</html>
`;

// 3. SEQUENCE 1: DAILY BATCH PRICING HTML
const seqBatchHtml = `<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<title>MAKJI - Sequence: Daily Batch & Pricing Sync</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Pretendard", "Malgun Gothic", sans-serif;
    background: #0D131F;
    color: #F1F5F9;
    padding: 32px;
    width: 1680px;
    height: 1080px;
    margin: 0 auto;
    display: flex;
    flex-direction: column;
    gap: 16px;
  }
  
  .header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid rgba(255,255,255,0.1);
    padding-bottom: 14px;
  }
  .header h1 { font-size: 23px; font-weight: 700; color: #FFF; }
  .header p { font-size: 13px; color: #94A3B8; margin-top: 2px; }

  /* Sequence Canvas */
  .seq-canvas {
    display: flex;
    flex-direction: column;
    flex: 1;
    background: rgba(15, 23, 42, 0.7);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 14px;
    padding: 20px;
    position: relative;
  }

  /* Lifelines Header */
  .lifelines {
    display: grid;
    grid-template-columns: repeat(7, 1fr);
    gap: 16px;
    text-align: center;
    border-bottom: 2px solid rgba(255,255,255,0.1);
    padding-bottom: 12px;
    margin-bottom: 16px;
  }
  .lifeline-box {
    background: rgba(30, 41, 59, 0.8);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 8px;
    padding: 8px 10px;
  }
  .ll-title { font-size: 13px; font-weight: 700; color: #F8FAFC; }
  .ll-role { font-size: 11px; color: #94A3B8; margin-top: 2px; }

  /* Steps Container */
  .steps-container {
    display: flex;
    flex-direction: column;
    gap: 11px;
    flex: 1;
  }

  .step-row {
    display: grid;
    grid-template-columns: 80px 180px 1fr 240px;
    gap: 16px;
    align-items: center;
    background: rgba(30, 41, 59, 0.4);
    border: 1px solid rgba(255,255,255,0.05);
    border-radius: 8px;
    padding: 8px 14px;
  }
  .step-time {
    font-size: 12px;
    font-weight: 700;
    color: #F59E0B;
    background: rgba(245, 158, 11, 0.1);
    padding: 3px 8px;
    border-radius: 4px;
    text-align: center;
  }
  .step-actors {
    font-size: 12px;
    font-weight: 600;
    color: #CBD5E1;
    display: flex;
    align-items: center;
    gap: 6px;
  }
  .step-msg {
    display: flex;
    flex-direction: column;
    gap: 2px;
  }
  .msg-text {
    font-size: 12.5px;
    font-weight: 600;
    color: #F8FAFC;
  }
  .msg-detail {
    font-size: 11px;
    color: #94A3B8;
  }
  .step-highlight {
    font-size: 11px;
    padding: 4px 10px;
    border-radius: 6px;
    background: rgba(255,255,255,0.05);
    color: #CBD5E1;
    text-align: right;
    border-left: 2px solid #38BDF8;
  }

  /* Phase separator */
  .phase-sep {
    display: flex;
    align-items: center;
    gap: 12px;
    margin: 2px 0;
  }
  .phase-line { flex: 1; height: 1px; background: rgba(255,255,255,0.08); }
  .phase-badge {
    font-size: 11px;
    font-weight: 700;
    padding: 2px 10px;
    border-radius: 12px;
    background: rgba(56, 189, 248, 0.15);
    color: #38BDF8;
    border: 1px solid rgba(56, 189, 248, 0.25);
  }
</style>
</head>
<body>

  <div class="header">
    <div>
      <h1>시퀀스 ① 일일 시장 지표 수집 및 빵 시세 자동 산출 배치 파이프라인</h1>
      <p>외부 4대 지표 수집 ➔ 가중치(60:25:15) 공식 계산 ➔ 3단계 안전 캡 및 마진 검증 ➔ Cafe24 자동 동기화</p>
    </div>
    <div style="font-size:12px; color:#F59E0B; background:rgba(245,158,11,0.1); border:1px solid rgba(245,158,11,0.25); padding:6px 14px; border-radius:6px; font-weight:600;">
      주기: 매일 08:50 ~ 익일 00:00 (KST)
    </div>
  </div>

  <div class="seq-canvas">
    <!-- Lifelines -->
    <div class="lifelines">
      <div class="lifeline-box" style="border-top:3px solid #F59E0B;">
        <div class="ll-title">⏰ Cron Scheduler</div>
        <div class="ll-role">정기 배치 트리거</div>
      </div>
      <div class="lifeline-box" style="border-top:3px solid #38BDF8;">
        <div class="ll-title">🌐 External Collector</div>
        <div class="ll-role">공공/포털 API 수집</div>
      </div>
      <div class="lifeline-box" style="border-top:3px solid #10B981;">
        <div class="ll-title">🧮 Pricing Engine</div>
        <div class="ll-role">60:25:15 시세 산출</div>
      </div>
      <div class="lifeline-box" style="border-top:3px solid #EF4444;">
        <div class="ll-title">🛡️ Safety Guard</div>
        <div class="ll-role">±5~10% 캡 & 마진55%</div>
      </div>
      <div class="lifeline-box" style="border-top:3px solid #C084FC;">
        <div class="ll-title">📰 Template Pool</div>
        <div class="ll-role">사전 승인 카피 셀렉터</div>
      </div>
      <div class="lifeline-box" style="border-top:3px solid #818CF8;">
        <div class="ll-title">💾 DB & Redis</div>
        <div class="ll-role">시세 영구저장/캐시</div>
      </div>
      <div class="lifeline-box" style="border-top:3px solid #F43F5E;">
        <div class="ll-title">🛍️ Cafe24 Admin API</div>
        <div class="ll-role">자사몰 상품/할인 반영</div>
      </div>
    </div>

    <!-- Steps -->
    <div class="steps-container">

      <div class="phase-sep">
        <div class="phase-line"></div>
        <div class="phase-badge">[단계 1: 외부 시장 데이터 다원 수집 (08:50 ~ 15:30)]</div>
        <div class="phase-line"></div>
      </div>

      <div class="step-row">
        <div class="step-time">08:50</div>
        <div class="step-actors">Cron ➔ Collector</div>
        <div class="step-msg">
          <div class="msg-text">기상청 단기예보 API 호출</div>
          <div class="msg-detail">당일 서울/수도권 강수 확률 및 날씨 코드 수집 (비 예보 시 Rainy Day 테마 플래그 활성화)</div>
        </div>
        <div class="step-highlight">기상청 Open API</div>
      </div>

      <div class="step-row">
        <div class="step-time">09:00</div>
        <div class="step-actors">Cron ➔ Collector</div>
        <div class="step-msg">
          <div class="msg-text">네이버 데이터랩 & 한국수출입은행 환율 API 호출</div>
          <div class="msg-detail">10개 빵 키워드 검색량 변동률(비중 60%) 및 USD/KRW 당일 최초 고시 환율(비중 15%) 수집</div>
        </div>
        <div class="step-highlight">Naver DataLab & Eximbank</div>
      </div>

      <div class="step-row">
        <div class="step-time">15:30</div>
        <div class="step-actors">Cron ➔ Collector</div>
        <div class="step-msg">
          <div class="msg-text">금융위원회 공공데이터 KOSPI 종가 수집</div>
          <div class="msg-detail">한국 증시 마감 후 당일 KOSPI 종합지수 등락률 확정치 수집 (비중 25%)</div>
        </div>
        <div class="step-highlight">금융공공데이터 포털</div>
      </div>

      <div class="phase-sep">
        <div class="phase-line"></div>
        <div class="phase-badge">[단계 2: 빵 시세 알고리즘 산출 및 마진 안전장치 검증 (23:50 ~ 00:00)]</div>
        <div class="phase-line"></div>
      </div>

      <div class="step-row">
        <div class="step-time">23:50</div>
        <div class="step-actors">Collector ➔ Pricing</div>
        <div class="step-msg">
          <div class="msg-text">정규화된 3대 시장 지표 변동률 전달 및 공식 계산</div>
          <div class="msg-detail"><code>변동률 = (검색트렌드 변동률×0.6 + KOSPI 변동률×0.25 + 환율 변동률×0.15) × 5</code> 계산</div>
        </div>
        <div class="step-highlight">가중치 60:25:15 & ×5 증폭</div>
      </div>

      <div class="step-row">
        <div class="step-time">23:52</div>
        <div class="step-actors">Pricing ➔ Safety Guard</div>
        <div class="step-msg">
          <div class="msg-text">가격대별 상·하한 캡 적용 & 최저 마진 55% 검증</div>
          <div class="msg-detail">1만원 미만(±10%), 1~2만원(±7%), 2만원 이상(±5%) 클리핑 및 기본 정가 기준 재계산</div>
        </div>
        <div class="step-highlight" style="border-left-color:#EF4444;">10% / 7% / 5% 안전 캡</div>
      </div>

      <div class="step-row">
        <div class="step-time">23:55</div>
        <div class="step-actors">Safety ➔ Template</div>
        <div class="step-msg">
          <div class="msg-text">지표 등락폭 기반 사전 승인 마케팅 카피 자동 매핑 (RFP 원칙 준수)</div>
          <div class="msg-detail">AI 무작위 카피 엄격 배제: 사전 승인된 템플릿 풀에서 모닝 빵뉴스 & 운세 콘텐츠 조합 확정</div>
        </div>
        <div class="step-highlight">Approved Template Pool</div>
      </div>

      <div class="phase-sep">
        <div class="phase-line"></div>
        <div class="phase-badge">[단계 3: DB/Redis 캐싱 및 Cafe24 자사몰 실시간 동기화 (00:00)]</div>
        <div class="phase-line"></div>
      </div>

      <div class="step-row">
        <div class="step-time">23:58</div>
        <div class="step-actors">Pricing ➔ DB & Redis</div>
        <div class="step-msg">
          <div class="msg-text">오늘의 빵 시세 영구 히스토리 기록 및 In-Memory 캐시 갱신</div>
          <div class="msg-detail">Redis에 TOP 1 강조 빵, TOP 5 랭킹, BREAD-DAQ 종합지수 캐시 저장 (TTL 24h)</div>
        </div>
        <div class="step-highlight">PostgreSQL & Redis Cache</div>
      </div>

      <div class="step-row">
        <div class="step-time">00:00</div>
        <div class="step-actors">Engine ➔ Cafe24 API</div>
        <div class="step-msg">
          <div class="msg-text">Cafe24 <code>/api/v2/admin/products</code> 상품 가격/할인가 일괄 동기화</div>
          <div class="msg-detail">OAuth 인증 토큰 갱신 후 10종 상품의 당일 판매가격을 Cafe24 본체에 배치 업데이트 ➔ 200 OK</div>
        </div>
        <div class="step-highlight" style="border-left-color:#F43F5E;">Cafe24 Admin Product Sync</div>
      </div>

    </div>
  </div>

</body>
</html>
`;

// 4. SEQUENCE 2: PREDICTION & CHECKOUT HTML
const seqPredictHtml = `<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<title>MAKJI - Sequence: Prediction & Reward Checkout</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Pretendard", "Malgun Gothic", sans-serif;
    background: #090F1D;
    color: #F1F5F9;
    padding: 32px;
    width: 1680px;
    height: 1080px;
    margin: 0 auto;
    display: flex;
    flex-direction: column;
    gap: 16px;
  }
  
  .header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid rgba(255,255,255,0.1);
    padding-bottom: 14px;
  }
  .header h1 { font-size: 23px; font-weight: 700; color: #FFF; }
  .header p { font-size: 13px; color: #94A3B8; margin-top: 2px; }

  .seq-canvas {
    display: flex;
    flex-direction: column;
    flex: 1;
    background: rgba(15, 23, 42, 0.7);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 14px;
    padding: 20px;
    position: relative;
  }

  .lifelines {
    display: grid;
    grid-template-columns: repeat(6, 1fr);
    gap: 16px;
    text-align: center;
    border-bottom: 2px solid rgba(255,255,255,0.1);
    padding-bottom: 12px;
    margin-bottom: 16px;
  }
  .lifeline-box {
    background: rgba(30, 41, 59, 0.8);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 8px;
    padding: 8px 10px;
  }
  .ll-title { font-size: 13px; font-weight: 700; color: #F8FAFC; }
  .ll-role { font-size: 11px; color: #94A3B8; margin-top: 2px; }

  .steps-container {
    display: flex;
    flex-direction: column;
    gap: 12px;
    flex: 1;
  }

  .step-row {
    display: grid;
    grid-template-columns: 80px 200px 1fr 220px;
    gap: 16px;
    align-items: center;
    background: rgba(30, 41, 59, 0.4);
    border: 1px solid rgba(255,255,255,0.05);
    border-radius: 8px;
    padding: 9px 14px;
  }
  .step-phase-tag {
    font-size: 11px;
    font-weight: 700;
    color: #10B981;
    background: rgba(16, 185, 129, 0.12);
    padding: 3px 8px;
    border-radius: 4px;
    text-align: center;
  }
  .step-actors {
    font-size: 12px;
    font-weight: 600;
    color: #CBD5E1;
  }
  .step-msg {
    display: flex;
    flex-direction: column;
    gap: 2px;
  }
  .msg-text {
    font-size: 13px;
    font-weight: 600;
    color: #F8FAFC;
  }
  .msg-detail {
    font-size: 11px;
    color: #94A3B8;
  }
  .step-highlight {
    font-size: 11px;
    padding: 4px 10px;
    border-radius: 6px;
    background: rgba(255,255,255,0.05);
    color: #CBD5E1;
    text-align: right;
    border-left: 2px solid #10B981;
  }

  .phase-sep {
    display: flex;
    align-items: center;
    gap: 12px;
    margin: 2px 0;
  }
  .phase-line { flex: 1; height: 1px; background: rgba(255,255,255,0.08); }
  .phase-badge {
    font-size: 11px;
    font-weight: 700;
    padding: 2px 10px;
    border-radius: 12px;
    background: rgba(16, 185, 129, 0.15);
    color: #34D399;
    border: 1px solid rgba(16, 185, 129, 0.25);
  }
</style>
</head>
<body>

  <div class="header">
    <div>
      <h1>시퀀스 ② '내일의 빵' 예측 투표 & 성공 보상(쿠폰) 발급 / 장바구니 전환 플로우</h1>
      <p>랜덤 빵 추첨 ➔ A/B 등락 투표 ➔ 익일 실제 시세 판정 ➔ 500원 할인코드 발급 ➔ Cafe24 장바구니 슛팅 및 결제</p>
    </div>
    <div style="font-size:12px; color:#10B981; background:rgba(16,185,129,0.1); border:1px solid rgba(16,185,129,0.25); padding:6px 14px; border-radius:6px; font-weight:600;">
      자사몰 데일리 재방문(DAU) 핵심 플로우
    </div>
  </div>

  <div class="seq-canvas">
    <div class="lifelines">
      <div class="lifeline-box" style="border-top:3px solid #38BDF8;">
        <div class="ll-title">👤 User (Visitor)</div>
        <div class="ll-role">소비자 / 방문자</div>
      </div>
      <div class="lifeline-box" style="border-top:3px solid #38BDF8;">
        <div class="ll-title">📱 Client Web UI</div>
        <div class="ll-role">홈 예측 화면 / 모달</div>
      </div>
      <div class="lifeline-box" style="border-top:3px solid #A855F7;">
        <div class="ll-title">⚡ BFF / API Gateway</div>
        <div class="ll-role">세션 & 요청 라우팅</div>
      </div>
      <div class="lifeline-box" style="border-top:3px solid #10B981;">
        <div class="ll-title">🎯 Prediction Service</div>
        <div class="ll-role">투표 집계 & 성공 판정</div>
      </div>
      <div class="lifeline-box" style="border-top:3px solid #818CF8;">
        <div class="ll-title">💾 DB & Redis Cache</div>
        <div class="ll-role">투표 기록 / 결과 검증</div>
      </div>
      <div class="lifeline-box" style="border-top:3px solid #F43F5E;">
        <div class="ll-title">🛍️ Cafe24 Storefront</div>
        <div class="ll-role">장바구니 슛팅 & 주문 결제</div>
      </div>
    </div>

    <div class="steps-container">

      <div class="phase-sep">
        <div class="phase-line"></div>
        <div class="phase-badge">[Day 1 : 내일의 빵 확인 및 A/B 등락 예측 투표]</div>
        <div class="phase-line"></div>
      </div>

      <div class="step-row">
        <div class="step-phase-tag">Day 1</div>
        <div class="step-actors">User ➔ Client UI</div>
        <div class="step-msg">
          <div class="msg-text">MAKJI STOCK 홈 화면 접속</div>
          <div class="msg-detail">Client UI가 로컬스토리지 익명 식별자(UUID) 확인 후 없으면 신규 생성</div>
        </div>
        <div class="step-highlight">Anonymous UUID Handshake</div>
      </div>

      <div class="step-row">
        <div class="step-phase-tag">Day 1</div>
        <div class="step-actors">Client UI ➔ BFF ➔ Service</div>
        <div class="step-msg">
          <div class="msg-text"><code>GET /api/v1/predict/today</code> 오늘의 랜덤 예측 빵 정보 요청</div>
          <div class="msg-detail">10종 중 당일 선정된 빵 (예: 휘낭시에 3,800원) 및 현재 실시간 A/B 투표 비율 수신</div>
        </div>
        <div class="step-highlight">Redis Daily Target Item</div>
      </div>

      <div class="step-row">
        <div class="step-phase-tag">Day 1</div>
        <div class="step-actors">User ➔ Client UI</div>
        <div class="step-msg">
          <div class="msg-text">"내일 오른다 [ A ]" 선택 버튼 클릭</div>
          <div class="msg-detail">투표 버튼 애니메이션 활성화 및 '투표 완료' UI 즉시 렌더링</div>
        </div>
        <div class="step-highlight">Optimistic UI Update</div>
      </div>

      <div class="step-row">
        <div class="step-phase-tag">Day 1</div>
        <div class="step-actors">Client UI ➔ Service ➔ DB</div>
        <div class="step-msg">
          <div class="msg-text"><code>POST /api/v1/predict/vote</code> { anonId, breadId, choice: 'UP' }</div>
          <div class="msg-detail">중복 투표 방지 체크 후 DB에 투표 레코드 영구 저장, Redis 실시간 카운터 +1 갱신</div>
        </div>
        <div class="step-highlight">Atomic Counter Increment</div>
      </div>

      <div class="phase-sep">
        <div class="phase-line"></div>
        <div class="phase-badge">[Day 2 : 익일 재방문 ➔ 예측 판정 ➔ 500원 쿠폰 획득 & 결제 전환]</div>
        <div class="phase-line"></div>
      </div>

      <div class="step-row">
        <div class="step-phase-tag">Day 2</div>
        <div class="step-actors">User ➔ Client UI</div>
        <div class="step-msg">
          <div class="msg-text">익일 시세 확인을 위해 홈 화면 재방문 (DAU 달성)</div>
          <div class="msg-detail">Client UI가 이전 투표 기록이 있음을 감지하고 결과 확인 팝업 트리거</div>
        </div>
        <div class="step-highlight">Retention Hook Trigger</div>
      </div>

      <div class="step-row">
        <div class="step-phase-tag">Day 2</div>
        <div class="step-actors">Client UI ➔ Service ➔ DB</div>
        <div class="step-msg">
          <div class="msg-text"><code>GET /api/v1/predict/result?anonId=...</code> 예측 성공 검증 요청</div>
          <div class="msg-detail">당일 확정된 휘낭시에 시세(+8.0% 상승)와 유저 선택('UP') 대조 ➔ <strong>예측 성공 판정!</strong></div>
        </div>
        <div class="step-highlight" style="border-left-color:#34D399;">Success Verification</div>
      </div>

      <div class="step-row">
        <div class="step-phase-tag">Day 2</div>
        <div class="step-actors">Service ➔ Cafe24 API</div>
        <div class="step-msg">
          <div class="msg-text">성공 유저 대상 500원 할인코드 발급 (<code>BREAD2026-XXXX</code>)</div>
          <div class="msg-detail">Cafe24 쿠폰 API를 통해 당일 유효한 500원 쿠폰 생성 및 전용 할인 URL 바인딩</div>
        </div>
        <div class="step-highlight">Cafe24 Coupon Generation</div>
      </div>

      <div class="step-row">
        <div class="step-phase-tag">Day 2</div>
        <div class="step-actors">Client UI ➔ User</div>
        <div class="step-msg">
          <div class="msg-text">🎉 "축하합니다! 내일의 빵 예측 성공! 500원 할인 쿠폰 지급" 모달 노출</div>
          <div class="msg-detail">휘낭시에 오늘의 할인가에 500원 추가 쿠폰이 적용된 투명 영수증 표시</div>
        </div>
        <div class="step-highlight">Reward Celebration Modal</div>
      </div>

      <div class="step-row">
        <div class="step-phase-tag">Day 2</div>
        <div class="step-actors">User ➔ Client UI ➔ Cafe24</div>
        <div class="step-msg">
          <div class="msg-text"><strong>[500원 할인받고 바로 구매하기]</strong> 원클릭 클릭</div>
          <div class="msg-detail">Direct Cart Injection: 상품 ID + 수량 + 발급된 500원 쿠폰코드를 Cafe24 주문서로 즉시 전달</div>
        </div>
        <div class="step-highlight" style="border-left-color:#F43F5E;">Cart Direct Injection</div>
      </div>

      <div class="step-row">
        <div class="step-phase-tag">Day 2</div>
        <div class="step-actors">Cafe24 Storefront ➔ User</div>
        <div class="step-msg">
          <div class="msg-text">자사몰 주문 결제창 호출 및 원클릭 간편결제 완료</div>
          <div class="msg-detail">네이버페이/카카오페이/토스페이 결제 ➔ 스마트 HACCP 생산 라인으로 주문 자동 접수</div>
        </div>
        <div class="step-highlight">Order Complete & Fulfillment</div>
      </div>

    </div>
  </div>

</body>
</html>
`;

// 5. SEQUENCE 3: MINIGAME & DIRECT ORDER HTML
const seqGameHtml = `<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<title>MAKJI - Sequence: Minigame & Margin-Guarded Order</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Pretendard", "Malgun Gothic", sans-serif;
    background: #0E101B;
    color: #F1F5F9;
    padding: 32px;
    width: 1680px;
    height: 1080px;
    margin: 0 auto;
    display: flex;
    flex-direction: column;
    gap: 16px;
  }
  
  .header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid rgba(255,255,255,0.1);
    padding-bottom: 14px;
  }
  .header h1 { font-size: 23px; font-weight: 700; color: #FFF; }
  .header p { font-size: 13px; color: #94A3B8; margin-top: 2px; }

  .seq-canvas {
    display: flex;
    flex-direction: column;
    flex: 1;
    background: rgba(15, 23, 42, 0.7);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 14px;
    padding: 20px;
    position: relative;
  }

  .lifelines {
    display: grid;
    grid-template-columns: repeat(6, 1fr);
    gap: 16px;
    text-align: center;
    border-bottom: 2px solid rgba(255,255,255,0.1);
    padding-bottom: 12px;
    margin-bottom: 16px;
  }
  .lifeline-box {
    background: rgba(30, 41, 59, 0.8);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 8px;
    padding: 8px 10px;
  }
  .ll-title { font-size: 13px; font-weight: 700; color: #F8FAFC; }
  .ll-role { font-size: 11px; color: #94A3B8; margin-top: 2px; }

  .steps-container {
    display: flex;
    flex-direction: column;
    gap: 12px;
    flex: 1;
  }

  .step-row {
    display: grid;
    grid-template-columns: 80px 200px 1fr 220px;
    gap: 16px;
    align-items: center;
    background: rgba(30, 41, 59, 0.4);
    border: 1px solid rgba(255,255,255,0.05);
    border-radius: 8px;
    padding: 9px 14px;
  }
  .step-phase-tag {
    font-size: 11px;
    font-weight: 700;
    color: #F43F5E;
    background: rgba(244, 63, 94, 0.12);
    padding: 3px 8px;
    border-radius: 4px;
    text-align: center;
  }
  .step-actors {
    font-size: 12px;
    font-weight: 600;
    color: #CBD5E1;
  }
  .step-msg {
    display: flex;
    flex-direction: column;
    gap: 2px;
  }
  .msg-text {
    font-size: 13px;
    font-weight: 600;
    color: #F8FAFC;
  }
  .msg-detail {
    font-size: 11px;
    color: #94A3B8;
  }
  .step-highlight {
    font-size: 11px;
    padding: 4px 10px;
    border-radius: 6px;
    background: rgba(255,255,255,0.05);
    color: #CBD5E1;
    text-align: right;
    border-left: 2px solid #F43F5E;
  }

  .phase-sep {
    display: flex;
    align-items: center;
    gap: 12px;
    margin: 2px 0;
  }
  .phase-line { flex: 1; height: 1px; background: rgba(255,255,255,0.08); }
  .phase-badge {
    font-size: 11px;
    font-weight: 700;
    padding: 2px 10px;
    border-radius: 12px;
    background: rgba(244, 63, 94, 0.15);
    color: #FB7185;
    border: 1px solid rgba(244, 63, 94, 0.25);
  }
</style>
</head>
<body>

  <div class="header">
    <div>
      <h1>시퀀스 ③ 데일리 미니게임 참여, 1일 1회 마진 방어 쿠폰 발급 및 카페24 결제 플로우</h1>
      <p>황금 식빵 자르기 / 오븐 운세 ➔ 1일 1회 마진 방어 쿠폰 발급 ➔ 2회차 무제한 랭킹전 ➔ Cafe24 결제</p>
    </div>
    <div style="font-size:12px; color:#F43F5E; background:rgba(244,63,94,0.1); border:1px solid rgba(244,63,94,0.25); padding:6px 14px; border-radius:6px; font-weight:600;">
      마진 방어율 55% 이상 준수
    </div>
  </div>

  <div class="seq-canvas">
    <div class="lifelines">
      <div class="lifeline-box" style="border-top:3px solid #38BDF8;">
        <div class="ll-title">👤 User (Player)</div>
        <div class="ll-role">게임 참여자</div>
      </div>
      <div class="lifeline-box" style="border-top:3px solid #F59E0B;">
        <div class="ll-title">🎮 Minigame Canvas</div>
        <div class="ll-role">식빵 자르기 / 운세 UI</div>
      </div>
      <div class="lifeline-box" style="border-top:3px solid #A855F7;">
        <div class="ll-title">⚡ Event Controller</div>
        <div class="ll-role">게임 세션 & 판정</div>
      </div>
      <div class="lifeline-box" style="border-top:3px solid #EF4444;">
        <div class="ll-title">🛡️ Margin & Daily Guard</div>
        <div class="ll-role">1일 1회 500원 캡 방어</div>
      </div>
      <div class="lifeline-box" style="border-top:3px solid #818CF8;">
        <div class="ll-title">🏆 Leaderboard & DB</div>
        <div class="ll-role">TOP 10 명예의 전당</div>
      </div>
      <div class="lifeline-box" style="border-top:3px solid #F43F5E;">
        <div class="ll-title">🛍️ Cafe24 Admin & Cart</div>
        <div class="ll-role">쿠폰 바인딩 & 결제 처리</div>
      </div>
    </div>

    <div class="steps-container">

      <div class="phase-sep">
        <div class="phase-line"></div>
        <div class="phase-badge">[단계 1: 데일리 1회차 게임 플레이 & 500원 쿠폰 획득]</div>
        <div class="phase-line"></div>
      </div>

      <div class="step-row">
        <div class="step-phase-tag">플레이 1</div>
        <div class="step-actors">User ➔ Minigame Canvas</div>
        <div class="step-msg">
          <div class="msg-text">이벤트 탭 진입 ➔ '황금 식빵 5:5 자르기' 시작</div>
          <div class="msg-detail">인터랙티브 나이프 슬라이더 조작을 통해 식빵을 정확히 50:50으로 자르는 미션 수행</div>
        </div>
        <div class="step-highlight">Interactive Bread Cut</div>
      </div>

      <div class="step-row">
        <div class="step-phase-tag">플레이 1</div>
        <div class="step-actors">Canvas ➔ Controller</div>
        <div class="step-msg">
          <div class="msg-text"><code>POST /api/v1/event/game-submit</code> { anonId, cutRatio: 49.8, score: 98 }</div>
          <div class="msg-detail">식빵 절단 정확도 98% 달성 점수 서버 전송</div>
        </div>
        <div class="step-highlight">Score Validation</div>
      </div>

      <div class="step-row">
        <div class="step-phase-tag">마진 검증</div>
        <div class="step-actors">Controller ➔ Daily Guard</div>
        <div class="step-msg">
          <div class="msg-text">금일 쿠폰 발급 이력 조회 (1일 1회 마진 방어 캡)</div>
          <div class="msg-detail">당일 첫 플레이 확인 완료 ➔ 500원 할인 쿠폰 발급 자격 승인 (전체 영업 마진 55% 방어)</div>
        </div>
        <div class="step-highlight" style="border-left-color:#10B981;">Daily Coupon Cap PASS</div>
      </div>

      <div class="step-row">
        <div class="step-phase-tag">쿠폰 발급</div>
        <div class="step-actors">Controller ➔ Cafe24 Admin API</div>
        <div class="step-msg">
          <div class="msg-text">Cafe24 쿠폰 발급 API 호출 ➔ 500원 할인코드 발급</div>
          <div class="msg-detail"><code>/api/v2/admin/coupons</code> 발급된 코드 (<code>GOLDEN-SLICE-500</code>) DB 매핑 완료</div>
        </div>
        <div class="step-highlight">Cafe24 Coupon Issued</div>
      </div>

      <div class="step-row">
        <div class="step-phase-tag">보상 표시</div>
        <div class="step-actors">Canvas ➔ User</div>
        <div class="step-msg">
          <div class="msg-text">🎉 "500원 할인 쿠폰 획득! (오늘의 쿠폰 소진, 추가 플레이는 랭킹 도전용)"</div>
          <div class="msg-detail">쿠폰 번호 저장 및 하단에 [추천 빵 바로 사러가기] 및 [랭킹 재도전] 버튼 제공</div>
        </div>
        <div class="step-highlight">Coupon Modal & CTA</div>
      </div>

      <div class="phase-sep">
        <div class="phase-line"></div>
        <div class="phase-badge">[단계 2: 2회차 이상 반복 플레이 시 ➔ 마진 방어 및 명예의 전당 랭킹전 전환]</div>
        <div class="phase-line"></div>
      </div>

      <div class="step-row">
        <div class="step-phase-tag">플레이 2+</div>
        <div class="step-actors">User ➔ Canvas ➔ Controller</div>
        <div class="step-msg">
          <div class="msg-text">사용자가 더 높은 점수를 위해 2회차 재플레이 실행 (Score: 99.5)</div>
          <div class="msg-detail">Daily Guard가 당일 쿠폰 이미 수령됨을 감지 ➔ <strong>추가 쿠폰 발급 차단 (마진 방어)</strong></div>
        </div>
        <div class="step-highlight" style="border-left-color:#EF4444;">Margin Defense Guard</div>
      </div>

      <div class="step-row">
        <div class="step-phase-tag">랭킹 등록</div>
        <div class="step-actors">Controller ➔ Leaderboard DB</div>
        <div class="step-msg">
          <div class="msg-text">실시간 TOP 10 명예의 전당 랭킹 점수 갱신</div>
          <div class="msg-detail">유저 닉네임 입력 후 상위 10위 캡 유지 및 실시간 소팅 반영</div>
        </div>
        <div class="step-highlight">Redis Sorted Set (ZSET)</div>
      </div>

      <div class="phase-sep">
        <div class="phase-line"></div>
        <div class="phase-badge">[단계 3: 쿠폰 자동 적용 Cafe24 장바구니 슛팅 & 주문 결제]</div>
        <div class="phase-line"></div>
      </div>

      <div class="step-row">
        <div class="step-phase-tag">주문 전환</div>
        <div class="step-actors">User ➔ Canvas ➔ Cafe24 Cart</div>
        <div class="step-msg">
          <div class="msg-text"><strong>[500원 쿠폰 적용하고 즉시 주문하기]</strong> 클릭</div>
          <div class="msg-detail">Cafe24 Direct Cart Injection: 장바구니에 인기 상품(예: ZERO 카스테라) + 500원 쿠폰 바인딩</div>
        </div>
        <div class="step-highlight" style="border-left-color:#F43F5E;">Direct Cart Injection</div>
      </div>

      <div class="step-row">
        <div class="step-phase-tag">결제 완료</div>
        <div class="step-actors">Cafe24 Storefront ➔ User</div>
        <div class="step-msg">
          <div class="msg-text">자사몰 주문서에서 500원 즉시 할인 반영 및 간편결제 승인</div>
          <div class="msg-detail">결제 완료 영수증 출력 및 "내일의 빵 시세 변동 알림 받기" 동의 팝업 제공</div>
        </div>
        <div class="step-highlight">Order Success & Next Loop</div>
      </div>

    </div>
  </div>

</body>
</html>
`;

// Helper: Run Playwright to screenshot HTML files
async function renderAll() {
  console.log('--- Starting Diagram Generation via Playwright ---');
  
  const diagrams = [
    { name: 'architecture_diagram', html: architectureHtml, width: 1680, height: 1180 },
    { name: 'usecase_diagram', html: usecaseHtml, width: 1680, height: 1100 },
    { name: 'sequence_diagram_pricing_batch', html: seqBatchHtml, width: 1680, height: 1080 },
    { name: 'sequence_diagram_prediction_checkout', html: seqPredictHtml, width: 1680, height: 1080 },
    { name: 'sequence_diagram_minigame_order', html: seqGameHtml, width: 1680, height: 1080 }
  ];

  const browser = await chromium.launch({
    executablePath: 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe',
    headless: true
  });

  try {
    for (const d of diagrams) {
      console.log(`Rendering ${d.name}...`);
      const page = await browser.newPage({
        viewport: { width: d.width, height: d.height },
        deviceScaleFactor: 2 // 2x Retina resolution for sharp crisp text
      });

      await page.setContent(d.html, { waitUntil: 'networkidle' });
      await page.waitForTimeout(300);

      const outPath1 = path.join(OUTPUT_DIR, `${d.name}.png`);
      const outPath2 = path.join(ARTIFACT_DIR, `${d.name}.png`);

      await page.screenshot({ path: outPath1, fullPage: true });
      fs.copyFileSync(outPath1, outPath2);

      console.log(`Saved ${d.name}.png -> ${outPath1} and artifact dir`);
      await page.close();
    }

    console.log('--- All 5 Diagrams Rendered Successfully! ---');
  } catch (err) {
    console.error('Render error:', err);
    process.exit(1);
  } finally {
    await browser.close();
  }
}

renderAll();
