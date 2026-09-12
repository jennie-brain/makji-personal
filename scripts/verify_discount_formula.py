# -*- coding: utf-8 -*-
"""막지 스톡 할인율 산식 검증 - 입력: 데이터랩.xlsx + 환율데이터.xls 만 사용"""
import re, html, json, openpyxl, statistics as st, datetime as dt, collections, os

D = os.path.expanduser('~/Downloads')
OUT = os.path.dirname(os.path.abspath(__file__))

# ---------- 입력 1: 환율 (매매기준율) ----------
raw = open(os.path.join(D, '환율데이터.xls'), encoding='euc-kr', errors='replace').read()
FX = {}
for r in re.findall(r'<tr.*?</tr>', raw, re.S | re.I):
    c = [html.unescape(re.sub(r'<.*?>', '', x)).strip()
         for x in re.findall(r'<t[dh].*?</t[dh]>', r, re.S | re.I)]
    if len(c) >= 7 and re.match(r'^\d{4}\.\d{2}\.\d{2}$', c[0]):
        FX[c[0].replace('.', '-')] = float(re.match(r'^([\d,\.]+)', c[5]).group(1).replace(',', ''))

# ---------- 입력 2: 검색량 (네이버 데이터랩) ----------
ws = openpyxl.load_workbook(os.path.join(D, '데이터랩.xlsx'), data_only=True).active
rows = list(ws.iter_rows(values_only=True))
META = {r[0]: r[1] for r in rows[:7] if r[0]}
KW = rows[6][1]
S = {r[0]: float(r[1]) for r in rows[7:] if r[0] and r[1] not in (None, '')}

# ---------- 산식 파라미터 ----------
W_FX, SCALE, W_S = 0.28, 50, 0.1
CAP_FX, CAP_TOTAL = 28.0, 38.0
BASE_PRICE = 4500

fk, sk = sorted(FX), sorted(S)
drop = {b: (FX[a] - FX[b]) / FX[a] * 100 for a, b in zip(fk, fk[1:])}

# ---------- 일별 시뮬레이션 (09:00 개장, D-1 기준, 휴장일 이월) ----------
WD = '월화수목금토일'
day, end, last, daily = dt.date.fromisoformat(fk[1]), dt.date.fromisoformat(sk[-1]), None, []
while day <= end:
    p = (day - dt.timedelta(days=1)).isoformat()
    fresh = p in drop
    if fresh:
        last = drop[p]
    if last is not None and p in S:
        fx_disc = min(CAP_FX, max(0, last * W_FX * SCALE))
        coupon = S[p] * W_S
        total = min(CAP_TOTAL, fx_disc + coupon)
        daily.append({
            'date': day.isoformat(), 'wd': WD[day.weekday()], 'src': p,
            'fx_rate': FX.get(p), 'drop': round(last, 4),
            'fx_disc': round(fx_disc, 2), 'idx': S[p], 'coupon': round(coupon, 2),
            'total': round(total, 2), 'fresh': fresh,
            'price_incl': round(BASE_PRICE * (1 - total / 100)),
            'price_sep': round(BASE_PRICE * (1 - fx_disc / 100)),
        })
    day += dt.timedelta(days=1)

fx_d = [d['fx_disc'] for d in daily]
cp_d = [d['coupon'] for d in daily]
tot_d = [d['total'] for d in daily]
dv = list(drop.values())


def pct(n, d):
    return round(100 * n / d, 1)


# ---------- 요일별 ----------
byw = collections.defaultdict(list)
for d in daily:
    byw[d['wd']].append(d)
weekday = [{'wd': w, 'n': len(byw[w]),
            'idx': round(st.mean([x['idx'] for x in byw[w]]), 1),
            'coupon': round(st.mean([x['coupon'] for x in byw[w]]), 2),
            'fx': round(st.mean([x['fx_disc'] for x in byw[w]]), 2),
            'total': round(st.mean([x['total'] for x in byw[w]]), 2),
            'fresh': sum(1 for x in byw[w] if x['fresh'])} for w in WD]

# ---------- 토/일/월 동결 ----------
frozen = []
for i in range(len(daily) - 2):
    w3 = daily[i:i + 3]
    if [x['wd'] for x in w3] == ['토', '일', '월'] and len({round(x['fx_disc'], 4) for x in w3}) == 1:
        t = [x['total'] for x in w3]
        frozen.append({'date': w3[0]['date'], 'fx': w3[0]['fx_disc'],
                       'coupons': [x['coupon'] for x in w3], 'totals': t,
                       'spread': round(max(t) - min(t), 2)})
fresh_delta = [abs(daily[i]['total'] - daily[i - 1]['total'])
               for i in range(1, len(daily)) if daily[i]['fresh']]


# ---------- 시나리오: 쿠폰 포함 vs 분리 ----------
def scen(vals):
    dd = [abs(vals[i] - vals[i - 1]) for i in range(1, len(vals))]
    return {'median': round(st.median(vals), 1), 'mean': round(st.mean(vals), 1),
            'max': round(max(vals), 1), 'min': round(min(vals), 1),
            'zero_days': sum(1 for v in vals if v == 0),
            'zero_pct': pct(sum(1 for v in vals if v == 0), len(vals)),
            'daily_move': round(st.mean(dd), 2),
            'still_days': sum(1 for v in dd if v < 0.5),
            'still_pct': pct(sum(1 for v in dd if v < 0.5), len(dd))}


scenarios = {'include': scen(tot_d), 'separate': scen(fx_d)}

# ---------- 분포 ----------
bins = [(0, 0.01, '0%'), (0.01, 5, '0~5'), (5, 10, '5~10'), (10, 15, '10~15'),
        (15, 20, '15~20'), (20, 25, '20~25'), (25, 30, '25~30'), (30, 38.1, '30~38')]


def hist(vals):
    return [{'label': lb, 'n': sum(1 for v in vals if lo <= v < hi),
             'pct': pct(sum(1 for v in vals if lo <= v < hi), len(vals))} for lo, hi, lb in bins]


# ---------- 통계의 통계 (산식 근거) ----------
mf, mc = st.mean(fx_d), st.mean(cp_d)
vf, vc, vt = st.pvariance(fx_d), st.pvariance(cp_d), st.pvariance(tot_d)
cov = st.mean([(fx_d[i] - mf) * (cp_d[i] - mc) for i in range(len(daily))])
corr = cov / ((vf ** .5) * (vc ** .5))

evidence = {
    'budget': {'fx_alloc': CAP_FX, 'fx_used_mean': round(mf, 2), 'fx_used_pct': pct(mf, CAP_FX),
               'fx_used_max': round(max(fx_d), 2), 'fx_max_pct': pct(max(fx_d), CAP_FX),
               'cp_alloc': 10.0, 'cp_used_mean': round(mc, 2), 'cp_used_pct': pct(mc, 10),
               'cp_used_max': round(max(cp_d), 2), 'cp_max_pct': pct(max(cp_d), 10)},
    'variance': {'fx': round(vf, 2), 'coupon': round(vc, 2), 'total': round(vt, 2),
                 'fx_share': pct(vf, vf + vc), 'cp_share': pct(vc, vf + vc),
                 'corr': round(corr, 3)},
    'caps': {'fx_cap_hits': sum(1 for v in fx_d if v >= CAP_FX),
             'total_cap_hits': sum(1 for v in tot_d if v >= CAP_TOTAL),
             'trigger_drop': round(CAP_FX / (W_FX * SCALE), 2),
             'max_drop_obs': round(max(dv), 3), 'n_fx_days': len(dv),
             'days_over_1': sum(1 for v in dv if v >= 1.0),
             'days_over_15': sum(1 for v in dv if v >= 1.5),
             'days_over_2': sum(1 for v in dv if v >= 2.0),
             'headroom': round(CAP_FX - max(fx_d), 2)},
    'slope': {'effective': W_FX * SCALE, 'per_0_5': round(0.5 * W_FX * SCALE, 1),
              'per_1_0': round(1.0 * W_FX * SCALE, 1),
              'mean_drop': round(st.mean(dv), 3),
              'mean_drop_disc': round(st.mean(dv) * W_FX * SCALE, 1)},
    'movement': {'daily_move': round(st.mean([abs(tot_d[i] - tot_d[i - 1])
                                              for i in range(1, len(tot_d))]), 2),
                 'fresh_move': round(st.mean(fresh_delta), 2),
                 'frozen_spread': round(st.mean([f['spread'] for f in frozen]), 2),
                 'ratio': round(st.mean(fresh_delta) / st.mean([f['spread'] for f in frozen]), 1)},
    'margin': {'max_total': round(max(tot_d), 2),
               'p95': round(sorted(tot_d)[int(.95 * len(tot_d))], 2),
               'over_30': sum(1 for v in tot_d if v >= 30),
               'over_25': sum(1 for v in tot_d if v >= 25)},
}

result = {
    'meta': {'keyword': KW, 'period': META.get('기간'), 'fx_days': len(fk), 'search_days': len(S),
             'sim_days': len(daily), 'fx_src': '매매기준율', 'base_price': BASE_PRICE,
             'params': {'w_fx': W_FX, 'scale': SCALE, 'w_s': W_S,
                        'cap_fx': CAP_FX, 'cap_total': CAP_TOTAL}},
    'fx_stats': {'mean_drop': round(st.mean(dv), 3), 'max_drop': round(max(dv), 3),
                 'max_rise': round(min(dv), 3), 'n': len(dv),
                 'fx_min': min(FX.values()), 'fx_max': max(FX.values()),
                 'fx_first': FX[fk[0]], 'fx_last': FX[fk[-1]]},
    'search_stats': {'min': min(S.values()), 'max': max(S.values()),
                     'mean': round(st.mean(list(S.values())), 1),
                     'median': round(st.median(list(S.values())), 1)},
    'totals': {'median': round(st.median(tot_d), 1), 'mean': round(st.mean(tot_d), 1),
               'max': round(max(tot_d), 1), 'min': round(min(tot_d), 1),
               'sd': round(st.pstdev(tot_d), 1),
               'fx_zero_days': sum(1 for v in fx_d if v == 0),
               'fx_zero_pct': pct(sum(1 for v in fx_d if v == 0), len(fx_d))},
    'hist_total': hist(tot_d), 'hist_fx': hist(fx_d),
    'weekday': weekday, 'frozen': frozen, 'scenarios': scenarios, 'evidence': evidence,
    'daily': daily,
}
json.dump(result, open(os.path.join(OUT, 'result.json'), 'w', encoding='utf-8'),
          ensure_ascii=False, indent=1)

t = result['totals']
e = evidence
print('키워드 {} / {} / 시뮬 {}일'.format(KW, META.get('기간'), len(daily)))
print('총할인 중앙값 {} 평균 {} 최대 {} 최소 {} SD {}'.format(
    t['median'], t['mean'], t['max'], t['min'], t['sd']))
print('예산소진 환율 {}% (평균 {}pp/28) 검색 {}% (평균 {}pp/10)'.format(
    e['budget']['fx_used_pct'], e['budget']['fx_used_mean'],
    e['budget']['cp_used_pct'], e['budget']['cp_used_mean']))
print('변동성기여 환율 {}% 검색 {}% 상관 {}'.format(
    e['variance']['fx_share'], e['variance']['cp_share'], e['variance']['corr']))
print('캡 28pp {}회 / 38 {}회 / 헤드룸 {}pp / 임계 {}%'.format(
    e['caps']['fx_cap_hits'], e['caps']['total_cap_hits'],
    e['caps']['headroom'], e['caps']['trigger_drop']))
print('움직임 전체 {} 갱신일 {} 동결 {} 배수 {}'.format(
    e['movement']['daily_move'], e['movement']['fresh_move'],
    e['movement']['frozen_spread'], e['movement']['ratio']))
print('포함:', scenarios['include'])
print('분리:', scenarios['separate'])
print('동결주말 {}회 / 마진 p95 {} / 30%이상 {}일'.format(
    len(frozen), e['margin']['p95'], e['margin']['over_30']))
