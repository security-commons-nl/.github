# Redactiestatuut security-commons-nl

Vastgesteld 28-08-2026, B3 en B10 aangevuld op 29-08-2026, B4 op 30-08-2026, A11 toegevoegd op 31-08-2026, B13 en B14 op 02-09-2026, Cbw in B2 op 02-09-2026, B9 herzien op 03-09-2026 (PROJECTEN.md), B14 verduidelijkt op 03-09-2026, B2 aangevuld en B15 toegevoegd op 25-09-2026 (vindbaarheid van het register aangevuld dezelfde dag), B3 aangevuld op 13-10-2026 (leesversie per stuk), B4 aangevuld op 14-10-2026 (inhoudswijzers op de domeinroot), blok C toegevoegd en B2, B8, B9, B13 en B14 aangevuld op 29-10-2026 (de site is het product, het profiel), C5 aangevuld op 30-10-2026 (automatische controle, prototype in een route). Geldt voor alle repo's van de organisatie. De inhoudsregels (A) gelden overal.
letterlijk; de structuurregels (B) gelden overal in vorm, met per repo één afspraak over wat de eerste
laag betekent (zie B1). Waar een repo een script heeft dat deze regels controleert, verwijst elke melding
naar het regelnummer hieronder.

Dit statuut vult [PRINCIPLES.md](PRINCIPLES.md) (waarom we dit doen), [CONTRIBUTING.md](CONTRIBUTING.md)
(hoe je bijdraagt) en [DOCUMENTATION-STANDARD.md](DOCUMENTATION-STANDARD.md) (documentatie bij software) aan.

## A. Inhoud

**A1. Geen auteursvermelding.** Alles hier komt van vakgenoten; dat hoeft er niet bij. Geen namen, geen
"vakgenoot", geen "aangedragen door", geen `auteur:` in frontmatter, geen kopje "Auteur". Wat wel mag:
de herkomst als rol of organisatietype, als dat de lezer helpt ("in gebruik bij de CISO-organisatie van een
gemeente"). Wie deelt, hoeft daar zijn naam niet aan te verbinden. Dat verlaagt de drempel voor iedereen.

**A2. Persoonsnamen in de inhoud.** Alleen publieke functionarissen in hun publieke hoedanigheid (een
minister, een directeur van een instituut, een wethouder in een citaat uit een publiek stuk). Alle anderen
worden een functiebeschrijving. Fictieve namen in lesmateriaal mogen, met de vermelding "verzonnen".

**A3. Organisatienamen.** Publiek bekende casussen en bronnen mogen (een gemeente in een publiek
incidentrapport, NCSC, AP, VNG, IBD). De organisatie waar een stuk vandaan komt wordt nooit genoemd, tenzij
die organisatie zelf publiceert of schriftelijk instemt. De eigen organisaties van bijdragers worden nooit
als herkomst genoemd.

**A4. Toestemming.** Andermans werk alleen met toestemming van de auteur. De toestemming zelf staat niet in
de repo; wel de zin "gedeeld met toestemming". Waar de toestemming is vastgelegd bepaalt de plaatser, en
dat is nooit git.

**A5. Links.** Externe links alleen naar instituties, normen, wetten, overheidspublicaties, GitHub-repo's en
gedocumenteerde tooling. Geen links naar sociale media (LinkedIn, X, Substack, Medium, Facebook, Instagram),
persoonlijke blogs of profielen. Een bron van sociale media wordt tekst: "via LinkedIn", zonder link en
zonder naam. Interne links relatief, zodat ze op GitHub en op de website werken.

**A6. Datums.** Alleen een datum die de geldigheid van de inhoud bepaalt: `peildatum` (dataset,
dreigingsbeeld) of `versie` (document dat de bron zelf nummert). Die staat in de frontmatter, formaat
`JJJJ-MM-DD` of `JJJJ-MM`. Geen "opgenomen op", "gevonden op" of "aangedragen op" in de tekst; dat is
git-metadata. Een changelog in een README ("bijgewerkt na review") mag, omdat die over de inhoud gaat.

**A7. AI-gebruik.** Wordt niet per stuk vermeld; dat is consistent met A1. Wat wel geldt: een mens heeft
elk stuk gelezen en begrepen voordat het op `main` staat. Principe 8 (AI bereidt voor, de mens beslist) blijft leidend.

**A8. Git-historie.** Wordt niet herschreven om namen of herkomst te verwijderen; fix vooruit in een nieuwe
commit. Uitzondering: persoonsgegevens van derden of geheimen (sleutels, wachtwoorden). Dan wél
history-rewrite, rotatie van het geheim, en een regel in het besluitenlog van de repo.

**A9. Interne stukken.** Documenten van de eigen organisaties (pdf's, xlsx, interne memo's) komen in geen
enkele repo, ook niet "even tijdelijk". Eerst anonimiseren tot een sjabloon of casus, dan pas plaatsen.

**A10. Taal.** Nederlands. Engelse vaktermen blijven Engels (SSDLC, passkeys, red teaming, blue team).

**A11. Vragen.** De commons publiceert niet alleen wat we weten, ook wat we zoeken. Een vraag valt
onder dezelfde inhoudsregels als een gedeeld stuk: geen naam nodig (A1), personen worden functies (A2),
en de organisatie van de vrager wordt nooit genoemd (A3). Vragen onder een schuilnaam mag expliciet en
hoeft niet te worden toegelicht; in dit vakgebied is een hulpvraag ook een uitspraak over wat je zelf
nog niet geregeld hebt, en die drempel hoort niet bij ons te liggen. **Om dezelfde reden beschrijft een
vraag het vraagstuk op sectorniveau en nooit de situatie van een organisatie, ook niet die van onszelf.**
Geen "wij hebben dit niet opgelost" en geen "daar hebben we weinig van": dat is voor wie kwaad wil een
kant-en-klare inventarisatie. Schrijf wat er in het veld ontbreekt, en beschrijf de eigen positie alleen
in wat er al gedeeld is. Nodig een lezer ook niet uit om zijn eigen gaten te benoemen. Wat een vraag wel moet bevatten:
waar je zelf al staat, wat je zoekt, en wat er met het antwoord gebeurt. Zonder dat laatste weet
niemand waarom hij zou antwoorden. Een beantwoorde vraag verdwijnt niet maar wijst naar het stuk dat
eruit voortkwam; dat is het bewijs dat het werkt. Een vraag die een jaar open staat wordt herschreven
of weggehaald, want een lijst met onbeantwoorde vragen leest binnen een half jaar als een kerkhof.

## C. De publicatie

De eenheid van de commons is de route, niet de repository. Blok A zegt wat erin mag, blok B hoe een stuk en
een repo eruitzien; dit blok zegt hoe het geheel leest. Toegevoegd 29-10-2026 na feedback van twee externe
lezers die losse bouwstenen zagen in plaats van een geheel; het plan
[de site is het product](plannen/2026-10-29-site-is-het-product.md) legt de afwegingen vast.

**C1. De site is het product, GitHub de werkplaats.** Alles wat een lezer nodig heeft staat op
`security-commons-nl.github.io`. Een link naar github.com staat alleen waar de lezer iets moet doen dat de
site niet kan: code draaien (een script of een lokale tool), een issue of discussion openen, meebouwen. In een
leesroute komt geen repo-naam voor; een instrument heet naar wat het doet ("de zelfcheck", "de meting"),
niet naar zijn repository. Reden: wie kennis zoekt en een organisatieprofiel van een ontwikkelaar krijgt,
haakt af; de repositories zijn het hoe, niet het wat. B13 blijft bestaan en geldt voor de werkplaats: elk
project heeft een pagina, maar die pagina is pas voordeur als het project in een route zit (C2). De
projectenlijst staat op `security-commons-nl.github.io/werkplaats/`, niet op de voorpagina.

**C2. Elk stuk zit in een route, of het staat in de catalogus.** Een leesroute is een geordende reeks stukken
voor één rol in één situatie: de eerste honderd dagen als ISO, een CISO die op de Cbw voorsorteert, een
privacy officer vóór een DPIA. De routes staan in `site/routes.json` van de site-repo, met per stap één zin
waarom nu; de voorpagina toont ze onder "Begin bij je rol". Een stuk dat in geen enkele route past, blijft
vindbaar via zoeken en de catalogus (de kennisbank-index per vakgebied), maar staat niet op de voorpagina en
niet in de voordeur per rol. Een nieuw stuk in de kennisbank noemt in de frontmatter zijn route(s) in het
veld `route`, of expliciet `route: geen`; de build van de kennisbank blokkeert een stuk zonder dat veld
(sinds 29-10-2026; alle bestaande stukken hebben het veld). Reden: dit is de rem op de breedte. De vraag "in welke
route hoort dit, en op welke plek" wordt gesteld vóór het schrijven, niet erna. Geldt streng, ook voor nieuwe
stukken die al gepland zijn.

**C3. Een instrument is een stap in een route, geen product in een lijst.** Een instrument staat op de
voorpagina alleen als stap in een route, met de vraag die het beantwoordt als titel. De projectentabel (B9)
blijft de bron voor de werkplaats en de catalogus, maar wordt niet als lijst op de voorpagina getoond.
Reden: een lezer merkt fragmentatie van software pas als hij software gebruikt; een instrument dat als
bijlage bij een handleiding komt ("lees dit, en als je het wilt meten, hier is een pagina die rekent") is
een hulpmiddel, geen product dat moet concurreren met twintig andere.

**C4. Eén publicatie, één gezicht.** Elke pagina op de site, instrument of tekst, deelt dezelfde huisstijl
(`thema.css` van de site-build, besluit 15-10-2026), hetzelfde kruimelpad (B10), dezelfde taal (A10:
Nederlands, ook knoppen, labels en foutmeldingen), en toont onderaan versie of peildatum (A6) en de status
(B8). Reden: de commons komt van meer dan één maker en dat mag je niet zien.

**C5. De lat voor instrumenten in een route.** Een instrument staat pas in een route als het:
- volledig in de browser rekent (B14) en offline werkt na één keer laden;
- zijn rekenregels in één referentie-implementatie heeft met tests, en de browserversie daartegen toetst
  (zoals procescheck en de CSIR-tool doen met `reken.py` en `app.js`);
- tests in CI heeft die groen zijn, met een link naar die tests op de pagina;
- een versienummer en peildatum op de pagina toont;
- geen fouten in de browserconsole geeft en werkt op een telefoon (375 px breed, zonder horizontale scroll);
- een export heeft in een open formaat (JSON of Markdown) die de gebruiker zelf bewaart, en die import weer
  inleest (geen account, geen opslag: de gebruiker is zijn eigen dossier).

Een instrument dat de lat niet haalt, draagt status `prototype` of `concept` (B8) en staat in de catalogus,
niet in een route. De lat wordt gehaald op het moment dat een instrument wordt aangeraakt, niet in één
operatie; een instrument dat niemand aanraakt, blijft prototype en dat is eerlijk. Een prototype dat al in een
route stond toen deze regel kwam (29-10-2026), blijft daar tot het de lat haalt bij zijn eerstvolgende aanraking;
de CI van de site waarschuwt bij elke build voor een prototype in een route (`site/test_routes.mjs`), zodat het
zichtbaar blijft en niet stil wordt vergeten.
Reden: "vibe-coded" is geen probleem van herkomst maar van toetsbaarheid; wat getest, versienummerd en
uniform is, hoeft zich niet te verdedigen. `repo-compliance.yml` controleert sinds 30-10-2026 bij elk instrument
met status `in gebruik` de meetbare delen: een teststap in CI, een versie of peildatum op de pagina, de status op
de pagina gelijk aan de projectentabel, en een kruimelpad naar de voorpagina (B10). Huisstijl, telefoonbreedte en
consolefouten zijn een toets met het oog bij elke aanraking, en staan per instrument in de tabel van het plan.

## B. Structuur

**B1. Item = map met README.** Elk stuk is precies één map met een `README.md`, exact twee lagen diep:
`categorie/item/`. Wat "categorie" betekent, staat per repo vast:

| Repo | Eerste laag |
|---|---|
| kennisbank | vakgebied: `security`, `privacy`, `bcm`, `governance`; items van type `handleiding` dragen `barrieres:` uit `paden.json` en zijn de bron van het handelingsperspectief |
| dreigingsanalyse | maandversie (`vJJJJ.MM`) |
| aanvalspaden | `check/` (de zelfcheck), `methode/`, `meting/` (volgt); `paden.json` op de root is de bron |
| overige repo's | volgt `DOCUMENTATION-STANDARD.md` (software) of één regel in de eigen README |

Geen losse bestanden in een categorie-map behalve `README.md` en gegenereerde `index.html`. Geen derde laag.
Mapnamen: kleine letters, cijfers en koppeltekens; geen spaties, geen versies of woorden als "definitief".

**B2. Frontmatter, negen velden, vast.** Elke item-README begint met (het negende veld, `route`, sinds 29-10-2026, C2):

```yaml
---
titel: Leesbare naam van het item
vakgebied: security | privacy | bcm | governance      # per repo: de eerste-laag-waarde
type: beleid | sjabloon | lesmateriaal | dataset | referentie | aanpak | rapportage | handleiding
normen: [BIO2, ISO 27001, AVG, NIS2, Cbw, CRA, AI Act, GIBIT 2025, ISO 22301]   # mag leeg: []
peildatum: JJJJ-MM-DD          # óf versie: "1.3 (herzien BIO2), 2026-08"; één van beide
herkomst: rol of organisatietype, geen naam
status: concept | in gebruik | sjabloon | gearchiveerd
samenvatting: twee tot vier zinnen; dit wordt de kaarttekst op de website
route: [iso, eerste-honderd-dagen]   # id's uit routes.json van de site, of: geen
---
```

`Cbw` en `NIS2` mogen naast elkaar staan als een item beide raakt: de richtlijn voor de Europese
context, de wet voor de Nederlandse verplichting (aangevuld 02-09-2026, issue #16).

`auteur` bestaat niet (A1). `licentie` alleen als het item afwijkt van EUPL-1.2 (B5). Bij type
`handleiding` komen daar drie velden bij: `barrieres` (verplicht, `vraag_id`'s uit `paden.json`),
`rol` (`fundering`, `alternatief` of `verdieping`) en `pijler` (het item waar de handleiding uit
voortkomt). Elk item mag daarnaast `bronnen` dragen: een lijst met id's uit `bronnen.json` op de
root van de kennisbank (B15). `route` noemt de leesroute(s) waarin het stuk een stap is, of `geen`;
`tools/build.py` controleert in twee richtingen tegen `routes.json` (kopie van de site, `tools/haal_routes.py`).
Andere velden niet.

**B3. Bestandsvormen.** Markdown is de bron. Elk tekstitem heeft daarnaast een self-contained HTML-leesversie
(geen externe fonts of scripts, print op A4, plakbaar in Word). Binaire bestanden (docx, pptx, xlsx, pdf)
alleen als er geen redelijke markdown-vorm is, en dan met een README die zegt wat erin zit.
Wat in de map van een item staat, staat als **link** in de README en op de leesversie. Een bijlage die
alleen als bestandsnaam wordt genoemd, bestaat niet voor een lezer die op de pagina binnenkomt: hij ziet
de beschrijving en kan er niet bij. Verwijzingen wijzen naar bestanden die bestaan en blijven binnen de
eigen repo. In de kennisbank blokkeert `tools/build.py` op alle drie.
Een los stuk naast de README (een procedure, een brief, een beleidsstuk) heeft een eigen leesversie met
dezelfde naam en `.html`, met een link terug naar de markdown; de leesversie van het item linkt naar die
leesversie. In de kennisbank maakt `tools/build.py` hem en blokkeert hij als hij ontbreekt of achterloopt.

**B4. Indexpagina's worden gegenereerd.** De overzichtspagina's (`index.html` per categorie en op de root)
zijn output van een script dat eerst alle regels controleert en dan bouwt. Handmatig bewerken is
zinloos: de volgende run overschrijft. Het script blokkeert bij elke overtreding en noemt bestand, regel
en regelnummer. Het draait lokaal vóór een commit en als GitHub Action bij elke push naar `main`.
De **volgorde van de items** op die pagina's is redactioneel en staat als genummerde lijst onder
`## Volgorde` in de README van de sectie. Alfabetisch sorteren zet toevallige mapnamen bovenaan; deze
lijst zet er een oordeel in: wat je morgen kunt toepassen bovenaan, naslag in het midden, verwijzingen
naar het werk van anderen onderaan. Zelfde principe als B9 voor de projectentabel. Ontbreekt een item in
de lijst, of staat er een naam die niet bestaat, dan blokkeert de build.
De **inhoudswijzers** vallen onder dezelfde regel: `sitemap.xml` en `llms.txt` worden afgeleid, nooit met
de hand bijgehouden. De kennisbank schrijft ze bij elke build zelf uit de frontmatter, met elk stuk en elke
losse leesversie. De root-site telt en somt de kennisbank niet op, maar verwijst: `robots.txt` naar beide
sitemaps, `llms.txt` naar `kennisbank/llms.txt`. Een uitgelicht stuk in de root-`llms.txt` mag, een
handgeteld aantal niet. `site/test_inhoudswijzers.mjs` in de root-site blokkeert als dat terugkomt.

**B5. Licentie.** EUPL-1.2 voor alles. Wijkt een bron af (CC-BY, MIT, "alleen met toestemming"), dan is
`licentie:` in de frontmatter verplicht en staat er een zin in de README.

**B6. Commits.** Nederlands, één onderwerp per commit, map als prefix: `security: Security Annex toegevoegd`.
Geen AI-attributie of sessie-verwijzingen in de commitboodschap (A7).

**B7. Bijdragen.** Een issue of discussion is een volwaardige bijdrage; maintainers zetten het om. "Maak maar
een PR" is nooit het antwoord.

**B8. Statuslabels.** Elk project draagt precies één van vier labels, met deze criteria. Het label staat op
het org-profiel; dat profiel is de enige bron (B9).

| Label | Criterium |
|---|---|
| **in gebruik** | Draait echt (gehost, of geinstalleerd bij een organisatie) en heeft tests of CI die groen staan. Iemand gebruikt het vandaag. Een instrument haalt daarnaast de lat van C5; haalt het die niet, dan is het een prototype (29-10-2026). |
| **prototype** | Werkt en is te draaien, maar zonder belofte over volledigheid, onderhoud of ondersteuning. |
| **concept** | Ontwerp, plan of documentatie; geen werkende code. Ook een mockup valt hieronder. |
| **gearchiveerd** | Niet meer onderhouden. Blijft leesbaar, krijgt hooguit kritieke beveiligingsfixes. |

Bij twijfel geldt het lagere label. Een project dat zichzelf hoger labelt dan de criteria toelaten, is een
belofte aan een lezer die je niet waarmaakt.

Een repo die geen project is maar infrastructuur (een proxy, de site-build) draagt in zijn README het
label `infrastructuur`, staat niet in de projectentabel maar in de alinea "Onderliggende infrastructuur"
eronder, en wordt wel gecontroleerd op de README-kop en de licentie (B11, B5).

**B9. PROJECTEN.md is de enige projectenlijst.** `.github/PROJECTEN.md` bevat de projectentabel; de
voorpagina, `llms.txt`, `sitemap.xml` en de root-`CLAUDE.md` worden daaruit gegenereerd of afgeleid. Een
project bestaat pas als het in die tabel staat, met label en doelgroep. De volgorde van de tabel is
redactioneel: de eerste drie rijen met een live link zijn de uitgelichte kaarten op de voorpagina. Repo's
die geen project zijn (infrastructuur, gearchiveerd, opgegaan in een ander project) staan in de alinea's
onder de tabel, met de reden erbij; `repo-compliance.yml` eist dat elke repo op een van die plekken staat.
Het organisatieprofiel (`profile/README.md`) verwijst naar deze lijst en naar de voorkant op Pages.
Sinds 29-10-2026 (C1, C3) toont de voorpagina de tabel niet meer als lijst; de kaarten staan op
`security-commons-nl.github.io/werkplaats/`, en de eerste drie rijen met een live link blijven de
uitgelichte kaarten op de voorpagina, met een naam die zegt wat het instrument doet in plaats van de
repo-naam.

**B10. Elke pagina wijst terug.** Elke pagina op Pages begint met een kruimelpad naar de hoofdpagina en
naar het niveau erboven, bijvoorbeeld: Security Commons NL > Kennisbank > Security > Passkeys invoeren. Een
losse tool krijgt minimaal Security Commons NL > naam van het project. Reden: veel lezers komen via een
zoekmachine binnen op een diepe pagina en moeten van daaruit de rest kunnen vinden. In de kennisbank zet
`tools/build.py` het kruimelpad automatisch en bewaakt `--check` dat het er staat; in een losse tool staat
het in de eigen opmaak. Elke leesversie **sluit af** met een voetregel naar de bronbestanden van dat item,
de licentie en de plek om een verbetering voor te stellen. Zonder die regel is een itempagina een
doodlopend eind: wel de tekst, geen route naar de map met de bijlagen, terwijl de gegenereerde
overzichtspagina's zo'n voet al hadden.

**B11. Elke repo heeft dezelfde kop.** De README van elke levende repo begint met: de naam als `#`-kop, een
zin wat het is en voor wie, een regel `Status: <label>.` met daarachter in gewone woorden wat werkt en wat
niet, en daarna de koppen `## Voor wie`, `## Snel starten`, `## Bijdragen` en `## Licentie`, in die
volgorde. Meer mag, minder niet. Een aparte `docs/`-map is alleen nodig als de README anders langer dan
ongeveer 1500 woorden wordt. Reden: een bezoeker die van de voorpagina doorklikt naar GitHub moet in tien
seconden zien wat het is, of het werkt en hoe hij begint. `repo-compliance.yml` controleert dit.

**B12. Status staat op een plek.** Het label in de projectentabel is de bron. De regel `Status:` in de
README van de repo herhaalt dat label letterlijk; `repo-compliance.yml` vergelijkt beide en wordt rood
als ze verschillen. Wie een status wijzigt, wijzigt eerst de tabel.

**B13. Elk project heeft een pagina.** Elke repo in de projectentabel publiceert een pagina op
`security-commons-nl.github.io/<naam>/`, ongeacht status. Minimaal is dat de leesversie van de README,
gebouwd met de gedeelde site-build; een tool of kennisbank publiceert zijn eigen pagina. De kolom *Direct
openen* in de projectentabel zegt wat een lezer aantreft: *Live tool*, *Leesbare versie* of *Ontwerp*; een
rij met alleen een ontwerp staat niet in de eerste drie rijen, want dat zijn de uitgelichte kaarten. Reden:
de site is de etalage, GitHub de werkplaats. Een project dat alleen op GitHub bestaat is onvindbaar voor
wie via de voorpagina of een zoekmachine binnenkomt, en een concept op de site nodigt uit tot meedenken.
Infrastructuurrepo's (B8) vallen buiten deze regel. De uitrol naar bestaande repo's staat in
[het plan van 02-09-2026](plannen/2026-09-02-elk-project-een-pagina.md). Sinds 29-10-2026 geldt deze regel
voor de werkplaats en de catalogus: een projectpagina is pas voordeur als het project in een leesroute zit
(C2, C3).

**B14. Een project is een instrument of een script, nooit een applicatie.** Een instrument rekent
volledig in de browser, zonder server, account of telemetrie, en is het enige dat in de projectentabel
*Live tool* heet. Een script draait lokaal op data die de gebruiker al heeft, zonder server en zonder
eigen opslag, en staat in de tabel als *Leesbare versie* met een download; de README zegt waarom het
geen instrument is. Een applicatie met backend, database, authenticatie of gedeelde staat hoort niet in
de commons. Infrastructuur die een instrument opt-in ondersteunt (B8) is de uitzondering en wordt met
naam in `BESLUITEN.md` vastgelegd. Reden: een tool die een DPIA, inkoop en een beheerder vraagt voordat
iemand hem kan proberen, haalt de drempel niet weg waarvoor de commons bestaat; wat je opent, gebruik je
vandaag. Vastgesteld 02-09-2026 (issue #17); `repo-compliance.yml` controleert dit niet, de projectentabel
en het plan *lichte commons* zijn de controle. Een opt-in AI-hulp met de sleutel van de gebruiker maakt van een
instrument geen applicatie, mits: een aparte pagina met eigen Content-Security-Policy zodat de tool zelf
`default-src 'none'` houdt; de sleutel alleen in `sessionStorage`, nooit in dossier, voorstel of URL; de
uitkomst een voorstel dat de gebruiker per regel overneemt, nooit een schrijfactie in het dossier; en
toestemming per sessie met de melding wat waarheen gaat (verduidelijkt 03-09-2026, issue #18; het
patroon staat in het plan *AI-hulp*). Browseropslag op het eigen apparaat is geen opslag in de zin van deze regel:
het profiel van de commons (zestien vragen, twee met een vervolgvraag, alleen vaste keuzes, geen naam of inventaris) staat onder één bewaarnaam
`commons-profiel` voor alle pagina's op het domein, elke pagina die het leest zegt dat en heeft een wisknop, en
niets ervan gaat naar een server (verduidelijkt 29-10-2026, plan *de site is het product*, stap 9).

**B15. Verwijs naar wat anderen al hebben.** De commons staat niet naast het stelsel maar erin. Heeft
een andere partij over hetzelfde onderwerp al een handreiking, factsheet, tool of uitleg, dan verwijst
het item daar met naam en adres naar, naar het specifieke stuk en niet naar een homepage. Dat maakt een
item bruikbaarder, voorkomt dat de commons dubbel werk doet, en doet het werk van anderen recht.

- **Een register, een plek per stuk.** Verwijzingen staan in `bronnen.json` op de root van de
  kennisbank: titel, adres, partij, toegang en de datum waarop iemand het stuk zag. Een item noemt alleen
  de id's, in het veld `bronnen` (B2). Verhuist een stuk, dan verandert een regel en niet elk item dat
  ernaar wijst.
- **De partij komt uit de stelselkaart.** Elke bron hoort bij een partij uit
  `security/stelselkaart-security-gremia/`, en die partij heeft een adres. Dat adres is de terugval:
  blijkt een stuk weg, dan krijgt de bron `vervallen` met de datum en wijst de leesversie naar de partij
  zelf, zo mogelijk met een archiefversie. Een dode link wordt zo een aanwijzing waar je verder zoekt.
- **Eerlijk over de toegang.** `open`, `inlog` of `onbekend`. Bij `inlog` staat erbij wie er wel bij
  kan (de `kring`, bijvoorbeeld "gemeenten, via de community van de IBD"). Wat achter een inlog staat,
  kan de commons niet controleren; daarom staat de datum `gezien` op de pagina. Een verwijzing naar een
  besloten stuk noemt de titel en de plek, nooit de inhoud (A9).
- **Alleen wat al openbaar bestaat.** Een besloten stuk komt alleen in het register als zijn *bestaan*
  openbaar is en alleen het stuk zelf achter de inlog staat, bijvoorbeeld een product dat op een
  openbare productpagina staat maar pas na inloggen te downloaden is. Nooit in het register: stukken met
  een TLP-markering (GREEN, AMBER of RED; ook een titel op een openbare pagina doorbreekt die), en
  samenwerkruimtes met eigen gedragsregels of een kring waar een lezer niet in kan komen. De build
  weigert een bron waarvan titel of adres naar een TLP-markering verwijst.
- **Wat de lezer ziet.** Onderaan de leesversie een blok *Wat anderen al hebben*, gegenereerd door
  `tools/build.py`. Een verwijzing in de lopende tekst, met een zin over wat het andere stuk wel en dit
  stuk niet doet, blijft daarnaast gewoon mogen en is vaak waardevoller dan de lijst.
- **Alles in het register is vindbaar, ook zonder item.** Het zoekvak van de kennisbank doorzoekt de
  eigen stukken en het register samen; een bron hoeft niet aan een item te hangen om gevonden te worden.
  Daarom staan de openbare catalogi van de IBD en CIP er in hun geheel in (`tools/haal_catalogi.py`).
  Zoekwoorden per partij en synoniemen staan als data in hetzelfde register; een zoekwoord per partij
  alleen als het niet vervuilt (een woord als "privacy" of "gemeenten" zou elke bron van die partij
  opleveren).
- **Wat de build controleert.** Elk id in een item bestaat in het register; elke bron heeft de
  verplichte velden, een https-adres, een partij uit de stelselkaart met een adres, en bij `inlog` een
  kring; hetzelfde adres staat er niet twee keer in; zoekwoorden horen bij een bestaande partij en een
  synoniemgroep heeft minstens twee woorden. A5 geldt: geen sociale media. `tools/test_zoeken.js` toetst
  het zoekvak zelf, op de gebouwde voorpagina.
- **Wat maandelijks gebeurt.** `tools/linkcheck.py` loopt elk adres na en opent een issue met label
  `linkcheck` bij een dood of veranderd adres. Het script wijzigt niets; een mens beslist of een stuk
  verhuisd is of weg.

Vastgesteld 25-09-2026. Reden: van de 56 items verwees er op die datum een naar het werk van een andere
partij in het stelsel, terwijl de stelselkaart van dezelfde kennisbank er 83 in kaart brengt.

## Wijzigen van dit statuut

Voorstel via issue of PR op deze repo (`.github`). Een wijziging krijgt een datum bovenaan en een regel in
[het besluitenlog van de organisatie](BESLUITEN.md). Scripts die regels controleren, worden in
dezelfde wijziging bijgewerkt.
