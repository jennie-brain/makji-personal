import { addDays, dateRange } from "../lib/pricing/dates.mjs";
import { fetchUsdKrwOpenCloseRates } from "../lib/pricing/fx.mjs";
import { buildSessionFxSignals, calculateDay } from "../lib/pricing/pricing.mjs";
import { readFile } from "node:fs/promises";
import path from "node:path";

const backtestRoot = path.join(import.meta.dirname, "..", "backtest");

function parseArgs(argv) {
  const args = {};
  for (let i = 0; i < argv.length; i += 1) {
    const item = argv[i];
    if (!item.startsWith("--")) continue;
    const key = item.slice(2);
    const next = argv[i + 1];
    if (!next || next.startsWith("--")) args[key] = true;
    else { args[key] = next; i += 1; }
  }
  return args;
}

const args = parseArgs(process.argv.slice(2));
const days = Number(args.days ?? 91);
const endDate = args.end ?? "2026-09-10";
const startDate = addDays(endDate, -(days - 1));
const publishDates = dateRange(startDate, endDate);

const config = JSON.parse(await readFile(path.join(backtestRoot, "config.json"), "utf8"));
const pricing = config.pricing;

console.log(`실제 lib/pricing 코드로 FX-only 백테스트 (검색지수=0으로 고정, 환율 성분만 격리)`);
console.log(`기간: ${startDate} ~ ${endDate} (${days}일, publishDates=${publishDates.length})`);
console.log(`ECOS 자격 모드: ${process.env.BOK_ECOS_API_KEY ? "api-key" : "sample"}\n`);

const fxResult = await fetchUsdKrwOpenCloseRates({
  startDate: addDays(startDate, -14),
  endDate,
  log: (msg) => console.log("  ", msg),
});

const fxSignals = buildSessionFxSignals({
  closesByDate: fxResult.closesByDate,
  opensByDate: fxResult.opensByDate,
  publishDates,
});

const rows = [];
for (const publishDate of publishDates) {
  for (const sessionKey of ["morning", "afternoon"]) {
    const fx = fxSignals[publishDate]?.[sessionKey];
    if (!fx) continue;
    const calc = calculateDay({
      searchRatio: 0,
      fxDeclinePct: fx.declinePct,
      basePriceWon: 4500,
      pricing,
    });
    const hitDiscountCap = calc.fxRawAdjustmentPct >= 0 && calc.fxAdjustmentPct >= pricing.fxDiscountCapPct - 1e-9;
    const hitSurchargeCap = calc.fxRawAdjustmentPct < 0 && calc.fxAdjustmentPct <= -pricing.fxSurchargeCapPct + 1e-9;
    rows.push({
      publishDate,
      session: sessionKey,
      reference: fx.reference,
      declinePct: fx.declinePct,
      previousRate: fx.previousRate,
      currentRate: fx.currentRate,
      carriedForward: fx.carriedForward,
      fxRawAdjustmentPct: calc.fxRawAdjustmentPct,
      fxAdjustmentPct: calc.fxAdjustmentPct,
      capped: hitDiscountCap || hitSurchargeCap,
    });
  }
}

function summarize(label, filterFn) {
  const subset = rows.filter(filterFn);
  const declines = subset.map((r) => r.declinePct);
  const adjustments = subset.map((r) => r.fxAdjustmentPct);
  const cappedCount = subset.filter((r) => r.capped).length;
  const maxDecline = Math.max(...declines);
  const minDecline = Math.min(...declines);
  const avgAbsDecline = declines.reduce((a, b) => a + Math.abs(b), 0) / declines.length;
  console.log(`\n=== ${label} (n=${subset.length}) ===`);
  console.log(`  하락률 평균|값|: ${avgAbsDecline.toFixed(4)}%  최대하락(=최대 declinePct): ${maxDecline.toFixed(4)}%  최대상승: ${minDecline.toFixed(4)}%`);
  console.log(`  캡에 걸린 세션 수: ${cappedCount} (${(cappedCount / subset.length * 100).toFixed(2)}%)`);
  const sorted = [...subset].sort((a, b) => b.declinePct - a.declinePct).slice(0, 5);
  console.log(`  하락률 TOP5:`);
  for (const r of sorted) {
    console.log(`    ${r.publishDate} ${r.session.padEnd(9)} rate ${r.previousRate}->${r.currentRate}  declinePct=${r.declinePct.toFixed(3)}%  rawAdj=${r.fxRawAdjustmentPct.toFixed(2)}%p  cappedAdj=${r.fxAdjustmentPct.toFixed(2)}%p  carriedForward=${r.carriedForward}`);
  }
}

summarize("전체 (오전+오후)", () => true);
summarize("오전 06:00 세션 (PREVIOUS_CLOSE_TO_CLOSE)", (r) => r.session === "morning");
summarize("오후 16:00 세션 (PREVIOUS_CLOSE_TO_TODAY_OPEN)", (r) => r.session === "afternoon");

console.log(`\n총 세션 수: ${rows.length} (publishDates=${publishDates.length} x 2, 결측 제외)`);
console.log(`carriedForward(주말/공휴일로 값 이월)된 세션 수: ${rows.filter((r) => r.carriedForward).length}`);
console.log(`\n샘플 원본 rate 5건 (진짜 시장 환율인지 육안 확인용):`);
for (const r of rows.slice(0, 5)) {
  console.log(`  ${r.publishDate} ${r.session}: ${r.previousRate} -> ${r.currentRate}`);
}
