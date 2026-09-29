import sys
import re

with open(r'C:\Users\Administrator\workspace\makji\docs\04_presentations\막지스톡-발표스토리라인.md', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('막지스톡_기업대표_서비스기획_발표v5.0.pptx', '막지스톡_기업대표_서비스기획_발표v6.0.pptx')
content = content.replace('온라인 시장은 커지는데, 자사몰은 아침에 둘러보고 저녁에 사서 방문과 구매의 시점이 어긋난다', "기존 빵 시장은 '얼마나 싸게/빨리'의 출혈 경쟁 중이며, 자사몰은 아침 방문과 저녁 결제가 엇갈린다")
content = content.replace('매일 두 번 움직이는 가격(막지스톡)이 유입 → 체류 → 전환을 한 걸음에 잇는다', "'빵을 주식처럼' — 마감 할인 대신 '타이밍 런'의 재미로 유입 → 체류 → 전환을 능동적으로 잇는다")

old_text = "전략은 두 가지입니다. 하나, 가격 자체를 콘텐츠로 만들어 매일 오게 한다. 둘, 고객이 직접 고르는 혜택으로 참여와 주도성을 준다. 이 둘을 묶은 것이 막지스톡입니다. 빵값을 주식시장처럼 하루 두 번 열고, 그 안에서 고객이 자기 방식대로 혜택을 고릅니다. 경쟁 6곳 중 가격 변동 자체를 콘텐츠로 쓰는 곳은 아직 없습니다."
new_text = "전략은 두 가지입니다. 하나, 가격 자체를 콘텐츠로 만들어 아침에 매일 오게 한다(쇼핑의 오락화). 둘, 맹목적인 '마감 할인' 대신 고객이 직접 고르는 혜택으로 득템의 주도성을 준다. 이 둘을 묶은 것이 막지스톡입니다. 빵값을 주식시장처럼 하루 두 번 열고, 그 안에서 고객이 자기 방식대로 예측하고 혜택을 쟁취합니다. 파리바게뜨나 새벽배송 등 기존 빵 시장이 편리함에 머물 때, 우리는 '득템의 재미'라는 독보적 가치를 팝니다."
content = content.replace(old_text, new_text)

with open(r'C:\Users\Administrator\workspace\makji\docs\04_presentations\막지스톡-발표스토리라인_v6.0.md', 'w', encoding='utf-8') as f:
    f.write(content)
