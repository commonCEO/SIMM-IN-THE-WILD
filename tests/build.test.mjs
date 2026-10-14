import test from 'node:test';
import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
test('root HTML in the repository ZIP is the self-contained playable build',async()=>{
 const html=await readFile(new URL('../index.html',import.meta.url),'utf8');
 const alternate=await readFile(new URL('../play/index.html',import.meta.url),'utf8');
 assert.equal(html,alternate);
 assert.ok(html.includes('<style>'));
 assert.ok(html.includes('data:font/ttf;base64,'));
 assert.ok(html.includes('data:image/png;base64,'));
 assert.doesNotMatch(html,/['"]\/assets\/art\//);
 assert.ok(html.includes('function freshState()'));
 assert.ok(html.includes('function frame(time)'));
 assert.ok(html.includes('id="font-licenses"'));
 assert.doesNotMatch(html,/<script[^>]+src=/);
 assert.doesNotMatch(html,/<link[^>]+rel="stylesheet"/);
 assert.doesNotMatch(html,/^import /m);
});
