export const STACK_SIZE = 20;
export const DROP_LIFETIME = 600;
export const names = {wood:'Puit',stone:'Kivi',berries:'Marjad',crystal:'Kristall',star:'Tähemetall',herbs:'Maitsetaim',meat:'Metsloomaliha',roast:'Küpseliha',stew:'Metsahautis',ironOre:'Rauamaak',copperOre:'Vasemaak',iron:'Rauakang',copper:'Vasekang',slab:'Kiviplaat',fish:'Kala',cookedFish:'Küpsetatud kala'};
export const icons = {wood:'🪵',stone:'🪨',berries:'🫐',crystal:'💎',star:'✦',herbs:'🌿',meat:'🥩',roast:'🍗',stew:'🍲',ironOre:'◈',copperOre:'◆',iron:'▰',copper:'▰',slab:'▱',fish:'🐟',cookedFish:'🍢'};
export const tools = [{id:'hand',icon:'✋',name:'Käsi'},{id:'axe',icon:'🪓',name:'Kirves'},{id:'pickaxe',icon:'⛏️',name:'Kirka'},{id:'bow',icon:'🏹',name:'Vibu'},{id:'torch',icon:'🔥',name:'Tõrvik'},{id:'rod',icon:'🎣',name:'Õng'}];
export function freshState() {
  return {inventory:Object.fromEntries(Object.keys(names).map(k=>[k,0])),bagSlots:20,gathered:{wood:0,stone:0,berries:0},tools:['hand','axe'],buildings:[],skills:{combat:0,craft:0,gather:0,star:0},level:1,xp:0,points:0,health:5,hunger:100,day:1,time:0,worldAge:0,drops:[],crystalFound:false,alienFriend:false,alienFollowing:true,alien:null,shelterFound:false,nightsSurvived:0,beaconBuilt:false,meteorArrived:false,inCave:false,stumpsRemoved:[]};
}
export const recipes = [
{id:'pickaxe',name:'Kivikirka',icon:'⛏️',cost:{wood:5}},
{id:'torch',name:'Tõrvik',icon:'🔥',cost:{wood:3,berries:1}},
{id:'bow',name:'Vibu',icon:'🏹',cost:{wood:10,stone:3}},
{id:'rod',name:'Õng',icon:'🎣',cost:{wood:6,herbs:2}},
{id:'ironAxe',name:'Raudkirves',icon:'🪓',cost:{wood:5,iron:2},gear:'axe'},
{id:'copperPickaxe',name:'Vaskkirka',icon:'⛏️',cost:{wood:4,copper:2},gear:'pickaxe'},
{id:'bag',name:'Suurem seljakott (+5 pesa)',icon:'🎒',cost:{wood:20,star:2},upgrade:true},
{id:'roast',name:'Küpsetatud liha',icon:'🍗',cost:{meat:1},cook:true},
{id:'stew',name:'Metsahautis',icon:'🍲',cost:{berries:2,meat:1,herbs:1},cook:true},
{id:'cookedFish',name:'Küpsetatud kala',icon:'🍢',cost:{fish:1},cook:true},
{id:'iron',name:'Rauakang',icon:'▰',cost:{ironOre:2},smelt:true},
{id:'copper',name:'Vasekang',icon:'▰',cost:{copperOre:2},smelt:true},
{id:'slab',name:'Kiviplaat',icon:'▱',cost:{stone:2},smelt:true,quantity:2},
{id:'fire',name:'Lõke',icon:'🔥',cost:{wood:5,stone:4},build:true},
{id:'furnace',name:'Sulatusahi',icon:'▣',cost:{stone:12,wood:4},build:true},
{id:'floor',name:'Puitpõrand',icon:'▦',cost:{wood:1},build:true},
{id:'wall',name:'Puitsein',icon:'▤',cost:{wood:2},build:true},
{id:'door',name:'Uks',icon:'▥',cost:{wood:3},build:true},
{id:'stoneFloor',name:'Kivipõrand',icon:'▱',cost:{slab:1},build:true},
{id:'beacon',name:'Tähemajakas',icon:'✦',cost:{wood:10,star:4,crystal:2,iron:2,copper:2},build:true},
{id:'nest',name:'Tulnuka pesa',icon:'🛸',cost:{wood:8,star:2},build:true}
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
export function dropItem(s,id,x,y,inCave=false){if(!s.inventory[id])return false;s.inventory[id]--;s.drops.push({id,amount:1,x,y,inCave,expires:(s.worldAge||0)+DROP_LIFETIME});return true;}
export function bowStats(s,charge){const power=Math.min(1,Math.max(0,charge)/(s.skills.quickdraw ? .78 : 1.2));return {power,range:120+power*300,speed:220+power*220,damage:1+power*3+(s.skills.combat||0)+(s.skills.quickdraw?1:0)};}
export function inWater(x,y){const tx=x/32,ty=y/32;return ((tx-15)**2/36+(ty-19)**2/65<1)||((tx-53)**2/32+(ty-39)**2/27<1);}
export function wallOrientation(b,buildings){if(b.rotation)return b.rotation;const neighbor=(dx,dy)=>buildings.some(n=>n!==b&&(n.type==='wall'||n.type==='door')&&n.x===b.x+dx&&n.y===b.y+dy);return neighbor(0,1)||neighbor(0,-1)?'v':'h';}

export function questSteps(s){return [
 {title:'Esimesed varud',text:'Vali kirves ja korja puust vähemalt viis puitu.',done:(s.gathered.wood||0)>=5},
 {title:'Tööriistad seikluseks',text:'Mine meisterdamislaua kõrvale ja valmista kirka.',done:s.tools.includes('pickaxe')},
 {title:'Valgus pimeduses',text:'Meisterda tõrvik: vajad kolme puitu ja ühte marja.',done:s.tools.includes('torch')},
 {title:'Metsa saladus',text:'Mine põhja pool asuvasse koopasse ja leia metsakristall.',done:s.crystalFound},
 {title:'Sõber tähtedelt',text:'Leia ida poolt meteoriit ja ütle Nupsile tere.',done:s.alienFriend},
 {title:'Oma paik maailmas',text:'Ehita suletud tuba seinte ja uksega, siis astu oma koju sisse.',done:s.shelterFound},
 {title:'Kolm tähistaevast',text:`Ela üle kolm ööd. Seni üle elatud: ${s.nightsSurvived||0}/3.`,done:(s.nightsSurvived||0)>=3},
 {title:'Tähemajakas',text:'Sulata metallid ja ehita kristallist tähemajakas — sinu baasi särav süda.',done:s.beaconBuilt}
];}
