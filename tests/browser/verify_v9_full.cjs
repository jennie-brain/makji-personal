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
    console.log('--- Testing prototype-v9.html (Full Verification) ---');
    const page = await browser.newPage({ viewport: { width: 390, height: 844 } });
    const errors = [];
    page.on('pageerror', e => errors.push(e.message));
    page.on('console', msg => {
      if (msg.type() === 'error') errors.push(msg.text());
    });

    await page.goto(pathToFileURL(path.resolve(__dirname, '../..', 'prototypes', 'stock', 'prototype-v9.html')).href);
    await page.waitForTimeout(500);

    // 1. 마켓 탭 & 바텀시트 멀티뷰 차트 테스트
    console.log('Step 1: Testing Market tab & Multi-view Chart...');
    await page.locator('.bottom-nav .nav-item:nth-child(2)').click();
    await page.waitForTimeout(300);

    // 마틸다 케이크 클릭
    await page.locator('.bread-stock-item:last-child').click();
    await page.waitForTimeout(400);

    assert.equal(await page.locator('#tossSheet.open').count(), 1, 'Bottom sheet must be open');
    console.log('Sheet opened for:', await page.locator('#sheetName').innerText());

    // 차트 모드 2 (일봉 캔들) 전환
    console.log('Switching to Mode 2 (Candle)...');
    await page.locator('#btnMode2').click();
    await page.waitForTimeout(400);
    assert.equal(await page.locator('#btnMode2.active').count(), 1);

    // 차트 모드 3 (혜택 밴드) 전환
    console.log('Switching to Mode 3 (Benefit Band)...');
    await page.locator('#btnMode3').click();
    await page.waitForTimeout(400);
    assert.equal(await page.locator('#btnMode3.active').count(), 1);

    // 바텀시트 닫기
    await page.locator('.modal-overlay').click({ position: { x: 10, y: 10 } });
    await page.waitForTimeout(300);

    // 2. 미니게임천국 & 1일 1회 데일리 쿠폰 캡 테스트
    console.log('Step 2: Testing Arcade & 1-per-day Coupon Cap...');
    await page.locator('.bottom-nav .nav-item:nth-child(3)').click();
    await page.waitForTimeout(300);

    // 게임 1 (골든 슬라이스) 첫 판 플레이
    await page.locator('.game-card-item:nth-child(1)').click();
    await page.waitForTimeout(300);
    await page.locator('#gameActionBtn').click();
    await page.waitForTimeout(300);

    // 첫 판: 쿠폰 지급 확인
    const rewardBox1 = await page.locator('#rewardNotificationBox').innerText();
    console.log('First play reward message:', rewardBox1);
    assert.ok(rewardBox1.includes('500원 할인 쿠폰 발급 완료'), 'First play must give coupon');

    // 닉네임 입력 & 랭킹 등록
    await page.locator('#playerNickname').fill('마진수호자');
    await page.locator('#screenResult button.btn-cute:has-text("랭킹 등록")').click();
    await page.waitForTimeout(300);

    assert.equal(await page.locator('#screenLeaderboard').isVisible(), true);
    console.log('Rank registered successfully!');

    // 닫고 2번째 판 도전 (마진 방어 모드 확인)
    await page.locator('#screenLeaderboard button:has-text("게임 목록")').click();
    await page.waitForTimeout(300);

    console.log('Step 3: Testing Second Play (Margin Defense Mode)...');
    await page.locator('.game-card-item:nth-child(5)').click(); // 포춘쿠키
    await page.waitForTimeout(300);
    await page.locator('#g5Cookie').click();
    await page.waitForTimeout(400);

    // 두 번째 판: 마진 방어(쿠폰 미지급) 확인
    const rewardBox2 = await page.locator('#rewardNotificationBox').innerText();
    console.log('Second play reward message:', rewardBox2);
    assert.ok(rewardBox2.includes('마진 방어 랭킹 모드'), 'Second play must activate margin defense cap');

    await page.screenshot({ path: 'v9-prototype-full-preview.png' });
    console.log('v9-prototype-full-preview.png captured successfully.');

    console.log('\nAll tests passed with 0 errors! Page errors:', errors);
    assert.equal(errors.length, 0, 'Must have zero page errors');
  } catch (err) {
    console.error('Test failed:', err);
    process.exit(1);
  } finally {
    await browser.close();
  }
})();
