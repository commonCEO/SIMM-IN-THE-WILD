import assert from 'node:assert/strict';
import{readFile}from'node:fs/promises';
import{chromium}from'playwright';
const browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||undefined,args:['--no-sandbox']});
try{
 const page=await browser.newPage({viewport:{width:1920,height:1080}}),errors=[],requests=[];
 page.on('pageerror',e=>errors.push(e.message));page.on('request',r=>requests.push(r.url()));
 await page.setContent(await readFile(new URL('../index.html',import.meta.url),'utf8'));
 await page.getByRole('button',{name:'Alusta seiklust'}).click();await page.waitForTimeout(250);
 await page.keyboard.press('KeyI');assert.equal(await page.locator('.bag-grid .inv-slot').count(),20);await page.getByRole('button',{name:'Sulge',exact:true}).click();
 await page.getByRole('button',{name:'♫ Heli väljas'}).click();assert.equal(await page.locator('#audioButton').getAttribute('aria-pressed'),'true');
 await page.keyboard.press('KeyK');assert.equal(await page.locator('.skill-node').count(),12);assert.equal(await page.locator('#modalDetail').isVisible(),true);await page.getByRole('button',{name:'Sulge',exact:true}).click();
 await page.keyboard.press('Escape');await page.getByRole('button',{name:'Uus mäng',exact:true}).click();await page.getByRole('button',{name:'Jah, alusta uut mängu'}).click();assert.equal(await page.locator('#dayLabel').textContent(),'1. päev');
 await page.waitForTimeout(300);await page.screenshot({path:'/tmp/simm-standalone03.png'});
 assert.deepEqual(errors,[]);assert.deepEqual(requests,[]);console.log('PASS: standalone game, embedded art, large skill menu, audio and New Game work without asset requests.');
}finally{await browser.close();}
