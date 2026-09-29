import pandas as pd
import numpy as np

file_path = r"C:\Users\Administrator\Downloads\6년 환율.xls"
tables = pd.read_html(file_path, encoding='euc-kr')
df = tables[1]

# Row 0 is the header, but due to encoding we just use indices
df.columns = range(df.shape[1])
df = df.iloc[1:].copy()

df['rate'] = pd.to_numeric(df[2], errors='coerce')
df = df.dropna(subset=['rate'])
df = df.sort_values(by=0, ascending=True).reset_index(drop=True)

df['prev_rate'] = df['rate'].shift(1)
df['drop_pct'] = ((df['prev_rate'] - df['rate']) / df['prev_rate']) * 100
df = df.dropna(subset=['drop_pct'])

drops = df['drop_pct']

print("--- 일일 환율 하락률(Drop Pct) 통계 ---")
print(f"Total trading days: {len(drops)}")
print(f"Mean drop (when dropping): {drops[drops > 0].mean():.2f}%")
print(f"Max drop: {drops.max():.2f}%")
print("\n--- 상위 백분위수 (Percentiles) ---")
for p in [50, 70, 80, 90, 95, 98, 99]:
    val = np.percentile(drops, p)
    print(f"Top {100-p}% (P{p}): {val:.2f}% 이상 하락")

p99 = np.percentile(drops, 99)
print(f"\n만약 P99 ({p99:.2f}% 하락) 일 때 최대치 17% 할인을 주도록 배수를 설정한다면:")
multiplier = 17 / p99
print(f"적용 스케일 배수(Multiplier): {multiplier:.2f}배")
