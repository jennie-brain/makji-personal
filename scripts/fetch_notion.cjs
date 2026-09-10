const { chromium } = require('C:/Users/Administrator/workspace/cardfit/node_modules/playwright');
const fs = require('fs');
const path = require('node:path');
const os = require('node:os');

(async () => {
  const browser = await chromium.launch({
    executablePath: 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe',
    headless: true
  });

  const page = await browser.newPage({ viewport: { width: 1280, height: 1000 } });
  
  const targetUrl = 'https://app.notion.com/p/3d44d2757f86808996c1cd8c025e11fb?v=3d44d2757f8680559d8f000ccea7e138&p=3d64d2757f8680df8c76d05e59fc3e24&pm=s';
  console.log('Navigating to:', targetUrl);

  try {
    await page.goto(targetUrl, { waitUntil: 'networkidle', timeout: 30000 });
  } catch (e) {
    console.log('Navigation networkidle timeout, continuing anyway...');
  }

  // 대기 시간 조금 부여
  await page.waitForTimeout(5000);

  // 스크린샷 저장
  await page.screenshot({ path: path.join(os.tmpdir(), 'makji-notion-preview.png'), fullPage: true });
  console.log('Saved screenshot to notion_preview.png');

  // 본문 텍스트 추출
  const bodyText = await page.evaluate(() => document.body.innerText);
  fs.writeFileSync(path.resolve(__dirname, '../research/raw/notion_extracted_text.txt'), bodyText, 'utf-8');
  console.log('Saved body text, length:', bodyText.length);

  // 페이지 타이틀
  const title = await page.title();
  console.log('Page title:', title);

  await browser.close();
})();
