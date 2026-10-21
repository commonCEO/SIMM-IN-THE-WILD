import assert from 'node:assert/strict';
import{readFile}from'node:fs/promises';
import{chromium}from'playwright';
const browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||undefined,args:['--no-sandbox']});
try{
 const page=await browser.newPage({viewport:{width:1920,height:1080}}),errors=[],requests=[];
 page.on('pageerror',e=>errors.push(e.message));page.on('request',r=>requests.push(r.url()));
 await page.setContent(await readFile(new URL('../index.html',import.meta.url),'utf8'));
 await page.locator('.language-choices [data-language=et]').click();await page.getByRole('button',{name:'Alusta seiklust'}).click();await page.waitForTimeout(250);
 await page.keyboard.press('KeyI');assert.equal(await page.locator('.bag-grid .inv-slot').count(),20);await page.getByRole('button',{name:'Sulge',exact:true}).click();
 await page.getByRole('button',{name:'♫ Heli väljas'}).click();assert.equal(await page.locator('#audioButton').getAttribute('aria-pressed'),'true');
 await page.keyboard.press('KeyK');await page.getByRole('tab',{name:'OSKUSED',exact:true}).click();assert.equal(await page.locator('.skill-node').count(),13);assert.equal(await page.locator('#modalDetail').isVisible(),true);await page.getByRole('button',{name:'Sulge',exact:true}).click();
 await page.keyboard.press('Escape');await page.getByRole('button',{name:'Uus mäng',exact:true}).click();await page.getByRole('button',{name:'Jah, alusta uut mängu'}).click();assert.equal(await page.locator('#dayLabel').textContent(),'1. päev');
 await page.waitForTimeout(300);await page.screenshot({path:'/tmp/simm-standalone03.png'});
 assert.deepEqual(errors,[]);assert.deepEqual(requests,[]);console.log('PASS: standalone game, embedded art, large skill menu, audio and New Game work without asset requests.');
 await page.close();
 for(const filename of ['index.html','play/index.html']){
  const context=await browser.newContext({viewport:{width:1440,height:900}}),external=[];let file=await context.newPage();
  file.on('pageerror',e=>errors.push(e.message));file.on('request',r=>{if(/^https?:/.test(r.url())&&r.resourceType()!=='document')external.push(r.url());});
  try{await file.goto(new URL('../'+filename,import.meta.url).href);}catch(e){if(!String(e).includes('ERR_BLOCKED_BY_ADMINISTRATOR'))throw e;console.log('SKIP direct file URL: managed browser policy blocks file navigation; checking embedded build over HTTP:',filename);await file.close();file=await context.newPage();file.on('pageerror',e=>errors.push(e.message));file.on('request',r=>{if(/^https?:/.test(r.url())&&r.resourceType()!=='document')external.push(r.url());});await file.goto((process.env.TEST_URL||'http://127.0.0.1:3000')+'/'+filename);}await file.locator('.language-choices [data-language=et]').click();await file.getByRole('button',{name:'Alusta seiklust'}).click();await file.keyboard.press('KeyI');assert.equal(await file.locator('.bag-grid .inv-slot').count(),20);await file.getByRole('tab',{name:'OSKUSED',exact:true}).click();assert.equal(await file.locator('.skill-node').count(),13);await file.getByRole('button',{name:'Sulge',exact:true}).click();await file.evaluate(()=>window.dispatchEvent(new Event('blur')));await file.reload();await file.getByRole('button',{name:'Jätka seiklust'}).click();assert.equal(await file.locator('#dayLabel').textContent(),'1. päev');assert.deepEqual(external,[]);await context.close();
 }
 assert.deepEqual(errors,[]);console.log('PASS: both standalone HTML files start, save/reload and make no external asset requests (file URLs where browser policy permits).');

}finally{await browser.close();}
