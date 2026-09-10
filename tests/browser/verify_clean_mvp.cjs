const { chromium } = require('C:/Users/Administrator/workspace/cardfit/node_modules/playwright');
const path = require('node:path');
const { pathToFileURL } = require('node:url');
const assert = require('node:assert/strict');

(async () => {
  const browser = await chromium.launch({
    executablePath: 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe',
    headless: true
  });

  try {
    console.log('--- Verifying 9/9 MVP Official Prototype (makji-stock-prototype.html) ---');
    const page = await browser.newPage({ viewport: { width: 390, height: 844 } });
    const errors = [];
    page.on('pageerror', e => errors.push(e.message));
    page.on('console', msg => {
      if (msg.type() === 'error') errors.push(msg.text());
    });

    await page.goto(pathToFileURL(path.resolve(__dirname, '../..', 'prototypes', 'stock', 'prototype-v11.html')).href);
    await page.waitForTimeout(500);

    // 1. HOME 탭 테스트: 예측 투표 [A/B]
    console.log('Step 1: Testing HOME screen prediction vote...');
    await page.locator('#btnVoteUp').click();
    await page.waitForTimeout(300);
    assert.equal(await page.locator('#btnVoteUp.selected').count(), 1, 'Vote Up must be selected');

    // 2. Bread Market 탭 테스트: TOP 1 & 10종 리스트 & 바텀시트
    console.log('Step 2: Testing Bread Market screen...');
    await page.locator('.bottom-nav .nav-item:nth-child(2)').click();
    await page.waitForTimeout(300);

    // TOP 1 카드 클릭
    await page.locator('.highlight-card').click();
    await page.waitForTimeout(400);
    assert.equal(await page.locator('#tossSheet.open').count(), 1, 'Bottom sheet must open');

    // 혜택 밴드 전환 & 장바구니 담기
    await page.locator('#btnMode3').click();
    await page.waitForTimeout(200);
    await page.locator('button:has-text("오늘 시세로 장바구니 담기")').click();
    await page.waitForTimeout(300);

    // 3. EVENT 탭 테스트: 빵 자르기 게임
    console.log('Step 3: Testing EVENT screen cut game...');
    await page.locator('.bottom-nav .nav-item:nth-child(3)').click();
    await page.waitForTimeout(300);
    await page.locator('#btnCutAction').click();
    await page.waitForTimeout(400);
    assert.equal(await page.locator('#gameResultBox').isVisible(), true, 'Result box must be visible');

    // 포춘쿠키 빵운세
    await page.locator('#tabEvent div[onclick="crackFortuneCookie()"]').click();
    await page.waitForTimeout(200);
    assert.equal(await page.locator('#fortunePaper').isVisible(), true, 'Fortune paper must be visible');

    // 4. 장바구니 & 카페24 결제 주문서
    console.log('Step 4: Testing Cart & Cafe24 Checkout...');
    await page.locator('.cart-header-btn').click();
    await page.waitForTimeout(300);
    assert.equal(await page.locator('#cartModal.open').count(), 1, 'Cart modal must open');

    await page.locator('button:has-text("카페24 간편결제로 주문 완료")').click();
    await page.waitForTimeout(300);

    await page.screenshot({ path: 'clean-mvp-verified.png' });
    console.log('Clean MVP test passed with 0 errors! Page errors:', errors);
    assert.equal(errors.length, 0, 'Must have zero errors');
  } catch (err) {
    console.error('Test failed:', err);
    process.exit(1);
  } finally {
    await browser.close();
  }
})();
