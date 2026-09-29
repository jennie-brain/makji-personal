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

N = 15
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


# Z-pattern frame -------------------------------------------------------
def frame(idx, kicker, headline, kpi, evidence, sowhat, source=None, notes=""):
    s = prs.slides.add_slide(BLANK)
    # A: top-left
    text(s, 0.6, 0.42, 8.2, 0.3, kicker, size=11, bold=True, color=ACC2)
    text(s, 0.6, 0.74, 8.2, 1.25, headline, size=25, bold=True, color=INK, lsp=1.12)
    # B: top-right (one number to remember)
    rect(s, 9.05, 0.42, 3.68, 1.5, TINT, r=0.14)
    text(s, 9.3, 0.55, 3.2, 0.25, kpi[0], size=10, bold=True, color=ACC2)
    text(s, 9.3, 0.8, 3.2, 0.62, kpi[1], size=kpi[3] if len(kpi) > 3 else 34, bold=True, color=INK, anchor="m")
    text(s, 9.3, 1.44, 3.2, 0.42, kpi[2], size=9.5, color=INK2, lsp=1.1)
    # C: bottom-left evidence
    rect(s, 0.6, 5.78, 7.75, 1.18, SOFT, r=0.12)
    text(s, 0.82, 5.86, 3, 0.2, "근거", size=9, bold=True, color=MUTE)
    evidence(s, 0.82, 6.1, 7.3, 0.8)
    # D: bottom-right so-what
    rect(s, 8.6, 5.78, 4.13, 1.18, ACC, r=0.12)
    text(s, 8.85, 5.86, 3.5, 0.2, "SO WHAT", size=9, bold=True, color=rgb("DCEAF7"))
    text(s, 8.85, 6.1, 3.7, 0.8, sowhat, size=13, bold=True, color=WHITE, lsp=1.2)
    # footer
    if source:
        text(s, 0.6, 7.08, 10.3, 0.3, source, size=7.5, color=MUTE, lsp=1.1)
    text(s, 11.2, 7.1, 1.53, 0.2, [[("MAKJI STOCK  ", {"bold": True, "color": INK2}), ("%02d / %d" % (idx, N), {"color": MUTE})]], size=8.5, align="r")
    if notes:
        s.notes_slide.notes_text_frame.text = notes
    return s


def ev_lines(*lines, size=11):
    def draw(s, x, y, w, h):
        text(s, x, y, w, h, list(lines), size=size, color=INK2, lsp=1.2, gap=2)
    return draw


def ev_stats(items):
    """items: [(value, label)] 가로 나열"""
    def draw(s, x, y, w, h):
        n = len(items); cw = w / n
        for i, (v, l) in enumerate(items):
            text(s, x + i * cw, y - 0.02, cw - 0.1, 0.4, v, size=18, bold=True, color=INK, anchor="m")
            text(s, x + i * cw, y + 0.4, cw - 0.12, 0.4, l, size=9, color=INK2, lsp=1.1)
    return draw



def ev_copy(s, x, y, w, h):
    items = [("즉시 구매하기", "고민하는 순간 내일 가격이 오를 수 있어요!", GRN2), ("가격 잠그기 (하루 1회)", "바쁘다면 일단 잠그세요. 오후에 올라도 이 가격 그대로.", AMB2), ("가격 예측하고 5% 쿠폰 받기", "예측에 참여하고 최적가에 쿠폰까지 얹어 구매하세요.", TINT)]
    for i, (b, c, fl) in enumerate(items):
        xx = x + i * 2.5
        rect(s, xx, y - 0.02, 2.4, 0.86, fl, r=0.08)
        text(s, xx + 0.1, y - 0.02, 2.2, 0.86, [[(b, {"bold": True, "color": INK})], [(c, {"color": INK2, "size": 8.5})]], size=9.5, anchor="m", lsp=1.1, gap=1)

def card(s, x, y, w, h, fill=WHITE, line_c=LINE):
    return rect(s, x, y, w, h, fill, line_c, r=0.14)


def bars(s, x, y_base, maxh, vmax, data, bw, gap, lab_size=12, cat_size=10):
    """data: [(cat, sub, value, color, label)]"""
    for i, (cat, sub, v, c, lab) in enumerate(data):
        bx = x + i * (bw + gap); h = v / vmax * maxh
        rect(s, bx, y_base - h, bw, h, c, r=0.06)
        text(s, bx - 0.2, y_base - h - 0.3, bw + 0.4, 0.26, lab, size=lab_size, bold=True, color=INK, align="c")
        text(s, bx - 0.2, y_base + 0.08, bw + 0.4, 0.22, cat, size=cat_size, bold=True, color=INK, align="c")
        if sub:
            text(s, bx - 0.2, y_base + 0.29, bw + 0.4, 0.2, sub, size=8.5, color=MUTE, align="c")
    line(s, x - 0.25, y_base, x + len(data) * (bw + gap) - gap + 0.25, y_base, LINE, 1.5)


# ------------------------------------------------------------------ slide 1
s = prs.slides.add_slide(BLANK)
rect(s, 0, 0, 0.22, 7.5, ACC, r=0)
text(s, 0.75, 0.45, 4, 0.3, [[("●  ", {"color": ACC}), ("MAKJI", {"bold": True})]], size=13, bold=True, color=INK)
text(s, 7.5, 0.45, 5.2, 0.3, "BUSINESS PROPOSAL 2026 · 기업 대표 보고", size=10.5, bold=True, color=MUTE, align="r")
tag(s, 0.75, 1.95, "Project Proposal", TINT, ACC2, w=1.55, size=10)
text(s, 0.75, 2.35, 7.2, 2.6, [[("MAKJI", {})], [("STOCK", {"color": ACC})]], size=76, bold=True, color=INK, lsp=0.95)
text(s, 0.75, 5.0, 7, 0.9, ["웰니스 베이커리 막지의 B2C 확장 —", "매일 두 번 움직이는 빵값으로 자사몰의 방문과 구매를 만듭니다."], size=16, color=INK2, lsp=1.35)
for i, (a, b) in enumerate([("FNC 글루텐프리 휘낭시에", "▼ 오전장 06:00"), ("MRL 제로 모닝롤", "▼ 오전장 06:00"), ("TTR 테트리스 브레드", "▼ 오후장 16:00")]):
    y = 2.35 + i * 0.85
    card(s, 8.35, y, 4.38, 0.68)
    text(s, 8.6, y, 2.6, 0.68, a, size=12.5, bold=True, color=INK, anchor="m")
    text(s, 11.0, y, 1.5, 0.68, b, size=11, bold=True, color=GRN, align="r", anchor="m")
text(s, 0.75, 6.75, 6, 0.3, "빵값연구소   |   기업 대표 보고 v5.0", size=11, color=INK2)
text(s, 8.35, 6.75, 4.38, 0.3, "2026.09", size=11, color=INK2, align="r")
s.notes_slide.notes_text_frame.text = ("[30초] 오늘 말씀드릴 것은 세 가지입니다. 시장에 기회가 있고, 우리는 그 기회를 ‘가격’으로 잡으려 하며, "
                                       "그 방식이 마진을 지킨다는 것입니다. 마지막에 세 가지 요청을 드리겠습니다.")

# ------------------------------------------------------------------ slide 2  시장 기회
s = frame(2, "시장 기회", ["온라인 베이커리 시장은 4년 만에 2배 가까이 커졌고,", "유사 업체도 빠르게 성장하고 있습니다."],
          ("온라인 베이커리 시장 성장 (2021→2025)", "+95%", "3,200억 → 6,250억원 · 연평균 +18%"),
          ev_stats([("3.3배", "신세계푸드 온라인 베이커리 2023 255억 → 2025 850억원"), ("+104%", "널담 2025년 매출 성장(전년 대비), 2018년 온라인으로 시작"), ("0 / 6", "경쟁 6곳 중 가격 변동을 콘텐츠로 쓰는 곳")]),
          "수요와 경쟁자 모두 성장 중입니다. 비어 있는 자리는 ‘가격’입니다.",
          source="출처: aT 온라인 베이커리 시장 규모(매일경제 2026.03.23 보도) · 널담 2025 매출 약 330억, 2026 목표 800억(플래텀·메트로서울 2026.01). 2024는 역산 추정, 2023은 내부 시장분석. 널담 매출에는 오프라인 유통 포함",
          notes="[1분] 온라인 베이커리 시장은 2021년 3,200억에서 2025년 6,250억으로 커졌습니다. 같은 시장의 저당·고단백 브랜드 널담은 지난해 매출이 두 배가 됐습니다. "
                "그런데 경쟁 6곳 중 가격 변동 자체를 콘텐츠로 쓰는 곳은 한 곳도 없습니다. 수요와 경쟁이 모두 커지는데 ‘가격’이라는 자리는 비어 있습니다.")
card(s, 0.6, 2.15, 5.95, 3.45); card(s, 6.78, 2.15, 5.95, 3.45)
text(s, 0.85, 2.3, 4, 0.3, "국내 온라인 베이커리 시장 (억원)", size=12, bold=True)
tag(s, 4.9, 2.3, "연평균 +18%", TINT, ACC2, w=1.4)
bars(s, 1.35, 5.0, 2.0, 6600, [("2021", "", 3200, LB, "3,200"), ("2024", "", 5400, LB, "5,400"), ("2025", "", 6250, ACC, "6,250")], 1.05, 0.7)
text(s, 7.03, 2.3, 4, 0.3, "널담 연 매출 (억원)", size=12, bold=True)
text(s, 10.35, 2.34, 0.9, 0.2, "■ 실적", size=9, color=ACC); text(s, 11.2, 2.34, 1.4, 0.2, "■ 역산·목표", size=9, color=rgb("8FB5DA"))
bars(s, 7.4, 5.0, 2.0, 830, [("2023", "", 145.6, ACC, "145.6"), ("2024", "역산", 162, LB, "≈162"), ("2025", "", 330, ACC, "≈330"), ("2026", "목표", 800, LB, "800")], 0.85, 0.55, lab_size=11)

# ------------------------------------------------------------------ slide 3  방향·목표
s = frame(3, "우리의 방향과 목표", ["웰니스 베이커리 막지는 B2C 자사몰로 확장합니다.", "목표는 유입이 먼저, 그다음이 체류와 전환입니다."],
          ("5월 파일럿 결제 완결률", "73.5%", "연환산 상품매출은 0.30억원 — 반복 방문 구조가 필요"),
          ev_stats([("147건", "5월 단일상품 파일럿 생성 주문"), ("108건", "실제 결제 완료"), ("73.5%", "주문 생성 → 결제 완결률"), ("0.30억", "단순 연환산 상품매출")]),
          "먼저 유입을 늘리고, 그다음 체류시간과 전환율을 높입니다.",
          source="출처: 막지 자사몰 5월 주문내역(단일상품 막지 ZERO 카스테라 기준)",
          notes="[1분] 막지는 저당·무설탕·글루텐프리 웰니스 베이커리이고, B2B 공급으로 제품력을 검증했습니다. 이제 자사몰(B2C)로 확장 중인데, 5월 파일럿에서 결제 완결률은 73.5%로 준수했지만 연환산 0.30억으로 성장판이 얕습니다. "
                "그래서 우리의 서비스 목표는 두 단계입니다. 첫째 유입, 둘째 체류시간과 전환율입니다.")
for i, (tg, tt, dd, fl, tc) in enumerate([("지금까지", "B2B 제품 공급", "저당·무설탕·글루텐프리 제품력 검증", SOFT, INK), ("지금", "B2C 자사몰 확장", "5월 단일상품 파일럿 운영", TINT, INK), ("과제", "다시 오게 하고, 사게 하기", "반복 방문 구조가 필요", INK, WHITE)]):
    x = 0.6 + i * 4.19
    rect(s, x, 2.15, 3.75, 1.3, fl, r=0.14)
    tag(s, x + 0.2, 2.3, tg, WHITE, ACC2 if i < 2 else INK, w=0.85)
    text(s, x + 0.2, 2.62, 3.4, 0.35, tt, size=15, bold=True, color=tc)
    text(s, x + 0.2, 3.0, 3.4, 0.35, dd, size=10.5, color=INK2 if i < 2 else rgb("D5DBE8"))
    if i < 2:
        arrow(s, x + 3.8, 2.65, 0.34, 0.3)
rect(s, 0.6, 3.65, 4.3, 1.95, ACC, r=0.14)
tag(s, 0.85, 3.82, "우선순위 1", WHITE, ACC2, w=1.0)
text(s, 0.85, 4.15, 3.9, 0.45, "자사몰 유입 증가", size=21, bold=True, color=WHITE)
text(s, 0.85, 4.7, 3.8, 0.8, "광고를 켠 날에만 팔리는 구조에서 벗어나, 고객이 스스로 찾아오게 합니다.", size=11.5, color=WHITE, lsp=1.3)
rect(s, 5.1, 3.65, 7.63, 1.95, TINT, r=0.14)
tag(s, 5.35, 3.82, "우선순위 2", WHITE, ACC2, w=1.0)
text(s, 5.35, 4.15, 7, 0.45, "체류시간 확대 + 전환율 제고", size=21, bold=True, color=INK)
for j, (h, d) in enumerate([("① 체류시간", "가격을 확인·비교하며 머무는 시간"), ("② 전환율", "가격 탐색 후 자사몰 구매까지")]):
    xx = 5.35 + j * 3.6
    rect(s, xx, 4.78, 3.4, 0.62, WHITE, r=0.1)
    text(s, xx + 0.15, 4.78, 3.15, 0.62, [[(h + "  ", {"bold": True}), (d, {"color": INK2})]], size=11, anchor="m")

# ------------------------------------------------------------------ slide 4  전략→솔루션
s = frame(4, "세부 전략과 솔루션", ["두 가지 전략을 하나로 묶은 솔루션이", "‘막지스톡’입니다."],
          ("솔루션", "막지스톡", "가격 콘텐츠 + 직접 고르는 혜택", 30),
          ev_lines("근거: 경쟁 6곳(널담 포함)은 모두 고정 가격·고정 혜택 — 움직이는 가격과 선택형 혜택을 함께 쓰는 곳이 없습니다.",
                   "전략 1은 방문(유입·체류)을, 전략 2는 참여(체류·전환)를 직접 겨냥합니다."),
          "유입·체류·전환을 하나의 서비스로 동시에 개선합니다.",
          notes="[1분] 목표를 이루는 전략은 두 가지입니다. 하나, 가격 자체를 콘텐츠로 만들어 매일 오게 한다. 둘, 고객이 직접 고르는 혜택으로 참여와 주도성을 준다. "
                "이 둘을 묶은 것이 막지스톡입니다. 빵값을 주식시장처럼 하루 두 번 열고, 그 안에서 고객이 자기 방식대로 혜택을 고릅니다.")
for i, (num, colr, tg, tt, bl) in enumerate([("1", ACC, "유입 · 체류 ↑", "가격 자체를 콘텐츠로", ["빵값이 매일 두 번 바뀌어 ‘오늘은 얼마일까?’가 방문 이유가 됩니다", "검색 수요·환율 같은 실제 신호로 움직여 이유가 설명됩니다"]),
                                             ("2", ORG, "참여 · 전환 ↑", "고객이 직접 고르는 혜택", ["가격 잠금 또는 보상 고르기 — 내가 원하는 방식으로 혜택을 받습니다", "고객이 주도성을 느끼고, 선택한 만큼 구매로 이어집니다"])]):
    x = 0.6 + i * 6.18
    rect(s, x, 2.15, 5.95, 1.75, WHITE, colr, r=0.14, lw=2)
    text(s, x + 0.25, 2.25, 0.8, 0.8, num, size=40, bold=True, color=colr, anchor="m")
    tag(s, x + 1.0, 2.35, tg, TINT if i == 0 else ORG, ACC2 if i == 0 else WHITE, w=1.45)
    text(s, x + 1.0, 2.62, 4.8, 0.4, tt, size=16, bold=True)
    line(s, x + 0.25, 3.12, x + 5.7, 3.12)
    text(s, x + 0.25, 3.2, 5.5, 0.65, ["• " + b for b in bl], size=10.5, color=INK2, lsp=1.15, gap=2)
arrow(s, 6.5, 3.93, 0.32, 0.3, ACC).rotation = 90
rect(s, 0.6, 4.28, 12.13, 1.32, ACC, r=0.14)
text(s, 0.9, 4.38, 3, 0.22, "SOLUTION", size=9, bold=True, color=rgb("DCEAF7"))
text(s, 0.9, 4.6, 5.2, 0.62, "MAKJI STOCK", size=32, bold=True, color=WHITE)
text(s, 0.9, 5.2, 5.5, 0.35, "빵값을 주식시장처럼 — 하루 두 번 열리는 시세를 보고, 내 방식대로 혜택을 골라 자사몰에서 삽니다.", size=9.5, color=WHITE)
for i, (a, b) in enumerate([("매일 확인하러 옵니다", "유입 ↑"), ("가격을 비교하며 머뭅니다", "체류 ↑"), ("고른 혜택으로 결제합니다", "전환 ↑")]):
    y = 4.4 + i * 0.36
    rect(s, 7.3, y, 5.15, 0.3, rgb("5E9CD3"), r=0.08)
    text(s, 7.45, y, 3.5, 0.3, a, size=10.5, bold=True, color=WHITE, anchor="m")
    text(s, 10.9, y, 1.4, 0.3, "→ " + b, size=10.5, bold=True, color=WHITE, anchor="m", align="r")

# ------------------------------------------------------------------ slide 5  서비스
s = frame(5, "서비스 소개", ["하루가 이렇게 돌아갑니다 —", "세 가지 기능이 하루를 잇습니다."],
          ("시세 갱신", "하루 2회", "오전장 06:00 · 오후장 16:00", 32),
          ev_lines("오전장 06:00~15:59 (전일 종가 기준)  ·  오후장 16:00~익일 01:59 (당일 시가 기준)  ·  정가 02:00~05:59 (할인 없음)",
                   "가격 잠금은 오전장에 하루 1개 — 오후에 올라도 잠근 가격, 내려가면 더 싼 오후가가 자동 적용됩니다."),
          "선택은 언제나 고객 몫이고, 잠금 때문에 손해 보는 경우는 없습니다.",
          notes="[1분] 하루는 이렇게 돌아갑니다. 아침 6시 오전장이 열려 시세를 보고, 마음에 드는 빵 하나를 잠급니다. 오후 4시 오후장에서 잠금이 정산되고, 자사몰에서 결제합니다. "
                "다음 날 6시에는 예측 결과를 확인하러 다시 옵니다. 이 하루를 세 가지 기능이 잇습니다 — 오늘의 시세, 가격 잠금, 오늘의 보상 고르기.")
line(s, 1.3, 2.5, 12.0, 2.5, LINE, 3)
for i, (tm, ds, c) in enumerate([("06:00", "오전장 개장\n오늘의 시세 확인", ACC), ("오전장 중", "가격 잠금\n(하루 1회)", AMB), ("16:00", "오후장 개장\n잠금 정산", ORG), ("구매", "막지 자사몰에서\n결제", INK), ("익일 06:00", "예측 결과 확인\n다시 개장", GRN)]):
    cx = 1.3 + i * 2.675
    dot(s, cx - 0.16, 2.34, 0.32, c); dot(s, cx - 0.07, 2.43, 0.14, WHITE)
    text(s, cx - 1.1, 2.72, 2.2, 0.3, tm, size=12, bold=True, align="c")
    text(s, cx - 1.1, 3.02, 2.2, 0.5, ds, size=9.5, color=INK2, align="c", lsp=1.15)
for i, (tg, tc, tt, dd, fl) in enumerate([("기능 1 · 전략 1", ACC2, "오늘의 시세", "6종의 가격과 할인율을 하루 두 번 공개합니다. 정가 대비 얼마나 저렴한지 한눈에 비교합니다.", TINT),
                                          ("기능 2 · 전략 2", rgb("7A5B00"), "가격 잠금", "오전장 가격을 하루 1개 잠그면 오후에 올라도 잠근 가격으로 구매합니다. 내려가면 더 싼 가격이 자동 적용됩니다.", AMB2),
                                          ("기능 3 · 전략 2", rgb("B6451B"), "오늘의 보상 고르기", "안정형은 즉시 확정 쿠폰, 공격형은 내일 가격 예측에 걸고 더 큰 쿠폰에 도전합니다.", ORG2)]):
    x = 0.6 + i * 4.09
    rect(s, x, 3.72, 3.95, 1.88, fl, r=0.14)
    tag(s, x + 0.2, 3.88, tg, WHITE, tc, w=1.35)
    text(s, x + 0.2, 4.22, 3.55, 0.35, tt, size=15, bold=True)
    text(s, x + 0.2, 4.62, 3.55, 0.9, dd, size=10.5, color=INK2, lsp=1.3)

# ------------------------------------------------------------------ slide 6  여정
s = frame(6, "사용자 여정 — 구매 의사별 행동 플로우", ["잠금과 예측은 구매를 미루는 장치가 아니라,", "가장 유리한 구매 방식을 보장하는 무기입니다."],
          ("구매 의사 유형", "3유형", "즉시 구매 · 가격 확보 · 관망·기대", 32),
          ev_copy,
          "고객 상황에 맞는 가장 유리한 구매 방식을 고를 수 있습니다.",
          notes="[1분] 고객은 세 부류입니다. 가격이 마음에 들고 바로 결제할 수 있는 즉시 구매형, 가격은 좋은데 결제는 나중에 할 가격 확보형, 오후에 더 싸지길 기다리는 관망형입니다. "
                "잠금은 가격 확보형의 상승 위험을 없애 주고, 예측은 관망형이 내일 다시 오게 만듭니다. 세 부류 모두 결제는 자사몰에서 이어집니다.")
card(s, 0.6, 2.15, 2.15, 3.45)
text(s, 0.6, 2.9, 2.15, 0.5, "마켓 방문", size=15, bold=True, align="c")
text(s, 0.6, 3.4, 2.15, 0.3, "오늘의 가격 확인", size=10, color=INK2, align="c")
text(s, 0.6, 3.7, 2.15, 0.3, "4,500원 → 3,200원", size=12, bold=True, color=ACC2, align="c")
rows = [("즉시 구매형", "이 가격 완벽해!", "가격 만족 ○ · 결제 가능 ○", "오늘 가격으로 즉시 구매", "결제 · 오늘가로 즉시 결제", rgb("E6FAF3"), rgb("20C997"), rgb("087F5B")),
        ("가격 확보형", "가격은 좋은데 결제는 이따가!", "가격 만족 ○ · 결제 보류 ×", "오전가 잠금 후 이따가 구매", "결제 · 오후에 올라도 잠근 가격으로", rgb("FFF1E0"), rgb("FF922B"), rgb("B8470D")),
        ("관망·기대형", "오후장에 더 싸지면 살래", "가격 관망 × · 결제 보류 ×", "내일 가격 예측 참여", "결제 · 도달 시 쿠폰 적용, 최적가", rgb("E6F3FF"), rgb("339AF0"), rgb("1864AB"))]
for i, (nm, q, cond, act, fin, fl, bd, tc) in enumerate(rows):
    y = 2.15 + i * 1.18
    arrow(s, 2.8, y + 0.4, 0.25, 0.25)
    rect(s, 3.1, y, 3.35, 1.08, fl, bd, r=0.12, lw=1.5)
    text(s, 3.25, y + 0.08, 3.1, 0.95, [[(nm, {"bold": True, "size": 12.5})], [(q, {"size": 10.5})], [(cond, {"size": 8.5})]], color=tc, lsp=1.15, gap=1)
    arrow(s, 6.5, y + 0.4, 0.25, 0.25)
    rect(s, 6.8, y, 3.0, 1.08, SOFT, LINE, r=0.12)
    text(s, 6.95, y, 2.75, 1.08, [[(act, {"bold": True, "size": 11.5})]], color=INK, anchor="m")
    arrow(s, 9.84, y + 0.4, 0.25, 0.25)
    rect(s, 10.15, y, 2.58, 1.08, INK, r=0.12)
    text(s, 10.3, y, 2.3, 1.08, fin, size=10.5, bold=True, color=WHITE, anchor="m", lsp=1.2)

# ------------------------------------------------------------------ slide 7  가격 결정
s = frame(7, "가격 결정 방식", ["하루 세 구간, 두 개의 신호.", "가격은 공개된 산식으로만 움직입니다."],
          ("최대 할인율 (상한)", "≤ 38%", "0% 이상 · 잠금·예측 쿠폰을 합쳐도 38% 이내"),
          lambda s, x, y, w, h: table(s, x, y - 0.12, [1.65, 0.95, 1.05, 0.9, 0.9, 1.0, 0.85], 0.222,
                                      [["정가 · 6종 (원)", "모닝롤", "테트리스", "머핀", "스콘", "휘낭시에", "냉동생지"],
                                       ["정가", "4,500", "11,000", "1,500", "3,800", "3,800", "21,000"],
                                       ["평균 할인(15%)", "3,830", "9,350", "1,280", "3,230", "3,230", "17,850"],
                                       ["최대 할인(38%)", "2,790", "6,820", "930", "2,360", "2,360", "13,020"]], size=8.5, hl=2),
          "산식은 공개하고, 정가를 넘지 않으며, 상한은 38%로 고정합니다.",
          notes="[1분] 가격은 임의의 세일이 아니라 공개된 산식입니다. 신호는 두 개입니다. 검색지수는 수요 신호로 최대 15% 할인을 더하고, 환율은 원가 신호로 내리면 전부 돌려주고 오르면 절반만 반영합니다. "
                "합계는 0에서 38% 사이로 고정되어 정가를 넘지 않습니다. 아래 표처럼 평균 할인 15%면 모닝롤이 4,500원에서 3,830원이 됩니다.")
for (a, b, lab, fl, tc) in [(6, 16, "오전장  06:00 ~ 15:59", ACC, WHITE), (16, 26, "오후장  16:00 ~ 익일 01:59", ORG, WHITE), (26, 30, "정가 02:00~05:59", LINE, INK)]:
    x = 0.6 + (a - 6) / 24 * 12.13; w = (b - a) / 24 * 12.13 - 0.06
    rect(s, x, 2.15, w, 0.78, fl, r=0.12)
    text(s, x + 0.2, 2.2, w - 0.3, 0.3, lab, size=13 if a < 26 else 10, bold=True, color=tc)
    sub = {6: "전일 종가 기준 · 잠금 가능 · 예측 참여", 16: "당일 시가 기준 · 잠금 정산 · 예측 판정", 26: "할인 없음"}[a]
    text(s, x + 0.2, 2.52, w - 0.3, 0.3, sub, size=9.5, color=WHITE if a < 26 else INK2)
for i, (tg, tc, fl, tt, dd) in enumerate([("수요 신호", ACC2, TINT, "검색지수 × 0.15", "0~15% 할인. 많이 찾는 빵에 할인을 더해 첫 구매를 끌어옵니다."),
                                          ("원가 신호", rgb("7A5B00"), AMB2, "환율 (원/달러)", "내리면 하락률×14 전부 환원(최대 +28%), 오르면 ×7 절반만 반영합니다."),
                                          ("안전장치", rgb("0B6F55"), GRN2, "0% ~ 38% 고정", "정가를 넘지 않고, 잠금·예측 쿠폰을 합쳐도 38% 이내입니다."),
                                          ("총 할인율", WHITE, INK, "= clamp(검색 + 환율, 0, 38)", "판매가 = 정가 × (1 − 총 할인율), 10원 단위 반올림")]):
    x = 0.6 + i * 3.06
    rect(s, x, 3.12, 2.95, 2.45, fl, r=0.14)
    tag(s, x + 0.2, 3.3, tg, WHITE if i < 3 else ACC, tc if i < 3 else WHITE, w=1.0)
    text(s, x + 0.2, 3.7, 2.6, 0.7, tt, size=13.5 if i < 3 else 12, bold=True, color=INK if i < 3 else WHITE, lsp=1.15)
    text(s, x + 0.2, 4.4, 2.6, 1.1, dd, size=10.5, color=INK2 if i < 3 else rgb("D5DBE8"), lsp=1.3)

# ------------------------------------------------------------------ slide 8  할인율 분포
AM, PM = [1, 9, 37, 25, 14, 5], [1, 18, 40, 22, 8, 2]
BN = ["5% 미만", "5~10%", "10~15%", "15~20%", "20~25%", "25% 이상"]
s = frame(8, "할인율 분포", ["세션의 84%가 할인 20% 미만이고,", "25% 이상 큰 할인은 3.8%뿐입니다."],
          ("평균 할인율 (91일 · 182세션)", "15.0%", "2026.06.12 ~ 09.10 · 중앙값 13.5%"),
          ev_stats([("15.8%", "오전장 평균"), ("14.2%", "오후장 평균"), ("4.6 ~ 38%", "최저 ~ 최고(상한)"), ("3.8%", "25% 이상 세션 (7/182)")]),
          "대부분의 세션은 얕은 할인이고, 깊은 할인은 드물게만 나옵니다.",
          source="실제 가격 엔진(v1.0)에 한국은행 ECOS 원/달러 시가·종가와 일별 검색지수를 넣은 재현값 · 세션 = 하루 2회 × 91일 · 25% 이상 7세션 중 6세션은 38% 상한 · 검색지수는 6종 합산 단일 시계열",
          notes="[1분] 이 가격 엔진을 실제 환율과 검색지수로 91일 돌려 봤습니다. 하루 두 번, 182개 세션의 평균 할인율은 15%입니다. 세션의 84%가 20% 미만이고, 25% 이상 큰 할인은 7번, 3.8%뿐입니다. "
                "오전장이 오후장보다 약간 깊게 할인됩니다. 이 분포가 다음 장의 마진 방어의 근거입니다.")
card(s, 0.6, 2.15, 6.75, 3.45)
text(s, 0.85, 2.28, 4, 0.3, "구간별 세션 수", size=12, bold=True)
text(s, 5.2, 2.32, 0.9, 0.2, "■ 오전장", size=9, color=ACC); text(s, 6.1, 2.32, 1.0, 0.2, "■ 오후장", size=9, color=ORG)
base = 5.0; mh = 2.0
for i in range(6):
    x = 0.95 + i * 1.03
    for j, (v, c) in enumerate([(AM[i], ACC), (PM[i], ORG)]):
        h = v / 45 * mh
        rect(s, x + j * 0.36, base - h, 0.32, max(h, 0.03), c, r=0.04)
        text(s, x + j * 0.36 - 0.1, base - h - 0.24, 0.52, 0.22, str(v), size=9.5, bold=True, align="c")
    text(s, x - 0.15, base + 0.08, 1.05, 0.22, BN[i], size=9, bold=True, align="c")
line(s, 0.85, base, 7.15, base, LINE, 1.5)
card(s, 7.55, 2.15, 5.18, 3.45)
rows = [["구간", "오전장", "오후장", "합계", "비율", "누적"]]
cum = 0
for i in range(6):
    t = AM[i] + PM[i]; cum += t
    rows.append([BN[i], str(AM[i]), str(PM[i]), str(t), "%.1f%%" % (t / 182 * 100), "%.1f%%" % (cum / 182 * 100)])
rows.append(["합계", "91", "91", "182", "100%", ""])
table(s, 7.7, 2.3, [1.0, 0.75, 0.75, 0.7, 0.75, 0.75], 0.4, rows, size=10, hl=3)

# ------------------------------------------------------------------ slide 9  마진
s = frame(9, "마진율 방어", ["할인은 대부분 얕은 구간에 몰려 있고,", "깊은 할인은 상한 38%에서 멈춥니다."],
          ("최악 세션(38%)의 마진율", "+3.2%", "정가 마진 40% 가정 · 마진 50%면 19.4%"),
          lambda s, x, y, w, h: table(s, x, y - 0.12, [2.3, 1.85, 1.85, 1.75], 0.222,
                                      [["정가 마진 가정", "평균 할인 15%일 때", "최악 38%일 때", "손익분기 판매량"],
                                       ["40%", "29.4%", "3.2%", "+60%"], ["50%", "41.2%", "19.4%", "+43%"], ["60%", "52.9%", "35.5%", "+33%"]], size=9, hl=2),
          "정가 마진이 40% 이상이면 가장 깊은 할인 세션에서도 적자가 나지 않습니다.",
          source="※ 실제 원가·마진 자료가 없어 정가 마진율 40/50/60%를 가정한 시나리오 (마진율 = (판매가 − 원가) ÷ 판매가, 원가는 정가 기준 고정) · 손익분기 판매량 = 할인율 ÷ (마진율 − 할인율)",
          notes="[1분 30초] 걱정되는 것은 마진입니다. 첫째, 할인은 얕은 구간에 몰려 있습니다. 둘째, 합계 38%가 상한이라 더 깊어지지 않습니다. 정가 마진이 40%라고 가정해도 가장 깊은 할인 세션의 마진은 3.2%로 흑자입니다. "
                "셋째, 평균 할인 기준으로는 마진 50%일 때 판매량이 43% 늘면 본전입니다. 다만 실제 원가·마진 자료가 없어 40/50/60% 가정이라는 점, 실제 수치를 주시면 정밀 검증하겠다는 점을 말씀드립니다.")
card(s, 0.6, 2.15, 7.2, 3.45)
text(s, 0.85, 2.28, 5, 0.3, "할인율별 남는 마진율", size=12, bold=True)
text(s, 5.0, 2.32, 0.8, 0.2, "■ 60%", size=9, color=GRN); text(s, 5.7, 2.32, 0.8, 0.2, "■ 50%", size=9, color=ACC); text(s, 6.4, 2.32, 0.9, 0.2, "■ 40%", size=9, color=ORG)
cx0, cy0, cw, ch = 1.35, 2.75, 6.1, 2.35
px = lambda d: cx0 + d / 40 * cw
py = lambda m: cy0 + ch - m / 70 * ch
rect(s, px(0), cy0, px(20) - px(0), ch, TINT, r=0)
text(s, px(0), cy0 + 0.02, px(20) - px(0), 0.25, "세션의 84%", size=9.5, bold=True, color=ACC2, align="c")
for v in (0, 20, 40, 60):
    line(s, cx0, py(v), cx0 + cw, py(v), LINE, 0.75)
    text(s, cx0 - 0.5, py(v) - 0.1, 0.4, 0.2, "%d%%" % v, size=8.5, color=MUTE, align="r")
for d in (0, 10, 20, 30):
    text(s, px(d) - 0.3, cy0 + ch + 0.05, 0.6, 0.2, "%d%%" % d, size=8.5, color=MUTE, align="c")
text(s, px(38) - 0.55, cy0 + ch + 0.05, 1.1, 0.2, "할인율", size=8.5, bold=True, align="c")
line(s, px(38), cy0, px(38), cy0 + ch, ORG, 1, dash=True)
text(s, px(38) - 1.0, cy0 + 0.02, 0.95, 0.2, "상한 38%", size=8.5, bold=True, color=ORG, align="r")
for m, c in [(60, GRN), (50, ACC), (40, ORG)]:
    pts = [(x, ((1 - x / 100) - (1 - m / 100)) / (1 - x / 100) * 100) for x in range(0, 39, 2)] + [(38, ((1 - .38) - (1 - m / 100)) / (1 - .38) * 100)]
    for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
        line(s, px(x1), py(y1), px(x2), py(y2), c, 2.5)
    a = ((1 - .15) - (1 - m / 100)) / (1 - .15) * 100
    z = ((1 - .38) - (1 - m / 100)) / (1 - .38) * 100
    dot(s, px(15) - 0.06, py(a) - 0.06, 0.12, WHITE).line.color.rgb = c
    text(s, px(15) + 0.08, py(a) - 0.26, 0.6, 0.2, "%.1f%%" % a, size=8.5, bold=True)
    dot(s, px(38) - 0.06, py(z) - 0.06, 0.12, c)
    text(s, px(38) - 0.72, py(z) - 0.24, 0.62, 0.2, "%.1f%%" % z, size=8.5, bold=True, align="r")
for i, (tg, fl, tc, tt, dd) in enumerate([("방어 ① 분포", INK, WHITE, "84%가 20% 미만", "평균 할인 15.0% · 25% 이상 깊은 할인은 3.8%"),
                                          ("방어 ② 상한", TINT, INK, "38% 고정 · 정가 초과 0", "마진 40% 가정에서도 최악 세션 마진 +3.2%"),
                                          ("방어 ③ 판매량", GRN2, INK, "손익분기 +43%", "평균 할인 기준, 마진 50% → +43% · 60% → +33%")]):
    y = 2.15 + i * 1.18
    rect(s, 8.0, y, 4.73, 1.09, fl, r=0.14)
    tag(s, 8.2, y + 0.12, tg, WHITE, INK if i == 0 else (ACC2 if i == 1 else rgb("0B6F55")), w=1.15)
    text(s, 8.2, y + 0.4, 4.3, 0.3, tt, size=13, bold=True, color=tc)
    text(s, 8.2, y + 0.72, 4.3, 0.3, dd, size=9.5, color=rgb("D5DBE8") if i == 0 else INK2)

# ------------------------------------------------------------------ slide 10  MVP
s = frame(10, "MVP 범위", ["첫 버전은 두 전략을 검증하는", "기능만 담습니다."],
          ("반드시 포함(Must)", "6개", "시세 · 잠금 · 보상 · 전환 · 신뢰 · 상한 가드레일", 34),
          ev_stats([("2~3주차", "구현 — API·가격·참여·구매 이동"), ("9/28 ~ 9/30", "검증 — 오류·사용성 점검, 발표 준비"), ("6종 (승인 대기)", "MVP 상품 수 — 대표 6종 기준")]),
          "상품 수 확정만 되면 구현·검증 일정에 바로 들어갑니다.",
          notes="[1분] 첫 버전은 두 전략을 검증하는 기능만 담습니다. 반드시 포함하는 것은 시세 확인, 가격 잠금, 보상 고르기, 자사몰 전환, ‘투자가 아닙니다’ 안내, 38% 상한 가드레일입니다. "
                "도감·씰, 매수가 기준 보상, 막지스톡 안의 결제는 이번에 하지 않습니다. 구현은 2~3주차, 검증은 9월 28~30일이고, 상품 수만 확정되면 됩니다.")
rect(s, 0.6, 2.15, 5.9, 3.45, TINT, r=0.14)
tag(s, 0.85, 2.3, "MUST · 반드시 포함", WHITE, ACC2, w=1.7)
for i, (k, a, b) in enumerate([("전략1", "오전장·오후장 가격 확인", "세션 상태 표시 · 상품 상세와 할인 구성"), ("전략2", "가격 잠금", "오전장 하루 1회"), ("전략2", "오늘의 보상 고르기", "안정형 / 공격형"),
                               ("전환", "자사몰 이동·구매", "원클릭 지향"), ("신뢰", "‘투자가 아닙니다’ 안내", "가격 근거 배지"), ("안전", "38% 상한 가드레일", "")]):
    y = 2.68 + i * 0.47
    text(s, 0.85, y, 0.7, 0.4, k, size=10, bold=True, color=ACC2 if k == "전략1" else (rgb("C2410C") if k == "전략2" else INK2), anchor="m")
    text(s, 1.6, y, 4.7, 0.4, [[(a, {"bold": True}), ("   " + b, {"color": INK2, "size": 9})]], size=11, anchor="m")
rect(s, 6.7, 2.15, 3.1, 3.45, AMB2, r=0.14)
tag(s, 6.95, 2.3, "SHOULD · 여력 시", AMB, rgb("4A3600"), w=1.5)
text(s, 6.95, 2.72, 2.7, 0.6, "가격 하락·지정가 이메일 알림", size=13, bold=True, lsp=1.15)
text(s, 6.95, 3.35, 2.7, 0.6, "가격이 내려가면 알려 주어 재방문을 돕습니다.", size=10, color=INK2, lsp=1.25)
line(s, 6.95, 4.05, 9.55, 4.05, rgb("EAD9A0"))
text(s, 6.95, 4.15, 2.7, 0.3, "운영 과제", size=12, bold=True)
text(s, 6.95, 4.5, 2.7, 0.9, "화제성 콘텐츠 캘린더는 시스템이 아니라 지속 운영 프로세스로 관리합니다.", size=10, color=INK2, lsp=1.25)
rect(s, 10.0, 2.15, 2.73, 3.45, SOFT, r=0.14)
tag(s, 10.25, 2.3, "이번 범위 제외", LINE, INK2, w=1.3)
text(s, 10.25, 2.72, 2.35, 2.7, ["• 도감·씰 수집 콘텐츠", "• 매수가 기준 보상", "• 막지스톡 안에서의 결제", "• 막지스톡 자체 로그인·회원가입", "• 38% 초과 이벤트성 할인"], size=10.5, color=INK2, lsp=1.2, gap=6)

# ------------------------------------------------------------------ slide 11  KPI
s = frame(11, "KPI", ["서비스 목표와 같은 순서로", "측정합니다."],
          ("북극성 KPI · 현재 기준선", "미측정", "STOCK→자사몰 전환율 · 베타 1주차에 기준선 확보", 32),
          ev_lines("GUARDRAIL — 하나라도 초과하면 롤아웃 즉시 중단",
                   "총혜택 상한 위반 0 · 사행성 문구 0 · 표시·결제가 불일치 0 · 가격 계산 오류율 ≤ 0.1% · 쿠폰 중복 적용 0", size=10.5),
          "목표값은 근거 없이 만들지 않고, 베타 1주차 실측 후 확정합니다.",
          notes="[1분] KPI는 서비스 목표와 같은 순서입니다. 북극성 지표는 STOCK에서 잠금·보상을 고른 세션이 자사몰 구매까지 가는 비율입니다. 아직 서비스 전이라 미측정이고, 베타 첫 주에 기준선을 잡습니다. "
                "목표 숫자를 근거 없이 정하지 않는다는 원칙이라 ‘베타 실측 후 확정’이라고 적었습니다. 가드레일은 하나라도 넘으면 즉시 중단합니다.")
rect(s, 0.6, 2.15, 3.5, 3.45, ACC, r=0.14)
tag(s, 0.85, 2.3, "북극성 KPI", WHITE, ACC2, w=1.1)
text(s, 0.85, 2.7, 3.0, 0.9, ["STOCK → 자사몰", "전환율"], size=20, bold=True, color=WHITE, lsp=1.15)
text(s, 0.85, 3.85, 3.0, 0.8, "가격 잠금·보상 선택을 완료한 세션 중 자사몰 구매까지 도달한 세션의 비율", size=10.5, color=WHITE, lsp=1.3)
line(s, 0.85, 4.75, 3.85, 4.75, rgb("8FB5DA"))
text(s, 0.85, 4.85, 3.0, 0.6, "서비스 미출시로 현재 미측정", size=10.5, bold=True, color=WHITE)
card(s, 4.3, 2.15, 8.43, 3.45)
table(s, 4.45, 2.3, [1.45, 3.45, 1.85, 1.5], 0.62,
      [["목표", "지표", "현재 기준선", "목표값"],
       ["1순위 유입", "방문자 수 · 신규 가입 · 자사몰 구매 이동률", "신규가입 5월 40건", "베타 실측 후 확정"],
       ["2순위 체류", "익일 재방문율 · 세션 체류시간 · 가격 잠금 사용률", "미측정", "베타 실측 후 확정"],
       ["2순위 전환", "STOCK→자사몰 전환율 · 쿠폰 사용률 · 결제 완결률", "결제 완결률 73.5%", "기준선 확보 후"],
       ["신뢰", "안심 고지 열람률", "미측정", "≥ 50%"]], size=10, aligns=["l", "l", "l", "l"])
# left-align text columns of KPI table is handled by right alignment default; acceptable for compact numeric-ish table

# ------------------------------------------------------------------ slide 12  매출
s = frame(12, "매출 시나리오", ["KPI가 달성되면 매출은 이렇게 그려집니다 —", "점유율 확대만으로 잡은 5개년 시나리오."],
          ("Base 시나리오 · 5년차 매출", "18.8억", "1년차 5.7억 → 5년차 18.8억 (Worst 2.8억 ~ Best 35.3억)"),
          ev_stats([("13.6조원", "TAM · 국내 베이커리 시장(2025)"), ("2,100~2,650억", "SAM · 전문점×온라인×2030"), ("0.5 ~ 3%", "SAM 대비 목표 점유율")]),
          "시장이 커진다는 가정 없이, 점유율만으로 Base 18.8억을 그립니다.",
          source="시장 성장률을 얹지 않고 점유율 확대만 반영 · 망넛이네(2018년 약 5.7억)·널담(2019년 약 9.9억) 초기 실적은 ‘성공 벤치마크’로만 참고, 확정 전망이 아님",
          notes="[1분] KPI가 달성됐을 때의 매출입니다. 매출은 유입 곱하기 전환율 곱하기 객단가이고, 5월 객단가는 2.32만 원입니다. 시장이 성장한다는 가정은 넣지 않고 점유율만 0.5%에서 3%로 넓혔습니다. "
                "Base는 1년차 5.7억에서 5년차 18.8억, Worst는 2.8억, Best는 35.3억입니다. 망넛이네와 널담의 초기 실적은 확정 전망이 아니라 성공 벤치마크로만 참고했습니다.")
rect(s, 0.6, 2.15, 12.13, 0.55, TINT, r=0.12)
text(s, 0.6, 2.15, 12.13, 0.55, [[("매출", {"bold": True}), ("   =   ", {"color": ACC}), ("유입(방문자)", {"bold": True}), ("   ×   ", {"color": ACC}), ("구매 전환율", {"bold": True}), ("   ×   ", {"color": ACC}), ("객단가 ", {"bold": True}), ("(5월 2.32만원)", {"color": INK2, "size": 10})]], size=14, align="c", anchor="m")
card(s, 0.6, 2.85, 12.13, 2.75)
text(s, 0.85, 2.95, 4, 0.3, "시나리오별 연 매출 (억원)", size=12, bold=True)
text(s, 10.3, 2.99, 1.2, 0.2, "■ 1년차", size=9, color=rgb("8FB5DA")); text(s, 11.3, 2.99, 1.2, 0.2, "■ 5년차", size=9, color=ACC)
for i, (nm, a, b) in enumerate([("Worst", 1.2, 2.8), ("Base", 5.7, 18.8), ("Best", 9.9, 35.3)]):
    x = 2.0 + i * 3.4
    for j, (v, c) in enumerate([(a, LB), (b, ACC)]):
        h = v / 36 * 1.75
        rect(s, x + j * 0.95, 5.2 - h, 0.8, max(h, 0.04), c, r=0.06)
        text(s, x + j * 0.95 - 0.2, 5.2 - h - 0.27, 1.2, 0.25, str(v), size=12, bold=True, align="c")
    text(s, x - 0.2, 5.24, 2.2, 0.25, nm + "  (1년차 → 5년차)", size=10, bold=True, align="c")
    line(s, x - 0.3, 5.2, x + 2.05, 5.2, LINE, 1.25)

# ------------------------------------------------------------------ slide 13  리스크
s = frame(13, "핵심 리스크", ["구조적 제약 하나와,", "실행으로 관리 가능한 다섯 가지입니다."],
          ("핵심 리스크", "6개", "구조적 1 · HIGH 3 · 관리중 2", 34),
          ev_lines("대응 원칙", "총혜택 상한 38% 고정 · 표시가 = 결제가 일치 검증 · 할인 표시 법무 검토 · 3구간 모델 기준 백테스트 재실행"),
          "HIGH 3건(키워드·표시 불일치·법적)은 출시 전에 해소합니다.",
          notes="[1분] 리스크는 여섯 가지입니다. 막지스톡과 자사몰 결제 시스템이 분리된 것은 RFP가 정한 구조라 없앨 수 없고, 원클릭으로 줄이기만 합니다. HIGH는 세 가지 — 키워드 적합성, 표시가와 결제가 불일치, 법적 위험입니다. "
                "나머지 둘은 관리 중입니다. 총혜택 상한 38%, 표시가=결제가 검증, 법무 검토, 백테스트 재실행으로 대응합니다.")
risks = [("01", "STOCK ↔ 자사몰 구조적 분리", "RFP 요구사항 — 완전 해소 불가, 원클릭·자동인식으로 최소화만 가능", "구조적", INK, WHITE),
         ("02", "검색 키워드 적합성", "백테스트는 모닝빵 1종 중심 — 나머지 상품 키워드 검증 필요", "HIGH", ORG, WHITE),
         ("03", "표시·결제가 불일치", "STOCK 표시가와 자사몰 결제가가 다르면 신뢰·전환 훼손", "HIGH", ORG, WHITE),
         ("04", "법적 위험", "기준가격·할인율·적용기간 표시가 실제와 다르면 표시광고법 저촉 소지", "HIGH", ORG, WHITE),
         ("05", "가격모델 전환 재검증", "3구간 모델로 바뀌어 91일 백테스트 재실행 필요", "관리중", AMB, rgb("4A3600")),
         ("06", "쿠폰 중복 적용", "잠금·보상 쿠폰 동시 적용 시 총혜택 상한(38%) 초과 가능", "관리중", AMB, rgb("4A3600"))]
for i, (n, t_, d_, lv, lf, lc) in enumerate(risks):
    x = 0.6 + (i % 3) * 4.09; y = 2.15 + (i // 3) * 1.78
    card(s, x, y, 3.95, 1.66)
    rect(s, x + 0.2, y + 0.2, 0.42, 0.42, INK, r=0.1)
    text(s, x + 0.2, y + 0.2, 0.42, 0.42, n, size=11, bold=True, color=WHITE, align="c", anchor="m")
    tag(s, x + 3.95 - 0.2 - 0.85, y + 0.28, lv, lf, lc, w=0.85)
    text(s, x + 0.2, y + 0.75, 3.55, 0.3, t_, size=12.5, bold=True)
    text(s, x + 0.2, y + 1.08, 3.55, 0.55, d_, size=9.5, color=INK2, lsp=1.25)

# ------------------------------------------------------------------ slide 14  로드맵·요청
s = frame(14, "로드맵과 요청 사항", ["3단계로 구현하고,", "대표님께는 세 가지를 요청드립니다."],
          ("요청 사항", "3건", "상품 수 · 원가·마진 · 법무 검토", 34),
          ev_lines("향후 확장(설계 단계, 이번 구현 범위 아님)", "Bakery ETF · FX Bakery · Bread Index · 연속 방문 스트릭 보상"),
          "세 가지가 정해지면 바로 구현·검증 단계로 들어갑니다.",
          notes="[1분 + 요청] 로드맵은 3단계입니다. 1단계 MVP는 시세·비교·구매 이동, 2단계는 잠금·보상 고르기·알림, 3단계는 자사몰 실연동입니다. "
                "오늘 대표님께 요청드릴 것은 세 가지입니다. 하나, MVP 상품 수 확정. 둘, 실제 원가·마진율 공유 — 지금은 40/50/60% 가정이라 실제 수치로 마진 방어를 정밀 검증하겠습니다. 셋, 할인 표시에 대한 법무 검토입니다.")
line(s, 0.6, 2.42, 12.73, 2.42, LINE, 3)
for i, (ph, c, tt, dd) in enumerate([("PHASE 1", ACC, "MVP", "Bread Market — 시세 · 비교 · 구매 이동"), ("PHASE 2", AMB, "참여", "가격 잠금 · 보상 고르기 · 가격 알림"), ("PHASE 3", ORG, "연동", "자사몰 실연동 — 판매가 · 쿠폰 · 구매 데이터")]):
    x = 0.6 + i * 4.09
    dot(s, x, 2.28, 0.28, c); dot(s, x + 0.08, 2.36, 0.12, WHITE)
    tag(s, x, 2.7, ph, TINT if i == 0 else (AMB if i == 1 else ORG), ACC2 if i == 0 else (rgb("4A3600") if i == 1 else WHITE), w=0.95)
    text(s, x + 1.05, 2.66, 2.8, 0.3, tt, size=15, bold=True)
    text(s, x, 3.05, 3.9, 0.4, dd, size=10.5, color=INK2)
text(s, 0.6, 3.62, 5, 0.25, "대표님께 요청드리는 것", size=11, bold=True, color=MUTE)
for i, (n, c, fl, tt, dd) in enumerate([("01", ACC, TINT, "MVP 상품 수 확정", "대표 6종 기준으로 준비 중이며, 최종 승인이 필요합니다."),
                                        ("02", rgb("C98F00"), AMB2, "실제 원가·마진율 공유", "지금은 40/50/60% 가정입니다. 실제 수치로 마진 방어를 정밀 검증합니다."),
                                        ("03", ORG, ORG2, "할인 표시 법무 검토", "기준가격·할인율·적용기간 표시가 표시광고법에 맞는지 사전 검토가 필요합니다.")]):
    x = 0.6 + i * 4.09
    rect(s, x, 3.95, 3.95, 1.65, fl, r=0.14)
    text(s, x + 0.2, 4.03, 1, 0.5, n, size=24, bold=True, color=c)
    text(s, x + 0.2, 4.55, 3.55, 0.3, tt, size=13.5, bold=True)
    text(s, x + 0.2, 4.9, 3.55, 0.65, dd, size=10, color=INK2, lsp=1.25)

# ------------------------------------------------------------------ slide 15  Q&A
s = prs.slides.add_slide(BLANK)
rect(s, 0, 0, 0.22, 7.5, ACC, r=0)
text(s, 0.75, 0.45, 4, 0.3, [[("●  ", {"color": ACC}), ("MAKJI", {"bold": True})]], size=13, bold=True, color=INK)
text(s, 7.5, 0.45, 5.2, 0.3, "Q&A", size=10.5, bold=True, color=MUTE, align="r")
tag(s, 0.75, 2.4, "Thank you", TINT, ACC2, w=1.2, size=10)
text(s, 0.75, 2.85, 11.5, 2.2, [["가격이 움직인다는 사실 자체가,"], [("다시 찾는 이유", {"color": ACC}), ("가 됩니다.", {})]], size=44, bold=True, lsp=1.15)
text(s, 0.75, 5.2, 8, 0.4, "질문과 의견을 듣겠습니다.", size=16, color=INK2)
text(s, 0.75, 6.75, 6, 0.3, "빵값연구소   |   MAKJI STOCK", size=11, color=INK2)
s.notes_slide.notes_text_frame.text = "[Q&A] 예상 질문은 발표 스토리라인 문서의 ‘예상 질문과 답변’을 참고하세요."

OUT.parent.mkdir(parents=True, exist_ok=True)
prs.save(str(OUT))
print("saved", OUT, "slides", len(prs.slides))
