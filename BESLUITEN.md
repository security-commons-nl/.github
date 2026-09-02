# Besluiten van de organisatie

Append-only. Elke wijziging aan het [redactiestatuut](REDACTIESTATUUT.md) of aan de opzet van de commons
krijgt hier een regel: datum, wat er is besloten, en waarom. Nieuwste bovenaan. Besluiten die alleen over
één repo gaan, staan in die repo.

Dit log begint op 29-08-2026, toen bleek dat het statuut er wel naar verwees maar het nergens stond.

## 03-09-2026 · procescheck is een instrument; blast-radius is erin opgegaan en gearchiveerd

**Besloten.** `procescheck` rekent sinds vandaag in de browser: de BIA en BIV-classificatie, de
continuiteitsparameters, de businesscontext en de blast radius in een pagina van 116 kB, met het dossier
als JSON-bestand op het apparaat van de gebruiker. De applicatievorm (React, FastAPI, PostgreSQL, Azure AD)
is van `main` af en staat op tag `v0-applicatie`, waar het instrument zijn vragen en rekenregels ook
vandaan haalt. `blast-radius` is opgegaan in de tab *Blast radius* en op GitHub gearchiveerd; kloon plus
bundle staan in `X:\ARCHIEFlast-radius*`.

**Waarom.** Uitvoering van fase 4 en 6 van het plan *lichte commons* en van B14: wat procescheck een
applicatie maakte was hosting, geen inhoud. Een database, een account en een beheerder stonden tussen de
gebruiker en een formulier met zes vragen. De inhoud zelf is niet aangeraakt: de zes vragen, de dertig
antwoordteksten, de vijf klassen en de tien volledigheidscontroles zijn woordelijk uit de code op de tag
gehaald door `instrument/haal_bron.py`, en een test legt ze daar telkens weer naast.

**Twee bewuste afwijkingen**, allebei in `verantwoording.md`: het gedachtestreepje in een redentekst werd
een komma, en de lichtste prioriteit heet `low` in plaats van `medium`, zodat de prioriteit gelijkloopt met
de volledigheidsbanden die de applicatie zelf al hanteerde.

**Wat vervalt.** Inloggen, de auditlog, de exportserver voor xlsx/docx/pptx en de Docker-omgeving. De
auditlog bestond omdat meerdere mensen in dezelfde database werkten; een dossier op je eigen schijf heeft
git of een gedateerde kopie als audit trail.

## 02-09-2026 · Scanners zijn geen projecten: posture-tool en iamscan gaan op in meting, blast-radius in procescheck

**Besloten.** `security-posture-tool` en `iamscan` gaan op in `aanvalspaden/meting/` (diepte 2 van de keten);
`blast-radius` gaat op in `procescheck`. Geen browserversies naast de CLI's, zoals het plan *lichte commons*
eerst zei, en geen samenvoeging onder `applicatiecheck`. De repo's blijven staan tot hun opvolger live is en
worden dan gearchiveerd. `applicatiecheck` blijft een eigen instrument (eenheid: één applicatie) en is de
referentie-implementatie van de bewijs-vorm die meting overneemt.

**Waarom.** Vier repo's lazen ieder een export, toetsten die deterministisch en schreven een rapport; de
posture-tool had daar een eigen motor voor ontworpen (observation, finding, rule engine, zeven lagen) die
applicatiecheck nu voor een tweede keer aan het bouwen was. Eén vorm, gedocumenteerd in `ARCHITECTUUR.md`,
en per eenheid één instrument: landschap (meting), applicatie (applicatiecheck), proces (procescheck), object
(CSIR). Een scanner die één vraag op één export beantwoordt is in die indeling een bron plus regelset, geen
project. De scope overlapt niet (nagekeken: applicatiecheck zegt zelf "eenheid is één applicatie, niet het
landschap"), de machinerie wel; daar zat het duplicaat.

**Afgewezen.** Alles onder applicatiecheck hangen: dat maakt van een applicatie-instrument een
landschapsinstrument en breekt zijn eigen afbakening. Losse browserversies per scanner: dan is de motor
alsnog vier keer gebouwd, alleen client-side.

## 02-09-2026 · BIO 2.0 in `normen`: alleen nummers, titels en thema's; geen tekst van het CIP

**Besloten.** De tekst van de overheidsmaatregelen en het risico uit de BIO 2.0-publicatie gaan niet mee in
`normen/bio2.json`. Wat blijft: nummer, titel en thema. Dit corrigeert het besluit van eerder vandaag, dat de
tekst van de overheidsmaatregel en het risico als "open" liet staan.

**Waarom.** Het CIP publiceert onder CC BY-NC-SA 4.0. Niet-commercieel en share-alike zijn niet te verenigen
met herdistributie onder EUPL-1.2, en de commons publiceert voor iedereen, ook voor wie er een dienst omheen
bouwt. Dezelfde regel als voor de ISO-tekst, om dezelfde reden: het nummer is van iedereen, de tekst niet. De
aanvalspaden werkten al zo; `normen` volgt nu, en `applicatiecheck` moet volgen (issue `applicatiecheck#2`).

## 02-09-2026 · De normbronnen krijgen een eigen dataset-repo `normen`

**Besloten.** BIO 2.0, NIST CSF 2.0, het Wpg-toetsingskader en de AVG (nu in `aanvalspaden/mappingen/bronnen/`,
met `cisochat/data/bio2.json` als bron) verhuizen naar een eigen repo `normen`, type dataset, in de
projectentabel met een leesbare versie. De mappingen (welke barriere levert bewijs voor welke maatregel)
blijven bij de aanvalspaden. Afnemers (aanvalspaden, applicatiecheck, policy-as-code, later de CSIR-tool)
kopieren met een vingerafdruk, zoals de bestaande harde koppelingen. Het veld `iso_maatregel` met de
woordelijke ISO 27002-tekst gaat er bij de verhuizing uit; de crosswalk gebruikt alleen de BIO-nummering en
de overheidsmaatregel.

**Waarom.** Eén dataset met vier afnemers hoort niet onder een van die vier. Het crosswalk-plan van 30-08
noemde een gedeelde kaders-repo al als vervolgbesluit. En als centrale dataset is herdistributie van
ISO-tekst een ander verhaal dan als data bij een concept; BIO 2.0 is open, ISO niet.

## 02-09-2026 · De commons levert instrumenten en scripts, geen applicaties meer

**Besloten.** Een project in de projectentabel is een instrument (rekent volledig in de browser, zonder
server, account of telemetrie) of een script (draait lokaal op data die je al hebt, zonder server en zonder
eigen opslag). Applicaties met een backend, database, authenticatie of gedeelde staat horen niet meer in de
commons. `grc-platform` neemt afscheid en wordt gearchiveerd; de lokale kopie met volledige historie blijft
bewaard. `procescheck`, `security-posture-tool`, `blast-radius` en `iamscan` worden omgebouwd naar de vorm
van de zelfcheck en de CSIR Assessment Tool. `cisochat` en `hosting-bouwblokken` volgen na een oogst van
wat er aan kennis in zit. `anonimizer-proxy` is de enige uitzondering, opt-in en met naam. Het plan staat
in [plannen/2026-09-02-lichte-commons.md](plannen/2026-09-02-lichte-commons.md); statuut B14 volgt via de
wijzigingsprocedure.

**Waarom.** Alles wat de afgelopen week live ging is client-side; alles met een backend staat op prototype of
concept en loopt vast op hosting (de IMS-pilot geparkeerd op de hostingdrempel, het codeplatform zonder
CI/CD). Een tool die een DPIA, inkoop en een beheerder vraagt voordat iemand hem kan proberen, haalt precies
de drempel niet weg waarvoor de commons bestaat. Het register hoort daarmee bij de gebruiker: elk instrument
levert een dossier als JSON dat hij meeneemt naar zijn eigen managementsysteem.

**Afgewezen.** "Client-side als norm met gemotiveerde uitzonderingen": dat had grc-platform een uitzondering
gemaakt en de norm meteen zacht. De keuze is hard, met één benoemde uitzondering voor infrastructuur.

## 02-09-2026 · B13: elk project heeft een pagina op het domein

Elke repo in de projectentabel krijgt een pagina op `security-commons-nl.github.io/<naam>/`, ongeacht
status; minimaal de leesversie van de README via de gedeelde site-build. De kolom *Direct openen* krijgt
er een derde label bij, *Ontwerp*, naast *Live tool* en *Leesbare versie*. Vastgelegd als **B13** in het
redactiestatuut; de uitrol staat in [het plan](plannen/2026-09-02-elk-project-een-pagina.md).

**Aanleiding.** Bij het aanmaken van `applicatiecheck` (concept) bleek dat tien van de zestien projecten
in de tabel niet op het domein staan. Wie via de voorpagina binnenkomt, komt bij die tien op GitHub
terecht of nergens; een concept bestond voor de meeste lezers niet.

**Onderbouwing.** De site is de etalage, GitHub de werkplaats. De infra ligt er al: de herbruikbare
workflow `pages-docs.yml` en een `site/config.json` per repo, dus de kosten per repo zijn een workflow van
drie regels en een config. Voorwaarde is dat de site-build op één plek gaat wonen; hij wordt nu per repo
gekopieerd en `applicatiecheck` is de derde kopie met een eigen afwijking. Een kopie zonder bewaking wordt
binnen een half jaar een tweede waarheid, dus het centraliseren is onderdeel van dezelfde uitrol. De
statuutcontrole op B13 gaat pas aan als de tien repo's om zijn, zodat de regel niet begint met tien rode
runs.

## 31-08-2026 · A11 aangescherpt: een vraag beschrijft het vraagstuk, nooit de eigen zwakte

Toevoeging aan A11: een vraag staat op sectorniveau en beschrijft nooit de situatie van een organisatie,
ook niet die van de vragensteller zelf. Formuleringen als "wij hebben dit nog niet opgelost" of "daar
hebben we weinig van" horen er niet in, en een lezer wordt ook niet uitgenodigd om zijn eigen gaten te
benoemen.

**Aanleiding.** Bij het openen van de discussielijst met acht startvragen stond dit in vier ervan wel zo.
Een vraag over telefonie-uitval meldde dat het nog niet opgelost was, een vraag over publicatiecontrole
dat er aan de voorkant weinig lag, en de aankondiging nodigde lezers uit om te antwoorden met "wij hebben
het ook niet geregeld". Dat is precies het tegenovergestelde van wat een commons hoort te doen: het maakt
van een uitnodiging tot delen een inventarisatie van zwakke plekken, doorzoekbaar en permanent.

**Onderbouwing.** De drempel om te vragen is in dit vakgebied de kern van het probleem, en A11 haalde die
al weg door een schuilnaam toe te staan. Maar anonimiteit van de vrager helpt niet als de vraag zelf de
zwakte beschrijft; bij een klein aantal organisaties met hetzelfde profiel is dat alsnog herleidbaar. De
regel moet dus over de inhoud gaan, niet alleen over de naam eronder. Alle negen bestaande posts zijn
herschreven voordat deze regel is vastgelegd.

## 31-08-2026 · Halen en brengen: vragen stellen wordt een eigen soort werk, onder eigen naam of schuilnaam

De commons publiceerde tot nu toe alleen wat we weten. Daar komt bij wat we zoeken. Dat is vastgelegd als
**A11** in het redactiestatuut, als derde soort werk in [ARCHITECTUUR.md](ARCHITECTUUR.md) naast Sprong en
Gat, en op het organisatieprofiel is de sectie *Meedoen* verbreed tot **Halen en brengen**. Vragen leven in
Discussions op deze repo, in vier categorieen: hulpvraag uit de praktijk, gevraagd wie deelt dit, werkt dit
bij jou, en aankondigingen.

**Onderbouwing.** Een kenniscommons die alleen zendt, groeit alleen zo hard als zijn oprichters. De
schaarste zit niet in plekken om te praten: in de publieke sector zijn er gremia genoeg. De schaarste zit
in plekken waar de neerslag blijft staan, en dat is precies wat de kennisbank is. Door de vraag en het
antwoord aan elkaar te knopen wordt een gesprek een stuk, in plaats van een verslag dat niemand terugleest.

**De kern is de drempel, niet de plek.** In dit vakgebied is een hulpvraag ook een zwakteverklaring: wie
vraagt hoe je een sleutelbesluitprocedure opzet, zegt daarmee dat hij die niet heeft. Dat is de reden dat
vakfora hier leeglopen, en het is met een categorie niet op te lossen. Daarom staat in A11 expliciet dat
een schuilnaam mag en dat de organisatie van de vrager nooit wordt genoemd. Dat is dezelfde redenering als
A1 voor gedeelde stukken ("wie deelt, hoeft daar zijn naam niet aan te verbinden"), nu doorgetrokken naar
wie vraagt.

**Bewust niet gekozen: een tussenpersoon.** Overwogen is dat een maintainer vragen namens anderen zou
plaatsen, zodat ook de vrager onzichtbaar blijft voor iedereen behalve die maintainer. Dat is afgewezen:
het maakt de maintainer een flessenhals, het vertraagt, en het verplaatst het vertrouwensprobleem in plaats
van het op te lossen. Er zijn nu drie routes en de vrager kiest zelf: eigen naam, schuilnaam, of later een
formulier op de site dat zonder account post. Dat formulier is nog niet gebouwd; het vraagt een eigen
botidentiteit (een token van een persoonlijk account zou elke anonieme vraag op diens naam zetten),
snelheidsbegrenzing tegen misbruik, en een afspraak over opruimen achteraf.

**Wat hierbij hoort.** Een vraag draagt een status en een peildatum. Een beantwoorde vraag blijft staan en
wijst naar het stuk dat eruit voortkwam; een vraag die een jaar open staat wordt herschreven of gaat weg.
Liever vier scherpe vragen dan twintig vage: een pagina met onbeantwoorde vragen leest als een dood project
en straalt af op de rest.

## 31-08-2026 · Casus *Meten voordat je ingrijpt*: toestemming rond, en de game is generiek gemaakt

**A4 afgerond.** Het materiaal dat op 29-08 als casus is ingebracht, stond sindsdien met een open
toestemmingspunt in de kennisbank. De eigenaar heeft dat op 31-08 afgerond. Een sweep over de zeven items
die de casus als herkomst dragen, laat niets herleidbaars zien: geen organisatienamen, geen personen,
geen e-mailadressen, geen interne documenten, en de herkomstregel noemt alleen "een gemeentelijke
organisatie" (statuut A3). Het punt is daarmee dicht.

**De weerbaarheidsgame is generiek gemaakt.** Daar zat wel herleidbaar materiaal, en dat was tot nu toe
niemand opgevallen omdat de game buiten de kennisbank valt en dus niet door `build.py` wordt gecontroleerd:
op vijf plekken de naam van een intern programma met de naam van een medewerker erbij (A1 en A2), een
verstreken presentatiedatum (A6), en in de begeleidende beschrijving vier interne documenten met hun
bestandsnaam (A9). Alles is vervangen door generieke formuleringen zonder datum: "een
weerbaarheidsprogramma", "de eigen continuiteitsrapportage", "de CISO presenteert".

Daaruit volgt een les over de reikwijdte van het statuut: het geldt voor alles wat de commons publiceert,
maar het wordt alleen machinaal gecontroleerd in de kennisbank. Repo's met een eigen HTML-product vallen
buiten die controle, en daar is dit blijven staan. Wie zo'n product inbrengt, doet de sweep met de hand.

**Handelingsperspectief is verwijderd** (31-08, door de eigenaar), waarmee het besluit van 30-08 is
uitgevoerd. De laatste verwijzingen ernaar zijn opgeruimd: de vermelding in de gearchiveerd-alinea van het
profiel en een dode link in de changelog van `ai-gebruik-in-beeld`. De lokale kloon blijft voorlopig staan;
die is nu de enige kopie van de git-historie.

## 31-08-2026 · Een stuk bevat een soort materiaal, en een pijler toont wat eronder hangt

*Meten voordat je ingrijpt* was 33.000 tekens en zestien hoofdstukken, en bevatte vier soorten materiaal
tegelijk: een methode, een bestuursverhaal, twee technische handleidingen en naslag. Wie het opende moest
zelf uitzoeken welk deel voor hem was. Dat er een tabel *Wat je hier vindt* nodig was om dat op te lossen,
was het bewijs van het probleem en niet de oplossing ervan.

Het is opgesplitst naar wat het is: de methode blijft onder de oude naam (10.500 tekens), het
bestuursverhaal wordt *Sturen op weerbaarheid* voor bestuur en directie, en de twee technische
hoofdstukken worden handleidingen bij hun barriere (`segment` en `edr`/`execution`). De regel die daaruit
volgt: een stuk bevat een soort materiaal en zegt in zijn `type` welk soort dat is. Bevat het er meer,
dan splits je.

Tegelijk is het veld `pijler` zichtbaar geworden. Het bestond al en werd door `build.py` gecontroleerd,
maar werd nergens getoond: twee handleidingen droegen het en geen enkele lezer kwam het verband ooit
tegen. Een veld dat alleen gecontroleerd wordt en nooit getoond, is administratie. Nu toont een pijler
welke stukken eronder hangen, en toont een stuk bij welke pijler het hoort.

Dat mechanisme is meteen toegepast op de SOC-cluster: `centrale-logverzameling` is de pijler van de vier
routes eronder, en heeft een vergelijkingstabel gekregen. Wie moest kiezen kreeg daarvoor alleen een
lijstje met vier links en moest vier pagina's naast elkaar leggen. Bewust geen apart keuzewijzer-item: dat
zou het probleem herhalen dat hierboven is opgelost.

## 30-08-2026 · De security-shop gaat op in de kennisbank

De catalogus deelde zijn patronen in naar ZTMM-pijler, terwijl de rest van de keten aan de barrieres uit
`paden.json` hangt. Twee taxonomieen over hetzelfde onderwerp betekent dat de lezer zelf moet vertalen,
en dat een verbetering op twee plekken bijgehouden moet worden. De shop had bovendien geen tests en geen
bijdragen buiten de mockup.

Tegelijk was de inhoud precies wat er ontbrak: 24 van de 30 barrieres zonder handelingsperspectief
hadden er al een patroon. Daarom is de catalogus niet weggegooid maar verhuisd: dertig patronen zijn
herschreven tot handleidingen in de kennisbank, gekoppeld aan hun barriere, met een kop Bewijs erbij.
Wat geen barriere raakte, staat als idee in de issues van de kennisbank. De repo is gearchiveerd en zijn
README verwijst door.

Gevolg voor het statuut: de regel `security-shop | ZTMM-pillar of cross-cutting capability` is uit de
B1-tabel gehaald, en het veld `barrieres:` mag voortaan ook bij een item van type `aanpak` of `sjabloon`
staan. De passkeys-aanpak en de Security Annex richten net zo goed een maatregel in; alleen de vorm
verschilt, en het `type` blijft zeggen wat de lezer krijgt.

## 30-08-2026 · De kennisbank is de bron van het handelingsperspectief

De koppeling barriere naar handleiding werd in `aanvalspaden/mappingen/` met de hand bijgehouden. Die
lijst liep per definitie achter zodra de kennisbank een artikel toevoegde, precies het probleem dat de
normverankering voor de normenkaders al had opgelost.

De koppeling staat nu in de frontmatter van het kennisbank-item zelf (`barrieres:` en `rol:`).
`kennisbank/tools/build.py` exporteert hem, `aanvalspaden/tools/haal_handelingsperspectief.py` kopieert
hem met een sha256 eronder, en CI vergelijkt. Een verlopen kopie valt om in plaats van stilletjes een
verkeerde handleiding te beloven.

`gevraagd.json` blijft handwerk en blijft in aanvalspaden: wat een nog ongeschreven handleiding zou
moeten dekken, weet de kennisbank niet.

## 30-08-2026 · De volgorde van kennisbankitems is redactioneel (B4 aangevuld)

De overzichtspagina's sorteerden op mapnaam. Daardoor stond de awareness-sessie bovenaan omdat die met
een a begint, boven de Annex en de risicoanalyse. Het alfabet is geen oordeel.

Besloten: de volgorde staat als genummerde lijst onder `## Volgorde` in de README van de sectie, en
`tools/build.py` volgt die. Zelfde mechanisme als de projectentabel op de org-pagina (B9): één zichtbare
bron, te bespreken in een pull request. Een item dat in de lijst ontbreekt of een naam die niet bestaat
blokkeert de build, zodat een nieuw stuk niet stil onderaan belandt.

Twee alternatieven afgevallen. Een rangnummer in de frontmatter kan niet zonder B2 te wijzigen (gesloten
set van acht velden) en nodigt uit tot drift. Sorteren op statuslabel meet rijpheid, niet waarde, en kan
niet uitdrukken welk stuk het vlaggenschip is.

## 30-08-2026 · procescheck gaat naar EUPL-1.2; geen uitzondering in B5

Eén repo stond rood op de statuutcontrole: GPL v3, terwijl B5 EUPL-1.2 eist. Het auteursrecht ligt bij de
oorspronkelijke auteur, dus herlicentiëren was nooit een keuze van deze organisatie. Een eerdere poging om
het stil recht te zetten is daarom teruggedraaid.

De vraag is voorgelegd met de overweging erbij. EUPL-werk mag opgaan in een GPL-geheel, andersom niet.
Voegen we procescheck en `grc-platform` samen, dan wordt dat geheel dus GPL v3. De licentievraag en de
fusievraag zijn daarmee één vraag, en dat maakte het een keuze en geen formaliteit.

De auteur heeft de licentie zelf omgezet naar EUPL-1.2 en tegelijk een nieuwe versie gepubliceerd. De
statuutcontrole is groen. De overwogen uitzondering bij B5 komt er dus niet, en dat is winst: B5 blijft
absoluut (EUPL-1.2 voor alles), en een afwijkende licentie blijft een gesprek met de rechthebbende in
plaats van een uitzonderingsregel die de controle stiller maakt.

**Wat dit opent:** een samenvoeging met `grc-platform` kan nu zonder dat het geheel naar GPL kantelt. Die
afweging zelf staat nog open.

## 29-08-2026 · Een itempagina wijst naar zijn eigen bestanden (B3 en B10 aangevuld)

Aanleiding: de pagina van de awareness-sessie beschrijft een presentatie van veertig minuten en linkt hem
nergens. Het bestand staat er wel en is bereikbaar, maar alleen als je de URL zelf typt.

Twee oorzaken. De leesversies zijn gerenderde README's en misten de voetregel die de gegenereerde
overzichtspagina's wel hebben, dus vanaf een itempagina was er geen enkele route naar de bron: negen van
de elf pagina's kwamen niet verder dan het kruimelpad. En een bijlage die in de README als opmaakcode
staat in plaats van als link, verdwijnt op de site uit beeld.

Besloten: B3 eist voortaan dat wat in de map staat als link in de README én op de leesversie staat, en dat
verwijzingen bestaan en binnen de eigen repo blijven. B10 eist een bronvoet onder elke leesversie.
`tools/build.py` zet die voet, controleert de rest en blokkeert; `tools/test_build.py` test de controles.

Wat de nieuwe controle meteen vond: de presentatie en twee datasets stonden nergens als link, de
handleiding voor het blue team wees nog naar een bestandsnaam die na de B3-opruiming index.html heet, het
AI-beleid verwees een niveau te hoog waardoor licentie en kennisbank-link op de site doodliepen, en de
markdown-bron van de Annex en van het AI-beleid was vanaf hun eigen pagina niet te vinden.

**Wat hierbij opviel en niet is opgelost:** de leesversies komen uit drie verschillende renders (twee
sjablonen en een handgemaakte pagina) en er is geen script dat ze opnieuw maakt. Daardoor kan een
bijgewerkte README stil uit de pas lopen met de pagina, precies zoals bij het blue team gebeurde. Een
render-stap in `build.py` zou dat sluiten; dat is een eigen klus en een eigen besluit.

## 29-08-2026 · Handelingsperspectief wordt het kennisbankitem "Meten voordat je ingrijpt"

Het was het enige kennisstuk met een eigen repo en een eigen site-generator. Alle andere kennis staat in de
kennisbank en krijgt daar frontmatter met acht velden, een peildatum, een statuslabel, de statuutcontrole,
de anonimizer-scan, een kruimelpad en een leesversie; dit stuk had niets daarvan. Omvang was geen argument:
met 5.400 woorden is het kleiner dan twee bestaande items.

Ook de naam is mee verhuisd. "Handelingsperspectief" is standaardtaal in beleidsstukken en NCSC-adviezen,
zegt niets over het onderwerp en kwam in de tekst zelf geen enkele keer voor. De andere kennisbankstukken
heten naar wat je gaat doen (Passkeys invoeren, Een blue team opzetten); "Meten voordat je ingrijpt" is de
eerste zin van de methode zelf en past in dat rijtje.

De acht hoofdstukken zijn een document geworden met een leeswijzer bovenaan; de zes KQL-query's staan als
bijlagen in `data/`. De oude repo is een doorverwijzing en daarna gearchiveerd, zodat gedeelde links en de
Pages-URL blijven werken.

**Wat bewust niet is samengevoegd:** de killchain-tabel bleef staan. Die volgt de volledige keten met alle
MITRE-fasen en is een andere snit dan AP09 in `paden.json`, dat vier barrieres toetst. In plaats van
verwijderen staat er nu een expliciete uitleg bij hoe de twee zich verhouden.

**Nog te doen:** de inbrenger van de casus moet nog worden bijgepraat over de verhuizing en de naam.
Statuut A4 gaat over publiceren en het stuk stond al gepubliceerd, dus dit hield de verhuizing niet tegen,
maar het gesprek hoort er wel bij.

## 29-08-2026 · dreigingsanalyse is geen repo van de organisatie

Bij de uitrol van de README-norm bleek dat `dreigingsanalyse` geen remote heeft en niet op GitHub staat:
het is een lokale map waarvan de inhoud is opgegaan in het kennisbankitem Risicoanalyse langs
aanvalspaden. Hij is daarom uit het profiel gehaald (de verwijzing gaf een 404 op de voorpagina), telt
niet mee in de statuutcontrole en hoeft niet gearchiveerd te worden.

**Waarom dit telt:** het profiel is de enige projectenlijst (B9). Wat daar staat, moet bestaan.

## 29-08-2026 · De voorpagina is voor de gebruiker; de werkplaats krijgt een norm die wordt afgedwongen

De landingspagina opende met een manifest en een repo-overzicht; een CISO die iets zoekt om vandaag te
gebruiken moest daar doorheen. Besloten: de voorpagina opent met wat je kunt doen, in de volgorde van de
gebruiker; het verhaal blijft hetzelfde en de bron blijft een bestand (B9, gepreciseerd). Tegelijk bleek
de documentatiestandaard zwaarder dan de praktijk (2 van 22 repo's voldeden) en werd hij daarom omzeild.
Vervangen door een README-kop die haalbaar is (B11), een status die op een plek woont (B12), een label
voor infrastructuur (B8), en een herbruikbare controle die dit afdwingt.
Bouwplan: `2026-08-29-bouwplan-voorpagina-en-werkplaats.md`.

## 29-08-2026 · De toolpagina is opgeheven

`/tools/` beschreef drie eigen tools (publicatiescan, iamscan, blast-radius) plus vier tools die er nog
niet waren. Dat botste met B9: de projectentabel op het org-profiel is de enige projectenlijst. De pagina
was bovendien een derde plek waar hetzelfde verhaal stond, naast de tabel en de README van elke repo, en
liep achter: de omschrijving in `llms.txt` noemde onderwerpen die niet op de pagina stonden.

De pagina is vervangen door een doorverwijzing naar de hoofdpagina, zodat een eerder gedeelde link niet
doodloopt. Wat alleen daar stond is bewaard: de grens "toetsen, niet aanvallen" is principe 11 geworden,
en de vier richtingen die in voorbereiding zijn staan onder Meedoen op het profiel, met de zin erbij dat
een tool pas bestaat als hij in de tabel staat.

**Aanleiding:** een lezer die niet kon zien wat die pagina was, en of het over eigen of externe tooling
ging. Dat onderscheid is nu expliciet: eigen tools in de projectentabel, tooling van anderen in het
kennisbankitem Externe referenties, waar het profiel nu ook naar verwijst.

## 29-08-2026 · B10, elke pagina wijst terug

Twaalf van de vijftien pagina's op Pages hadden geen enkele link terug naar de hoofdpagina, en geen van de
kennisbankitems verwees naar zijn eigen vakgebied. Wie via een zoekmachine op een diepe pagina binnenkomt,
kwam daar dus niet verder.

Regel B10 toegevoegd: elke pagina begint met een kruimelpad naar de hoofdpagina en naar het niveau
erboven. In de kennisbank zet `tools/build.py` het kruimelpad automatisch en maakt `--check` het rood als
het ontbreekt of verouderd is; in een losse tool staat het in de eigen opmaak.

## 29-08-2026 · B3 wordt gecontroleerd, en een leesversie verwijst niet naar zichzelf

B3 eist al sinds het begin een HTML-leesversie bij elk tekstitem, maar niets controleerde dat. Twee items
hadden er geen, en een verwijzing naar zo'n item liep dood op een 404. `tools/build.py` controleert dit nu.

Daarnaast haalt de build de regel "lees dit online" uit de gegenereerde leesversie. Die hoort in de README,
waar hij de lezer op GitHub naar de leesversie wijst, maar op de leesversie zelf was het een link naar de
pagina waar je al stond.
