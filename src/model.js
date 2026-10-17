export const STACK_SIZE = 20;
export const DROP_LIFETIME = 600;
export const names = {wood:'Puit',stone:'Kivi',berries:'Marjad',crystal:'Kristall',star:'Tähemetall',herbs:'Maitsetaim',meat:'Metsloomaliha',roast:'Küpseliha',stew:'Metsahautis',ironOre:'Rauamaak',copperOre:'Vasemaak',iron:'Rauakang',copper:'Vasekang',slab:'Kiviplaat',fish:'Kala',cookedFish:'Küpsetatud kala',carrot:'Porgand',potato:'Kartul',magicFlower:'Võlulill',healPotion:'Tervendav jook',speedPotion:'Kiirusejook',peacePotion:'Loomasõbra jook',water:'Joogivesi',pearl:'Merepärl',fiber:'Taimekiud',sand:'Liiv',glass:'Klaas',bakedPotato:'Küpsekartul'};
export const icons = {wood:'🪵',stone:'🪨',berries:'🫐',crystal:'💎',star:'✦',herbs:'🌿',meat:'🥩',roast:'🍗',stew:'🍲',ironOre:'◈',copperOre:'◆',iron:'▰',copper:'▰',slab:'▱',fish:'🐟',cookedFish:'🍢',carrot:'🥕',potato:'🥔',magicFlower:'✿',healPotion:'♥',speedPotion:'➤',peacePotion:'❧',water:'💧',pearl:'◉',fiber:'〰',sand:'▧',glass:'◇',bakedPotato:'🥔'};
export const tools = [{id:'hand',icon:'✋',name:'Käsi'},{id:'axe',icon:'🪓',name:'Kirves'},{id:'pickaxe',icon:'⛏️',name:'Kirka'},{id:'bow',icon:'🏹',name:'Vibu'},{id:'torch',icon:'🔥',name:'Tõrvik'},{id:'rod',icon:'🎣',name:'Õng'}];
export function freshState() {
  return {inventory:Object.fromEntries(Object.keys(names).map(k=>[k,0])),bagSlots:20,gathered:{wood:0,stone:0,berries:0},tools:['hand','axe'],buildings:[],skills:{combat:0,craft:0,gather:0,star:0},level:1,xp:0,points:0,health:5,hunger:100,day:1,time:0,worldAge:0,drops:[],crystalFound:false,alienFriend:false,alienFollowing:true,alien:null,shelterFound:false,nightsSurvived:0,beaconBuilt:false,meteorArrived:false,inCave:false,stumpsRemoved:[],regrowth:{},wildlifeReturns:[],effects:{},thirst:100,heat:0,camera:0,jump:0,interior:null,roomItems:[],npcQuests:{},harvested:0,whalesReleased:0,boatId:null};
}
export const recipes = [
{id:'fiber',name:'Taimekiud',icon:'〰',cost:{herbs:1},quantity:3,item:true,hand:true},
{id:'axe',name:'Kivikirves',icon:'🪓',cost:{wood:3,stone:4,fiber:1}},
{id:'pickaxe',name:'Kivikirka',icon:'⛏️',cost:{wood:3,stone:3,fiber:1}},
{id:'torch',name:'Tõrvik',icon:'🔥',cost:{wood:2,fiber:1}},
{id:'bow',name:'Vibu',icon:'🏹',cost:{wood:6,fiber:3}},
{id:'rod',name:'Õng',icon:'🎣',cost:{wood:4,fiber:2}},
{id:'ironAxe',name:'Raudkirves',icon:'🪓',cost:{wood:3,iron:2,fiber:1},gear:'axe'},
{id:'copperPickaxe',name:'Vaskkirka',icon:'⛏️',cost:{wood:3,copper:2,fiber:1},gear:'pickaxe'},
{id:'bag',name:'Suurem seljakott (+5 pesa)',icon:'🎒',cost:{fiber:12,herbs:2},upgrade:true},
{id:'roast',name:'Küpsetatud liha',icon:'🍗',cost:{meat:1},cook:true},
{id:'bakedPotato',name:'Küpsekartul',icon:'🥔',cost:{potato:1},cook:true},
{id:'stew',name:'Metsahautis',icon:'🍲',cost:{meat:1,carrot:1,potato:1,herbs:1,water:1},cook:true},
{id:'cookedFish',name:'Küpsetatud kala',icon:'🍢',cost:{fish:1},cook:true},
{id:'iron',name:'Rauakang',icon:'▰',cost:{ironOre:2},smelt:true},
{id:'copper',name:'Vasekang',icon:'▰',cost:{copperOre:2},smelt:true},
{id:'slab',name:'Kiviplaat',icon:'▱',cost:{stone:2},smelt:true},
{id:'glass',name:'Klaas',icon:'◇',cost:{sand:2},smelt:true},
{id:'fire',name:'Lõke',icon:'🔥',cost:{wood:5,stone:4},build:true},
{id:'furnace',name:'Sulatusahi',icon:'▣',cost:{stone:12,wood:4},build:true},
{id:'floor',name:'Puitpõrand',icon:'▦',cost:{wood:1},build:true},
{id:'wall',name:'Puitsein',icon:'▤',cost:{wood:2},build:true},
{id:'door',name:'Uks',icon:'▥',cost:{wood:3,fiber:1},build:true},
{id:'stoneFloor',name:'Kivipõrand',icon:'▱',cost:{slab:1},build:true},
{id:'beacon',name:'Tähemajakas',icon:'✦',cost:{wood:10,star:4,crystal:2,iron:2,copper:2},build:true},
{id:'roof',name:'Katus',icon:'⌂',cost:{wood:2,fiber:1},build:true},
{id:'window',name:'Aknaga sein',icon:'▣',cost:{wood:2,glass:1},build:true},
{id:'chest',name:'Hoiukast',icon:'▣',cost:{wood:6,fiber:2},build:true},
{id:'bed',name:'Voodi',icon:'▰',cost:{wood:5,fiber:6},build:true},
{id:'table',name:'Laud',icon:'▤',cost:{wood:4},build:true},
{id:'stairs',name:'Trepp',icon:'▟',cost:{wood:8},build:true},
{id:'ceiling',name:'Vahelagi',icon:'▦',cost:{wood:1},build:true},
{id:'garden',name:'Kastpeenar',icon:'❀',cost:{wood:4,stone:1},build:true},
{id:'boat',name:'Sõudepaat',icon:'⛵',cost:{wood:25,iron:2,fiber:4},build:true},
{id:'deskLamp',name:'Laualamp',icon:'♧',cost:{wood:2,copper:1,glass:1},build:true},
{id:'wallLamp',name:'Seinalatern',icon:'☼',cost:{iron:2,glass:1},build:true},
{id:'yardLamp',name:'Õuelatern',icon:'☀',cost:{wood:3,iron:1,glass:1},build:true},
{id:'crystalLamp',name:'Kristalllamp',icon:'✦',cost:{crystal:1,copper:1,stone:2},build:true},
{id:'healPotion',name:'Tervendav jook',icon:'♥',cost:{herbs:2,berries:2,water:1},item:true},
{id:'speedPotion',name:'Kiirusejook',icon:'➤',cost:{magicFlower:1,carrot:1,water:1},item:true},
{id:'peacePotion',name:'Loomasõbra jook',icon:'❧',cost:{magicFlower:1,herbs:2,water:1},item:true},
{id:'water',name:'Täida veepudel',icon:'💧',cost:{},item:true,water:true,hand:true},
{id:'nest',name:'Tulnuka pesa',icon:'🛸',cost:{wood:8,star:2,fiber:3},build:true}
];
export const skills = [
{id:'combat',branch:'combat',name:'Vapper seikleja',icon:'⚔',max:3,description:'+1 löögijõudu ja üks lisasüda igal astmel.'},
{id:'quickdraw',branch:'combat',requires:'combat',name:'Täpsuslask',icon:'🏹',max:1,description:'Vibu laeb 35% kiiremini ning laetud nool teeb rohkem kahju.'},
{id:'guardian',branch:'combat',requires:'combat',name:'Kindel süda',icon:'♥',max:1,description:'Kolm lisasüdant. Pikem puutumatus pärast pihta saamist.'},
{id:'craft',branch:'craft',name:'Nutikas meister',icon:'⚒',max:3,description:'Meisterdamine ja ehitamine maksab iga astmega 10% vähem.'},
{id:'mason',branch:'craft',requires:'craft',name:'Kivimeister',icon:'▱',max:1,description:'Sulatusahjust saad kaks korda rohkem kiviplaate.'},
{id:'smelter',branch:'craft',requires:'craft',name:'Ahjumeister',icon:'🔥',max:1,description:'Puit põleb ahjus ja lõkkes kaks korda kauem.'},
{id:'gather',branch:'gather',name:'Metsa sõber',icon:'❧',max:3,description:'Korjad rohkem materjale ning tööriistad töötavad kiiremini.'},
{id:'logger',branch:'gather',requires:'gather',name:'Puuraidur',icon:'🪓',max:1,description:'Igast puust saad veel kaks puitu. Kännud annavad kolm puitu.'},
{id:'angler',branch:'gather',requires:'gather',name:'Kalameister',icon:'🎣',max:1,description:'Iga õnnestunud püügiga saad kaks kala.'},
{id:'star',branch:'star',name:'Täheleiutaja',icon:'✦',max:3,description:'Nups aeglustab lähedasi vastaseid tugevamalt ja töötab kiiremini.'},
{id:'frost',branch:'star',requires:'star',name:'Täheudu',icon:'❄',max:1,description:'Nupsi aeglustav aura ulatub kaugemale.'},
{id:'leap',branch:'gather',requires:'gather',name:'Kõrge hüpe',icon:'↟',max:2,description:'Iga aste lubab hüpata ühe maapinna astme võrra kõrgemale.'},
{id:'helper',branch:'star',requires:'star',name:'Usin abiline',icon:'🛸',max:1,description:'Baasi jäetud Nups toob kaks korda rohkem marju.'}
];
export function canPay(s,cost){return Object.entries(cost).every(([k,v])=>Number.isFinite(v)&&v>=0&&(s.inventory[k]||0)>=v);}
export function pay(s,cost){if(!canPay(s,cost))return false;for(const[k,v]of Object.entries(cost))s.inventory[k]-=v;return true;}
export function gainXP(s,n){s.xp+=n;while(s.xp>=s.level*35){s.xp-=s.level*35;s.level++;s.points++;}}
export function maxHealth(s){return 5+(s.skills.combat||0)+(s.skills.guardian?3:0);}
export function canUpgrade(s,id){const node=skills.find(x=>x.id===id);return !!node&&s.points>0&&(s.skills[id]||0)<node.max&&(!node.requires||(s.skills[node.requires]||0)>0);}
export function upgrade(s,id){if(!canUpgrade(s,id))return false;const before=maxHealth(s);s.points--;s.skills[id]=(s.skills[id]||0)+1;s.health+=maxHealth(s)-before;return true;}
export function advanceTime(s,dt){s.worldAge=(s.worldAge||0)+dt;s.time+=dt;while(s.time>=360){s.time-=360;s.day++;}s.hunger=Math.max(0,s.hunger-dt*.045);s.drops=(s.drops||[]).filter(d=>d.expires>s.worldAge);}
export function usedSlots(s){return Object.values(s.inventory).reduce((n,v)=>n+Math.ceil(v/STACK_SIZE),0);}
export function addItem(s,id,amount){if(!Object.hasOwn(s.inventory,id)||!Number.isInteger(amount)||amount<0)return false;const old=s.inventory[id];s.inventory[id]+=amount;if(usedSlots(s)>(s.bagSlots||20)){s.inventory[id]=old;return false;}return true;}
export function cook(s,recipe){if((!recipe.cook&&!recipe.smelt)||!canPay(s,recipe.cost))return false;const next={...s,inventory:{...s.inventory}};pay(next,recipe.cost);const n=(recipe.quantity||1)*(recipe.id==='slab'&&s.skills.mason?2:1);if(!addItem(next,recipe.id,n))return false;s.inventory=next.inventory;return true;}
export function dropItem(s,id,x,y,inCave=false){if(!s.inventory[id])return false;s.inventory[id]--;s.drops.push({id,amount:1,x,y,inCave,room:s.interior?.id||null,level:s.interior?.level||0,expires:(s.worldAge||0)+DROP_LIFETIME});return true;}
export function bowStats(s,charge){const power=Math.min(1,Math.max(0,charge)/(s.skills.quickdraw ? .78 : 1.2));return {power,range:120+power*300,speed:220+power*220,damage:1+power*3+(s.skills.combat||0)+(s.skills.quickdraw?1:0)};}
export function lakeWater(x,y){const tx=x/32,ty=y/32;return ((tx-15)**2/36+(ty-19)**2/65<1)||((tx-53)**2/32+(ty-39)**2/27<1);}
export function wallOrientation(b,buildings){if(b.rotation)return b.rotation;const neighbor=(dx,dy)=>buildings.some(n=>n!==b&&['wall','door','window'].includes(n.type)&&n.x===b.x+dx&&n.y===b.y+dy);return neighbor(0,1)||neighbor(0,-1)?'v':'h';}

export function questSteps(s){return [
 {title:'Esimesed varud',text:'Korja maast oksi või raiu kirvega puud. Kogu viis puitu.',done:(s.gathered.wood||0)>=5},
 {title:'Tööriistad seikluseks',text:'Kivikirka vajab 3 puitu, 3 väikest kivi ja 1 taimekiudu. Kiud saad maitsetaimest; kirka valmista laual.',done:s.tools.includes('pickaxe')},
 {title:'Valgus pimeduses',text:'Meisterda tõrvik: 2 puitu ja 1 taimekiud tahiks.',done:s.tools.includes('torch')},
 {title:'Metsa saladus',text:'Mine põhja pool asuvasse koopasse ja leia metsakristall.',done:s.crystalFound},
 {title:'Sõber tähtedelt',text:'Leia ida poolt meteoriit ja ütle Nupsile tere.',done:s.alienFriend},
 {title:'Oma paik maailmas',text:'Ehita suletud tuba seinte ja uksega, siis astu oma koju sisse.',done:s.shelterFound},
 {title:'Kolm tähistaevast',text:`Ela üle kolm ööd. Seni üle elatud: ${s.nightsSurvived||0}/3.`,done:(s.nightsSurvived||0)>=3},
 {title:'Tähemajakas',text:'Sulata metallid ja ehita kristallist tähemajakas — sinu baasi särav süda.',done:s.beaconBuilt}
];}

// Version 0.4 systems use game seconds, including while away from a biome.
export function inWater(x,y){const cx=(Math.floor(x/32)+.5)*32,cy=(Math.floor(y/32)+.5)*32;return cx>=58*32||Math.hypot(cx-50*32,cy-16*32)<48||lakeWater(cx,cy);}
export function biomeAt(x,y){return x>=58*32?'sea':x>44*32&&y<22*32?'desert':'forest';}
export function heightAt(x,y){
 if(inWater(x,y))return 0;const tx=Math.floor(x/32),ty=Math.floor(y/32);if(Math.hypot(tx+.5-31,ty+.5-29)<6.5)return 0;
 if(biomeAt(x,y)==='desert')return Math.max(0,Math.floor(1.4+Math.sin(tx*.65)*Math.cos(ty*.4)*1.6));
 const hills=[[23,28,5,2],[39,36,6,3],[21,9,5,2],[43,9,4,2]];
 return hills.reduce((h,[cx,cy,r,top])=>Math.max(h,Math.max(0,Math.ceil(top*(1-Math.hypot(tx-cx,ty-cy)/r)))),0);
}
export function canStep(s,x,y,jumping=s.jump>0){return heightAt(x,y)<=(jumping?(s.jumpOrigin??heightAt(s.player.x,s.player.y))+1+(s.skills.leap||0):heightAt(s.player.x,s.player.y));}
export function rotateVector(x,y,quarter=0){const q=((quarter%4)+4)%4;return q===0?{x,y}:q===1?{x:-y,y:x}:q===2?{x:-x,y:-y}:{x:y,y:-x};}
export function projectPoint(x,y,quarter=0,height=heightAt(x,y)){const r=rotateVector(x,y,quarter);return {x:r.x,y:r.y*.62-height*12};}
export function sameScene(a,b){return (a.room||null)===(b.interior?.id||null)&&(a.level||0)===(b.interior?.level||0);}
export function sceneBuildings(s){return s.interior?s.roomItems.filter(b=>sameScene(b,s)):s.buildings;}
export function nearbyChests(s,radius=120){return sceneBuildings(s).filter(b=>b.type==='chest'&&Math.hypot((b.x+.5)*32-s.player.x,(b.y+.5)*32-s.player.y)<=radius);}
export function availableInventory(s){const inventory={...s.inventory};for(const b of nearbyChests(s))for(const[k,v]of Object.entries(b.items||{}))inventory[k]=(inventory[k]||0)+v;return inventory;}
export function payNearby(s,cost){if(!canPay({inventory:availableInventory(s)},cost))return false;for(const[k,v]of Object.entries(cost)){let left=v,own=Math.min(left,s.inventory[k]||0);s.inventory[k]-=own;left-=own;for(const b of nearbyChests(s)){const n=Math.min(left,b.items?.[k]||0);if(n){b.items[k]-=n;left-=n;}}}return true;}
export function transferItem(s,chest,id,toChest,amount=1){
 if(!names[id]||!Number.isInteger(amount)||amount<1)return false;chest.items??={};
 if(toChest){if((s.inventory[id]||0)<amount)return false;s.inventory[id]-=amount;chest.items[id]=(chest.items[id]||0)+amount;}
 else{if((chest.items[id]||0)<amount||!addItem(s,id,amount))return false;chest.items[id]-=amount;}return true;
}
export function craftItem(s,recipe,cost=recipe.cost){
 if(!(recipe.item||recipe.cook||recipe.smelt)||!canPay({inventory:availableInventory(s)},cost))return false;
 const inventory={...s.inventory},chests=nearbyChests(s),backups=chests.map(c=>({...c.items}));
 payNearby(s,cost);if(addItem(s,recipe.id,(recipe.quantity||1)*(recipe.id==='slab'&&s.skills.mason?2:1)))return true;
 s.inventory=inventory;chests.forEach((c,i)=>c.items=backups[i]);return false;
}
export const crops={carrot:{name:'Porgand',duration:180,yield:3},potato:{name:'Kartul',duration:240,yield:4},berries:{name:'Marjad',duration:210,yield:3},herbs:{name:'Ravimtaimed',duration:180,yield:3},magicFlower:{name:'Võlulilled',duration:300,yield:2}};
export function plantCrop(s,bed,crop){if(bed.crop||!crops[crop])return false;bed.crop=crop;bed.planted=s.worldAge;return true;}
export function cropProgress(s,bed){return bed.crop?Math.min(1,Math.max(0,(s.worldAge-bed.planted)/crops[bed.crop].duration)):0;}
export function harvestCrop(s,bed){if(cropProgress(s,bed)<1)return false;if(!addItem(s,bed.crop,crops[bed.crop].yield))return false;bed.crop=null;s.harvested++;gainXP(s,10);return true;}
export function usePotion(s,id){if(!s.inventory[id])return false;
 if(id==='healPotion'){if(s.health>=maxHealth(s))return false;s.health=Math.min(maxHealth(s),s.health+4);}
 else if(id==='speedPotion')s.effects.speed=90;else if(id==='peacePotion')s.effects.peace=120;else return false;s.inventory[id]--;return true;
}
export function tickEffects(s,dt){for(const k of Object.keys(s.effects))s.effects[k]=Math.max(0,s.effects[k]-dt);s.jump=Math.max(0,(s.jump||0)-dt);}
export function regrowResources(s,resources){for(const r of resources){if(r.inCave||r.alive||!['wood','herbs','berries','cactus',...Object.keys(forageDefs)].includes(r.type))continue;
 const due=s.regrowth[r.id]??(s.regrowth[r.id]=s.worldAge+(r.type==='wood'?1080:r.type==='pebble'?720:360));
 if(s.worldAge<due||s.buildings.some(b=>Math.abs((b.x+.5)*32-r.x)<30&&Math.abs((b.y+.5)*32-r.y)<30))continue;
 r.alive=true;r.removed=false;r.hp=3;delete s.regrowth[r.id];}}
export function predatorIntent(a,p,peace=false){const d=Math.hypot(a.x-p.x,a.y-p.y),home=Math.hypot(p.x-a.homeX,p.y-a.homeY);
 if(peace){a.chasing=false;return 'home';}if(a.type==='bear'){a.chasing=home<125;return a.chasing?'chase':'home';}
 if(d<150)a.chasing=true;if(d>350)a.chasing=false;return a.chasing?'chase':'home';}
export function findHouses(buildings){
 const floors=buildings.filter(b=>['floor','stoneFloor'].includes(b.type)),tiles=new Map(floors.map(b=>[b.x+','+b.y,b])),seen=new Set(),houses=[];
 for(const f of floors){const key=f.x+','+f.y;if(seen.has(key))continue;const group=[],stack=[f];
 while(stack.length){const b=stack.pop(),k=b.x+','+b.y;if(seen.has(k))continue;seen.add(k);group.push(b);for(const[dx,dy]of[[1,0],[-1,0],[0,1],[0,-1]]){const n=tiles.get((b.x+dx)+','+(b.y+dy));if(n&&!seen.has(n.x+','+n.y))stack.push(n);}}
 const width=Math.max(...group.map(b=>b.x))-Math.min(...group.map(b=>b.x))+1,height=Math.max(...group.map(b=>b.y))-Math.min(...group.map(b=>b.y))+1;if(group.length!==width*height)continue;
 const keys=new Set(group.map(b=>b.x+','+b.y)),boundary=group.filter(b=>[[1,0],[-1,0],[0,1],[0,-1]].some(([dx,dy])=>!keys.has((b.x+dx)+','+(b.y+dy))));
 const at=(b,types)=>buildings.find(n=>n.x===b.x&&n.y===b.y&&types.includes(n.type)),door=boundary.map(b=>at(b,['door'])).find(Boolean);
 if(group.length>boundary.length&&door&&boundary.every(b=>at(b,['wall','door','window']))&&group.every(b=>at(b,['roof']))){const minX=Math.min(...group.map(b=>b.x)),minY=Math.min(...group.map(b=>b.y));houses.push({id:'house:'+minX+':'+minY,tiles:group,door,minX,minY,maxX:Math.max(...group.map(b=>b.x)),maxY:Math.max(...group.map(b=>b.y))});}}
 return houses;
}
export function canAscend(s){if(!s.interior)return false;const items=sceneBuildings(s),ceilings=new Set(items.filter(b=>b.type==='ceiling').map(b=>b.x+','+b.y));for(let x=2;x<=9;x++)for(let y=2;y<=7;y++)if(!ceilings.has(x+','+y))return false;return items.some(b=>b.type==='stairs');}
export const npcData=[
 {id:'ranger',name:'METSAVAHT',x:29*32,y:27*32,line:'TERE, SIMM! KASVATAME KOOS TOITU.',request:{carrot:3},reward:{herbs:4,wood:8},task:'TOO MULLE KOLM PORGANDIT.'},
 {id:'miner',name:'KAEVUR',x:35*32,y:17*32,line:'KIVID PEIDAVAD TOREDAID AARDEID!',request:{iron:2},reward:{crystal:2,copper:3},task:'TOO MULLE KAKS RAUAKANGI.'},
 {id:'trader',name:'KAUPMEES',x:43*32,y:25*32,line:'VÕLULILLED ON VÄGA VAHVAD!',request:{magicFlower:2},reward:{iron:3,water:5},task:'TOO MULLE KAKS VÕLULILLE.'}
];
export function finishNPCQuest(s,npc){if(s.npcQuests[npc.id]||!canPay(s,npc.request))return false;const next={...s,inventory:{...s.inventory}};pay(next,npc.request);for(const[k,v]of Object.entries(npc.reward))if(!addItem(next,k,v))return false;s.inventory=next.inventory;s.npcQuests[npc.id]=true;gainXP(s,35);return true;}
export function whaleStep(game,dt,held){game.time+=dt;const target=.5+Math.sin(game.time*2)*.28;game.marker=Math.max(0,Math.min(1,game.marker+(held?.72:-.48)*dt));game.target=target;game.progress=Math.max(0,Math.min(1,game.progress+(Math.abs(game.marker-target)<.2?.32:-.08)*dt));return game.progress>=1?'caught':game.time>=35?'escaped':'playing';}

export function houseExitPoint(h){const d=h.door,dx=d.y===h.minY||d.y===h.maxY?0:d.x===h.minX?-1:1,dy=d.y===h.minY?-1:d.y===h.maxY?1:0;return {x:(d.x+.5)*32+dx*42,y:(d.y+.5)*32+dy*42};}

// Loose supplies have independent IDs and RNG: adding them does not shuffle old forest saves.
export const forageDefs={branch:{item:'wood',quantity:1,label:'Korja oks',delay:360},pebble:{item:'stone',quantity:1,label:'Korja väike kivi',delay:720},sand:{item:'sand',quantity:3,label:'Korja liiva',delay:360}};
export function looseResources(){
 const result=[],put=(id,x,y,type)=>{if(!inWater(x,y))result.push({id,x,y,type,hp:1,alive:true,removed:false});};
 [[-56,88,'branch'],[72,100,'branch'],[-104,128,'branch'],[-80,32,'pebble'],[72,56,'pebble'],[-24,136,'pebble'],[104,112,'pebble'],[-112,-16,'pebble']].forEach(([dx,dy,type],i)=>put(8000+i,31*32+dx,29*32+dy,type));
 for(let y=3;y<45;y++)for(let x=3;x<61;x++){
  const hash=((Math.imul(x+17,73856093)^Math.imul(y+31,19349663))>>>0)/4294967296,px=(x+.5)*32,py=(y+.5)*32;
  if(Math.hypot(px-31*32,py-29*32)<190)continue;
  if(hash<.01&&biomeAt(px,py)==='forest')put(9000+y*64+x,px,py,'branch');else if(hash>=.01&&hash<.02)put(9000+y*64+x,px,py,'pebble');
 }
 [[48,18],[52,17],[54,13],[55,19]].forEach(([x,y],i)=>put(13000+i,(x+.5)*32,(y+.5)*32,'sand'));
 return result;
}
export function gatherLoose(s,r){const def=forageDefs[r.type];if(!def||!r.alive||!addItem(s,def.item,def.quantity))return false;r.alive=false;r.hp=0;s.gathered[def.item]=(s.gathered[def.item]||0)+def.quantity;s.regrowth[r.id]=s.worldAge+def.delay;gainXP(s,2);return true;}
// Body footprints follow the drawn wall strips, rather than blocking a 38x38 square.
export function buildingBounds(b,buildings){
 const cx=(b.x+.5)*32,cy=(b.y+.5)*32,box=(w,h)=>({x:cx-w/2,y:cy-h/2,w,h});
 if(['wall','window','door'].includes(b.type)){
  if(b.type==='door'&&b.open)return [];
  const vertical=wallOrientation(b,buildings)==='v',horizontal=!vertical||(!b.rotation&&buildings.some(n=>n!==b&&['wall','door','window'].includes(n.type)&&n.y===b.y&&Math.abs(n.x-b.x)===1));
  return [...(horizontal?[box(32,10)]:[]),...(vertical?[box(10,32)]:[])];
 }
 if(b.type==='chest')return [box(28,16)];if(b.type==='table')return [box(32,18)];if(b.type==='bed')return [box(26,30)];return [];
}
export function solidBuildingAt(buildings,x,y,radius=5){return buildings.find(b=>buildingBounds(b,buildings).some(rect=>{const dx=x-Math.max(rect.x,Math.min(x,rect.x+rect.w)),dy=y-Math.max(rect.y,Math.min(y,rect.y+rect.h));return dx*dx+dy*dy<radius*radius;}));}
