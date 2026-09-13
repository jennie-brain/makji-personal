#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MAKJI STOCK 91-Day Parameter Grid Search and Optimal Ratio / Scale Inference
"""

import json
import statistics as st
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "docs" / "02_pricing_engine" / "data" / "dataset_91d.json"

with open(DATA_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

ratios = [
    (0.30, 0.08, "30:8 (환율극대형)"),
    (0.28, 0.10, "28:10 (원안)"),
    (0.25, 0.13, "25:13 (중간안A)"),
    (0.22, 0.16, "22:16 (중간안B)"),
    (0.20, 0.18, "20:18 (ADR-002)"),
    (0.18, 0.20, "18:20 (검색우위)"),
]

scales = [10, 15, 20, 25, 30, 35, 40, 50, 60, 75, 100, 150, 200]

results = []

for w_fx, w_s, label in ratios:
    cap_fx = w_fx * 100.0
    for sc in scales:
        totals, fxs, coupons = [], [], []
        for d in data:
            fx = min(cap_fx, max(0.0, d["drop"] * w_fx * sc))
            cp = d["idx"] * w_s
            tot = min(38.0, fx + cp)
            totals.append(tot)
            fxs.append(fx)
            coupons.append(cp)

        deltas = [abs(totals[i] - totals[i - 1]) for i in range(1, len(totals))]
        mean_delta = st.mean(deltas)

        vf = st.pvariance(fxs)
        vc = st.pvariance(coupons)
        fx_share = vf / (vf + vc) * 100 if (vf + vc) > 0 else 0

        cap_hits = sum(1 for t in totals if t >= 38.0 - 1e-6)
        fx_cap_hits = sum(1 for f in fxs if f >= cap_fx - 1e-6)

        sorted_tot = sorted(totals)
        p95 = sorted_tot[int(0.95 * len(totals))]

        results.append({
            "ratio": label,
            "w_fx": w_fx,
            "w_s": w_s,
            "scale": sc,
            "slope": round(w_fx * sc, 2),
            "trigger": round(100.0 / sc, 2) if sc > 0 else 999,
            "median": round(st.median(totals), 2),
            "mean": round(st.mean(totals), 2),
            "max": round(max(totals), 2),
            "min": round(min(totals), 2),
            "std": round(st.pstdev(totals), 2),
            "p95": round(p95, 2),
            "daily_delta": round(mean_delta, 2),
            "fx_share": round(fx_share, 1),
            "cp_share": round(100 - fx_share, 1),
            "cap_hits": cap_hits,
            "fx_cap_hits": fx_cap_hits,
            "under_10": sum(1 for t in totals if t < 10.0),
            "under_12": sum(1 for t in totals if t < 12.0),
            "over_25": sum(1 for t in totals if t >= 25.0),
        })

print(f"Total scenarios computed: {len(results)}")

print("\n" + "=" * 90)
print("📌 [분석 1] 기존 원안(28:10)에서의 SCALE 민감도 분석")
print("=" * 90)
header = f"{'Scale':>5} | {'기울기':>6} | {'임계치':>6} | {'중앙값':>6} | {'평균':>6} | {'최대':>6} | {'P95':>6} | {'일변동':>6} | {'38%캡':>5} | {'FX캡':>5} | {'환율기여':>6} | {'<10%일수':>7}"
print(header)
print("-" * 90)
for r in [x for x in results if x["w_fx"] == 0.28 and x["scale"] in [15, 20, 25, 30, 35, 40, 50, 60, 75, 100]]:
    print(f"{r['scale']:5d} | {r['slope']:6.1f} | {r['trigger']:5.2f}% | {r['median']:5.1f}% | {r['mean']:5.1f}% | {r['max']:5.1f}% | {r['p95']:5.1f}% | {r['daily_delta']:5.2f}%p | {r['cap_hits']:4d}회 | {r['fx_cap_hits']:4d}회 | {r['fx_share']:5.1f}% | {r['under_10']:6d}일")

print("\n" + "=" * 90)
print("📌 [분석 2] 확정안(20:18)에서의 SCALE 민감도 분석")
print("=" * 90)
print(header)
print("-" * 90)
for r in [x for x in results if x["w_fx"] == 0.20 and x["scale"] in [15, 20, 25, 30, 35, 40, 50, 60, 75, 100]]:
    print(f"{r['scale']:5d} | {r['slope']:6.1f} | {r['trigger']:5.2f}% | {r['median']:5.1f}% | {r['mean']:5.1f}% | {r['max']:5.1f}% | {r['p95']:5.1f}% | {r['daily_delta']:5.2f}%p | {r['cap_hits']:4d}회 | {r['fx_cap_hits']:4d}회 | {r['fx_share']:5.1f}% | {r['under_10']:6d}일")

print("\n" + "=" * 90)
print("📌 [분석 3] 동일 스케일 조건에서 비율(Ratio) 간의 직접 비교")
print("=" * 90)
r_header = f"{'비율 시나리오':<18} | {'Scale':>5} | {'실효기울기':>6} | {'중앙값':>6} | {'평균':>6} | {'최소':>6} | {'최대':>6} | {'일변동':>6} | {'환율기여':>6} | {'<10%일수':>7}"
print(r_header)
print("-" * 90)
for sc in [35, 50]:
    print(f"--- [ Scale = {sc} ] ---")
    for r in [x for x in results if x["scale"] == sc]:
        print(f"{r['ratio']:<18} | {r['scale']:5d} | {r['slope']:6.1f} | {r['median']:5.1f}% | {r['mean']:5.1f}% | {r['min']:5.1f}% | {r['max']:5.1f}% | {r['daily_delta']:5.2f}%p | {r['fx_share']:5.1f}% | {r['under_10']:6d}일")
