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
    console.log('--- Testing prototype-v8.html (MiniGame Paradise) ---');
    const page = await browser.newPage({ viewport: { width: 390, height: 844 } });
    const errors = [];
    page.on('pageerror', e => errors.push(e.message));
    page.on('console', msg => {
      if (msg.type() === 'error') errors.push(msg.text());
    });

    await page.goto(pathToFileURL(path.resolve(__dirname, '../..', 'prototypes', 'stock', 'prototype-v8.html')).href);
    await page.waitForTimeout(500);

    // 1. 미니게임 탭 이동
    console.log('Step 1: Switching to Arcade tab...');
    await page.locator('.bottom-nav .nav-item:nth-child(3)').click();
    await page.waitForTimeout(300);

    // 5개 게임 카드 존재하는지 확인
    const gameCards = await page.locator('.game-card-item').count();
    console.log('Game cards count:', gameCards);
    assert.equal(gameCards, 5, 'Must have 5 games');

    // 2. 게임 1 (골든 슬라이스) 플레이 & 랭킹 등록
    console.log('Step 2: Testing Game 1 (Golden Slice)...');
    await page.locator('.game-card-item:nth-child(1)').click();
    await page.waitForTimeout(300);
    assert.equal(await page.locator('#gameStageModal.active').count(), 1);

    // 자르기 버튼 클릭
    await page.locator('#gameActionBtn').click();
    await page.waitForTimeout(300);

    // 결과 화면 노출 확인
    assert.equal(await page.locator('#screenResult').isVisible(), true);
    console.log('Score:', await page.locator('#resultFinalScore').innerText());

    // 닉네임 입력 & 랭킹 등록
    await page.locator('#playerNickname').fill('골든칼잡이');
    await page.locator('#screenResult button.btn-cute:has-text("랭킹 등록")').click();
    await page.waitForTimeout(300);

    // 랭킹 화면 노출 & 10위 캡 확인
    assert.equal(await page.locator('#screenLeaderboard').isVisible(), true);
    const countRank = await page.locator('#stageRankList .rank-item').count();
    console.log('Rank list items in modal:', countRank);
    assert.ok(countRank <= 10, 'Must not exceed 10');

    // 닫기
    await page.locator('#screenLeaderboard button:has-text("게임 목록")').click();
    await page.waitForTimeout(300);

    // 3. 게임 5 (황금 포춘쿠키)
    console.log('Step 3: Testing Game 5 (Fortune Cookie)...');
    await page.locator('.game-card-item:nth-child(5)').click();
    await page.waitForTimeout(300);
    await page.locator('#g5Cookie').click();
    await page.waitForTimeout(500);

    assert.equal(await page.locator('#screenResult').isVisible(), true);
    await page.locator('#playerNickname').fill('대박쿠키');
    await page.locator('#screenResult button.btn-cute:has-text("랭킹 등록")').click();
    await page.waitForTimeout(300);

    // 랭킹 스크린샷 캡처
    await page.screenshot({ path: 'minigame-ranking-preview.png' });
    console.log('minigame-ranking-preview.png captured successfully.');

    await page.locator('#screenLeaderboard button:has-text("게임 목록")').click();
    await page.waitForTimeout(300);

    // 메인 아케이드 스크린샷 캡처
    await page.screenshot({ path: 'minigame-arcade-preview.png' });
    console.log('minigame-arcade-preview.png captured successfully.');

    console.log('\nAll tests passed with 0 errors! Page errors:', errors);
    assert.equal(errors.length, 0, 'Must have zero page errors');
  } catch (err) {
    console.error('Test failed:', err);
    process.exit(1);
  } finally {
    await browser.close();
  }
})();
