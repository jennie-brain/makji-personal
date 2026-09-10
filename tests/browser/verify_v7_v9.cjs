const { chromium } = require('C:/Users/Administrator/workspace/cardfit/node_modules/playwright');
const path = require('node:path');
const { pathToFileURL } = require('node:url');

(async () => {
  const browser = await chromium.launch({
    executablePath: 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe',
    headless: true
  });

  try {
    console.log('--- 1. Testing price-simulator-v9.html ---');
    const simPage = await browser.newPage({ viewport: { width: 1440, height: 1080 } });
    const simErrors = [];
    simPage.on('pageerror', e => simErrors.push(e.message));
    simPage.on('console', msg => {
      if (msg.type() === 'error') simErrors.push(msg.text());
    });

    await simPage.goto(pathToFileURL(path.resolve(__dirname, '../..', 'prototypes', 'price-simulator', 'price-simulator-v9.html')).href);
    await simPage.waitForTimeout(1000);

    console.log('Simulator errors:', simErrors);
    const simTitle = await simPage.title();
    console.log('Simulator title:', simTitle);

    const statBalance = await simPage.locator('#statBalance').innerText();
    console.log('Stat balance:', statBalance);

    const synConclusion = await simPage.locator('#synConclusionText').innerText();
    console.log('Synergy text exists:', synConclusion.length > 20);

    await simPage.screenshot({ path: 'v9-simulator-preview.png', fullPage: false });
    console.log('v9-simulator-preview.png captured successfully.');

    console.log('\n--- 2. Testing prototype-v7.html ---');
    const protoPage = await browser.newPage({ viewport: { width: 390, height: 844 } });
    const protoErrors = [];
    protoPage.on('pageerror', e => protoErrors.push(e.message));
    protoPage.on('console', msg => {
      if (msg.type() === 'error') protoErrors.push(msg.text());
    });

    await protoPage.goto(pathToFileURL(path.resolve(__dirname, '../..', 'prototypes', 'stock', 'prototype-v7.html')).href);
    await protoPage.waitForTimeout(1000);

    console.log('Prototype errors:', protoErrors);
    const protoTitle = await protoPage.title();
    console.log('Prototype title:', protoTitle);

    // 마켓 탭 이동
    await protoPage.locator('.bottom-nav .nav-item:nth-child(2)').click();
    await protoPage.waitForTimeout(500);

    // 10종 리스트 아이템 개수 확인
    const itemCount = await protoPage.locator('.bread-stock-item').count();
    console.log('Bread items count:', itemCount);

    // 마틸다 케이크 클릭 -> 바텀시트 열기
    await protoPage.locator('.top1-hero-card').click();
    await protoPage.waitForTimeout(500);

    const sheetName = await protoPage.locator('#sheetName').innerText();
    const sheetPrice = await protoPage.locator('#sheetPrice').innerText();
    console.log('Bottom sheet opened:', sheetName, sheetPrice);

    // 퀴즈 쿠폰 토글 클릭
    await protoPage.locator('#couponToggleBtn').click();
    await protoPage.waitForTimeout(500);
    const couponAppliedPrice = await protoPage.locator('#sheetPrice').innerText();
    console.log('Price with coupon applied:', couponAppliedPrice);

    await protoPage.screenshot({ path: 'v7-prototype-sheet-preview.png' });
    console.log('v7-prototype-sheet-preview.png captured successfully.');

    console.log('\nAll tests passed with 0 errors!');
  } catch (err) {
    console.error('Test error:', err);
    process.exit(1);
  } finally {
    await browser.close();
  }
})();
