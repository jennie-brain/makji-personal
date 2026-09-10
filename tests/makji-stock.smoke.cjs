// Usage: node tests/makji-stock.smoke.cjs [path to installed playwright]
const { chromium } = require(process.argv[2] || 'playwright');
const assert = require('node:assert/strict');
const path = require('node:path');
const { pathToFileURL } = require('node:url');
(async () => {
  const browser = await chromium.launch({ executablePath: 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe', headless: true });
  try {
    const page = await browser.newPage({ viewport: { width: 390, height: 844 } });
    const errors = [];
    page.on('pageerror', e => errors.push(e.message));
    await page.goto(pathToFileURL(path.resolve(__dirname, '../index.html')).href);
    assert.deepEqual(errors, [], 'Page initialization errors');
    assert.equal(await page.locator('.product-row').count(), 10);
    assert.equal(await page.locator('.rank-row').count(), 5);
    assert.equal(await page.evaluate(() => quote(product('cake')).price), 39930);
    assert.equal(await page.evaluate(() => products.filter(p => quote(p).price < p.base).length), 8);
    assert.equal(await page.evaluate(() => {
      for (const p of products) for (let i = 0; i < 100; i++) {
        const q = calculate(p, i);
        if (q.trend < -6 || q.trend > 0 || Math.abs(q.kospi) > 1 || Math.abs(q.fx) > 3 || Math.abs(q.rate) > capFor(p) || q.price % 10 !== 0) return false;
      }
      return true;
    }), true);
    await page.screenshot({ path: 'makji-stock-home-preview.png', fullPage: true });
    await page.locator('[data-vote="down"]').click();
    await page.locator('#voteModal.show').waitFor();
    assert.match(await page.locator('#voteMessage').innerText(), /내린다/);
    await page.locator('#copyCode').click();
    await page.keyboard.press('Escape');
    await page.locator('.nav [data-tab="market"]').click();
    const before = await page.locator('#productList').innerText();
    await page.locator('[data-mode="weekend"]').click();
    assert.equal(await page.locator('#nextQuote').isDisabled(), true);
    assert.equal(await page.locator('#productList').innerText(), before);
    await page.locator('[data-mode="weekday"]').click();
    await page.locator('#highlight').click();
    assert.equal(await page.locator('#sheetPrice').innerText(), '39,930원');
    for (const period of ['month', 'day', 'week']) await page.locator('[data-period="' + period + '"]').click();
    await page.locator('#addCart').click();
    assert.equal(await page.evaluate(() => state.cart.length), 1);
    await page.screenshot({ path: 'makji-stock-sheet-preview.png' });
    await page.keyboard.press('Escape');
    await page.locator('.nav [data-tab="home"]').click();
    await page.locator('.news-item[data-news="1"]').click();
    await page.locator('[data-article="0"]').click();
    await page.locator('#articleCta').click();
    assert.equal(await page.locator('#sheetName').innerText(), '글루텐프리 스콘');
    assert.equal(await page.evaluate(() => state.tab), 'market');
    await page.keyboard.press('Escape');
    await page.locator('.nav [data-tab="events"]').click();
    await page.locator('#cookie').click();
    assert.equal(await page.locator('#cookieStage.opened').count(), 1);
    await page.locator('#cutRange').fill('50');
    await page.locator('#cutButton').click();
    assert.match(await page.locator('#gameResult').innerText(), /GOLDEN10/);
    await page.locator('#cutRange').fill('42.3');
    await page.locator('#cutButton').click();
    assert.match(await page.locator('#gameResult').innerText(), /7.70%p/);
    for (const width of [320, 390, 430, 1280]) {
      await page.setViewportSize({ width, height: 900 });
      for (const name of ['home', 'market', 'events']) {
        await page.locator('.nav [data-tab="' + name + '"]').click();
        assert.equal(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth), true, 'Overflow: ' + name + ' @ ' + width);
      }
    }
    const offline = await browser.newPage({ viewport: { width: 390, height: 844 } });
    await offline.route('https://**', r => r.abort());
    await offline.goto(pathToFileURL(path.resolve(__dirname, '../index.html')).href);
    await offline.locator('.nav [data-tab="market"]').click();
    await offline.locator('#highlight').click();
    assert.match(await offline.locator('#chartNote').innerText(), /오프라인/);
    assert.deepEqual(errors, []);
    console.log('PASS: prices, caps, 10 products, rankings, quiz, clipboard action, weekend freeze, chart periods, cart, newsletter deep link, fortune, game, 4 viewport widths, CDN-blocked fallback; Chart.js=' + await page.evaluate(() => window.Chart?.version || 'fallback'));
  } finally { await browser.close(); }
})().catch(e => { console.error(e); process.exitCode = 1; });
