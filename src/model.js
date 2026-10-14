export function freshState(){return {inventory:{wood:0,stone:0,berries:0,crystal:0,star:0,herbs:0,meat:0,roast:0,stew:0},bagSlots:20,gathered:{wood:0,stone:0,berries:0},tools:['hand','axe'],buildings:[],skills:{combat:0,craft:0,gather:0,star:0},level:1,xp:0,points:0,health:5,hunger:100,day:1,time:0,crystalFound:false,alienFriend:false,meteorArrived:false,inCave:false};}
export const recipes=[
{id:'pickaxe',name:'Kivikirka',icon:'⛏️',cost:{wood:5}},
{id:'torch',name:'Tõrvik',icon:'🔥',cost:{wood:3,berries:1}},
{id:'bow',name:'Vibu',icon:'🏹',cost:{wood:10,stone:3}},
{id:'bag',name:'Suurem seljakott (+5 pesa)',icon:'🎒',cost:{wood:20,star:2},upgrade:true},
{id:'roast',name:'Küpsetatud liha',icon:'🍗',cost:{meat:1},cook:true},
{id:'stew',name:'Metsahautis',icon:'🍲',cost:{berries:2,meat:1,herbs:1},cook:true},
{id:'fire',name:'Lõke',icon:'🔥',cost:{wood:5,stone:4},build:true},
{id:'floor',name:'Puitpõrand',icon:'▦',cost:{wood:1},build:true},
{id:'wall',name:'Puitsein',icon:'▤',cost:{wood:2},build:true},
{id:'door',name:'Uks',icon:'▥',cost:{wood:3},build:true},
{id:'nest',name:'Tulnuka pesa',icon:'🛸',cost:{wood:8,star:2},build:true}
];
export const skills=[
{id:'combat',name:'Vapper vibukütt',icon:'⚔',description:'Iga aste annab +1 löögijõudu ja ühe lisasüdame.'},
{id:'craft',name:'Nutikas meister',icon:'⚒',description:'Iga aste vähendab meisterdamise ja ehitamise kulu 10%.'},
{id:'gather',name:'Metsa sõber',icon:'❧',description:'Iga aste annab korjates lisamaterjali ja kiirendab tööd.'},
{id:'star',name:'Täheleiutaja',icon:'✦',description:'Nups töötab iga astmega kiiremini. Tema pesa särab tähevalguses.'}
];
export function canPay(s,cost){return Object.entries(cost).every(([k,v])=>Number.isFinite(v)&&v>=0&&(s.inventory[k]||0)>=v);}
export function pay(s,cost){if(!canPay(s,cost))return false;for(const[k,v]of Object.entries(cost))s.inventory[k]-=v;return true;}
export function gainXP(s,n){s.xp+=n;while(s.xp>=s.level*35){s.xp-=s.level*35;s.level++;s.points++;}}
export function upgrade(s,id){if(!skills.some(x=>x.id===id)||s.points<1||(s.skills[id]||0)>=3)return false;s.points--;s.skills[id]=(s.skills[id]||0)+1;if(id==='combat')s.health++;return true;}
export function advanceTime(s,dt){s.time+=dt;while(s.time>=360){s.time-=360;s.day++;}s.hunger=Math.max(0,s.hunger-dt*.055);}

export const STACK_SIZE=20;
export function usedSlots(s){return Object.values(s.inventory).reduce((n,v)=>n+Math.ceil(v/STACK_SIZE),0);}
export function addItem(s,id,amount){if(!Object.hasOwn(s.inventory,id)||!Number.isInteger(amount)||amount<0)return false;const old=s.inventory[id];s.inventory[id]+=amount;if(usedSlots(s)>(s.bagSlots||20)){s.inventory[id]=old;return false;}return true;}
export function cook(s,recipe){if(!recipe.cook||!canPay(s,recipe.cost))return false;const next={...s,inventory:{...s.inventory}};pay(next,recipe.cost);if(!addItem(next,recipe.id,1))return false;s.inventory=next.inventory;return true;}
