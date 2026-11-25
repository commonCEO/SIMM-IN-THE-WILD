# SIMM IN THE WILD mängudisaini dokument

**Tööversioon 1.0 · 18. november 2026 · brauseri 0.6.0 taastamise lähtealus Godotile**

SIMM on Mattiasega koos arendatav üksikmäng, kus noor seikleja kogub metsas materjale, valmistab tööriistu, aitab tegelasi, rajab kodu ja uurib järjest kaugemaid piirkondi. Godotile üleviimise eesmärk on säilitada olemasoleva brauserimängu mehaanika, kasutajaliides ja kasutusvood ning teha maailm päriselt ruumiliseks, ilusamaks ja edaspidi laiendatavaks.

Praegune Godoti laager on toimiv katseala, mitte kogu brauserimängu koopia. Selle lihtsustatud retseptimenüü, piiratud esemeloend ja ajutine ressursimajandus ei muutu vaikimisi uueks mängudisainiks. Edasise arenduse alus on allpool kirjeldatud brauserikäitumine koos selgelt eristatud kasutaja otsustega.

Täpsed andmeloendid on [mängudisaini andmetabelites](GAME-DESIGN-DATA.md) ja nende [masinloetavas lähtekoopias](browser-design-baseline.json): **48 mudeliretsepti, 13 oskust, 37 inventari esemeliiki, kuus ülesandetegelast, kolm majaplaani ja kuus kiirriba tööriistakohta**. Kõik mudelis olevad retseptid ei ole igas mängukontekstis nähtavad.

## 1. Disaini lähtealus ja otsuste järjekord

Kehtiv alus on brauseri versioon 0.6.0. Vanemate versioonide kirjeldused selgitavad päritolu ja põhjendusi; hilisem teadlik muudatus asendab varasema lahenduse. Eriti oluline on 0.6 majade tellimissüsteem, mis asendas uute õuemajade tükkhaaval kokkuladumise.

Töötamise järjekord on järgmine:

1. Kasutaja praegused selged otsused, sh 3D-sse üleviimine ja nõue säilitada mehaanika, UX ja UI.
2. Praegune brauseri lähtekood, kehtivad 0.6 nõuded ja nende käitumist kontrollivad testid.
3. Versioonide märkmed ja varasemate kontrollide aruanded, arvestades nende kuupäeva ja versiooni.
4. Godoti praegune teostus kirjeldab üleviimise seisu; selle juhuslik kõrvalekalle ei asenda brauserireeglit.

Kui nõue, kood ja ajalooline märge ei ühti, tuleb vastuolu nähtavaks teha. Juhuslikku viga ei pea kujundama tahtlikuks disainiks, kuid selle parandamine ei tohi toimuda varjatud reeglimuudatusena.

### Kasutaja kinnitatud suund

- Visuaalne siht on [kunstisuundade lehe](v06-art-directions.png) **ülemine parempoolne paneel 2**: soe, ruumiline metsadioraam.
- Brauseri olemasolev 2.5D teostus on käitumise alus, mitte lõpliku 3D kunsti kvaliteedieeskuju.
- Kaamera peab olema rahulik. Kohalikus mängukatses häirinud suunamuutusega õõtsumine ja kõndimishüplemine eemaldati ning uus kindla nurgaga jälgimine sai kasutajalt positiivse tagasiside.
- Tõrvik peab andma päris valgust; Simmi kujuline vari võib jääda, aga selle serv peab olema väga pehme.
- Kiirriba paikneb all ning LB/RB vahetab maailmas tööriista.
- D-padi allanool vahetab kohalikus prooviversioonis päeva ja õhtu valgustust. See on eraldi lubatud **testimise abifunktsioon**, mitte brauseri automaatse päevatsükli asendus.
- Arendus ja mängukatsetus toimuvad sellel Windowsi arvutil. Mattiase füüsilise puldiga saadud tagasiside täiendab automaatkontrolle.

## 2. Mängu identiteet ja mängijakogemus

Põhikogemus on arusaadav avastamis- ja meisterdamisseiklus. Mängija näeb lähedal väikest eesmärki, leiab vajalikud esemed, saab tegevusele selge tagasiside ning avab sellega järgmise võimaluse. Näiteks oksad ja väikesed kivid võimaldavad kirka valmistada; kirka ja tõrvik võimaldavad koopasse minna.

Mattiasega mängides peab tegevus olema loetav ka ilma pikkade seletusteta: milline tööriist on käes, mis tegevus on lähedal võimalik, millist materjali veel napib ning mis pärast nupuvajutust muutus. Menüüd peavad töötama lõpuni puldiga. Hiir ei tohi olla vajalik mingi üksiku valiku või kinnituse päästmiseks.

Varasemates märkmetes on sisuline ja kunstiline siht PEGI 7 laadne seiklus; ametlikku vanusepiirangu hinnangut pole saadud. Loomade ja vastastega võideldakse ilma vere ja graafilise vägivallata. Kaotus säilitab varud ja edenemise, et üks eksimus ei kustutaks kogu mängukorda.

### Põhiring

**Avasta → kogu → valmista → kasuta või ehita → aita tegelast → ava järgmine piirkond → naase ja salvesta.**

Lühikeses mängukorras peab olema võimalik lõpetada üks selge tegevus: teha esimene tööriist, saada valmis peenar, täita üks tarne või valmistada ette kooparetk. Pikemad eesmärgid on kodu, uued piirkonnad, Nups, ööde üleelamine ja tähemajakas.

## 3. Versioonide areng ja kehtivus

| Etapp | Lisandunud või muudetud süsteem | Mõju Godotile üleviimisele |
| --- | --- | --- |
| 0.2 | Täisekraaniline mänguvaade, puldimenüüd, nähtav oskusepunktide info, ruudupõhine ehitus, vibu, kaotusest taastumine, Nups, sulatamine, kalastamine ja piiratud seljakott | Need on juba olemasoleva kogemuse osad, mitte hilisemad uued ideed |
| 0.4 | Laiendatud ellujäämine ja maailm, hoiustamine, põllundus, tegelaste ülesanded, majad ja korrused, paadid/vaal, maastik, kaamera suunad | Vanad kirjeldused tuleb kontrollida 0.6 muudatuste vastu |
| 0.4.1 | Materjaliloogika ülevaatus, 3+3+1 kirka, lahtised algusmaterjalid, kiud, õhemad ehitiste kokkupõrked ja läbipääsetavad kännud | Alguse ummikuvaba läbimine ja täpne majandus on kohustuslikud |
| 0.4.2 | Kaotusejärgse korduva rünnaku parandus; normaalajas värske mängu teekond | Kaotuse järel taastatakse vaenlaste kodupositsioonid ja ajutine rahu |
| 0.4.3 | Täpne puldi ehituskursor, puudujääkide näitamine, kastist virnaga liigutamine, EN/ET ja säiliv paigutusfookus | UX ja sisendit tuleb üle tuua konteksti järgi, mitte ainult nupuloendina |
| 0.5 | Kolme veeruga meisterdamine, kategooriad, kuue NPC heaks kiidetud kujundused, suurem maailm, saak ja harv vikerkaar | Ühine menüüraam, selge fookus ja külgpaneelid on alusdisain |
| 0.5.1 | Natiivne pikslitihedus, loetavad tegelased/maailmasildid, korrektne osuti ja muutuv DPI | Uus mootor ei tohi tekstiloetavuses ega ekraanisuuruste toes tagasi minna |
| 0.6.0 | 192×144 maailm, dioraamspriidid, suum, Bronkingsilt tellitavad majad, suurem dungeon, vulkaan, seljakoti selged tegevused | See on praegune käitumuslik sihtversioon |
| Kohalik Godoti proovilaager | Päris 3D liikumine, füüsika, maquette-kujud, esialgne korjamine/meisterdamine/salvestus, tööriistad, kiirriba ja tõrvik | Tõestab üksikuid süsteeme; allpool olev vastavusloend piiritleb puudujäägid |

Allikad: [README versioonide ajalugu](../README.md), [0.5 disainimärkmed](v05-design-notes.txt), [0.6 nõuded](v06-requirements.txt), [0.6 väljalaskemärkmed](v06-release.txt), [0.6 kontrolliaruanne](e2e-results-v06.txt).

## 4. Uue mängu lähteolek

Brauseris algab seiklus esimesel päeval: viis elu, nälg ja janu 100, kuumus 0, tase 1, XP ja vabad oskusepunktid 0. Kõigi inventariesemete kogused on 0. Seljakotis on 20 pesa; üks virn mahutab 20 sama liiki eset. Tööriistad ei kuluta neid materjalipesi.

Mängija **omab kätt ja kirvest**, kuid alguses on valitud käsi. See lähteolek on nüüd ka Godoti uues mänguolekus taastatud. Olemasoleva salvestuse ostetud või valmistatud tööriistu ei kustutata; varasemat käsi-ainult proovilaagri salvestust ei kirjutata salaja uueks mänguks ümber.

Keele vaikeseadistus on brauseris inglise keel. Mängija saab kohe valida eesti keele; keele-eelistus säilib mängusalvestusest sõltumatult. Käesoleva kohaliku Godoti katseala eestikeelne tekst ei tähenda, et kahe keele tugi oleks sinna juba üle toodud.

Algus ei tohi jääda enda taha kinni. Laagri lähedal on garanteeritud käsitsi korjatavad oksad ja väikesed kivid; herbidest saadakse kiudu ilma töölauata. Sulatusahju esimene ehitus ei vaja metalli, mida saab valmistada ainult samas ahjus.

## 5. Esemed, seljakott ja materjalimajandus

### Mahutavus ja tegevused

Kasutatud pesade arv on iga esemeliigi koguse ja virnasuuruse jagatise ülespoole ümarduste summa. Seljakoti parandamine lisab viis pesa korraga, kuni 40 pesani. Eseme valimine menüüs ei kasuta ega viska seda ära.

Seljakotis on virnade ruudustik ja valitud eseme detailid. Kasutataval esemel on eraldi **Joo vett**, **Söö** või **Kasuta** tegevus ning eraldi **Pane 1 maha**. Mittevajalik toit või jook jääb alles. Maha pandud ese paikneb õiges maailmas, koopatüübis või maja korrusel ning on 600 aktiivse mängusekundi jooksul tagasi korjatav. Menüüs pausil see aeg ei jookse.

Kui lahtine oks või väike kivi kotti ei mahu, jääb see korjamata. Kui tööriistaga saadud saak kotti ei mahu, pannakse see maailmas maha; tehtud töö ei tohi lihtsalt kaduda. Täis koti hoiatus ja edukas kogus peavad olema nähtavad. Kastist väljavõtmine arvestab ka osaliselt mahtuva virnaga.

### Meisterdamine ja hoiukastid

Baaskulude täielik loend on [andmetabelites](GAME-DESIGN-DATA.md). Põhiretseptid on:

| Retsept | Kulu | Tulemus ja koht |
| --- | --- | --- |
| Taimekiud | 1 maitsetaim | 3 kiudu, käsitsi |
| Kivikirka | 3 puitu + 3 kivi + 1 kiud | Kirka, meisterdamislaual |
| Kivikirves | 3 puitu + 4 kivi + 1 kiud | Kirves, meisterdamislaual; uue mängu algkirves on eraldi lähtevarustus |
| Tõrvik | 2 puitu + 1 kiud | Tõrvik, meisterdamislaual |
| Vibu | 6 puitu + 3 kiudu | Vibu, meisterdamislaual |
| Õng | 4 puitu + 2 kiudu | Õng, meisterdamislaual |

Ühe taimobjekti korjamine ja ühe inventaris oleva maitsetaime töötlemine on erinevad sammud: praegune brauseri taimobjekt annab tavaliselt **3 maitsetaime**; retsept kulutab neist ühe ja annab **3 kiudu**. Varasem retseptiproosa ei kirjelda alati maailmaobjekti saaki üheselt.

Lähedal asuvad kastid, kuni 120 brauseri maailmaühiku kaugusel, osalevad meisterdamise materjalides. Kõigepealt kulub seljakoti varu, seejärel lähedaste kastide varu. Ebaõnnestunud meisterdamine, sealhulgas tulemuse mittesobimine kotti, peab jätma kõik varud endiseks. Käsitsi retseptid, töölaud, veekogu lähedus, lõke ja sulatusahi on eraldi tingimused.

Meisterdamisoskuse aste vähendab iga tavalise retsepti materjalirida eraldi: `kulu = max(1, ceil(baaskulu × (1 − 0,1 × oskuseaste)))`. Seega ümardatakse üles ja olemasolev materjalirida ei muutu tasuta; tühja kuluga veepudeliretseptile uut materjalirida ei lisata. Bronkingsi majateenus kasutab täit baaskulu ja ei saa seda soodustust. Kivimeistri oskus kahekordistab kiviplaadi retsepti väljundi, mitte sisendikulu.

Aktiivse meisterdamismenüü edukas tavavalmistamine annab **8 XP**. Tööriista valmistamine lisab selle omandisse, kuid ei vaheta automaatselt käes olevat tööriista. Täiendatud kirves/vibu/kirka on varustuse täiendus, mitte suvaline uus inventarivirn. Need reeglid lähtuvad praegusest `activateRecipe()` voost; lähtefailis alles olevad vanemad renderdusharud ei määra aktiivse menüü XP-tasu. Allikad: `src/game.js:217`, `src/game.js:265`, `src/model.js:137`.

Allikad: [andmemudel](../src/model.js), [meisterdamise ja seljakoti kasutusvood](../src/game.js), [retseptide ajalooline ülevaatus](recipes.txt).

## 6. Korjamine ja tööriistade kasutamine

Kiirriba järjekord on alati **käsi, kirves, kirka, vibu, tõrvik, õng**. Maailmas LB/RB vahetab omandatud tööriistade vahel ja jätab puuduvad vahele; klaviatuuri 1–6 vastab samadele kohtadele. Puuduv tööriist ei tohi nihutada ülejäänute numbreid.

Oks annab 1 puitu, väike kivi 1 kivi ja käsitsi korjatav liiv 3 liiva. Suur puu nõuab valitud kirvest; kivi ja maak nõuavad valitud kirkat. Baasressursil on kolm elupunkti. Õige tööriista löök vähendab neid; taimed korjatakse baasolukorras ühe tegevusega. Kogumisoskus ja täiustatud tööriistad mõjutavad löögijõudu ning saaki.

Baassaak makstakse **ressursi ammendumisel**, mitte iga löögiga: puu 5 puitu, suur kivi 4 kivi ning taim või marjapõõsas 3 vastavat eset. Puu jätab kännu. Järgmine kirvekasutus eemaldab kännu ja annab 2 puitu; puuraiduri oskusega 3. Puuraidur annab lisaks täispuu saagile 2 puitu. Oskuse muud saagilisad tuleb arvestada samas tehingus.

Taastumine kasutab salvestatavat aktiivse maailma aega: puu 1080 sekundit, oks 360, väike kivi 720 ning sobivad taimed ja liiv 360. Taastumine ootab, kui koht on majaõue, hoone, NPC või paigutatud eseme tõttu hõivatud. Suurte kivide ja maagi taastumist ei tohi oletada üksnes tähtaja kirjutamisest: praeguse taastamisfunktsiooni lubatud tüüpide loendis neid pole. See käitumine ja võimalik soovitud muudatus tuleb eraldi otsustada.

### Tegevus ja sihtimine

A/E suhtleb lähima sobiva sihtmärgiga ning võib korjata või raiuda sihitud ressurssi. Kui sihtmärki pole, käivitab see hüppe. F hüppab eraldi. Kõrgusastme taga olev objekt ei tohi neelata hüppeks mõeldud vajutust. Jaamad, uksed ja muud olulised tegevused saavad olukorrast sõltuva eelistuse; valitud tööriist aitab sobivat ressurssi eristada.

RT, tühik, hiir või X käivitab lisaks tööriista tegevuse: lähilöök, vibu või kalastamine. Brauseri baasinteraktsiooni jahtumisaeg on 0,28 sekundit ning rünnakul 0,35 sekundit. Hoidmine ei tähenda suvalist automaatset löögikordust. Vibu laeb RT/tühiku/hiirenupu hoidmisel ja laseb vabastamisel; puldi X laseb vajutamisel kohe laadimata noole. Tavaline täislaadimine kestab 1,2 sekundit, vastava oskusega 0,78. Nähtav sihtmärk ja jõuriba on ainult laadimise ajal.

Tõrvik peab olema nähtav käes, valgustama lähedust ja aitama öö/koopa kogemust. Godotis on kasutaja soovil säilitatud pehme Simmi siluett, mitte maalitud varjupilt maapinnal.

## 7. Kasutajaliides ja juhtimine

### Maailmavaade

Ülal vasakul on elu ja nälg, keskosas mängu/ülesande info ning paremal päev, aeg ja juhtelemendid. Mängija peab nägema vabu oskusepunkte, mõjuolekuid, piirkonda ja hetkeülesannet. All on seljakoti ja meisterdamise avamine, kuue tööriista riba ning ehitamise ja söömise tegevused. Kontekstivihje asub kiirriba kohal; saagiteated, üldteated ja kahjutagasiside on eristatavad.

Tekst ja ikoonid peavad jääma loetavaks 720p, 1080p ja 4K vaadetes ning mõlemas keeles. Värv üksi ei tohi olla ainus saadavuse märge. Hiirekursori vana asukoht ei tohi puldiga mängides juhtimist üle võtta. Suum ja ekraani pikslitihedus ei muuda maailma koordinaate ega paigutusruudu asukohta.

### Ühine menüüraam

Püsiv vahelehtede järjekord on **SELJAKOTT → ÜLESANDED → MEISTERDAMINE → EHITAMINE → OSKUSED → KAART**. Kõigil on sama välisraam ja mõõdud: pealkiri, sulgemine, vahelehed, keritav sisu ning kontekstikohane puldijuhis. Jaama või NPC-ga suhtlemine avab kohe vastava tegevuse.

Seljakotis on esemete ruudustik ja detailid. Meisterdamisel/ehitamisel on korraga nähtavad isiklik varu, stabiilses järjekorras retseptid/kategooriad ning valitud retsepti üksikasjad. Retseptirida sisaldab ikooni, nime ja lühikest valmisolekut; pikka koostisosade loendit ei suruta igasse ritta. Detailides näidatakse kaasas/kastis/kokku kogust ning nõutavat hulka.

Puuduvate materjalidega retsept jääb valitavaks ja uuritavaks. Fookus ega hiirega üleliikumine ei valmista eset. Kinnitamine käivitab ühe tehingu. Õnnestunud meisterdamine või vahelehe vahetamine ei tohi kaotada selle vahelehe valikut ja kerimiskohta. Uues stseenis tuleb kategooria kehtivus kontrollida, et õue Majad-filter ei jätaks maja sisustamise menüüd tühjaks.

Oskused kasutavad nelja kompaktset haru ja püsivat selgituspaneeli. Lukustatud oskust saab uurida; selle õppimine nõuab eeldusi, vaba punkti ja lubatud järgmist astet.

### Puldi kontekstireeglid

| Sisend | Maailm | Põhimenüü või jaam | Ehitamise paigutus |
| --- | --- | --- | --- |
| Vasak kang | Liikumine kaamera suhtes | Ruumiline fookuse liigutamine | Liigutab Simmi, mitte valitud ruutu |
| A | Suhtle/korja; sihtmärgita hüppa | Kinnita valitud tegevus üks kord | Paigalda |
| B | Nupsi oota/järgne käsk | Tagasi/sulge | Lõpeta paigutamine |
| Y | Ava Ehitamine | Kontekstis määratud tegevus; mitte uus üldine kotinupp | Järgib brauseri ehitusvoogu |
| View / D-pad üles | Ava Seljakott | D-pad liigub fookuses | Paigutuse kontekst on ülimuslik |
| Menu/Start | Paus | Pausi/tagasi käitumine | Paus |
| LB/RB | Eelmine/järgmine omandatud tööriist | Eelmine/järgmine põhivaheleht | Tööriista ja paigutuse kontekst kontrollida lähtevooga |
| LT/RT | LT sööb; RT kasutab tööriista / laeb vibu | Retseptikategooria vahetus | RT paigaldab |
| X | Puudutab tööriistategevust | Kastis liigutab virna | Pöörab valitud ehitusdetaili |
| Parem kang | Sihtimine; hoia R3 ja liiguta vertikaalselt suumiks | Detailide/sisu kerimine | Muudab absoluutset paigutusruutu |
| D-pad vasak/parem | Pööra kaamerat nelja suuna vahel | Ruumiline fookus | Muudab absoluutset paigutusruutu |
| D-pad alla | Godoti kohalik päev/õhtu testlüliti | Navigeerimine, mitte ajamuutus | Navigeerimine, mitte ajamuutus |

Brauseri menüüs on hoitud suuna esimene samm kohene, kordus algab 260 ms järel ja kordub 85 ms järel; kangi fookuselävi on 0,40. See on lähteväärtus, mida ei asendata märkamatult eelmise/järgmise nupu lihtsa ringiga.

Klaviatuuri olulised vasted on WASD/nooled, E/F, Z/V, tööriistakohad 1–6, I/C/J/B/K vastava menüü avamiseks, nurksulud/Tab põhivahelehe vahetuseks, PageUp/PageDown kategooriaks, Enter/Escape kinnitamiseks/tagasi ning tühik tööriistaks. Klaviatuuri B ei tähenda sama mis puldi B.

Paus sisaldab jätkamist, abi, oskusi, uut mängu, päevikut, keelt ja suumi. Uue mängu kinnituses on vaikimisi ohutu valik **säilita olemasolev seiklus**. Keelevahetus ei muuda mängu ID-sid, varusid ega salvestust.

Allikad: [menüüde disainimärkmed](v05-design-notes.txt), [brauseri sisend ja vaated](../src/game.js), [paigutus](../src/style.css), [ekraanielemendid](../src/index.html).

## 8. Maailm, tegevused ja edenemine

### Piirkonnad ja liikumine

0.6 maailm on 192×144 ruutu. Mets, lõunapoolne džungel, kirdepoolsed lumemäed, sisemaakõrb, kagupoolne vulkaan ja meri on eri võimaluste ja ohtudega piirkonnad. Piirid ja rannik on orgaanilised. Veepilt, liikumispiir ja paadi paigutus lähtuvad samast geomeetriast. Kõrgusastmed mõjutavad läbipääsu ja hüppamist; alguslaager on tasane.

Brauseri maastik on 2.5D dioraam. Godoti 3D kaamera, meetermõõt ja füüsika ei tähenda luba muuta liikumise reegleid. Puu/kivi liikumist blokeerivus ja nähtavate ruutude projektsioon on allpool eraldi sobitamisküsimused.

### Tegelased ja identiteet

Simm on pruunipäine noor seikleja kollase jope, oliivrohelise seljakoti, tumedate pükste ja pruunide saabastega. Tema vanust ega uut taustalugu ei lisata oletusena.

| Tegelane | Kinnitatud identiteet |
| --- | --- |
| Leina | 13, aednik, punakaspruun hobusesaba, kollane särk ja koralltooni tunked; lilled ja kastekann |
| Bronkings | 22, kiilaspäine sepp, lai nahkpõll tööriistataskutega, haamer, sõbralik ja õiglane |
| Diego | 7, metsik džunglipoiss, sassis pruunid juuksed, katkised laimirohelised riided, paljajalu; õlal rott |
| Karjon | 165, hõbedased juuksed, lapitud pruun kuub, punased püksid, vasak konks ja paremas käes nuga |
| Anyo | 36, hõljuv võlur, tumesinised juuksed hõbedase triibuga, lilla-kuldne rüü |
| Salty | 27, punapäine kalamees, kollased/sinised riided ja vetikad |

Igal kuuel NPC-l on dialoog, portree, maailmakujutis ja ühekordne vahetusülesanne. Leina küsib 3 porgandit ning annab 4 maitsetaime ja 8 puitu. Bronkings küsib 2 rauda ning annab 2 kristalli ja 3 vaske. Ülejäänud nõuded ja tasud on [täielikus NPC tabelis](GAME-DESIGN-DATA.md#tegelaste-vahetusülesanded). Vahetus annab 35 XP ja ei tohi osaliselt tasuda, kui tasu kotti ei mahu. Ajaloolised tehnilised ID-d jäävad stabiilseks: näiteks Leina ID on `ranger`, Bronkingsi oma `miner`.

### Päev, ellujäämine ja kaotus

Päevatsükkel kestab 360 aktiivset sekundit: 300 päevavalgust ja 60 ööd. Menüü või paus peatab mänguaja. Nälg väheneb 0,045 ühikut sekundis; toit taastab nälga ja vajaduse korral elu. Vesi taastab kuni 60 janu ja vähendab kuumust 35. Kõrbe kuumus ja janu, öö vastased, loomad, koobas ja laava annavad piirkonnale tähenduse.

Pihtasaamine annab selge tagasiside ning ühise ajutise kaitse, et mitu samal hetkel puudutavat vastast ei põhjustaks mitut vältimatut tabamust. Kaotuse järel naaseb Simm laagri juurde järgmisse hommikusse, säilitades asjad ja edenemise. Vaenlased taastatakse kodupositsioonidele ning nad jäävad 12 aktiivseks sekundiks rahulikuks; laagris ei tohi järgneda kohest uut kaotust. Telgis või voodis puhkamine liigub järgmisse hommikusse ja taastab määratud näitajad.

### Ehitus, kodu ja tootmine

Praegune 0.6 õuekodu tellitakse Bronkingsilt või Ehitamine → Majad kaudu. Tellimiseks tuleb olla Bronkingsi lähedal, tasuda materjalid üks kord ja oodata kolm mängupäeva. Esimene metsamaja maksab 25 puitu, 15 kivi ja 6 kiudu; järgmised kaks taset on andmetabelis. Uuendus säilitab mööbli ja kastisisu, lisab korrused ning jätab ukse ja õue vabaks. Vana ise ehitatud maja peab vanast salvestusest alles jääma.

Jaamu, kaste, peenraid, mööblit ja lampe paigutatakse endiselt vabalt. Ehitamisel valitakse absoluutne maailmaruut: Simm võib kõndida, aga valitud ruut ei tohi temaga kaasa liikuda. Eelvaade näitab lubatud/keelatud kohta ja konkreetset põhjust. Valik jääb korduvaks paigutamiseks aktiivseks. Ukse, seina ja mööbli kokkupõrge peab vastama nähtavale kujule.

Lõkkel ja sulatusahjus annab 1 puit 120 sekundit kütust; ahjumeistri oskus kahekordistab selle 240 sekundini. Küpsetamine ja sulatamine nõuavad sobivat jaama ning positiivset kütusevaru. Edukas valmistamine toimub kohe ja vähendab jaama varu **5 kütusesekundi võrra**, vähemalt nullini; see ei ole viiesekundiline ooteaeg ega animatsiooni kestus. Allikad: `src/game.js:253`, `src/game.js:267`, `src/game.js:277`.

Kasti A liigutab ühe eseme, X kuni ühe 20-se virna; väljavõtmine arvestab mahutavust. Peenras valitakse kultuur, kasv jätkub aktiivsel mänguajal ning saagikoristus nõuab valmimist. Porgand ja maitsetaim kasvavad 180 sekundit ning annavad 3 saaki. Täielik kultuuriloend on andmetabelites.

### Uurimine ja pikem seiklus

Koopasse minemiseks peab omama kirkat ja tõrvikut. Metsakoobas sisaldab kuut ühendatud saali, koridore, maaki, nahkhiiri, püsiva sisuga kaste ja kaugel olevat kristalli. Väljapääsu tähistab valgusring; kaardivaade näitab kooparuume. Kristalli leidmine annab 3 kristalli ning edenemise. Vulkaanil on oma sissepääs, saalid, kastid ja tagasitee; eri stseenide maha pandud asjad ei tohi seguneda.

Tuhamäe vulkaani laavapraod teevad kahju; enne purset hoiatavad kraater ja tekst. Pursetsükkel sõltub aktiivsest maailmaajast. Ebaselgest ajaloolisest suulisest soovist ei tuletata baasi hävitamist ega uut karistust.

Meteoriidi saabumine avab kohtumise Nupsiga. Sõprus annab tähemetalli ja kaaslase, kes järgneb või ootab B/T käsuga ning mõjutab lähedasi vastaseid; oskused ja pesa laiendavad tema käitumist. Päevik juhatab varudest tööriistade, kristalli, Nupsi, kodu ja ööde kaudu tähemajaka juurde.

Kalastamine nõuab õnge ja sobivat veekogu kallast. Pärast **3 aktiivset sekundit** püügikohal saab ühe kala, kalameistri oskusega kaks; üle 12 maailmaühiku eemaldumine katkestab püügi. Edu annab 8 XP. Paat võimaldab merel liikuda. Vaalaga kohtumine on sõbralik ajastusmäng: RT hoiab märgi üleval, vabastamine laseb langeda, kuldses alas püsimine täidab edenemise; vabastatud vaal ei saa viga ja annab merepärli. Allikad: `src/game.js:422`, `src/game.js:511`, `src/game.js:607`.

Vikerkaare võimalikkus määratakse päevanumbrist deterministlikult, 8% lävega, alates **teisest päevast**. Päeva kontroll tehakse pärast 90. päevasekundini jõudmist; sündmus vajab õues viibimist ja sobivat ligipääsetavat kohta. Tekkinud vikerkaar kestab 120 aktiivset sekundit. Selle lõpust saab ühe korra **3 kulda ja 25 XP**; tasu saamiseks peab lähenema 45 maailmaühiku kaugusele ning kotti peab mahtuma. Sündmuse, kontrollitud päeva ja võetud preemia olek säilib salvestuses. Tegemist ei ole igal avamisel uuesti veeretatava 8% võimalusega. Allikad: `src/model.js:223`, `src/model.js:224`, `src/model.js:232`.

## 9. Oskused, võitlus ja tagasiside

Oskusepunktid ja XP on tegelase kasvamise osa. Järgmise taseme lävi on **35 × praegune tase**: läve ületamisel lahutatakse see XP-varust, tase suureneb ühe võrra ja lisandub üks vaba oskusepunkt. Suur tasu võib sama reegliga läbida mitu taset. Neli põhiharu on võitlus, meisterdamine, kogumine ja täheleiutamine; iga haru juures on eeldustega spetsialiseerumised. Kõik 13 kirjet, astmepiirid ja kirjeldused on [oskuste tabelis](GAME-DESIGN-DATA.md#oskused). Õppimine kulutab ühe punkti ainult lubatud järgmise astme korral. Allikas: `src/model.js:78`.

Maksimaalne tervis on **5 + võitlusoskuse aste + amuleti 1 + kaitsjaoskuse 3**; kaks viimast lisa rakenduvad vastava varustuse/oskuse olemasolul. Tervise ülempiiri suurendav õppimine või aktiivses menüüs valmistatud amulett lisab hetketervisele sama suurenemise. Ravijook ja ravisalv taastavad kuni neli elu, ülempiiri ületamata, ning täie tervise korral jäävad alles. Kiirusejook määrab mõju kestuseks 90, loomarahujook 120 aktiivset sekundit; menüü või paus peatab kestuse kulumise. Allikad: `src/model.js:79`, `src/model.js:81`, `src/model.js:147`, `src/model.js:151`, `src/game.js:268`.

Vastased ja loomad erinevad elupunktide, kodupiirkonna ja tagaajamiskäitumise poolest. Karu kaitseb pesa ümbrust; teised kiskjad kasutavad lähene/kaugene lävesid. Rahujook ja kaaslase mõju on tegelikud olekud, mitte üksnes visuaalsed efektid. Võidetud vastaste materjalid on seotud retseptidega: luud, kangas, kihvad, karusnahk, trollisammal ja jääkillud avavad täiendusi ning uusi esemeid.

Tagasiside peab siduma põhjuse ja tulemuse: löök, allesjäänud tervis, ajutine kaitse, saadud kogus, retsepti puudujääk, tehtud tööriist, kasti liigutus ja ülesande tasu. Kõik need peavad olema arusaadavad ka helita. Heli on brauseris algul väljas, kasutaja lülitab selle sisse ja reguleerib helitugevust. Olemasolev heli on kohalikult sünteesitud; uut salvestatud kõnet ei loeta olemasolevaks funktsiooniks.

## 10. Visuaalne suund ja 3D vara leping

Soovitud tulemus on soe, pehme ja käega vormitud tundega metsadioraam: ümarad ruumilised lehestikukobarad, selgelt eristatavad näod ja siluetid, loetavad tööriistad, naturaalne puit/riie/nahk ning ühtne valgus ja kontaktvarjud. Plastikune läige, tugev tahulisus ja fotorealistlik nahk ei ole siht.

Tegelane ja puu peavad säilitama ruumilise kuju ka teise kaameranurga alt. Tervet objekti asendav lame pilditasapind, maapinnale maalitud vari või tegelase jalgega kaasa liikuv varjuketas ei vasta lepingule. UI tekstisildid on eraldi loetavuse vahend, mitte ruumilise geomeetria asendus.

Esimene kooskõlaline komplekt on Simm, Leina, Bronkings, töölaud, telk, tamm, mänd, kask, kivi, marjapõõsas, oks, väike kivi ja rohumätas. Simm, tamm ja töölaud määravad esimesena proportsiooni ning materjalide stiili. [Manifest](../godot/assets/manifest.json) määrab nimed, mõõdud, asukohad ja animatsioonid; [Blenderi üleandmine](FABLE-BLENDER-HANDOVER.txt) on vara täpne leping.

Üks ühik on üks meeter; pöördepunkt on maapinnal/jalgades. Blenderi +Z muutub glTF kaudu Godoti +Y-ks ning tegelase eesmine suund Godotis on +Z. Import ei paranda vales mõõdus mudelit automaatse ümbermõõtmisega. GLB sisaldab enda materjale/tekstuure ja vajalikke skeleti/animatsiooni andmeid; stseeni ei ekspordita stuudiopõrandat, tulesid ega kaameraid.

Simm vajab klippe `idle`, `walk`, `gather`; NPC-d `idle`, `talk`; parema käe liides on `hand_r_socket`. Ajutised kohalikud maquette-kujud ja jäigad tööriistad ei täida seda animatsioonilepingut. Mudelite autorfailid säilivad, olemasolevat tööd ei kirjutata üle. Lõplikku välimust hinnatakse tegeliku Godoti pildi, teise kaameranurga ja lühikese kõnni/korjamise järgi.

## 11. Salvestus ja tehnilised piirid

Brauser salvestab terve seikluse: inventari, tööriistad, oskused, mängija ja maailmaaja, hooned, ruumisisustuse, maha pandud asjad, ammendunud ressursid, eemaldatud kännud, loomad, NPC ülesanded, kodutellimused ning sündmused. Vanad versioonid migreeritakse; algse metsa ressursi-ID-d ei nihku uue piirkonna lisamisel. Suum, keel ja heli seadistused on mängu edenemisest eraldi.

Brauseri valitud kiirribakoht on jooksva seansi väärtus ja avamisel on valitud käsi. Godoti praegune prooviversioon salvestab käes oleva tööriista; see on dokumenteeritud erinevus, mitte vaikimisi uus pariteedinõue. Godoti proovilaagri kohalik salvestus on eraldi ning ei impordi praegu brauseri salvestusi.

Godoti ülesehituses tuleb lahus hoida andmed/reeglid, maailmaobjektid, kasutajaliides, sisendi kontekst ja visuaalsed varad. Retsept, NPC või esemeliik peab säilitama sama ID kogu ahelas. Koodi ümberkorraldus ei tohi muuta baaskulu, kogust, toimingu järjekorda ega salvestatud tulemusi.

Brauser töötab iseseisvate HTML-failidena lokaalsete varadega. Godoti jaoks on praegu kontrollitud kohaliku Windowsi prototüübi käivitamine ja MCP; levitamiseks sobiva ekspordi, installerite või platvormiintegratsioonide olemasolu sellest ei järeldu. Mäng ise ei vaja AI-teenust ega kontot. Multiplayer on selgelt edasi lükatud, mitte pooleliolev olemasolev süsteem.

## 12. Godoti vastavusse viimise register

Register on uuendatud kohaliku proovilaagri järgi 20. novembril. „Osaline” tähendab töötavat alamhulka, mitte kogu süsteemi valmimist.

| Valdkond | Praegune Godot | Vajalik brauseriga vastavus |
| --- | --- | --- |
| Liikumine, kaamera ja pult | Töötav 3D liikumine, kindel kaameranurk, kohalik puldikatse | Säilita rahulik kaamera; taasta neli vaatesuunda, hüppamine ja maailmakõrguse reeglid |
| Kunst | Kõigil 13 algsel clearing'u varal Blenderi autorfail ja GLB; tegelastel kaalutud rig ja nõutud animatsioonid; korjatavatel okstel/kivikestel ja ääreala rohututtidel uus kunst | Täieliku komplekti visuaalne heakskiit, valguse/materjalide viimistlus ja heakskiidetud clearing; laiema maailma kunst on veel prototüüp |
| Uus mäng | Käsi + kirves, valitud käsi; valmistamine ei muuda valikut | Täielik algolek, keeled, tiitel ja ohutu uus-mäng voog |
| Kiirriba | 6 püsivat kohta ja 1–6, LB/RB jätab puuduva vahele; vibu ja õng toimivad, valik katkestab laadimise | Menüü kontekstide täielik vastavus kogu kampaanias |
| Korjamine | Algse laagri ning 60 lisasõlme puu/kivi/maak/taimed/liiv, õiged tööriistad/oskused/täiustused, lõppsaak, kännud, ületäitumine/maha pandud saak ja salvestatav ajapõhine taastumine | Kogu brauserikaart, kõrgusastmed ja täielik sihtmärgivalik |
| Inventar | 37 esemeliiki, 20–40 pesa/20 kaupa virnad, ruudustik/detailid, tarbimine/mahapanek/tagasikorje/aegumine, kastide A/X tehingud | Kogu maailmaga seotud tarneahel |
| Meisterdamine | Kõik 25 mitteehitusretsepti ja nende tegelikud koostisainete hanketeed proovialas; 48 retsepti andmed, aatomiline makse/mahutavus, lähikastid, õpitavate oskuste kulureeglid, jaamad ja kütus | Kogu biomeerikaart ning ülejäänud ehitusretseptide maailmatoimingud |
| UI ja juhtimine | Ühine kuue vahelehe raam; koti, meisterdamise ja 13 oskuse nelja haruga vaade; ühepunktiline õppimine, eeldused/astmed/detailid; A/Enter õpib, hiireklõps uurib; Nupsi B/T, kang/ristnupud, A/B, LB/RB, filtrid, kerimine ja valiku säilimine | Ülesannete/ehituse/kaardi täielik sisu ning EN/ET keeleseadistus; kõrgushüppe maailmamõju |
| Päev ja ellujäämine | Ainult päev/õhtu valgustuse testlüliti | Automaatne 300+60 tsükkel, paus, nälg/janu/elu, uni, öö ja kaotus |
| NPC-d | Leina/Bronkingsi lihtsad vihjed | Kuus identiteeti, portreed, ühekordsed tarnevahetused, tasud, kodutellimus |
| Ehitus ja tootmine | Lõkke/ahju/kasti/peenra ruudupaigutus proovilaagris, kütus ja kastid; kõik viis kultuuri õigete kasvuaegade/saakidega, makse paigaldamisel | Kogu brauserikaardi paigutusreeglid, 0.6 kodutellimus, muu mööbel ja maailm |
| Võitlus ja avastamine | Kohalikud loomad/vastased ja lähivõitlus, laaditavad nooled/saak/XP, puldi/hiire sihtimine, õng ja proovikaevandus; Nupsi meteoriit/sõprus/järgnemine/ootamine, aeglustus ning Star/Frost/Helper pesa töö | Kogu piirkondade/vastaste/dungeon'i kaart, vulkaan, paadid/vaal/vikerkaar ja kaotuse täielik päevavahetus |
| Salvestus | Laagri v4: v1–v3 kadudeta üleviimine, inventar/tööriistad/jaamad/oskused, maailma aeg, ressursside ja loomade olek, taimed ning koopa/pinna maasolevad esemed | Terve brauserimaailma migratsioon, mängija positsioon, kogu kaardi stseenid/sündmused ja ehitus |

## 13. Teostusjärjekord ja valmimise tingimused

Järgmine etapp on brauseri **esimese tervikliku mänguteekonna** taastamine õige UI-ga, mitte uute süsteemide juhuslik lisamine. Töö jagatakse kontrollitavateks osadeks; iga osa peab sisaldama reeglit, nähtavat tagasisidet, puldikasutust ja salvestuse tulemust.

1. **Kinnista lähteolek ja sisendileping.** Kuus kiirribakohta, algkirves, valiku käitumine, A/RT rollid, View/üles, Y ehitus ja menüü vahelehed. Säilita kasutaja rahulik kaamera ja pehme tõrvikuvari.
2. **Taasta korjamise ja seljakoti täpne majandus.** Õiged löögid, saak, kännud, piisav algusvaru, taastumine, 20-pesaline inventar ja täis koti käitumine. Mõlemad teed — algkirves ja lahtised varud — peavad töötama ilma testvarude süstimiseta.
3. **Taasta menüüraam, seljakott ja meisterdamisvaade.** Õige ruudustik/detailid, eraldi tegevused, kategooriad, jaamanõuded, fookus ja kerimine. Puldiga peab saama kõike teha ilma hiire abita.
4. **Lisa hoiustamine, peenar ja tootmine.** Kasti tehingud ning lähikasti materjalid, kasv ja saak, lõke/ahi/kütus; inventari ja jaama olek säilib.
5. **Taasta praegune kodu- ja NPC voog.** Leina tarne, Bronkingsi tellimus/uuendus, kolm päris mängupäeva või tavalist puhkust, sisustus ja ohutu ukseesine. Ära too vana õue moodulmaja esmaseks ehitusvooguks tagasi.
6. **Taasta ülejäänud edenemine ja maailm.** Oskused, ellujäämine/kaotus, võitlus, Nups, koobas, muud bioomid ja sündmused; läbimängitavad päeviku etapid.
7. **Valideeri tervik.** Värske seiklus ilma kunstlike varude/XP/aja lisamiseta, salvestus ja laadimine, mõlemad keeled, sihtresolutsioonid, füüsiline pult ja visuaalne võrdlus.

Kogu brauseritaseme valmidust ei saa järeldada sellest, et esimene kirka töötab või parser annab puhta tulemuse. Godoti praegused testid tõendavad proovilaagri sisemist toimimist; brauseriga võrdluseks peavad testid ootama brauseri väärtusi.

## 14. Kontrolliplaan ja tõendite piirid

| Kontroll | Valmimise tõend |
| --- | --- |
| Andmete vastavus | Kõik esemete/retseptide/NPC/oskuste ID-d ja baasarvud ühtivad eksporditud lähteandmetega |
| Värske algus | Algvarustus, korjamine, kiud, kirka ja tõrvik on UI kaudu tehtavad; puuduva ressursi või ebaõige tööriista korral on arusaadav põhjus |
| Tehingud | Blokeeritud craft/ülesanne/kastitoiming ei muuda osaliselt koguseid; täis koti korral ei kao saak |
| Puldiga UX | Avamine, vahelehed, kategooriad, ruumiline fookus, kerimine, tegevus ja tagasi toimivad; vajutuse serv ei tekita topelttegevust |
| Ehitus/kodu | Absoluutne ruut ei liigu kõndimisega, kaamerasuunad ei muuda valikut, blokeerimise põhjus on õige; kodutellimus tasub üks kord ning uuendus säilitab sisustuse |
| Maailm ja aeg | Aeg peatub menüüs, taastumine ja tähtajad säilivad, uni ja kaotus annavad õige uue oleku, koopad/vulkaan ei jaga ekslikult esemeid |
| Salvestus | Laadimine taastab maailma/tegelase, varud, ülesanded ja tähtajad; vana salvestus säilib või migreeritakse selgelt |
| UI/resolutsioon | EN/ET 1280×720, 1920×1080, 3840×2160; ei ole teksti/ikooni kattumist ega menüüraami hüppamist |
| Kunst | Tegelik Godoti pilt võrdlusnurgast ja teisest nurgast, kõnni/korjamise klipp, mõistlikud mõõdud ja sama valgus; proovikujud ei asenda lõplikku heakskiitu |

Olemasolevad brauseritestid on regressioonispetsifikatsioon. [0.6 kontrolliaruanne](e2e-results-v06.txt) kirjeldab 52 mudelitesti ja 0.6 stsenaariume; see on ajalooline kontrollitulemus, mitte väide, et need jooksutati selle dokumendi koostamisel uuesti. Vanem [pideva värske mängu teekond](e2e-results-v043.txt) tõendab toonast käsitsi maja ehitust; 0.6 praeguse kodu jaoks tuleb kasutada selle asendanud testivoogu. Seemendatud salvestusega süsteemitest ei tõenda kogu mängu normaalajas algusest läbimist.

Praeguses kohalikus Godoti katses kinnitas kasutaja füüsilise puldiga liikumist, korjamist ning kirka, kirve ja tõrviku kasutamist. Kohalikud automaattestid kontrollivad muu hulgas kaameranurga stabiilsust, tehinguid, menüüsisendit, tööriistu, ammendumist ja laadimist. Need ei kinnita veel kogu brauserimehaanika vastavust ega lõplikku visuaalset kvaliteeti.

## 15. Vastuolud ja eraldi otsust vajavad küsimused

- **Puu/kivi kokkupõrge.** Brauseri liikumisblokeerijad ei hõlma samal viisil puid ja kive; Godoti üleandmine nõuab tüve füüsikat. Täpse mehaanikakoopia ning uue 3D füüsikalepingu erinevus tuleb enne lõplikku maailmaliikumist lahendada. Känd ei tohi jääda nähtamatuks täiskõrguseks blokeerijaks.
- **Maapinna projektsioon.** 0.6 kasutajanõue kirjeldab ekraanil võrdselt laiu ja kõrgeid ruute; uue 3D dioraami vaatenurk võib ruudud projitseerida teisiti. Seda ei nimetata automaatselt sama tulemuse saavutamiseks. Paigutus ja suhteline kaugus vajavad visuaalset võrdlust.
- **Vanad nupujuhised.** README 0.4 kontrollitabel ja uued 0.6 vood ei kattu kõigis avamisnuppudes. Praeguse `readPad()` käitumine ja kontekst on alus; Y ehitab, View/üles avab koti. Godoti senine Y-koti alias on ajutine erinevus.
- **Retseptiproosa ja taimobjekt.** Ajaloolise „ühest taimest kolm kiudu” sõnastuse kõrval on praeguses koodis kolm maitsetaime ühelt maailmaobjektilt ja kolm kiudu ühe inventarieseme kulutamisel. GDD eristab neid etappe.
- **Mudeliretseptid ja nähtav UI.** Kõik 48 retsepti on andmemudelis, kuid vana õue moodulmaja retseptid ei tähenda, et 0.6 õuemajavoog tuleks tagasi muuta. Piirangud on osa disainist.
- **Suure kivi taastumine.** Korjamine kirjutab tähtaja, aga taastamisfunktsiooni lubatud tüüpide loend välistab suure kivi/maagi. Seda tuleb käsitleda koodifakti ja võimaliku disainiküsimusena, mitte oletada kõigi ressursside taastumist.
- **Salvestuse üleviimine.** Brauseri salvestuse import Godotisse ei ole tehtud. ID-de/mõõtkava/stseenide teisendus peab olema eraldi kontrollitud, enne kui saab lubada vana seikluse jätkamist uues mootoris.
- **Turu- ja väljalaskeplaan.** README varasem soovitud hind või avaldamiskoht ei tõenda avaldatud mängu, kinnitatud äriplaani ega saadud vanusepiirangut. Need ei ole praeguse pariteedietapi vastuvõtukriteeriumid.

## 16. Dokumendi hooldus ja allikad

Pärast teadlikku disainimuudatust uuendatakse esmalt muutunud reeglit ja vastavat kontrolli ning siis GDD-d. Andmetabelid uuendatakse käsuga `node scripts/export-design-baseline.mjs`; ekspordi muutus ei kirjuta ümber mängu ega salvestusi. Godoti pariteedirea saab lõpetatuks märkida alles siis, kui brauseriga võrreldav kontroll ja nähtav UX on läbitud.

Põhiallikad:

- [README ja versioonide ajalugu](../README.md)
- [0.6 nõuded ja valitud kunstisuund](v06-requirements.txt), [0.6 väljalase](v06-release.txt), [0.6 kontrollid](e2e-results-v06.txt)
- [0.5 UX ja controller-disain](v05-design-notes.txt), [0.5.1 renderdusparandus](render-fix-v051.txt)
- [Ajaloolised retseptipõhimõtted](recipes.txt), [0.4.3 pidev teekond](e2e-results-v043.txt), [0.4.2 teekond ja kaotus](e2e-results.txt)
- [Brauseri andmemudel](../src/model.js), [mänguloogika ja UX](../src/game.js), [ekraanid](../src/index.html), [stiilid](../src/style.css), [keel](../src/i18n.js), [heli](../src/audio.js)
- [Praegused brauseritestid](../tests), [Godoti testid](../godot/tests), [Godoti prototüübi juhis](../godot/README.txt)
- [Kohalik Godoti üleandmine](LOCAL-CODEX-GODOT-HANDOVER.txt), [kunstniku leping](FABLE-BLENDER-HANDOVER.txt), [vara manifest](../godot/assets/manifest.json)
- [Heaks kiidetud NPC-kujundused](npc-concepts-v2.png), [visuaalse sihi leht — paneel 2](v06-art-directions.png)


## Uued otsused · 25. november 2026

Ämber (1 puit + 10 rauamaaki), talvepiirkonna pingviin ja Mattiase kolm
bossidisaini on kirjas [uute ideede lehel](MATTIAS-NEW-IDEAS.md). Need on teadlikud
lisandused brauseri lähtealusele, mitte tagantjärele muudetud brauserireeglid.
