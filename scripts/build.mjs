import { readFile, mkdir, writeFile } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import path from 'node:path';
const root=path.resolve(fileURLToPath(new URL('..',import.meta.url)));
let html=await readFile(path.join(root,'index.html'),'utf8');
let css=await readFile(path.join(root,'src/style.css'),'utf8');
for(const name of ['dm-sans','outfit']){
 const data=await readFile(path.join(root,`assets/fonts/${name}.ttf`));
 css=css.replace(`/assets/fonts/${name}.ttf`,`data:font/ttf;base64,${data.toString('base64')}`);
}
const sources=await Promise.all(['model','audio','game'].map(name=>readFile(path.join(root,`src/${name}.js`),'utf8')));
const clean=s=>s.replace(/^import .*;\n/gm,'').replace(/^export /gm,'');
const js=[clean(sources[0]),`const {toggleAudio,sound,updateAudio}=(()=>{${clean(sources[1])}\nreturn {toggleAudio,sound,updateAudio};})();`,clean(sources[2])].join('\n');
html=html.replace('<link rel="stylesheet" href="/src/style.css">',`<style>${css}</style>`).replace('<script type="module" src="/src/game.js"></script>',()=>`<script type="module">${js}</script>`);
const licenses=await Promise.all(['DM-Sans-OFL.txt','Outfit-OFL.txt'].map(name=>readFile(path.join(root,'assets/fonts',name),'utf8')));
html=html.replace('</body>',()=>`<script type="text/plain" id="font-licenses">${licenses.join('\n\n')}</script></body>`);
html=html.replace('href="/" aria-label="Simm avaleht"','href="#" aria-label="Simm avaleht"');
await mkdir(path.join(root,'play'),{recursive:true});
await writeFile(path.join(root,'play/index.html'),html);
console.log('Built play/index.html — open directly in a browser, or upload play/ to a static host.');
