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
    console.log('--- Verifying prototype-v10.html Full User Flow & Capturing Deck Slides ---');
    const page = await browser.newPage({ viewport: { width: 390, height: 844 } });
    const errors = [];
    page.on('pageerror', e => errors.push(e.message));
    page.on('console', msg => {
      if (msg.type() === 'error') errors.push(msg.text());
    });

    await page.goto(pathToFileURL(path.resolve(__dirname, '../..', 'prototypes', 'stock', 'prototype-v10.html')).href);
    await page.waitForTimeout(500);

    // [Slide 1] 홈 화면 캡처
    console.log('Step 1: Capturing Flow 1 - Home Dashboard...');
    await page.screenshot({ path: 'flow-1-home-dashboard.png' });

    // [Slide 2] 시세표 탭 이동 & 토스 멀티뷰 차트 오픈
    console.log('Step 2: Testing Market & Chart Bottomsheet...');
    await page.locator('.bottom-nav .nav-item:nth-child(2)').click();
    await page.waitForTimeout(300);
    // 마틸다 케이크 클릭
    await page.locator('#marketListContainer .bread-stock-item:last-child').click();
    await page.waitForTimeout(400);
    assert.equal(await page.locator('#tossSheet.open').count(), 1, 'Sheet must be open');
    
    // 혜택 밴드 모드로 전환하여 캡처
    await page.locator('#btnMode3').click();
    await page.waitForTimeout(300);
    await page.screenshot({ path: 'flow-2-chart-bottomsheet.png' });

    // 장바구니 담기 버튼 클릭
    await page.locator('#sheetCtaBtn').click();
    await page.waitForTimeout(300);

    // [Slide 3] RFP 확장: Bakery ETF & FX 마켓
    console.log('Step 3: Testing RFP Expansion (Bakery ETF & FX)...');
    await page.locator('.bottom-nav .nav-item:nth-child(3)').click();
    await page.waitForTimeout(300);
    // ETF 하나 장바구니 담기
    await page.locator('.etf-card button').first().click();
    await page.waitForTimeout(200);
    await page.screenshot({ path: 'flow-3-expansion-etf.png' });

    // FX 탭 서브 전환
    await page.locator('#btnSubFx').click();
    await page.waitForTimeout(300);
    await page.screenshot({ path: 'flow-3-expansion-fx.png' });

    // [Slide 4] 미니게임천국 & 쿠폰 발급
    console.log('Step 4: Testing Arcade & 500w Coupon Generation...');
    await page.locator('.bottom-nav .nav-item:nth-child(4)').click();
    await page.waitForTimeout(300);
    // 골든 슬라이스 실행
    await page.locator('.game-card-item:nth-child(1)').click();
    await page.waitForTimeout(300);
    await page.locator('#gameActionBtn').click();
    await page.waitForTimeout(300);

    const rewardText = await page.locator('#rewardNotificationBox').innerText();
    console.log('Coupon Reward Text:', rewardText);
    assert.ok(rewardText.includes('500원 할인 쿠폰'), 'First play must generate coupon');

    // 랭킹 등록
    await page.locator('#playerNickname').fill('발표자');
    await page.locator('#screenResult button:has-text("랭킹 등록")').click();
    await page.waitForTimeout(300);
    await page.screenshot({ path: 'flow-4-arcade-reward.png' });
    await page.locator('#screenLeaderboard button:has-text("목록")').click();
    await page.waitForTimeout(200);

    // [Slide 5] 장바구니 & 카페24 주문서 결제
    console.log('Step 5: Testing Cart & Cafe24 Checkout Flow...');
    await page.locator('.bottom-nav .nav-item:nth-child(5)').click();
    await page.waitForTimeout(400);
    await page.screenshot({ path: 'flow-5-cart-receipt.png' });

    // 카페24 결제 모달 열기
    await page.locator('button:has-text("카페24 간편결제로 주문하기")').click();
    await page.waitForTimeout(300);
    assert.equal(await page.locator('#checkoutModal.open').count(), 1, 'Checkout modal must open');
    await page.screenshot({ path: 'flow-6-checkout-modal.png' });

    // 결제 승인 클릭
    await page.locator('#btnSubmitPayment').click();
    // 1초 결제 시뮬레이션 대기
    await page.waitForTimeout(1400);

    // 주문 완료 화면 확인
    assert.equal(await page.locator('#viewOrderComplete.active').count(), 1, 'Order complete view must be active');
    await page.screenshot({ path: 'flow-7-order-complete.png' });
    console.log('Order completed successfully!');

    console.log('\nAll 5-Step User Flow tests passed with 0 errors! Page errors:', errors);
    assert.equal(errors.length, 0, 'Must have zero page errors');
  } catch (err) {
    console.error('Test failed:', err);
    process.exit(1);
  } finally {
    await browser.close();
  }
})();
