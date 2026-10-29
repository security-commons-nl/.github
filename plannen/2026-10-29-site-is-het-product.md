# Plan: de site is het product, de werkplaats staat erachter

**Doel:** de commons laten lezen als één publicatie met routes, in plaats van als een organisatie met
twintig repositories. De site (`security-commons-nl.github.io`) is het product; GitHub is de werkplaats en
komt alleen in beeld waar de lezer code moet draaien of wil bijdragen. Daarbij twee dingen die het statuut
nu niet afdwingt: een rem op de breedte (elk stuk zit in een leesroute, of het staat niet op de voordeur) en
een lat voor de instrumenten die in een route staan.

**Aanleiding:** op 29-10-2026 kreeg de initiatiefnemer schriftelijke feedback van twee externe consultants
die de commons op verzoek hadden bekeken. Geanonimiseerd, in hun woorden:

> *Consultant 1.* Een AI-kwetsbaarheidsscan van de site gaf geen bevindingen. Waarde voor minder volwassen
> publieke organisaties als centrale bron over weerbaarheid en compliance; de anonimizer en de BIA-tool zijn
> goed doordacht, de optie van een eigen of EU-gebaseerd taalmodel is een sterk punt. Maar: "a vibe-coded
> website [...] in its current state not groundbreaking [...] in an early stage of development. It almost
> resembles a large Excel workbook with many tabs covering different topics rather than a cohesive
> application that actively helps organizations move forward."
>
> *Consultant 2.* Interessant vanuit adviesperspectief, omdat het veel aspecten van de dienstverlening onder
> één paraplu brengt. Het waardevolste idee: de beweging van documentgebaseerde governance naar herbruikbare,
> evidence-driven en uitvoerbare governance (continuous control monitoring, compliance-as-code,
> AI-ondersteunde risicobeoordeling). "One important observation: the initiative appears to be creating
> separate building blocks rather than a single integrated platform." Code niet zelf gedraaid.

Beide zeggen hetzelfde: losse bouwstenen, geen geheel. De initiatiefnemer herkent dat: "van begin tot eind een
zooitje", ook al is "pak wat je nodig hebt" (de markt) een bewuste keuze.

**Besluiten bij het sparren (29-10-2026):**
1. De markt blijft. Eén geïntegreerde toepassing is het grc-platform dat op 02-09-2026 bewust is
   gearchiveerd ([lichte commons](2026-09-02-lichte-commons.md)); dat besluit wordt niet omgekeerd op basis
   van twee externe meningen. Een markt heeft wel een plattegrond nodig, en die ontbreekt.
2. De echte waarde zit in de pagina's op github.io, niet in de software erachter. De kennis en de routes zijn
   het product. De repositories zijn alleen relevant waar iets te draaien of te bouwen valt (anonimizer,
   scripts, meting).
3. De kennisbank zelf is ook te breed en moet strakker. Dat vraagt regels, niet alleen een andere voorpagina.
4. De software is "gewoon vibe-coded" en moet beter. Niet door herbouw, maar door een zichtbare lat per
   instrument, gehaald op het moment dat een instrument toch wordt aangeraakt.

**Wat niet mee gaat:** een backend, account of gedeelde staat (B14 blijft); een nieuwe projectenlijst naast
`PROJECTEN.md` (B9 blijft, maar geldt voor de werkplaats); het herschrijven van bestaande stukken om ze in
een route te persen (een stuk dat nergens past gaat naar de catalogus, niet op de schop); namen van de
consultants of hun bureau.

**Stand:** vastgesteld 29-10-2026; issue [.github#49](https://github.com/security-commons-nl/.github/issues/49) met de stappen als afvinklijst.
Op 29-10-2026 voorbereid op branches en getest, te mergen in deze volgorde: site #25 (voorpagina, werkplaats, routes) ·
`.github` #51 (statuut) · kennisbank #109 (veld `route`, routes per vakgebied; CI leest routes.json van de site, dus na #25) ·
weerbaarheid-game #5 en aanvalspaden #14 (lat). Open: de C5-controle in `repo-compliance.yml`, de referentie-implementatie van de game, en stap 9.

**Keuzes op de acht dilemma's (29-10-2026, na sparren):** C2 streng, ook voor de zeven nieuwe AI-stukken
(geen route, geen voordeur) · de weerbaarheidsgame blijft op de bestuurdersroute en haalt als eerste de lat,
binnen weken · de lat per aanraking, geen operatie; de AI-securitylijn blijft op schema · het gedeelde
dossier pas na de exports · de projectenlijst naar een aparte werkplaatspagina · vijf routes bij de start ·
de citaten van de consultants blijven letterlijk staan, geanonimiseerd · uitvoering via branch en PR.

---

## 0. Wat er al is, en waarom het niet genoeg was

Dit is het derde plan over voorpagina en werkplaats. Het [plan van 29-08-2026](2026-08-29-voorpagina-en-werkplaats.md)
maakte de site de voorpagina voor de gebruiker en GitHub de werkplaats met een afgedwongen norm. Het
[plan van 03-09-2026](2026-09-03-ontvlechting-voorpagina-en-werkplaats.md) ontvlechtte de bronbestanden:
`PROJECTEN.md` als enige lijst, `content.md` als voorpaginatekst, een visitekaart op GitHub. Het statuut zegt
het sindsdien letterlijk in B13: "de site is de etalage, GitHub de werkplaats".

Toch landt een bezoeker nog steeds in de werkplaats, en dat komt door drie dingen die die plannen niet raakten:

| Wat de bezoeker ervaart | Waardoor | Welke regel het toeliet |
|---|---|---|
| Twintig deuren in plaats van vier stations | De voorpagina heeft een keten van vier vragen, maar daaronder staat `<!-- PROJECTEN_GROEPEN -->`: alle projecten, gegroepeerd naar vorm, met repo-namen als titel | B13 eist dat elk project een pagina heeft en in de etalage staat; niets zegt dat een project ook in een route moet zitten |
| Elk tabblad begint leeg | Elk instrument heeft een eigen invoer, eigen begrippen en eigen uitvoer; niets van wat je in de zelfcheck invult komt aan in de procescheck of de beleidsset-generator | B14 definieert wat een instrument is, niet hoe instrumenten zich tot elkaar verhouden |
| Het voelt als twintig makers | Verschillende huisstijlen, wel of geen versienummer, wel of geen zichtbare tests, Engelse en Nederlandse knoppen door elkaar | B10 en B11 regelen kruimelpad en README-kop, niet uiterlijk, toon of kwaliteit van de pagina zelf |

De kennisbank heeft daarnaast een eigen breedte: vakgebieden, handleidingen, de beleidsset, de normwijzer,
de referenties. De voordeur per rol (`site/rollen.json`, sinds 28-09-2026) geeft per rol drie stukken, maar
de kennisbank-index blijft een catalogus met tellingen, geen leesroute.

## 1. Het statuut: blok C, de publicatie

Nieuw blok in `REDACTIESTATUUT.md`, vóór blok B, omdat het de eenheid van de commons verlegt van repo naar
route. Conceptteksten; vaststellen via PR op `.github` en een regel in `BESLUITEN.md` (procedure onderaan het
statuut).

**C1. De site is het product, GitHub de werkplaats.** Alles wat een lezer nodig heeft staat op
`security-commons-nl.github.io`. Een link naar github.com staat alleen waar de lezer iets moet doen dat de
site niet kan: code draaien (een script of een lokale tool), een issue of discussion openen, meebouwen.
In een leesroute komt geen repo-naam voor; een instrument heet naar wat het doet ("de zelfcheck", "de
meting"), niet naar zijn repository. Reden: wie kennis zoekt en een organisatieprofiel van een ontwikkelaar
krijgt, haakt af; de repositories zijn het hoe, niet het wat. B13 blijft bestaan en geldt voor de
werkplaats: elk project heeft een pagina, maar die pagina is pas voordeur als het project in een route zit (C2).

**C2. Elk stuk zit in een route, of het staat in de catalogus.** Een leesroute is een geordende reeks
stukken voor één rol in één situatie (bijvoorbeeld: de eerste maand als ISO bij een gemeente; een CISO die
op de Cbw voorsorteert; een privacy officer vóór een DPIA). De routes staan in `site/routes.json` en worden
gebouwd zoals de rollenblokken nu. Een stuk dat in geen enkele route past, blijft vindbaar via zoeken en de
catalogus (de kennisbank-index per vakgebied), maar staat niet op de voorpagina en niet in de voordeur per
rol. Een nieuw stuk noemt in de frontmatter zijn route(s) of expliciet `route: geen`. Reden: dit is de rem op
de breedte. De vraag "in welke route hoort dit, en op welke plek" wordt gesteld vóór het schrijven, niet erna.

**C3. Een instrument is een stap in een route, geen product in een lijst.** Een instrument staat op de
voorpagina alleen als stap in een route, met de vraag die het beantwoordt als titel. De projectentabel
(B9) blijft de bron voor de werkplaats en voor de catalogus, maar wordt niet als lijst op de voorpagina
getoond. Reden: een lezer merkt fragmentatie van software pas als hij software gebruikt; een instrument dat
als bijlage bij een handleiding komt ("lees dit, en als je het wilt meten, hier is een pagina die rekent")
is een hulpmiddel, geen product dat moet concurreren met negentien andere.

**C4. Eén publicatie, één gezicht.** Elke pagina op de site, instrument of tekst, deelt dezelfde huisstijl
(`thema.css` van de site-build), hetzelfde kruimelpad (B10), dezelfde taal (A10: Nederlands, ook knoppen en
foutmeldingen), en toont onderaan versie of peildatum (A6) en de status (B8). Reden: de commons komt van
meer dan één maker en dat mag je niet zien.

**C5. De lat voor instrumenten in een route.** Een instrument staat pas in een route als het:
- volledig in de browser rekent (B14) en offline werkt na één keer laden;
- zijn rekenregels in één referentie-implementatie heeft met tests, en de browserversie daartegen toetst
  (zoals procescheck en de CSIR-tool dat doen met `reken.py` en `app.js`);
- tests in CI heeft die groen zijn, met de badge of het aantal zichtbaar op de pagina;
- een versienummer en peildatum op de pagina toont;
- geen fouten in de browserconsole geeft en werkt op een telefoon (375 px);
- een export heeft in een open formaat (JSON of Markdown) die de gebruiker zelf bewaart, en die import
  weer inleest (geen account, geen opslag; de gebruiker is zijn eigen dossier).
Een instrument dat de lat niet haalt, draagt status `prototype` of `concept` (B8) en staat in de catalogus,
niet in een route. De lat wordt gehaald op het moment dat een instrument wordt aangeraakt, niet in één
operatie; een instrument dat niemand aanraakt, blijft prototype en dat is eerlijk. Reden: "vibe-coded" is
geen probleem van herkomst maar van toetsbaarheid; wat getest, versienummerd en uniform is, hoeft zich niet
te verdedigen.

**Aanpassingen in bestaande regels:** B9 en B13 krijgen de toevoeging "geldt voor de werkplaats en de
catalogus; de voorpagina volgt C2 en C3". B8 krijgt bij `in gebruik` de eis van C5 voor instrumenten
(`in gebruik` zonder lat kan niet meer). `repo-compliance.yml` controleert C4 en de meetbare delen van C5
(versie en peildatum op de pagina, tests in CI, huisstijl-stylesheet geladen); de rest is redactie.

## 2. De voorpagina en de kennisbank-index

1. `content.md`: de keten van vier vragen blijft en wordt de hoofdstructuur. "Alle projecten" en
   "Onderliggende infrastructuur" gaan van de voorpagina naar een pagina `/werkplaats/` die de projectentabel
   toont met status, en vandaaruit naar GitHub. De voorpagina linkt één keer naar de werkplaats, onderaan,
   onder "Meedoen".
2. De voordeur per rol (`rollen.json`) wordt de kop van een leesroute per rol (`routes.json`): niet drie
   stukken, maar de hele route met een volgorde en per stap één zin waarom dit nu. De eerste vier routes zijn
   de bestaande rollen: CISO, ISO, privacy officer, bestuurder. De vijfde is de route die het meest wordt
   gemist en die de kennisbank al bijna heeft: "de eerste honderd dagen" (open stap in het
   [plan van 28-09-2026](2026-09-28-ingang-en-vulling.md)).
3. De kennisbank-index per vakgebied blijft de catalogus, maar krijgt bovenaan de routes die door dat
   vakgebied lopen, en per stuk de route-vermelding uit de frontmatter. De tellingen per vakgebied gaan weg
   van de voorpagina; een lezer heeft niets aan "negen stukken privacy".
4. Zoeken blijft zoals het is: de catalogus is voor wie weet wat hij zoekt, de route voor wie dat niet weet.

## 3. De instrumenten langs de lat

Gemeten op 29-10-2026, avond: de repo's in de werkmap (testbestanden, CI-workflows, referentie-implementatie,
export en import in de code) en de live pagina's met een headless browser (laden op 375 px en 1280 px,
consolefouten, versie of peildatum in de tekst, `thema.css` of een topbalk geladen, kruimelpad, tests of status
zichtbaar). Het script staat niet in een repo; het is een eenmalige meting en de kolommen zijn de lat van C5.
"Op de pagina" betekent zichtbaar voor de lezer, niet aanwezig in de repo.

| Instrument | Status (B8) | Testbestanden | CI | Referentie-implementatie | Export / import | Versie of peildatum op de pagina | 375 px zonder scroll | Consolefouten | Thema of topbalk | Kruimelpad | Tests zichtbaar | In een route (na PR 25) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| zelfcheck (aanvalspaden) | prototype | 15 | ja | ja, `tools/score.py` gespiegeld in `check/bron/app.js` (correctie: eerder "geen" genoteerd) | ja / ja | ja sinds PR 29-10 (eerder alleen de bronversie) | ja | geen | nee | ja | ja sinds PR 29-10 | ja, stap 1 in drie routes |
| meting (aanvalspaden/meting) | prototype | (zelfde repo) | ja | ja, `meting/reken.py` en `bron/app.js` | ja / ja | ja | ja | geen | nee | ja | nee | ja, CISO en ISO |
| normwijzer (normen) | in gebruik | 3 | ja | n.v.t. (naslag met zoekvak) | nee / nee | nee | ja | geen | ja | ja | nee | ja, drie routes |
| procescheck | prototype | 8 | ja | ja, `reken.py` en `bron/app.js` | ja / ja (JSON) | ja | ja | geen | nee | ja | nee | ja, ISO stap 3 |
| csir-assessment-tool | prototype | 4 | ja | ja, `reken.py` en `bron/app.js` | ja / ja | nee (wel de versie van de richtlijn) | ja | geen | ja | ja | nee | nee |
| beleidsset-generator (kennisbank) | in gebruik | 7 (kennisbank) | ja | ja, py en js gespiegeld | ja (md, docx) / ja | nee | ja | geen | nee | ja | nee | ja, ISO en eerste honderd dagen |
| weerbaarheid-game | in gebruik | 1 (+1 sinds PR 29-10) | ja | nee | ja / ja sinds PR 29-10 | ja sinds PR 29-10 | ja | geen | nee | ja sinds PR 29-10 | ja sinds PR 29-10 | ja, bestuurder stap 2 |
| anonimizer-browser | in gebruik | 5 | ja | n.v.t. | n.v.t. / bestand inlezen | nee | ja | geen | nee | ja | nee | ja, privacy officer |
| publicatiescan (script, leesversie) | in gebruik | 22 | ja | n.v.t. | n.v.t. | nee | ja | geen | nee | ja | ja | ja, privacy officer |
| applicatiecheck (ontwerp) | concept | 1 | ja | nee | nee | ja (peildatum) | ja | geen | nee | ja | nee | nee |
| policy-as-code (ontwerp) | concept | 0 | ja | nee | nee | ja | ja | geen | nee | ja | nee | nee |

Wat de meting zegt, tegenover het beeld "op het oog" van eerder op de dag:
- **Geen enkel instrument toont zijn tests op de pagina**, en maar drie tonen een versie of peildatum. De lat is
  op dat punt voor iedereen nieuw; dat is de eerste klus bij elke aanraking.
- **Alle twaalf pagina's laden schoon**: geen consolefouten, geen horizontale scroll op 375 px. Het "zooitje"
  zit niet in kapotte pagina's maar in samenhang en uniformiteit.
- **De weerbaarheidsgame mist het kruimelpad** (B10, al verplicht) naast alles van C5 behalve het laden. Hij
  staat op de bestuurdersroute (keuze 29-10) en is daarmee de eerste aanraking: kruimelpad, versie, tests,
  export van de ingevulde stand.
- **De zelfcheck heeft export, import én een referentie-implementatie** (`tools/score.py`; de eerste meting had
  dat gemist). Wat ontbrak was zichtbaarheid: versie van de app, status, tests. Gedaan in de PR van 29-10.
- Procescheck, CSIR-tool en meting halen de lat op de bouw (referentie, export, import) en missen alleen de
  zichtbaarheid (versie, tests). Dat is per instrument een klein werk.
- De thema-detectie (`thema.css` of een topbalk) vond maar twee pagina's; de kennisbank gebruikt sinds 15-10 een
  eigen huisstijlbron (`huisstijl.py` en `base.css`). Of dat hetzelfde gezicht is, is een redactionele toets
  met het oog, geen regex; C4 vraagt die toets bij elke aanraking.

Volgorde van aanraken, naar waar een route hem nodig heeft en wat de meting zegt: weerbaarheidsgame ·
zelfcheck · beleidsset-generator (versie en tests zichtbaar) · procescheck, CSIR-tool en meting (idem) · de
rest op het moment dat iemand ze aanraakt. Statuslabels: de game en de normwijzer heten `in gebruik` zonder de
lat; volgens B8 zoals aangevuld zijn ze prototype tot ze hem halen. Bas koos op 29-10 de game op de route te
laten staan met een korte termijn; de normwijzer is naslag en valt onder B14 niet als instrument, dus de lat
geldt daar alleen voor versie en peildatum. Beide labels blijven staan tot de eerste aanraking; daarna geldt
de regel zonder uitzondering.

**De munt (nog geen besluit).** Zodra drie instrumenten een JSON-export hebben (procescheck heeft hem, de
zelfcheck en de beleidsset-generator volgen uit C5), wordt zichtbaar waar een gebruiker nu met de hand
overtikt: processen uit de procescheck in de contextvragen van de beleidsset, barrières uit de zelfcheck in
de normwijzer. Dan is een gedeeld schema (`mijn-organisatie.json`: één lokaal bestand dat elk instrument
inleest en aanvult) de logische volgende stap: de munt én de tas van de markt, zonder platform. Dat is een
eigen plan, pas te schrijven als de exports er zijn; nu vastleggen zou bouwen op aannames.

Aanvulling van de initiatiefnemer (29-10-2026, 's avonds, als idee om later over te sparren): een
**extractielaag** die zonder inlog, via een assistent, de organisatie uitvraagt (processen, applicaties,
leveranciers, barrières, contextvragen) en daarmee elk afzonderlijk instrument vult. Dat is de munt met een
intake ervoor: het dossier `mijn-organisatie.json` is de uitkomst van het gesprek, en elk instrument leest
het in plaats van opnieuw te vragen. Past bij de AI-hulp met eigen sleutel (opt-in, voorstel in plaats van
wijziging) en bij B14 (geen account, geen opslag). Nog niet uitgewerkt; hoort bij stap 9.

## 4. Stappen

| # | Stap | Wat het oplevert | Controle | Wie |
|---|---|---|---|---|
| 1 | Statuut: blok C1 tot en met C5 en de aanpassingen aan B8, B9, B13; regel in `BESLUITEN.md` | De eenheid is de route, niet de repo | PR op `.github` gemerged; `repo-compliance.yml` bijgewerkt in dezelfde PR (procedure statuut) | redactie · **in PR 29-10**; de compliance-controle volgt als de meetbare delen van C5 zijn uitgewerkt |
| 2 | Voorpagina: projectenlijst en infrastructuur naar `/werkplaats/`, tellingen weg, één link naar de werkplaats onderaan | Vier stations, geen twintig deuren | `test_voorpagina.py` aangepast: geen repo-naam en geen github.com-link boven "Meedoen"; linkcheck groen | bouwer · **in PR 29-10** (site #25; de tellingen per vakgebied staan in de kennisbank-index, stap 5) |
| 3 | Lat toetsen: per instrument in de tabel van §3 de zes punten van C5 nalopen en de kolommen invullen | Een eerlijke stand per instrument, geen "op het oog" | tabel in dit plan bijgewerkt; afwijkende statuslabels in `PROJECTEN.md` gecorrigeerd | bouwer · **gemeten 29-10** (tabel in §3); statuslabels blijven tot de eerste aanraking |
| 4 | Routes: `routes.json` met vijf routes (CISO, ISO, privacy officer, bestuurder, eerste honderd dagen), per stap één zin waarom; `rollen.json` gaat erin op; frontmatter-veld `route` in de kennisbank | De leesroute per rol | elk adres in de routes bestaat (linkcheck); elk stuk in de kennisbank heeft `route:` gevuld of `geen` (build faalt anders) | redactie · **routes in PR 29-10** (site #25, 34 stappen, elk adres 200); het frontmatter-veld `route` in de kennisbank is gevuld voor alle 83 items met controle in twee richtingen (kennisbank-PR 29-10) |
| 5 | Kennisbank-index: routes bovenaan per vakgebied, route-vermelding per stuk | De catalogus wijst naar de routes | `build.py`-test op aanwezigheid | bouwer · **in kennisbank-PR 29-10** (blok "Routes door dit vakgebied" op elke vakgebiedpagina, etiket "route: ISO stap 3" op de kaart) |
| 6 | Zelfcheck langs de lat: referentie-implementatie met tests, JSON-export en -import, versie en peildatum op de pagina | Stap 1 van de keten haalt de lat | tests groen in CI; export-import rondgang als test | bouwer · **in PR 29-10** (aanvalspaden: versie, status en tests in de voet; referentie en export waren er al) |
| 7 | Weerbaarheidsgame langs de lat, of terug naar `prototype` en van de bestuurdersroute af tot hij de lat haalt | Geen instrument op de voordeur zonder lat | idem | bouwer · **in PR 29-10** (weerbaarheid-game#5: kruimelpad, versie, status, tests, stand opslaan en laden met rondgangtest); open: referentie-implementatie van de rekenregels |
| 8 | Procescheck en beleidsset-generator in de ISO-route en de eerste-honderd-dagen-route | De sterkste instrumenten staan waar ze horen | routes-linkcheck | redactie · **in PR 29-10** (site #25: ISO stap 3 en 4, eerste honderd dagen stap 6) |
| 9 | Plan "de munt": gedeeld schema, pas na stap 6 | Besluit op feiten over waar overgetikt wordt | apart plan | redactie |

Stap 1 en 2 zijn één avond en meteen zichtbaar. Stap 3 en 4 zijn schrijfwerk en lopen naast de
[AI-securitylijn](2026-10-15-ai-securitylijn.md) (dezelfde soort werk, dezelfde deadline van 1 december voor
wat de initiatiefnemer zelf moet doen). Stap 5 tot en met 8 zijn lopend en hebben geen einddatum; de lat
geldt per aanraking. Stap 9 is bewust uitgesteld.

## 5. Wat dit plan niet doet

- Het zegt niet dat de software slecht is. Het zegt dat software die in een route staat toetsbaar moet
  zijn, en dat software die dat niet is, eerlijk `prototype` heet.
- Het bouwt geen platform en geen gedeeld dossier. Het maakt de voorwaarde daarvoor (exports) tot onderdeel
  van de lat, zodat het volgende plan op feiten kan bouwen.
- Het herschrijft de kennisbank niet. Het hangt een route-veld aan elk stuk en laat de stukken die nergens
  passen in de catalogus staan. Of die stukken daar blijven, is een vraag voor de portfolio-review van
  volgend jaar, niet voor nu.
- Het verwijdert niets van GitHub. De werkplaats blijft volledig; hij staat alleen niet meer in de etalage.
