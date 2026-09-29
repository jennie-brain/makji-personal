"""MAKJI STOCK 기업 대표 보고 덱 (Z-패턴 구조) → 편집 가능한 PPTX.

Google Slides에서는 Drive에 업로드한 뒤 "Google 슬라이드로 열기"로 변환한다.
모든 도형·텍스트·차트(도형으로 그림)는 네이티브 객체라 그대로 편집된다.

Z-패턴 (시선 이동: A → B → 대각선 → C → D)
  A 좌상단  키커 + 헤드라인(메시지)
  B 우상단  핵심 숫자 1개
  대각선    메인 시각자료(차트·다이어그램)
  C 좌하단  근거 / 세부
  D 우하단  So what (결론·행동)
"""
from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_CONNECTOR, MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Emu, Inches, Pt

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "04_presentations" / "막지스톡_기업대표_서비스기획_발표v5.0.pptx"

FONT = "Noto Sans KR"
rgb = lambda h: RGBColor.from_string(h.lstrip("#").upper())
ACC, ACC2, TINT = rgb("4087C7"), rgb("2F6FAD"), rgb("EAF2FA")
INK, INK2, MUTE, LINE, SOFT, WHITE = rgb("111827"), rgb("4B5563"), rgb("9CA3AF"), rgb("E5E7EB"), rgb("F5F7FA"), rgb("FFFFFF")
ORG, ORG2, GRN, GRN2, AMB, AMB2 = rgb("FF7A45"), rgb("FFEEE6"), rgb("10A37F"), rgb("E3F6F0"), rgb("F5B301"), rgb("FFF6DB")
LB = rgb("BFD6EC")

N = 16
prs = Presentation()
prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
BLANK = prs.slide_layouts[6]


# ------------------------------------------------------------------ helpers
def rect(s, x, y, w, h, fill=None, line=None, r=0.12, lw=0.75, shape=None):
    kind = shape or (MSO_SHAPE.ROUNDED_RECTANGLE if r else MSO_SHAPE.RECTANGLE)
    sh = s.shapes.add_shape(kind, Inches(x), Inches(y), Inches(w), Inches(h))
    sh.shadow.inherit = False
    if kind == MSO_SHAPE.ROUNDED_RECTANGLE:
        sh.adjustments[0] = min(0.5, r / min(w, h))
    if fill is None:
        sh.fill.background()
    else:
        sh.fill.solid(); sh.fill.fore_color.rgb = fill
    if line is None:
        sh.line.fill.background()
    else:
        sh.line.color.rgb = line; sh.line.width = Pt(lw)
    return sh


def _runs(p, content, size, bold, color):
    parts = content if isinstance(content, list) else [content]
    for part in parts:
        txt, o = (part, {}) if isinstance(part, str) else part
        r = p.add_run(); r.text = txt
        f = r.font; f.name = FONT; f.size = Pt(o.get("size", size)); f.bold = o.get("bold", bold)
        f.color.rgb = o.get("color", color)


def text(s, x, y, w, h, content, size=12, bold=False, color=INK, align="l", anchor="t", lsp=1.18, gap=0):
    tb = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame; tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = {"t": MSO_ANCHOR.TOP, "m": MSO_ANCHOR.MIDDLE, "b": MSO_ANCHOR.BOTTOM}[anchor]
    paras = content if isinstance(content, list) and content and isinstance(content[0], (list, str)) and not (
        isinstance(content[0], tuple)) else [content]
    if isinstance(content, str):
        paras = content.split("\n")
    for i, para in enumerate(paras):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = {"l": PP_ALIGN.LEFT, "c": PP_ALIGN.CENTER, "r": PP_ALIGN.RIGHT}[align]
        p.line_spacing = lsp
        if i: p.space_before = Pt(gap)
        _runs(p, para, size, bold, color)
    return tb


def tag(s, x, y, txt, fill=TINT, color=ACC2, w=None, size=9):
    w = w or (0.16 + 0.135 * len(txt) * size / 9)
    rect(s, x, y, w, 0.24, fill, r=0.12)
    text(s, x, y, w, 0.24, txt, size=size, bold=True, color=color, align="c", anchor="m")
    return w


def line(s, x1, y1, x2, y2, color=LINE, w=1.0, dash=False):
    c = s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(x1), Inches(y1), Inches(x2), Inches(y2))
    c.line.color.rgb = color; c.line.width = Pt(w)
    from pptx.oxml.ns import qn
    from lxml import etree
    sp = c._element.spPr
    if sp.find(qn("a:effectLst")) is None:
        sp.append(etree.SubElement(sp, qn("a:effectLst")))
    if dash:
        c.line.dash_style = 4
    return c


def dot(s, x, y, d, fill):
    return rect(s, x, y, d, d, fill, r=0, shape=MSO_SHAPE.OVAL)


def arrow(s, x, y, w=0.3, h=0.3, fill=ACC):
    return rect(s, x, y, w, h, fill, r=0, shape=MSO_SHAPE.RIGHT_ARROW)


def table(s, x, y, colw, rowh, rows, size=10, hl=None, head=True, align0="l", aligns=None):
    yy = y
    for ri, row in enumerate(rows):
        if hl is not None and ri == hl:
            rect(s, x, yy, sum(colw), rowh, TINT, r=0)
        xx = x
        for ci, cell in enumerate(row):
            is_head = head and ri == 0
            text(s, xx + 0.06, yy, colw[ci] - 0.12, rowh, cell, size=size - 1 if is_head else size,
                 bold=is_head or (hl is not None and ri == hl), color=MUTE if is_head else INK,
                 align=(aligns[ci] if aligns else (align0 if ci == 0 else "r")), anchor="m")
            xx += colw[ci]
        line(s, x, yy + rowh, x + sum(colw), yy + rowh, INK if (head and ri == 0) else LINE, 1.25 if (head and ri == 0) else 0.6)
        yy += rowh



# ------------------------------------------------------------------ Z-flow frame
# 시선: 좌상단 헤드라인 → 중앙 시각자료(숫자는 차트 안에) → 우하단 결론 한 줄.
# 카드로 구역을 채우지 않고 여백을 남긴다.
L, RIGHT = 0.9, 12.43


def frame(idx, kicker, headline, sowhat, source=None, notes=""):
    s = prs.slides.add_slide(BLANK)
    text(s, L, 0.62, 8, 0.3, kicker, size=11, bold=True, color=ACC2)
    text(s, L, 0.95, 9.5, 1.2, headline, size=27, bold=True, color=INK, lsp=1.15)
    if sowhat:
        rect(s, RIGHT - 0.42, 6.42, 0.42, 0.045, ACC, r=0)
        text(s, 5.2, 6.55, RIGHT - 5.2, 0.4, sowhat, size=14, bold=True, color=ACC2, align="r")
    if source:
        text(s, L, 7.02, 10.6, 0.3, source, size=7.5, color=MUTE, lsp=1.1)
    text(s, 11.0, 7.05, RIGHT - 11.0, 0.2, "%02d / %d" % (len(prs.slides), N), size=8.5, color=MUTE, align="r")
    if notes:
        s.notes_slide.notes_text_frame.text = notes
    return s


def pill(s, x, y, w, txt, fill=ACC, color=WHITE, size=13, h=0.36):
    rect(s, x, y, w, h, fill, r=0.18)
    text(s, x, y, w, h, txt, size=size, bold=True, color=color, align="c", anchor="m")


def caption(s, x, y, w, txt):
    text(s, x, y, w, 0.25, txt, size=11, color=MUTE)


def bar_chart(s, x, base, maxh, vmax, data, bw, gap, lab=15):
    for i, (cat, sub, v, c, lb) in enumerate(data):
        bx = x + i * (bw + gap); h = v / vmax * maxh
        rect(s, bx, base - h, bw, h, c, r=0.05)
        text(s, bx - 0.3, base - h - 0.36, bw + 0.6, 0.3, lb, size=lab, bold=True, align="c")
        text(s, bx - 0.3, base + 0.1, bw + 0.6, 0.25, cat, size=12, bold=True, align="c")
        if sub:
            text(s, bx - 0.3, base + 0.36, bw + 0.6, 0.22, sub, size=9.5, color=MUTE, align="c")
    line(s, x - 0.3, base, x + len(data) * (bw + gap) - gap + 0.3, base, LINE, 1.5)


# ------------------------------------------------------------------ 1 표지
s = prs.slides.add_slide(BLANK)
rect(s, 0, 0, 0.22, 7.5, ACC, r=0)
text(s, 0.9, 0.55, 4, 0.3, [[("●  ", {"color": ACC}), ("MAKJI", {"bold": True})]], size=13, bold=True, color=INK)
text(s, 7.5, 0.55, 4.93, 0.3, "BUSINESS PROPOSAL 2026", size=10.5, bold=True, color=MUTE, align="r")
text(s, 0.9, 2.3, 8, 2.6, [[("MAKJI", {})], [("STOCK", {"color": ACC})]], size=80, bold=True, color=INK, lsp=0.95)
text(s, 0.9, 5.0, 9, 0.9, ["웰니스 베이커리 막지의 B2C 확장 —", "매일 두 번 움직이는 빵값으로 자사몰의 방문과 구매를 만듭니다."], size=16, color=INK2, lsp=1.4)
text(s, 0.9, 6.75, 6, 0.3, "빵값연구소  |  기업 대표 보고", size=11, color=INK2)
text(s, 6.9, 6.75, 5.53, 0.3, "2026.09", size=11, color=INK2, align="r")
s.notes_slide.notes_text_frame.text = ("[30초] 오늘 말씀드릴 것은 세 가지입니다. 시장에 기회가 있고, 우리는 그 기회를 ‘가격’으로 잡으려 하며, "
                                       "그 방식이 마진을 지킨다는 것입니다. 마지막에 세 가지 요청을 드리겠습니다.")

# ------------------------------------------------------------------ 2 시장 기회
s = frame(2, "시장 기회", ["온라인 베이커리 시장은 4년 만에 2배 가까이 커졌고,", "유사 업체도 빠르게 성장하고 있습니다."],
          "성장하는 온라인 시장 — 이 수요를 어떻게 가져올지가 우리의 과제입니다.",
          source="출처: aT 온라인 베이커리 시장 규모(매일경제 2026.03.23) · 널담 2025 매출 약 330억, 2026 목표 800억(플래텀·메트로서울 2026.01) · 2024는 역산 추정, 2023은 내부 시장분석 · 널담 매출에는 오프라인 유통 포함",
          notes="[1분] 온라인 베이커리 시장은 2021년 3,200억에서 2025년 6,250억으로 커졌습니다(연평균 +18%). 신세계푸드의 온라인 베이커리 매출도 2023년 255억에서 2025년 850억으로 3.3배가 됐습니다. "
                "같은 시장의 저당·고단백 브랜드 널담은 2025년 매출이 전년 대비 104% 늘었습니다. 온라인 수요는 커지고 있고, 유사 업체는 이미 그 수요를 가져가고 있습니다.")
caption(s, 1.1, 2.55, 5, "국내 온라인 베이커리 시장 (억원)")
bar_chart(s, 1.3, 5.75, 2.55, 6600, [("2021", "", 3200, LB, "3,200"), ("2024", "", 5400, LB, "5,400"), ("2025", "", 6250, ACC, "6,250")], 1.2, 0.55)
pill(s, 1.3, 2.95, 1.5, "+95%")
text(s, 2.9, 2.95, 2.5, 0.36, "2021 → 2025", size=11, color=MUTE, anchor="m")
caption(s, 7.3, 2.55, 5, "널담 연 매출 (억원)")
bar_chart(s, 7.5, 5.75, 2.55, 830, [("2023", "", 145.6, ACC, "145.6"), ("2024", "역산", 162, LB, "≈162"), ("2025", "", 330, ACC, "≈330"), ("2026", "목표", 800, LB, "800")], 0.95, 0.5, lab=14)
pill(s, 7.5, 2.95, 1.5, "+104%")
text(s, 9.1, 2.95, 2.5, 0.36, "2025 전년 대비", size=11, color=MUTE, anchor="m")

# ------------------------------------------------------------------ 3 방향 · 시점 불일치
s = frame(3, "우리의 방향", ["웰니스 베이커리 막지는 B2C 자사몰로 확장하고 있는데,", "방문하는 시간과 구매하는 시간이 어긋납니다."],
          "관심이 생긴 순간부터 구매까지, 한 걸음에 이어지는 구조가 필요합니다.",
          source="출처: 막지 자사몰 5월 시간별 분석 (로그인 90회 · 결제금액 기준, 단일상품 막지 ZERO 카스테라)",
          notes="[1분] 막지는 저당·무설탕·글루텐프리 웰니스 베이커리이고, B2B 공급으로 제품력을 검증했습니다. 이제 자사몰(B2C)로 확장 중입니다. "
                "그런데 5월 자사몰 데이터를 보면 로그인은 오전 8~10시에 25.6%가 몰렸는데 결제금액은 8.0%뿐이고, 저녁 20~24시에는 로그인 20.0%인데 결제금액이 28.4%입니다. "
                "아침에 둘러보고 저녁에 삽니다. 관심이 생긴 순간과 구매하는 순간 사이가 벌어져 있습니다.")
text(s, L, 2.3, 8, 0.3, [[("B2B 제품 공급", {"color": MUTE}), ("   →   ", {"color": ACC, "bold": True}), ("B2C 자사몰 확장", {"color": ACC2, "bold": True})]], size=13)
text(s, 9.3, 2.3, 3.13, 0.25, "■ 로그인 비중", size=10.5, color=ACC, align="r")
text(s, 9.3, 2.55, 3.13, 0.25, "■ 결제금액 비중", size=10.5, color=ORG, align="r")
base = 5.55; mh = 2.4
for gi, (nm, sub, a, b) in enumerate([("오전 8~10시", "아침에 둘러보고", 25.6, 8.0), ("저녁 20~24시", "저녁에 삽니다", 20.0, 28.4)]):
    x = 2.2 + gi * 5.3
    for j, (v, c) in enumerate([(a, ACC), (b, ORG)]):
        h = v / 30 * mh
        rect(s, x + j * 1.5, base - h, 1.25, h, c, r=0.05)
        text(s, x + j * 1.5 - 0.2, base - h - 0.45, 1.65, 0.4, "%s%%" % v, size=20, bold=True, align="c")
    text(s, x - 0.2, base + 0.12, 3.15, 0.3, nm, size=13, bold=True, align="c")
    text(s, x - 0.2, base + 0.44, 3.15, 0.3, sub, size=11.5, color=MUTE, align="c")
line(s, L, base, RIGHT, base, LINE, 1.5)

# ------------------------------------------------------------------ 4 서비스 목표
s = frame(4, "서비스 목표", ["목표는 두 단계 —", "유입이 먼저, 그다음이 체류와 전환입니다."],
          "유입 후 구매까지 한 걸음에 이어지도록 구상했습니다.",
          notes="[1분] 그래서 서비스 목표는 두 단계입니다. 첫째 자사몰 유입을 늘리는 것이 최우선입니다. 광고를 켠 날에만 팔리는 구조가 아니라 고객이 스스로 찾아오게 합니다. "
                "둘째 체류시간을 늘리고, 가격을 탐색한 고객이 구매까지 이어지는 전환율을 높입니다. 유입에서 구매까지 한 걸음에 이어지도록 구상했습니다.")
text(s, L, 2.55, 0.8, 1.0, "1", size=54, bold=True, color=ACC)
text(s, L + 0.95, 2.67, 4.8, 0.5, "자사몰 유입 증가", size=22, bold=True)
text(s, L + 0.95, 3.25, 4.8, 0.6, "광고를 켠 날에만 팔리는 구조에서 벗어나\n고객이 스스로 찾아오게 합니다.", size=12, color=INK2, lsp=1.35)
text(s, 6.9, 2.55, 0.8, 1.0, "2", size=54, bold=True, color=ORG)
text(s, 7.85, 2.67, 4.6, 0.5, "체류시간 ↑ · 전환율 ↑", size=22, bold=True)
text(s, 7.85, 3.25, 4.6, 0.6, "가격을 확인·비교하며 머무르고\n탐색한 뒤 자사몰 구매까지 이어지게 합니다.", size=12, color=INK2, lsp=1.35)
line(s, L, 4.55, RIGHT, 4.55, LINE, 0.75)
for i, (t1, c) in enumerate([("유입", ACC), ("체류 · 가격 확인", ACC), ("탐색 · 지금 살까?", ACC), ("구매", INK)]):
    x = L + i * 3.05
    dot(s, x, 5.16, 0.2, c)
    text(s, x + 0.32, 5.07, 2.4, 0.4, t1, size=14, bold=True, anchor="m")
    if i < 3:
        text(s, x + 2.3, 5.05, 0.6, 0.4, "→", size=18, bold=True, color=ACC, anchor="m", align="c")

# ------------------------------------------------------------------ 4 전략·솔루션
s = frame(4, "세부 전략과 솔루션", ["두 가지 전략을 하나로 묶은 솔루션이", "‘막지스톡’입니다."],
          "하나의 서비스로 유입·체류·전환을 동시에 개선합니다.",
          notes="[1분] 목표를 이루는 전략은 두 가지입니다. 하나, 가격 자체를 콘텐츠로 만들어 매일 오게 한다. 둘, 고객이 직접 고르는 혜택으로 참여와 주도성을 준다. "
                "이 둘을 묶은 것이 막지스톡입니다. 빵값을 주식시장처럼 하루 두 번 열고, 그 안에서 고객이 자기 방식대로 혜택을 고릅니다. 경쟁 6곳은 모두 고정 가격·고정 혜택이라 이 조합을 쓰는 곳이 없습니다.")
for i, (n, c, tt, dd) in enumerate([("1", ACC, "가격 자체를 콘텐츠로", "매일 두 번 바뀌는 빵값이 ‘오늘은 얼마일까?’라는 방문 이유가 됩니다."),
                                    ("2", ORG, "고객이 직접 고르는 혜택", "잠금 또는 보상 고르기 — 내가 원하는 방식으로 혜택을 받고, 주도성을 느낍니다.")]):
    x = L + i * 5.9
    text(s, x, 2.5, 0.8, 1.0, n, size=50, bold=True, color=c)
    text(s, x + 0.85, 2.62, 4.7, 0.5, tt, size=20, bold=True)
    text(s, x + 0.85, 3.2, 4.7, 0.8, dd, size=12, color=INK2, lsp=1.4)
text(s, 6.4, 4.15, 0.6, 0.5, "↓", size=24, bold=True, color=ACC, align="c")
text(s, L, 4.75, 11.5, 1.0, "MAKJI STOCK", size=46, bold=True, color=ACC, align="c")
text(s, L, 5.65, 11.5, 0.4, "빵값을 주식시장처럼 — 하루 두 번 열리는 시세를 보고, 내 방식대로 혜택을 골라 자사몰에서 삽니다.", size=13, color=INK2, align="c")
text(s, L, 6.02, 11.5, 0.3, "경쟁 6곳 중 가격 변동 자체를 콘텐츠로 쓰는 곳은 아직 없습니다.", size=11.5, bold=True, color=ACC2, align="c")

# ------------------------------------------------------------------ 5 서비스
s = frame(5, "서비스 소개", ["하루가 이렇게 돌아갑니다 —", "세 가지 기능이 하루를 잇습니다."],
          "선택은 언제나 고객 몫이고, 잠금 때문에 손해 보는 경우는 없습니다.",
          notes="[1분] 아침 6시 오전장이 열려 시세를 보고, 마음에 드는 빵 하나를 잠급니다. 오후 4시 오후장에서 잠금이 정산되고 자사몰에서 결제합니다. 다음 날 6시에는 예측 결과를 확인하러 다시 옵니다. "
                "5월 로그인은 오전 8~10시에, 결제는 저녁 20~24시에 몰렸는데 6시와 16시는 그 두 시점 직전입니다. 세 기능 — 오늘의 시세, 가격 잠금, 오늘의 보상 고르기 — 이 하루를 잇습니다.")
line(s, 1.5, 2.95, 11.85, 2.95, LINE, 2.5)
for i, (tm, ds, c) in enumerate([("06:00", "오전장 개장 · 시세 확인", ACC), ("오전장 중", "가격 잠금 (하루 1회)", AMB), ("16:00", "오후장 개장 · 잠금 정산", ORG), ("구매", "막지 자사몰에서 결제", INK), ("익일 06:00", "예측 결과 확인", GRN)]):
    cx = 1.5 + i * 2.59
    dot(s, cx - 0.14, 2.81, 0.28, c)
    text(s, cx - 1.2, 3.2, 2.4, 0.3, tm, size=14, bold=True, align="c")
    text(s, cx - 1.2, 3.55, 2.4, 0.3, ds, size=10.5, color=MUTE, align="c")
for i, (c, tt, dd) in enumerate([(ACC, "오늘의 시세", "6종의 가격과 할인율을 하루 두 번 공개합니다."),
                                  (AMB, "가격 잠금", "오전가를 하루 1개 잠그면, 오후에 올라도 그 가격입니다."),
                                  (ORG, "오늘의 보상 고르기", "안정형은 즉시 확정 쿠폰, 공격형은 내일 예측에 도전합니다.")]):
    x = L + i * 3.9
    rect(s, x, 4.75, 0.5, 0.05, c, r=0)
    text(s, x, 4.95, 3.5, 0.4, tt, size=17, bold=True)
    text(s, x, 5.45, 3.4, 0.7, dd, size=11.5, color=INK2, lsp=1.4)

# ------------------------------------------------------------------ 6 여정
s = frame(6, "사용자 여정 — 구매 의사별 행동", ["고객은 세 부류 —", "각자 가장 유리한 구매 방식을 고를 수 있습니다."],
          "잠금과 예측은 구매를 미루는 장치가 아니라 가장 유리한 방식을 보장하는 무기입니다.",
          notes="[1분] 고객은 세 부류입니다. 가격이 마음에 들고 바로 결제할 수 있는 즉시 구매형, 가격은 좋은데 결제는 나중에 할 가격 확보형, 오후에 더 싸지길 기다리는 관망형입니다. "
                "잠금은 가격 확보형의 상승 위험을 없애 주고, 예측은 관망형이 내일 다시 오게 만듭니다. 세 부류 모두 결제는 자사몰에서 이어집니다.")
text(s, L, 2.3, 8, 0.3, [[("마켓 방문  ", {"bold": True, "color": INK}), ("오늘의 가격 확인   4,500원 → 3,200원", {"color": ACC2, "bold": True})]], size=12)
rows = [("즉시 구매형", "이 가격 완벽해!", "오늘 가격으로 즉시 구매", "오늘가로 즉시 결제", rgb("E6FAF3"), rgb("20C997"), rgb("087F5B")),
        ("가격 확보형", "가격은 좋은데 결제는 이따가!", "오전가 잠금 후 이따가 구매", "잠근 가격으로 안심 결제", rgb("FFF1E0"), rgb("FF922B"), rgb("B8470D")),
        ("관망·기대형", "오후장에 더 싸지면 살래", "내일 가격 예측 참여", "쿠폰 적용해 최적가 결제", rgb("E6F3FF"), rgb("339AF0"), rgb("1864AB"))]
for i, (nm, q, act, fin, fl, bd, tc) in enumerate(rows):
    y = 2.9 + i * 1.12
    rect(s, L, y, 4.0, 0.85, fl, bd, r=0.14, lw=1.25)
    text(s, L + 0.25, y, 3.6, 0.85, [[(nm, {"bold": True, "size": 14})], [(q, {"size": 11})]], color=tc, anchor="m", lsp=1.2)
    text(s, L + 4.15, y, 0.5, 0.85, "→", size=20, bold=True, color=ACC, align="c", anchor="m")
    text(s, L + 4.7, y, 3.4, 0.85, act, size=14, bold=True, anchor="m")
    text(s, L + 8.05, y, 0.5, 0.85, "→", size=20, bold=True, color=ACC, align="c", anchor="m")
    rect(s, L + 8.6, y + 0.12, 2.93, 0.61, INK, r=0.3)
    text(s, L + 8.6, y + 0.12, 2.93, 0.61, fin, size=11.5, bold=True, color=WHITE, align="c", anchor="m")

# ------------------------------------------------------------------ 7 가격 결정
s = frame(7, "가격 결정 방식", ["하루 세 구간, 두 개의 신호.", "가격은 공개된 산식으로만 움직입니다."],
          "산식은 공개하고, 정가를 넘지 않으며, 상한은 38%로 고정합니다.",
          notes="[1분] 가격은 임의의 세일이 아니라 공개된 산식입니다. 검색지수는 수요 신호로 최대 15% 할인을 더하고, 환율은 원가 신호로 내리면 하락률의 14배를 전부 돌려주고 오르면 7배, 절반만 반영합니다. "
                "합계는 0에서 38% 사이로 고정되어 정가를 넘지 않습니다. 모닝롤을 예로 들면 정가 4,500원이 평균 할인 15%에서 3,830원, 최대 할인 38%에서 2,790원입니다. 나머지 5종도 같은 산식입니다.")
for (a, b, lab, sub, fl, tc) in [(6, 16, "오전장  06:00 ~ 15:59", "전일 종가 기준", ACC, WHITE), (16, 26, "오후장  16:00 ~ 익일 01:59", "당일 시가 기준", ORG, WHITE), (26, 30, "정가  02:00~05:59", "", LINE, INK2)]:
    x = L + (a - 6) / 24 * 11.53; w = (b - a) / 24 * 11.53 - 0.05
    rect(s, x, 2.45, w, 0.62, fl, r=0.12)
    text(s, x + 0.2, 2.45, w - 0.3, 0.62, [[(lab, {"bold": True, "size": 12.5 if a < 26 else 10}), ("   " + sub, {"size": 10, "color": rgb("E6EEF7") if a < 26 else INK2})]], color=tc, anchor="m")
text(s, L, 3.55, 11.5, 0.6, [[("총 할인율  =  ", {}), ("검색 할인", {"color": ACC2}), ("  +  ", {"color": MUTE}), ("환율 조정", {"color": ORG}), ("     (0% ~ 38%)", {"color": MUTE, "size": 16})]], size=26, bold=True, align="c")
text(s, L, 4.2, 11.5, 0.35, "검색지수 × 0.15 (최대 15%)   ·   환율 하락은 ×14 전부 환원, 상승은 ×7 절반만 반영", size=12, color=INK2, align="c")
text(s, L, 4.95, 3, 0.25, "예시 · 막지 제로 모닝롤", size=11, color=MUTE)
for i, (lb, v, c) in enumerate([("정가", "4,500원", INK2), ("평균 할인 15%", "3,830원", ACC2), ("최대 할인 38%", "2,790원", ORG)]):
    x = L + i * 3.85
    text(s, x, 5.3, 3.4, 0.35, lb, size=12, color=MUTE)
    text(s, x, 5.62, 3.4, 0.6, v, size=28, bold=True, color=c)
    if i < 2:
        text(s, x + 2.6, 5.55, 0.6, 0.6, "→", size=22, bold=True, color=ACC, align="c")

# ------------------------------------------------------------------ 8 할인율 분포
AM, PM = [1, 9, 37, 25, 14, 5], [1, 18, 40, 22, 8, 2]
BN = ["5% 미만", "5~10%", "10~15%", "15~20%", "20~25%", "25% 이상"]
s = frame(8, "할인율 분포", ["세션의 84%가 할인 20% 미만이고,", "25% 이상 큰 할인은 3.8%뿐입니다."],
          "대부분은 얕은 할인이고, 깊은 할인은 드물게만 나옵니다.",
          source="실제 가격 엔진(v1.0)에 한국은행 ECOS 원/달러 시가·종가와 일별 검색지수를 넣은 재현값 (2026.06.12~09.10, 하루 2세션 × 91일) · 25% 이상 7세션 중 6세션은 상한 38% · 검색지수는 6종 합산 단일 시계열",
          notes="[1분] 이 가격 엔진을 실제 환율과 검색지수로 91일 돌려 봤습니다. 하루 두 번, 182개 세션의 평균 할인율은 15%(오전장 15.8%, 오후장 14.2%)입니다. 세션의 84%가 20% 미만이고, 25% 이상 큰 할인은 7번, 3.8%뿐입니다. "
                "이 분포가 다음 장의 마진 방어의 근거입니다.")
text(s, L + 8.6, 2.05, 2.9, 0.55, [[("평균 ", {"size": 12, "color": MUTE}), ("15.0%", {"size": 26, "bold": True, "color": ACC2})]], anchor="m", align="r")
text(s, L + 7.0, 2.62, 4.5, 0.25, "오전장 15.8% · 오후장 14.2%", size=10.5, color=MUTE, align="r")
text(s, L, 2.3, 1.2, 0.25, "■ 오전장", size=10.5, color=ACC); text(s, L + 1.0, 2.3, 1.2, 0.25, "■ 오후장", size=10.5, color=ORG)
base = 5.5; mh = 2.35
for i in range(6):
    x = L + 0.35 + i * 1.86
    for j, (v, c) in enumerate([(AM[i], ACC), (PM[i], ORG)]):
        h = v / 45 * mh
        rect(s, x + j * 0.62, base - h, 0.55, max(h, 0.03), c, r=0.04)
        text(s, x + j * 0.62 - 0.1, base - h - 0.3, 0.75, 0.26, str(v), size=12, bold=True, align="c")
    text(s, x - 0.2, base + 0.1, 1.95, 0.25, BN[i], size=12, bold=True, align="c")
    text(s, x - 0.2, base + 0.37, 1.95, 0.22, "%.1f%%" % ((AM[i] + PM[i]) / 182 * 100), size=10.5, color=MUTE, align="c")
line(s, L, base, RIGHT, base, LINE, 1.5)
xb0, xb1 = L + 0.35 - 0.1, L + 0.35 + 3 * 1.86 + 1.17
line(s, xb0, 2.98, xb1, 2.98, ACC, 1.5)
text(s, xb0, 2.62, xb1 - xb0, 0.3, "84%  (153 / 182 세션)", size=12.5, bold=True, color=ACC2, align="c")

# ------------------------------------------------------------------ 9 마진
s = frame(9, "마진율 방어", ["할인은 대부분 얕은 구간에 몰려 있고,", "깊은 할인은 상한 38%에서 멈춥니다."],
          "정가 마진 40% 이상이면 가장 깊은 할인에서도 적자가 나지 않습니다.",
          source="※ 실제 원가·마진 자료가 없어 정가 마진율 40/50/60%를 가정한 시나리오입니다 (마진율 = (판매가 − 원가) ÷ 판매가, 원가는 정가 기준 고정)",
          notes="[1분 30초] 걱정되는 것은 마진입니다. 할인은 얕은 구간에 몰려 있고, 합계 38%가 상한이라 더 깊어지지 않습니다. 정가 마진이 40%라고 가정해도 가장 깊은 할인 세션의 마진은 3.2%로 흑자입니다. "
                "평균 할인 15%에서는 마진율이 29~53%로 유지됩니다. 손익분기 판매량은 평균 할인 기준으로 마진 50%면 +43%, 60%면 +33%, 40%면 +60%입니다. "
                "다만 실제 원가·마진 자료가 없어 40/50/60% 가정이라는 점, 실제 수치를 주시면 정밀 검증하겠다는 점을 말씀드립니다.")
cx0, cy0, cw, ch = 1.7, 2.35, 8.6, 3.35
px = lambda d: cx0 + d / 40 * cw
py = lambda m: cy0 + ch - m / 70 * ch
rect(s, px(0), cy0, px(20) - px(0), ch, TINT, r=0)
text(s, px(0), cy0 + 0.05, px(20) - px(0), 0.28, "세션의 84%", size=11.5, bold=True, color=ACC2, align="c")
for v in (0, 20, 40, 60):
    line(s, cx0, py(v), cx0 + cw, py(v), LINE, 0.6)
    text(s, cx0 - 0.6, py(v) - 0.11, 0.5, 0.22, "%d%%" % v, size=10, color=MUTE, align="r")
for d in (0, 10, 20, 30, 38):
    text(s, px(d) - 0.35, cy0 + ch + 0.08, 0.7, 0.22, "%d%%" % d, size=10, color=MUTE, align="c")
text(s, px(38) + 0.5, cy0 + ch + 0.08, 1.0, 0.22, "← 할인율", size=10.5, bold=True, color=INK2)
line(s, px(38), cy0, px(38), cy0 + ch, ORG, 1, dash=True)
for m, c in [(60, GRN), (50, ACC), (40, ORG)]:
    pts = [(x, ((1 - x / 100) - (1 - m / 100)) / (1 - x / 100) * 100) for x in range(0, 39, 2)] + [(38, ((1 - .38) - (1 - m / 100)) / (1 - .38) * 100)]
    for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
        line(s, px(x1), py(y1), px(x2), py(y2), c, 2.75)
    a = ((1 - .15) - (1 - m / 100)) / (1 - .15) * 100
    z = ((1 - .38) - (1 - m / 100)) / (1 - .38) * 100
    dot(s, px(15) - 0.07, py(a) - 0.07, 0.14, WHITE).line.color.rgb = c
    text(s, px(15) - 0.1, py(a) - 0.34, 0.9, 0.24, "%.1f%%" % a, size=11, bold=True)
    dot(s, px(38) - 0.07, py(z) - 0.07, 0.14, c)
    text(s, px(38) + 0.14, py(z) - 0.13, 2.0, 0.26, [[("%.1f%%" % z, {"bold": True, "color": INK}), ("   마진 %d%%" % m, {"color": c, "bold": True, "size": 10.5})]], size=11.5)
text(s, px(15) - 0.6, cy0 + ch + 0.36, 1.2, 0.22, "평균 15%", size=10, bold=True, color=ACC2, align="c")

# ------------------------------------------------------------------ 10 MVP
s = frame(10, "MVP 범위", ["첫 버전은 두 전략을 검증하는", "기능만 담습니다."],
          "구현 2~3주 · 검증 9/28~9/30 — 상품 수만 확정되면 바로 착수합니다.",
          notes="[1분] 첫 버전은 두 전략을 검증하는 기능만 담습니다. 반드시 포함하는 것은 시세 확인, 가격 잠금, 보상 고르기, 자사몰 전환, ‘투자가 아닙니다’ 안내, 38% 상한 가드레일입니다. "
                "여력이 되면 가격 하락 이메일 알림을 넣습니다. 도감·씰, 매수가 기준 보상, 막지스톡 안의 결제는 이번에 하지 않습니다. 구현은 2~3주차, 검증은 9월 28~30일이고, 상품 수(대표 6종 기준)만 확정되면 됩니다.")
text(s, L, 2.45, 6, 0.3, "포함 (Must)", size=12, bold=True, color=ACC2)
for i, (k, v) in enumerate([("전략 1", "오전장·오후장 가격 확인"), ("전략 2", "가격 잠금 (오전장 하루 1회)"), ("전략 2", "오늘의 보상 고르기 (안정형 / 공격형)"), ("전환", "자사몰 이동·구매 (원클릭 지향)"), ("신뢰", "‘투자가 아닙니다’ 안내 · 가격 근거"), ("안전", "38% 상한 가드레일")]):
    y = 2.9 + i * 0.5
    text(s, L, y, 0.9, 0.4, k, size=11, bold=True, color=ACC2 if k == "전략 1" else (rgb("C2410C") if k == "전략 2" else MUTE), anchor="m")
    text(s, L + 1.0, y, 5.2, 0.4, v, size=15, bold=True, anchor="m")
line(s, 7.55, 2.55, 7.55, 5.85, LINE, 0.75)
text(s, 8.0, 2.45, 4, 0.3, "이번 범위 제외 · 여력 시", size=12, bold=True, color=MUTE)
for i, v in enumerate(["여력 시 · 가격 하락 이메일 알림", "도감·씰 수집 콘텐츠", "매수가 기준 보상", "막지스톡 안에서의 결제", "막지스톡 자체 로그인·회원가입"]):
    text(s, 8.0, 2.9 + i * 0.5, 4.4, 0.4, v, size=13.5, color=INK2 if i else ACC2, bold=(i == 0), anchor="m")

# ------------------------------------------------------------------ 11 KPI
s = frame(11, "KPI", ["서비스 목표와 같은 순서로", "측정합니다."],
          "목표값은 근거 없이 만들지 않고, 베타 1주차 실측 후 확정합니다.",
          source="GUARDRAIL(하나라도 초과 시 롤아웃 중단): 총혜택 상한 위반 0 · 사행성 문구 0 · 표시·결제가 불일치 0 · 가격 계산 오류율 ≤ 0.1% · 쿠폰 중복 적용 0",
          notes="[1분] KPI는 서비스 목표와 같은 순서입니다. 북극성 지표는 STOCK에서 잠금·보상을 고른 세션이 자사몰 구매까지 가는 비율이고, 아직 서비스 전이라 미측정입니다. 베타 첫 주에 기준선을 잡습니다. "
                "5월 기준으로는 신규 가입 40건, 결제 완결률 73.5%가 있습니다. 목표 숫자를 근거 없이 정하지 않는다는 원칙이라 ‘베타 실측 후 확정’이라고 적었습니다. 가드레일은 하나라도 넘으면 즉시 중단합니다.")
text(s, L, 2.4, 3, 0.3, "북극성 KPI", size=11, bold=True, color=ACC2)
text(s, L, 2.72, 9, 0.6, [[("STOCK → 자사몰 전환율", {"bold": True}), ("     현재 미측정 · 베타 1주차에 기준선 확보", {"size": 13, "color": MUTE})]], size=26)
line(s, L, 3.6, RIGHT, 3.6, LINE, 0.75)
for i, (tg, c, tc, k, cur) in enumerate([("1순위 유입", TINT, ACC2, "방문자 수 · 신규 가입 · 자사몰 구매 이동률", "신규가입 5월 40건"),
                                         ("2순위 체류", AMB2, rgb("7A5B00"), "익일 재방문율 · 체류시간 · 가격 잠금 사용률", "미측정"),
                                         ("2순위 전환", ORG2, rgb("B6451B"), "STOCK→자사몰 전환율 · 쿠폰 사용률 · 결제 완결률", "결제 완결률 73.5%")]):
    y = 3.85 + i * 0.75
    pill(s, L, y, 1.4, tg, c, tc, size=11.5, h=0.4)
    text(s, L + 1.7, y, 7.2, 0.4, k, size=14.5, anchor="m")
    text(s, L + 8.7, y, 2.83, 0.4, cur, size=12.5, color=MUTE, align="r", anchor="m")

# ------------------------------------------------------------------ 12 매출
s = frame(12, "매출 시나리오", ["KPI가 달성되면 매출은 이렇게 그려집니다 —", "점유율 확대만으로 잡은 5개년 시나리오."],
          "시장이 커진다는 가정 없이, 점유율만으로 Base 18.8억을 그립니다.",
          source="TAM 13.6조원(국내 베이커리 2025) · SAM 2,100~2,650억(전문점×온라인×2030) · 목표 점유율 0.5~3% · 시장 성장률 미반영 · 망넛이네(2018 약 5.7억)·널담(2019 약 9.9억) 초기 실적은 벤치마크로만 참고, 확정 전망 아님",
          notes="[1분] KPI가 달성됐을 때의 매출입니다. 매출은 유입 × 전환율 × 객단가이고 5월 객단가는 2.32만 원입니다. 시장 규모 TAM 13.6조, SAM 2,100~2,650억에서 시장이 성장한다는 가정은 넣지 않고 점유율만 0.5%에서 3%로 넓혔습니다. "
                "Base는 1년차 5.7억에서 5년차 18.8억, Worst 2.8억, Best 35.3억입니다. 망넛이네와 널담의 초기 실적은 확정 전망이 아니라 성공 벤치마크로만 참고했습니다.")
text(s, 5.6, 2.15, 6.83, 0.3, [[("매출 = 유입 × 구매 전환율 × 객단가 ", {"color": INK2}), ("(5월 2.32만원)", {"color": MUTE, "size": 10})]], size=12, bold=True, align="r")
text(s, L, 2.45, 2, 0.25, "■ 1년차", size=10.5, color=rgb("8FB5DA")); text(s, L + 0.9, 2.45, 2, 0.25, "■ 5년차", size=10.5, color=ACC)
for i, (nm, a, b) in enumerate([("Worst", 1.2, 2.8), ("Base", 5.7, 18.8), ("Best", 9.9, 35.3)]):
    x = 1.9 + i * 3.7
    for j, (v, c) in enumerate([(a, LB), (b, ACC)]):
        h = v / 36 * 2.9
        rect(s, x + j * 1.3, 5.85 - h, 1.1, max(h, 0.05), c, r=0.05)
        text(s, x + j * 1.3 - 0.2, 5.85 - h - 0.4, 1.5, 0.35, str(v) + "억", size=15, bold=True, align="c", color=ACC2 if (j and i == 1) else INK)
    text(s, x - 0.2, 5.98, 2.9, 0.28, nm, size=12.5, bold=True, align="c")
    line(s, x - 0.3, 5.85, x + 2.7, 5.85, LINE, 1.25)

# ------------------------------------------------------------------ 13 리스크
s = frame(13, "핵심 리스크", ["구조적 제약 하나와,", "실행으로 관리 가능한 다섯 가지입니다."],
          "HIGH 3건은 출시 전에 해소합니다.",
          source="대응 원칙: 총혜택 상한 38% 고정 · 표시가 = 결제가 일치 검증 · 할인 표시 법무 검토 · 3구간 모델 기준 백테스트 재실행",
          notes="[1분] 리스크는 여섯 가지입니다. 막지스톡과 자사몰 결제 시스템이 분리된 것은 RFP가 정한 구조라 없앨 수 없고, 원클릭·자동 인식으로 줄이기만 합니다. HIGH는 키워드 적합성, 표시가·결제가 불일치, 법적 위험 세 가지입니다. "
                "나머지 둘은 관리 중입니다. 총혜택 상한 38%, 표시가=결제가 검증, 법무 검토, 백테스트 재실행으로 대응합니다.")
risks = [("01", "STOCK ↔ 자사몰 분리", "RFP 요구 구조 — 원클릭으로 최소화만 가능", "구조적", INK, WHITE),
         ("02", "검색 키워드 적합성", "백테스트는 모닝빵 1종 중심 — 나머지 검증 필요", "HIGH", ORG, WHITE),
         ("03", "표시·결제가 불일치", "다르면 신뢰·전환이 훼손됨", "HIGH", ORG, WHITE),
         ("04", "법적 위험", "할인 표시가 실제와 다르면 표시광고법 소지", "HIGH", ORG, WHITE),
         ("05", "가격모델 전환 재검증", "3구간 모델로 바뀌어 백테스트 재실행", "관리중", AMB, rgb("4A3600")),
         ("06", "쿠폰 중복 적용", "동시 적용 시 총혜택 상한 초과 가능", "관리중", AMB, rgb("4A3600"))]
for i, (n, tt, dd, lv, lf, lc) in enumerate(risks):
    x = L + (i // 3) * 5.95; y = 2.6 + (i % 3) * 1.15
    text(s, x, y, 0.6, 0.4, n, size=13, bold=True, color=MUTE, anchor="m")
    text(s, x + 0.65, y - 0.02, 3.6, 0.4, tt, size=15.5, bold=True, anchor="m")
    text(s, x + 0.65, y + 0.4, 4.2, 0.3, dd, size=10.5, color=MUTE)
    pill(s, x + 4.55, y + 0.03, 0.85, lv, lf, lc, size=10, h=0.3)

# ------------------------------------------------------------------ 14 로드맵·요청
s = frame(14, "로드맵과 요청 사항", ["3단계로 구현하고,", "대표님께는 세 가지를 요청드립니다."],
          "세 가지가 정해지면 바로 구현·검증 단계로 들어갑니다.",
          source="향후 확장(설계 단계, 이번 구현 범위 아님): Bakery ETF · FX Bakery · Bread Index · 연속 방문 스트릭 보상",
          notes="[1분 + 요청] 로드맵은 3단계입니다. 1단계 MVP는 시세·비교·구매 이동, 2단계는 잠금·보상 고르기·알림, 3단계는 자사몰 실연동입니다. "
                "오늘 요청드릴 것은 세 가지입니다. 하나, MVP 상품 수 확정. 둘, 실제 원가·마진율 공유 — 지금은 40/50/60% 가정이라 실제 수치로 마진 방어를 정밀 검증하겠습니다. 셋, 할인 표시에 대한 법무 검토입니다.")
line(s, L, 2.75, RIGHT, 2.75, LINE, 2.5)
for i, (ph, c, tt, dd) in enumerate([("PHASE 1", ACC, "MVP", "시세 · 비교 · 구매 이동"), ("PHASE 2", AMB, "참여", "가격 잠금 · 보상 고르기 · 알림"), ("PHASE 3", ORG, "연동", "자사몰 실연동 · 쿠폰 · 구매 데이터")]):
    x = L + i * 3.95
    dot(s, x, 2.61, 0.28, c)
    text(s, x, 3.05, 3.6, 0.3, [[(ph + "  ", {"size": 10.5, "color": MUTE, "bold": True}), (tt, {"size": 16, "bold": True})]])
    text(s, x, 3.42, 3.6, 0.3, dd, size=11, color=INK2)
text(s, L, 4.3, 5, 0.3, "요청 사항", size=11, bold=True, color=ACC2)
for i, (n, c, tt, dd) in enumerate([("01", ACC, "MVP 상품 수 확정", "대표 6종 기준으로 준비 중 · 최종 승인 필요"),
                                    ("02", AMB, "실제 원가·마진율 공유", "지금은 40/50/60% 가정 · 실제 수치로 정밀 검증"),
                                    ("03", ORG, "할인 표시 법무 검토", "기준가격·할인율·적용기간 표시가 표시광고법에 맞는지")]):
    y = 4.7 + i * 0.58
    text(s, L, y, 0.7, 0.45, n, size=20, bold=True, color=c, anchor="m")
    text(s, L + 0.8, y, 3.6, 0.45, tt, size=16, bold=True, anchor="m")
    text(s, L + 4.5, y, 7, 0.45, dd, size=12, color=INK2, anchor="m")

# ------------------------------------------------------------------ 15 Q&A
s = prs.slides.add_slide(BLANK)
rect(s, 0, 0, 0.22, 7.5, ACC, r=0)
text(s, 0.9, 0.55, 4, 0.3, [[("●  ", {"color": ACC}), ("MAKJI", {"bold": True})]], size=13, bold=True, color=INK)
text(s, 7.5, 0.55, 4.93, 0.3, "Q&A", size=10.5, bold=True, color=MUTE, align="r")
text(s, 0.9, 2.7, 11.5, 2.2, [["가격이 움직인다는 사실 자체가,"], [("다시 찾는 이유", {"color": ACC}), ("가 됩니다.", {})]], size=44, bold=True, lsp=1.15)
text(s, 0.9, 5.2, 8, 0.4, "질문과 의견을 듣겠습니다.", size=16, color=INK2)
text(s, 0.9, 6.75, 6, 0.3, "빵값연구소  |  MAKJI STOCK", size=11, color=INK2)
s.notes_slide.notes_text_frame.text = "[Q&A] 예상 질문은 발표 스토리라인 문서의 ‘예상 질문과 답변’을 참고하세요."

OUT.parent.mkdir(parents=True, exist_ok=True)
prs.save(str(OUT))
print("saved", OUT, "slides", len(prs.slides))
