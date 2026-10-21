import { readFile, mkdir, writeFile } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import path from 'node:path';
const root=path.resolve(fileURLToPath(new URL('..',import.meta.url)));
let html=await readFile(path.join(root,'src/index.html'),'utf8');
let css=await readFile(path.join(root,'src/style.css'),'utf8');
for(const name of ['dm-sans','outfit']){
 const data=await readFile(path.join(root,`assets/fonts/${name}.ttf`));
 css=css.replace(`/assets/fonts/${name}.ttf`,`data:font/ttf;base64,${data.toString('base64')}`);
}
const sources=await Promise.all(['i18n','model','audio','game'].map(name=>readFile(path.join(root,`src/${name}.js`),'utf8')));
const clean=s=>s.replace(/^import .*;\n/gm,'').replace(/^export /gm,'');
const modelBindings=sources[3].match(/import \{ (.*) \} from '\.\/model.js';/)[1].replace(/ as /g,':');
const modelExports=[...sources[1].matchAll(/^export (?:const|function) (\w+)/gm)].map(m=>m[1]).join(',');
const js=[clean(sources[0]),`const {${modelBindings}}=(()=>{${clean(sources[1])}\nreturn {${modelExports}};})();`,`const {toggleAudio,sound,updateAudio,setVolume}=(()=>{${clean(sources[2])}\nreturn {toggleAudio,sound,updateAudio,setVolume};})();`,clean(sources[3])].join('\n');
html=html.replace('<link rel="stylesheet" href="/src/style.css">',`<style>${css}</style>`).replace('<script type="module" src="/src/game.js"></script>',()=>`<script type="module">${js}</script>`);
for(const name of ['woodland-atlas.png','simm-walk.png','campsite-atlas.png','npcs-v05.png']){const data=await readFile(path.join(root,'assets/art',name));html=html.replaceAll(`/assets/art/${name}`,`data:image/png;base64,${data.toString('base64')}`);}
const licenses=await Promise.all(['DM-Sans-OFL.txt','Outfit-OFL.txt'].map(name=>readFile(path.join(root,'assets/fonts',name),'utf8')));
html=html.replace('</body>',()=>`<script type="text/plain" id="font-licenses">${licenses.join('\n\n')}</script></body>`);
html=html.replace('href="/" aria-label="Simm avaleht"','href="#" aria-label="Simm avaleht"');
await mkdir(path.join(root,'play'),{recursive:true});
await writeFile(path.join(root,'index.html'),html);
await writeFile(path.join(root,'play/index.html'),html);
console.log('Built index.html and play/index.html — open directly in a browser, or upload play/ to a static host.');
