import test from 'node:test';
import assert from 'node:assert/strict';
import {tr,setLanguage,localizedData} from '../src/i18n.js';
import {freshState,firstPickaxeStep} from '../src/model.js';
test('live localized data preserves gameplay identifiers and translates nested HTML text only',()=>{setLanguage('en');const item=localizedData({id:'wood',name:'Puit'});assert.equal(item.name,'Wood');assert.equal(item.id,'wood');assert.equal(tr('<button id="Puit" class="Puit">Puit</button>'),'<button id="Puit" class="Puit">Wood</button>');setLanguage('et');assert.equal(item.name,'Puit');assert.equal(item.id,'wood');setLanguage('en');assert.equal(tr`Puudu: ${3} Puit`,'Missing: 3 Wood');assert.equal(tr('Kivikirka'),'Stone pickaxe');});
test('first-pickaxe tutorial follows available backpack and nearby chest materials',()=>{const s=freshState();s.player={x:992,y:992};assert.match(firstPickaxeStep(s).text,/Puit 0\/3/);s.inventory.wood=3;s.inventory.stone=3;s.buildings=[{type:'chest',x:31,y:31,items:{fiber:1}}];assert.match(firstPickaxeStep(s).text,/Puit 3\/3.*Kivi 3\/3.*Taimekiud 1\/1/);s.tools.push('pickaxe');assert.equal(firstPickaxeStep(s).title,'Kivikirka valmis!');});
