import test from 'node:test';
import assert from 'node:assert/strict';
import * as m from '../src/model.js';
const recipe=id=>m.recipes.find(r=>r.id===id);
test('all recipes use known positive material quantities; glass, fibre, food and tools have a reachable supply chain',()=>{
 const ids=new Set();for(const r of m.recipes){assert.ok(!ids.has(r.id));ids.add(r.id);for(const[id,n]of Object.entries(r.cost)){assert.ok(m.names[id],`${r.id}: ${id}`);assert.ok(Number.isInteger(n)&&n>0,r.id);}assert.ok(!r.quantity||Number.isInteger(r.quantity)&&r.quantity>0);}
 assert.deepEqual(recipe('pickaxe').cost,{wood:3,stone:3,fiber:1});assert.ok(recipe('bow').cost.fiber);assert.ok(!recipe('bow').cost.stone);assert.ok(recipe('torch').cost.fiber);assert.ok(!recipe('torch').cost.berries);assert.ok(recipe('window').cost.glass);assert.ok(recipe('bag').cost.fiber);assert.ok(!recipe('bag').cost.star);
 const available=new Set(['wood','stone','herbs','berries','water','meat','fish','ironOre','copperOre','star','crystal','carrot','potato','magicFlower','sand']);
 for(const type of ['zombie','skeleton','bat',...m.hostileTypes])for(const id of Object.keys(m.creatureLoot(type)))available.add(id);available.add('gold');available.add('banana');
 let progress=true;while(progress){progress=false;for(const r of m.recipes)if(!available.has(r.id)&&Object.keys(r.cost).every(k=>available.has(k))){available.add(r.output||r.id);available.add(r.id);progress=true;}}
 for(const r of m.recipes)assert.ok(Object.keys(r.cost).every(id=>available.has(id)),`unreachable recipe: ${r.id}`);
});
test('rare branches and pebbles bootstrap a stone pickaxe using only hand gathering',()=>{
 const s=m.freshState();s.tools=['hand'];const nodes=m.looseResources();assert.ok(nodes.filter(r=>r.type==='branch').length<30);assert.ok(nodes.filter(r=>r.type==='pebble').length<35);
 const near=nodes.filter(r=>Math.hypot(r.x-992,r.y-928)<190);assert.ok(near.filter(r=>r.type==='branch').length>=3);assert.ok(near.filter(r=>r.type==='pebble').length>=3);
 for(const type of ['branch','pebble'])for(const r of near.filter(r=>r.type===type).slice(0,3))assert.ok(m.gatherLoose(s,r));
 assert.equal(s.inventory.wood,3);assert.equal(s.inventory.stone,3);s.inventory.herbs=1;assert.ok(m.craftItem(s,recipe('fiber')));assert.equal(s.inventory.fiber,3);assert.ok(m.pay(s,recipe('pickaxe').cost));assert.equal(s.inventory.wood,0);assert.equal(s.inventory.stone,0);assert.equal(s.inventory.fiber,2);
});
test('loose supplies preserve items on bag overflow and regrow only away from buildings',()=>{
 const s=m.freshState(),r=m.looseResources().find(r=>r.type==='pebble');s.inventory.wood=400;assert.equal(m.gatherLoose(s,r),false);assert.equal(r.alive,true);s.inventory.wood=0;assert.ok(m.gatherLoose(s,r));assert.equal(r.alive,false);assert.equal(s.inventory.stone,1);s.worldAge=720;s.buildings=[{type:'garden',x:Math.floor(r.x/32),y:Math.floor(r.y/32)}];m.regrowResources(s,[r]);assert.equal(r.alive,false);s.buildings=[];m.regrowResources(s,[r]);assert.equal(r.alive,true);
});
test('sand melts to glass while wood alone cannot create a window or lantern',()=>{
 const s=m.freshState();assert.ok(m.gatherLoose(s,m.looseResources().find(r=>r.type==='sand')));assert.equal(s.inventory.sand,3);assert.ok(m.craftItem(s,recipe('glass')));assert.equal(s.inventory.sand,1);assert.equal(s.inventory.glass,1);s.inventory.wood=10;assert.ok(m.pay(s,recipe('window').cost));assert.equal(s.inventory.glass,0);assert.equal(m.canPay(s,recipe('deskLamp').cost),false);
});
test('water and terrain heights are constant inside every rendered tile, including shores and camp edges',()=>{
 for(let y=2;y<46;y++)for(let x=2;x<62;x++)for(const[dx,dy]of[[.01,.01],[31.99,.01],[.01,31.99],[31.99,31.99]]){
  assert.equal(m.inWater(x*32+dx,y*32+dy),m.inWater(x*32+16,y*32+16));assert.equal(m.heightAt(x*32+dx,y*32+dy),m.heightAt(x*32+16,y*32+16));
 }
 for(let y=25;y<=33;y++)for(let x=27;x<=35;x++)assert.equal(m.heightAt(x*32+16,y*32+16),0,'camp must have no hidden uphill lip');
});
test('wall collision follows thin visible strips and leaves parallel paths and open doors traversable',()=>{
 const h={type:'wall',x:31,y:31,rotation:'h'},v={...h,rotation:'v'};
 assert.equal(m.solidBuildingAt([h],1008,990),undefined);assert.equal(m.solidBuildingAt([h],1008,1008),h);
 assert.equal(m.solidBuildingAt([v],990,1008),undefined);assert.equal(m.solidBuildingAt([v],1008,1008),v);
 const room=[{type:'wall',x:30,y:31,rotation:'h'},{type:'door',x:31,y:31,rotation:'h',open:true},{type:'wall',x:32,y:31,rotation:'h'}];
 for(let y=970;y<=1040;y++)assert.equal(m.solidBuildingAt(room,1008,y),undefined);room[1].open=false;assert.equal(m.solidBuildingAt(room,1008,1008),room[1]);
 assert.equal(m.solidBuildingAt([{type:'floor',x:31,y:31},{type:'roof',x:31,y:31}],1008,1008),undefined);
});
