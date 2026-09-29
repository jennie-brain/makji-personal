"""MAKJI STOCK 기업 대표 보고 덱 v7.0 (편집 가능한 PPTX).

- 기준: 사용자가 수정한 v5.0(18장: 사용자 여정 상세 3장 추가, 마진 슬라이드 제외)
- 헤드라인은 한 줄, 포인트 색은 블루(#4087C7) + 빵색 연갈색, 숫자는 검증된 출처만 사용
- 사용자 여정 상세(8~10번)는 하단을 앱 화면 목업 자리로 비워 둔다
"""
from pathlib import Path

from lxml import etree
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_CONNECTOR, MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Inches, Pt

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "04_presentations" / "막지스톡_기업대표_서비스기획_발표v7.0.pptx"

FONT = "Noto Sans KR"
rgb = lambda h: RGBColor.from_string(h.lstrip("#").upper())
# palette — blue(primary) + bread(secondary) + neutrals
ACC, ACC2, TINT, LB = rgb("4087C7"), rgb("2F6FAD"), rgb("EAF2FA"), rgb("BFD6EC")
BREAD, BREAD2, BREAD_T, BREAD_L = rgb("C9A06F"), rgb("8A6238"), rgb("F6EEE3"), rgb("E8D9C3")
GRN, GRN2, GRN_T = rgb("10A37F"), rgb("0B6F55"), rgb("E3F6F0")
INK, INK2, MUTE, LINE, WHITE = rgb("161A23"), rgb("4B5563"), rgb("6B7280"), rgb("E7E1D8"), rgb("FFFFFF")
PANEL, PANEL_L = rgb("F9F6F1"), rgb("FCFAF7")

N = 18
L, RIGHT = 0.8, 12.53
W = RIGHT - L

prs = Presentation()
prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
BLANK = prs.slide_layouts[6]


# ------------------------------------------------------------------ helpers
def shadow(sh, blur=14, dist=3, alpha=9):
    sp = sh._element.spPr
    for e in sp.findall(qn("a:effectLst")):
        sp.remove(e)
    eff = etree.SubElement(sp, qn("a:effectLst"))
    sd = etree.SubElement(eff, qn("a:outerShdw"), blurRad=str(int(blur * 12700)), dist=str(int(dist * 12700)),
                          dir="5400000", algn="t", rotWithShape="0")
    c = etree.SubElement(sd, qn("a:srgbClr"), val="1B1B1F")
    etree.SubElement(c, qn("a:alpha"), val=str(alpha * 1000))


def rect(s, x, y, w, h, fill=None, line=None, r=0.12, lw=0.75, shape=None, shd=False):
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
    if shd:
        shadow(sh)
    return sh


def _runs(p, content, size, bold, color):
    for part in (content if isinstance(content, list) else [content]):
        txt, o = (part, {}) if isinstance(part, str) else part
        r = p.add_run(); r.text = txt
        f = r.font; f.name = FONT; f.size = Pt(o.get("size", size)); f.bold = o.get("bold", bold)
        f.color.rgb = o.get("color", color)


def text(s, x, y, w, h, content, size=12, bold=False, color=INK, align="l", anchor="t", lsp=1.2, gap=0):
    tb = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame; tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = {"t": MSO_ANCHOR.TOP, "m": MSO_ANCHOR.MIDDLE, "b": MSO_ANCHOR.BOTTOM}[anchor]
    paras = content.split("\n") if isinstance(content, str) else (
        content if content and isinstance(content[0], (list, str)) else [content])
    for i, para in enumerate(paras):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = {"l": PP_ALIGN.LEFT, "c": PP_ALIGN.CENTER, "r": PP_ALIGN.RIGHT}[align]
        p.line_spacing = lsp
        if i:
            p.space_before = Pt(gap)
        _runs(p, para, size, bold, color)
    return tb


def line(s, x1, y1, x2, y2, color=LINE, w=1.0, dash=False):
    c = s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(x1), Inches(y1), Inches(x2), Inches(y2))
    c.line.color.rgb = color; c.line.width = Pt(w)
    sp = c._element.spPr
    if sp.find(qn("a:effectLst")) is None:
        etree.SubElement(sp, qn("a:effectLst"))
    if dash:
        c.line.dash_style = 4
    return c


def dot(s, x, y, d, fill):
    return rect(s, x, y, d, d, fill, r=0, shape=MSO_SHAPE.OVAL)


def panel(s, x, y, w, h, fill=PANEL, line_c=None):
    return rect(s, x, y, w, h, fill, line_c, r=0.16)


def card(s, x, y, w, h, fill=WHITE, line_c=LINE):
    return rect(s, x, y, w, h, fill, line_c, r=0.16, shd=True)


def pill(s, x, y, w, txt, fill=ACC, color=WHITE, size=12, h=0.34, bold=True):
    rect(s, x, y, w, h, fill, r=h / 2)
    text(s, x, y, w, h, txt, size=size, bold=bold, color=color, align="c", anchor="m")


def arrow(s, x, y, w=0.28, color=ACC, size=16):
    text(s, x, y, w, 0.4, "→", size=size, bold=True, color=color, align="c", anchor="m")


def frame(kicker, headline, sowhat, source=None, notes=""):
    s = prs.slides.add_slide(BLANK)
    idx = len(prs.slides)
    dot(s, L, 0.575, 0.09, BREAD)
    text(s, L + 0.2, 0.5, 8, 0.28, kicker, size=11, bold=True, color=ACC2)
    text(s, L, 0.86, W, 0.62, headline, size=26, bold=True, color=INK, anchor="m")
    if sowhat:
        rect(s, RIGHT - 0.42, 6.42, 0.42, 0.045, ACC, r=0)
        text(s, 3.0, 6.55, RIGHT - 3.0, 0.4, sowhat, size=14, bold=True, color=ACC2, align="r")
    if source:
        text(s, L, 7.02, 10.6, 0.3, source, size=8, color=MUTE, lsp=1.1)
    text(s, 11.0, 7.05, RIGHT - 11.0, 0.2, "%02d / %d" % (idx, N), size=9, color=MUTE, align="r")
    if notes:
        s.notes_slide.notes_text_frame.text = notes
    return s


def bar_chart(s, x, base, maxh, vmax, data, bw, gap, lab=15):
    for i, (cat, sub, v, c, lb) in enumerate(data):
        bx = x + i * (bw + gap); h = v / vmax * maxh
        rect(s, bx, base - h, bw, h, c, r=0.05)
        text(s, bx - 0.3, base - h - 0.36, bw + 0.6, 0.3, lb, size=lab, bold=True, align="c")
        text(s, bx - 0.3, base + 0.1, bw + 0.6, 0.25, cat, size=12, bold=True, align="c")
        if sub:
            text(s, bx - 0.3, base + 0.35, bw + 0.6, 0.22, sub, size=10, color=MUTE, align="c")
    line(s, x - 0.3, base, x + len(data) * (bw + gap) - gap + 0.3, base, LINE, 1.5)


NOTES = {
    2: "[핵심] 온라인 베이커리 시장은 3년 만에 70% 가까이 커졌습니다.\n"
       "[근거] aT 자료로 2021년 3,200억에서 2024년 5,400억이 됐습니다. 유사한 업체도 성장 중인데, 신세계푸드의 온라인 베이커리 매출은 2023년 255억에서 2025년 850억으로 3.3배가 됐고, 저당 베이커리 널담은 2025년 매출 약 330억으로 전년의 2배, 2026년 목표는 800억입니다. 수요 배경으로 성인의 65%가 체중을 줄이거나 유지하려 시도합니다(질병관리청 2024 지역사회건강조사). 참고로 기사에는 2025년 시장이 6,250억으로 ‘추산’된다고 나와 있으나, 추산치라 슬라이드에는 넣지 않았습니다.\n"
       "[연결] 이 성장 시장에서 막지도 B2B를 넘어 자사몰(B2C)로 성장축을 넓히고 있습니다. 그런데 자사몰을 열어 보니 문제가 보였습니다.",
    3: "[핵심] 그런데 막지 자사몰은 아침에 둘러보고 저녁에 삽니다. 방문과 구매의 시점이 어긋납니다.\n"
       "[멘트] 출근길엔 눈으로 장바구니를 채우고, 퇴근하고 나서야 지갑이 열린다는 얘기입니다.\n"
       "[근거] 5월 데이터에서 로그인은 오전 8~10시에 25.6%가 몰렸지만 그 시간 결제금액은 8.0%뿐이고, 저녁 20~24시에는 로그인 20.0%에 결제금액 28.4%입니다. 막지는 저당·무설탕·글루텐프리 웰니스 베이커리로 B2B에서 제품력을 검증했지만, 자사몰에서는 관심이 생긴 순간 구매로 이어지지 못하고 있습니다.\n"
       "[연결] 이것이 풀어야 할 문제입니다. 그래서 목표를 이렇게 세웠습니다.",
    4: "[핵심] 그래서 목표는 두 단계입니다. 먼저 방문을 늘리고, 방문한 고객을 한 걸음에 구매까지 잇습니다.\n"
       "[멘트] 손님이 구경하고 결제하기까지 대략 열두 시간이 비어 있는 셈입니다.\n"
       "[근거] 첫째 자사몰 유입이 최우선입니다. 광고를 켠 날에만 팔리는 구조가 아니라 고객이 스스로 찾아오게 합니다. 둘째 체류시간과 전환율입니다. 가격을 확인하고 비교하다가 구매까지 가게 합니다.\n"
       "[연결] 그러면 무엇이 매일 오게 하고, 살 때까지 붙잡아 줄까요?",
    5: "[핵심] 그 답이 막지스톡입니다. 가격이 방문의 이유가 되고, 고르는 혜택이 구매까지 붙잡습니다.\n"
       "[멘트] ‘빵값을 주식처럼’이라고 하면 투자를 떠올리실 수 있는데, 빵에 투자하시라는 얘기가 아닙니다. 더 싸게 사는 타이밍을 알려 드린다는 뜻입니다. 투자가 아니라 할인입니다.\n"
       "[근거] 전략 하나, 가격 자체를 콘텐츠로 — 빵값이 하루 두 번 바뀌어 ‘오늘은 얼마일까?’가 방문 이유가 됩니다. 전략 둘, 고객이 직접 고르는 혜택 — 잠금이나 예측 중 원하는 방식으로 혜택을 받아 주도성을 느낍니다. 경쟁 6곳 중 가격 변동 자체를 콘텐츠로 쓰는 곳은 아직 없습니다.\n"
       "[연결] 이것이 하루 안에서 어떻게 돌아가는지 보겠습니다.",
    6: "[핵심] 아침에 본 가격을 잠그면 저녁 결제까지 이어집니다.\n"
       "[멘트] 쉽게 말해 잠금은 ‘이 가격에 찜’입니다. 아침에 점찍은 빵을 저녁에 더 비싸게 만나지 않게 해 드립니다.\n"
       "[근거] 6시 오전장에서 시세를 보고 빵 하나를 잠급니다. 16시 오후장에서 잠금이 정산되고 자사몰에서 결제합니다. 다음 날 6시에는 예측 결과를 보러 다시 옵니다. 6시와 16시는 5월에 확인한 로그인 피크(8~10시)와 결제 피크(20~24시) 직전입니다. 시간에 따라 가격이 달라지는 경험은 이미 익숙합니다. 2026년 6월 15일부터 배달앱 3사가 저녁 시간대 마감할인(20% 이상)을 시작했습니다.\n"
       "[연결] 그런데 고객마다 구매 의사가 다릅니다.",
    7: "[핵심] 고객 상황에 따라 길은 세 가지이고, 모두 자사몰 결제로 이어집니다.\n"
       "[근거] 세로로는 고객 유형, 가로로는 시간입니다. 즉시 구매형은 오전장에서 확인하고 바로 결제합니다. 가격 확보형은 오전가를 잠그고 오후장에서 잠근 가격으로 결제합니다. 관망·기대형은 내일 가격을 예측하고, 다음 날 아침 결과를 확인해 쿠폰으로 결제합니다. 잠금은 가격 상승 위험을 없애고, 예측은 내일 다시 오게 만듭니다.\n"
       "[연결] 유형별로 실제 화면에서 어떻게 보이는지 차례로 보겠습니다.",
    8: "[핵심] 즉시 구매형은 이 가격이면 그 자리에서 삽니다.\n[근거] 오늘 가격을 확인하고, 마음에 들면 오늘 가격으로 바로 자사몰에서 결제합니다. (앱 화면 목업 삽입)\n[연결] 이번엔 결제는 나중에 하고 싶은 고객입니다.",
    9: "[핵심] 가격 확보형은 오전가를 잠그고, 저녁에 결제합니다.\n[근거] 가격은 마음에 드는데 지금 결제할 수 없는 고객입니다. 오전장에서 가격을 잠가 두면 오후에 가격이 올라도 잠근 가격으로 결제하고, 내려가면 더 싼 가격이 적용됩니다. (앱 화면 목업 삽입)\n[연결] 마지막은 더 싸지길 기다리는 고객입니다.",
    10: "[핵심] 관망·기대형은 내일 가격을 예측하고, 쿠폰으로 삽니다.\n[근거] 더 싸지면 사고 싶은 고객은 오늘 내일의 가격을 예측해 두고, 다음 날 아침 결과를 확인한 뒤 받은 쿠폰을 적용해 결제합니다. 결과가 궁금해서 내일 다시 오게 됩니다. (앱 화면 목업 삽입)\n[연결] 이 모든 길이 통하려면 먼저 가격을 믿을 수 있어야 합니다.",
    11: "[핵심] 가격을 믿을 수 있어야 하므로, 가격은 공개된 산식으로만 움직입니다.\n"
        "[멘트] 가격이 매일 바뀌면 ‘나만 모르고 비싸게 샀나’ 싶으실 수 있습니다. 그래서 왜 바뀌는지를 아예 공개합니다.\n"
        "[근거] 신호는 두 개입니다. 검색지수(수요)는 최대 15% 할인을 더하고, 환율(원가)은 내리면 하락률의 14배를 전부 돌려주고 오르면 7배, 절반만 반영합니다. 합계는 0~38%로 고정되어 정가를 넘지 않습니다. 원가 변화는 실제로 빵값에 반영되고 있습니다. 삼립은 2026년 9월부터 빵 50여 종 가격을 평균 9% 올렸습니다. 모닝롤은 정가 4,500원이 평균 할인에서 3,830원, 최대 할인에서 2,790원입니다.\n"
        "[연결] 그렇다면 실제로 얼마나 할인될까요? 91일을 돌려 봤습니다.",
    12: "[핵심] 실제로 91일을 돌려 보니 평균 할인은 15%, 세션의 84%가 20% 미만이었습니다.\n"
        "[멘트] 매일이 대박 세일은 아닙니다. 25%를 넘는 날은 182번 중 7번입니다.\n"
        "[근거] 하루 두 번, 182개 세션입니다. 오전장 평균 15.8%, 오후장 14.2%이고, 25% 이상 큰 할인은 7번, 3.8%뿐입니다. 상한 38%가 깊은 할인을 막습니다. (마진 검증은 실제 원가 자료를 받은 뒤 별도로 보여 드리겠습니다.)\n"
        "[연결] 이 가격 구조가 통하는지, 꼭 필요한 기능만으로 먼저 검증하겠습니다.",
    13: "[핵심] 첫 버전은 두 전략을 검증하는 기능만 담습니다.\n"
        "[근거] 시세 확인, 가격 잠금, 보상 고르기, 자사몰 전환, ‘투자가 아닙니다’ 안내, 38% 상한 가드레일이 필수이고, 가격 하락 이메일 알림은 여력이 되면 넣습니다. 도감·씰, 매수가 기준 보상, 막지스톡 안의 결제는 이번에 하지 않습니다. 구현은 2~3주, 검증은 9월 28~30일이고 상품 수(대표 6종 기준)만 확정되면 됩니다.\n"
        "[연결] 검증한다면 무엇으로 판단할까요?",
    14: "[핵심] 서비스 목표와 같은 순서로 측정합니다.\n"
        "[근거] 북극성은 STOCK에서 잠금·보상을 고른 세션이 자사몰 구매까지 가는 전환율이고, 아직 미측정이라 베타 첫 주에 기준선을 잡습니다. 유입은 방문자·신규 가입(5월 40건), 체류는 재방문율·체류시간, 전환은 쿠폰 사용률·결제 완결률(5월 73.5%)입니다. 목표값은 근거 없이 정하지 않고 베타 실측 후 확정하며, 가드레일은 하나라도 넘으면 즉시 중단합니다.\n"
        "[연결] 이 지표가 달성되면 매출은 어떻게 될까요?",
    15: "[핵심] 지표가 달성되면 Base 시나리오로 5년 뒤 매출은 18.8억입니다.\n"
        "[멘트] 숫자는 일부러 낙관적으로 그리지 않았습니다. 시장이 커진다는 가정은 뺐습니다.\n"
        "[근거] 매출은 유입 × 전환율 × 객단가(5월 2.32만 원)입니다. 시장 성장은 넣지 않고 점유율만 넓힌 시나리오이며, Worst 2.8억, Best 35.3억입니다. 참고로 Base 18.8억은 2024년 온라인 베이커리 시장 5,400억의 약 0.35%입니다. 망넛이네·널담의 초기 실적은 확정 전망이 아닌 성공 벤치마크입니다.\n"
        "[연결] 이 그림에는 리스크가 있습니다.",
    16: "[핵심] 리스크는 구조적 제약 하나와 관리 가능한 다섯 가지입니다.\n"
        "[멘트] 리스크는 숨기지 않고 먼저 말씀드리겠습니다.\n"
        "[근거] 막지스톡과 자사몰 결제가 분리된 것은 RFP가 정한 구조라 원클릭·자동 인식으로 줄이기만 합니다. HIGH는 키워드 적합성, 표시가·결제가 불일치, 법적 위험 세 가지이고, 나머지 둘(가격모델 재검증, 쿠폰 중복)은 관리 중입니다. 대응은 상한 38%, 표시가=결제가 검증, 법무 검토, 백테스트 재실행입니다.\n"
        "[연결] 그래서 대표님께 세 가지를 요청드립니다.",
    17: "[핵심] 그래서 세 가지를 요청드립니다. MVP 상품 수 확정, 실제 원가·마진율 공유, 할인 표시 법무 검토입니다.\n"
        "[멘트] 요청은 세 가지입니다. 하나씩 여쭙겠습니다.\n"
        "[근거] 실제 원가·마진 수치를 주시면 마진 방어를 정밀 검증해 보여 드리겠습니다. 로드맵은 MVP, 참여 기능, 자사몰 실연동의 3단계입니다. 향후 확장(Bakery ETF·FX Bakery·Bread Index)은 설계 단계입니다.\n"
        "[연결] 질문을 받겠습니다.",
}

# ------------------------------------------------------------------ 1 표지
s = prs.slides.add_slide(BLANK)
rect(s, 0, 0, 0.22, 7.5, ACC, r=0)
rect(s, 9.3, -1.6, 5.4, 5.4, BREAD_T, r=0, shape=MSO_SHAPE.OVAL)
rect(s, 10.7, 4.6, 3.6, 3.6, TINT, r=0, shape=MSO_SHAPE.OVAL)
dot(s, L, 0.62, 0.11, BREAD)
text(s, L + 0.22, 0.52, 4, 0.3, "MAKJI", size=13, bold=True, color=INK)
text(s, 7.5, 0.52, 5.03, 0.3, "BUSINESS PROPOSAL 2026", size=10.5, bold=True, color=MUTE, align="r")
text(s, L, 2.25, 8, 2.6, [[("MAKJI", {})], [("STOCK", {"color": ACC})]], size=80, bold=True, color=INK, lsp=0.95)
text(s, L, 5.0, 9, 0.9, ["웰니스 베이커리 막지의 B2C 확장 —", "매일 두 번 움직이는 빵값으로 자사몰의 방문과 구매를 만듭니다."], size=16, color=INK2, lsp=1.45)
text(s, L, 6.75, 6, 0.3, "빵값연구소  |  기업 대표 보고", size=11, color=INK2)
text(s, 6.9, 6.75, 5.63, 0.3, "2026.09", size=11, color=INK2, align="r")
s.notes_slide.notes_text_frame.text = ("[오프닝 멘트] 주식 앱은 하루에도 몇 번씩 열어 보시죠? 빵값은 어떨까요? 오늘은 그 이야기를 해 보려고 합니다.\n"
                                       "[핵심] 오늘 말씀드릴 것은 세 가지입니다. 시장에 기회가 있고, 우리는 그 기회를 ‘가격’으로 잡으려 하며, 그 방식이 통한다는 것입니다. 마지막에 세 가지 요청을 드리겠습니다.")

# ------------------------------------------------------------------ 2 시장 기회
s = frame("시장 기회", "온라인 베이커리 시장은 3년 만에 70% 가까이 커졌습니다",
          "성장하는 온라인 시장 — 이 수요를 어떻게 가져올지가 우리의 과제입니다.",
          source="출처: aT(매일경제 2026.03.23) — 시장 규모·신세계푸드 · 머니투데이 2026.01.21 — 널담 · 질병관리청 「2024 지역사회건강조사」(2026.05.16 발표). 2025년 시장 6,250억원은 기사상 ‘추산’이라 제외",
          notes=NOTES[2])
panel(s, L, 1.8, 5.75, 3.0); panel(s, 6.78, 1.8, 5.75, 3.0)
text(s, L + 0.3, 1.97, 5, 0.3, "국내 온라인 베이커리 시장 (억원)", size=12, bold=True, color=INK2)
bar_chart(s, 1.75, 4.25, 1.45, 5600, [("2021", "", 3200, LB, "3,200"), ("2024", "", 5400, ACC, "5,400")], 1.35, 0.95, lab=16)
pill(s, L + 0.3, 2.42, 1.15, "+69%")
text(s, L + 1.55, 2.42, 2.4, 0.34, "3년 만에", size=11.5, color=MUTE, anchor="m")
text(s, 7.08, 1.97, 5.3, 0.3, "신세계푸드 온라인 베이커리 매출 (억원)", size=12, bold=True, color=INK2)
bar_chart(s, 7.7, 4.25, 1.45, 850, [("2023", "", 255, LB, "255"), ("2024", "", 310, LB, "310"), ("2025", "", 850, ACC, "850")], 1.0, 0.65, lab=15)
pill(s, 7.08, 2.42, 1.15, "3.3배")
text(s, 8.33, 2.42, 2.4, 0.34, "2023 → 2025", size=11.5, color=MUTE, anchor="m")
for i, (big, unit, body) in enumerate([("2배", "", "널담 2025년 매출 약 330억원 — 전년 대비 2배 성장, 2026년 목표 800억원"),
                                        ("65.0", "%", "성인이 체중을 줄이거나 유지하려 시도 — 웰니스 수요의 배경")]):
    x = L + i * 5.98
    card(s, x, 5.0, 5.75, 1.2)
    text(s, x + 0.3, 5.0, 1.6, 1.2, [[(big, {"size": 34, "bold": True, "color": ACC2}), (unit, {"size": 18, "bold": True, "color": ACC2})]], anchor="m")
    text(s, x + 1.95, 5.0, 3.6, 1.2, body, size=12, color=INK2, anchor="m", lsp=1.35)

# ------------------------------------------------------------------ 3 현상
s = frame("현상 · 자사몰 5월 데이터", "그런데 자사몰은 아침에 둘러보고, 저녁에 삽니다",
          "방문이 구매로 이어지지 못하는 것이 자사몰의 핵심 문제입니다.",
          source="출처: 막지 자사몰 5월 시간별 분석 (로그인 90회 · 결제금액 기준, 단일상품 막지 ZERO 카스테라)",
          notes=NOTES[3])
panel(s, L, 1.8, W, 4.4)
text(s, L + 0.3, 1.98, 8, 0.3, "시간대별 로그인 비중 vs 결제금액 비중", size=12, bold=True, color=INK2)
text(s, 9.6, 1.96, 2.7, 0.25, "■ 로그인", size=11, color=ACC, align="r")
text(s, 9.6, 2.22, 2.7, 0.25, "■ 결제금액", size=11, color=BREAD2, align="r")
base = 5.35; mh = 2.2
for gi, (nm, sub, a, b) in enumerate([("오전 8~10시", "아침에 둘러보고", 25.6, 8.0), ("저녁 20~24시", "저녁에 삽니다", 20.0, 28.4)]):
    x = 2.5 + gi * 5.1
    for j, (v, c) in enumerate([(a, ACC), (b, BREAD)]):
        h = v / 30 * mh
        rect(s, x + j * 1.5, base - h, 1.25, h, c, r=0.05)
        text(s, x + j * 1.5 - 0.2, base - h - 0.42, 1.65, 0.38, "%s%%" % v, size=19, bold=True, align="c")
    text(s, x - 0.2, base + 0.12, 3.15, 0.3, nm, size=13, bold=True, align="c")
    text(s, x - 0.2, base + 0.42, 3.15, 0.3, sub, size=12, color=MUTE, align="c")
line(s, L + 0.3, base, RIGHT - 0.3, base, LINE, 1.5)

# ------------------------------------------------------------------ 4 서비스 목표
s = frame("서비스 목표", "그래서 목표는 방문을 늘리고, 한 걸음에 구매까지 잇는 것",
          "매일 오게 하고, 살 때까지 붙잡을 방법이 필요합니다.", notes=NOTES[4])
card(s, L, 1.85, 5.75, 2.55)
card(s, 6.78, 1.85, 5.75, 2.55)
for i, (n, c, tt, dd) in enumerate([("1", ACC, "자사몰 유입 증가", "광고를 켠 날에만 팔리는 구조에서 벗어나\n고객이 스스로 찾아오게 합니다."),
                                    ("2", BREAD, "체류시간 ↑ · 전환율 ↑", "가격을 확인·비교하며 머무르고\n탐색한 뒤 자사몰 구매까지 이어지게 합니다.")]):
    x = L + 0.35 + i * 5.98
    tag_c = TINT if i == 0 else BREAD_T
    pill(s, x, 2.08, 1.1, "우선순위 %s" % n, tag_c, ACC2 if i == 0 else BREAD2, size=10.5, h=0.3)
    text(s, x, 2.5, 5.2, 0.5, tt, size=22, bold=True)
    rect(s, x, 3.1, 0.5, 0.05, c, r=0)
    text(s, x, 3.3, 5.2, 0.9, dd, size=12.5, color=INK2, lsp=1.45)
panel(s, L, 4.65, W, 1.3, PANEL)
for i, (t1, c) in enumerate([("유입", ACC), ("체류 · 가격 확인", ACC), ("탐색 · 지금 살까?", ACC), ("구매", INK)]):
    x = L + 0.45 + i * 2.9
    dot(s, x, 5.2, 0.22, c)
    text(s, x + 0.36, 5.1, 2.1, 0.42, t1, size=14, bold=True, anchor="m")
    if i < 3:
        arrow(s, x + 2.2, 5.1, 0.5, ACC, 18)

# ------------------------------------------------------------------ 5 전략·솔루션
s = frame("세부 전략과 솔루션 — 그 답이 막지스톡", "가격이 방문 이유가 되고, 고르는 혜택이 구매를 붙잡습니다",
          "두 전략이 방문(유입)과 구매(전환)를 동시에 겨냥합니다.", notes=NOTES[5])
card(s, L, 1.85, 5.75, 1.95, fill=WHITE)
card(s, 6.78, 1.85, 5.75, 1.95, fill=WHITE)
for i, (n, c, tt, dd) in enumerate([("1", ACC, "가격 자체를 콘텐츠로", "매일 두 번 바뀌는 빵값이 ‘오늘은 얼마일까?’라는\n방문 이유가 됩니다."),
                                    ("2", BREAD, "고객이 직접 고르는 혜택", "잠금 또는 보상 고르기 — 내가 원하는 방식으로\n혜택을 받고, 주도성을 느낍니다.")]):
    x = L + 0.35 + i * 5.98
    rect(s, x, 2.1, 0.55, 0.55, TINT if i == 0 else BREAD_T, r=0.28)
    text(s, x, 2.1, 0.55, 0.55, n, size=20, bold=True, color=ACC2 if i == 0 else BREAD2, align="c", anchor="m")
    text(s, x + 0.75, 2.12, 4.4, 0.5, tt, size=19, bold=True, anchor="m")
    text(s, x, 2.9, 5.2, 0.8, dd, size=12, color=INK2, lsp=1.45)
text(s, 6.4, 3.85, 0.6, 0.4, "↓", size=22, bold=True, color=ACC, align="c")
rect(s, L, 4.3, W, 1.95, ACC, r=0.18)
text(s, L, 4.4, W, 0.9, "MAKJI STOCK", size=40, bold=True, color=WHITE, align="c", anchor="m")
text(s, L, 5.3, W, 0.32, "빵값을 주식시장처럼 — 하루 두 번 열리는 시세를 보고, 내 방식대로 혜택을 골라 자사몰에서 삽니다.", size=12.5, color=WHITE, align="c")
text(s, L, 5.72, W, 0.3, "경쟁 6곳 중 가격 변동 자체를 콘텐츠로 쓰는 곳은 아직 없습니다", size=11.5, bold=True, color=rgb("DCEAF7"), align="c")

# ------------------------------------------------------------------ 6 서비스 소개
s = frame("서비스 소개", "아침에 본 가격을 잠그면, 저녁 결제까지 이어집니다",
          "아침 관심과 저녁 결제 사이의 간극을 ‘잠금’이 메웁니다.",
          source="출처: 기후에너지환경부·배달 플랫폼 ‘마감할인’ 개시(머니투데이 2026.06.15, 2026.06.14 보도)",
          notes=NOTES[6])
panel(s, L, 1.85, W, 2.3, PANEL)
line(s, 1.9, 2.4, 11.45, 2.4, LINE, 2.5)
for i, (tm, ds, c) in enumerate([("06:00", "오전장 개장 · 시세 확인", ACC), ("오전장 중", "가격 잠금 (하루 1회)", BREAD), ("16:00", "오후장 개장 · 잠금 정산", ACC), ("구매", "막지 자사몰에서 결제", INK), ("익일 06:00", "예측 결과 확인", BREAD)]):
    cx = 1.9 + i * 2.39
    dot(s, cx - 0.14, 2.26, 0.28, c)
    text(s, cx - 1.1, 2.68, 2.2, 0.3, tm, size=14, bold=True, align="c")
    text(s, cx - 1.1, 3.04, 2.2, 0.3, ds, size=11, color=INK2, align="c")
line(s, L + 0.35, 3.62, RIGHT - 0.35, 3.62, LINE, 0.75)
text(s, L + 0.35, 3.7, W - 0.7, 0.3, [[("이미 익숙한 경험  ", {"bold": True, "color": BREAD2}), ("2026.06.15부터 배달앱 3사가 저녁 시간대 마감할인(20% 이상)을 시작했습니다", {"color": INK2})]], size=11)
for i, (c, tt, dd) in enumerate([(ACC, "오늘의 시세", "6종의 가격과 할인율을\n하루 두 번 공개합니다."),
                                  (BREAD, "가격 잠금", "오전가를 하루 1개 잠그면\n오후에 올라도 그 가격입니다."),
                                  (BREAD, "오늘의 보상 고르기", "안정형은 즉시 확정 쿠폰,\n공격형은 내일 예측에 도전합니다.")]):
    x = L + i * 3.95
    card(s, x, 4.35, 3.8, 1.85)
    rect(s, x + 0.3, 4.6, 0.5, 0.06, c, r=0)
    text(s, x + 0.3, 4.78, 3.3, 0.4, tt, size=17, bold=True)
    text(s, x + 0.3, 5.3, 3.3, 0.8, dd, size=12, color=INK2, lsp=1.4)

# ------------------------------------------------------------------ 7 사용자 여정 (언제·무엇을)
s = frame("사용자 여정 — 구매 의사별", "고객 상황에 따라 길은 세 가지, 모두 결제로 이어집니다",
          "잠금과 예측은 구매를 미루는 장치가 아니라 유리한 구매를 보장합니다.", notes=NOTES[7])
COLX = [3.25, 6.33, 9.41]; COLW = 3.0
for i, (tm, sub) in enumerate([("오늘 오전장", "06:00 ~ 15:59"), ("오늘 오후장", "16:00 ~"), ("내일 아침", "06:00 ~")]):
    x = COLX[i]
    dot(s, x, 1.86, 0.17, ACC if i < 2 else BREAD)
    text(s, x + 0.27, 1.79, 1.5, 0.3, tm, size=12.5, bold=True)
    text(s, x + 1.5, 1.82, 1.5, 0.3, sub, size=10.5, color=MUTE)
    if i:
        line(s, x - 0.14, 1.85, x - 0.14, 5.85, LINE, 0.75, dash=True)
personas = [("즉시 구매형", "“이 가격 완벽해!”", GRN, GRN_T, GRN2), ("가격 확보형", "“가격은 좋은데 결제는 이따가!”", BREAD, BREAD_T, BREAD2), ("관망·기대형", "“오후장에 더 싸지면 살래”", ACC, TINT, ACC2)]
for r_, (nm, q, c, ct, cd) in enumerate(personas):
    y = 2.3 + r_ * 1.2
    panel(s, L, y, W, 1.05, PANEL)
    rect(s, L + 0.15, y + 0.13, 2.15, 0.79, ct, c, r=0.14, lw=1.25)
    text(s, L + 0.3, y + 0.13, 1.95, 0.79, [[(nm, {"bold": True, "size": 13, "color": cd})], [(q, {"size": 9.5, "color": cd})]], anchor="m", lsp=1.2)


def node(x, y, w, label, fill=WHITE, border=LINE, color=INK, bold=True, size=11):
    rect(s, x, y, w, 0.6, fill, border, r=0.16, lw=1.0)
    text(s, x, y, w, 0.6, label, size=size, bold=bold, color=color, align="c", anchor="m")


def ynode(r_): return 2.3 + r_ * 1.2 + 0.225


# row 1 — 즉시 구매형 (오전장에서 끝)
node(COLX[0], ynode(0), 1.28, "가격 확인"); arrow(s, COLX[0] + 1.26, ynode(0) + 0.1, 0.32)
node(COLX[0] + 1.6, ynode(0), 1.28, "바로 결제 ✓", INK, INK, WHITE)
text(s, COLX[1], ynode(0), COLW - 0.3, 0.6, "그날 안에 끝", size=10.5, color=MUTE, anchor="m")
# row 2 — 가격 확보형
node(COLX[0], ynode(1), 1.28, "가격 확인"); arrow(s, COLX[0] + 1.26, ynode(1) + 0.1, 0.32)
node(COLX[0] + 1.6, ynode(1), 1.28, "가격 잠금", BREAD_T, BREAD, BREAD2)
arrow(s, COLX[0] + 2.86, ynode(1) + 0.1, 0.42, BREAD)
node(COLX[1] + 0.1, ynode(1), 2.4, "잠근 가격으로 결제 ✓", INK, INK, WHITE)
text(s, COLX[1] + 0.1, ynode(1) + 0.63, 2.8, 0.22, "오르면 잠근 가격, 내리면 더 싼 가격", size=8.5, color=MUTE)
# row 3 — 관망·기대형
node(COLX[0], ynode(2), 1.28, "가격 확인"); arrow(s, COLX[0] + 1.26, ynode(2) + 0.1, 0.32)
node(COLX[0] + 1.6, ynode(2), 1.28, "내일 예측", TINT, ACC, ACC2)
line(s, COLX[0] + 2.95, ynode(2) + 0.3, COLX[2] - 0.05, ynode(2) + 0.3, ACC, 1.25, dash=True)
text(s, COLX[1] + 0.2, ynode(2) - 0.12, 2.6, 0.24, "하룻밤 지나면", size=9, color=MUTE, align="c")
node(COLX[2] + 0.05, ynode(2), 1.28, "결과 확인"); arrow(s, COLX[2] + 1.31, ynode(2) + 0.1, 0.32)
node(COLX[2] + 1.65, ynode(2), 1.25, "쿠폰 결제 ✓", INK, INK, WHITE)
text(s, L, 5.93, 6, 0.25, "✓ 는 막지 자사몰에서 결제하는 순간입니다", size=9.5, color=MUTE)

# ------------------------------------------------------------------ 8~10 유형별 상세 (목업 자리)
detail = [
    ("사용자 여정 ① 즉시 구매형", "즉시 구매형 — 이 가격이면 오늘 바로 삽니다", "이 가격 완벽해!", "오늘 가격으로 즉시 구매", "오늘가로 즉시 결제", GRN, GRN_T, GRN2,
     ["가격 확인", "즉시 구매", "오늘가로 결제"], "고민하는 순간 내일 가격이 오를 수 있어요 — ‘즉시 구매하기’"),
    ("사용자 여정 ② 가격 확보형", "가격 확보형 — 오전가를 잠그고 저녁에 결제합니다", "가격은 좋은데 결제는 이따가!", "오전가 잠금 후 이따가 구매", "잠근 가격으로 안심 결제", BREAD, BREAD_T, BREAD2,
     ["오전가 확인", "가격 잠금 (하루 1회)", "잠근 가격으로 결제"], "바쁘다면 일단 잠그세요 — ‘가격 잠그기’"),
    ("사용자 여정 ③ 관망·기대형", "관망·기대형 — 내일 가격을 예측하고 쿠폰으로 삽니다", "오후장에 더 싸지면 살래", "내일 가격 예측 참여", "쿠폰 적용해 최적가 결제", ACC, TINT, ACC2,
     ["가격 확인", "내일 가격 예측", "다음 날 결과 · 쿠폰 결제"], "더 싼 가격을 기다리시나요? — ‘가격 예측하고 5% 쿠폰 받기’"),
]
for k, (kick, head, q, act, fin, c, ct, cd, steps, cta) in enumerate(detail):
    s = frame(kick, head, cta, notes=NOTES[8 + k])
    panel(s, L, 1.7, W, 1.1, PANEL)
    rect(s, L + 0.15, 1.85, 3.9, 0.8, ct, c, r=0.14, lw=1.25)
    text(s, L + 0.4, 1.85, 3.5, 0.8, [[(head.split(" — ")[0], {"bold": True, "size": 14, "color": cd})], [("“" + q + "”", {"size": 11.5, "color": cd})]], anchor="m", lsp=1.2)
    arrow(s, L + 4.15, 1.7, 0.5, ACC, 20)
    text(s, L + 4.75, 1.7, 3.3, 1.1, act, size=14.5, bold=True, anchor="m")
    arrow(s, L + 8.05, 1.7, 0.5, ACC, 20)
    rect(s, L + 8.6, 1.87, 2.9, 0.76, INK, r=0.38)
    text(s, L + 8.6, 1.87, 2.9, 0.76, fin, size=11.5, bold=True, color=WHITE, align="c", anchor="m")
    for j, st in enumerate(steps):
        cx = 2.9 + j * 3.77
        dot(s, cx - 1.6, 3.05, 0.34, c)
        text(s, cx - 1.6, 3.05, 0.34, 0.34, str(j + 1), size=11, bold=True, color=WHITE, align="c", anchor="m")
        text(s, cx - 1.15, 3.03, 2.9, 0.38, st, size=12.5, bold=True, anchor="m")

# ------------------------------------------------------------------ 11 가격 결정
s = frame("가격 결정 방식", "이 모든 것이 통하려면, 가격은 공개된 산식으로만 움직입니다",
          "산식은 공개하고 상한은 38% — 그렇다면 실제 할인은 얼마나 될까요?",
          source="출처: 삼립 가격 인상 — 이투데이·뉴스핌 2026.08.09~10 보도(빵 50여 종 평균 9%, 편의점 판매가 2026.09.01부터)",
          notes=NOTES[11])
for (a, b, lab, sub, fl, tc) in [(6, 16, "오전장  06:00 ~ 15:59", "전일 종가 기준", ACC, WHITE), (16, 26, "오후장  16:00 ~ 익일 01:59", "당일 시가 기준", BREAD, WHITE), (26, 30, "정가  02:00~05:59", "", LINE, INK2)]:
    x = L + (a - 6) / 24 * W; w = (b - a) / 24 * W - 0.05
    rect(s, x, 1.85, w, 0.58, fl, r=0.12)
    text(s, x + 0.2, 1.85, w - 0.3, 0.58, [[(lab, {"bold": True, "size": 12.5 if a < 26 else 10}), ("   " + sub, {"size": 10.5, "color": rgb("EDF3F9") if a < 26 else INK2})]], color=tc, anchor="m")
panel(s, L, 2.65, W, 1.85, PANEL)
text(s, L, 2.75, W, 0.65, [[("총 할인율  =  ", {}), ("검색 할인", {"color": ACC2}), ("  +  ", {"color": MUTE}), ("환율 조정", {"color": BREAD2}), ("     (0% ~ 38%)", {"color": MUTE, "size": 16})]], size=26, bold=True, align="c", anchor="m")
text(s, L, 3.42, W, 0.32, "검색지수 × 0.15 (최대 15%)   ·   환율 하락은 ×14 전부 환원, 상승은 ×7 절반만 반영", size=12.5, color=INK2, align="c")
line(s, L + 0.5, 3.92, RIGHT - 0.5, 3.92, LINE, 0.75)
text(s, L + 0.5, 4.02, W - 1.0, 0.32, [[("원가는 실제로 빵값을 움직입니다  ", {"bold": True, "color": BREAD2}), ("삼립, 빵 50여 종 평균 9% 인상 (2026.09)", {"color": INK2})]], size=11.5, align="c")
card(s, L, 4.7, W, 1.5)
text(s, L + 0.35, 4.83, 5, 0.25, "예시 · 막지 제로 모닝롤", size=11.5, bold=True, color=ACC2)
for i, (lb, v, c) in enumerate([("정가", "4,500원", INK2), ("평균 할인 15%", "3,830원", ACC2), ("최대 할인 38%", "2,790원", BREAD2)]):
    x = L + 0.35 + i * 3.85
    text(s, x, 5.15, 3.3, 0.3, lb, size=12, color=INK2)
    text(s, x, 5.45, 3.3, 0.6, v, size=28, bold=True, color=c)
    if i < 2:
        arrow(s, x + 2.65, 5.42, 0.6, ACC, 22)

# ------------------------------------------------------------------ 12 할인율 분포
AM, PM = [1, 9, 37, 25, 14, 5], [1, 18, 40, 22, 8, 2]
BN = ["5% 미만", "5~10%", "10~15%", "15~20%", "20~25%", "25% 이상"]
s = frame("할인율 분포", "평균 할인은 15%, 세션의 84%가 20% 미만이었습니다",
          "대부분은 얕은 할인이고, 상한 38%가 깊은 할인을 막습니다.",
          source="실제 가격 엔진(v1.0)에 한국은행 ECOS 원/달러 시가·종가와 일별 검색지수를 넣은 재현값 (2026.06.12~09.10, 하루 2세션 × 91일) · 25% 이상 7세션 중 6세션은 상한 38% · 검색지수는 6종 합산 단일 시계열",
          notes=NOTES[12])
panel(s, L, 1.75, W, 4.45)
text(s, L + 0.3, 1.93, 1.2, 0.25, "■ 오전장", size=11, color=ACC); text(s, L + 1.3, 1.93, 1.2, 0.25, "■ 오후장", size=11, color=BREAD2)
text(s, 8.6, 1.85, 3.63, 0.5, [[("평균 ", {"size": 12, "color": MUTE}), ("15.0%", {"size": 26, "bold": True, "color": ACC2})]], anchor="m", align="r")
text(s, 8.0, 2.37, 4.23, 0.25, "오전장 15.8% · 오후장 14.2%", size=11, color=MUTE, align="r")
base = 5.4; mh = 2.1
for i in range(6):
    x = 1.55 + i * 1.8
    for j, (v, c) in enumerate([(AM[i], ACC), (PM[i], BREAD)]):
        h = v / 45 * mh
        rect(s, x + j * 0.62, base - h, 0.55, max(h, 0.03), c, r=0.04)
        text(s, x + j * 0.62 - 0.1, base - h - 0.3, 0.75, 0.26, str(v), size=12, bold=True, align="c")
    text(s, x - 0.2, base + 0.1, 1.95, 0.25, BN[i], size=12, bold=True, align="c")
    text(s, x - 0.2, base + 0.38, 1.95, 0.22, "%.1f%%" % ((AM[i] + PM[i]) / 182 * 100), size=11, color=MUTE, align="c")
line(s, L + 0.3, base, RIGHT - 0.3, base, LINE, 1.5)
xb0, xb1 = 1.45, 1.55 + 3 * 1.8 + 1.17
line(s, xb0, 3.3, xb1, 3.3, ACC, 1.5)
text(s, xb0, 2.96, xb1 - xb0, 0.3, "84%  (153 / 182 세션)", size=12.5, bold=True, color=ACC2, align="c")

# ------------------------------------------------------------------ 13 MVP
s = frame("MVP 범위", "첫 버전은 두 전략을 검증하는 기능만 담습니다",
          "구현 2~3주 · 검증 9/28~9/30 — 상품 수만 확정되면 바로 착수합니다.", notes=NOTES[13])
card(s, L, 1.85, 6.4, 4.35)
text(s, L + 0.35, 2.05, 6, 0.3, "포함 (Must)", size=12.5, bold=True, color=ACC2)
for i, (k, v) in enumerate([("전략 1", "오전장·오후장 가격 확인"), ("전략 2", "가격 잠금 (오전장 하루 1회)"), ("전략 2", "오늘의 보상 고르기 (안정형 / 공격형)"), ("전환", "자사몰 이동·구매 (원클릭 지향)"), ("신뢰", "‘투자가 아닙니다’ 안내 · 가격 근거"), ("안전", "38% 상한 가드레일")]):
    y = 2.5 + i * 0.6
    pill(s, L + 0.35, y + 0.05, 0.85, k, TINT if k == "전략 1" else (BREAD_T if k == "전략 2" else PANEL), ACC2 if k == "전략 1" else (BREAD2 if k == "전략 2" else INK2), size=10, h=0.3)
    text(s, L + 1.45, y, 4.8, 0.4, v, size=15, bold=True, anchor="m")
panel(s, 7.4, 1.85, 5.13, 4.35, PANEL)
text(s, 7.75, 2.05, 4, 0.3, "이번 범위 제외 · 여력 시", size=12.5, bold=True, color=INK2)
for i, v in enumerate(["여력 시 · 가격 하락 이메일 알림", "도감·씰 수집 콘텐츠", "매수가 기준 보상", "막지스톡 안에서의 결제", "막지스톡 자체 로그인·회원가입"]):
    text(s, 7.75, 2.5 + i * 0.6, 4.5, 0.4, ("+  " if i == 0 else "–  ") + v, size=14, color=ACC2 if i == 0 else INK2, bold=(i == 0), anchor="m")

# ------------------------------------------------------------------ 14 KPI
s = frame("KPI", "성공은 서비스 목표와 같은 순서로 측정합니다",
          "목표값은 근거 없이 만들지 않고, 베타 1주차 실측 후 확정합니다.",
          source="GUARDRAIL(하나라도 초과 시 롤아웃 중단): 총혜택 상한 위반 0 · 사행성 문구 0 · 표시·결제가 불일치 0 · 가격 계산 오류율 ≤ 0.1% · 쿠폰 중복 적용 0",
          notes=NOTES[14])
rect(s, L, 1.85, W, 1.3, ACC, r=0.18)
text(s, L + 0.4, 1.98, 3, 0.3, "북극성 KPI", size=11.5, bold=True, color=rgb("DCEAF7"))
text(s, L + 0.4, 2.3, 11, 0.6, [[("STOCK → 자사몰 전환율", {"bold": True}), ("      현재 미측정 · 베타 1주차에 기준선 확보", {"size": 13, "color": rgb("DCEAF7")})]], size=25, color=WHITE, anchor="m")
for i, (tg, c, tc, k, cur) in enumerate([("1순위 유입", TINT, ACC2, "방문자 수 · 신규 가입 · 자사몰 구매 이동률", "신규가입 5월 40건"),
                                         ("2순위 체류", BREAD_T, BREAD2, "익일 재방문율 · 체류시간 · 가격 잠금 사용률", "미측정"),
                                         ("2순위 전환", BREAD_T, BREAD2, "STOCK→자사몰 전환율 · 쿠폰 사용률 · 결제 완결률", "결제 완결률 73.5%")]):
    y = 3.4 + i * 0.95
    card(s, L, y, W, 0.8)
    pill(s, L + 0.25, y + 0.19, 1.45, tg, c, tc, size=11.5, h=0.42)
    text(s, L + 2.0, y, 6.9, 0.8, k, size=14.5, anchor="m")
    text(s, 9.5, y, 2.8, 0.8, cur, size=12.5, bold=True, color=INK2, align="r", anchor="m")

# ------------------------------------------------------------------ 15 매출
s = frame("매출 시나리오", "지표가 달성되면 Base 시나리오로 5년 뒤 18.8억입니다",
          "시장이 커진다는 가정 없이, 점유율만으로 그린 시나리오입니다.",
          source="시장 성장률 미반영, 점유율 확대만 반영한 시나리오(내부 시장분석) · 온라인 베이커리 시장 5,400억원은 aT 2024년 기준(매일경제 2026.03.23) · 망넛이네(2018 약 5.7억)·널담(2019 약 9.9억) 초기 실적은 벤치마크로만 참고",
          notes=NOTES[15])
panel(s, L, 1.75, W, 4.45)
text(s, L + 0.3, 1.93, 2, 0.25, "■ 1년차", size=11, color=rgb("6E9CC9")); text(s, L + 1.3, 1.93, 2, 0.25, "■ 5년차", size=11, color=ACC)
text(s, 5.4, 1.9, 6.83, 0.3, [[("매출 = 유입 × 구매 전환율 × 객단가 ", {"color": INK2}), ("(5월 2.32만원)", {"color": MUTE, "size": 10.5})]], size=12.5, bold=True, align="r")
for i, (nm, a, b) in enumerate([("Worst", 1.2, 2.8), ("Base", 5.7, 18.8), ("Best", 9.9, 35.3)]):
    x = 1.95 + i * 3.6
    for j, (v, c) in enumerate([(a, LB), (b, ACC)]):
        h = v / 36 * 2.5
        rect(s, x + j * 1.3, 5.45 - h, 1.1, max(h, 0.05), c, r=0.05)
        text(s, x + j * 1.3 - 0.2, 5.45 - h - 0.4, 1.5, 0.35, str(v) + "억", size=15, bold=True, align="c", color=ACC2 if (j and i == 1) else INK)
    text(s, x - 0.2, 5.58, 2.9, 0.28, nm, size=12.5, bold=True, align="c")
    line(s, x - 0.3, 5.45, x + 2.7, 5.45, LINE, 1.25)
pill(s, 8.6, 2.45, 3.6, "Base 5년차 ≈ 온라인 시장(5,400억)의 0.35%", BREAD_T, BREAD2, size=10.5, h=0.34)

# ------------------------------------------------------------------ 16 리스크
s = frame("핵심 리스크", "구조적 제약 1개와 관리 가능한 리스크 5개가 있습니다",
          "HIGH 3건은 출시 전에 해소합니다.",
          source="대응 원칙: 총혜택 상한 38% 고정 · 표시가 = 결제가 일치 검증 · 할인 표시 법무 검토 · 3구간 모델 기준 백테스트 재실행",
          notes=NOTES[16])
risks = [("01", "STOCK ↔ 자사몰 분리", "RFP 요구 구조 — 원클릭으로 최소화만 가능", "구조적", INK, WHITE),
         ("02", "검색 키워드 적합성", "백테스트는 모닝빵 1종 중심 — 나머지 검증 필요", "HIGH", BREAD, WHITE),
         ("03", "표시·결제가 불일치", "다르면 신뢰·전환이 훼손됨", "HIGH", BREAD, WHITE),
         ("04", "법적 위험", "할인 표시가 실제와 다르면 표시광고법 소지", "HIGH", BREAD, WHITE),
         ("05", "가격모델 전환 재검증", "3구간 모델로 바뀌어 백테스트 재실행", "관리중", BREAD_T, BREAD2),
         ("06", "쿠폰 중복 적용", "동시 적용 시 총혜택 상한 초과 가능", "관리중", BREAD_T, BREAD2)]
for i, (n, tt, dd, lv, lf, lc) in enumerate(risks):
    x = L + (i // 3) * 5.98; y = 1.85 + (i % 3) * 1.45
    card(s, x, y, 5.75, 1.25)
    text(s, x + 0.25, y, 0.55, 1.25, n, size=14, bold=True, color=MUTE, anchor="m")
    text(s, x + 0.85, y + 0.22, 3.6, 0.4, tt, size=15.5, bold=True, anchor="m")
    text(s, x + 0.85, y + 0.68, 4.6, 0.3, dd, size=11, color=INK2)
    pill(s, x + 4.65, y + 0.24, 0.9, lv, lf, lc, size=10.5, h=0.32)

# ------------------------------------------------------------------ 17 로드맵·요청
s = frame("요청 사항과 로드맵", "세 가지가 정해지면 바로 3단계로 시작합니다",
          "세 가지가 정해지면 바로 구현·검증 단계로 들어갑니다.",
          source="향후 확장(설계 단계, 이번 구현 범위 아님): Bakery ETF · FX Bakery · Bread Index · 연속 방문 스트릭 보상",
          notes=NOTES[17])
panel(s, L, 1.85, W, 1.85, PANEL)
line(s, L + 0.5, 2.3, RIGHT - 0.5, 2.3, LINE, 2.5)
for i, (ph, c, tt, dd) in enumerate([("PHASE 1", ACC, "MVP", "시세 · 비교 · 구매 이동"), ("PHASE 2", BREAD, "참여", "가격 잠금 · 보상 고르기 · 알림"), ("PHASE 3", ACC, "연동", "자사몰 실연동 · 쿠폰 · 구매 데이터")]):
    x = L + 0.5 + i * 3.85
    dot(s, x, 2.16, 0.28, c)
    text(s, x, 2.6, 3.6, 0.35, [[(ph + "  ", {"size": 10.5, "color": MUTE, "bold": True}), (tt, {"size": 16, "bold": True})]])
    text(s, x, 3.04, 3.6, 0.3, dd, size=11.5, color=INK2)
for i, (n, c, fl, tt, dd) in enumerate([("01", ACC2, TINT, "MVP 상품 수 확정", "대표 6종 기준으로 준비 중 · 최종 승인 필요"),
                                        ("02", BREAD2, BREAD_T, "실제 원가·마진율 공유", "실제 수치로 마진 방어를 정밀 검증합니다"),
                                        ("03", ACC2, TINT, "할인 표시 법무 검토", "기준가격·할인율·적용기간 표시가 표시광고법에 맞는지")]):
    y = 3.95 + i * 0.75
    panel(s, L, y, W, 0.63, fl)
    text(s, L + 0.35, y, 0.7, 0.63, n, size=19, bold=True, color=c, anchor="m")
    text(s, L + 1.2, y, 3.8, 0.63, tt, size=15.5, bold=True, anchor="m")
    text(s, 5.9, y, 6.4, 0.63, dd, size=12, color=INK2, anchor="m")

# ------------------------------------------------------------------ 18 Q&A
s = prs.slides.add_slide(BLANK)
rect(s, 0, 0, 0.22, 7.5, ACC, r=0)
rect(s, 9.6, 4.2, 5.2, 5.2, BREAD_T, r=0, shape=MSO_SHAPE.OVAL)
dot(s, L, 0.62, 0.11, BREAD)
text(s, L + 0.22, 0.52, 4, 0.3, "MAKJI", size=13, bold=True, color=INK)
text(s, 7.5, 0.52, 5.03, 0.3, "Q&A", size=10.5, bold=True, color=MUTE, align="r")
text(s, L, 2.7, 11.5, 2.2, [["가격이 움직인다는 사실 자체가,"], [("다시 찾는 이유", {"color": ACC}), ("가 됩니다.", {})]], size=44, bold=True, lsp=1.15)
text(s, L, 5.2, 8, 0.4, "질문과 의견을 듣겠습니다.", size=16, color=INK2)
text(s, L, 6.75, 6, 0.3, "빵값연구소  |  MAKJI STOCK", size=11, color=INK2)
s.notes_slide.notes_text_frame.text = "[클로징 멘트] 가격이 움직이니 손님도 움직입니다. 질문 주시면 저도 움직이겠습니다.\n[Q&A] 예상 질문은 발표 스토리라인 문서의 ‘예상 질문과 답변’을 참고하세요."

OUT.parent.mkdir(parents=True, exist_ok=True)
prs.save(str(OUT))
print("saved", OUT, "slides", len(prs.slides))
