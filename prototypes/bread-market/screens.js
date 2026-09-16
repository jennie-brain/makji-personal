/* MAKJI STOCK · 빵마켓 — 화면 템플릿 (classic script) */
var A = '../../assets/bread-market/';

function ic(p, s, w) {
  s = s || 24; w = w || 1.8;
  return '<svg width="' + s + '" height="' + s + '" viewBox="0 0 24 24" fill="none" ' +
    'stroke="currentColor" stroke-width="' + w + '" stroke-linecap="round" stroke-linejoin="round">' +
    p + '</svg>';
}

var I = {
  bell: '<path d="M18.2 8.6a6.2 6.2 0 1 0-12.4 0c0 6.4-2.6 8.2-2.6 8.2h17.6s-2.6-1.8-2.6-8.2z"/><path d="M13.9 20.4a2.2 2.2 0 0 1-3.8 0"/>',
  search: '<circle cx="11" cy="11" r="7"/><path d="m16.3 16.3 4.4 4.4"/>',
  home: '<path d="M3.6 10.6 12 4.1l8.4 6.5V20a1 1 0 0 1-1 1h-4.6v-6.2H9.2V21H4.6a1 1 0 0 1-1-1z"/>',
  store: '<path d="M4.4 9.6V20a1 1 0 0 0 1 1h13.2a1 1 0 0 0 1-1V9.6"/><path d="M2.8 9.6h18.4l-1.7-4.9a1 1 0 0 0-.94-.67H5.44a1 1 0 0 0-.94.67z"/><path d="M9.6 21v-5.6h4.8V21"/>',
  gift: '<path d="M4.6 11.4h14.8V20a1 1 0 0 1-1 1H5.6a1 1 0 0 1-1-1z"/><path d="M3.2 7.9h17.6v3.5H3.2z"/><path d="M12 7.9V21"/><path d="M12 7.9S9.9 8 8.7 7.4a2 2 0 1 1 1.8-3.5C11.7 4.6 12 7.9 12 7.9z"/><path d="M12 7.9s2.1.1 3.3-.5a2 2 0 1 0-1.8-3.5C12.3 4.6 12 7.9 12 7.9z"/>',
  back: '<path d="m14.6 5.2-7 6.8 7 6.8"/>',
  share: '<path d="M12 15.4V3.6"/><path d="m8.1 7.3 3.9-3.7 3.9 3.7"/><path d="M5.6 12.4V20a1 1 0 0 0 1 1h10.8a1 1 0 0 0 1-1v-7.6"/>',
  ext: '<path d="M14.2 4h5.8v5.8"/><path d="M20 4 10.6 13.4"/><path d="M18 14.6V19a1.6 1.6 0 0 1-1.6 1.6H5A1.6 1.6 0 0 1 3.4 19V7.6A1.6 1.6 0 0 1 5 6h4.4"/>',
  down: '<path d="M12 4.8v13.4"/><path d="m6.6 12.8 5.4 5.4 5.4-5.4"/>',
  chevD: '<path d="m6.4 9.2 5.6 5.4 5.6-5.4"/>',
  trend: '<path d="M3.6 7.6 9.4 13.4l3.4-3.4 7.6 7.2"/><path d="M20.4 12.4v5h-5"/>',
  clock: '<circle cx="12" cy="12" r="8.4"/><path d="M12 7.2v5l3.2 2"/>',
  shield: '<path d="M12 3.2 5.2 5.9v5.3c0 4.2 2.8 7.9 6.8 9.1 4-1.2 6.8-4.9 6.8-9.1V5.9z"/><path d="m9.2 12 2.1 2.1 4-4.2"/>'
};

function statusbar() {
  return '<div class="status"><span>9:41</span><span class="sig">' +
    '<svg width="18" height="12" viewBox="0 0 18 12" fill="currentColor">' +
    '<rect x="0" y="7.6" width="3" height="4.4" rx="1"/><rect x="4.7" y="5.2" width="3" height="6.8" rx="1"/>' +
    '<rect x="9.4" y="2.8" width="3" height="9.2" rx="1"/><rect x="14.1" y="0" width="3" height="12" rx="1"/></svg>' +
    '<svg width="16" height="12" viewBox="0 0 16 12" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round">' +
    '<path d="M1.7 4.3a9.4 9.4 0 0 1 12.6 0"/><path d="M4.3 7.1a5.9 5.9 0 0 1 7.4 0"/><path d="M6.9 9.8a2.4 2.4 0 0 1 2.2 0"/></svg>' +
    '<svg width="25" height="12" viewBox="0 0 25 12" fill="none">' +
    '<rect x=".6" y=".6" width="20.4" height="10.8" rx="3.3" stroke="currentColor" stroke-opacity=".36" stroke-width="1.1"/>' +
    '<rect x="2.3" y="2.3" width="15.4" height="7.4" rx="2.1" fill="currentColor"/>' +
    '<path d="M22.7 4.3c.9.3.9 3.1 0 3.4z" fill="currentColor" fill-opacity=".42"/></svg>' +
    '</span></div>';
}

function wordmark(logoOnly) {
  return '<div class="wordmark"><div class="logo-crop' + (logoOnly ? ' lg' : '') + '">' +
    '<img src="' + A + 'makji-logo.png" alt="MAKJI"></div>' +
    (logoOnly ? '' : '<span class="wm-stock">STOCK</span>') + '</div>';
}

function nav() {
  return '<div class="nav"><div class="nav-row">' +
    '<div class="nav-item">' + ic(I.home, 23) + '<span>홈</span></div>' +
    '<div class="nav-item on">' + ic(I.store, 23) + '<span>빵마켓</span></div>' +
    '<div class="nav-item">' + ic(I.gift, 23) + '<span>이벤트</span></div>' +
    '</div><div class="home-ind"></div></div>';
}

var PRODUCTS = [
  { img: 'morning-roll.png',   name: '제로 무설탕 모닝롤',  now: '3,660', was: '4,500', off: 19 },
  { img: 'english-muffin.png', name: '비건 잉글리시 머핀',  now: '1,260', was: '1,500', off: 16, tone: 1 },
  { img: 'financier.png',      name: '글루텐프리 휘낭시에', now: '3,310', was: '3,800', off: 13 },
  { img: 'scone.png',          name: '글루텐프리 스콘',     now: '3,380', was: '3,800', off: 11 },
  { img: 'castella.png',       name: '막지 ZERO 카스테라',  now: '11,040', was: '12,000', off: 8 }
];

var SCREENS = {};

/* ── 화면 1 · 빵마켓 랜딩 ───────────────────────────── */
SCREENS.home = function () {
  return '<div class="phone">' + statusbar() +
    '<div class="appbar">' + wordmark() +
      '<div class="iconbtn">' + ic(I.bell, 22) + '<i class="dot"></i></div></div>' +
    '<div class="body" style="padding:14px 20px 0">' +
      '<div class="page-tag"><i></i>오늘의 빵마켓</div>' +
      '<div class="eyebrow" style="margin-top:8px">9월 15일 화요일 · 오늘의 빵값</div>' +
      '<h1 class="head" style="margin-top:13px">오늘 더 맛있는<br>가격이 열렸어요</h1>' +
      '<p class="sub" style="margin-top:9px">매일 오전 9시, 막지의 빵값이 새로워져요.</p>' +

      '<div class="hero" style="margin-top:22px">' +
        '<div class="hero-top"><div class="live"><i></i>오늘 가격 공개</div>' +
          '<div class="hero-time">09:00 기준</div></div>' +
        '<div class="hero-name">제로 무설탕 모닝롤</div>' +
        '<div class="hero-price"><b>3,660<span>원</span></b></div>' +
        '<div class="hero-meta"><span class="pill-off">19%</span>' +
          '<span class="hero-was">4,500원</span></div>' +
        '<div class="hero-delta">' + ic(I.down, 15, 2.2) + '어제보다 220원 내려갔어요</div>' +
        '<div class="hero-foot" style="margin-top:16px"><span class="l">다음 가격 공개</span>' +
          '<span class="r">' + ic(I.clock, 14, 2) + '내일 오전 9시</span></div>' +
      '</div>' +

      '<div class="sect" style="margin-top:30px">오늘 가장 많이 내린 빵</div>' +
      '<div class="best" style="margin-top:14px">' +
        '<div class="best-row">' +
          '<div class="best-thumb"><img src="' + A + 'morning-roll.png" alt="담백폭신 막지 제로 무설탕 모닝롤">' +
            '<span class="badge">오늘 -19%</span></div>' +
          '<div class="best-info">' +
            '<div class="best-name">담백폭신 막지 제로<br>무설탕 모닝롤</div>' +
            '<div class="best-price"><span class="off">19%</span>' +
              '<span class="now">3,660원</span><span class="was">4,500원</span></div>' +
          '</div>' +
        '</div>' +
        '<div class="btn-line">오늘 가격 자세히 보기</div>' +
      '</div>' +
    '</div>' + nav() + '</div>';
};

/* ── 화면 2 · 빵 목록 비교 ──────────────────────────── */
SCREENS.list = function () {
  var cards = PRODUCTS.map(function (p) {
    return '<div class="card">' +
      '<div class="card-img"><img class="' + (p.tone ? 'tone' : '') + '" src="' + A + p.img +
        '" alt="' + p.name + '">' +
        '<span class="badge">' + p.off + '%</span></div>' +
      '<div class="card-b"><div class="card-name">' + p.name + '</div>' +
        '<div class="card-p"><span class="now">' + p.now + '원</span>' +
          '<span class="was">' + p.was + '원</span></div></div></div>';
  }).join('');

  return '<div class="phone">' + statusbar() +
    '<div class="appbar">' + wordmark() +
      '<div class="iconbtn">' + ic(I.search, 22) + '</div></div>' +
    '<div class="body" style="padding:10px 20px 0">' +
      '<h2 class="title">오늘의 빵마켓</h2>' +
      '<p class="sub" style="margin-top:6px">오늘만 만날 수 있는 막지 가격이에요.</p>' +
      '<div class="chips" style="margin-top:14px">' +
        '<div class="chip on">전체 <b>5</b></div>' +
        '<div class="chip">오늘의 특가</div>' +
        '<div class="chip">글루텐프리</div>' +
        '<div class="chip">식사빵</div>' +
      '</div>' +
      '<div class="summary" style="margin-top:12px">' +
        '<span class="l">' + ic(I.trend, 16, 2) + '오늘 평균 14% 할인</span>' +
        '<span class="r">할인 높은 순' + ic(I.chevD, 13, 2.2) + '</span></div>' +
      '<div class="grid" style="margin-top:14px">' + cards + '</div>' +
    '</div>' + nav() + '</div>';
};

/* ── 화면 3 · 근거 확인 (상품 상세) ─────────────────── */
SCREENS.detail = function () {
  var it = MARKET[0];
  return '<div class="phone">' + statusbar() +
    '<div class="hero-img" style="height:300px">' +
      '<div class="ph"><img src="' + A + it.img + '" alt="담백폭신 막지 제로 무설탕 모닝롤"></div>' +
      '<div class="ovl"><div class="iconbtn solid">' + ic(I.back, 21) + '</div>' +
        '<div class="iconbtn solid">' + ic(I.share, 20) + '</div></div>' +
      '<div class="pager">1 / 3</div>' +
    '</div>' +
    '<div class="body" style="padding:16px 20px 12px">' +
      '<div class="tags"><span class="tag">' + it.code + '</span>' +
        '<span class="tag">무설탕</span><span class="tag hot">오늘의 빵</span></div>' +
      '<div class="d-name" style="margin-top:11px">담백폭신 막지 제로<br>무설탕 모닝롤</div>' +
      '<div class="d-price" style="margin-top:13px"><span class="off">' + it.off + '%</span>' +
        '<span class="now">' + won(it.now) + '원</span>' +
        '<span class="was">' + won(it.base) + '원</span></div>' +

      '<div class="panel" style="margin-top:18px">' +
        '<div class="panel-h"><span class="t">오늘 가격은 이렇게 열렸어요</span></div>' +
        '<div class="dp">' +
          '<div class="dp-r"><span>정가</span><b>' + won(it.base) + '원</b></div>' +
          '<div class="dp-r"><span>환율이 내려서</span><b class="m">−' + won(it.fx) + '원</b></div>' +
          '<div class="dp-r"><span>많이 찾아봐서</span><b class="m">−' + won(it.se) + '원</b></div>' +
        '</div>' +
        '<div class="dp-t"><span class="l">오늘 가격</span>' +
          '<span class="r"><em>' + it.off + '%</em><b>' + won(it.now) + '원</b></span></div>' +
      '</div>' +

      '<div class="notes" style="margin-top:12px">' +
        '<div class="note">' + ic(I.down, 16, 2.2) + '<span>어제보다 <b>' +
          won(Math.abs(it.diff)) + '원</b> 저렴해요.</span></div>' +
        '<div class="note">' + ic(I.clock, 16, 2) + '<span>오늘 가격은 자정까지 유지돼요.</span></div>' +
      '</div>' +
    '</div>' +
    '<div class="cta-bar"><div class="btn primary">막지몰에서 ' + won(it.now) + '원에 구매하기</div>' +
      '<div class="home-ind"></div></div>' +
    '</div>';
};

/* ── 화면 4 · 막지 자사몰 이동 안내 ─────────────────── */
SCREENS.handoff = function () {
  return '<div class="phone handoff">' + statusbar() +
    '<div class="appbar center"><div class="iconbtn back">' + ic(I.back, 21) + '</div>' +
      wordmark(true) + '</div>' +
    '<div class="body" style="padding:0 20px">' +
      '<div style="display:flex;justify-content:center;margin-top:auto"><div class="ring">' +
        ic(I.ext, 38, 1.7) + '</div></div>' +
      '<h1 class="head" style="text-align:center;margin-top:46px">막지몰로 이동할게요</h1>' +
      '<p class="sub" style="text-align:center;margin-top:11px">선택한 상품과 오늘 가격을 확인하고<br>' +
        '안전하게 주문을 이어갈 수 있어요.</p>' +
      '<div class="sel" style="margin-top:34px">' +
        '<div class="sel-thumb"><img src="' + A + 'morning-roll.png" alt="제로 무설탕 모닝롤"></div>' +
        '<div><div class="sel-lb">선택한 상품</div>' +
          '<div class="sel-name">제로 무설탕 모닝롤</div>' +
          '<div class="sel-price">3,660원</div></div>' +
      '</div>' +
      '<div class="mall" style="margin-top:12px">' +
        '<div class="ic">' + ic(I.shield, 19, 1.9) + '</div>' +
        '<div><div class="t">막지 공식 자사몰 makji.kr</div>' +
          '<div class="d">상품 페이지에서 옵션을 고른 뒤 주문해 주세요.</div></div>' +
      '</div>' +
      '<div style="margin-top:auto">' +
        '<div class="btn primary">막지몰에서 구매 계속하기' + ic(I.ext, 19, 2.1) + '</div>' +
        '<div class="ghost">가격을 더 살펴볼게요</div></div>' +
    '</div>' +
    '<div class="home-ind"></div></div>';
};

/* ── 화면 5 · 빵마켓 · 실시간 차트 ──────────────────── */

/* base 기준가 · now 오늘가 · fx 환율 반영분 · se 검색 반영분
   prev 어제가 · series 최근 14일(9/02~9/15) · hot 많이 찾는 순위 */
var MARKET = [
  { code: 'MOR', desc: '담백하고 폭신한 매일 아침의 무설탕 모닝롤', name: '제로 무설탕 모닝롤', img: 'morning-roll.png', cat: '식사빵',
    tag: ['저당', '식사빵'], base: 4500, now: 3660, off: 19, fx: 535, se: 305,
    prev: 3880, diff: -220, rate: -5.7, hot: 1,
    series: [4420,4300,4350,4210,4260,4100,4290,4180,4020,3880,3540,3760,3880,3660] },
  { code: 'MUF', desc: '통곡물로 구워낸 비건 잉글리시 머핀', name: '비건 잉글리시 머핀', img: 'english-muffin.png', cat: '식사빵', tone: 1,
    tag: ['식사빵'], base: 1500, now: 1260, off: 16, fx: 165, se: 75,
    prev: 1215, diff: 45, rate: 3.7, hot: 3,
    series: [1440,1395,1420,1365,1390,1330,1355,1290,1320,1260,1290,1235,1215,1260] },
  { code: 'FNC', desc: '밀가루 없이 구운 촉촉한 휘낭시에', name: '글루텐프리 휘낭시에', img: 'financier.png', cat: '디저트',
    tag: ['글루텐프리'], base: 3800, now: 3310, off: 13, fx: 340, se: 150,
    prev: 3430, diff: -120, rate: -3.5, hot: 2,
    series: [3720,3660,3690,3600,3640,3550,3580,3500,3540,3460,3490,3400,3430,3310] },
  { code: 'SCN', desc: '겉은 바삭 속은 촉촉한 글루텐프리 스콘', name: '글루텐프리 스콘', img: 'scone.png', cat: '디저트',
    tag: ['글루텐프리'], base: 3800, now: 3380, off: 11, fx: 305, se: 115,
    prev: 3350, diff: 30, rate: 0.9, hot: 5,
    series: [3660,3600,3640,3560,3590,3510,3540,3470,3500,3430,3460,3390,3350,3380] },
  { code: 'CST', desc: '설탕 없이 구운 부드러운 카스테라', name: '막지 ZERO 카스테라', img: 'castella.png', cat: '디저트',
    tag: ['저당'], base: 12000, now: 11040, off: 8, fx: 720, se: 240,
    prev: 11280, diff: -240, rate: -2.1, hot: 4,
    series: [11760,11640,11700,11520,11580,11400,11460,11320,11380,11240,11300,11180,11280,11040] }
];

/* 30일 시세 = 앞 16일(8/17~9/01) + 뒤 14일(9/02~9/15).
   앞 16일은 기준가 대비 비율로 되돌린 값이고, 뒤 14일이 품목별 실제 시리즈다. */
var PRE = [.998,.994,.996,.989,.992,.986,.990,.982,.985,.979,.983,.975,.979,.972,.976,.968];
function series30(it) {
  return PRE.map(function (r) { return Math.round(it.base * r / 10) * 10; }).concat(it.series);
}
function avg(a) {
  var t = a.reduce(function (x, v) { return x + v; }, 0);
  return Math.round(t / a.length / 10) * 10;
}

function won(n) { return String(n).replace(/\B(?=(\d{3})+(?!\d))/g, ','); }

/* 값 배열 → 좌표 배열 */
function pts(vals, w, top, bot, lo, hi) {
  var span = (hi - lo) || 1, n = vals.length - 1;
  return vals.map(function (v, i) {
    return [ (i / n) * w, bot - ((v - lo) / span) * (bot - top) ];
  });
}
function poly(p) { return p.map(function (q) { return q[0].toFixed(1) + ',' + q[1].toFixed(1); }).join(' '); }

/* 이동평균 */
function ma(vals, n) {
  return vals.map(function (v, i) {
    if (i < n - 1) return null;
    var t = 0;
    for (var k = i - n + 1; k <= i; k++) t += vals[k];
    return t / n;
  });
}

/* 히어로 주식차트 — 격자 + 우측 눈금 + 기준가 상한선 + 7일 이동평균 */
function stockChart(it, vals) {
  var W = 334, H = 78, R = 46, PW = W - R, TOP = 7, BOT = 70;
  var lo = Math.floor(Math.min.apply(null, vals) / 100) * 100;
  var hi = Math.ceil(Math.max(Math.max.apply(null, vals), it.base) / 100) * 100;
  var mid = Math.round((lo + hi) / 200) * 100;
  var y = function (v) { return BOT - ((v - lo) / (hi - lo)) * (BOT - TOP); };

  var p = pts(vals, PW, TOP, BOT, lo, hi);
  var m = ma(vals, 7);
  var mp = [];
  m.forEach(function (v, i) { if (v !== null) mp.push([(i / (vals.length - 1)) * PW, y(v)]); });
  var last = p[p.length - 1];

  var grid = [hi, mid, lo].map(function (v) {
    var gy = y(v);
    return '<line x1="0" y1="' + gy.toFixed(1) + '" x2="' + PW + '" y2="' + gy.toFixed(1) + '" ' +
      'stroke="rgba(255,255,255,' + (v === hi ? '.5' : '.18') + ')" stroke-width="1"' +
      (v === hi ? ' stroke-dasharray="4 4"' : '') + '/>' +
      '<text x="' + (PW + 8) + '" y="' + (gy + 3.4).toFixed(1) + '" fill="rgba(255,255,255,' +
      (v === hi ? '.88' : '.6') + ')" font-size="9.5" font-weight="700">' + won(v) + '</text>';
  }).join('');

  return '<div class="bm-chart">' +
    '<svg viewBox="0 0 ' + W + ' ' + H + '" height="' + H + '">' +
      '<defs><linearGradient id="bmfill" x1="0" y1="0" x2="0" y2="1">' +
        '<stop offset="0" stop-color="#fff" stop-opacity=".3"/>' +
        '<stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient></defs>' +
      grid +
      '<polygon points="0,' + BOT + ' ' + poly(p) + ' ' + PW + ',' + BOT + '" fill="url(#bmfill)"/>' +
      '<polyline points="' + poly(mp) + '" fill="none" stroke="rgba(255,255,255,.5)" ' +
        'stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/>' +
      '<polyline points="' + poly(p) + '" fill="none" stroke="#fff" stroke-width="2.2" ' +
        'stroke-linecap="round" stroke-linejoin="round"/>' +
      '<circle cx="' + last[0].toFixed(1) + '" cy="' + last[1].toFixed(1) + '" r="7" fill="#fff" fill-opacity=".3"/>' +
      '<circle cx="' + last[0].toFixed(1) + '" cy="' + last[1].toFixed(1) + '" r="3.8" fill="#fff"/>' +
    '</svg>' +
    '<div class="xax" style="width:' + (PW / W * 100) + '%">' +
      '<span>8/17</span><span>9/01</span><span>오늘</span></div>' +
  '</div>';
}

/* 리스트 행 스파크라인 */
function spark(it) {
  var W = 64, H = 22;
  var lo = Math.min.apply(null, it.series), hi = Math.max.apply(null, it.series);
  var p = pts(it.series, W, 3, H - 3, lo, hi);
  var col = it.series[it.series.length - 1] < it.series[0] ? '#377DA9' : '#ED725D';
  return '<svg width="' + W + '" height="' + H + '" viewBox="0 0 ' + W + ' ' + H + '">' +
    '<polyline points="' + poly(p) + '" fill="none" stroke="' + col + '" stroke-width="1.7" ' +
    'stroke-linecap="round" stroke-linejoin="round"/></svg>';
}

function rateTxt(it) {
  var d = it.diff < 0;
  return '<div class="bm-rate ' + (d ? 'dn' : 'up') + '">' + (d ? '▼' : '▲') +
    ' ' + won(Math.abs(it.diff)) + '원 ' + Math.abs(it.rate).toFixed(1) + '%</div>';
}

function ticker() {
  return '<div class="bm-ticker">' + MARKET.map(function (it) {
    var d = it.diff < 0;
    return '<div class="bm-tk"><span class="c">' + it.code + '</span>' +
      '<span class="v">' + won(it.now) + '</span>' +
      '<span class="r ' + (d ? 'dn' : 'up') + '">' + (d ? '▼' : '▲') +
        Math.abs(it.rate).toFixed(1) + '%</span></div>';
  }).join('') + '</div>';
}

/* ── 오늘의 빵 (가판대) ─────────────────────── */
function todayBox() {
  var it = MARKET[0];               /* 오늘 할인율이 가장 높은 빵 */
  var s30 = series30(it);
  return '<div class="bm-hero">' +

    '<div class="bm-shot">' +
      '<img class="' + (it.tone ? 'tone' : '') + '" src="' + A + it.img + '" alt="' + it.name + '">' +
      '<span class="bm-shot-tag"><i></i>오늘의 빵</span>' +
      '<span class="bm-shot-off">오늘 -' + it.off + '%</span>' +
      '<div class="bm-shot-b"><div class="c">' + it.code + ' · ' + it.cat + '</div>' +
        '<div class="n">' + it.name + '<span class="ch">›</span></div></div>' +
    '</div>' +

    '<div class="bm-mkt">' +
      '<div class="bm-mkt-top">' +
        '<div class="bm-mkt-p"><b>' + won(it.now) + '<span>원</span></b>' +
          '<span class="d">▼ ' + won(Math.abs(it.diff)) + '원 ' + Math.abs(it.rate).toFixed(1) + '%</span></div>' +
        '<div class="bm-tabs"><i>7일</i><i class="on">30일</i><i>3개월</i></div>' +
      '</div>' +
      stockChart(it, s30) +
      '<div class="bm-mkt-l">기준가 ' + won(it.base) + '원 · 7일 평균 ' +
        won(avg(it.series.slice(-7))) + '원 · 30일 평균 ' + won(avg(s30)) + '원</div>' +
    '</div>' +
  '</div>';
}

/* ── 내일의 빵 퀴즈 ─────────────────────────── */
function quizBox() {
  var q = MARKET[1], up = 61;
  return '<div class="bm-quiz">' +
    '<div class="bm-q-top"><span class="bm-q-lb"><i></i>내일의 빵 퀴즈</span>' +
      '<span class="bm-q-c">내일 오전 9시 발표</span></div>' +
    '<div class="bm-q-row">' +
      '<div class="bm-q-th"><img class="' + (q.tone ? 'tone' : '') + '" src="' + A + q.img +
        '" alt="' + q.name + '"></div>' +
      '<div><div class="bm-q-n">' + q.name + '</div>' +
        '<div class="bm-q-p"><span class="v">오늘 ' + won(q.now) + '원</span>' +
          '<span class="r" style="color:var(--up)">▲ ' + q.rate.toFixed(1) + '%</span></div></div>' +
    '</div>' +
    '<div class="bm-vote">' +
      '<div class="bm-v up"><span class="g" style="width:' + up + '%"></span>' +
        '<b>▲ 오를 것 같아요</b><em>' + up + '%</em></div>' +
      '<div class="bm-v dn"><span class="g" style="width:' + (100 - up) + '%"></span>' +
        '<b>▼ 내릴 것 같아요</b><em>' + (100 - up) + '%</em></div>' +
    '</div>' +
    '<div class="bm-q-f">맞히면 할인 쿠폰을 드려요 · 지금까지 1,284명 참여</div>' +
  '</div>';
}

/* ── 실시간 차트 리스트 ─────────────────────── */
function chartList() {
  var rows = MARKET.slice().sort(function (a, b) { return a.rate - b.rate; })
    .map(function (it) {
      return '<div class="bm-row">' +
        '<div class="bm-th"><img class="' + (it.tone ? 'tone' : '') + '" src="' + A + it.img +
          '" alt="' + it.name + '"></div>' +
        '<div class="bm-mid">' +
          '<div class="bm-code">' + it.code + ' <span>· ' + it.tag.join(' · ') + '</span></div>' +
          '<div class="bm-name">' + it.name + '</div>' + spark(it) +
        '</div>' +
        '<div class="bm-rt"><div class="bm-now">' + won(it.now) + '원</div>' +
          '<div class="bm-sub"><span class="off">' + it.off + '%</span>' +
            '<span class="was">' + won(it.base) + '원</span></div>' +
          rateTxt(it) +
        '</div>' +
      '</div>';
    }).join('');

  return '<div class="bm-sect"><span class="t">실시간 차트</span>' +
      '<span class="c">5종 평균 13% 할인</span></div>' +
    '<div class="chips" style="margin-top:13px">' +
      '<div class="chip on">전체 <b>5</b></div>' +
      '<div class="chip">글루텐프리</div>' +
      '<div class="chip">저당</div>' +
      '<div class="chip">식사빵</div>' +
    '</div>' +
    '<div class="bm-sorts">' +
      '<div class="bm-sort on">많이 내린 순</div>' +
      '<div class="bm-sort">많이 오른 순</div>' +
      '<div class="bm-sort">많이 찾는 순</div>' +
    '</div>' +
    '<div class="bm-rows" style="margin-top:14px">' + rows + '</div>';
}

SCREENS.market = function (tall) {
  return '<div class="phone ' + (tall ? 'tall' : 'scroll') + '">' + statusbar() +
    '<div class="appbar">' +
      '<div class="bm-date"><i></i>2026.09.15 (화) · 오전 9시 공개</div>' +
      '<div class="iconbtn">' + ic(I.search, 22) + '</div></div>' +
    '<div class="body">' +
      ticker() +
      '<div style="flex:none;padding:18px 20px 24px">' +
        todayBox() +
        '<div style="margin-top:16px">' + quizBox() + '</div>' +
        '<div style="margin-top:26px">' + chartList() + '</div>' +
      '</div>' +
    '</div>' + nav() + '</div>';
};
