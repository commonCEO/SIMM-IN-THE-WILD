import { tr, getLanguage, setLanguage, localizedData } from './i18n.js';
import { toggleAudio, sound, updateAudio, setVolume } from './audio.js';
import { freshState, recipes as sourceRecipes, skills as sourceSkills, names as sourceNames, icons, tools as sourceTools, pay, canPay, gainXP, canUpgrade, upgrade, maxHealth, advanceTime, addItem, usedSlots, STACK_SIZE, dropItem, bowStats, inWater, lakeWater, wallOrientation, questSteps as sourceQuestSteps, biomeAt, heightAt, canStep, rotateVector, projectPoint, sceneBuildings, availableInventory, payNearby, transferItem, craftItem, crops as sourceCrops, plantCrop, cropProgress, harvestCrop, usePotion, tickEffects, regrowResources, predatorIntent, findHouses, houseExitPoint, canAscend, npcData as sourceNpcData, finishNPCQuest, whaleStep, forageDefs as sourceForageDefs, looseResources, gatherLoose, solidBuildingAt, buildingBounds, resetHostilesAfterDefeat, firstPickaxeStep as sourceFirstPickaxeStep } from './model.js';

const names=localizedData(sourceNames), tools=localizedData(sourceTools), recipes=localizedData(sourceRecipes), skills=localizedData(sourceSkills), crops=Object.fromEntries(Object.entries(sourceCrops).map(([id,c])=>[id,localizedData(c)])), npcData=localizedData(sourceNpcData), forageDefs=Object.fromEntries(Object.entries(sourceForageDefs).map(([id,d])=>[id,localizedData(d)]));
const questSteps=s=>sourceQuestSteps(s).map(localizedData), firstPickaxeStep=s=>localizedData(sourceFirstPickaxeStep(s));
const $ = id => document.getElementById(id);
const canvas = $('game'), ctx = canvas.getContext('2d');

const staticCopy=[];
function captureStaticCopy(){
 const walker=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT,{acceptNode:n=>n.parentElement.closest('script,style,canvas')?NodeFilter.FILTER_REJECT:NodeFilter.FILTER_ACCEPT});
 while(walker.nextNode()){const node=walker.currentNode;if(node.textContent.trim())staticCopy.push({node,source:node.textContent});}
 for(const node of document.querySelectorAll('[aria-label],[title]'))for(const attribute of ['aria-label','title'])if(node.hasAttribute(attribute))staticCopy.push({node,attribute,source:node.getAttribute(attribute)});
 staticCopy.push({node:document.querySelector('title').firstChild,source:document.title});
}
function applyStaticLanguage(){for(const entry of staticCopy){if(entry.attribute)entry.node.setAttribute(entry.attribute,tr(entry.source));else entry.node.textContent=tr(entry.source);}document.documentElement.lang=getLanguage();document.querySelectorAll('[data-language]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.language===getLanguage())));}
function changeLanguage(value){setLanguage(value);applyStaticLanguage();$('audioButton').textContent=tr($('audioButton').getAttribute('aria-pressed')==='true'?'♫ Heli sees':'♫ Heli väljas');questTrackerCache='';targetLock=null;refresh();if(saveFound){$('startButton').textContent=tr('Jätka seiklust →');document.querySelector('.intro-card p').textContent=tr('Sinu mets, varud ja ehitised on alles. Versioon 0.4.3 ootab uut seiklust.');}if(assetsReady)$('loadStatus').textContent=tr('WASD + hiir või Xboxi pult · A alustab · Y uus mäng');if(menuKind)openModal(menuKind);updateHUD();draw();}
captureStaticCopy();applyStaticLanguage();
$('languageButton').onclick=()=>openModal('language');document.querySelectorAll('.language-choices [data-language]').forEach(b=>b.onclick=()=>changeLanguage(b.dataset.language));
const TILE=32, W=64, H=48;
const base={x:31*TILE,y:29*TILE}, cave={x:33*TILE,y:16*TILE}, meteor={x:45*TILE,y:27*TILE};
let seed=1742;
function rand(){seed=(seed*1664525+1013904223)>>>0;return seed/4294967296;}
const state=freshState();
state.player={x:base.x,y:base.y+64,face:1,walk:0};
let saveFound=false,saveVersion=4;
try {
  const saved=JSON.parse(localStorage.getItem('simm-save-v1')||'null');
  if(saved?.state?.inventory&&Number.isFinite(saved.state.player?.x)){
    saveVersion=saved.version||1;Object.assign(state,saved.state);
    state.inventory={...freshState().inventory,...saved.state.inventory};
    state.skills={...freshState().skills,...saved.state.skills};
    state.drops=state.drops||[];state.stumpsRemoved=state.stumpsRemoved||[];
    state.alienFollowing=state.alienFollowing??true;state.camera=((state.camera||0)%4+4)%4;state.jump=0;
    saveFound=true;
  }
}catch{}
let assetsReady=false;
let started=false,paused=false,last=0,elapsed=0,cam={x:0,y:0},keys={},tool=0,buildType=null,rotation='auto',toastTime=0,actionCooldown=0,autosave=0,padPrevious={},padMoveAt=0,menuIndex=0,menuKind=null,menuCache=[],menuDirection=null,menuRepeatAt=0,selectedSkill=null;
let cliffHintUntil=0,buildCursor=null,buildDirection=null,buildRepeatAt=0,inputMode='mouse',targetLock=null;
const pickups=[];
let aim={x:1,y:0},charge=null,invulnerable=0,damageFlash=0,death=null,fishing=null,currentTarget=null,meteorFall=null;
const particles=[],resources=[],animals=[],zombies=[],bats=[],arrows=[];
const water=inWater;
const mainTabs=['bag','journal','craft','build','skills','map'];
const tabNames=['SELJAKOTT','ÜLESANDED','MEISTERDAMINE','EHITAMINE','OSKUSED','KAART'];
const menuSelections={};let chestOpen=null,gardenOpen=null,npcOpen=null,whaleGame=null,whaleHeld=false,worldTick=0;
function canPayLocal(cost){return canPay({inventory:availableInventory(state)},cost);}
function worldItems(){return sceneBuildings(state);}
function isOutside(){return !state.inCave&&!state.interior;}
function openMain(){openModal('bag');}
function changeTab(direction){if(!mainTabs.includes(menuKind))return;const next=mainTabs[(mainTabs.indexOf(menuKind)+direction+6)%6];openModal(next);}
function drawTabs(){const tabs=$('menuTabs');tabs.replaceChildren();tabs.classList.toggle('hidden',!mainTabs.includes(menuKind));if(!mainTabs.includes(menuKind))return;mainTabs.forEach((kind,i)=>{const b=document.createElement('button');b.textContent=tr(tabNames[i]);b.setAttribute('role','tab');b.setAttribute('aria-selected',String(kind===menuKind));b.tabIndex=kind===menuKind?0:-1;b.onclick=()=>openModal(kind);tabs.append(b);});}
function rotateCamera(d){if(state.interior||state.inCave)return;state.camera=(state.camera+d+4)%4;canvas._pointer=null;draw();notify(tr('Vaade: ')+[tr('PÕHI'),tr('IDA'),tr('LÕUNA'),tr('LÄÄS')][state.camera]+tr(' · Z/V või D-pad ←/→'));}
function jump(){if(state.jump<=0&&!state.boatId){state.jumpOrigin=heightAt(state.player.x,state.player.y);state.jump=.65;state.jumps=(state.jumps||0)+1;sound('swing');}}
function useBagItem(id){if(id==='water'){if(state.thirst>=100)return;state.inventory.water--;state.thirst=Math.min(100,state.thirst+60);}else if(!usePotion(state,id))return;refresh();save();openModal('bag');}
function enterHouse(h){state.interior={id:h.id,level:0,outside:houseExitPoint(h)};state.player.x=6*32;state.player.y=7.5*32;state.boatId=null;charge=null;arrows.length=0;canvas._pointer=null;state.shelterFound=true;notify(tr('SINU KODU · ehita mööblit, kaste, vahelagesid ja trepp.'));save();}
function leaveHouse(){const out=state.interior.outside;state.interior=null;state.player.x=out.x;state.player.y=out.y;canvas._pointer=null;save();}
function respawnWildlife(){
 for(let i=state.wildlifeReturns.length-1;i>=0;i--){const r=state.wildlifeReturns[i];if(state.worldAge<r.at)continue;
  const a={...r.animal,x:r.animal.homeX??r.animal.x,y:r.animal.homeY??r.animal.y},home={x:a.x,y:a.y},region=biomeAt(a.x,a.y),points=[home];
  for(let radius=64;radius<=192;radius+=64)for(let angle=0;angle<8;angle++)points.push({x:home.x+Math.cos(angle*Math.PI/4)*radius,y:home.y+Math.sin(angle*Math.PI/4)*radius});
  const free=points.find(p=>p.x>=64&&p.y>=70&&p.x<W*32-64&&p.y<H*32-64&&!water(p.x,p.y)&&biomeAt(p.x,p.y)===region&&!state.buildings.some(b=>Math.hypot((b.x+.5)*32-p.x,(b.y+.5)*32-p.y)<55));
  if(!free)continue;Object.assign(a,free);a.hp=a.type==='bear'?7:a.type==='wolf'?4:a.type==='deer'?3:1;a.chasing=false;animals.push(a);state.wildlifeReturns.splice(i,1);
 }
}

for(let i=0;i<290;i++){
  const x=(3+rand()*(W-6))*TILE,y=(3+rand()*(H-6))*TILE;
  if(Math.hypot(x-base.x,y-base.y)<150||Math.hypot(x-cave.x,y-cave.y)<110||Math.hypot(x-meteor.x,y-meteor.y)<100||lakeWater(x,y))continue;
  // Keep the original forest layout so version 0.1 saved resource IDs still match.
  const type=rand()<.60?'wood':rand()<.48?'stone':rand()<.7?'berries':'herbs';
  if(water(x,y))continue;
  resources.push({id:i,x,y,type:biomeAt(x,y)==='desert'&&type==='wood'?'cactus':type,hp:3,alive:!state.depleted?.includes(i),removed:state.stumpsRemoved.includes(i)});
}
for(const [id,x,y,type]of[[500,-95,60,'wood'],[501,98,45,'stone'],[502,-65,110,'berries'],[503,130,-35,'wood'],[504,-120,-45,'stone'],[505,65,150,'herbs']])resources.push({id,x:base.x+x,y:base.y+y,type,hp:3,alive:!state.depleted?.includes(id),removed:state.stumpsRemoved.includes(id)});
for(let i=0;i<14;i++){
  let x,y;
  do{x=(12+rand()*38)*TILE;y=(12+rand()*25)*TILE;}while(water(x,y)||water(x-8,y)||water(x+8,y)||water(x,y-6)||water(x,y+6));
  animals.push({x,y,type:i%3?'rabbit':'deer',dir:rand()*6.28,timer:rand()*3,step:rand()*6,hp:i%3?1:3});
}
for(const[type,x,y]of[['wolf',24,22],['wolf',40,32],['bear',39,12],['skeleton',49,12],['skeleton',52,8]])animals.push({type,x:x*TILE,y:y*TILE,homeX:x*TILE,homeY:y*TILE,hp:type==='bear'?7:4,dir:0,timer:1,step:0});
for(const a of animals){a.homeX??=a.x;a.homeY??=a.y;}
const initialWildlife=animals.map(a=>({...a}));
if(Array.isArray(state.wildlife)){animals.length=0;for(const a of state.wildlife){if(Number.isFinite(a.x)&&Number.isFinite(a.y)&&['rabbit','deer','wolf','bear','skeleton'].includes(a.type)&&!water(a.x,a.y))animals.push({...a});}}
if(saveVersion<4&&Array.isArray(state.wildlife))for(const a of initialWildlife.filter(a=>['wolf','bear','skeleton'].includes(a.type)))animals.push({...a});
for(let i=0;i<3;i++)bats.push({x:(29+i*2)*TILE,y:(21+i%3)*TILE,hp:1,phase:rand()*6.28,hit:0});
for(const [id,x,y,type]of[[600,29,22,'ironOre'],[601,35,23,'copperOre'],[602,28,26,'ironOre'],[603,36,27,'copperOre'],[604,28,19,'stone']])resources.push({id,x:x*TILE,y:y*TILE,type,hp:3,inCave:true,alive:!state.depleted?.includes(id)});
for(const r of looseResources())resources.push({...r,alive:!state.depleted?.includes(r.id)&&!state.buildings.some(b=>Math.hypot((b.x+.5)*32-r.x,(b.y+.5)*32-r.y)<30)});
if(state.alienFriend&&!state.alien)state.alien={x:state.player.x+35,y:state.player.y+25,inCave:state.inCave};
function notify(text){$('toast').textContent=tr(text);$('toast').classList.remove('hidden');toastTime=4;}
function save(){try{state.wildlife=animals.map(a=>({...a}));state.depleted=resources.filter(r=>!r.alive).map(r=>r.id);state.stumpsRemoved=resources.filter(r=>r.removed).map(r=>r.id);localStorage.setItem('simm-save-v1',JSON.stringify({version:4,state}));}catch{}}
function start(){if(!assetsReady)return;recoverShorePosition();started=true;if(state.time>=300)spawnZombies();$('startOverlay').classList.add('hidden');canvas.focus();notify(saveFound?tr('Tere tagasi, Simm!'):tr('Metsakristall ootab põhja pool. A / E suhtleb või hüppab. View / I avab menüü.'));refresh();}
$('startButton').onclick=start;$('newGameButton').onclick=()=>saveFound?openModal('newgame'):startNewGame();$('pauseButton').onclick=()=>openModal('pause');
if(saveFound){$('startButton').textContent=tr('Jätka seiklust →');document.querySelector('.intro-card p').textContent=tr('Sinu mets, varud ja ehitised on alles. Versioon 0.4.3 ootab uut seiklust.');}
$('audioButton').onclick=async()=>{try{const enabled=await toggleAudio();setVolume(Number($('volume').value)/100);$('audioButton').textContent=enabled?tr('♫ Heli sees'):tr('♫ Heli väljas');$('audioButton').setAttribute('aria-pressed',String(enabled));}catch{notify(tr('Brauser ei saanud heli käivitada.'));}};
$('volume').oninput=()=>setVolume(Number($('volume').value)/100);
$('fullscreenButton').onclick=async()=>{try{if(document.fullscreenElement)await document.exitFullscreen();else await document.documentElement.requestFullscreen();}catch{notify(tr('Kasuta brauseri täisekraani klahvi F11.'));}};
$('journalButton').onclick=openMain;$('helpButton').onclick=()=>openModal('help');$('skillsButton').onclick=openMain;$('craftButton').onclick=openMain;$('buildButton').onclick=()=>openModal('build');$('bagButton').onclick=openMain;$('eatButton').onclick=eat;
function closeModal(){if(menuKind)menuSelections[menuKind]={key:menuCache[menuIndex]?.dataset.key,scroll:$('modalContent').scrollTop};if($('modal').open)$('modal').close();paused=false;menuKind=null;menuCache=[];menuDirection=null;canvas.focus({preventScroll:true});}
$('closeModal').onclick=closeModal;$('modal').addEventListener('cancel',e=>{e.preventDefault();closeModal();});
$('modal').addEventListener('click',e=>{if(e.target===$('modal')){const r=$('modal').getBoundingClientRect();if(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom)closeModal();}});
function uiGlyph(id){
 const colors={gold:'#e8ce87',mint:'#a3cab0',wood:'#bd9759',steel:'#bdcfbf',dark:'#324b36'};
 const paths={
  wood:'<path d="M15 15h36v13H15zM10 36h36v13H10z" fill="wood"/><ellipse cx="15" cy="22" rx="8" ry="7" fill="gold"/><ellipse cx="10" cy="43" rx="8" ry="7" fill="gold"/><ellipse cx="15" cy="22" rx="4" ry="3" fill="wood"/><ellipse cx="10" cy="43" rx="4" ry="3" fill="wood"/>',
  hand:'<path d="M21 52V31c0-5 6-5 6 0V16c0-5 6-5 6 0v15-18c0-5 6-5 6 0v19-14c0-5 6-5 6 0v19l5-5c5-4 9 1 5 6L43 55H25z" fill="gold"/>',
  axe:'<path d="M18 55L39 10" stroke="wood" stroke-width="7"/><path d="M29 12l14-6 14 9-7 13-19-6z" fill="steel"/><path d="M46 8l11 7-7 13" fill="mint"/>',
  pickaxe:'<path d="M17 55L39 15" stroke="wood" stroke-width="7"/><path d="M9 24Q34-7 57 17L36 13z" fill="steel"/>',
  bow:'<path d="M17 8Q61 31 17 56" fill="none" stroke="wood" stroke-width="6"/><path d="M17 8L25 32 17 56M9 32h46" fill="none" stroke="gold" stroke-width="2"/><path d="M48 28l8 4-8 4" fill="steel"/>',
  torch:'<path d="M27 38h10l-2 20h-6z" fill="wood"/><path d="M31 5c-9 13-20 20-13 31 8 15 28 11 31-3 3-11-8-18-10-25 0 12-7 14-8-3z" fill="gold"/><path d="M32 20c-6 7-10 11-6 18 4 7 13 4 13-3 0-6-4-9-7-15z" fill="#f2edb5"/>',
  rod:'<path d="M13 57L34 8Q43 11 51 23" fill="none" stroke="wood" stroke-width="4"/><path d="M51 23v24q0 10-8 7" fill="none" stroke="mint" stroke-width="2"/><circle cx="51" cy="31" r="3" fill="gold"/>',
  combat:'<path d="M14 10l35 36-6 7-35-36zM50 10L15 46l6 7 35-36z" fill="steel"/><path d="M10 40l14 14M40 54l14-14" stroke="gold" stroke-width="5"/><path d="M9 55l7-8M48 47l7 8" stroke="wood" stroke-width="6"/>',
  craft:'<path d="M17 56L38 20" stroke="wood" stroke-width="7"/><path d="M24 13l19-8 14 13-7 10-24-8z" fill="steel"/><path d="M9 10l29 44" stroke="gold" stroke-width="4"/>',
  gather:'<path d="M13 55Q19 12 55 8C59 39 34 55 13 55z" fill="gold"/><path d="M13 55l33-37M27 40l-3-11M36 30l13 1" stroke="dark" stroke-width="2" fill="none"/>',
  star:'<path d="M32 5l8 18 19 9-19 8-8 19-8-19-19-8 19-9z" fill="gold"/><circle cx="32" cy="32" r="5" fill="#f4ecd1"/>',
  guardian:'<path d="M32 55C-8 30 12 0 32 18 52 0 72 30 32 55z" fill="gold"/>',
  mason:'<path d="M6 44l27 11 25-14-27-9zM6 31l27 11 25-14-27-9zM6 18l27 11 25-14L31 6z" fill="steel" stroke="dark" stroke-width="2"/>',
  frost:'<path d="M32 6v52M9 19l46 26M9 45l46-26M24 11l8 8 8-8M24 53l8-8 8 8M11 27l11-3-1-11M43 51l-1-12 11-3M11 37l11 3-1 11M43 13l-1 12 11 3" stroke="mint" stroke-width="3" fill="none"/>',
  helper:'<ellipse cx="32" cy="37" rx="27" ry="10" fill="steel"/><path d="M16 34c0-23 32-23 32 0z" fill="mint"/><path d="M20 51l-4 7M32 51v9M44 51l4 7" stroke="gold" stroke-width="3"/><circle cx="15" cy="36" r="2" fill="gold"/><circle cx="32" cy="38" r="2" fill="gold"/><circle cx="49" cy="36" r="2" fill="gold"/>'
 };
 const aliases={quickdraw:'bow',logger:'axe',smelter:'torch',angler:'rod',ironAxe:'axe',copperPickaxe:'pickaxe'};
 const p=paths[aliases[id]||id];if(!p)return null;
 return `<svg class="ui-glyph" viewBox="0 0 64 64" aria-hidden="true" xmlns="http://www.w3.org/2000/svg">${p.replace(/gold|mint|wood|steel|dark/g,k=>colors[k])}</svg>`;
}

function menuButtons(){return menuCache;}
function cacheMenu(){
  menuCache=[...$('modalContent').querySelectorAll('button[data-nav],button:not(:disabled)')].filter(b=>!b.closest('.hidden'));
  for(const button of menuCache){button.addEventListener('pointermove',e=>{const i=menuCache.indexOf(button);if((e.movementX||e.movementY)&&i>=0&&i!==menuIndex)focusMenu(i,false);});}
}
function focusMenu(index,scroll=true){
  if(!menuCache.length){$('closeModal').focus({preventScroll:true});return;}
  const previous=menuCache[menuIndex];previous?.classList.remove('pad-focused');
  menuIndex=Math.max(0,Math.min(menuCache.length-1,index));const button=menuCache[menuIndex];
  button.classList.add('pad-focused');button.focus({preventScroll:true});
  // Only scroll the content container, and only when the selected card is actually outside it.
  if(scroll){const box=button.getBoundingClientRect(),container=$('modalContent'),bounds=container.getBoundingClientRect();if(box.top<bounds.top+8)container.scrollTop-=bounds.top-box.top+12;else if(box.bottom>bounds.bottom-8)container.scrollTop+=box.bottom-bounds.bottom+12;}
  updateMenuDetail(button);
}
function moveMenu(dx,dy){
  if(!menuCache.length)return;
  const current=menuCache[menuIndex],a=current.getBoundingClientRect();let best=-1,score=Infinity;
  if(menuKind==='skills'&&dy){
    const node=skills.find(s=>s.id===current.dataset.skill);let target=null;
    if(dy>0&&!node?.requires)target=skills.find(s=>s.requires===node?.id)?.id;
    else if(node?.requires){const siblings=menuCache.filter(b=>{const n=skills.find(s=>s.id===b.dataset.skill),r=b.getBoundingClientRect();return n?.requires===node.requires&&dy*(r.top-a.top)>8;});siblings.sort((l,r)=>{const score=b=>{const z=b.getBoundingClientRect();return Math.abs(z.left-a.left)*3+Math.abs(z.top-a.top);};return score(l)-score(r);});target=siblings[0]?.dataset.skill||(dy<0?node.requires:null);}
    const i=menuCache.findIndex(b=>b.dataset.skill===target);if(i>=0)focusMenu(i);return;
  }
  for(let i=0;i<menuCache.length;i++){
    if(i===menuIndex)continue;const b=menuCache[i].getBoundingClientRect(),vx=(b.left+b.width/2)-(a.left+a.width/2),vy=(b.top+b.height/2)-(a.top+a.height/2);
    const forward=dx*vx+dy*vy,side=Math.abs(dx?vy:vx);if(forward<=2)continue;
    const value=forward+side*2.8;if(value<score){best=i;score=value;}
  }
  if(best>=0)focusMenu(best);
}
function activateMenu(){const button=menuCache[menuIndex];if(!button&&document.activeElement===$('closeModal')){closeModal();return;}if(button?.dataset.skill){selectedSkill=button.dataset.skill;learnSelectedSkill();}else if(button&&!button.disabled)button.click();}
function updateMenuDetail(button){
  if(!button?.dataset.skill)return;
  const s=skills.find(s=>s.id===button.dataset.skill),rank=state.skills[s.id]||0;
  selectedSkill=s.id;
  const available=canUpgrade(state,s.id),locked=s.requires&&!state.skills[s.requires];
  $('modalDetail').innerHTML=tr`<span class="detail-icon">${uiGlyph(s.id)||s.icon}</span><div class="eyebrow">${{combat:tr('VÕITLUS'),craft:tr('MEISTERDAMINE'),gather:tr('KORJAMINE'),star:tr('TÄHELEIUTAMINE')}[s.branch]}</div><h3>${s.name}</h3><p>${s.description}</p><div class="rank-meter">${Array.from({length:s.max},(_,i)=>`<i class="${i<rank?'filled':''}"></i>`).join('')}</div><strong>Aste ${rank} / ${s.max}</strong><p class="unlock-copy">${locked?tr('Kõigepealt õpi: ')+skills.find(n=>n.id===s.requires).name:rank>=s.max?tr('See oskus on täielikult õpitud.'):!state.points?tr('Järgmise tasemega teenid uue oskuspunkti.'):tr('Sul on ')+state.points+tr(' oskuspunkti. Õpi, et oma seiklust muuta.')}</p><button id="learnSkillButton" class="primary" ${!available?'disabled':''}>${locked?tr('Esmalt põhioskus'):rank>=s.max?tr('Õpitud'):!state.points?tr('Vajad oskuspunkti'):tr('A / Enter · Õpi (1 punkt)')}</button>`;
  $('learnSkillButton').onclick=learnSelectedSkill;
}
function learnSelectedSkill(){if(!selectedSkill)return;if(upgrade(state,selectedSkill)){const keep=selectedSkill;sound('craft');refresh();save();openModal('skills');const i=menuCache.findIndex(b=>b.dataset.skill===keep);focusMenu(Math.max(0,i));notify(tr('Õppisid uue oskuse!'));}else sound('swing');}
function startNewGame(){
  if(!assetsReady)return;
  for(const k of Object.keys(state))delete state[k];Object.assign(state,freshState());state.player={x:base.x,y:base.y+64,face:1,walk:0};
  for(const r of resources){r.alive=true;r.removed=false;r.hp=3;}
  animals.splice(0,animals.length,...initialWildlife.map(a=>({...a})));zombies.length=0;arrows.length=0;particles.length=0;
  bats.forEach((b,i)=>Object.assign(b,{x:(29+i*2)*TILE,y:(21+i%3)*TILE,hp:1,hit:0}));
  tool=0;buildType=null;buildCursor=null;targetLock=null;pickups.length=0;chestOpen=null;gardenOpen=null;npcOpen=null;whaleGame=null;whaleHeld=false;worldTick=0;for(const key of Object.keys(menuSelections))delete menuSelections[key];charge=null;death=null;fishing=null;meteorFall=null;invulnerable=0;damageFlash=0;autosave=0;aim={x:1,y:0};canvas._pointer=null;saveFound=false;
  $('deathOverlay').classList.add('hidden');closeModal();save();start();notify(tr('Uus seiklus algab. Tere tulemast Rohelaande, Simm!'));
}
function refresh(){
  const hotbar=$('hotbar');hotbar.replaceChildren();
  tools.forEach((t,i)=>{const b=document.createElement('button');b.className='tool-slot'+(tool===i?' active':'')+(!state.tools.includes(t.id)?' locked':'');b.title=t.name;b.setAttribute('aria-label',t.name);b.setAttribute('aria-pressed',String(tool===i));b.innerHTML=`<kbd>${i+1}</kbd>${uiGlyph(t.id)||t.icon}`;b.onclick=()=>selectTool(i);hotbar.append(b);});
  paintMenuArt();$('bagCount').textContent=`${usedSlots(state)}/${state.bagSlots}`;
  $('pointsLabel').textContent=tr`${state.points} OSKUSPUNKTI`;
  $('skillsButton').classList.toggle('has-points',state.points>0);
  $('skillSubtitle').textContent=tr`Tase ${state.level} · I / View`;
  $('questText').textContent=(questSteps(state).find(q=>!q.done)?.title||tr('Sinu seiklus jätkub'))+tr(' · Seikluspäevik ↑');
}
function costFor(r){return Object.fromEntries(Object.entries(r.cost).map(([k,v])=>[k,Math.max(1,Math.ceil(v*(1-.1*(state.skills.craft||0))))]));}
function nearBench(){return isOutside()&&Math.hypot(state.player.x-(base.x+35),state.player.y-base.y)<46;}
function nearStation(type){return !state.inCave&&worldItems().find(b=>b.type===type&&Math.hypot(state.player.x-(b.x+.5)*TILE,state.player.y-(b.y+.5)*TILE)<48);}
function nearFire(){return nearStation('fire');}
function openModal(kind){
  if(death)return;if(menuKind)menuSelections[menuKind]={key:menuCache[menuIndex]?.dataset.key,scroll:$('modalContent').scrollTop};const previousKey=menuSelections[kind]?.key;
  charge=null;fishing=null;paused=true;keys={};
  const modal=$('modal'),content=$('modalContent');menuKind=kind;menuDirection=null;menuRepeatAt=0;modal.dataset.kind=kind;drawTabs();modal.classList.toggle('wide',kind==='skills');$('modalDetail').classList.toggle('hidden',kind!=='skills');content.replaceChildren();
  $('modalEyebrow').textContent={language:tr('Keele valik'),skills:tr`TASE ${state.level}`,craft:tr('MEISTERDAMISLAUD'),build:tr('OMA KODU, OMA REEGLID'),bag:tr('KÕIK VAJALIK KAASAS'),fire:tr('LÕKKE ÄÄRES'),furnace:tr('MAAGIST METALLIKS'),help:tr('VÄIKE SPIKKER'),pause:tr('VÕTA HETK ENDALE'),newgame:tr('UUS ALGUS'),journal:tr('IGA SAMM LOEB'),map:tr('SUUR MAAILM'),chest:tr('IGA ASI OMA KOHALE'),garden:tr('KASVAB ILMA KASTMATA'),npc:tr('SÕBRAD JA ÜLESANDED'),whale:tr('MERESÕBRA MÄNG')}[kind];
  $('modalTitle').textContent={language:tr('Vali mängu keel'),skills:tr('Vali oma rada'),craft:tr('Valmista midagi head'),build:tr('Ehita oma kodu'),bag:tr('Sinu seljakott'),fire:tr('Soe tuli, hea toit'),furnace:tr('Sulatusahi'),help:tr('Seiklus algab siit'),pause:tr('Seiklus ootab sind'),newgame:tr('Alustame uut seiklust?'),journal:tr('Sinu seikluse lugu'),map:tr('Sinu maailm'),chest:tr('Hoiukast'),garden:tr('Sinu kastpeenar'),npc:npcOpen?.name,whale:tr('Sõbralik vaalapüük')}[kind];
  if(kind==='language'){content.innerHTML=tr('<p class="build-note">Tekstid ja subtiitrid kasutavad valitud keelt. Tulevane räägitud dialoog on inglise keeles.</p><button class="storage-row" data-language="en">English</button><button class="storage-row" data-language="et">Eesti</button>');content.querySelectorAll('[data-language]').forEach(b=>{b.setAttribute('aria-pressed',String(b.dataset.language===getLanguage()));b.onclick=()=>changeLanguage(b.dataset.language);});}else if(extraMenu(kind,content)){}else if(kind==='journal'){const steps=questSteps(state),active=steps.findIndex(q=>!q.done);content.innerHTML='<div class="journal-list">'+steps.map((q,i)=>`<article class="journal-step ${q.done?'complete':''} ${i===active?'active':''}"><span>${q.done?'✓':String(i+1).padStart(2,'0')}</span><div><h3>${q.title}</h3><p>${q.text}</p></div>${i===active?tr('<small>SINU JÄRGMINE SAMM</small>'):''}</article>`).join('')+'</div>'+npcData.map(n=>`<article class="journal-step"><span>${state.npcQuests[n.id]?'✓':'!'}</span><div><h3>${n.name}</h3><p>${n.task} ${state.npcQuests[n.id]?tr('TEHTUD!'):''}</p></div></article>`).join('');
  }else if(kind==='pause'){content.innerHTML=tr('<div class="pause-grid"><button id="resumeGame" class="primary">Jätka seiklust</button><button id="pauseSkills">✦ Minu oskused</button><button id="pauseHelp">? Kuidas mängida</button><button id="pauseNew">Uus mäng</button><button id="pauseJournal">⚑ Seikluspäevik</button><button id="pauseLanguage">English / Eesti</button></div><p class="build-note">Mäng on pausil ja sinu seiklus salvestatud.</p>');save();$('resumeGame').onclick=closeModal;$('pauseSkills').onclick=()=>openModal('skills');$('pauseHelp').onclick=()=>openModal('help');$('pauseNew').onclick=()=>openModal('newgame');$('pauseJournal').onclick=()=>openModal('journal');$('pauseLanguage').onclick=()=>openModal('language');
  }else if(kind==='newgame'){content.innerHTML=tr('<div class="newgame-confirm"><span>✧</span><h3>Üks mets. Tuhat uut võimalust.</h3><p>Alustad esimesest päevast tühja seljakotiga. Praegune seiklus asendatakse uuega.</p><div class="pause-grid"><button id="cancelNewGame">Jäta praegune seiklus alles</button><button id="confirmNewGame" class="primary">Jah, alusta uut mängu</button></div></div>');$('cancelNewGame').onclick=closeModal;$('confirmNewGame').onclick=startNewGame;
  }else if(kind==='bag'){
    content.innerHTML=tr`<p class="build-note">${usedSlots(state)} / ${state.bagSlots} pesa · Virnas kuni ${STACK_SIZE} eset. Vali ese, et üks maha panna. Ese püsib 10 mänguminutit ja selle saab A / E-ga uuesti üles korjata.</p>`;
    const grid=document.createElement('div');grid.className='bag-grid';
    for(const[k,v]of Object.entries(state.inventory))for(let n=v;n>0;n-=STACK_SIZE){const slot=document.createElement('button');slot.className='inv-slot';slot.title=`${names[k]} · ${['water','healPotion','speedPotion','peacePotion'].includes(k)?tr('kasuta'):tr('pane üks maha')}`;slot.setAttribute('aria-label',`${['water','healPotion','speedPotion','peacePotion'].includes(k)?tr('Kasuta'):tr('Pane maha')}: ${names[k]}`);slot.dataset.key=k;slot.innerHTML=`${menuArt(k,icons[k])}<span class="slot-name">${names[k]}</span><small>${Math.min(n,STACK_SIZE)}</small>`;slot.onclick=()=>{if(['water','healPotion','speedPotion','peacePotion'].includes(k)){useBagItem(k);return;}dropItem(state,k,state.player.x+aim.x*20,state.player.y+aim.y*20,state.inCave);refresh();save();openModal('bag');};grid.append(slot);}
    while(grid.children.length<state.bagSlots){const d=document.createElement('div');d.className='inv-slot empty';grid.append(d);}content.append(grid);
  }else if(kind==='skills'){
    content.innerHTML=tr`<div class="skill-points">✦ <strong>${state.points}</strong> oskuspunkti <span>Vali rada. Vaata võimalusi. Kasva omas tempos.</span></div>`;
    const tree=document.createElement('div');tree.className='skill-tree';
    for(const branch of ['combat','craft','gather','star']){
      const column=document.createElement('div');column.className='skill-branch';column.dataset.branch=branch;
      const label=document.createElement('h3');label.className='branch-label';label.textContent={combat:tr('Vapper seikleja'),craft:tr('Nutikas meister'),gather:tr('Metsa sõber'),star:tr('Täheleiutaja')}[branch];column.append(label);
      const children=document.createElement('div');children.className='tree-children';
      for(const s of skills.filter(s=>s.branch===branch)){
        const rank=state.skills[s.id]||0,locked=s.requires&&!state.skills[s.requires],card=document.createElement('div');
        card.className='skill-node'+(rank?' owned':'')+(canUpgrade(state,s.id)?' available':'')+(locked?' locked':'');
        const button=document.createElement('button');button.dataset.skill=s.id;button.dataset.key=s.id;button.dataset.nav='true';button.setAttribute('aria-label',s.name);button.innerHTML=`<span class="node-icon">${uiGlyph(s.id)||s.icon}</span><strong>${s.name}</strong><span class="node-rank">${rank}/${s.max} ${locked?'· 🔒':rank>=s.max?'· ✓':canUpgrade(state,s.id)?'· +':''}</span>`;
        button.onclick=()=>{focusMenu(menuCache.indexOf(button),false);};button.ondblclick=learnSelectedSkill;
        card.append(button);if(s.requires)children.append(card);else column.append(card);
      }column.append(children);tree.append(column);
    }content.append(tree);
  }else if(kind==='help'){
    content.innerHTML=tr`<div class="help-copy"><p><strong>Liikumine:</strong> WASD / vasak kang. A / E suhtleb lähedal oleva esemega, mujal hüppab. F hüppab alati. Z/V või D-pad vasak/parem pöörab kaamerat. Hüppa liikudes ühe astme peale; Kõrge hüpe oskus lubab kõrgemale.</p><p><strong>Menüü:</strong> I / View avab SELJAKOTI, Y avab EHITAMISE. LB/RB või [ / ] / Tab vahetab vahelehti. Vali vasaku kangi või nooltega, A / Enter kinnitab, B / Esc sulgeb. Parem kang kerib. Seljakotis vali jook või vesi kasutamiseks; muud esemed saab maha panna.</p><p><strong>Materjalid:</strong> korja A / E-ga maast harvu oksi ja väikseid kive. Oks annab ühe puidu, väike kivi ühe kivi. Maitsetaimest saad menüüs käsitsi kolm taimekiudu. Kivikirka vajab 3 puitu, 3 kivi ja 1 kiudu. Kõrbest korjatud liiv sulab ahjus klaasiks. Akendel ja tavalistel lampidel on klaasist osad.</p><p><strong>Tööriistad:</strong> RT / tühik / hiir kasutab tööriista. Vibu laeb hoides ning laseb vabastades. LB/RB valib tööriista. LT / R sööb. Ehitades valib parem kang või ristnupud ruudu, A / RT paigaldab, X / Q pöörab ja B lõpetab. Mujal juhib B / T Nupsi. Menu / Esc avab pausi.</p><p><strong>Kodu:</strong> ehita vähemalt 3×3 põrand. Pane igale servaruudule sein, aken või uks ning igale põrandaruudule katus. Aknad asendavad seina ja on vabatahtlikud. Valmis majja sisene ukse juures A-ga. Sees on 8×6 ehitusala. Täida see vahelagedega ja lisa trepp, et avada järgmine korrus. Trepi juures A viib üles, välisukse juures A alla või õue.</p><p><strong>Kast ja peenar:</strong> ehita ning ava A-ga. Kastimenüüs saad valida ühe eseme seljakotist kasti või kastist seljakotti. Meisterdamine kasutab kuni 120 sammu kaugusel sama ruumi ja korruse kaste. Peenras vali taim: seemnevaru on olemas, kasta pole vaja. Küpse saagi korjad A-ga.</p><p><strong>Kõrb ja meri:</strong> kirdeosas on kuum kõrb, kaktused, varemed ja oaas. Võta kaasa joogivett. Idarannas ehita paat vette, istu A-ga sisse ning aeruta merele. Vaal ootab ida pool. Stiliseeritud harpuun käivitab püügimängu: hoia RT / tühikut, et tõsta märki; vabastades märk langeb. Hoia märki kuldses alas. Pärast püüki saad vaala vabastada.</p><p><strong>Seiklus:</strong> metsavaht, kaevur ja kaupmees annavad ülesandeid. Hundist jookse kaugele, karu juurest lahku pesast eemale. Loomasõbra jook kaitseb loomade eest 120 sekundit, kiirusejook kestab 90 sekundit. Lambid põlevad püsivalt. Puud taastuvad kolme päevaga, taimed ühe ja loomad kahe päevaga; ehitised takistavad taastumist.</p></div>`;
  }else if(kind==='fire'||kind==='furnace'){
    const station=nearStation(kind);
    if(!station){content.innerHTML=tr('<p class="build-note">Mine jaama kõrvale, et seda kasutada.</p>');}
    else{
      content.innerHTML=tr`<div class="station-fuel"><p class="build-note">Kütust: ${Math.ceil(station.fuel||0)} sekundit · 1 puit = ${state.skills.smelter?4:2} minutit.</p><button id="fuelButton" ${availableInventory(state).wood<1?'disabled':''}>Lisa 1 puit · süüta tuli</button></div>`;
      $('fuelButton').dataset.key='fuel';$('fuelButton').onclick=()=>{if(payNearby(state,{wood:1})){station.fuel=(station.fuel||0)+120*(state.skills.smelter?2:1);refresh();save();openModal(kind);}};
      for(const r of recipes.filter(r=>kind==='fire'?r.cook:r.smelt)){
        const row=recipeRow(r,r.cost,!(station.fuel>0)||!canPayLocal(r.cost),kind==='fire'?tr('Küpseta'):tr('Sulata'));
        row.querySelector('button').onclick=()=>{if(station.fuel>0&&craftItem(state,r)){station.fuel=Math.max(0,station.fuel-5);gainXP(state,8);sound('craft');refresh();save();openModal(kind);notify(tr`${r.name} valmis!`);}else notify(tr('Seljakott on täis. Tee ruumi või kasuta hoiukasti.'));};content.append(row);
      }
    }
  }else if(kind==='craft'&&!nearBench()){
    content.innerHTML=tr('<p class="build-note">Mine meisterdamislaua kõrvale tööriistade ja võlujookide jaoks. Käsitsi saad teha taimekiudu; veekogu kaldal võtta joogivett.</p>');
    for(const r of recipes.filter(r=>r.hand)){const cost=costFor(r),row=recipeRow(r,cost,!canPayLocal(cost)||r.water&&!shorePoint(),r.water?tr('Täida'):tr('Valmista'));row.querySelector('button').onclick=()=>{if((!r.water||shorePoint())&&craftItem(state,r,cost)){refresh();save();openModal('craft');}else notify(tr('Vajad materjale, vaba seljakotiruumi või joogivee jaoks veekogu lähedust.'));};content.append(row);}
  }
  else{
    if(kind==='build')content.innerHTML=tr('<p class="build-note">Vali osa. Pult: parem kang või ristnupud valivad ruudu, vasak kang liigutab Simmi, A paigaldab ja B lõpetab. Hiirega sihi maapinda: roheline eelvaade lubab ehitada, punane näitab takistust. Q / X pöörab seina. A / klõps paigutab. Seinad ühenduvad automaatselt; suletud tuba koos uksega kaitseb öösel.</p>');
    for(const r of recipes.filter(r=>!r.cook&&!r.smelt&&(kind==='build')===!!r.build)){
      const cost=costFor(r),owned=r.gear?!!state.gear?.[r.gear]:r.upgrade?state.bagSlots>=40:!r.build&&state.tools.includes(r.id);
      const row=recipeRow(r,cost,owned||!canPayLocal(cost)||r.gear&&!state.tools.includes(r.gear)||r.water&&!shorePoint(),owned?tr('Olemas'):r.build?tr('Vali'):tr('Valmista'));
      row.querySelector('button').onclick=()=>{
        if(r.build){buildType=r.id;rotation='auto';buildCursor=null;buildDirection=null;closeModal();if(inputMode==='pad')ensureBuildCursor();notify(tr`${r.name} · A / E paigutab · parem kang / ristnupud valivad ruudu · X pöörab · B lõpetab`);}
        else if(r.item){if(r.water&&!shorePoint()){notify(tr('Vee võtmiseks mine veekogu kaldale.'));return;}if(craftItem(state,r,cost)){gainXP(state,8);refresh();save();openModal('craft');}else notify(tr('Seljakott on täis. Tee ruumi või kasuta hoiukasti.'));}else if(payNearby(state,cost)){if(r.gear){state.gear=state.gear||{};state.gear[r.gear]=true;}else if(r.upgrade)state.bagSlots+=5;else state.tools.push(r.id);gainXP(state,12);sound('craft');refresh();save();openModal('craft');}
      };content.append(row);
    }
  }
  if(!modal.open)modal.showModal();
  cacheMenu();$('modalContent').scrollTop=menuSelections[kind]?.scroll||0;const keep=previousKey?menuCache.findIndex(b=>b.dataset.key===previousKey):-1;focusMenu(keep>=0?keep:0,!['help','journal'].includes(kind));paintMenuArt();document.querySelector('.modal-hint').textContent=kind==='skills'?tr('Vasak kang / ristnupud: vali · A: õpi · LB/RB: vaheleht · B: tagasi'):['help','journal'].includes(kind)?tr('Parem kang / hiireratas: keri · B: tagasi'):mainTabs.includes(kind)?tr('LB/RB või [ / ]: vaheleht · A: kinnita · B: tagasi'):tr('Vasak kang / ristnupud: vali · A: kinnita · B: tagasi');
}
function recipeRow(r,cost,disabled,label){const row=document.createElement('div');row.className='recipe';row.innerHTML=`<span>${menuArt(r.id,r.icon)}</span><div><strong>${r.name}${r.quantity>1?` ×${r.quantity}`:''}</strong><p>${Object.entries(cost).map(([k,v])=>tr`${names[k]} ${v} <small class="material-count ${availableInventory(state)[k]>=v?'enough':'missing'}">(${availableInventory(state)[k]||0} olemas)</small>`).join(' · ')||tr('Veekogu ääres · korduvkasutatav veepudel')}</p></div><button ${disabled?'disabled':''}>${label}</button>`;row.querySelector('button').dataset.key=r.id;const missing=missingMaterials(cost);if(missing){const note=document.createElement('p');note.className='recipe-missing';note.textContent=tr`Puudu: ${missing}`;row.children[1].append(note);}return row;}
function selectTool(i){if(state.tools.includes(tools[i]?.id)){charge=null;fishing=null;tool=i;refresh();}else notify(tr('Meisterda kõigepealt see tööriist.'));}
function cycleTool(d){for(let i=0;i<tools.length;i++){const next=(tool+d+tools.length)%tools.length;tool=next;if(state.tools.includes(tools[tool].id))break;}charge=null;refresh();}
function burst(x,y,color,count=8){for(let i=0;i<count;i++)particles.push({x,y,vx:(Math.random()-.5)*85,vy:-20-Math.random()*45,life:.7,color});}
function showPickup(id,n,x=state.player.x,y=state.player.y){pickups.push({id,n,x,y,life:1.5});}
function addOrDrop(id,n,x=state.player.x,y=state.player.y){const added=addItem(state,id,n);if(added)showPickup(id,n,x,y);if(!added){state.drops.push({id,amount:n,x,y,inCave:state.inCave,room:state.interior?.id||null,level:state.interior?.level||0,expires:state.worldAge+600});notify(tr`${names[id]} jäi maha — seljakott on täis.`);}refresh();return added;}
function collect(r){
  if(forageDefs[r.type]){if(gatherLoose(state,r)){showPickup(forageDefs[r.type].item,forageDefs[r.type].quantity,r.x,r.y);sound(r.type==='branch'?'wood':'stone');burst(r.x,r.y,'#e1d0a0',4);notify('+'+forageDefs[r.type].quantity+' '+names[forageDefs[r.type].item].toLowerCase());refresh();save();}else notify(tr('Seljakott on täis. Tee ruumi või kasuta hoiukasti.'));return;}
  const selected=tools[tool].id,stump=!r.alive&&r.type==='wood'&&!r.removed;
  if((r.type==='wood'&&selected!=='axe')||(['stone','ironOre','copperOre'].includes(r.type)&&selected!=='pickaxe')){notify(r.type==='wood'?tr('Vali kirves.'):tr('Vali kirka.'));return;}
  if(stump){r.removed=true;addOrDrop('wood',state.skills.logger?3:2,r.x,r.y);sound('wood');burst(r.x,r.y,'#bd9864');gainXP(state,4);save();return;}
  r.hp-=['berries','herbs','cactus'].includes(r.type)?3:1+(state.skills.gather||0)+(r.type==='wood'&&state.gear?.axe?1:0)+(['stone','ironOre','copperOre'].includes(r.type)&&state.gear?.pickaxe?1:0);sound(r.type==='wood'?'wood':r.type==='berries'?'berries':'stone');burst(r.x,r.y,r.type==='wood'?'#c7a36b':'#afbda3');
  if(r.hp<=0){r.alive=false;state.regrowth[r.id]=state.worldAge+(r.type==='wood'?1080:360);const n=(r.type==='wood'?5:r.type==='stone'?4:3)+(state.skills.gather||0)+(r.type==='wood'&&state.skills.logger?2:0);const added=addOrDrop(r.type==='cactus'?'water':r.type,n,r.x,r.y);state.gathered[r.type]=(state.gathered[r.type]||0)+n;const level=state.level;gainXP(state,10);if(added)notify(`+${n} ${names[r.type==='cactus'?'water':r.type].toLowerCase()}${state.level>level?tr(' · Uus oskuspunkt!'):''}`);refresh();save();}
}
function chooseTarget(candidates){
 if(!candidates.length){targetLock=null;return;}
 const p=state.player,hasInteraction=candidates.some(c=>!['resource','drop'].includes(c.kind)),score=c=>{const n=c.d||1,dot=((c.x-p.x)*aim.x+(c.y-p.y)*aim.y)/n;const resource=c.kind==='resource'?c.ref:null,selected=tools[tool].id,toolMatch=resource&&(selected==='axe'&&resource.type==='wood'||selected==='pickaxe'&&['stone','ironOre','copperOre'].includes(resource.type));return c.d-dot*4-(toolMatch&&!hasInteraction?18:0)+(resource&&hasInteraction?8:0);};
 candidates.sort((a,b)=>score(a)-score(b));const best=candidates[0],held=candidates.find(c=>c.kind===targetLock?.kind&&c.ref===targetLock?.ref&&c.x===targetLock?.x&&c.y===targetLock?.y);
 const chosen=held&&score(held)<=score(best)+2?held:best;targetLock=chosen;return chosen;
}
function getTarget(){
  if(state.interior)return interiorTarget();
  const p=state.player,candidates=[];if(state.boatId){if(p.x>59*32&&Math.hypot(p.x-61*32,p.y-25*32)<240)return {kind:'whale',x:61*32,y:25*32,label:tr('Sõbralik vaalapüük')};return {kind:'boatExit',x:p.x,y:p.y,label:tr('Astu kaldale')};}
  function candidate(kind,x,y,range,label,ref){const d=Math.hypot(p.x-x,p.y-y);if(d<range&&(state.inCave||heightAt(x,y)===heightAt(p.x,p.y)))candidates.push({kind,x,y,d,label,ref});}
  for(const drop of state.drops.filter(d=>!!d.inCave===state.inCave&&!d.room))candidate('drop',drop.x,drop.y,40,tr`Korja ${names[drop.id].toLowerCase()} (${drop.amount})`,drop);
  for(const r of resources.filter(r=>!!r.inCave===state.inCave&&(r.alive||r.type==='wood'&&!r.removed)))candidate('resource',r.x,r.y,45,forageDefs[r.type]?.label||(!r.alive?tr('Eemalda känd'):r.type==='wood'?tr('Raiu puud'):['stone','ironOre','copperOre'].includes(r.type)?tr`Kaevanda ${names[r.type==='cactus'?'water':r.type].toLowerCase()}`:r.type==='herbs'?tr('Korja maitsetaimi'):r.type==='cactus'?tr('Kogu kaktusevett'):tr('Korja marju')),r);
  if(state.inCave){if(!state.crystalFound)candidate('crystal',32*TILE,20*TILE,48,tr('Võta metsakristall'));candidate('exit',32*TILE,29*TILE,48,tr('Mine metsa'));}
  else{
    for(const n of npcData)candidate('npc',n.x,n.y,44,tr`Räägi: ${n.name}`,n);
    for(const b of state.buildings.filter(b=>['chest','garden','boat','door'].includes(b.type)))candidate(b.type,(b.x+.5)*32,(b.y+.5)*32,42,({chest:tr('Ava hoiukast'),garden:b.crop?gardenDescription(b):tr('Istuta peenrasse'),boat:state.boatId?tr('Astu kaldale'):tr('Istu paati'),door:tr('Ava uks / sisene majja')})[b.type],b);
    if(state.boatId)candidate('boatExit',p.x,p.y,1,tr('Astu kaldale'));
    if(state.boatId&&p.x>59*32&&Math.hypot(p.x-61*32,p.y-25*32)<240)candidate('whale',61*32,25*32,240,tr('Sõbralik vaalapüük'));
    candidate('bench',base.x+35,base.y,46,tr('Kasuta meisterdamislauda'));candidate('cave',cave.x,cave.y,58,tr('Sisene salakoopasse'));
    for(const b of state.buildings.filter(b=>['fire','furnace'].includes(b.type)))candidate(b.type,(b.x+.5)*TILE,(b.y+.5)*TILE,48,b.type==='fire'?tr('Lõke ja toiduvalmistamine'):tr('Sulatusahi'),b);
    if(state.meteorArrived&&!state.alienFriend)candidate('alien',meteor.x+30,meteor.y+30,55,tr('Ütle Nupsile tere'));
  }
  return chooseTarget(candidates);
}
function interact(){
  if(!started||paused||death||actionCooldown>0)return;
  if(buildType){const p=buildPoint();place(p.x,p.y);return;}
  const t=getTarget();if(!t){jump();return;}if(extraInteract(t))return;
  if(t.kind==='resource'){collect(t.ref);actionCooldown=.28;}
  else if(t.kind==='drop'){if(addItem(state,t.ref.id,t.ref.amount)){state.drops.splice(state.drops.indexOf(t.ref),1);notify(tr('Korjasid oma asjad üles.'));refresh();save();}else notify(tr('Seljakott on täis.'));}
  else if(['bench','fire','furnace'].includes(t.kind))openModal(t.kind==='bench'?'craft':t.kind);
  else if(t.kind==='crystal'){state.crystalFound=true;const added=addOrDrop('crystal',3);gainXP(state,55);sound('crystal');if(added)notify(tr('Metsakristall leitud! Sinu esimene suur seiklus on tehtud.'));refresh();save();}
  else if(t.kind==='cave'){
    if(!state.tools.includes('pickaxe')||!state.tools.includes('torch')){notify(tr('Koopasse minekuks vajad kirkat ja tõrvikut.'));return;}
    state.inCave=true;state.player.x=32*TILE;state.player.y=27*TILE;moveAlienScene();notify(tr('Salakoobas · kristall asub põhja pool.'));
  }else if(t.kind==='exit'){state.inCave=false;state.player.x=cave.x;state.player.y=cave.y+48;moveAlienScene();}
  else if(t.kind==='alien'){state.alienFriend=true;state.alienFollowing=true;state.alien={x:t.x,y:t.y,inCave:false};const added=addOrDrop('star',6);gainXP(state,35);sound('alien');if(added)notify(tr('Nups on sinu sõber! B / T käsib tal oodata või kaasa tulla.'));refresh();save();}
}
function moveAlienScene(){if(state.alienFriend&&state.alienFollowing){state.alien.inCave=state.inCave;state.alien.x=state.player.x+35;state.alien.y=state.player.y+20;}}
function alienCommand(){
  if(!state.alienFriend){notify(tr('Kõigepealt leia meteoriidiga saabunud Nups.'));return;}
  if(state.alienFollowing){state.alienFollowing=false;notify(tr('Nups ootab siin. Mine tema juurde ja vajuta B / T, et ta kaasa kutsuda.'));}
  else if(state.alien.inCave===state.inCave&&Math.hypot(state.alien.x-state.player.x,state.alien.y-state.player.y)<95){state.alienFollowing=true;sound('alien');notify(tr('Nups tuleb sinuga kaasa ja aeglustab vastaseid.'));}
  else notify(tr('Nups ootab seal, kuhu ta jätsid. Kutsu teda lähedalt.'));save();
}
function beginAction(){if(!started||paused||death)return;if(buildType){rotateBuild();return;}if(tools[tool].id==='bow'){if(!charge)charge={time:0};}else if(tools[tool].id==='rod')beginFishing();else attack();}
function endAction(){if(charge&&!paused&&!death){const stats=bowStats(state,charge.time),p=state.player;arrows.push({x:p.x+aim.x*16,y:p.y-10+aim.y*16,vx:aim.x*stats.speed,vy:aim.y*stats.speed,remaining:stats.range,damage:stats.damage,inCave:state.inCave});state.arrowsFired=(state.arrowsFired||0)+1;state.lastShot={power:stats.power,range:stats.range};sound('arrow');actionCooldown=.25;}charge=null;}
function attack(){
  if(actionCooldown>0)return;actionCooldown=.35;state.player.swing=.2;sound('swing');
  const p=state.player;
  if(tools[tool].id==='axe'&&isOutside()){
    const wall=state.buildings.filter(b=>b.type==='wall'&&Math.hypot((b.x+.5)*TILE-p.x,(b.y+.5)*TILE-p.y)<53).sort((a,b)=>Math.hypot((a.x+.5)*TILE-p.x,(a.y+.5)*TILE-p.y)-Math.hypot((b.x+.5)*TILE-p.x,(b.y+.5)*TILE-p.y))[0];
    if(wall){wall.hp=(wall.hp??3)-1;if(wall.hp<=0){state.buildings.splice(state.buildings.indexOf(wall),1);const n=Math.floor((wall.paidWood??2)/2);if(n)state.drops.push({id:'wood',amount:n,x:(wall.x+.5)*TILE,y:(wall.y+.5)*TILE,inCave:false,expires:state.worldAge+600});notify(tr('Sein lõhutud. Pool puidust jäi maha.'));save();}burst((wall.x+.5)*TILE,(wall.y+.5)*TILE,'#b9975d');return;}
  }
  const entities=state.interior?[]:state.inCave?bats.filter(b=>b.hp>0):[...zombies,...animals];
  const target=entities.filter(e=>Math.hypot(e.x-p.x,e.y-p.y)<52).sort((a,b)=>Math.hypot(a.x-p.x,a.y-p.y)-Math.hypot(b.x-p.x,b.y-p.y))[0];
  if(target){hitEntity(target,1+(state.skills.combat||0)+(tools[tool].id==='axe'&&state.gear?.axe?1:0));return;}
  const t=getTarget();if(t?.kind==='resource')collect(t.ref);
}
function hitEntity(e,damage){e.hp-=damage;burst(e.x,e.y,e.type?'#e0d4ae':'#b6c998');if(e.hp<=0){if(animals.includes(e)){state.wildlifeReturns.push({at:state.worldAge+720,animal:{...e}});animals.splice(animals.indexOf(e),1);const added=e.type!=='skeleton'?addOrDrop('meat',e.type==='deer'?3:1,e.x,e.y):addOrDrop('stone',2,e.x,e.y);if(added&&e.type!=='skeleton')notify(tr('Metsloomalt said liha. Lõkkel saab süüa teha.'));}else if(zombies.includes(e))zombies.splice(zombies.indexOf(e),1);gainXP(state,8);refresh();}else{e.x+=aim.x*12;e.y+=aim.y*12;}}
function eat(){if(!started||death)return;const food=['stew','cookedFish','roast','bakedPotato','carrot','berries'].find(k=>state.inventory[k]>0);if(!food){notify(tr('Korja marju või valmista lõkkel süüa.'));return;}if(state.hunger>=100&&state.health>=maxHealth(state))return;const value={stew:[65,3],roast:[40,2],cookedFish:[45,2],berries:[25,1],carrot:[30,1],bakedPotato:[35,1]}[food];state.inventory[food]--;state.hunger=Math.min(100,state.hunger+value[0]);state.health=Math.min(maxHealth(state),state.health+value[1]);sound('eat');notify(tr`${names[food]} · +${value[0]} kõhtu`);refresh();save();}
function shorePoint(){if(state.inCave||state.interior)return null;const p=state.player;for(let radius=20;radius<=75;radius+=10)for(let a=0;a<16;a++){const angle=a*Math.PI/8,x=p.x+Math.cos(angle)*radius,y=p.y+Math.sin(angle)*radius;if(water(x,y))return{x,y};}return null;}
function beginFishing(){if(fishing){fishing=null;notify(tr('Õng on kokku pandud.'));return;}const shore=shorePoint();if(!shore){notify(tr('Kalapüügiks mine veekogu kaldale.'));return;}fishing={...shore,time:0,origin:{x:state.player.x,y:state.player.y}};notify(tr('Õng vees… oota natuke ja hoia paigal.'));}
function rotateBuild(){if(!['wall','door'].includes(buildType))return;rotation=rotation==='v'?'h':'v';notify(rotation==='v'?tr('Sein: vertikaalne'):tr('Sein: horisontaalne'));}
function ensureBuildCursor(){if(!buildCursor){const p=state.player;buildCursor={x:Math.floor((p.x+aim.x*48)/32),y:Math.floor((p.y+aim.y*48)/32)};}return buildCursor;}
function moveBuildCursor(dx,dy){inputMode='pad';canvas._pointer=null;const c=ensureBuildCursor(),v=rotateVector(dx,dy,isOutside()?-(state.camera||0):0);c.x=Math.max(2,Math.min(state.interior?9:W-3,c.x+v.x));c.y=Math.max(2,Math.min(state.interior?7:H-3,c.y+v.y));}
function buildPoint(){if(inputMode==='pad'){const c=ensureBuildCursor();return {x:(c.x+.5)*32,y:(c.y+.5)*32};}return canvas._pointer||{x:state.player.x+aim.x*48,y:state.player.y+aim.y*48};}
function missingMaterials(cost){const inventory=availableInventory(state);return Object.entries(cost).filter(([id,n])=>(inventory[id]||0)<n).map(([id,n])=>`${n-(inventory[id]||0)} ${names[id]}`).join(', ');}
function placement(x,y){
 const gx=Math.floor(x/32),gy=Math.floor(y/32),cx=(gx+.5)*32,cy=(gy+.5)*32,r=recipes.find(r=>r.id===buildType),items=worldItems();
 const layers=t=>['floor','stoneFloor'].includes(t)?'floor':t==='roof'?'roof':t==='ceiling'?'ceiling':['deskLamp','wallLamp'].includes(t)?'lamp':'object';
 let reason='';
 if(!r)reason=tr('Vali ehitusosa.');
 else if(state.inCave)reason=tr('Koopas ei saa ehitada.');
 else if(Math.hypot(cx-state.player.x,cy-state.player.y)>=145)reason=tr('Liiga kaugel — liigu lähemale.');
 else if(state.interior&&(gx<2||gx>9||gy<2||gy>7))reason=tr('Väljaspool toa ehitusala.');
 else if(state.interior&&!['chest','bed','table','stairs','ceiling','deskLamp','wallLamp','crystalLamp','fire','furnace'].includes(buildType))reason=tr('See osa sobib ainult õue.');
 else if(!state.interior){
  if(gx<2||gy<2||gx>=W-2||gy>=H-2)reason=tr('Väljaspool ehitusala.');
  else if(findHouses(state.buildings).some(h=>h.tiles.some(t=>t.x===gx&&t.y===gy)))reason=tr('Valmis maja on ees.');
  else if(buildType==='boat'?!(water(cx,cy)&&cx>=58*32):water(cx,cy))reason=buildType==='boat'?tr('Paat vajab merevett.'):tr('Siin on vesi.');
  else if(Math.hypot(cx-cave.x,cy-cave.y)<=75||Math.hypot(cx-(base.x+35),cy-base.y)<=32||npcData.some(n=>Math.hypot(cx-n.x,cy-n.y)<30))reason=tr('Jäta käigutee vabaks.');
  else if(resources.some(r=>!r.inCave&&(r.alive||r.type==='wood'&&!r.removed)&&!['berries','herbs',...Object.keys(forageDefs)].includes(r.type)&&Math.hypot(r.x-cx,r.y-cy)<25))reason=tr('Eemalda esmalt puu, känd või kivi.');
 }
 if(!reason&&items.some(b=>b.x===gx&&b.y===gy&&layers(b.type)===layers(buildType)))reason=tr('See ruut on juba hõivatud.');
 if(!reason&&['roof','wall','door','window'].includes(buildType)&&!items.some(b=>b.x===gx&&b.y===gy&&['floor','stoneFloor'].includes(b.type)))reason=tr('Paigalda esmalt põrand.');
 if(!reason&&['wall','window','door','chest','table','bed'].includes(buildType)&&solidBuildingAt([{x:gx,y:gy,type:buildType,rotation:rotation==='auto'?undefined:rotation}],state.player.x,state.player.y))reason=tr('Simm on ees — astu kõrvale.');
 if(!reason&&r){const missing=missingMaterials(costFor(r));if(missing)reason=tr`Puudu: ${missing}`;}
 return {gx,gy,cx,cy,valid:!reason,reason};
}
function place(x,y){if(!buildType)return;const loc=placement(x,y);if(!loc.valid){notify(loc.reason);return;}const r=recipes.find(r=>r.id===buildType),cost=costFor(r);if(!payNearby(state,cost))return;
 const b={id:'b'+state.worldAge+':'+loc.gx+':'+loc.gy,x:loc.gx,y:loc.gy,type:buildType,paidWood:cost.wood||0};if(state.interior){b.room=state.interior.id;b.level=state.interior.level;state.roomItems.push(b);}else state.buildings.push(b);
 if(rotation!=='auto'&&['wall','door','window'].includes(buildType))b.rotation=rotation;if(['fire','furnace'].includes(buildType))b.fuel=0;if(buildType==='chest')b.items={};if(!state.interior)for(const resource of resources.filter(r=>!r.inCave&&Math.hypot(r.x-loc.cx,r.y-loc.cy)<25&&['berries','herbs',...Object.keys(forageDefs)].includes(r.type))){resource.alive=false;state.regrowth[resource.id]=state.worldAge+360;}
 if(buildType==='beacon'){state.beaconBuilt=true;sound('crystal');notify(tr('Tähemajakas särab!'));}gainXP(state,5);burst(loc.cx,loc.cy,'#e4c576');sound('build');refresh();save();notify(tr`${r.name} paigaldatud. Vali järgmine ruut.`);
}
function isSheltered(){if(state.interior)return true;if(state.inCave)return false;const sx=Math.floor(state.player.x/TILE),sy=Math.floor(state.player.y/TILE);const walls=state.buildings.filter(b=>b.type==='wall'||b.type==='window'||b.type==='door'&&!b.open);if(walls.length<4)return false;const blocks=new Set(walls.map(b=>`${b.x},${b.y}`)),stack=[[sx,sy]],seen=new Set();if(blocks.has(`${sx},${sy}`))return false;while(stack.length){const[x,y]=stack.pop(),k=`${x},${y}`;if(blocks.has(k)||seen.has(k))continue;if(x<0||y<0||x>=W||y>=H)return false;seen.add(k);for(const[dx,dy]of[[1,0],[-1,0],[0,1],[0,-1]])stack.push([x+dx,y+dy]);}return true;}
function blocked(x,y,enemy=false,inCave=state.inCave){
 if(state.interior)return x<2*32||x>10*32||y<2*32||y>8*32||!!solidBuildingAt(worldItems(),x,y);
 if(inCave)return x<27*TILE||x>37*TILE||y<18*TILE||y>30*TILE;
 if(x<60||y<70||x>W*TILE-38||y>H*TILE-60)return true;
 if(state.boatId&&!enemy)return !water(x,y)||x<58*32;
 return water(x,y)||!!solidBuildingAt(state.buildings,x,y);
}
function recoverShorePosition(){
 const p=state.player;if(!isOutside()||state.boatId||!water(p.x,p.y))return;
 const points=[];for(let dy=-5;dy<=5;dy++)for(let dx=-5;dx<=5;dx++){const x=(Math.floor(p.x/32)+dx+.5)*32,y=(Math.floor(p.y/32)+dy+.5)*32;if(!blocked(x,y))points.push({x,y,d:Math.hypot(x-p.x,y-p.y)});}
 points.sort((a,b)=>a.d-b.d);if(points[0]){p.x=points[0].x;p.y=points[0].y;}
}
function scaredByFire(x,y){if(tools[tool].id==='torch'&&Math.hypot(x-state.player.x,y-state.player.y)<110)return{x:state.player.x,y:state.player.y};if(!state.inCave)return state.buildings.filter(b=>b.type==='fire'&&b.fuel>0).map(b=>({x:(b.x+.5)*TILE,y:(b.y+.5)*TILE})).find(f=>Math.hypot(x-f.x,y-f.y)<150);return null;}
function damagePlayer(amount=1){if(invulnerable>0||death)return;state.health=Math.max(0,state.health-amount);invulnerable=state.skills.guardian?3:2;damageFlash=.55;sound('hurt');burst(state.player.x,state.player.y,'#efd39a',12);if(state.health<=0)beginDeath();}
function beginDeath(){death={time:0,restored:false};charge=null;fishing=null;state.player.walk=0;keys={};$('deathOverlay').classList.remove('hidden');}
function updateDeath(dt){death.time+=dt;$('deathOverlay').style.opacity=String(death.time<.8?death.time/.8:death.time<1.8?1:Math.max(0,1-(death.time-1.8)/.9));if(death.time>=1&&!death.restored){death.restored=true;state.player.x=base.x;state.player.y=base.y+64;state.inCave=false;state.interior=null;state.boatId=null;state.health=maxHealth(state);state.hunger=100;state.thirst=100;state.day++;state.time=0;zombies.length=0;resetHostilesAfterDefeat(state,animals);invulnerable=3;moveAlienScene();refresh();save();}if(death.time>=2.7){death=null;$('deathOverlay').classList.add('hidden');notify(tr('Uus hommik. Kõik asjad on alles.'));}}
function spawnZombies(){zombies.length=0;const p=state.player;for(let i=0;i<4;i++){const a=i*Math.PI/2,x=Math.max(70,Math.min(W*TILE-70,p.x+Math.cos(a)*260)),y=Math.max(80,Math.min(H*TILE-70,p.y+Math.sin(a)*260));if(!water(x,y))zombies.push({x,y,hp:2,hit:0});}}
function slowed(e){return state.alienFriend&&state.alienFollowing&&state.alien.inCave===state.inCave&&Math.hypot(e.x-state.alien.x,e.y-state.alien.y)<(state.skills.frost?160:100);}
function moveEnemy(e,dt,speed,sheltered=false){const fire=scaredByFire(e.x,e.y),p=state.player;const dx=fire?e.x-fire.x:p.x-e.x,dy=fire?e.y-fire.y:p.y-e.y,n=Math.hypot(dx,dy)||1;e.slowed=slowed(e);if(fire||!sheltered){const v=fire?55:speed*(e.slowed?Math.max(.25,.6-.08*(state.skills.star||0)):1);const nx=e.x+dx/n*v*dt,ny=e.y+dy/n*v*dt;if(!blocked(nx,e.y,true))e.x=nx;if(!blocked(e.x,ny,true))e.y=ny;if(!fire&&n<25)damagePlayer();}}
function updateAlien(dt){if(!state.alienFriend||state.interior)return;const a=state.alien;if(state.alienFollowing&&a.inCave===state.inCave){const dx=state.player.x-aim.x*28-a.x,dy=state.player.y-aim.y*28-a.y,n=Math.hypot(dx,dy);if(n>10){const step=Math.min(n,105*dt);const nx=a.x+dx/n*step,ny=a.y+dy/n*step;if(!blocked(nx,a.y,false,a.inCave))a.x=nx;if(!blocked(a.x,ny,false,a.inCave))a.y=ny;}}else if(!a.inCave&&state.buildings.some(b=>b.type==='nest'&&Math.hypot((b.x+.5)*TILE-a.x,(b.y+.5)*TILE-a.y)<120)){state.alienWork=(state.alienWork||0)+dt;if(state.alienWork>=35/(1+(state.skills.star||0)*.5)){state.alienWork=0;if(addOrDrop('berries',state.skills.helper?4:2,a.x,a.y))notify(tr('Nups tõi baasi marju!'));}}}
function updateArrows(dt){for(let i=arrows.length-1;i>=0;i--){const a=arrows[i],distance=Math.hypot(a.vx,a.vy)*dt;const steps=Math.max(1,Math.ceil(distance/7));let gone=false;for(let j=0;j<steps;j++){a.x+=a.vx*dt/steps;a.y+=a.vy*dt/steps;a.remaining-=distance/steps;if(blocked(a.x,a.y,false,a.inCave)){gone=true;break;}const entities=a.inCave?bats.filter(b=>b.hp>0):[...zombies,...animals];const e=entities.find(e=>Math.hypot(e.x-a.x,e.y-10-a.y)<20);if(e){hitEntity(e,a.damage);gone=true;break;}}if(gone||a.remaining<=0)arrows.splice(i,1);}}
function updateHUD(){
  $('hearts').textContent=Array.from({length:maxHealth(state)},(_,i)=>i<state.health?'♥':'♡').join(' ');$('foodBar').style.width=`${state.hunger}%`;$('foodText').textContent=`${Math.ceil(state.hunger)}%`;
  const night=state.time>=300,left=Math.ceil((night?360:300)-state.time);$('sunIcon').textContent=night?'☾':'☀';$('dayLabel').textContent=getLanguage()==='et'?`${state.day}. päev`:`Day ${state.day}`;$('timeLabel').textContent=`${night?tr('Öö'):tr('Päev')} · ${Math.floor(left/60)}:${String(left%60).padStart(2,'0')}`;$('effectStatus').textContent=[state.effects.speed>0?tr('➤ KIIRUS ')+Math.ceil(state.effects.speed)+' s':'',state.effects.peace>0?tr('❧ LOOMASÕBER ')+Math.ceil(state.effects.peace)+' s':'',isOutside()&&biomeAt(state.player.x,state.player.y)==='desert'?tr('☀ KUUMUS ')+Math.ceil(state.heat)+tr('% · VESI ')+Math.ceil(state.thirst)+'%':''].filter(Boolean).join('\n');$('areaName').textContent=state.interior?tr('Sinu kodu · ')+(state.interior.level+1)+tr('. korrus'):isOutside()&&biomeAt(state.player.x,state.player.y)==='desert'?tr('Päikeseliiva kõrb'):state.boatId?tr('Sõudepaat · Idameri'):state.inCave?tr('Metsakristalli salakoobas'):isSheltered()?tr('Sinu turvaline kodu'):tr('Rohelaane mets');
  currentTarget=getTarget();$('interaction').dataset.target=currentTarget?.kind||'';let prompt=buildType?(inputMode==='pad'?tr('Parem kang / ristnupud · Vali ruut   A · Ehita   X · Pööra   B · Lõpeta'):tr('Hiir · Vali ruut   E / klõps · Ehita   Q · Pööra   Esc · Lõpeta')):fishing?tr('Õng vees… kala näkkab varsti'):charge?tr`Vibu laeb · ${Math.round(bowStats(state,charge.time).power*100)}% · vabasta RT / tühik`:currentTarget?`A / E · ${currentTarget.label}`:tools[tool].id==='rod'&&shorePoint()?tr('RT / tühik · Püüa kala'):tr('A / E · Hüppa');
  if(!buildType&&!currentTarget&&cliffHintUntil>elapsed)prompt=tr('Kõrgusaste · A / E või F · Hüppa üles');
  $('interaction').textContent=prompt;$('interaction').classList.toggle('hidden',!prompt||paused||!!death);
  $('buildInfo').classList.toggle('hidden',!buildType);
  if(buildType){const r=recipes.find(r=>r.id===buildType),point=buildPoint(),loc=placement(point.x,point.y),inventory=availableInventory(state),cost=costFor(r),count=Math.min(...Object.entries(cost).map(([id,n])=>Math.floor((inventory[id]||0)/n)));$('buildInfo').dataset.grid=`${loc.gx},${loc.gy}`;$('buildInfo').dataset.valid=String(loc.valid);$('buildInfo').innerHTML=tr`<strong>${r.name}</strong>${Object.entries(cost).map(([k,v])=>`${names[k]}: ${v} (${inventory[k]||0})`).join(' · ')}<br>Saad ehitada: ${count}<br>Ruut: ${loc.gx}, ${loc.gy}<br>${loc.valid?tr('Valmis ehitamiseks'):loc.reason}`;}
  $('hearts').classList.toggle('hurt',damageFlash>0);$('hearts').classList.toggle('protected',invulnerable>0);$('hearts').setAttribute('aria-label',`${state.health} / ${maxHealth(state)} · ${invulnerable>0?tr('Ajutine kaitse'):tr('Elupunktid')}`);
  $('protectionStatus').textContent=invulnerable>0?tr`◈ Ajutine kaitse · ${Math.ceil(invulnerable)} s`:'';
  updateQuestTracker();
  $('damageOverlay').style.opacity=String(Math.max(0,damageFlash/.55));
}
function update(dt,pad){
  elapsed+=dt;tickEffects(state,dt);toastTime-=dt;if(toastTime<=0)$('toast').classList.add('hidden');damageFlash=Math.max(0,damageFlash-dt);invulnerable=Math.max(0,invulnerable-dt);
  if(!started||paused){updateHUD();return;}if(death){updateDeath(dt);updateHUD();return;}if(state.health<=0){beginDeath();updateHUD();return;}
  actionCooldown=Math.max(0,actionCooldown-dt);const p=state.player;
  let dx=(keys.KeyD||keys.ArrowRight?1:0)-(keys.KeyA||keys.ArrowLeft?1:0)+pad.x,dy=(keys.KeyS||keys.ArrowDown?1:0)-(keys.KeyW||keys.ArrowUp?1:0)+pad.y,n=Math.hypot(dx,dy);
  if(n>0){
   if(n>1){dx/=n;dy/=n;}const v=rotateVector(dx,dy,isOutside()?-(state.camera||0):0);dx=v.x;dy=v.y;
   const speed=(state.boatId?85:105)*(state.effects.speed>0?1.5:1),nx=p.x+dx*speed*dt,ny=p.y+dy*speed*dt,oldX=p.x,oldY=p.y;
   function step(x,y){if(blocked(x,y))return false;if(isOutside()&&!canStep(state,x,y)){cliffHintUntil=elapsed+1.2;return false;}return true;}
   if(step(nx,p.y))p.x=nx;if(step(p.x,ny))p.y=ny;
   if(Math.hypot(p.x-oldX,p.y-oldY)>.001)p.walk+=dt*10;else p.walk=0;
   if(dx)p.face=dx<0?-1:1;if(!canvas._pointer&&!pad.aimed&&!charge){const length=Math.hypot(dx,dy);aim={x:dx/length,y:dy/length};}
  }else p.walk=0;
  if(p.swing)p.swing-=dt;if(charge)charge.time=Math.min(1.5,charge.time+dt);
  worldTick+=dt;if(worldTick>=1){worldTick=0;regrowResources(state,resources);respawnWildlife();}
  if(isOutside()&&biomeAt(p.x,p.y)==='desert'){state.heat=Math.min(100,state.heat+dt*2);state.thirst=Math.max(0,state.thirst-dt*.8);if(lakeWaterNear())state.thirst=Math.min(100,state.thirst+dt*8);if(state.thirst===0){state.heatDamage=(state.heatDamage||0)+dt;if(state.heatDamage>8){damagePlayer();state.heatDamage=0;notify(tr('PALAV! JOO VETT VÕI LEIA OAAS.'));}}}else state.heat=Math.max(0,state.heat-dt*3);
  const wasNight=state.time>=300;advanceTime(state,dt);if(!wasNight&&state.time>=300){spawnZombies();notify(tr('Öö saabus. Lõke, tõrvik ja kodu kaitsevad sind.'));}if(wasNight&&state.time<300){zombies.length=0;state.nightsSurvived=(state.nightsSurvived||0)+1;gainXP(state,20);refresh();notify(tr('Algab uus päev! Elasid öö üle.'));}
  if(!state.meteorArrived&&(state.time>55||state.day>1)){state.meteorArrived=true;meteorFall={time:0};notify(tr('Tähelangus ida pool! Sealt saabub väike külaline.'));save();}
  if(state.hunger<=0){state.starve=(state.starve||0)+dt;if(state.starve>15){damagePlayer();state.starve=0;notify(tr('Kõht on tühi! Söö marju.'));}}
  if(fishing){fishing.time+=dt;if(Math.hypot(p.x-fishing.origin.x,p.y-fishing.origin.y)>12){fishing=null;notify(tr('Liikusid eemale — püük katkes.'));}else if(fishing.time>=3){const added=addOrDrop('fish',state.skills.angler?2:1);gainXP(state,8);sound('fish');if(added)notify(tr('Kala käes! Lõkkel saad selle küpsetada.'));fishing=null;save();}}
  if(meteorFall){meteorFall.time+=dt;if(meteorFall.time>=1.5){burst(meteor.x,meteor.y,'#e6d591',35);sound('crystal');meteorFall=null;}}
  updateAlien(dt);
  if(isOutside()){
    for(const a of animals){if(['wolf','bear','skeleton'].includes(a.type)){updatePredator(a,dt);continue;}a.timer-=dt;const d=Math.hypot(a.x-p.x,a.y-p.y),fire=scaredByFire(a.x,a.y);if(fire||d<100){const from=fire||p;a.dir=Math.atan2(a.y-from.y,a.x-from.x);a.timer=.4;}else if(a.timer<0){a.dir=rand()*6.28;a.timer=2+rand()*4;}const speed=fire||d<100?52:9;const nx=a.x+Math.cos(a.dir)*speed*dt,ny=a.y+Math.sin(a.dir)*speed*dt;if(!blocked(nx,ny,false,false)&&!water(nx-8,ny)&&!water(nx+8,ny)&&!water(nx,ny-6)&&!water(nx,ny+6)){a.x=nx;a.y=ny;a.step+=dt*8;}else a.dir+=2;}
    const sheltered=isSheltered();if(sheltered&&!state.shelterFound){state.shelterFound=true;gainXP(state,35);refresh();save();notify(tr('Oma kodu! Sinu esimene turvaline tuba on valmis.'));}for(const z of zombies)moveEnemy(z,dt,23,sheltered);
  }else if(state.inCave)for(const b of bats.filter(b=>b.hp>0))moveEnemy(b,dt,17);
  for(const b of state.buildings.filter(b=>['fire','furnace'].includes(b.type)))b.fuel=Math.max(0,(b.fuel||0)-dt);
  updateArrows(dt);
  for(let i=particles.length-1;i>=0;i--){const a=particles[i];a.life-=dt;a.x+=a.vx*dt;a.y+=a.vy*dt;a.vy+=90*dt;if(a.life<=0)particles.splice(i,1);}
  for(let i=pickups.length-1;i>=0;i--){pickups[i].life-=dt;if(pickups[i].life<=0)pickups.splice(i,1);}
  autosave+=dt;if(autosave>10){save();autosave=0;}
  updateHUD();
}
window.addEventListener('keydown',e=>{
  if(e.ctrlKey||e.metaKey||e.altKey)return;
  if(['Space','ArrowUp','ArrowDown','ArrowLeft','ArrowRight','Escape'].includes(e.code))e.preventDefault();
  if(e.repeat)return;keys[e.code]=true;
  if(paused){if(menuKind==='whale'&&whaleGame?.status==='playing'&&e.code==='Space'){e.preventDefault();whaleHeld=true;return;}if(e.code==='BracketLeft'){changeTab(-1);return;}if(e.code==='BracketRight'||e.code==='Tab'){e.preventDefault();changeTab(1);return;}if(e.code==='Escape')closeModal();else if(['ArrowDown','KeyS'].includes(e.code))moveMenu(0,1);else if(['ArrowUp','KeyW'].includes(e.code))moveMenu(0,-1);else if(['ArrowLeft','KeyA'].includes(e.code))moveMenu(-1,0);else if(['ArrowRight','KeyD'].includes(e.code))moveMenu(1,0);else if(e.code==='Enter'||e.code==='Space'){e.preventDefault();activateMenu();}return;}
  if(e.code==='Escape'){if(buildType)buildType=null;else if(started)openModal('pause');return;}if(!started){if(e.code==='Enter'&&document.activeElement?.tagName!=='BUTTON')start();return;}if(death)return;
  if(/^Digit[1-6]$/.test(e.code)){selectTool(+e.code.slice(-1)-1);return;}
  switch(e.code){case'KeyE':interact();break;case'Space':beginAction();break;case'KeyR':eat();break;case'KeyC':openMain();break;case'KeyB':openModal('build');break;case'KeyK':openMain();break;case'KeyI':openMain();break;case'KeyT':alienCommand();break;case'KeyJ':openMain();break;case'KeyZ':rotateCamera(-1);break;case'KeyV':rotateCamera(1);break;case'KeyF':jump();break;case'KeyQ':rotateBuild();break;}
});
window.addEventListener('keyup',e=>{keys[e.code]=false;if(e.code==='Space')whaleHeld=false;if(e.code==='Space')endAction();});
window.addEventListener('blur',()=>{keys={};charge=null;save();});document.addEventListener('visibilitychange',()=>{last=0;keys={};charge=null;if(document.hidden)save();});window.addEventListener('pagehide',save);
function pointerWorld(e){const r=canvas.getBoundingClientRect(),sx=(e.clientX-r.left)*canvas.width/r.width+cam.x,sy=(e.clientY-r.top)*canvas.height/r.height+cam.y;let pos=rotateVector(sx,sy/.62,isOutside()?-(state.camera||0):0);if(isOutside())for(let i=0;i<3;i++)pos=rotateVector(sx,(sy+heightAt(pos.x,pos.y)*12)/.62,-(state.camera||0));return pos;}
canvas.addEventListener('pointermove',e=>{if(!e.movementX&&!e.movementY)return;inputMode='mouse';const pos=pointerWorld(e),dx=pos.x-state.player.x,dy=pos.y-state.player.y,n=Math.hypot(dx,dy)||1;aim={x:dx/n,y:dy/n};if(Math.abs(aim.x)>.15)state.player.face=aim.x<0?-1:1;canvas._pointer=pos;});
canvas.addEventListener('pointerdown',e=>{if(!started||paused||death)return;inputMode='mouse';canvas.focus();canvas.setPointerCapture(e.pointerId);if(buildType){const pos=pointerWorld(e);place(pos.x,pos.y);}else beginAction();});canvas.addEventListener('pointerup',endAction);canvas.addEventListener('pointercancel',()=>charge=null);
function readPad(){
  const pad=[...(navigator.getGamepads?.()||[])].find(p=>p?.connected);
  if(!pad){if($('controllerStatus').textContent!==tr('KLAVIATUUR + HIIR'))$('controllerStatus').textContent=tr('KLAVIATUUR + HIIR');padPrevious={};return{x:0,y:0};}
  if($('controllerStatus').textContent!==tr('XBOX · VIEW KOTT · Y EHITA · RT TÖÖRIIST'))$('controllerStatus').textContent=tr('XBOX · VIEW KOTT · Y EHITA · RT TÖÖRIIST');
  const down=i=>!!pad.buttons[i]&&(pad.buttons[i].pressed||pad.buttons[i].value>.25),pressed=i=>down(i)&&!padPrevious[i],released=i=>!down(i)&&padPrevious[i];
  const lx=pad.axes[0]||0,ly=pad.axes[1]||0,ax=pad.axes[2]||0,ay=pad.axes[3]||0;
  if(!assetsReady){pad.buttons.forEach((_,i)=>padPrevious[i]=down(i));return{x:0,y:0};}
  if(paused){
    whaleHeld=down(7)||!!keys.Space;
    if(pressed(1)||pressed(9))closeModal();
    else{if(Math.abs(ay)>.25){const panel=menuKind==='skills'?$('modalDetail'):$('modalContent');panel.scrollTop+=ay*12;}
      let direction=null;
      if(down(12))direction={x:0,y:-1};else if(down(13))direction={x:0,y:1};else if(down(14))direction={x:-1,y:0};else if(down(15))direction={x:1,y:0};
      else if(Math.max(Math.abs(lx),Math.abs(ly))>.40)direction=Math.abs(ly)>=Math.abs(lx)?{x:0,y:Math.sign(ly)}:{x:Math.sign(lx),y:0};
      const key=direction?`${direction.x},${direction.y}`:null,now=performance.now();
      if(key&&key!==menuDirection){if(!menuCache.length&&direction.y)$('modalContent').scrollTop+=direction.y*110;else moveMenu(direction.x,direction.y);menuRepeatAt=now+260;}
      else if(key&&now>=menuRepeatAt){if(!menuCache.length&&direction.y)$('modalContent').scrollTop+=direction.y*110;else moveMenu(direction.x,direction.y);menuRepeatAt=now+85;}
      menuDirection=key;if(!key)menuRepeatAt=0;
      if(pressed(0))inputMode='pad';if(pressed(0)&&!(menuKind==='whale'&&whaleGame?.status==='playing'))activateMenu();
      if(menuKind==='chest'&&pressed(2))transferFocusedStack();if(pressed(4))changeTab(-1);if(pressed(5))changeTab(1);
    }
  }else if(!started){if(pressed(0))start();if(pressed(3)){if(saveFound)openModal('newgame');else startNewGame();}
  }else if(!death){
    if(buildType){let d=down(12)?[0,-1]:down(13)?[0,1]:down(14)?[-1,0]:down(15)?[1,0]:Math.max(Math.abs(ax),Math.abs(ay))>.5?(Math.abs(ax)>Math.abs(ay)?[Math.sign(ax),0]:[0,Math.sign(ay)]):null;const key=d?.join(','),now=performance.now();if(key&&(key!==buildDirection||now>=buildRepeatAt)){moveBuildCursor(...d);buildRepeatAt=now+(key!==buildDirection?280:140);}buildDirection=key;if(pressed(0)||pressed(7)){inputMode='pad';interact();}}else if(pressed(0))interact();if(pressed(2)){if(buildType)rotateBuild();else{beginAction();if(tools[tool].id==='bow')endAction();}}
    if(pressed(3)){inputMode='pad';openModal('build');}if(pressed(8)){inputMode='pad';openMain();}if(pressed(9))openModal('pause');if(pressed(11))openMain();if(!buildType){if(pressed(12))openMain();if(pressed(14))rotateCamera(-1);if(pressed(15))rotateCamera(1);}
    if(pressed(1)){if(buildType)buildType=null;else alienCommand();}
    if(pressed(4))cycleTool(-1);if(pressed(5))cycleTool(1);if(pressed(6))eat();
    if(pressed(7)&&!buildType)beginAction();if(released(7)&&!buildType)endAction();
  }
  pad.buttons.forEach((_,i)=>padPrevious[i]=down(i));
  const aimed=Math.hypot(ax,ay)>.2;if(aimed&&!paused&&!buildType){const n=Math.hypot(ax,ay);aim=rotateVector(ax/n,ay/n,isOutside()?-(state.camera||0):0);if(Math.abs(aim.x)>.15)state.player.face=aim.x<0?-1:1;canvas._pointer=null;}
  if(Math.abs(lx)>.18||Math.abs(ly)>.18){canvas._pointer=null;inputMode='pad';if(buildType)ensureBuildCursor();}
  return{x:Math.abs(lx)>.18?lx:0,y:Math.abs(ly)>.18?ly:0,aimed};
}

function moveChestStack(id,toChest){const source=toChest?state.inventory:chestOpen.items;let amount=Math.min(STACK_SIZE,source[id]||0);if(!toChest)while(amount>0&&!addItem({...state,inventory:{...state.inventory}},id,amount))amount--;if(amount&&transferItem(state,chestOpen,id,toChest,amount)){save();refresh();openModal('chest');}else notify(tr('Seljakott on täis. Tee ruumi või kasuta hoiukasti.'));}
function transferFocusedStack(){const key=menuCache[menuIndex]?.dataset.key;if(!key)return;const[direction,id]=key.split(':');moveChestStack(id,direction==='in');}
function gardenDescription(bed){const progress=cropProgress(state,bed),left=Math.ceil(Math.max(0,crops[bed.crop].duration-(state.worldAge-bed.planted))),stage=progress>=1?tr('Saagiküps'):progress>=.66?tr('Valmimas'):progress>=.33?tr('Kasvab'):tr('Võrsed');return `${crops[bed.crop].name} · ${stage} · ${Math.floor(progress*100)}%${left?tr` · Saagini ~${Math.ceil(left/60)} min`:''}`;}
function trackedQuest(){
 if(!state.tools.includes('pickaxe')){const step=firstPickaxeStep(state);return {title:step.title,text:step.text};}
 const npc=npcData.find(n=>!state.npcQuests[n.id]);if(npc)return {title:npc.name,text:Object.entries(npc.request).map(([id,n])=>`${names[id]}: ${Math.min(state.inventory[id]||0,n)}/${n}`).join(' · ')};
 const next=questSteps(state).find(q=>!q.done);return next||{title:tr('Sinu seiklus jätkub'),text:tr('Avasta ja ehita oma maailma.')};
}
let questTrackerCache='';
function updateQuestTracker(){const q=trackedQuest(),text=q.title+' · '+q.text;if(text===questTrackerCache)return;questTrackerCache=text;$('questTracker').textContent=text;}
function extraMenu(kind,content){
 if(kind==='map'){
  content.innerHTML=tr('<p class="build-note">PÕHI ↑ · Metsavaht laagri lähedal · Kaevur koopa kõrval · Kaupmees idas · Kõrb kirdes · Meri idas</p><canvas id="worldMap" width="768" height="576" aria-label="Maailmakaart"></canvas>');
  const g=$('worldMap').getContext('2d');for(let y=0;y<H;y++)for(let x=0;x<W;x++){const biome=biomeAt((x+.5)*32,(y+.5)*32);g.fillStyle=water((x+.5)*32,(y+.5)*32)?'#397c93':biome==='desert'?'#d6b979':heightAt(x*32,y*32)>0?'#91a46b':'#50734b';g.fillRect(x*12,y*12,12,12);}
  function marker(x,y,label,color){g.fillStyle=color;g.beginPath();g.arc(x/32*12,y/32*12,5,0,7);g.fill();g.font='bold 13px sans-serif';g.fillText(label,x/32*12+7,y/32*12-6);}
  marker(base.x,base.y,tr('LAAGER'),'#ffdd8c');marker(cave.x,cave.y,tr('KOOBAS'),'#b7e5ef');npcData.forEach(n=>marker(n.x,n.y,n.name,'#ebdcaf'));marker(61*32,25*32,tr('VAAL'),'#89e0ed');marker(state.interior?.outside.x??state.player.x,state.interior?.outside.y??state.player.y,'SIMM','#fff');return true;
 }
 if(kind==='chest'){
  content.innerHTML=tr('<p class="build-note">A liigutab ühe eseme. X liigutab kuni 20 eset. Seljakotist → kasti või kastist → seljakotti. Sama ruumi ja korruse lähedasi kaste kasutatakse meisterdamisel automaatselt.</p><div class="storage-columns"><section><h3>SELJAKOTT → KAST</h3><div id="depositList"></div></section><section><h3>KAST → SELJAKOTT</h3><div id="withdrawList"></div></section></div>');
  for(const[toChest,inventory,target]of[[true,state.inventory,'depositList'],[false,chestOpen.items||{},'withdrawList']])for(const[id,n]of Object.entries(inventory)){if(!n)continue;const b=document.createElement('button');b.className='storage-row';b.dataset.key=(toChest?'in:':'out:')+id;b.textContent=`${icons[id]} ${names[id]} · ${n} ${toChest?'→':'←'}`;b.onclick=()=>{if(transferItem(state,chestOpen,id,toChest)){save();refresh();openModal('chest');}else notify(tr('Seljakott on täis. Tee ruumi või kasuta hoiukasti.'));};const row=document.createElement('div');row.className='storage-item';const stack=document.createElement('button');stack.className='storage-stack';stack.dataset.key=(toChest?'in:':'out:')+id+':stack';stack.textContent=tr`Liiguta pakk (${Math.min(STACK_SIZE,n)})`;stack.onclick=()=>moveChestStack(id,toChest);row.append(b,stack);$(target).append(row);}return true;
 }
 if(kind==='garden'){
  if(gardenOpen.crop){const progress=cropProgress(state,gardenOpen);content.innerHTML=tr`<p class="build-note">${gardenDescription(gardenOpen)}</p><progress max="1" value="${progress}"></progress><button id="harvestButton" ${progress<1?'disabled':''}>Korista saak</button>`;if(progress<1)content.innerHTML+=tr('<p class="build-note">Kasv jätkub mängu ajal. Sulge menüü ja tule hiljem tagasi.</p>');$('harvestButton').onclick=()=>{if(harvestCrop(state,gardenOpen)){refresh();save();openModal('garden');}else notify(tr('Seljakott on täis. Tee ruumi või kasuta hoiukasti.'));};
  }else{content.innerHTML=tr('<p class="build-note">Vali taim. Seemned on peenraga kaasas ja kastmist pole vaja.</p>');for(const[id,crop]of Object.entries(crops)){const b=document.createElement('button');b.className='storage-row';b.dataset.key=id;b.textContent=tr`${icons[id]} ${crop.name} · ${crop.duration} s · saak ${crop.yield}`;b.onclick=()=>{plantCrop(state,gardenOpen,id);save();openModal('garden');};content.append(b);}}return true;
 }
 if(kind==='npc'){
  const n=npcOpen,done=state.npcQuests[n.id];content.innerHTML=`<div class="npc-dialog"><span>${{ranger:'❧',miner:'⛏',trader:'◈'}[n.id]}</span><h3>${done?tr('AITÄH, SIMM! SA OLED TORE SÕBER.'):n.line}</h3><p>${done?tr('HEAD SEIKLEMIST!'):n.task}</p><p>${done?'':tr('TASU: ')+Object.entries(n.reward).map(([k,v])=>`${names[k].toUpperCase()} ${v}`).join(' · ')}</p><button id="npcQuestButton" ${done||!canPay(state,n.request)?'disabled':''}>${done?tr('ÜLESANNE TEHTUD'):tr('ANNA ASJAD JA VÕTA TASU')}</button></div>`;$('npcQuestButton').onclick=()=>{if(finishNPCQuest(state,n)){sound('craft');refresh();save();openModal('npc');}else notify(tr('TEE SELJAKOTIS RUUMI.'));};return true;
 }
 if(kind==='whale'){
  if(!whaleGame)whaleGame={time:0,marker:.5,target:.5,progress:0,status:'ready'};
  content.innerHTML=tr('<div class="whale-copy"><div id="whaleScene" class="whale-scene"><span>⛵</span><i>──────────✦</i><span>🐋</span></div><h3 id="whaleTitle">TERE, MERESÕBER!</h3><p>PEHME VALGUSHARPUUN ALUSTAB MÄNGU. VAAL EI SAA VIGA.</p><button id="whaleStart">A · HEIDA VALGUSHARPUUN</button><div id="whaleTrack" class="whale-track hidden"><i id="whaleTarget"></i><b id="whaleMarker"></b></div><p id="whaleHint">Hoia RT / tühikut: märk tõuseb. Vabasta: märk langeb. Püsi kuldses alas.</p><progress id="whaleProgress" max="1" value="0"></progress><button id="whaleRelease" class="hidden">A · VABASTA VAAL</button></div>');
  $('whaleStart').onclick=()=>{whaleHeld=false;whaleGame.status='playing';$('whaleScene').classList.add('harpooned');$('whaleStart').classList.add('hidden');$('whaleTrack').classList.remove('hidden');$('whaleTitle').textContent=tr('HOIA MÄRKI KULDSES ALAS');cacheMenu();};
  $('whaleRelease').onclick=()=>{state.whalesReleased++;const added=addOrDrop('pearl',1);gainXP(state,20);whaleGame=null;closeModal();save();if(added)notify(tr('VAAL LEHVITAB! LEIDSID MEREPÄRLI.'));};return true;
 }
 return false;
}
function tickWhale(dt){if(menuKind!=='whale'||!whaleGame||whaleGame.status!=='playing')return;const result=whaleStep(whaleGame,dt,whaleHeld);$('whaleMarker').style.left=whaleGame.marker*100+'%';$('whaleTarget').style.left=(whaleGame.target-.2)*100+'%';$('whaleProgress').value=whaleGame.progress;
 if(result==='caught'){whaleGame.status=result;$('whaleTitle').textContent=tr('SAID HAKKAMA! VAAL OOTAB VABASTAMIST.');$('whaleRelease').classList.remove('hidden');$('whaleHint').textContent=tr('Vajuta A / Enter, et sõber vabastada.');cacheMenu();focusMenu(menuCache.indexOf($('whaleRelease')));}
 if(result==='escaped'){whaleGame=null;closeModal();notify(tr('VAAL UJUS EDASI. PROOVI JÄLLE!'));}
}
function interiorTarget(){const p=state.player,targets=[];
 for(const d of state.drops.filter(d=>d.room===state.interior.id&&(d.level||0)===state.interior.level)){const distance=Math.hypot(p.x-d.x,p.y-d.y);if(distance<40)targets.push({kind:'drop',x:d.x,y:d.y,d:distance,ref:d,label:tr('Korja ')+names[d.id]});}
 for(const b of worldItems()){const d=Math.hypot(p.x-(b.x+.5)*32,p.y-(b.y+.5)*32);if(d<45&&['chest','stairs','bed','fire','furnace'].includes(b.type))targets.push({kind:b.type,x:(b.x+.5)*32,y:(b.y+.5)*32,d,ref:b,label:{chest:tr('Ava hoiukast'),stairs:tr('Mine järgmisele korrusele'),bed:tr('Puhka voodis'),fire:tr('Valmista toitu'),furnace:tr('Sulata')}[b.type]});}
 if(Math.hypot(p.x-6*32,p.y-8*32)<50)targets.push({kind:'houseExit',x:6*32,y:8*32,d:Math.hypot(p.x-6*32,p.y-8*32),label:state.interior.level?tr('Mine alumisele korrusele'):tr('Mine õue')});
 return chooseTarget(targets);
}
function extraInteract(t){
 if(t.kind==='chest'){chestOpen=t.ref;chestOpen.items??={};openModal('chest');}
 else if(t.kind==='garden'){gardenOpen=t.ref;openModal('garden');}
 else if(t.kind==='npc'){npcOpen=t.ref;openModal('npc');}
 else if(t.kind==='door'){const h=findHouses(state.buildings).find(h=>h.door===t.ref);if(h)enterHouse(h);else{t.ref.open=!t.ref.open;notify(t.ref.open?tr('Uks lahti.'):tr('Uks kinni.'));save();}}
 else if(t.kind==='houseExit'){if(state.interior.level>0){state.interior.level--;state.player.y=7*32;save();}else leaveHouse();}
 else if(t.kind==='stairs'){if(canAscend(state)){state.interior.level++;state.player.x=6*32;state.player.y=7*32;notify(tr('KORRUS ')+(state.interior.level+1));save();}else notify(tr('Üles minekuks täida 8×6 ehitusala vahelagedega.'));}
 else if(t.kind==='bed'){state.health=maxHealth(state);state.hunger=Math.max(25,state.hunger);state.day++;state.time=0;state.worldAge+=360;state.thirst=Math.max(50,state.thirst);zombies.length=0;regrowResources(state,resources);save();notify(tr('HEA HOMMIK!'));}
 else if(t.kind==='boat'){state.boatId=t.ref.id||('boat:'+t.ref.x+':'+t.ref.y);state.player.x=(t.ref.x+.5)*32;state.player.y=(t.ref.y+.5)*32;notify(tr('Aeruta vasaku kangi või WASD-ga. A kaldal väljub.'));save();}
 else if(t.kind==='boatExit'){const p=state.player;let shore=null;for(let r=24;r<=90&&!shore;r+=12)for(let i=0;i<16;i++){const x=p.x+Math.cos(i*Math.PI/8)*r,y=p.y+Math.sin(i*Math.PI/8)*r;if(!water(x,y)&&!blocked(x,y,true)&&heightAt(x,y)===0){shore={x,y};break;}}if(!shore){notify(tr('Väljumiseks aeruta ranna lähedale.'));return true;}const boat=state.buildings.find(b=>(b.id||('boat:'+b.x+':'+b.y))===state.boatId);if(boat){boat.x=Math.floor(p.x/32);boat.y=Math.floor(p.y/32);}state.boatId=null;Object.assign(p,shore);save();}
 else if(t.kind==='whale'){whaleGame=null;openModal('whale');}
 else return false;return true;
}
function lakeWaterNear(){return Math.hypot(state.player.x-50*32,state.player.y-16*32)<70;}
function updatePredator(a,dt){
 if((a.calmUntil||0)>state.worldAge)return;
 const p=state.player,peace=state.effects.peace>0&&a.type!=='skeleton';const intent=predatorIntent(a,p,peace),target=intent==='chase'?p:{x:a.homeX,y:a.homeY};
 if(a.type==='skeleton'){const d=Math.hypot(a.x-p.x,a.y-p.y);if(d<210){moveEnemy(a,dt,29,isSheltered());return;}}
 const dx=target.x-a.x,dy=target.y-a.y,n=Math.hypot(dx,dy)||1;a.slowed=slowed(a);const speed=(intent==='chase'?(a.type==='wolf'?73:55):22)*(a.slowed?.45:1);if(n>10){const nx=a.x+dx/n*speed*dt,ny=a.y+dy/n*speed*dt;if(!blocked(nx,a.y,true,false))a.x=nx;if(!blocked(a.x,ny,true,false))a.y=ny;a.step+=dt*8;}
 if(intent==='chase'&&n<26&&!isSheltered()&&!peace)damagePlayer();
}

// Original generated artwork, with a procedural fallback while the sprite sheet loads.
const atlasImage=new Image();atlasImage.onload=()=>{paintMenuArt();paintTitlePortrait();};atlasImage.src='/assets/art/woodland-atlas.png';
const heroImage=new Image();heroImage.onload=paintTitlePortrait;heroImage.src='/assets/art/simm-walk.png';
const extraImage=new Image();extraImage.onload=()=>{paintMenuArt();paintTitlePortrait();};extraImage.src='/assets/art/campsite-atlas.png';
const artRects={
 oak:[0,0,370,377],pine:[374,0,271,377],birch:[650,0,307,377],berries:[963,94,291,282],
 rock:[9,397,343,264],ironOre:[361,405,290,242],copperOre:[649,391,308,266],crystal:[961,367,293,296],
 bench:[8,670,352,277],furnace:[360,672,293,280],fire:[660,667,301,288],nest:[962,658,292,304],
 alien:[35,948,265,305],rabbit:[365,951,287,303],deer:[675,946,277,307],zombie:[970,960,284,293],
 cave:[15,10,552,501,'extra'],tent:[573,110,434,400,'extra'],bat:[1016,208,371,228,'extra'],stump:[1390,197,372,308,'extra'],
 wallH:[69,589,454,239,'extra'],wallV:[612,533,222,309,'extra'],floor:[990,522,334,322,'extra'],stoneFloor:[1388,522,345,322,'extra']
};
const itemArt={beacon:'crystal',wall:'wallH',stoneFloor:'stoneFloor',floor:'floor',stone:'rock',berries:'berries',crystal:'crystal',ironOre:'ironOre',copperOre:'copperOre',iron:'ironOre',copper:'copperOre',nest:'nest',fire:'fire',furnace:'furnace'};
function menuArt(id,fallback='✦'){const key=itemArt[id]||id;return artRects[key]?`<canvas class="menu-art" width="96" height="96" data-art="${key}" aria-hidden="true"></canvas>`:(uiGlyph(id)||fallback);}
function paintMenuArt(){for(const c of document.querySelectorAll('canvas[data-art]')){const r=artRects[c.dataset.art];if(!r)continue;const image=r[4]==='extra'?extraImage:atlasImage;if(!image.complete||!image.naturalWidth)continue;const g=c.getContext('2d');g.imageSmoothingEnabled=false;g.clearRect(0,0,96,96);const w=80*r[2]/r[3],h=w>86?80*86/w:80,width=w>86?86:w;g.drawImage(image,r[0],r[1],r[2],r[3],(96-width)/2,(96-h)/2,width,h);}}
function paintTitlePortrait(){const c=$('titlePortrait');if(!c)return;const g=c.getContext('2d');g.imageSmoothingEnabled=false;g.clearRect(0,0,c.width,c.height);const glow=g.createRadialGradient(200,210,5,200,210,190);glow.addColorStop(0,'#e6d28435');glow.addColorStop(1,'#e6d28400');g.fillStyle=glow;g.fillRect(0,0,400,450);if(heroImage.complete&&heroImage.naturalWidth)g.drawImage(heroImage,120,88,300,545,80,30,185,337);if(atlasImage.complete&&atlasImage.naturalWidth){const r=artRects.alien;g.drawImage(atlasImage,r[0],r[1],r[2],r[3],245,275,115,130);}}
function artSprite(id,x,y,height,flip=false){
 const r=artRects[id],image=r[4]==='extra'?extraImage:atlasImage;if(!image.complete||!image.naturalWidth)return false;
 const width=height*r[2]/r[3];ctx.save();ctx.translate(Math.round(x),Math.round(y));if(flip)ctx.scale(-1,1);ctx.drawImage(image,r[0],r[1],r[2],r[3],Math.round(-width/2),-height,Math.round(width),height);ctx.restore();return true;
}
// Small, hand-drawn pixel sprites. All scenery stays local and animates on canvas.
function rect(x,y,w,h,c){ctx.fillStyle=c;ctx.fillRect(Math.round(x),Math.round(y),w,h);}
function ellipse(x,y,rx,ry,c){ctx.fillStyle=c;ctx.beginPath();ctx.ellipse(x,y,rx,ry,0,0,Math.PI*2);ctx.fill();}
function poly(points,c){ctx.fillStyle=c;ctx.beginPath();points.forEach(([x,y],i)=>i?ctx.lineTo(x,y):ctx.moveTo(x,y));ctx.closePath();ctx.fill();}
function shadow(x,y,rx=18,ry=6){ellipse(x,y,rx,ry,'#152c2040');}
function tree(x,y,variant=0){const occluded=Math.abs(state.player.x-x)<36&&state.player.y<y&&state.player.y>y-85;ctx.save();if(occluded)ctx.globalAlpha*=.55;if(artSprite(variant===1?'pine':Math.round(x)%5===0?'birch':'oak',x+Math.sin(elapsed*1.1+x)*.6,y+6,variant===1?104:90)){ctx.restore();return;}ctx.restore();const sway=Math.sin(elapsed*1.1+x)*1.2;shadow(x,y+3,27,9);rect(x-5,y-29,10,33,'#705038');rect(x-2,y-27,3,27,'#9c7247');rect(x+5,y-12,4,5,'#705038');if(variant===1){poly([[x+sway,y-101],[x-22+sway,y-61],[x-12+sway,y-61],[x-30+sway,y-39],[x-21+sway,y-39],[x-34+sway,y-17],[x+34+sway,y-17],[x+21+sway,y-39],[x+29+sway,y-39],[x+12+sway,y-61],[x+23+sway,y-61]],'#244f3b');poly([[x+sway,y-96],[x-15+sway,y-62],[x-8+sway,y-62],[x-24+sway,y-40],[x-13+sway,y-40],[x-24+sway,y-23],[x+3+sway,y-23],[x+10+sway,y-40],[x+2+sway,y-62]],'#39714a');rect(x-18+sway,y-41,12,3,'#548153');}else{const xx=x+sway;rect(xx-24,y-65,47,35,'#244e35');rect(xx-33,y-54,64,20,'#244e35');rect(xx-20,y-83,38,23,'#365d39');rect(xx-30,y-69,54,30,'#3c6f41');rect(xx-19,y-83,32,30,'#4b7b46');rect(xx-11,y-91,21,11,'#4b7b46');rect(xx-26,y-64,14,11,'#608b4e');rect(xx-15,y-76,11,8,'#70974f');rect(xx+3,y-60,21,10,'#538143');rect(xx+14,y-46,11,7,'#3c6136');rect(xx-21,y-41,25,9,'#315f37');rect(xx-4,y-78,8,3,'#86a65d');}}
function rock(x,y,big=false){if(artSprite('rock',x,y+5,big?42:34))return;shadow(x,y+3,19,6);poly([[x-19,y],[x-15,y-18],[x-4,y-25],[x+11,y-20],[x+19,y-8],[x+14,y+5],[x-10,y+6]],'#61796b');poly([[x-15,y-17],[x-4,y-24],[x+10,y-20],[x+2,y-10],[x-12,y-6]],'#9aaa88');poly([[x+2,y-10],[x+11,y-19],[x+18,y-7],[x+13,y+4],[x+2,y+3]],'#718b79');rect(x-8,y-17,9,3,'#b9c2a0');if(big)rect(x+5,y-7,4,5,'#b8c7a1');}
function bush(x,y){if(artSprite('berries',x,y+3,35))return;shadow(x,y+3,17,5);rect(x-13,y-16,26,17,'#305b36');rect(x-19,y-10,36,11,'#3c7140');rect(x-9,y-22,17,13,'#518347');rect(x-15,y-14,12,5,'#699047');for(const[dx,dy]of[[-10,-8],[-3,-17],[6,-10],[12,-5]]){rect(x+dx,y+dy,5,5,'#7473ad');rect(x+dx,y+dy,2,2,'#b2a3df');}}
function drawHeldTool(x,y){
 const selected=tools[tool].id;
 if(state.player.swing>0){const angle=Math.atan2(aim.y,aim.x)+(state.player.swing/.2-.5)*1.5;ctx.save();ctx.translate(x,y-14);ctx.rotate(angle);rect(8,-2,19,3,'#b8925b');poly([[23,-8],[31,-6],[31,4],[24,7]],'#cbd2b2');ctx.restore();}
 else if(selected==='torch'){const tx=x+12,ty=y-18;rect(tx,ty,3,12,'#9b7545');ellipse(tx+1,ty-3,3.5+Math.sin(elapsed*13)*.6,6,'#f4b34d');ellipse(tx+1,ty-4,1.5,3,'#ffe1a0');}
 else if(selected==='rod'){ctx.strokeStyle='#bda46b';ctx.lineWidth=2;ctx.beginPath();ctx.moveTo(x+8,y-14);ctx.lineTo(x+18,y-39);ctx.stroke();}
}
function simm(x,y){if(heroImage.complete&&heroImage.naturalWidth){const moving=state.player.walk>0,frame=moving?Math.floor(state.player.walk*1.1)%4:0,bob=moving?Math.sin(state.player.walk)*.45:Math.sin(elapsed*2)*.15;ctx.save();ctx.translate(Math.round(x),Math.round(y+bob));if(state.player.face<0)ctx.scale(-1,1);ctx.drawImage(heroImage,frame*(heroImage.naturalWidth/4)+120,88,300,545,-13,-45,27,49);ctx.restore();drawHeldTool(x,y);return;}const p=state.player,bob=p.walk?Math.sin(p.walk)*1.5:0;shadow(x,y+2,12,4);const yy=y+bob,step=p.walk?Math.sin(p.walk)*3:0;rect(x-7,yy-8,5,9+step,'#384739');rect(x+2,yy-8,5,9-step,'#384739');rect(x-8,yy+step,6,3,'#332e23');rect(x+2,yy-step,6,3,'#332e23');rect(x-9,yy-23,18,16,'#d7ac43');rect(x-6,yy-22,9,13,'#ebc45d');rect(x-12,yy-21,4,12,'#b28b37');rect(x+8,yy-21,4,12,'#e4b854');rect(x-12,yy-10,4,4,'#f2c293');rect(x+8,yy-10,4,4,'#f2c293');rect(x-5,yy-33,12,11,'#dca776');rect(x-7,yy-38,14,7,'#695333');rect(x-8,yy-33,4,7,'#695333');rect(x-4,yy-37,9,3,'#937141');rect(x+(p.face<0?-4:3),yy-30,2,2,'#263629');rect(x-6,yy-24,12,3,'#e4c664');rect(x-5,yy-17,3,4,'#b98d38');if(p.swing>0){const sx=x+aim.x*19,sy=yy-15+aim.y*16;rect(sx-2,sy-10,3,21,'#b89259');poly([[sx-8,sy-11],[sx+5,sy-13],[sx+9,sy-6],[sx-7,sy-3]],'#bdc5a9');ellipse(x+aim.x*29,yy-12+aim.y*26,6,3,'#e5db8c80');}else if(tools[tool].id==='torch'){rect(x+12,yy-21,3,12,'#956d3c');ellipse(x+14,yy-26,4+Math.sin(elapsed*12),7,'#eab559');rect(x+12,yy-28,3,5,'#fff1ac');}}
function rabbit(a){if(artSprite('rabbit',a.x,a.y+2+Math.sin(a.step)*.8,24,Math.cos(a.dir)<0))return;const x=a.x,y=a.y,b=Math.sin(a.step)*1;shadow(x,y+2,9,3);rect(x-7,y-9+b,13,8,'#d6cbb3');rect(x+3,y-13+b,8,9,'#e5ddc4');rect(x+4,y-23+b,3,12,'#e5ddc4');rect(x+8,y-21+b,3,9,'#c9bca3');rect(x+5,y-21+b,1,6,'#d7a79e');rect(x+9,y-11+b,2,2,'#343d2c');rect(x-10,y-7+b,4,4,'#eee7d0');rect(x-5,y,3,3,'#b5ad91');rect(x+5,y,3,3,'#b5ad91');}
function deer(a){if(artSprite('deer',a.x,a.y+3+Math.sin(a.step)*.6,44,Math.cos(a.dir)<0))return;const x=a.x,y=a.y,b=Math.sin(a.step);shadow(x,y+1,17,5);for(const dx of[-11,-4,6,12])rect(x+dx,y-13,3,14+Math.sin(a.step+dx)*2,'#876346');rect(x-14,y-26+b,27,14,'#ae8150');rect(x-12,y-25+b,19,5,'#c29965');rect(x+9,y-35+b,7,20,'#b58a59');rect(x+11,y-39+b,14,10,'#bd9663');rect(x+20,y-36+b,2,2,'#293c2c');rect(x+10,y-44+b,4,7,'#a7784c');rect(x+18,y-43+b,4,7,'#a7784c');rect(x-17,y-25+b,5,5,'#e2d0a1');for(const dx of[-5,2,7])rect(x+dx,y-22+b,2,2,'#e5c995');}
function alien(x,y){if(artSprite('alien',x,y+3+Math.sin(elapsed*3)*1.4,35))return;const float=Math.sin(elapsed*3)*2;shadow(x,y+2,11,4);rect(x-8,y-19+float,16,15,'#83b8aa');rect(x-11,y-29+float,22,15,'#a5d0b5');rect(x-8,y-33+float,16,8,'#a5d0b5');rect(x-7,y-26+float,4,6,'#27394a');rect(x+3,y-26+float,4,6,'#27394a');rect(x-6,y-26+float,1,2,'#f0ffdb');rect(x+4,y-26+float,1,2,'#f0ffdb');rect(x-3,y-17+float,6,6,'#d6c17b');rect(x-8,y-37+float,2,6,'#81af9c');rect(x+6,y-37+float,2,6,'#81af9c');rect(x-9,y-39+float,4,3,'#ecdb93');rect(x+5,y-39+float,4,3,'#ecdb93');}
function zombie(z){if(artSprite('zombie',z.x,z.y+4+Math.sin(elapsed*4+z.x)*.8,39,z.x>state.player.x))return;const bob=Math.sin(elapsed*5+z.x)*1;shadow(z.x,z.y,11,4);rect(z.x-7,z.y-10,5,11,'#314c3b');rect(z.x+3,z.y-10,5,11,'#314c3b');rect(z.x-10,z.y-25+bob,20,17,'#637658');rect(z.x-7,z.y-38+bob,15,14,'#9ab678');rect(z.x-12,z.y-22+bob,4,13,'#8fa769');rect(z.x+9,z.y-22+bob,4,13,'#8fa769');rect(z.x-4,z.y-33+bob,3,3,'#354230');rect(z.x+3,z.y-33+bob,3,3,'#354230');rect(z.x-2,z.y-27+bob,6,2,'#4c633a');}
function herb(x,y){shadow(x,y+2,10,3);for(let i=0;i<7;i++){const a=i*Math.PI/3.5,dx=Math.cos(a)*8,dy=Math.sin(a)*4;poly([[x,y],[x+dx,y-12+dy],[x+dx+3,y-8+dy],[x+dx*.5,y-2]],i%2?'#9db965':'#728f4a');rect(x+dx,y-11+dy,2,2,'#bed184');}rect(x-1,y-5,2,6,'#526b34');}
function batSprite(b){if(artSprite('bat',b.x,b.y+Math.sin(elapsed*4+b.phase)*2,22)){return;}const x=b.x,y=b.y+Math.sin(elapsed*4+b.phase)*3,wing=Math.sin(elapsed*10+b.phase)*8;shadow(x,y+25,9,3);poly([[x-4,y],[x-21,y-8-wing],[x-16,y+4],[x-6,y+7]],'#9f90b7');poly([[x+4,y],[x+21,y-8-wing],[x+16,y+4],[x+6,y+7]],'#9f90b7');rect(x-5,y-7,10,15,'#b8a8c9');rect(x-5,y-12,3,6,'#b8a8c9');rect(x+2,y-12,3,6,'#b8a8c9');rect(x-3,y-3,2,3,'#354347');rect(x+2,y-3,2,3,'#354347');rect(x-2,y+4,4,1,'#e9d8d8');}
function bench(){const x=base.x+35,y=base.y;if(!artSprite('bench',x,y+5,43)){shadow(x,y+4,22,6);rect(x-16,y-17,5,23,'#65462e');rect(x+11,y-17,5,23,'#65462e');rect(x-22,y-25,44,10,'#a8804e');rect(x-22,y-26,44,3,'#d1ab6b');rect(x-17,y-23,2,7,'#785831');rect(x-14,y-32,8,7,'#7e9583');rect(x-9,y-36,3,5,'#aabc9a');rect(x+4,y-31,10,5,'#cfb579');rect(x+6,y-37,3,9,'#79664e');}const tx=base.x-55,ty=base.y+6;if(artSprite('tent',tx,ty+6,55))return;shadow(tx,ty+1,33,8);poly([[tx,ty-42],[tx-31,ty],[tx+29,ty]],'#c3ab64');poly([[tx,ty-42],[tx+29,ty],[tx+6,ty]],'#a48f53');poly([[tx,ty-30],[tx-13,ty],[tx+11,ty]],'#3b4630');rect(tx-34,ty,68,3,'#765e3e');}
function caveSprite(){const x=cave.x,y=cave.y;if(artSprite('cave',x,y+12,92)){ctx.fillStyle='#e1dfb7';ctx.font='9px monospace';ctx.textAlign='center';ctx.fillText('SALAKOOBAS',x,y-86);return;}shadow(x,y+8,50,14);poly([[x-55,y+3],[x-46,y-38],[x-23,y-60],[x+19,y-63],[x+46,y-38],[x+53,y+3]],'#607d6a');poly([[x-44,y-37],[x-23,y-58],[x+16,y-60],[x+8,y-36],[x-15,y-28]],'#8aa18a');poly([[x-25,y+3],[x-24,y-23],[x-10,y-37],[x+10,y-36],[x+24,y-20],[x+26,y+3]],'#172c28');rect(x-21,y-9,44,14,'#172c28');rect(x-30,y-31,9,5,'#a8b49b');rect(x+26,y-22,12,4,'#81967a');rect(x-38,y+2,75,6,'#a3976b');bush(x+51,y+6);ctx.fillStyle='#e1dfb7';ctx.font='9px monospace';ctx.textAlign='center';ctx.fillText('SALAKOOBAS',x,y-72);}
function crystal(x,y){if(artSprite('crystal',x,y+4+Math.sin(elapsed*2)*2,57)){ellipse(x,y,24,8,'#72dad028');return;}const bob=Math.sin(elapsed*2)*3;ellipse(x,y,27,9,'#7bd2cc22');poly([[x,y-37+bob],[x-13,y-18+bob],[x,y+1+bob],[x+13,y-18+bob]],'#5d9fc2');poly([[x,y-37+bob],[x-13,y-18+bob],[x,y-13+bob]],'#b6f4e2');poly([[x,y-37+bob],[x,y-13+bob],[x+13,y-18+bob]],'#80ceda');poly([[x-13,y-18+bob],[x,y-13+bob],[x,y+1+bob]],'#6dbbcc');rect(x-21,y-27+Math.sin(elapsed*3)*6,3,3,'#cbfff1');rect(x+21,y-10+Math.sin(elapsed*2)*7,2,2,'#e4ffe1');}
function fireSprite(x,y,fuel){shadow(x,y+4,22,6);for(let i=0;i<7;i++){const a=i*Math.PI*2/7;rect(x+Math.cos(a)*17-4,y+Math.sin(a)*7-3,8,6,'#a0a28c');}rect(x-13,y-3,26,5,'#795234');rect(x-8,y-7,17,4,'#b38c4e');if(fuel>0){const flick=Math.sin(elapsed*13)*3;poly([[x-10,y-3],[x-7,y-17],[x-2,y-11],[x+2,y-29-flick],[x+8,y-14],[x+11,y-3]],'#e99045');poly([[x-5,y-4],[x-2,y-19],[x+2,y-13],[x+5,y-5]],'#ffe0a0');rect(x+5+Math.sin(elapsed*2)*5,y-34-(elapsed*12%12),2,2,'#f8cf88');}}
function artWall(id,x,y,w,h){const r=artRects[id];if(!extraImage.complete||!extraImage.naturalWidth)return false;ctx.drawImage(extraImage,r[0],r[1],r[2],r[3],x,y,w,h);return true;}
function building(b){
 const x=b.x*TILE,y=b.y*TILE,cx=x+16,cy=y+16;
 if(b.type==='floor'||b.type==='stoneFloor'){
   const stone=b.type==='stoneFloor';const key=stone?'stoneFloor':'floor',r=artRects[key];if(extraImage.complete&&extraImage.naturalWidth){ctx.drawImage(extraImage,r[0],r[1],r[2],r[3],x,y,32,32);return;}rect(x,y,TILE,TILE,stone?'#959b87':'#9e804c');
   for(let i=0;i<4;i++){rect(x,y+i*8,TILE,1,stone?'#6f7a69':'#715b34');rect(x+3,y+2+i*8,25,1,stone?'#adb09b':'#bd9c5e');}
 }
 if(b.type==='wall'||b.type==='door'){
   const v=wallOrientation(b,state.buildings)==='v';
   if(b.type==='door'){
     rect(v?cx-6:x,v?y:cy-6,v?12:32,v?32:12,'#5e4b30');
     rect(v?cx-4:x+3,v?y+3:cy-4,v?8:26,v?26:8,'#b89655');rect(cx-1,cy-1,3,3,'#f0d38c');
   }else{
     const horizontal=!v||state.buildings.some(n=>['wall','door'].includes(n.type)&&n.y===b.y&&Math.abs(n.x-b.x)===1);
     const vertical=v||state.buildings.some(n=>['wall','door'].includes(n.type)&&n.x===b.x&&Math.abs(n.y-b.y)===1);
     if(horizontal){if(extraImage.complete&&extraImage.naturalWidth)rect(x,cy-5,32,6,'#795c39');if(!artWall('wallH',x,cy-15,32,24)){rect(x,cy-7,32,15,'#654b2c');rect(x,cy-11,32,12,'#a9864e');rect(x,cy-11,32,3,'#d6b36b');rect(x+3,cy-3,26,2,'#7e6037');}}
     if(vertical){if(extraImage.complete&&extraImage.naturalWidth)rect(cx-3,y,7,32,'#795c39');if(!artWall('wallV',cx-9,y,18,32)){rect(cx-6,y,14,32,'#654b2c');rect(cx-9,y,12,32,'#b69456');rect(cx-9,y,3,32,'#d9b972');rect(cx-2,y+3,2,26,'#8b6c3c');}}
     if(!extraImage.complete||!extraImage.naturalWidth){rect(cx-6,cy-10,12,12,'#c3a263');rect(cx-4,cy-9,8,3,'#e0c483');}else if(horizontal&&vertical){ellipse(cx,cy-8,4,3,'#b69a64');ellipse(cx,cy-8,2,1,'#d6b77a');}
   }
 }
 if(b.type==='fire'){if(b.fuel>0){if(!artSprite('fire',cx+Math.sin(elapsed*11)*.2,cy+9,43+Math.sin(elapsed*13)*.6))fireSprite(cx,cy,b.fuel);else{const g=ctx.createRadialGradient(cx,cy-10,3,cx,cy-10,70);g.addColorStop(0,'#ffc7661b');g.addColorStop(1,'#ffc76600');ctx.fillStyle=g;ctx.fillRect(cx-70,cy-80,140,140);}}else fireSprite(cx,cy,0);}
 if(b.type==='furnace'){if(!artSprite('furnace',cx,cy+12,55)){
   shadow(cx,cy+10,23,7);rect(x-1,y-18,34,40,'#65776b');rect(x+3,y-21,26,7,'#a0aa91');rect(x+7,y-15,18,10,'#81917e');rect(x+7,y+1,18,17,'#29372e');rect(x+5,y-1,22,3,'#a6a98b');
   if(b.fuel>0){rect(x+10,y+6,12,10,'#e39552');rect(x+13,y+3,6,11,'#f8cf7e');}rect(x+9,y-31,14,12,'#758472');}if(!(b.fuel>0))rect(cx-8,cy-5,16,10,'#23312ed9');
 }
 if(b.type==='beacon'){shadow(cx,cy+10,22,7);rect(cx-16,cy-5,32,14,'#596f5d');rect(cx-13,cy-8,26,5,'#b9a05d');rect(cx-9,cy-25,18,19,'#647d70');artSprite('crystal',cx,cy-16+Math.sin(elapsed*2)*1.3,46);const glow=ctx.createRadialGradient(cx,cy-30,2,cx,cy-30,65);glow.addColorStop(0,'#a0f0d02b');glow.addColorStop(1,'#a0f0d000');ctx.fillStyle=glow;ctx.fillRect(cx-65,cy-95,130,130);}
 if(b.type==='nest'){if(artSprite('nest',cx,cy+16,65))return;shadow(cx,y+19,23,8);rect(x-2,y-5,36,29,'#717b71');rect(x+3,y-15,26,13,'#a5b39c');rect(x+8,y-21,16,8,'#bfc5a5');rect(x+6,y+4,20,20,'#244a44');rect(x+4,y-7,24,4,'#8fd0b1');rect(x+11,y-13,10,4,'#eed186');}
}
const terrainCache={forest:null,cave:null};
function groundNoise(x,y){const n=Math.sin(x*12.9898+y*78.233)*43758.5453;return n-Math.floor(n);}
function makeGround(isCave){
 const layer=document.createElement('canvas');layer.width=W*TILE;layer.height=H*TILE;const g=layer.getContext('2d');
 for(let y=0;y<layer.height;y+=4)for(let x=0;x<layer.width;x+=4){
  const grain=groundNoise(x,y),slow=Math.sin(x*.012)*Math.cos(y*.009),shift=Math.round((grain-.5)*9+slow*5);
  if(isCave){const inside=x>=27*TILE&&x<=37*TILE&&y>=18*TILE&&y<=30*TILE;g.fillStyle=inside?`rgb(${48+shift},${63+shift},${58+shift})`:`rgb(${29+shift},${49+shift},${45+shift})`;}
  else if(water(x+2,y+2)){const edge=!water(x+10,y+2)||!water(x-6,y+2)||!water(x+2,y+10)||!water(x+2,y-6);g.fillStyle=edge?`rgb(${83+shift},${135+shift},${119+shift})`:`rgb(${49+shift},${102+shift},${103+shift})`;}
  else{
   const tx=x/TILE,ty=y/TILE,clearing=Math.hypot(tx-31,ty-29)<3.7;
   const path=(Math.abs(tx-31.2-Math.sin(ty*.45)*.22)<.85&&ty>=16&&ty<=31)||(Math.abs(ty-28.3-Math.sin(tx*.35)*.22)<.85&&tx>=31&&tx<=46);
   const shore=water(x+10,y+2)||water(x-6,y+2)||water(x+2,y+10)||water(x+2,y-6);
   if(path||clearing)g.fillStyle=`rgb(${132+shift},${125+shift},${79+shift})`;
   else if(shore)g.fillStyle=`rgb(${132+shift},${143+shift},${99+shift})`;
   else g.fillStyle=`rgb(${88+shift},${120+shift},${66+shift})`;
  }
  g.fillRect(x,y,4,4);
 }
 for(let y=8;y<layer.height-8;y+=16)for(let x=8;x<layer.width-8;x+=16){
  const n=groundNoise(x,y),px=x+Math.floor(n*10),py=y+Math.floor(groundNoise(y,x)*10);
  if(isCave){if(n>.6){g.fillStyle='#7a847453';g.fillRect(px,py,3,1);}continue;}
  if(water(px,py))continue;
  const path=(Math.abs(px/TILE-31)<1.3&&py/TILE>16&&py/TILE<32)||Math.hypot(px/TILE-31,py/TILE-29)<3.7||(Math.abs(py/TILE-28)<1.3&&px/TILE>31&&px/TILE<46);
  if(path){if(n>.65){g.fillStyle='#b7ac745e';g.fillRect(px,py,2,1);g.fillStyle='#6d674430';g.fillRect(px+1,py+1,2,1);}continue;}
  if(n<.55){g.fillStyle='#345d3a75';g.fillRect(px,py,1,4);g.fillRect(px-2,py+2,1,3);g.fillRect(px+2,py+1,1,3);g.fillStyle='#99b26355';g.fillRect(px+1,py,1,2);}
  if(n>.89){const colors=['#eacb75','#b0bdce','#dabcba'];g.fillStyle=colors[Math.floor(n*100)%3];g.fillRect(px,py-3,2,2);g.fillRect(px-2,py-2,2,2);g.fillRect(px+2,py-2,2,2);g.fillStyle='#e5dcad';g.fillRect(px,py-2,1,1);}
  else if(n>.79){g.fillStyle='#c4af6535';g.fillRect(px,py,3,1);g.fillRect(px+2,py+1,2,1);}
 }
 return layer;
}
function terrain(){
 const key=state.inCave?'cave':'forest';if(!terrainCache[key])terrainCache[key]=makeGround(state.inCave);ctx.drawImage(terrainCache[key],0,0);
 if(!state.inCave){
  // Little water highlights share the exact collision boundary rather than square water tiles.
  for(let i=0;i<36;i++){const x=365+(i*47%340),y=368+(i*73%470);if(water(x,y)&&water(x+16,y)){const alpha=.14+.07*Math.sin(elapsed*1.5+i);ctx.fillStyle=`rgba(174,218,184,${alpha})`;ctx.fillRect(x+Math.sin(elapsed*.6+i)*3,y,10+i%9,1);}}
 }
}

const tiltedCache={};
function viewPoint(x,y,h){return projectPoint(x,y,isOutside()?state.camera:0,h??(isOutside()?heightAt(x,y):0));}
function billboard(x,y,draw,height){const pos=viewPoint(x,y,height);ctx.save();ctx.translate(pos.x-x,pos.y-y);draw();ctx.restore();}
function projectedTile(x,y,color,h=heightAt((x+.5)*32,(y+.5)*32),g=ctx){const q=isOutside()?state.camera:0,points=[[x*32,y*32],[(x+1)*32,y*32],[(x+1)*32,(y+1)*32],[x*32,(y+1)*32]].map(([a,b])=>projectPoint(a,b,q,h));g.fillStyle=color;g.beginPath();points.forEach((p,i)=>i?g.lineTo(p.x,p.y):g.moveTo(p.x,p.y));g.closePath();g.fill();return points;}
function tiltedTerrain(){
 const key=state.inCave?'cave':state.interior?'room':state.camera;
 if(state.interior){for(let y=1;y<=8;y++)for(let x=1;x<=10;x++)projectedTile(x,y,(x+y)%2?'#b4915d':'#a48151',0);const a=viewPoint(32,32,0),b=viewPoint(11*32,32,0);poly([[a.x,a.y],[b.x,b.y],[b.x,b.y-50],[a.x,a.y-50]],'#58796a');rect(a.x,a.y-50,b.x-a.x,5,'#c6b680');ctx.fillStyle='#eee2b6';ctx.font='12px sans-serif';ctx.textAlign='center';ctx.fillText(tr('SINU KODU · KORRUS ')+(state.interior.level+1),6*32,4);rect(5.5*32,8*32*.62,32,4,'#ffe1a0');return;}
 if(state.inCave){ctx.save();ctx.scale(1,.62);terrain();ctx.restore();return;}
 if(!tiltedCache[key]){
  const layer=document.createElement('canvas');layer.width=W*32+100;layer.height=W*32*.62+H*32*.62+160;const g=layer.getContext('2d');const origin={x:key===1||key===2?W*32:40,y:key===2||key===3?W*32*.62+80:80};g.translate(origin.x,origin.y);
  const tiles=[];for(let y=0;y<H;y++)for(let x=0;x<W;x++){const h=heightAt((x+.5)*32,(y+.5)*32),v=projectPoint(x*32,y*32,key,h);tiles.push({x,y,h,depth:v.y+h*12});}tiles.sort((a,b)=>a.depth-b.depth);
  const polygon=(points,color)=>{g.fillStyle=color;g.beginPath();points.forEach((p,i)=>i?g.lineTo(p.x,p.y):g.moveTo(p.x,p.y));g.closePath();g.fill();};
  for(const t of tiles){const{x,y,h}=t,biome=biomeAt((x+.5)*32,(y+.5)*32),wet=water((x+.5)*32,(y+.5)*32),n=groundNoise(x,y),v=Math.round(n*10);const pts=[[x*32,y*32],[(x+1)*32,y*32],[(x+1)*32,(y+1)*32],[x*32,(y+1)*32]].map(([a,b])=>projectPoint(a,b,key,h));
   const adjacent=[[0,-1],[1,0],[0,1],[-1,0]].map(([dx,dy])=>heightAt((x+dx+.5)*32,(y+dy+.5)*32));
   if(h)for(let i=0;i<4;i++){const delta=h-adjacent[i];if(delta<=0)continue;const a=pts[i],b=pts[(i+1)%4];polygon([a,b,{x:b.x,y:b.y+delta*12},{x:a.x,y:a.y+delta*12}],biome==='desert'?'#987746':'#576342');}
   const clearing=Math.hypot(x-31,y-29)<4;polygon(pts,wet?`rgb(${45+v},${102+v},${123+v})`:biome==='desert'?`rgb(${196+v},${164+v},${101+v})`:clearing?'#a59b65':`rgb(${81+v+h*8},${113+v+h*8},${65+v})`);
   for(let i=0;i<4;i++)if(h!==adjacent[i]){const a=pts[i],b=pts[(i+1)%4];g.strokeStyle=h>adjacent[i]?(biome==='desert'?'#f5d28f':'#d6d593'):'#394d37';g.lineWidth=1.3;g.beginPath();g.moveTo(a.x,a.y);g.lineTo(b.x,b.y);g.stroke();}
   if(n>.3){const p=projectPoint((x+.3)*32,(y+.4)*32,key,h);g.fillStyle=wet?'#9bd3cc66':biome==='desert'?'#f5de9e66':'#c5d68b44';g.fillRect(p.x,p.y,wet?12:3,1);}
  }tiltedCache[key]={layer,origin};
 }const cache=tiltedCache[key];ctx.drawImage(cache.layer,-cache.origin.x,-cache.origin.y);
}
function drawWall(b){
 const items=worldItems(),x=(b.x+.5)*32,y=(b.y+.5)*32,h=isOutside()?heightAt(x,y):0;
 const rects=buildingBounds(b.open?{...b,open:false}:b,items);
 for(const box of rects){const pts=[[box.x,box.y],[box.x+box.w,box.y],[box.x+box.w,box.y+box.h],[box.x,box.y+box.h]].map(([x,y])=>viewPoint(x,y,h));
  if(b.type==='door'&&b.open){for(const p of [pts[0],pts[2]])rect(p.x-2,p.y-25,4,26,'#d0ad72');continue;}
  for(let i=0;i<4;i++){const a=pts[i],z=pts[(i+1)%4];poly([[a.x,a.y],[z.x,z.y],[z.x,z.y-24],[a.x,a.y-24]],i%2?'#9b774c':'#b99560');}
  poly(pts.map(p=>[p.x,p.y-24]),'#dfbd7d');
 }
 const v=viewPoint(x,y,h);if(b.type==='door'&&!b.open){rect(v.x-6,v.y-21,12,23,'#725337');rect(v.x+2,v.y-10,2,3,'#ffe4a3');}
 if(b.type==='window'){rect(v.x-7,v.y-20,14,13,'#bce4df');rect(v.x-1,v.y-20,2,13,'#73563d');rect(v.x-7,v.y-14,14,2,'#73563d');}
}
function smallProp(b){if(['wall','door','window'].includes(b.type)){drawWall(b);return;}const x=(b.x+.5)*32,y=(b.y+.5)*32;
 if(['floor','stoneFloor','ceiling','roof'].includes(b.type)){const h=isOutside()?heightAt(x,y):0;projectedTile(b.x,b.y,b.type==='stoneFloor'?'#a5b0a0':b.type==='roof'?'#b46e56aa':b.type==='ceiling'?'#e3d49e55':'#c29e6d',h);return;}
 billboard(x,y,()=>{
 if(['chest','table','bed','stairs'].includes(b.type)){
  shadow(x,y,16,5);if(b.type==='chest'){rect(x-14,y-20,28,23,'#775134');rect(x-14,y-23,28,8,'#c29553');rect(x-12,y-12,24,2,'#d5ae66');rect(x-2,y-14,4,7,'#eee0a0');}
  if(b.type==='table'){rect(x-13,y-13,3,15,'#6d4e34');rect(x+10,y-13,3,15,'#6d4e34');rect(x-17,y-18,34,9,'#d3ac6e');}
  if(b.type==='bed'){rect(x-13,y-26,26,30,'#835a3a');rect(x-11,y-22,22,23,'#8cb8aa');rect(x-10,y-24,20,8,'#f3e4bc');}
  if(b.type==='stairs')for(let i=0;i<5;i++){rect(x-15+i*3,y-i*6-4,23,7,'#c3a46d');rect(x-15+i*3,y-i*6+1,23,3,'#8b6c46');}
 }else if(b.type==='garden'){
  rect(x-17,y-7,34,14,'#b28a52');rect(x-14,y-8,28,10,'#5c4932');if(b.crop){const ready=cropProgress(state,b)>=1,progress=cropProgress(state,b);for(let i=0;i<3;i++){rect(x-10+i*9,y-7-progress*12,2,8+progress*10,'#9ec47d');ellipse(x-9+i*9,y-8-progress*12,4,3,b.crop==='magicFlower'?'#d8aee6':ready?'#efd28b':'#a0c77a');}if(ready){ctx.fillStyle='#ffe8a4';ctx.font='9px sans-serif';ctx.textAlign='center';ctx.fillText(tr('SAAGIKÜPS'),x,y-29);}}
 }else if(b.type==='boat'){boatSprite(x,y);}
 else if(/Lamp$/.test(b.type)){
  const mounted=worldItems().some(n=>n.x===b.x&&n.y===b.y&&n.type==='table'),height=b.type==='yardLamp'?42:b.type==='wallLamp'?30:mounted?34:20;rect(x-2,y-height,4,height,'#9b8057');ellipse(x,y-height,8,10,b.type==='crystalLamp'?'#a6eee9':'#ffe4a3');const glow=ctx.createRadialGradient(x,y-height,2,x,y-height,60);glow.addColorStop(0,b.type==='crystalLamp'?'#a8f0e84a':'#ffe49c40');glow.addColorStop(1,'#ffe49c00');ctx.fillStyle=glow;ctx.fillRect(x-60,y-height-60,120,120);
 }else if(b.type==='window'){rect(x-16,y-30,32,30,'#ab8958');rect(x-8,y-26,16,17,'#b9ddd5');rect(x-1,y-26,2,17,'#71593c');rect(x-8,y-19,16,2,'#71593c');}
 else if(b.type==='door'&&b.open){rect(x-16,y-28,5,30,'#d2ac72');rect(x+11,y-28,5,30,'#d2ac72');rect(x-16,y-30,32,5,'#d2ac72');}
 else building(b);
 });
}
function looseSprite(r){const x=r.x,y=r.y;shadow(x,y+2,7,2);if(r.type==='branch'){ctx.strokeStyle='#513b25';ctx.lineWidth=4;ctx.beginPath();ctx.moveTo(x-8,y+1);ctx.lineTo(x+8,y-5);ctx.moveTo(x,y-2);ctx.lineTo(x+2,y-8);ctx.stroke();ctx.strokeStyle='#dcbd82';ctx.lineWidth=2;ctx.beginPath();ctx.moveTo(x-8,y);ctx.lineTo(x+8,y-6);ctx.stroke();}else if(r.type==='pebble'){poly([[x-7,y],[x-3,y-6],[x+3,y-7],[x+7,y-2],[x+4,y+2]],'#b9c7bd');rect(x-3,y-6,6,2,'#e2e2ca');}else{ellipse(x,y,11,4,'#e9c58a');ellipse(x+2,y-3,6,4,'#f1d49b');}}
function boatSprite(x,y){shadow(x,y+2,25,7);poly([[x-27,y-8],[x-19,y+7],[x+17,y+7],[x+28,y-8]],'#b88a52');rect(x-20,y-7,40,4,'#e3bb7d');rect(x-3,y-6,6,12,'#7c5c3b');const paddle=Math.sin(elapsed*4)*5;ctx.strokeStyle='#e8c88a';ctx.lineWidth=3;ctx.beginPath();ctx.moveTo(x-15,y-3);ctx.lineTo(x-30,y+9+paddle);ctx.moveTo(x+15,y-3);ctx.lineTo(x+30,y+9-paddle);ctx.stroke();}
function predatorSprite(a){const x=a.x,y=a.y;if(a.type==='skeleton'){shadow(x,y,10,4);rect(x-5,y-18,10,13,'#e4dfc7');rect(x-7,y-31,14,13,'#eee9d0');rect(x-4,y-27,3,4,'#4b6265');rect(x+2,y-27,3,4,'#4b6265');rect(x-3,y-20,6,2,'#b48b61');for(const dx of[-4,3]){rect(x+dx,y-5,3,8,'#e4dfc7');rect(x+dx*2,y-18,3,12,'#e4dfc7');}ellipse(x+10,y-29,7,4,'#d7b878');return;}
 const bear=a.type==='bear',color=bear?'#9f7957':'#98a9a5',w=bear?31:27;shadow(x,y,20,6);rect(x-w/2,y-25,w,22,color);ellipse(x+10,y-27,bear?12:9,bear?12:9,color);for(const dx of[-9,8])rect(x+dx,y-5,6,9,color);ellipse(x+4,y-36,4,5,color);ellipse(x+16,y-36,4,5,color);rect(x+13,y-29,3,3,'#263b3b');ellipse(x+20,y-23,5,4,bear?'#d5b78c':'#dce2cf');rect(x+22,y-25,3,3,'#35494a');if(!bear)poly([[x-13,y-20],[x-26,y-25],[x-19,y-11]],color);}
function npcSprite(n){const x=n.x,y=n.y;shadow(x,y,12,4);rect(x-9,y-23,18,20,{ranger:'#749c76',miner:'#8a9ca4',trader:'#b599b5'}[n.id]);rect(x-6,y-36,12,14,'#e2c499');rect(x-11,y-37,22,4,'#d1b26c');rect(x-7,y-43,14,8,'#bda064');rect(x-4,y-32,2,3,'#364749');rect(x+3,y-32,2,3,'#364749');rect(x-3,y-26,7,1,'#986d4d');rect(x-7,y-4,5,7,'#5c6250');rect(x+3,y-4,5,7,'#5c6250');ctx.fillStyle='#fff0bf';ctx.font='8px sans-serif';ctx.textAlign='center';ctx.fillText(n.name,x,y-49);}
function houseSprite(h){
 const corners=[[h.minX*32,h.minY*32],[(h.maxX+1)*32,h.minY*32],[(h.maxX+1)*32,(h.maxY+1)*32],[h.minX*32,(h.maxY+1)*32]].map(([x,y])=>viewPoint(x,y));
 for(let i=0;i<4;i++){const a=corners[i],b=corners[(i+1)%4];poly([[a.x,a.y],[b.x,b.y],[b.x,b.y-32],[a.x,a.y-32]],i%2?'#a77f51':'#c6a06a');}
 const eaves=corners.map(p=>({x:p.x,y:p.y-33})),ra={x:(eaves[0].x+eaves[1].x)/2,y:(eaves[0].y+eaves[1].y)/2-27},rb={x:(eaves[2].x+eaves[3].x)/2,y:(eaves[2].y+eaves[3].y)/2-27};
 const points=arr=>arr.map(p=>[p.x,p.y]);poly(points([eaves[0],eaves[1],ra]),'#dbba7d');poly(points([eaves[2],eaves[3],rb]),'#b48b58');poly(points([eaves[0],ra,rb,eaves[3]]),'#a35b4d');poly(points([ra,eaves[1],eaves[2],rb]),'#c87d5b');ctx.strokeStyle='#e8b282';ctx.lineWidth=3;ctx.beginPath();ctx.moveTo(ra.x,ra.y);ctx.lineTo(rb.x,rb.y);ctx.stroke();

 const door=viewPoint((h.door.x+.5)*32,(h.door.y+.5)*32);rect(door.x-8,door.y-25,16,26,'#5a4935');rect(door.x+3,door.y-12,3,3,'#ffe0a1');
 for(const b of state.buildings.filter(b=>b.type==='window'&&h.tiles.some(t=>t.x===b.x&&t.y===b.y))){const p=viewPoint((b.x+.5)*32,(b.y+.5)*32);rect(p.x-7,p.y-24,14,15,'#c9e3d5');rect(p.x-1,p.y-24,2,15,'#8a6b47');}
}
function draw(){
 const p=state.player,pv=viewPoint(p.x,p.y);cam.x=Math.round(pv.x-canvas.width/2);cam.y=Math.round(pv.y-canvas.height/2+20);
 ctx.fillStyle=state.inCave?'#192d2d':'#193b38';ctx.fillRect(0,0,canvas.width,canvas.height);ctx.save();ctx.translate(-cam.x,-cam.y);tiltedTerrain();
 const sprites=[],push=(x,y,fn)=>{const v=viewPoint(x,y);if(v.x<cam.x-130||v.x>cam.x+canvas.width+130||v.y<cam.y-100||v.y>cam.y+canvas.height+150)return;sprites.push({depth:v.y+(isOutside()?heightAt(x,y)*12:0),draw:()=>billboard(x,y,fn)});};
 const homes=findHouses(state.buildings),insideHome=b=>homes.some(h=>h.tiles.some(t=>t.x===b.x&&t.y===b.y));
 if(isOutside()){
  for(const b of state.buildings.filter(b=>!insideHome(b)&&['floor','stoneFloor'].includes(b.type)))smallProp(b);
  push(base.x,base.y,bench);push(cave.x,cave.y,caveSprite);
  npcData.forEach(n=>push(n.x,n.y,()=>npcSprite(n)));
  for(const h of homes){const v=viewPoint((h.minX+h.maxX+1)*16,(h.minY+h.maxY+1)*16);sprites.push({depth:v.y+20,draw:()=>houseSprite(h)});}
  for(const b of state.buildings.filter(b=>!insideHome(b)&&!['floor','stoneFloor'].includes(b.type)&&!(b.type==='boat'&&state.boatId===(b.id||('boat:'+b.x+':'+b.y))))){const pos=viewPoint((b.x+.5)*32,(b.y+.5)*32);sprites.push({depth:pos.y+heightAt((b.x+.5)*32,(b.y+.5)*32)*12,draw:()=>smallProp(b)});}
  for(const a of animals)push(a.x,a.y,()=>a.type==='rabbit'?rabbit(a):a.type==='deer'?deer(a):predatorSprite(a));
  for(const z of zombies)push(z.x,z.y,()=>zombie(z));
  if(state.meteorArrived){push(meteor.x,meteor.y,()=>rock(meteor.x,meteor.y,true));if(!state.alienFriend)push(meteor.x+30,meteor.y+30,()=>alien(meteor.x+30,meteor.y+30));}
  // Ruins, a friendly bear den and oasis landmark make the new regions discoverable.
  for(const[x,y]of[[48,10],[51,10],[51,7]])push(x*32,y*32,()=>{rect(x*32-12,y*32-38,24,38,'#c3b28c');rect(x*32-15,y*32-40,30,8,'#e2cca0');rect(x*32-8,y*32-25,5,7,'#8d8969');});
  push(39*32,12*32,()=>{ellipse(39*32,12*32-5,30,19,'#8d8970');ellipse(39*32,12*32,16,16,'#4e5945');});
  push(50*32,16*32,()=>{ctx.fillStyle='#ebdda2';ctx.font='9px sans-serif';ctx.textAlign='center';ctx.fillText(tr('OAAS'),50*32,16*32-20);});
  push(61*32,25*32,()=>{const x=61*32,y=25*32+Math.sin(elapsed)*3;ellipse(x,y,48,20,'#8cb8cb');ellipse(x+29,y-7,24,19,'#a0cbd6');ellipse(x+39,y-12,3,3,'#254a5c');poly([[x-39,y],[x-62,y-17],[x-57,y+4],[x-66,y+16],[x-40,y+7]],'#82afc3');ctx.strokeStyle='#d5edf0';ctx.lineWidth=2;ctx.beginPath();ctx.arc(x+38,y-5,7,0,Math.PI);ctx.stroke();rect(x+10,y-32,2,10,'#c5eef0');});
 }else if(state.inCave){for(const b of bats.filter(b=>b.hp>0))push(b.x,b.y,()=>batSprite(b));if(!state.crystalFound)push(32*32,20*32,()=>crystal(32*32,20*32));}
 else for(const b of worldItems()){const v=viewPoint((b.x+.5)*32,(b.y+.5)*32,0);sprites.push({depth:v.y,draw:()=>smallProp(b)});}
 if(!state.interior)for(const r of resources.filter(r=>!!r.inCave===state.inCave)){
  if(r.alive)push(r.x,r.y,()=>{if(forageDefs[r.type]){looseSprite(r);if(started&&Math.hypot(r.x-p.x,r.y-p.y)<150){ctx.strokeStyle='#f3dfa2';ctx.lineWidth=1;ctx.beginPath();ctx.ellipse(r.x,r.y,10,4,0,0,7);ctx.stroke();ctx.fillStyle='#ffe9ac';ctx.font='10px sans-serif';ctx.textAlign='center';ctx.fillText('✦',r.x,r.y-10-Math.sin(elapsed*3+r.id)*2);}}else if(r.type==='wood')tree(r.x,r.y,r.id%3===0?1:0);else if(r.type==='cactus'){rect(r.x-4,r.y-38,8,40,'#78a777');rect(r.x-15,r.y-26,12,6,'#78a777');rect(r.x-15,r.y-35,5,14,'#78a777');rect(r.x+2,r.y-19,14,6,'#78a777');rect(r.x+11,r.y-30,5,16,'#78a777');ellipse(r.x,r.y-40,4,3,'#f0c5b1');}else if(['stone','ironOre','copperOre'].includes(r.type)){if(!artSprite(r.type==='stone'?'rock':r.type,r.x,r.y+5,36))rock(r.x,r.y);}else if(r.type==='herbs')herb(r.x,r.y);else bush(r.x,r.y);});else if(r.type==='wood'&&!r.removed)push(r.x,r.y,()=>artSprite('stump',r.x,r.y+5,20));
 }
 for(const d of state.drops.filter(d=>!!d.inCave===state.inCave&&(d.room||null)===(state.interior?.id||null)&&(d.level||0)===(state.interior?.level||0)))push(d.x,d.y,()=>{ellipse(d.x,d.y,10,7,'#ffe39e44');ctx.font='13px sans-serif';ctx.textAlign='center';ctx.fillStyle='#ffe7a5';ctx.fillText(icons[d.id]||'✦',d.x,d.y);});
 if(state.alienFriend&&!state.interior&&state.alien.inCave===state.inCave)push(state.alien.x,state.alien.y,()=>alien(state.alien.x,state.alien.y));
 push(p.x,p.y,()=>{if(state.boatId)boatSprite(p.x,p.y+4);ctx.save();ctx.translate(0,-Math.sin((state.jump||0)/.65*Math.PI)*24);if(invulnerable>0&&Math.floor(elapsed*10)%2===0)ctx.globalAlpha=.5;simm(p.x,p.y);ctx.restore();});
 sprites.sort((a,b)=>a.depth-b.depth);for(const s of sprites)s.draw();
 if(currentTarget&&!paused&&!buildType){const t=currentTarget;billboard(t.x,t.y,()=>{ctx.strokeStyle='#ffe0a0';ctx.lineWidth=1.5;ctx.beginPath();ctx.ellipse(t.x,t.y+2,19,6,0,0,7);ctx.stroke();ctx.fillStyle='#ffe5ad';ctx.font='9px sans-serif';ctx.textAlign='center';ctx.fillText('A / E',t.x,t.y-42);});}
 if(started&&!paused){const start=viewPoint(p.x,p.y),end=viewPoint(p.x+aim.x*35,p.y+aim.y*35);ctx.strokeStyle='#ffe2a6';ctx.lineWidth=2;ctx.beginPath();ctx.moveTo(start.x,start.y-10);ctx.lineTo(end.x,end.y-10);ctx.stroke();if(charge){ctx.fillStyle='#ffe2a6';ctx.fillRect(start.x-18,start.y+15,36*bowStats(state,charge.time).power,4);}}
 for(const a of arrows.filter(a=>a.inCave===state.inCave)){const v=viewPoint(a.x,a.y),tail=viewPoint(a.x-a.vx*.025,a.y-a.vy*.025);ctx.strokeStyle='#ffe4ad';ctx.lineWidth=2;ctx.beginPath();ctx.moveTo(tail.x,tail.y-8);ctx.lineTo(v.x,v.y-8);ctx.stroke();}
 if(fishing){const v=viewPoint(fishing.x,fishing.y);ctx.strokeStyle='#f4dfa0';ctx.beginPath();ctx.moveTo(pv.x,pv.y-17);ctx.lineTo(v.x,v.y);ctx.stroke();ellipse(v.x,v.y,3,2,'#f7bb77');}
 if(meteorFall){const v=viewPoint(meteor.x,meteor.y),t=meteorFall.time/1.5;ctx.strokeStyle='#ffe6a2';ctx.lineWidth=4;ctx.beginPath();ctx.moveTo(v.x-(1-t)*180-20,v.y-(1-t)*240-35);ctx.lineTo(v.x-(1-t)*180,v.y-(1-t)*240);ctx.stroke();}
 for(const a of particles){const v=viewPoint(a.x,a.y);ctx.globalAlpha=Math.max(0,a.life/.7);rect(v.x,v.y,3,3,a.color);}ctx.globalAlpha=1;
 for(const item of pickups){const v=viewPoint(item.x,item.y);ctx.globalAlpha=Math.min(1,item.life*2);ctx.font='bold 10px sans-serif';ctx.textAlign='center';ctx.fillStyle='#fff0b0';ctx.strokeStyle='#122820';ctx.lineWidth=3;const text=`+${item.n} ${names[item.id]}`;ctx.strokeText(text,v.x,v.y-26-(1.5-item.life)*18);ctx.fillText(text,v.x,v.y-26-(1.5-item.life)*18);}ctx.globalAlpha=1;
 if(buildType){const point=buildPoint(),loc=placement(point.x,point.y);ctx.globalAlpha=.6;smallProp({x:loc.gx,y:loc.gy,type:buildType});ctx.globalAlpha=1;const pts=projectedTile(loc.gx,loc.gy,loc.valid?'#cce69b55':'#eb9b8e66',isOutside()?heightAt(loc.cx,loc.cy):0);ctx.strokeStyle=loc.valid?'#daf7a4':'#ffa997';ctx.lineWidth=2;ctx.beginPath();pts.forEach((p,i)=>i?ctx.lineTo(p.x,p.y):ctx.moveTo(p.x,p.y));ctx.closePath();ctx.stroke();}
 ctx.restore();const dark=state.interior?0:state.inCave?.25:state.time>=300?.35:0;if(dark){ctx.fillStyle=`rgba(8,20,38,${dark})`;ctx.fillRect(0,0,canvas.width,canvas.height);}
 for(const b of worldItems().filter(b=>/Lamp$/.test(b.type)||b.type==='fire'&&b.fuel>0)){const point=viewPoint((b.x+.5)*32,(b.y+.5)*32),x=point.x-cam.x,y=point.y-cam.y-18,g=ctx.createRadialGradient(x,y,2,x,y,70);g.addColorStop(0,b.type==='crystalLamp'?'#b4f5ed44':'#ffe6ac38');g.addColorStop(1,'#ffe6ac00');ctx.fillStyle=g;ctx.fillRect(x-70,y-70,140,140);}
}

function resize(){const r=canvas.getBoundingClientRect(),scale=r.height>=1400?3:2;canvas.width=Math.max(1,Math.round(r.width/scale));canvas.height=Math.max(1,Math.round(r.height/scale));ctx.imageSmoothingEnabled=false;}
new ResizeObserver(resize).observe(canvas);resize();refresh();
$('startButton').disabled=true;$('newGameButton').disabled=true;
Promise.allSettled([atlasImage.decode(),heroImage.decode(),extraImage.decode()]).then(()=>{updateHUD();draw();paintTitlePortrait();assetsReady=true;document.querySelector('.game-shell').dataset.ready='true';$('startButton').disabled=false;$('newGameButton').disabled=false;$('loadStatus').textContent=tr('WASD + hiir või Xboxi pult · A alustab · Y uus mäng');});
function frame(time){const dt=last?Math.min((time-last)/1000,.05):0;last=time;const pad=readPad();if(!document.hidden)tickWhale(dt);if(!document.hidden){if(!paused&&started&&assetsReady){update(dt,pad);draw();}}updateAudio({moving:state.player.walk>0,night:state.time>=300,inCave:state.inCave,nearFire:!!nearFire()?.fuel,paused:paused||!started||!!death||document.hidden});requestAnimationFrame(frame);}requestAnimationFrame(frame);
