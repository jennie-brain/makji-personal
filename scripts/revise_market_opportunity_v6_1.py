"""Create a non-destructive v6.1 deck with a rebuilt market-opportunity slide."""
from copy import deepcopy
from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_CONNECTOR, MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "docs" / "04_presentations" / "막지스톡_기업대표_서비스기획_발표v5.0.pptx"
OUTPUT = ROOT / "docs" / "04_presentations" / "막지스톡_기업대표_서비스기획_발표v6.1_시장기회개선.pptx"

FONT = "Noto Sans KR"
INK = RGBColor(17, 24, 39)
INK2 = RGBColor(75, 85, 99)
MUTE = RGBColor(156, 163, 175)
LINE = RGBColor(229, 231, 235)
SOFT = RGBColor(245, 247, 250)
WHITE = RGBColor(255, 255, 255)
ACC = RGBColor(64, 135, 199)
ACC2 = RGBColor(47, 111, 173)
TINT = RGBColor(234, 242, 250)
ORG = RGBColor(255, 122, 69)


def clear(slide):
    for shape in list(slide.shapes):
        shape._element.getparent().remove(shape._element)


def box(slide, x, y, w, h, fill=None, line=None, rounded=False):
    shape = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE if rounded else MSO_SHAPE.RECTANGLE,
        Inches(x), Inches(y), Inches(w), Inches(h),
    )
    if rounded:
        shape.adjustments[0] = 0.08
    if fill is None:
        shape.fill.background()
    else:
        shape.fill.solid(); shape.fill.fore_color.rgb = fill
    if line is None:
        shape.line.fill.background()
    else:
        shape.line.color.rgb = line; shape.line.width = Pt(0.75)
    return shape


def tx(slide, x, y, w, h, value, size=12, bold=False, color=INK, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP):
    shape = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = shape.text_frame
    tf.clear(); tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = anchor
    for idx, line in enumerate(value.split("\n")):
        paragraph = tf.paragraphs[0] if idx == 0 else tf.add_paragraph()
        paragraph.text = line
        paragraph.alignment = align
        paragraph.space_after = Pt(0)
        paragraph.font.name = FONT; paragraph.font.size = Pt(size); paragraph.font.bold = bold
        paragraph.font.color.rgb = color
    return shape


def line(slide, x1, y1, x2, y2, color=LINE, width=1):
    shape = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(x1), Inches(y1), Inches(x2), Inches(y2))
    shape.line.color.rgb = color; shape.line.width = Pt(width)
    return shape


def circle(slide, x, y, d, fill):
    return box(slide, x, y, d, d, fill, None, rounded=True)


def right_arrow(slide, x, y, w, h, fill):
    shape = slide.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(x), Inches(y), Inches(w), Inches(h))
    shape.fill.solid(); shape.fill.fore_color.rgb = fill
    shape.line.fill.background()
    return shape


prs = Presentation(SOURCE)
slide = prs.slides[1]
clear(slide)

# Frame: headline → single opportunity structure → concise conclusion.
tx(slide, 0.9, 0.62, 8.0, 0.3, "시장 기회", 11.5, True, ACC2)
tx(slide, 0.9, 0.95, 11.5, 0.85, "포화된 오프라인을 넘어,\n온라인 냉동 베이커리 시장은 1조 원대로 커지고 있습니다.", 25, True)

# Left: mature market context.
box(slide, 0.9, 2.22, 3.25, 3.93, SOFT, LINE, True)
tx(slide, 1.2, 2.52, 2.4, 0.25, "OFFLINE · MATURE", 10.5, True, MUTE)
tx(slide, 1.2, 2.98, 2.5, 0.5, "13.6조 원", 29, True, INK2)
tx(slide, 1.2, 3.57, 2.4, 0.28, "국내 베이커리 시장", 13.5, True, INK2)
line(slide, 1.24, 4.27, 3.75, 4.27, MUTE, 2.2)
for x in (1.6, 2.45, 3.3):
    circle(slide, x, 4.14, 0.26, MUTE)
tx(slide, 1.2, 4.65, 2.65, 0.28, "점포 수는 2022년 정점 이후 정체", 10.8, False, INK2)
tx(slide, 1.2, 5.18, 2.65, 0.48, "시장 규모는 크지만,\n오프라인 확장은 둔화", 10.5, False, MUTE)

# Connector is directional, not a third metric.
right_arrow(slide, 4.42, 4.0, 0.72, 0.43, ORG)
tx(slide, 4.05, 3.63, 1.45, 0.23, "기회 이동", 10.2, True, ORG, PP_ALIGN.CENTER)

# Right: defensible growth opportunity and evidence.
box(slide, 5.72, 2.22, 6.71, 3.93, TINT, RGBColor(191, 214, 236), True)
tx(slide, 6.02, 2.52, 5.8, 0.25, "ONLINE · FROZEN BAKERY", 10.5, True, ACC2)
tx(slide, 6.02, 2.95, 5.9, 0.35, "막지와 맞닿은 냉동생지 시장의 확장", 19, True)
tx(slide, 6.12, 3.67, 1.75, 0.4, "413억 원", 24, True, INK2, PP_ALIGN.CENTER)
tx(slide, 6.12, 4.12, 1.75, 0.22, "2020 시장 규모", 10.2, False, MUTE, PP_ALIGN.CENTER)
right_arrow(slide, 8.05, 3.84, 0.94, 0.35, ACC)
tx(slide, 9.25, 3.67, 2.35, 0.4, "1조 3,000억 원", 23, True, ACC2, PP_ALIGN.CENTER)
tx(slide, 9.25, 4.12, 2.35, 0.22, "2030 시장 전망", 10.2, False, MUTE, PP_ALIGN.CENTER)
tx(slide, 6.12, 4.56, 5.6, 0.22, "업계 추정 전망치 · 확정 실적과 구분", 10, False, MUTE, PP_ALIGN.CENTER)
line(slide, 6.1, 5.05, 12.02, 5.05, RGBColor(191, 214, 236), 1)
tx(slide, 6.1, 5.27, 5.93, 0.28, "온라인 출발 브랜드 널담 법인 매출", 11.5, True, ACC2, PP_ALIGN.CENTER)
tx(slide, 6.1, 5.56, 5.93, 0.33, "145.6억 원(2023)  →  330억 원(2025)", 14.5, True, INK2, PP_ALIGN.CENTER)

# Closing line and source.
box(slide, 12.01, 6.43, 0.42, 0.045, ACC, None)
tx(slide, 3.05, 6.55, 9.38, 0.34, "막지가 들어갈 곳은 정체된 점포 시장이 아니라, 빠르게 확장하는 온라인 냉동 베이커리입니다.", 13.5, True, ACC2, PP_ALIGN.RIGHT)
tx(slide, 0.9, 7.02, 10.8, 0.25, "출처: 삼일PwC 경영연구원 · 닐슨코리아 인용 냉동생지 시장 전망(2020→2030, 업계 추정) · 조인앤조인(널담) 법인 매출", 7.8, False, MUTE)
tx(slide, 11.0, 7.05, 1.43, 0.2, "02 / 16", 9, False, MUTE, PP_ALIGN.RIGHT)

slide.notes_slide.notes_text_frame.text = (
    "[핵심] 국내 베이커리 전체 시장은 포화됐지만, 온라인 냉동 베이커리 시장은 1조 원대로 커지고 있습니다.\n"
    "[근거] 국내 베이커리 시장은 13.6조 원으로 크지만 점포 수는 2022년 정점 이후 정체입니다. 반면 냉동생지 시장은 2020년 413억 원에서 2030년 1조 3,000억 원으로 확대될 전망입니다. 이는 업계 추정 전망치입니다. 온라인에서 출발한 널담의 법인 매출도 2023년 145.6억 원에서 2025년 330억 원으로 성장했습니다.\n"
    "[연결] 막지가 들어갈 곳은 정체된 점포 시장이 아니라 온라인 냉동 베이커리 시장입니다. 이제 자사몰에서 풀어야 할 문제를 보겠습니다."
)

prs.save(OUTPUT)
print(OUTPUT)
