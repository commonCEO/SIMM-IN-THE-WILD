# SIMM mängudisaini andmetabelid

Need tabelid on eksporditud brauseri praegusest andmemudelist. Reeglite ja ajalooliste erandite selgitused on [mängudisaini dokumendis](GAME-DESIGN-DOCUMENT.md). Tabeli olemasolu ei tähenda, et süsteem on Godotisse üle toodud.

Uuendamine: `node scripts/export-design-baseline.mjs`. Masinloetav paariline: [browser-design-baseline.json](browser-design-baseline.json).

## Kõik andmemudeli retseptid

Baaskulud enne oskuste soodustusi. See on mudeli täielik loend, mitte igas olukorras korraga nähtav menüü. Maja tellimused on eraldi tabelis; vana moodulmaja retseptide olemasolu ei taasta nende eemaldatud õuemenüüd.

| ID | Nimi | Baaskulu | Tulemus | Jaam või kontekst |
| --- | --- | --- | --- | --- |
| boneBow | Tugevdatud vibu | Luu × 3 + Taimekiud × 2 + Puit × 2 | Varustuse täiendus: Tugevdatud vibu | Meisterdamislaud |
| salve | Ravisalv | Trollisammal × 1 + Maitsetaim × 1 | Ravisalv × 1 | Käsitsi |
| fiberFromCloth | Taimekiud kangast | Kangas × 1 | Taimekiud × 4 | Käsitsi |
| hunterCharm | Jahimehe amulett | Kihv × 2 + Karusnahk × 2 + Taimekiud × 1 | Varustuse täiendus: Jahimehe amulett | Meisterdamislaud |
| frostLamp | Jäälatern | Jääkild × 2 + Luu × 1 + Kivi × 2 | Paigaldatav ehitis: Jäälatern | Ehitus; nähtavus sõltub stseenist |
| goldLamp | Kuldlatern | Kuld × 3 + Klaas × 1 + Puit × 2 | Paigaldatav ehitis: Kuldlatern | Ehitus; nähtavus sõltub stseenist |
| fiber | Taimekiud | Maitsetaim × 1 | Taimekiud × 3 | Käsitsi |
| axe | Kivikirves | Puit × 3 + Kivi × 4 + Taimekiud × 1 | Kirves × 1 | Meisterdamislaud |
| pickaxe | Kivikirka | Puit × 3 + Kivi × 3 + Taimekiud × 1 | Kirka × 1 | Meisterdamislaud |
| torch | Tõrvik | Puit × 2 + Taimekiud × 1 | Tõrvik × 1 | Meisterdamislaud |
| bow | Vibu | Puit × 6 + Taimekiud × 3 | Vibu × 1 | Meisterdamislaud |
| rod | Õng | Puit × 4 + Taimekiud × 2 | Õng × 1 | Meisterdamislaud |
| ironAxe | Raudkirves | Puit × 3 + Rauakang × 2 + Taimekiud × 1 | Varustuse täiendus: Raudkirves | Meisterdamislaud |
| copperPickaxe | Vaskkirka | Puit × 3 + Vasekang × 2 + Taimekiud × 1 | Varustuse täiendus: Vaskkirka | Meisterdamislaud |
| bag | Suurem seljakott (+5 pesa) | Taimekiud × 12 + Maitsetaim × 2 | +5 seljakotipesa, kuni 40 | Meisterdamislaud |
| roast | Küpsetatud liha | Metsloomaliha × 1 | Küpseliha × 1 | Lõke; kütus |
| bakedPotato | Küpsekartul | Kartul × 1 | Küpsekartul × 1 | Lõke; kütus |
| stew | Metsahautis | Metsloomaliha × 1 + Porgand × 1 + Kartul × 1 + Maitsetaim × 1 + Joogivesi × 1 | Metsahautis × 1 | Lõke; kütus |
| cookedFish | Küpsetatud kala | Kala × 1 | Küpsetatud kala × 1 | Lõke; kütus |
| iron | Rauakang | Rauamaak × 2 | Rauakang × 1 | Sulatusahi; kütus |
| copper | Vasekang | Vasemaak × 2 | Vasekang × 1 | Sulatusahi; kütus |
| slab | Kiviplaat | Kivi × 2 | Kiviplaat × 1 | Sulatusahi; kütus |
| glass | Klaas | Liiv × 2 | Klaas × 1 | Sulatusahi; kütus |
| fire | Lõke | Puit × 5 + Kivi × 4 | Paigaldatav ehitis: Lõke | Ehitus; nähtavus sõltub stseenist |
| furnace | Sulatusahi | Kivi × 12 + Puit × 4 | Paigaldatav ehitis: Sulatusahi | Ehitus; nähtavus sõltub stseenist |
| floor | Puitpõrand | Puit × 1 | Paigaldatav ehitis: Puitpõrand | Ehitus; nähtavus sõltub stseenist |
| wall | Puitsein | Puit × 2 | Paigaldatav ehitis: Puitsein | Ehitus; nähtavus sõltub stseenist |
| door | Uks | Puit × 3 + Taimekiud × 1 | Paigaldatav ehitis: Uks | Ehitus; nähtavus sõltub stseenist |
| stoneFloor | Kivipõrand | Kiviplaat × 1 | Paigaldatav ehitis: Kivipõrand | Ehitus; nähtavus sõltub stseenist |
| beacon | Tähemajakas | Puit × 10 + Tähemetall × 4 + Kristall × 2 + Rauakang × 2 + Vasekang × 2 | Paigaldatav ehitis: Tähemajakas | Ehitus; nähtavus sõltub stseenist |
| roof | Katus | Puit × 2 + Taimekiud × 1 | Paigaldatav ehitis: Katus | Ehitus; nähtavus sõltub stseenist |
| window | Aknaga sein | Puit × 2 + Klaas × 1 | Paigaldatav ehitis: Aknaga sein | Ehitus; nähtavus sõltub stseenist |
| chest | Hoiukast | Puit × 6 + Taimekiud × 2 | Paigaldatav ehitis: Hoiukast | Ehitus; nähtavus sõltub stseenist |
| bed | Voodi | Puit × 5 + Taimekiud × 6 | Paigaldatav ehitis: Voodi | Ehitus; nähtavus sõltub stseenist |
| table | Laud | Puit × 4 | Paigaldatav ehitis: Laud | Ehitus; nähtavus sõltub stseenist |
| stairs | Trepp | Puit × 8 | Paigaldatav ehitis: Trepp | Ehitus; nähtavus sõltub stseenist |
| ceiling | Vahelagi | Puit × 1 | Paigaldatav ehitis: Vahelagi | Ehitus; nähtavus sõltub stseenist |
| garden | Kastpeenar | Puit × 4 + Kivi × 1 | Paigaldatav ehitis: Kastpeenar | Ehitus; nähtavus sõltub stseenist |
| boat | Sõudepaat | Puit × 25 + Rauakang × 2 + Taimekiud × 4 | Paigaldatav ehitis: Sõudepaat | Ehitus; nähtavus sõltub stseenist |
| deskLamp | Laualamp | Puit × 2 + Vasekang × 1 + Klaas × 1 | Paigaldatav ehitis: Laualamp | Ehitus; nähtavus sõltub stseenist |
| wallLamp | Seinalatern | Rauakang × 2 + Klaas × 1 | Paigaldatav ehitis: Seinalatern | Ehitus; nähtavus sõltub stseenist |
| yardLamp | Õuelatern | Puit × 3 + Rauakang × 1 + Klaas × 1 | Paigaldatav ehitis: Õuelatern | Ehitus; nähtavus sõltub stseenist |
| crystalLamp | Kristalllamp | Kristall × 1 + Vasekang × 1 + Kivi × 2 | Paigaldatav ehitis: Kristalllamp | Ehitus; nähtavus sõltub stseenist |
| healPotion | Tervendav jook | Maitsetaim × 2 + Marjad × 2 + Joogivesi × 1 | Tervendav jook × 1 | Meisterdamislaud |
| speedPotion | Kiirusejook | Võlulill × 1 + Porgand × 1 + Joogivesi × 1 | Kiirusejook × 1 | Meisterdamislaud |
| peacePotion | Loomasõbra jook | Võlulill × 1 + Maitsetaim × 2 + Joogivesi × 1 | Loomasõbra jook × 1 | Meisterdamislaud |
| water | Täida veepudel | Materjalikulu puudub | Joogivesi × 1 | Käsitsi; veekogu lähedal |
| nest | Tulnuka pesa | Puit × 8 + Tähemetall × 2 + Taimekiud × 3 | Paigaldatav ehitis: Tulnuka pesa | Ehitus; nähtavus sõltub stseenist |

## Oskused

| ID | Haru | Nimi | Max aste | Eeldus | Mudeli kirjeldus |
| --- | --- | --- | --- | --- | --- |
| combat | combat | Vapper seikleja | 3 | Puudub | +1 löögijõudu ja üks lisasüda igal astmel. |
| quickdraw | combat | Täpsuslask | 1 | combat | Vibu laeb 35% kiiremini ning laetud nool teeb rohkem kahju. |
| guardian | combat | Kindel süda | 1 | combat | Kolm lisasüdant. Pikem puutumatus pärast pihta saamist. |
| craft | craft | Nutikas meister | 3 | Puudub | Meisterdamine ja ehitamine maksab iga astmega 10% vähem. |
| mason | craft | Kivimeister | 1 | craft | Sulatusahjust saad kaks korda rohkem kiviplaate. |
| smelter | craft | Ahjumeister | 1 | craft | Puit põleb ahjus ja lõkkes kaks korda kauem. |
| gather | gather | Metsa sõber | 3 | Puudub | Korjad rohkem materjale ning tööriistad töötavad kiiremini. |
| logger | gather | Puuraidur | 1 | gather | Igast puust saad veel kaks puitu. Kännud annavad kolm puitu. |
| angler | gather | Kalameister | 1 | gather | Iga õnnestunud püügiga saad kaks kala. |
| star | star | Täheleiutaja | 3 | Puudub | Nups aeglustab lähedasi vastaseid tugevamalt ja töötab kiiremini. |
| frost | star | Täheudu | 1 | star | Nupsi aeglustav aura ulatub kaugemale. |
| leap | gather | Kõrge hüpe | 2 | gather | Iga aste lubab hüpata ühe maapinna astme võrra kõrgemale. |
| helper | star | Usin abiline | 1 | star | Baasi jäetud Nups toob kaks korda rohkem marju. |

## Tegelaste vahetusülesanded

Mängu tekst ja ID ei ole sama asi. Näiteks Leina ajalooline ID on ranger ning Bronkingsil miner; tõlkimine ei muuda ID-sid.

| ID | Nimi | Vanus | Roll | Nõue | Tasu |
| --- | --- | --- | --- | --- | --- |
| ranger | LEINA | 13 | Aednik | Porgand × 3 | Maitsetaim × 4 + Puit × 8 |
| miner | BRONKINGS | 22 | Sepp | Rauakang × 2 | Kristall × 2 + Vasekang × 3 |
| trader | SALTY | 27 | Kalamees | Kala × 3 | Rauakang × 3 + Joogivesi × 5 |
| karjon | KARJON | 165 | Rändur | Luu × 3 | Jääkild × 2 + Puit × 10 |
| anyo | ANYO | 36 | Võlur | Kristall × 2 | Tähemetall × 4 + Võlulill × 3 |
| diego | DIEGO | 7 | Džunglipoiss | Marjad × 5 | Banaan × 5 + Taimekiud × 6 |

## Majade tellimused

| Tase | Nimi | Kulu | Kestus mängupäevades |
| --- | --- | --- | --- |
| 1 | Metsamaja | Puit × 25 + Kivi × 15 + Taimekiud × 6 | 3 |
| 2 | Suur metsamaja | Puit × 45 + Kiviplaat × 12 + Rauakang × 4 | 3 |
| 3 | Tähekodu | Puit × 60 + Kiviplaat × 20 + Klaas × 8 + Kristall × 3 | 3 |

## Kultuurtaimed

| ID | Nimi | Kasvuaeg sekundites | Saak |
| --- | --- | --- | --- |
| carrot | Porgand | 180 | 3 |
| potato | Kartul | 240 | 4 |
| berries | Marjad | 210 | 3 |
| herbs | Ravimtaimed | 180 | 3 |
| magicFlower | Võlulilled | 300 | 2 |

## Toit

| ID | Nimi | Nälja taastamine | Elu taastamine |
| --- | --- | --- | --- |
| banana | Banaan | 22 | 1 |
| stew | Metsahautis | 65 | 3 |
| roast | Küpseliha | 40 | 2 |
| cookedFish | Küpsetatud kala | 45 | 2 |
| berries | Marjad | 25 | 1 |
| carrot | Porgand | 30 | 1 |
| bakedPotato | Küpsekartul | 35 | 1 |

## Maast käsitsi korjatavad materjalid

| ID | Tulemus | Kogus | Taastumisaeg sekundites |
| --- | --- | --- | --- |
| branch | Puit | 1 | 360 |
| pebble | Kivi | 1 | 720 |
| sand | Liiv | 3 | 360 |

## Kiirriba püsiv järjekord

| Koht | ID | Nimi |
| --- | --- | --- |
| 1 | hand | Käsi |
| 2 | axe | Kirves |
| 3 | pickaxe | Kirka |
| 4 | bow | Vibu |
| 5 | torch | Tõrvik |
| 6 | rod | Õng |

## Päeviku etapid

1. **Esimesed varud.** Korja maast oksi või raiu kirvega puud. Kogu viis puitu.

2. **Tööriistad seikluseks.** Kivikirka vajab 3 puitu, 3 väikest kivi ja 1 taimekiudu. Kiud saad maitsetaimest; kirka valmista laual.

3. **Valgus pimeduses.** Meisterda tõrvik: 2 puitu ja 1 taimekiud tahiks.

4. **Metsa saladus.** Küsi Karjonilt vihjet. Koobas peitub kaugel idas, mägede lõunaservas.

5. **Sõber tähtedelt.** Leia ida poolt meteoriit ja ütle Nupsile tere.

6. **Oma paik maailmas.** Vii Bronkingsile maja materjalid. Kolme päeva pärast astu oma koju.

7. **Kolm tähistaevast.** Ela üle kolm ööd. Seni üle elatud: 0/3.

8. **Tähemajakas.** Sulata metallid ja ehita kristallist tähemajakas — sinu baasi särav süda.

## Kõik inventari esemeliigid

| ID | Nimi |
| --- | --- |
| bone | Luu |
| cloth | Kangas |
| fang | Kihv |
| fur | Karusnahk |
| frostShard | Jääkild |
| trollMoss | Trollisammal |
| gold | Kuld |
| banana | Banaan |
| salve | Ravisalv |
| wood | Puit |
| stone | Kivi |
| berries | Marjad |
| crystal | Kristall |
| star | Tähemetall |
| herbs | Maitsetaim |
| meat | Metsloomaliha |
| roast | Küpseliha |
| stew | Metsahautis |
| ironOre | Rauamaak |
| copperOre | Vasemaak |
| iron | Rauakang |
| copper | Vasekang |
| slab | Kiviplaat |
| fish | Kala |
| cookedFish | Küpsetatud kala |
| carrot | Porgand |
| potato | Kartul |
| magicFlower | Võlulill |
| healPotion | Tervendav jook |
| speedPotion | Kiirusejook |
| peacePotion | Loomasõbra jook |
| water | Joogivesi |
| pearl | Merepärl |
| fiber | Taimekiud |
| sand | Liiv |
| glass | Klaas |
| bakedPotato | Küpsekartul |
