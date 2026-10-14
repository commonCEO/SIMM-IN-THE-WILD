import { toggleAudio, sound, updateAudio, setVolume } from './audio.js';
import { freshState, recipes, skills, names, icons, tools, pay, canPay, gainXP, canUpgrade, upgrade, maxHealth, advanceTime, addItem, usedSlots, STACK_SIZE, cook, dropItem, bowStats, inWater, wallOrientation } from './model.js';
const $ = id => document.getElementById(id);
const canvas = $('game'), ctx = canvas.getContext('2d');
const TILE=32, W=64, H=48;
const base={x:31*TILE,y:29*TILE}, cave={x:33*TILE,y:16*TILE}, meteor={x:45*TILE,y:27*TILE};
let seed=1742;
function rand(){seed=(seed*1664525+1013904223)>>>0;return seed/4294967296;}
const state=freshState();
state.player={x:base.x,y:base.y+64,face:1,walk:0};
let saveFound=false;
try {
  const saved=JSON.parse(localStorage.getItem('simm-save-v1')||'null');
  if(saved?.state?.inventory&&Number.isFinite(saved.state.player?.x)){
    Object.assign(state,saved.state);
    state.inventory={...freshState().inventory,...saved.state.inventory};
    state.skills={...freshState().skills,...saved.state.skills};
    state.drops=state.drops||[];state.stumpsRemoved=state.stumpsRemoved||[];
    state.alienFollowing=state.alienFollowing??true;
    saveFound=true;
  }
}catch{}
let started=false,paused=false,last=0,elapsed=0,cam={x:0,y:0},keys={},tool=0,buildType=null,rotation='auto',toastTime=0,actionCooldown=0,autosave=0,padPrevious={},padMoveAt=0,menuIndex=0;
let aim={x:1,y:0},charge=null,invulnerable=0,damageFlash=0,death=null,fishing=null,currentTarget=null;
const particles=[],resources=[],animals=[],zombies=[],bats=[],arrows=[];
const water=inWater;
for(let i=0;i<290;i++){
  const x=(3+rand()*(W-6))*TILE,y=(3+rand()*(H-6))*TILE;
  if(Math.hypot(x-base.x,y-base.y)<150||Math.hypot(x-cave.x,y-cave.y)<110||Math.hypot(x-meteor.x,y-meteor.y)<100||water(x,y))continue;
  // Keep the original forest layout so version 0.1 saved resource IDs still match.
  const type=rand()<.60?'wood':rand()<.48?'stone':rand()<.7?'berries':'herbs';
  resources.push({id:i,x,y,type,hp:3,alive:!state.depleted?.includes(i),removed:state.stumpsRemoved.includes(i)});
}
for(const [id,x,y,type]of[[500,-95,60,'wood'],[501,98,45,'stone'],[502,-65,110,'berries'],[503,130,-35,'wood'],[504,-120,-45,'stone'],[505,65,150,'herbs']])resources.push({id,x:base.x+x,y:base.y+y,type,hp:3,alive:!state.depleted?.includes(id),removed:state.stumpsRemoved.includes(id)});
for(let i=0;i<14;i++){
  let x,y;
  do{x=(12+rand()*38)*TILE;y=(12+rand()*25)*TILE;}while(water(x,y)||water(x-8,y)||water(x+8,y)||water(x,y-6)||water(x,y+6));
  animals.push({x,y,type:i%3?'rabbit':'deer',dir:rand()*6.28,timer:rand()*3,step:rand()*6,hp:i%3?1:3});
}
if(Array.isArray(state.wildlife)){animals.length=0;for(const a of state.wildlife){if(Number.isFinite(a.x)&&Number.isFinite(a.y)&&['rabbit','deer'].includes(a.type)&&!water(a.x,a.y))animals.push({...a});}}
for(let i=0;i<3;i++)bats.push({x:(29+i*2)*TILE,y:(21+i%3)*TILE,hp:1,phase:rand()*6.28,hit:0});
for(const [id,x,y,type]of[[600,29,22,'ironOre'],[601,35,23,'copperOre'],[602,28,26,'ironOre'],[603,36,27,'copperOre'],[604,28,19,'stone']])resources.push({id,x:x*TILE,y:y*TILE,type,hp:3,inCave:true,alive:!state.depleted?.includes(id)});
if(state.alienFriend&&!state.alien)state.alien={x:state.player.x+35,y:state.player.y+25,inCave:state.inCave};
function notify(text){$('toast').textContent=text;$('toast').classList.remove('hidden');toastTime=4;}
function save(){try{state.wildlife=animals.map(a=>({...a}));state.depleted=resources.filter(r=>!r.alive).map(r=>r.id);state.stumpsRemoved=resources.filter(r=>r.removed).map(r=>r.id);localStorage.setItem('simm-save-v1',JSON.stringify({version:2,state}));}catch{}}
function start(){started=true;if(state.time>=300)spawnZombies();$('startOverlay').classList.add('hidden');canvas.focus();notify(saveFound?'Tere tagasi, Simm!':'Metsakristall ootab põhja pool. A / E suhtleb; Y / B ehitab.');refresh();}
$('startButton').onclick=start;
if(saveFound){$('startButton').textContent='Jätka seiklust →';document.querySelector('.intro-card p').textContent='Sinu mets, varud ja ehitised on alles. Versioon 0.2 ootab uut seiklust.';}
$('audioButton').onclick=async()=>{try{const enabled=await toggleAudio();setVolume(Number($('volume').value)/100);$('audioButton').textContent=enabled?'♫ Heli sees':'♫ Heli väljas';$('audioButton').setAttribute('aria-pressed',String(enabled));}catch{notify('Brauser ei saanud heli käivitada.');}};
$('volume').oninput=()=>setVolume(Number($('volume').value)/100);
$('fullscreenButton').onclick=async()=>{try{if(document.fullscreenElement)await document.exitFullscreen();else await document.documentElement.requestFullscreen();}catch{notify('Kasuta brauseri täisekraani klahvi F11.');}};
$('helpButton').onclick=()=>openModal('help');$('skillsButton').onclick=()=>openModal('skills');$('craftButton').onclick=()=>openModal('craft');$('buildButton').onclick=()=>openModal('build');$('bagButton').onclick=()=>openModal('bag');$('eatButton').onclick=eat;
function closeModal(){if($('modal').open)$('modal').close();paused=false;canvas.focus();}
$('closeModal').onclick=closeModal;$('modal').addEventListener('cancel',()=>{paused=false;});
$('modal').addEventListener('click',e=>{if(e.target===$('modal')){const r=$('modal').getBoundingClientRect();if(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom)closeModal();}});
function menuButtons(){return [...$('modalContent').querySelectorAll('button:not(:disabled)')];}
function focusMenu(index){const buttons=menuButtons();if(!buttons.length){$('closeModal').focus();return;}menuIndex=(index+buttons.length)%buttons.length;for(const b of $('modal').querySelectorAll('.pad-focused'))b.classList.remove('pad-focused');buttons[menuIndex].classList.add('pad-focused');buttons[menuIndex].focus();buttons[menuIndex].scrollIntoView({block:'nearest'});}
function refresh(){
  const hotbar=$('hotbar');hotbar.replaceChildren();
  tools.forEach((t,i)=>{const b=document.createElement('button');b.className='tool-slot'+(tool===i?' active':'')+(!state.tools.includes(t.id)?' locked':'');b.title=t.name;b.setAttribute('aria-label',t.name);b.setAttribute('aria-pressed',String(tool===i));b.innerHTML=`<kbd>${i+1}</kbd>${t.icon}`;b.onclick=()=>selectTool(i);hotbar.append(b);});
  $('bagCount').textContent=`${usedSlots(state)}/${state.bagSlots}`;
  $('pointsLabel').textContent=`${state.points} OSKUSPUNKTI`;
  $('skillsButton').classList.toggle('has-points',state.points>0);
  $('skillSubtitle').textContent=`Tase ${state.level} · K / Menu`;
  $('questText').textContent=!state.crystalFound?'Leia metsa südames peituv kristall':!state.alienFriend?'Leia ida poolt tähekülaline':'Ehita oma kodu · avasta · arene';
}
function costFor(r){return Object.fromEntries(Object.entries(r.cost).map(([k,v])=>[k,Math.max(1,Math.ceil(v*(1-.1*(state.skills.craft||0))))]));}
function nearBench(){return !state.inCave&&Math.hypot(state.player.x-(base.x+35),state.player.y-base.y)<46;}
function nearStation(type){return !state.inCave&&state.buildings.find(b=>b.type===type&&Math.hypot(state.player.x-(b.x+.5)*TILE,state.player.y-(b.y+.5)*TILE)<48);}
function nearFire(){return nearStation('fire');}
function openModal(kind){
  if(death)return;
  charge=null;fishing=null;paused=true;keys={};
  const modal=$('modal'),content=$('modalContent');modal.classList.toggle('wide',kind==='skills');content.replaceChildren();
  $('modalEyebrow').textContent={skills:`TASE ${state.level}`,craft:'MEISTERDAMISLAUD',build:'OMA KODU, OMA REEGLID',bag:'KÕIK VAJALIK KAASAS',fire:'LÕKKE ÄÄRES',furnace:'MAAGIST METALLIKS',help:'VÄIKE SPIKKER'}[kind];
  $('modalTitle').textContent={skills:'Vali oma rada',craft:'Valmista midagi head',build:'Ehita oma kodu',bag:'Sinu seljakott',fire:'Soe tuli, hea toit',furnace:'Sulatusahi',help:'Seiklus algab siit'}[kind];
  if(kind==='bag'){
    content.innerHTML=`<p class="build-note">${usedSlots(state)} / ${state.bagSlots} pesa · Virnas kuni ${STACK_SIZE} eset. Vali ese, et üks maha panna. Ese püsib 10 mänguminutit ja selle saab A / E-ga uuesti üles korjata.</p>`;
    const grid=document.createElement('div');grid.className='bag-grid';
    for(const[k,v]of Object.entries(state.inventory))for(let n=v;n>0;n-=STACK_SIZE){const slot=document.createElement('button');slot.className='inv-slot';slot.title=`${names[k]} · pane üks maha`;slot.setAttribute('aria-label',`Pane maha: ${names[k]}`);slot.innerHTML=`${icons[k]}<small>${Math.min(n,STACK_SIZE)}</small>`;slot.onclick=()=>{dropItem(state,k,state.player.x+aim.x*20,state.player.y+aim.y*20,state.inCave);refresh();save();openModal('bag');};grid.append(slot);}
    while(grid.children.length<state.bagSlots){const d=document.createElement('div');d.className='inv-slot empty';grid.append(d);}content.append(grid);
  }else if(kind==='skills'){
    content.innerHTML=`<div class="skill-points">✦ ${state.points} oskuspunkti — vali, millises suunas arened</div>`;
    const tree=document.createElement('div');tree.className='skill-tree';
    for(const branch of ['combat','craft','gather','star']){
      const column=document.createElement('div');column.className='skill-branch';const children=document.createElement('div');children.className='tree-children';
      for(const s of skills.filter(s=>s.branch===branch)){
        const rank=state.skills[s.id]||0,locked=s.requires&&!state.skills[s.requires],card=document.createElement('div');
        card.className='skill-node'+(rank?' owned':'')+(canUpgrade(state,s.id)?' available':'')+(locked?' locked':'');
        card.innerHTML=`<span>${s.icon}</span><strong>${s.name} ${rank}/${s.max}</strong><p>${s.description}</p><button ${!canUpgrade(state,s.id)?'disabled':''}>${locked?'Õpi kõigepealt põhioskus':rank>=s.max?'Õpitud':'Õpi · 1 punkt'}</button>`;
        card.querySelector('button').onclick=()=>{if(upgrade(state,s.id)){sound('craft');refresh();save();openModal('skills');}};if(s.requires)children.append(card);else column.append(card);
      }column.append(children);tree.append(column);
    }content.append(tree);
  }else if(kind==='help'){
    content.innerHTML=`<div class="help-copy"><p><strong>Xbox:</strong> vasak kang liigub, parem kang sihib. A suhtleb ja kinnitab. View (nupp vasaku kangi kõrval) avab seljakoti. Y avab ehitamise. X / RT kasutab tööriista; hoia RT all ja vabasta, et vibuga lasta. B käsib Nupsil oodata või kaasa tulla. LT sööb, LB/RB valib tööriista, Menu avab oskused. Menüüdes vali vasaku kangi või ristnuppudega; A kinnitab, B sulgeb.</p><p><strong>Klaviatuur:</strong> WASD liigub; E tegutseb; tühik / hiir kasutab tööriista (vibu: hoia ja vabasta). I seljakott, C meisterda lähedal laua juures, B ehita, K oskused, R söö, T tulnuka käsk. Ehitamisel Q või puldi X pöörab seina; hiireklõps / A paigutab ja Esc / B lõpetab.</p><p><strong>Kodu:</strong> ruudustik ja roheline eelvaade näitavad paigutust. Seinad ühenduvad naabritega ja uks sulgeb turvalise toa. Kirvega saad seina lõhkuda; pool kulunud puidust jääb maha. Ka kändudest saab veidi puitu.</p><p><strong>Uued varud:</strong> koopas leidub raua- ja vasemaaki. Ehita ahi, lisa puitu ning sulata kange või valmista kiviplaate. Õngega saad veekogu kaldal kala püüda. Laetud nool lendab kaugemale ja tabab ainult sihitud suunas. Loomad annavad liha ilma veriste efektideta.</p><p><strong>Nups:</strong> B / T jätab ta ootama või kutsub lähedalt kaasa. Kaasas olev Nups aeglustab vastaseid. Pesaga baasi jäetud Nups kogub marju. Maailm salvestub automaatselt sellesse brauserisse.</p><button id="resetSave">Alusta uut seiklust</button></div>`;
    $('resetSave').onclick=()=>{if(confirm('Kas alustame uut seiklust?')){localStorage.removeItem('simm-save-v1');location.reload();}};
  }else if(kind==='fire'||kind==='furnace'){
    const station=nearStation(kind);
    if(!station){content.innerHTML='<p class="build-note">Mine jaama kõrvale, et seda kasutada.</p>';}
    else{
      content.innerHTML=`<div class="station-fuel"><p class="build-note">Kütust: ${Math.ceil(station.fuel||0)} sekundit · 1 puit = ${state.skills.smelter?4:2} minutit.</p><button id="fuelButton" ${state.inventory.wood<1?'disabled':''}>Lisa 1 puit · süüta tuli</button></div>`;
      $('fuelButton').onclick=()=>{if(pay(state,{wood:1})){station.fuel=(station.fuel||0)+120*(state.skills.smelter?2:1);refresh();save();openModal(kind);}};
      for(const r of recipes.filter(r=>kind==='fire'?r.cook:r.smelt)){
        const row=recipeRow(r,r.cost,!(station.fuel>0)||!canPay(state,r.cost),kind==='fire'?'Küpseta':'Sulata');
        row.querySelector('button').onclick=()=>{if(station.fuel>0&&cook(state,r)){station.fuel=Math.max(0,station.fuel-5);gainXP(state,8);sound('craft');refresh();save();openModal(kind);notify(`${r.name} valmis!`);}else notify('Seljakotis pole ruumi.');};content.append(row);
      }
    }
  }else if(kind==='craft'&&!nearBench())content.innerHTML='<p class="build-note">Mine meisterdamislaua kõrvale. Laua ümber ilmub kollane rõngas, kui see on käeulatuses.</p>';
  else{
    if(kind==='build')content.innerHTML='<p class="build-note">Vali osa. Seejärel sihi maapinda: roheline eelvaade lubab ehitada, punane näitab takistust. Q / X pöörab seina. A / klõps paigutab. Seinad ühenduvad automaatselt; suletud tuba koos uksega kaitseb öösel.</p>';
    for(const r of recipes.filter(r=>!r.cook&&!r.smelt&&(kind==='build')===!!r.build)){
      const cost=costFor(r),owned=r.gear?!!state.gear?.[r.gear]:r.upgrade?state.bagSlots>=40:!r.build&&state.tools.includes(r.id);
      const row=recipeRow(r,cost,owned||!canPay(state,cost),owned?'Olemas':r.build?'Vali':'Valmista');
      row.querySelector('button').onclick=()=>{
        if(r.build){buildType=r.id;rotation='auto';closeModal();notify(`${r.name} · A paigutab · X pöörab · B lõpetab`);}
        else if(pay(state,cost)){if(r.gear){state.gear=state.gear||{};state.gear[r.gear]=true;}else if(r.upgrade)state.bagSlots+=5;else state.tools.push(r.id);gainXP(state,12);sound('craft');refresh();save();openModal('craft');}
      };content.append(row);
    }
  }
  if(!modal.open)modal.showModal();
  focusMenu(0);
}
function recipeRow(r,cost,disabled,label){const row=document.createElement('div');row.className='recipe';row.innerHTML=`<span>${r.icon}</span><div><strong>${r.name}</strong><p>${Object.entries(cost).map(([k,v])=>`${names[k]} ${v}`).join(' · ')}</p></div><button ${disabled?'disabled':''}>${label}</button>`;return row;}
function selectTool(i){if(state.tools.includes(tools[i]?.id)){charge=null;fishing=null;tool=i;refresh();}else notify('Meisterda kõigepealt see tööriist.');}
function cycleTool(d){for(let i=0;i<tools.length;i++){const next=(tool+d+tools.length)%tools.length;tool=next;if(state.tools.includes(tools[tool].id))break;}charge=null;refresh();}
function burst(x,y,color,count=8){for(let i=0;i<count;i++)particles.push({x,y,vx:(Math.random()-.5)*85,vy:-20-Math.random()*45,life:.7,color});}
function addOrDrop(id,n,x=state.player.x,y=state.player.y){if(!addItem(state,id,n)){state.drops.push({id,amount:n,x,y,inCave:state.inCave,expires:state.worldAge+600});notify(`${names[id]} jäi maha — seljakott on täis.`);}refresh();}
function collect(r){
  const selected=tools[tool].id,stump=!r.alive&&r.type==='wood'&&!r.removed;
  if((r.type==='wood'&&selected!=='axe')||(['stone','ironOre','copperOre'].includes(r.type)&&selected!=='pickaxe')){notify(r.type==='wood'?'Vali kirves.':'Vali kirka.');return;}
  if(stump){r.removed=true;addOrDrop('wood',state.skills.logger?3:2,r.x,r.y);sound('wood');burst(r.x,r.y,'#bd9864');gainXP(state,4);save();return;}
  r.hp-=['berries','herbs'].includes(r.type)?3:1+(state.skills.gather||0)+(r.type==='wood'&&state.gear?.axe?1:0)+(['stone','ironOre','copperOre'].includes(r.type)&&state.gear?.pickaxe?1:0);sound(r.type==='wood'?'wood':r.type==='berries'?'berries':'stone');burst(r.x,r.y,r.type==='wood'?'#c7a36b':'#afbda3');
  if(r.hp<=0){r.alive=false;const n=(r.type==='wood'?5:r.type==='stone'?4:3)+(state.skills.gather||0)+(r.type==='wood'&&state.skills.logger?2:0);addOrDrop(r.type,n,r.x,r.y);state.gathered[r.type]=(state.gathered[r.type]||0)+n;const level=state.level;gainXP(state,10);notify(`+${n} ${names[r.type].toLowerCase()}${state.level>level?' · Uus oskuspunkt!':''}`);refresh();save();}
}
function getTarget(){
  const p=state.player,candidates=[];
  function candidate(kind,x,y,range,label,ref){const d=Math.hypot(p.x-x,p.y-y);if(d<range)candidates.push({kind,x,y,d,label,ref});}
  for(const drop of state.drops.filter(d=>!!d.inCave===state.inCave))candidate('drop',drop.x,drop.y,40,`Korja ${names[drop.id].toLowerCase()} (${drop.amount})`,drop);
  for(const r of resources.filter(r=>!!r.inCave===state.inCave&&(r.alive||r.type==='wood'&&!r.removed)))candidate('resource',r.x,r.y,45,!r.alive?'Eemalda känd':r.type==='wood'?'Raiu puud':['stone','ironOre','copperOre'].includes(r.type)?`Kaevanda ${names[r.type].toLowerCase()}`:r.type==='herbs'?'Korja maitsetaimi':'Korja marju',r);
  if(state.inCave){if(!state.crystalFound)candidate('crystal',32*TILE,20*TILE,48,'Võta metsakristall');candidate('exit',32*TILE,29*TILE,48,'Mine metsa');}
  else{
    candidate('bench',base.x+35,base.y,46,'Meisterdamislaud');candidate('cave',cave.x,cave.y,58,'Sisene salakoopasse');
    for(const b of state.buildings.filter(b=>['fire','furnace'].includes(b.type)))candidate(b.type,(b.x+.5)*TILE,(b.y+.5)*TILE,48,b.type==='fire'?'Lõke ja toiduvalmistamine':'Sulatusahi',b);
    if(state.meteorArrived&&!state.alienFriend)candidate('alien',meteor.x+30,meteor.y+30,55,'Ütle Nupsile tere');
  }
  return candidates.sort((a,b)=>a.d-b.d)[0];
}
function interact(){
  if(!started||paused||death||actionCooldown>0)return;
  if(buildType){const p=buildPoint();place(p.x,p.y);return;}
  const t=getTarget();if(!t){if(tools[tool].id==='rod')beginFishing();return;}
  if(t.kind==='resource'){collect(t.ref);actionCooldown=.28;}
  else if(t.kind==='drop'){if(addItem(state,t.ref.id,t.ref.amount)){state.drops.splice(state.drops.indexOf(t.ref),1);notify('Korjasid oma asjad üles.');refresh();save();}else notify('Seljakott on täis.');}
  else if(['bench','fire','furnace'].includes(t.kind))openModal(t.kind==='bench'?'craft':t.kind);
  else if(t.kind==='crystal'){state.crystalFound=true;addOrDrop('crystal',3);gainXP(state,55);sound('crystal');notify('Metsakristall leitud! Sinu esimene suur seiklus on tehtud.');refresh();save();}
  else if(t.kind==='cave'){
    if(!state.tools.includes('pickaxe')||!state.tools.includes('torch')){notify('Koopasse minekuks vajad kirkat ja tõrvikut.');return;}
    state.inCave=true;state.player.x=32*TILE;state.player.y=27*TILE;moveAlienScene();notify('Salakoobas · kristall asub põhja pool.');
  }else if(t.kind==='exit'){state.inCave=false;state.player.x=cave.x;state.player.y=cave.y+48;moveAlienScene();}
  else if(t.kind==='alien'){state.alienFriend=true;state.alienFollowing=true;state.alien={x:t.x,y:t.y,inCave:false};addOrDrop('star',6);gainXP(state,35);sound('alien');notify('Nups on sinu sõber! B / T käsib tal oodata või kaasa tulla.');refresh();save();}
}
function moveAlienScene(){if(state.alienFriend&&state.alienFollowing){state.alien.inCave=state.inCave;state.alien.x=state.player.x+35;state.alien.y=state.player.y+20;}}
function alienCommand(){
  if(!state.alienFriend){notify('Kõigepealt leia meteoriidiga saabunud Nups.');return;}
  if(state.alienFollowing){state.alienFollowing=false;notify('Nups ootab siin. Mine tema juurde ja vajuta B / T, et ta kaasa kutsuda.');}
  else if(state.alien.inCave===state.inCave&&Math.hypot(state.alien.x-state.player.x,state.alien.y-state.player.y)<95){state.alienFollowing=true;sound('alien');notify('Nups tuleb sinuga kaasa ja aeglustab vastaseid.');}
  else notify('Nups ootab seal, kuhu ta jätsid. Kutsu teda lähedalt.');save();
}
function beginAction(){if(!started||paused||death)return;if(buildType){rotateBuild();return;}if(tools[tool].id==='bow'){if(!charge)charge={time:0};}else if(tools[tool].id==='rod')beginFishing();else attack();}
function endAction(){if(charge&&!paused&&!death){const stats=bowStats(state,charge.time),p=state.player;arrows.push({x:p.x+aim.x*16,y:p.y-10+aim.y*16,vx:aim.x*stats.speed,vy:aim.y*stats.speed,remaining:stats.range,damage:stats.damage,inCave:state.inCave});state.arrowsFired=(state.arrowsFired||0)+1;state.lastShot={power:stats.power,range:stats.range};sound('arrow');actionCooldown=.25;}charge=null;}
function attack(){
  if(actionCooldown>0)return;actionCooldown=.35;state.player.swing=.2;sound('swing');
  const p=state.player;
  if(tools[tool].id==='axe'&&!state.inCave){
    const wall=state.buildings.filter(b=>b.type==='wall'&&Math.hypot((b.x+.5)*TILE-p.x,(b.y+.5)*TILE-p.y)<53).sort((a,b)=>Math.hypot((a.x+.5)*TILE-p.x,(a.y+.5)*TILE-p.y)-Math.hypot((b.x+.5)*TILE-p.x,(b.y+.5)*TILE-p.y))[0];
    if(wall){wall.hp=(wall.hp??3)-1;if(wall.hp<=0){state.buildings.splice(state.buildings.indexOf(wall),1);const n=Math.floor((wall.paidWood??2)/2);if(n)state.drops.push({id:'wood',amount:n,x:(wall.x+.5)*TILE,y:(wall.y+.5)*TILE,inCave:false,expires:state.worldAge+600});notify('Sein lõhutud. Pool puidust jäi maha.');save();}burst((wall.x+.5)*TILE,(wall.y+.5)*TILE,'#b9975d');return;}
  }
  const entities=state.inCave?bats.filter(b=>b.hp>0):[...zombies,...animals];
  const target=entities.filter(e=>Math.hypot(e.x-p.x,e.y-p.y)<52).sort((a,b)=>Math.hypot(a.x-p.x,a.y-p.y)-Math.hypot(b.x-p.x,b.y-p.y))[0];
  if(target){hitEntity(target,1+(state.skills.combat||0)+(tools[tool].id==='axe'&&state.gear?.axe?1:0));return;}
  const t=getTarget();if(t?.kind==='resource')collect(t.ref);
}
function hitEntity(e,damage){e.hp-=damage;burst(e.x,e.y,e.type?'#e0d4ae':'#b6c998');if(e.hp<=0){if(animals.includes(e)){animals.splice(animals.indexOf(e),1);addOrDrop('meat',e.type==='deer'?3:1,e.x,e.y);notify('Metsloomalt said liha. Lõkkel saab süüa teha.');}else if(zombies.includes(e))zombies.splice(zombies.indexOf(e),1);gainXP(state,8);refresh();}else{e.x+=aim.x*12;e.y+=aim.y*12;}}
function eat(){if(!started||death)return;const food=['stew','cookedFish','roast','berries'].find(k=>state.inventory[k]>0);if(!food){notify('Korja marju või valmista lõkkel süüa.');return;}if(state.hunger>=100&&state.health>=maxHealth(state))return;const value={stew:[65,3],roast:[40,2],cookedFish:[45,2],berries:[25,1]}[food];state.inventory[food]--;state.hunger=Math.min(100,state.hunger+value[0]);state.health=Math.min(maxHealth(state),state.health+value[1]);sound('eat');notify(`${names[food]} · +${value[0]} kõhtu`);refresh();save();}
function shorePoint(){if(state.inCave)return null;const p=state.player;for(let radius=20;radius<=75;radius+=10)for(let a=0;a<16;a++){const angle=a*Math.PI/8,x=p.x+Math.cos(angle)*radius,y=p.y+Math.sin(angle)*radius;if(water(x,y))return{x,y};}return null;}
function beginFishing(){if(fishing){fishing=null;notify('Õng on kokku pandud.');return;}const shore=shorePoint();if(!shore){notify('Kalapüügiks mine veekogu kaldale.');return;}fishing={...shore,time:0,origin:{x:state.player.x,y:state.player.y}};notify('Õng vees… oota natuke ja hoia paigal.');}
function rotateBuild(){if(!['wall','door'].includes(buildType))return;rotation=rotation==='v'?'h':'v';notify(rotation==='v'?'Sein: vertikaalne':'Sein: horisontaalne');}
function buildPoint(){return canvas._pointer||{x:state.player.x+aim.x*48,y:state.player.y+aim.y*48};}
function placement(x,y){
  const gx=Math.floor(x/TILE),gy=Math.floor(y/TILE),cx=(gx+.5)*TILE,cy=(gy+.5)*TILE;
  const floors=['floor','stoneFloor'],floor=floors.includes(buildType);
  const valid=!state.inCave&&Math.hypot(cx-state.player.x,cy-state.player.y)<145&&gx>=2&&gy>=2&&gx<W-2&&gy<H-2&&!water(cx,cy)&&Math.hypot(cx-cave.x,cy-cave.y)>75&&Math.hypot(cx-(base.x+35),cy-base.y)>32&&!resources.some(r=>!r.inCave&&(r.alive||r.type==='wood'&&!r.removed)&&!['berries','herbs'].includes(r.type)&&Math.hypot(r.x-cx,r.y-cy)<25)&&!state.buildings.some(b=>b.x===gx&&b.y===gy&&(floor?floors.includes(b.type):!floors.includes(b.type)))&&!(buildType==='wall'&&Math.hypot(cx-state.player.x,cy-state.player.y)<25);
  return {gx,gy,cx,cy,valid:valid&&canPay(state,costFor(recipes.find(r=>r.id===buildType)))};
}
function place(x,y){if(!buildType)return;const loc=placement(x,y);if(!loc.valid){notify('Punane koht: liiga kaugel, hõivatud või materjale napib.');return;}const r=recipes.find(r=>r.id===buildType),cost=costFor(r);if(!pay(state,cost))return;const b={x:loc.gx,y:loc.gy,type:buildType,paidWood:cost.wood||0};if(rotation!=='auto'&&['wall','door'].includes(buildType))b.rotation=rotation;if(['fire','furnace'].includes(buildType))b.fuel=0;state.buildings.push(b);gainXP(state,5);burst(loc.cx,loc.cy,'#e4c576');sound('build');refresh();save();}
function isSheltered(){if(state.inCave)return false;const sx=Math.floor(state.player.x/TILE),sy=Math.floor(state.player.y/TILE);const walls=state.buildings.filter(b=>b.type==='wall'||b.type==='door');if(walls.length<4)return false;const blocks=new Set(walls.map(b=>`${b.x},${b.y}`)),stack=[[sx,sy]],seen=new Set();if(blocks.has(`${sx},${sy}`))return false;while(stack.length){const[x,y]=stack.pop(),k=`${x},${y}`;if(blocks.has(k)||seen.has(k))continue;if(x<0||y<0||x>=W||y>=H)return false;seen.add(k);for(const[dx,dy]of[[1,0],[-1,0],[0,1],[0,-1]])stack.push([x+dx,y+dy]);}return true;}
function blocked(x,y,enemy=false,inCave=state.inCave){if(inCave)return x<27*TILE||x>37*TILE||y<18*TILE||y>30*TILE;if(x<60||y<70||x>W*TILE-60||y>H*TILE-60||water(x,y))return true;return state.buildings.some(b=>(b.type==='wall'||enemy&&b.type==='door')&&Math.abs(x-(b.x+.5)*TILE)<21&&Math.abs(y-(b.y+.5)*TILE)<21);}
function scaredByFire(x,y){if(tools[tool].id==='torch'&&Math.hypot(x-state.player.x,y-state.player.y)<110)return{x:state.player.x,y:state.player.y};if(!state.inCave)return state.buildings.filter(b=>b.type==='fire'&&b.fuel>0).map(b=>({x:(b.x+.5)*TILE,y:(b.y+.5)*TILE})).find(f=>Math.hypot(x-f.x,y-f.y)<150);return null;}
function damagePlayer(amount=1){if(invulnerable>0||death)return;state.health=Math.max(0,state.health-amount);invulnerable=state.skills.guardian?3:2;damageFlash=.55;sound('hurt');burst(state.player.x,state.player.y,'#efd39a',12);if(state.health<=0)beginDeath();}
function beginDeath(){death={time:0,restored:false};charge=null;fishing=null;state.player.walk=0;keys={};$('deathOverlay').classList.remove('hidden');}
function updateDeath(dt){death.time+=dt;$('deathOverlay').style.opacity=String(death.time<.8?death.time/.8:death.time<1.8?1:Math.max(0,1-(death.time-1.8)/.9));if(death.time>=1&&!death.restored){death.restored=true;state.player.x=base.x;state.player.y=base.y+64;state.inCave=false;state.health=maxHealth(state);state.hunger=100;state.day++;state.time=0;zombies.length=0;invulnerable=3;moveAlienScene();refresh();save();}if(death.time>=2.7){death=null;$('deathOverlay').classList.add('hidden');notify('Uus hommik. Kõik asjad on alles.');}}
function spawnZombies(){zombies.length=0;const p=state.player;for(let i=0;i<4;i++){const a=i*Math.PI/2,x=Math.max(70,Math.min(W*TILE-70,p.x+Math.cos(a)*260)),y=Math.max(80,Math.min(H*TILE-70,p.y+Math.sin(a)*260));if(!water(x,y))zombies.push({x,y,hp:2,hit:0});}}
function slowed(e){return state.alienFriend&&state.alienFollowing&&state.alien.inCave===state.inCave&&Math.hypot(e.x-state.alien.x,e.y-state.alien.y)<(state.skills.frost?160:100);}
function moveEnemy(e,dt,speed,sheltered=false){const fire=scaredByFire(e.x,e.y),p=state.player;const dx=fire?e.x-fire.x:p.x-e.x,dy=fire?e.y-fire.y:p.y-e.y,n=Math.hypot(dx,dy)||1;e.slowed=slowed(e);if(fire||!sheltered){const v=fire?55:speed*(e.slowed?Math.max(.25,.6-.08*(state.skills.star||0)):1);const nx=e.x+dx/n*v*dt,ny=e.y+dy/n*v*dt;if(!blocked(nx,e.y,true))e.x=nx;if(!blocked(e.x,ny,true))e.y=ny;if(!fire&&n<25)damagePlayer();}}
function updateAlien(dt){if(!state.alienFriend)return;const a=state.alien;if(state.alienFollowing&&a.inCave===state.inCave){const dx=state.player.x-aim.x*28-a.x,dy=state.player.y-aim.y*28-a.y,n=Math.hypot(dx,dy);if(n>10){const step=Math.min(n,105*dt);const nx=a.x+dx/n*step,ny=a.y+dy/n*step;if(!blocked(nx,a.y,false,a.inCave))a.x=nx;if(!blocked(a.x,ny,false,a.inCave))a.y=ny;}}else if(!a.inCave&&state.buildings.some(b=>b.type==='nest'&&Math.hypot((b.x+.5)*TILE-a.x,(b.y+.5)*TILE-a.y)<120)){state.alienWork=(state.alienWork||0)+dt;if(state.alienWork>=35/(1+(state.skills.star||0)*.5)){state.alienWork=0;addOrDrop('berries',state.skills.helper?4:2,a.x,a.y);notify('Nups tõi baasi marju!');}}}
function updateArrows(dt){for(let i=arrows.length-1;i>=0;i--){const a=arrows[i],distance=Math.hypot(a.vx,a.vy)*dt;const steps=Math.max(1,Math.ceil(distance/7));let gone=false;for(let j=0;j<steps;j++){a.x+=a.vx*dt/steps;a.y+=a.vy*dt/steps;a.remaining-=distance/steps;if(blocked(a.x,a.y,false,a.inCave)){gone=true;break;}const entities=a.inCave?bats.filter(b=>b.hp>0):[...zombies,...animals];const e=entities.find(e=>Math.hypot(e.x-a.x,e.y-10-a.y)<20);if(e){hitEntity(e,a.damage);gone=true;break;}}if(gone||a.remaining<=0)arrows.splice(i,1);}}
function updateHUD(){
  $('hearts').textContent=Array.from({length:maxHealth(state)},(_,i)=>i<state.health?'♥':'♡').join(' ');$('foodBar').style.width=`${state.hunger}%`;$('foodText').textContent=`${Math.ceil(state.hunger)}%`;
  const night=state.time>=300,left=Math.ceil((night?360:300)-state.time);$('sunIcon').textContent=night?'☾':'☀';$('dayLabel').textContent=`${state.day}. päev`;$('timeLabel').textContent=`${night?'Öö':'Päev'} · ${Math.floor(left/60)}:${String(left%60).padStart(2,'0')}`;$('areaName').textContent=state.inCave?'Metsakristalli salakoobas':isSheltered()?'Sinu turvaline kodu':'Rohelaane mets';
  currentTarget=getTarget();let prompt=buildType?'A / klõps · Ehita   X / Q · Pööra   B / Esc · Lõpeta':fishing?'Õng vees… kala näkkab varsti':charge?`Vibu laeb · ${Math.round(bowStats(state,charge.time).power*100)}% · vabasta RT / tühik`:currentTarget?`A / E · ${currentTarget.label}`:tools[tool].id==='rod'&&shorePoint()?'RT / tühik · Püüa kala':'';
  $('interaction').textContent=prompt;$('interaction').classList.toggle('hidden',!prompt||paused||!!death);
  $('buildInfo').classList.toggle('hidden',!buildType);
  if(buildType){const r=recipes.find(r=>r.id===buildType);$('buildInfo').innerHTML=`<strong>${r.name}</strong>${Object.entries(costFor(r)).map(([k,v])=>`${names[k]}: ${v}`).join(' · ')}<br>Suund: ${rotation==='auto'?'ühendub naabritega':rotation==='v'?'vertikaalne':'horisontaalne'}<br>Roheline: vaba · punane: takistus`;}
  $('damageOverlay').style.opacity=String(Math.max(0,damageFlash/.55));
}
function update(dt,pad){
  elapsed+=dt;toastTime-=dt;if(toastTime<=0)$('toast').classList.add('hidden');damageFlash=Math.max(0,damageFlash-dt);invulnerable=Math.max(0,invulnerable-dt);
  if(!started||paused){updateHUD();return;}if(death){updateDeath(dt);updateHUD();return;}if(state.health<=0){beginDeath();updateHUD();return;}
  actionCooldown=Math.max(0,actionCooldown-dt);const p=state.player;
  let dx=(keys.KeyD||keys.ArrowRight?1:0)-(keys.KeyA||keys.ArrowLeft?1:0)+pad.x,dy=(keys.KeyS||keys.ArrowDown?1:0)-(keys.KeyW||keys.ArrowUp?1:0)+pad.y,n=Math.hypot(dx,dy);
  if(n>0){if(n>1){dx/=n;dy/=n;}if(!blocked(p.x+dx*105*dt,p.y))p.x+=dx*105*dt;if(!blocked(p.x,p.y+dy*105*dt))p.y+=dy*105*dt;p.walk+=dt*10;if(dx)p.face=dx<0?-1:1;if(!canvas._pointer&&!pad.aimed&&!charge){const length=Math.hypot(dx,dy);aim={x:dx/length,y:dy/length};}}else p.walk=0;
  if(p.swing)p.swing-=dt;if(charge)charge.time=Math.min(1.5,charge.time+dt);
  const wasNight=state.time>=300;advanceTime(state,dt);if(!wasNight&&state.time>=300){spawnZombies();notify('Öö saabus. Lõke, tõrvik ja kodu kaitsevad sind.');}if(wasNight&&state.time<300){zombies.length=0;notify('Algab uus päev!');}
  if(!state.meteorArrived&&(state.time>55||state.day>1)){state.meteorArrived=true;notify('Meteoriit ida pool! Sealt saabus väike külaline.');save();}
  if(state.hunger<=0){state.starve=(state.starve||0)+dt;if(state.starve>15){damagePlayer();state.starve=0;notify('Kõht on tühi! Söö marju.');}}
  if(fishing){fishing.time+=dt;if(Math.hypot(p.x-fishing.origin.x,p.y-fishing.origin.y)>12){fishing=null;notify('Liikusid eemale — püük katkes.');}else if(fishing.time>=3){addOrDrop('fish',state.skills.angler?2:1);gainXP(state,8);sound('fish');notify('Kala käes! Lõkkel saad selle küpsetada.');fishing=null;save();}}
  updateAlien(dt);
  if(!state.inCave){
    for(const a of animals){a.timer-=dt;const d=Math.hypot(a.x-p.x,a.y-p.y),fire=scaredByFire(a.x,a.y);if(fire||d<100){const from=fire||p;a.dir=Math.atan2(a.y-from.y,a.x-from.x);a.timer=.4;}else if(a.timer<0){a.dir=rand()*6.28;a.timer=2+rand()*4;}const speed=fire||d<100?52:9;const nx=a.x+Math.cos(a.dir)*speed*dt,ny=a.y+Math.sin(a.dir)*speed*dt;if(!blocked(nx,ny,false,false)&&!water(nx-8,ny)&&!water(nx+8,ny)&&!water(nx,ny-6)&&!water(nx,ny+6)){a.x=nx;a.y=ny;a.step+=dt*8;}else a.dir+=2;}
    const sheltered=isSheltered();for(const z of zombies)moveEnemy(z,dt,23,sheltered);
  }else for(const b of bats.filter(b=>b.hp>0))moveEnemy(b,dt,17);
  for(const b of state.buildings.filter(b=>['fire','furnace'].includes(b.type)))b.fuel=Math.max(0,(b.fuel||0)-dt);
  updateArrows(dt);
  for(let i=particles.length-1;i>=0;i--){const a=particles[i];a.life-=dt;a.x+=a.vx*dt;a.y+=a.vy*dt;a.vy+=90*dt;if(a.life<=0)particles.splice(i,1);}
  autosave+=dt;if(autosave>10){save();autosave=0;}
  updateHUD();
}
window.addEventListener('keydown',e=>{
  if(['Space','ArrowUp','ArrowDown','ArrowLeft','ArrowRight'].includes(e.code))e.preventDefault();
  if(e.repeat)return;keys[e.code]=true;
  if(paused){if(e.code==='Escape')closeModal();else if(['ArrowDown','ArrowRight','KeyS','KeyD'].includes(e.code))focusMenu(menuIndex+1);else if(['ArrowUp','ArrowLeft','KeyW','KeyA'].includes(e.code))focusMenu(menuIndex-1);else if(e.code==='Enter'||e.code==='Space')menuButtons()[menuIndex]?.click();return;}
  if(e.code==='Escape'){buildType=null;return;}if(!started){if(e.code==='Enter')start();return;}if(death)return;
  if(/^Digit[1-6]$/.test(e.code)){selectTool(+e.code.slice(-1)-1);return;}
  switch(e.code){case'KeyE':interact();break;case'Space':beginAction();break;case'KeyR':eat();break;case'KeyC':openModal('craft');break;case'KeyB':openModal('build');break;case'KeyK':openModal('skills');break;case'KeyI':openModal('bag');break;case'KeyT':alienCommand();break;case'KeyQ':rotateBuild();break;}
});
window.addEventListener('keyup',e=>{keys[e.code]=false;if(e.code==='Space')endAction();});
window.addEventListener('blur',()=>{keys={};charge=null;save();});document.addEventListener('visibilitychange',()=>{last=0;keys={};charge=null;if(document.hidden)save();});window.addEventListener('pagehide',save);
canvas.addEventListener('pointermove',e=>{const r=canvas.getBoundingClientRect(),x=(e.clientX-r.left)*canvas.width/r.width+cam.x,y=(e.clientY-r.top)*canvas.height/r.height+cam.y,dx=x-state.player.x,dy=y-state.player.y,n=Math.hypot(dx,dy)||1;aim={x:dx/n,y:dy/n};canvas._pointer={x,y};});
canvas.addEventListener('pointerdown',e=>{if(!started||paused||death)return;canvas.focus();canvas.setPointerCapture(e.pointerId);if(buildType){const r=canvas.getBoundingClientRect();place((e.clientX-r.left)*canvas.width/r.width+cam.x,(e.clientY-r.top)*canvas.height/r.height+cam.y);}else beginAction();});canvas.addEventListener('pointerup',endAction);canvas.addEventListener('pointercancel',()=>charge=null);
function readPad(){
  const pad=[...(navigator.getGamepads?.()||[])].find(p=>p?.connected);
  if(!pad){$('controllerStatus').textContent='KLAVIATUUR + HIIR';padPrevious={};return{x:0,y:0};}
  $('controllerStatus').textContent='XBOX · VIEW KOTT · Y EHITA · RT TÖÖRIIST';
  const down=i=>!!pad.buttons[i]&&(pad.buttons[i].pressed||pad.buttons[i].value>.25),pressed=i=>down(i)&&!padPrevious[i],released=i=>!down(i)&&padPrevious[i];
  const lx=pad.axes[0]||0,ly=pad.axes[1]||0,ax=pad.axes[2]||0,ay=pad.axes[3]||0;
  if(!started){if(pressed(0))start();}
  else if(paused){
    if(pressed(1))closeModal();
    else{
      const direction=pressed(12)||pressed(14)?-1:pressed(13)||pressed(15)?1:Math.abs(lx)>.55||Math.abs(ly)>.55?(Math.abs(ly)>=Math.abs(lx)?Math.sign(ly):Math.sign(lx)):0;
      if(direction&&(performance.now()>padMoveAt||pressed(12)||pressed(13)||pressed(14)||pressed(15))){focusMenu(menuIndex+direction);padMoveAt=performance.now()+230;}
      // Activate our own menu selection, never whichever unrelated element stole DOM focus.
      if(pressed(0)){const buttons=menuButtons();buttons[Math.min(menuIndex,buttons.length-1)]?.click();}
    }
  }else if(!death){
    if(pressed(0))interact();if(pressed(2)){if(buildType)rotateBuild();else{beginAction();if(tools[tool].id==='bow')endAction();}}
    if(pressed(3))openModal('build');if(pressed(8))openModal('bag');if(pressed(9))openModal('skills');
    if(pressed(1)){if(buildType)buildType=null;else alienCommand();}
    if(pressed(4))cycleTool(-1);if(pressed(5))cycleTool(1);if(pressed(6))eat();
    if(pressed(7))beginAction();if(released(7))endAction();
  }
  pad.buttons.forEach((_,i)=>padPrevious[i]=down(i));
  const aimed=Math.hypot(ax,ay)>.2;if(aimed&&!paused){const n=Math.hypot(ax,ay);aim={x:ax/n,y:ay/n};canvas._pointer=null;}
  if(Math.abs(lx)>.18||Math.abs(ly)>.18)canvas._pointer=null;
  return{x:Math.abs(lx)>.18?lx:0,y:Math.abs(ly)>.18?ly:0,aimed};
}

// Small, hand-drawn pixel sprites. All scenery stays local and animates on canvas.
function rect(x,y,w,h,c){ctx.fillStyle=c;ctx.fillRect(Math.round(x),Math.round(y),w,h);}
function ellipse(x,y,rx,ry,c){ctx.fillStyle=c;ctx.beginPath();ctx.ellipse(x,y,rx,ry,0,0,Math.PI*2);ctx.fill();}
function poly(points,c){ctx.fillStyle=c;ctx.beginPath();points.forEach(([x,y],i)=>i?ctx.lineTo(x,y):ctx.moveTo(x,y));ctx.closePath();ctx.fill();}
function shadow(x,y,rx=18,ry=6){ellipse(x,y,rx,ry,'#152c2040');}
function tree(x,y,variant=0){const sway=Math.sin(elapsed*1.1+x)*1.2;shadow(x,y+3,27,9);rect(x-5,y-29,10,33,'#705038');rect(x-2,y-27,3,27,'#9c7247');rect(x+5,y-12,4,5,'#705038');if(variant===1){poly([[x+sway,y-101],[x-22+sway,y-61],[x-12+sway,y-61],[x-30+sway,y-39],[x-21+sway,y-39],[x-34+sway,y-17],[x+34+sway,y-17],[x+21+sway,y-39],[x+29+sway,y-39],[x+12+sway,y-61],[x+23+sway,y-61]],'#244f3b');poly([[x+sway,y-96],[x-15+sway,y-62],[x-8+sway,y-62],[x-24+sway,y-40],[x-13+sway,y-40],[x-24+sway,y-23],[x+3+sway,y-23],[x+10+sway,y-40],[x+2+sway,y-62]],'#39714a');rect(x-18+sway,y-41,12,3,'#548153');}else{const xx=x+sway;rect(xx-24,y-65,47,35,'#244e35');rect(xx-33,y-54,64,20,'#244e35');rect(xx-20,y-83,38,23,'#365d39');rect(xx-30,y-69,54,30,'#3c6f41');rect(xx-19,y-83,32,30,'#4b7b46');rect(xx-11,y-91,21,11,'#4b7b46');rect(xx-26,y-64,14,11,'#608b4e');rect(xx-15,y-76,11,8,'#70974f');rect(xx+3,y-60,21,10,'#538143');rect(xx+14,y-46,11,7,'#3c6136');rect(xx-21,y-41,25,9,'#315f37');rect(xx-4,y-78,8,3,'#86a65d');}}
function rock(x,y,big=false){shadow(x,y+3,19,6);poly([[x-19,y],[x-15,y-18],[x-4,y-25],[x+11,y-20],[x+19,y-8],[x+14,y+5],[x-10,y+6]],'#61796b');poly([[x-15,y-17],[x-4,y-24],[x+10,y-20],[x+2,y-10],[x-12,y-6]],'#9aaa88');poly([[x+2,y-10],[x+11,y-19],[x+18,y-7],[x+13,y+4],[x+2,y+3]],'#718b79');rect(x-8,y-17,9,3,'#b9c2a0');if(big)rect(x+5,y-7,4,5,'#b8c7a1');}
function bush(x,y){shadow(x,y+3,17,5);rect(x-13,y-16,26,17,'#305b36');rect(x-19,y-10,36,11,'#3c7140');rect(x-9,y-22,17,13,'#518347');rect(x-15,y-14,12,5,'#699047');for(const[dx,dy]of[[-10,-8],[-3,-17],[6,-10],[12,-5]]){rect(x+dx,y+dy,5,5,'#7473ad');rect(x+dx,y+dy,2,2,'#b2a3df');}}
function simm(x,y){const p=state.player,bob=p.walk?Math.sin(p.walk)*1.5:0;shadow(x,y+2,12,4);const yy=y+bob,step=p.walk?Math.sin(p.walk)*3:0;rect(x-7,yy-8,5,9+step,'#384739');rect(x+2,yy-8,5,9-step,'#384739');rect(x-8,yy+step,6,3,'#332e23');rect(x+2,yy-step,6,3,'#332e23');rect(x-9,yy-23,18,16,'#d7ac43');rect(x-6,yy-22,9,13,'#ebc45d');rect(x-12,yy-21,4,12,'#b28b37');rect(x+8,yy-21,4,12,'#e4b854');rect(x-12,yy-10,4,4,'#f2c293');rect(x+8,yy-10,4,4,'#f2c293');rect(x-5,yy-33,12,11,'#dca776');rect(x-7,yy-38,14,7,'#695333');rect(x-8,yy-33,4,7,'#695333');rect(x-4,yy-37,9,3,'#937141');rect(x+(p.face<0?-4:3),yy-30,2,2,'#263629');rect(x-6,yy-24,12,3,'#e4c664');rect(x-5,yy-17,3,4,'#b98d38');if(p.swing>0){const sx=x+aim.x*19,sy=yy-15+aim.y*16;rect(sx-2,sy-10,3,21,'#b89259');poly([[sx-8,sy-11],[sx+5,sy-13],[sx+9,sy-6],[sx-7,sy-3]],'#bdc5a9');ellipse(x+aim.x*29,yy-12+aim.y*26,6,3,'#e5db8c80');}else if(tools[tool].id==='torch'){rect(x+12,yy-21,3,12,'#956d3c');ellipse(x+14,yy-26,4+Math.sin(elapsed*12),7,'#eab559');rect(x+12,yy-28,3,5,'#fff1ac');}}
function rabbit(a){const x=a.x,y=a.y,b=Math.sin(a.step)*1;shadow(x,y+2,9,3);rect(x-7,y-9+b,13,8,'#d6cbb3');rect(x+3,y-13+b,8,9,'#e5ddc4');rect(x+4,y-23+b,3,12,'#e5ddc4');rect(x+8,y-21+b,3,9,'#c9bca3');rect(x+5,y-21+b,1,6,'#d7a79e');rect(x+9,y-11+b,2,2,'#343d2c');rect(x-10,y-7+b,4,4,'#eee7d0');rect(x-5,y,3,3,'#b5ad91');rect(x+5,y,3,3,'#b5ad91');}
function deer(a){const x=a.x,y=a.y,b=Math.sin(a.step);shadow(x,y+1,17,5);for(const dx of[-11,-4,6,12])rect(x+dx,y-13,3,14+Math.sin(a.step+dx)*2,'#876346');rect(x-14,y-26+b,27,14,'#ae8150');rect(x-12,y-25+b,19,5,'#c29965');rect(x+9,y-35+b,7,20,'#b58a59');rect(x+11,y-39+b,14,10,'#bd9663');rect(x+20,y-36+b,2,2,'#293c2c');rect(x+10,y-44+b,4,7,'#a7784c');rect(x+18,y-43+b,4,7,'#a7784c');rect(x-17,y-25+b,5,5,'#e2d0a1');for(const dx of[-5,2,7])rect(x+dx,y-22+b,2,2,'#e5c995');}
function alien(x,y){const float=Math.sin(elapsed*3)*2;shadow(x,y+2,11,4);rect(x-8,y-19+float,16,15,'#83b8aa');rect(x-11,y-29+float,22,15,'#a5d0b5');rect(x-8,y-33+float,16,8,'#a5d0b5');rect(x-7,y-26+float,4,6,'#27394a');rect(x+3,y-26+float,4,6,'#27394a');rect(x-6,y-26+float,1,2,'#f0ffdb');rect(x+4,y-26+float,1,2,'#f0ffdb');rect(x-3,y-17+float,6,6,'#d6c17b');rect(x-8,y-37+float,2,6,'#81af9c');rect(x+6,y-37+float,2,6,'#81af9c');rect(x-9,y-39+float,4,3,'#ecdb93');rect(x+5,y-39+float,4,3,'#ecdb93');}
function zombie(z){const bob=Math.sin(elapsed*5+z.x)*1;shadow(z.x,z.y,11,4);rect(z.x-7,z.y-10,5,11,'#314c3b');rect(z.x+3,z.y-10,5,11,'#314c3b');rect(z.x-10,z.y-25+bob,20,17,'#637658');rect(z.x-7,z.y-38+bob,15,14,'#9ab678');rect(z.x-12,z.y-22+bob,4,13,'#8fa769');rect(z.x+9,z.y-22+bob,4,13,'#8fa769');rect(z.x-4,z.y-33+bob,3,3,'#354230');rect(z.x+3,z.y-33+bob,3,3,'#354230');rect(z.x-2,z.y-27+bob,6,2,'#4c633a');}
function herb(x,y){shadow(x,y+2,10,3);rect(x-1,y-18,2,20,'#365f37');rect(x-8,y-16,8,5,'#a4ba69');rect(x+1,y-12,9,5,'#8ba75a');rect(x-7,y-7,7,4,'#b6c979');rect(x,y-24,4,7,'#91ac61');}
function batSprite(b){const x=b.x,y=b.y+Math.sin(elapsed*4+b.phase)*3,wing=Math.sin(elapsed*10+b.phase)*8;shadow(x,y+25,9,3);poly([[x-4,y],[x-21,y-8-wing],[x-16,y+4],[x-6,y+7]],'#9f90b7');poly([[x+4,y],[x+21,y-8-wing],[x+16,y+4],[x+6,y+7]],'#9f90b7');rect(x-5,y-7,10,15,'#b8a8c9');rect(x-5,y-12,3,6,'#b8a8c9');rect(x+2,y-12,3,6,'#b8a8c9');rect(x-3,y-3,2,3,'#354347');rect(x+2,y-3,2,3,'#354347');rect(x-2,y+4,4,1,'#e9d8d8');}
function bench(){const x=base.x+35,y=base.y;shadow(x,y+4,22,6);rect(x-16,y-17,5,23,'#65462e');rect(x+11,y-17,5,23,'#65462e');rect(x-22,y-25,44,10,'#a8804e');rect(x-22,y-26,44,3,'#d1ab6b');rect(x-17,y-23,2,7,'#785831');rect(x-14,y-32,8,7,'#7e9583');rect(x-9,y-36,3,5,'#aabc9a');rect(x+4,y-31,10,5,'#cfb579');rect(x+6,y-37,3,9,'#79664e');const tx=base.x-55,ty=base.y+6;shadow(tx,ty+1,33,8);poly([[tx,ty-42],[tx-31,ty],[tx+29,ty]],'#c3ab64');poly([[tx,ty-42],[tx+29,ty],[tx+6,ty]],'#a48f53');poly([[tx,ty-30],[tx-13,ty],[tx+11,ty]],'#3b4630');rect(tx-34,ty,68,3,'#765e3e');}
function caveSprite(){const x=cave.x,y=cave.y;shadow(x,y+8,50,14);poly([[x-55,y+3],[x-46,y-38],[x-23,y-60],[x+19,y-63],[x+46,y-38],[x+53,y+3]],'#607d6a');poly([[x-44,y-37],[x-23,y-58],[x+16,y-60],[x+8,y-36],[x-15,y-28]],'#8aa18a');poly([[x-25,y+3],[x-24,y-23],[x-10,y-37],[x+10,y-36],[x+24,y-20],[x+26,y+3]],'#172c28');rect(x-21,y-9,44,14,'#172c28');rect(x-30,y-31,9,5,'#a8b49b');rect(x+26,y-22,12,4,'#81967a');rect(x-38,y+2,75,6,'#a3976b');bush(x+51,y+6);ctx.fillStyle='#e1dfb7';ctx.font='9px monospace';ctx.textAlign='center';ctx.fillText('SALAKOOBAS',x,y-72);}
function crystal(x,y){const bob=Math.sin(elapsed*2)*3;ellipse(x,y,27,9,'#7bd2cc22');poly([[x,y-37+bob],[x-13,y-18+bob],[x,y+1+bob],[x+13,y-18+bob]],'#5d9fc2');poly([[x,y-37+bob],[x-13,y-18+bob],[x,y-13+bob]],'#b6f4e2');poly([[x,y-37+bob],[x,y-13+bob],[x+13,y-18+bob]],'#80ceda');poly([[x-13,y-18+bob],[x,y-13+bob],[x,y+1+bob]],'#6dbbcc');rect(x-21,y-27+Math.sin(elapsed*3)*6,3,3,'#cbfff1');rect(x+21,y-10+Math.sin(elapsed*2)*7,2,2,'#e4ffe1');}
function fireSprite(x,y,fuel){shadow(x,y+4,22,6);for(let i=0;i<7;i++){const a=i*Math.PI*2/7;rect(x+Math.cos(a)*17-4,y+Math.sin(a)*7-3,8,6,'#a0a28c');}rect(x-13,y-3,26,5,'#795234');rect(x-8,y-7,17,4,'#b38c4e');if(fuel>0){const flick=Math.sin(elapsed*13)*3;poly([[x-10,y-3],[x-7,y-17],[x-2,y-11],[x+2,y-29-flick],[x+8,y-14],[x+11,y-3]],'#e99045');poly([[x-5,y-4],[x-2,y-19],[x+2,y-13],[x+5,y-5]],'#ffe0a0');rect(x+5+Math.sin(elapsed*2)*5,y-34-(elapsed*12%12),2,2,'#f8cf88');}}
function building(b){
 const x=b.x*TILE,y=b.y*TILE,cx=x+16,cy=y+16;
 if(b.type==='floor'||b.type==='stoneFloor'){
   const stone=b.type==='stoneFloor';rect(x,y,TILE,TILE,stone?'#959b87':'#9e804c');
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
     if(horizontal){rect(x,cy-7,32,15,'#654b2c');rect(x,cy-11,32,12,'#a9864e');rect(x,cy-11,32,3,'#d6b36b');rect(x+3,cy-3,26,2,'#7e6037');}
     if(vertical){rect(cx-6,y,14,32,'#654b2c');rect(cx-9,y,12,32,'#b69456');rect(cx-9,y,3,32,'#d9b972');rect(cx-2,y+3,2,26,'#8b6c3c');}
     rect(cx-6,cy-10,12,12,'#c3a263');rect(cx-4,cy-9,8,3,'#e0c483');
   }
 }
 if(b.type==='fire')fireSprite(cx,cy,b.fuel);
 if(b.type==='furnace'){
   shadow(cx,cy+10,23,7);rect(x-1,y-18,34,40,'#65776b');rect(x+3,y-21,26,7,'#a0aa91');rect(x+7,y-15,18,10,'#81917e');rect(x+7,y+1,18,17,'#29372e');rect(x+5,y-1,22,3,'#a6a98b');
   if(b.fuel>0){rect(x+10,y+6,12,10,'#e39552');rect(x+13,y+3,6,11,'#f8cf7e');}rect(x+9,y-31,14,12,'#758472');
 }
 if(b.type==='nest'){shadow(cx,y+19,23,8);rect(x-2,y-5,36,29,'#717b71');rect(x+3,y-15,26,13,'#a5b39c');rect(x+8,y-21,16,8,'#bfc5a5');rect(x+6,y+4,20,20,'#244a44');rect(x+4,y-7,24,4,'#8fd0b1');rect(x+11,y-13,10,4,'#eed186');}
}
function terrain(){const sx=Math.max(0,Math.floor(cam.x/TILE)),sy=Math.max(0,Math.floor(cam.y/TILE)),ex=Math.min(W,Math.ceil((cam.x+canvas.width)/TILE)+1),ey=Math.min(H,Math.ceil((cam.y+canvas.height)/TILE)+1);for(let y=sy;y<ey;y++)for(let x=sx;x<ex;x++){const hash=((x*73856093)^(y*19349663))>>>0;const px=x*TILE,py=y*TILE;if(state.inCave){rect(px,py,TILE,TILE,(x<27||x>37||y<18||y>30)?(hash%3?'#263d39':'#30463e'):(hash%3?'#3b4941':'#414f46'));if(x>=27&&x<=37&&y>=18&&y<=30){rect(px+hash%20,py+hash%17,5,2,'#58644e');}continue;}if(water(px+16,py+16)){rect(px,py,TILE,TILE,['#487e78','#4b827a','#518a80'][hash%3]);const wave=Math.floor(Math.sin(elapsed*1.5+x)*2);rect(px+5+wave,py+10,12,1,'#84b3a066');rect(px+16-wave,py+23,10,1,'#96bd9b66');continue;}const path=(Math.abs(x-31)<2&&y>=16&&y<=32)||(Math.abs(y-28)<1.5&&x>30&&x<46);const clearing=Math.hypot(x-31,y-29)<4;rect(px,py,TILE,TILE,path||clearing?['#8b8b55','#91905a','#8d8d55'][hash%3]:['#6a864c','#718c50','#6d884b','#748e51'][hash%4]);if(path||clearing){rect(px+hash%23,py+hash%25,3,2,'#aa9e65');if(hash%4===0)rect(px+19,py+8,2,2,'#726d46');}else{const cx=px+hash%24+3,cy=py+(hash>>>5)%24+3;rect(cx,cy,1,4,'#4b7547');rect(cx-2,cy+1,1,2,'#4b7547');if(hash%8===0){rect(cx+10,cy-5,3,3,'#dcc878');rect(cx+11,cy-4,1,1,'#f5e7a5');}if(hash%11===0){rect(cx-3,cy+10,2,3,'#aeb785');}}}}
function draw(){
 const p=state.player;
 cam.x=Math.round(Math.max(0,Math.min(W*TILE-canvas.width,p.x-canvas.width/2)));
 cam.y=Math.round(Math.max(0,Math.min(H*TILE-canvas.height,p.y-canvas.height/2)));
 ctx.clearRect(0,0,canvas.width,canvas.height);ctx.save();ctx.translate(-cam.x,-cam.y);terrain();
 if(buildType){
   ctx.strokeStyle='#ebdda333';ctx.lineWidth=.5;
   for(let x=Math.floor(cam.x/TILE)*TILE;x<cam.x+canvas.width;x+=TILE){ctx.beginPath();ctx.moveTo(x,cam.y);ctx.lineTo(x,cam.y+canvas.height);ctx.stroke();}
   for(let y=Math.floor(cam.y/TILE)*TILE;y<cam.y+canvas.height;y+=TILE){ctx.beginPath();ctx.moveTo(cam.x,y);ctx.lineTo(cam.x+canvas.width,y);ctx.stroke();}
 }
 const sprites=[];
 if(state.inCave){
   for(const [x,y]of[[27.5,20],[36.5,23],[28,28],[36,19]])sprites.push({y:y*TILE,draw:()=>rock(x*TILE,y*TILE,true)});
   for(const b of bats.filter(b=>b.hp>0))sprites.push({y:b.y,draw:()=>{if(b.slowed)ellipse(b.x,b.y+10,20,7,'#a0d8d43d');batSprite(b);}});
   if(!state.crystalFound)sprites.push({y:20*TILE,draw:()=>crystal(32*TILE,20*TILE)});
   rect(31*TILE,29*TILE,64,32,'#857c53');ctx.fillStyle='#d7d6a6';ctx.font='9px monospace';ctx.textAlign='center';ctx.fillText('VÄLJAPÄÄS',32*TILE,30*TILE+16);
 }else{
   for(const b of state.buildings.filter(b=>['floor','stoneFloor'].includes(b.type)))building(b);
   sprites.push({y:base.y,draw:bench},{y:cave.y,draw:caveSprite});
   for(const b of state.buildings.filter(b=>!['floor','stoneFloor'].includes(b.type)))sprites.push({y:(b.y+.5)*TILE,draw:()=>building(b)});
   for(const a of animals)sprites.push({y:a.y,draw:()=>a.type==='rabbit'?rabbit(a):deer(a)});
   for(const z of zombies)sprites.push({y:z.y,draw:()=>{if(z.slowed)ellipse(z.x,z.y,22,8,'#a0d8d43d');zombie(z);}});
   if(state.meteorArrived){sprites.push({y:meteor.y,draw:()=>{ellipse(meteor.x,meteor.y,42,15,'#5f645247');rock(meteor.x,meteor.y,true);rect(meteor.x-4,meteor.y-17,4,7,'#cfb3e5');rect(meteor.x+8,meteor.y-8,3,5,'#d9bded');}});if(!state.alienFriend)sprites.push({y:meteor.y+30,draw:()=>alien(meteor.x+30,meteor.y+30)});}
 }
 for(const r of resources.filter(r=>!!r.inCave===state.inCave)){
   if(r.x<cam.x-60||r.x>cam.x+canvas.width+60||r.y<cam.y-30||r.y>cam.y+canvas.height+110)continue;
   if(r.alive)sprites.push({y:r.y,draw:()=>{
     if(r.type==='wood')tree(r.x,r.y,r.id%3===0?1:0);else if(['stone','ironOre','copperOre'].includes(r.type)){rock(r.x,r.y);if(r.type!=='stone'){const c=r.type==='ironOre'?'#c6cbd2':'#d79259';for(const[dx,dy]of[[-8,-15],[4,-10],[-1,-22]])rect(r.x+dx,r.y+dy,5,4,c);}}else if(r.type==='herbs')herb(r.x,r.y);else bush(r.x,r.y);
   }});
   else if(r.type==='wood'&&!r.removed){rect(r.x-6,r.y-7,12,8,'#86653e');rect(r.x-5,r.y-9,10,3,'#bfa56e');}
 }
 for(const d of state.drops.filter(d=>!!d.inCave===state.inCave))sprites.push({y:d.y,draw:()=>{shadow(d.x,d.y+3,9,3);ellipse(d.x,d.y-3,11,9,'#f0d27c33');ctx.font='13px sans-serif';ctx.textAlign='center';ctx.fillStyle='#efe1b3';ctx.fillText(icons[d.id],d.x,d.y+1);}});
 if(state.alienFriend&&state.alien.inCave===state.inCave){const a=state.alien;if(state.alienFollowing){ellipse(a.x,a.y,(state.skills.frost?160:100),22,'#b0d6c215');ctx.strokeStyle='#9bccb344';ctx.lineWidth=1;ctx.beginPath();ctx.ellipse(a.x,a.y,36,12,0,0,Math.PI*2);ctx.stroke();}sprites.push({y:a.y,draw:()=>alien(a.x,a.y)});if(!state.alienFollowing){ctx.fillStyle='#e5d69e';ctx.font='8px monospace';ctx.textAlign='center';ctx.fillText('OOTA · B / T',a.x,a.y-47);}}
 sprites.push({y:p.y,draw:()=>{if(invulnerable>0&&Math.floor(elapsed*10)%2===0)ctx.globalAlpha=.5;simm(p.x,p.y);ctx.globalAlpha=1;}});
 sprites.sort((a,b)=>a.y-b.y);for(const s of sprites)s.draw();
 if(currentTarget&&!paused&&!buildType){
   const t=currentTarget;ctx.strokeStyle='#f4d887';ctx.lineWidth=1.5;ctx.beginPath();ctx.ellipse(t.x,t.y+2,t.kind==='cave'?47:t.kind==='bench'?28:20,7,0,0,Math.PI*2);ctx.stroke();
   ctx.fillStyle='#ffe5a8';ctx.font='8px monospace';ctx.textAlign='center';ctx.fillText('A / E',t.x,t.y-((t.kind==='resource'&&t.ref.alive&&t.ref.type==='wood')?97:40));
 }
 // The facing marker is visible even when there is no enemy to target.
 if(started&&!paused){
   const ax=p.x+aim.x*29,ay=p.y-10+aim.y*29;
   ctx.save();ctx.translate(ax,ay);ctx.rotate(Math.atan2(aim.y,aim.x));poly([[6,0],[-4,-4],[-2,0],[-4,4]],'#ffe39bbf');ctx.restore();
   if(tools[tool].id==='bow'){
     const stats=bowStats(state,charge?.time||0);ctx.strokeStyle=charge?'#f7dc8ecc':'#e5d29177';ctx.lineWidth=1;ctx.setLineDash([3,5]);ctx.beginPath();ctx.moveTo(p.x+aim.x*20,p.y-10+aim.y*20);ctx.lineTo(p.x+aim.x*stats.range,p.y-10+aim.y*stats.range);ctx.stroke();ctx.setLineDash([]);
     const x=p.x+aim.x*15,y=p.y-15+aim.y*15;ctx.strokeStyle='#c7a466';ctx.lineWidth=2;ctx.beginPath();ctx.arc(x,y,10,Math.atan2(aim.y,aim.x)-1.1,Math.atan2(aim.y,aim.x)+1.1);ctx.stroke();
     if(charge){rect(p.x-17,p.y+11,34,4,'#243c2c');rect(p.x-17,p.y+11,Math.round(stats.power*34),4,'#edd38a');}
   }
 }
 for(const a of arrows.filter(a=>a.inCave===state.inCave)){const n=Math.hypot(a.vx,a.vy);ctx.strokeStyle='#f3dda0';ctx.lineWidth=2;ctx.beginPath();ctx.moveTo(a.x-a.vx/n*10,a.y-a.vy/n*10);ctx.lineTo(a.x,a.y);ctx.stroke();}
 if(fishing){ctx.strokeStyle='#e8d9a1';ctx.lineWidth=1;ctx.beginPath();ctx.moveTo(p.x+9,p.y-17);ctx.lineTo(fishing.x,fishing.y);ctx.stroke();ellipse(fishing.x,fishing.y,3,2,'#f0ba79');}
 for(const a of particles){ctx.globalAlpha=Math.max(0,a.life/.7);rect(a.x,a.y,3,3,a.color);}ctx.globalAlpha=1;
 if(buildType){const point=buildPoint(),loc=placement(point.x,point.y);ctx.globalAlpha=.5;building({x:loc.gx,y:loc.gy,type:buildType,...(rotation!=='auto'?{rotation}:{})});ctx.globalAlpha=1;ctx.strokeStyle=loc.valid?'#c7e795':'#f2aa8d';ctx.lineWidth=2;ctx.strokeRect(loc.gx*TILE+1,loc.gy*TILE+1,30,30);}
 for(let i=0;i<16;i++){const x=cam.x+((i*137+elapsed*3)%(canvas.width+30)),y=cam.y+(i*83%canvas.height)+Math.sin(elapsed+i)*7;ctx.globalAlpha=.2+Math.sin(elapsed*2+i)*.13;rect(x,y,2,2,state.time>=300?'#f0dc8c':'#e3dd9c');}ctx.globalAlpha=1;ctx.restore();
 const night=state.time>=300,dark=state.inCave?.35:night?.40:state.time>270?(state.time-270)/30*.25:0;
 if(dark){ctx.fillStyle=`rgba(8,20,38,${dark})`;ctx.fillRect(0,0,canvas.width,canvas.height);const x=p.x-cam.x,y=p.y-cam.y,g=ctx.createRadialGradient(x,y-10,12,x,y-10,tools[tool].id==='torch'?150:80);g.addColorStop(0,'rgba(249,216,113,.16)');g.addColorStop(1,'rgba(249,216,113,0)');ctx.fillStyle=g;ctx.fillRect(0,0,canvas.width,canvas.height);}
 if(started&&!state.crystalFound&&!state.inCave){const x=canvas.width-35,y=canvas.height-105,angle=Math.atan2(cave.y-p.y,cave.x-p.x);ellipse(x,y,16,16,'#173024be');ctx.save();ctx.translate(x,y);ctx.rotate(angle);poly([[10,0],[-5,-5],[-2,0],[-5,5]],'#e9d388');ctx.restore();ctx.fillStyle='#d5d5ad';ctx.font='7px monospace';ctx.textAlign='center';ctx.fillText('KOOBAS',x,y+26);}
}
function resize(){const r=canvas.getBoundingClientRect();canvas.width=Math.max(1,Math.round(r.width/2));canvas.height=Math.max(1,Math.round(r.height/2));ctx.imageSmoothingEnabled=false;}
new ResizeObserver(resize).observe(canvas);resize();refresh();
function frame(time){const dt=last?Math.min((time-last)/1000,.05):0;last=time;const pad=readPad();if(!document.hidden){update(dt,pad);draw();}updateAudio({moving:state.player.walk>0,night:state.time>=300,inCave:state.inCave,nearFire:!!nearFire()?.fuel,paused:paused||!started||!!death||document.hidden});requestAnimationFrame(frame);}requestAnimationFrame(frame);
