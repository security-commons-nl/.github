# Plan: GRC voor security, privacy en continuïteit, één risicogestuurde PDCA-ronde

**Doel:** één kennisbankpagina onder `governance` die uitlegt wat GRC is, waarom security, privacy en
continuïteit één stelsel nodig hebben, en twee routes om dat te doen: een GRC-tool kopen, of een
risicoboom bouwen uit platte bronnen met vaste guardrails en een AI-assistent als lezer. De tweede route
moet morgen te beginnen zijn: met een voorbeeldboom van een verzonnen gemeente en plakbare prompts.

**Besluiten bij het sparren (Bas, 14-10-2026):** de inhoudswijzers op de domeinroot worden afgeleid, niet
bijgehouden (stap 0); de externe bronnen uit §8 gaan erbij, open-source GRC-tools mogen bij naam omdat ze
open source zijn en geen aanbieder; de pagina heet "GRC voor security, privacy en continuïteit: één
risicogestuurde PDCA-ronde", slug `risicogestuurd-managementsysteem`. Het woord risicoboom valt één keer,
als de werknaam van de herkomstorganisatie; in de tekst heet het "het register met afleiding en prioriteit".
PDCA: Plan is het register, Do de maatregelen, Check de bevindingen en controls, Act de prioriteit.

**Aanleiding:** de architectuur van de risicoboom (concept 0.4, 30-09-2026) staat als item 02 in de
intake van de overdracht (`risicoboom-sturen-op-risico`, governance, nieuw). Bij het sparren op
14-10-2026 bleek dat de architectuur alleen niet genoeg is: de lezer moet eerst snappen waarom hij een
stelsel nodig heeft en wat de keuze is, en moet het daarna zelf kunnen proberen. Dit plan vervangt item 02.

**Wat niet mee gaat:** het register, de bevindingen, de maatregelstanden en de generatorscripts van de
herkomstorganisatie. De pagina is methode plus verzonnen voorbeeld, geen software (besluit *lichte
commons*, 02-09-2026). Namen van GRC-leveranciers alleen als categorie.

---

## 1. Wat er komt

Map `kennisbank/governance/risicogestuurd-managementsysteem/`, type `aanpak`, status `concept`, normen
`[BIO2, ISO 27001, AVG, ISO 22301, Cbw]`.

| Bestand | Wat | Lezer |
|---|---|---|
| `README.md` | De pagina: GRC in gewone woorden, waarom één stelsel voor drie disciplines, route A (tool) en route B (register met afleiding en prioriteit), keuzewijzer, en de spelregels van het register | bestuurder, CISO, FG, BCM'er |
| `index.html` | Leesversie, gegenereerd met `tools/leesversie.py` | idem |
| `model.md` | Het model van de boom: vijf lagen, drie kaders, relaties, schema van een bevinding, niveau (opzet, bestaan, werking), prioriteit als gewicht maal gat, de twee soorten eigenaar | CISO, ISO |
| `voorbeeld-risicoregister.md` | Verzonnen gemeente: 3 SR's, 6 OR's over de drie kaders, 5 bevindingen, circa 15 maatregelen (BIO2, BCM-set, AVG-kader), 3 controls; tabs Prioriteit, Bevindingen, Maatregelen | wie wil zien wat eruit komt |
| `voorbeeld-risicoregister.html` | Dezelfde boom als self-contained pagina met tabs en filters, gebouwd uit `voorbeeld-risicoregister.md` door een generatorscript in `tools/` van de kennisbank, met test op inhoud en geometrie | idem |
| `prompts.md` | Drie plakbare prompts: (1) context lezen en kandidaat-bevindingen maken in het schema; (2) een bevinding toetsen aan de drie grenzen en OR en SR afleiden uit de maatregel; (3) de prioriteitslijst opnieuw opbouwen. Plus de guardrails als tekst: wat de assistent nooit doet | CISO die route B begint |
| `sjabloon-register.md` | Leeg register in drie delen (SR, OR, bevindingen) met het schema als tabelkop, om in te vullen | idem |

De README verwijst naar elk bestand in een bestandstabel, zoals `risicoanalyse-aanvalspaden` dat doet.
`governance/README.md` krijgt regel 5 in de volgorde; `build.py` blokkeert anders.

## 2. De inhoud van de pagina, in volgorde

1. **Wat GRC is.** Weten welke risico's je loopt, welke maatregelen daar tegenover staan en of die
   werken. Drie werkwoorden: sturen, beheersen, aantonen. Geen leveranciersjargon.
2. **Waarom één stelsel voor drie disciplines.** Security (BIO2, Cbw), privacy (AVG) en continuïteit
   (ISO 22301) hebben elk een eigen kader, toezichthouder en functionaris, maar dezelfde processen,
   systemen en directie. Drie losse lijstjes spreken elkaar tegen aan dezelfde tafel. De Cbw maakt de
   zorgplicht gemeenschappelijk en toetsbaar.
3. **Route A: een GRC-tool.** Wat je koopt: workflow, bewijsbeheer, normkoppelingen, audit trail,
   meerdere gebruikers. Wat het kost: een licentie van een paar honderd tot een paar duizend euro per
   jaar (ordegrootte, geen aanbieders), inrichting van het normenstelsel, en vooral de tijd om de tool
   te blijven voeden. Eerlijk: de tool is goed in het proces, niet in het denken.
4. **Route B: een register met afleiding, prioriteit en AI-guardrails.** Platte bronnen in markdown, een vast schema, een
   assistent die context leest en kandidaten klaarzet, een mens die trieert, een deterministische
   afleiding van risico uit maatregel. Wat het geeft: scherpte, herleidbaarheid, geen licentie. Wat het
   niet geeft: het proces. De schrijver is de kritieke afhankelijkheid.
5. **Keuzewijzer.** Begin met B, want je leert wat je stelsel moet doen. Koop A als je dat weet. De
   boom is dan de specificatie waar de tool aan moet voldoen.
6. **De spelregels van de boom**, kort, met verwijzing naar `model.md`: een kaderstand is geen
   bevinding; de titel is het gat, aangetoond is het bewijs; de maatregel is het anker; prioriteit is
   gewicht maal gat; de boom toont geen eigenaren, het register wel.
7. **Zo begin je morgen.** Vijf stappen met de bestanden erbij: register invullen uit de eigen SRA,
   OR's uit de standaardlijst van elk kader, maatregelen uit VvT, BCM-set en AVG-kader, eerste
   bevindingen uit incidentregister en laatste audit via `prompts.md`, boom bouwen.

De toon neemt route A serieus. De auteur bouwde route B zelf; dat staat in de herkomstregel en de
tekst pleit niet, hij vergelijkt. Een kleine organisatie met één medewerker informatiebeveiliging kiest
soms terecht voor een tool.

## 3. Het voorbeeld

Verzonnen gemeente, zonder naam die bestaat. De drie SR's dekken elk een discipline, zodat de lezer
ziet hoe ze in één boom hangen:

| SR | Discipline | OR's eronder |
|---|---|---|
| SR-01 Uitval van kritieke dienstverlening door een cyberaanval | security, continuïteit | OR over herstel (BCM-thema), OR over kwetsbaarheden (ISO 27002-control) |
| SR-02 Onrechtmatige verwerking van persoonsgegevens | privacy | OR over rechten van betrokkenen (AVG-thema), OR over verwerkersovereenkomsten |
| SR-03 Misbruik van bevoegdheden door een insider of een gekaapt account | security | OR over toegangsbeheer, OR over logging |

Vijf bevindingen, elk uit een andere bronsoort (toets, incident, meting, test, analyse), elk gekoppeld
aan één of twee maatregelen met reden, één met status *geaccepteerd* zodat de lezer ziet dat die niet
meetelt. Drie controls op de maatregelen van toegangsbeheer, met opzet, bestaan en werking ingevuld,
één met een negatieve werkingstoets. De prioriteitslijst laat dan zien: de maatregelen onder een OR met
bevinding eerst, de rest op SR-score, bij gelijke stand het laagste niveau eerst.

Sleutels in de stijl van de bronnen (`BIO2:8.08.01`, `BCM:A.03.2`, `AVG:4.1`), met de kanttekening dat
de nummering per organisatie verschilt en dat de lezer zijn eigen bronlijst neemt.

## 4. De prompts en de guardrails

Elke prompt is zelfstandig te plakken in een willekeurige assistent (de kennisbank is tool-neutraal) en
bevat het schema uit `model.md` letterlijk, zodat de uitkomst altijd in dezelfde vorm komt. De
guardrails staan in elke prompt en nog eens apart:

- de assistent bedenkt geen bevinding; zonder vastgesteld feit, datum en bron is het een zorg, en die
  krijgt een reden waarom hij geen bevinding is;
- een kaderstand (niet geïmplementeerd, rood, niet voltooid) is nooit een bevinding;
- de assistent typt geen OR of SR bij een bevinding; die volgen uit de maatregel;
- rollen in plaats van namen, geen exploiteerbare details (hostnamen, accounts, kwetsbaarheid per
  systeem), geen stukken over personen, niets privé;
- een half gelezen bron blijft liggen;
- de mens beslist: elke uitkomst is een kandidaat tot iemand hem *open* zet.

Prompt 3 (prioriteit opnieuw opbouwen) is de enige die rekent. Hij krijgt het register als invoer en
geeft de lijst terug met per regel de reden van de plek, zodat de lezer kan narekenen. Het
generatorscript doet hetzelfde deterministisch; de prompt is er voor wie geen Python draait.

## 5. Bouwvolgorde

0. **Vindbaarheid afdwingen, vóór de pagina.** In `security-commons-nl.github.io/site/build.mjs`:
   de sitemap-kandidaten uitbreiden met elke URL uit `https://security-commons-nl.github.io/kennisbank/llms.txt`
   (opgehaald tijdens de build; de workflow draait elk uur, dus een nieuwe pagina staat binnen een uur in
   de sitemap), en het aantal stukken in de root `llms.txt` uit dezelfde lijst halen in plaats van het
   vaste getal "52". Test ernaast (`site/test_sitemap.mjs`): faalt als een kennisbank-URL in de gebouwde
   sitemap ontbreekt of het getal niet klopt; draait in `ci.yml`. Fixture met een vaste llms.txt, zodat
   de test niet van het netwerk afhangt. Statuutregel erbij (B3-aanvulling): de inhoudswijzers op de
   domeinroot zijn afgeleid en worden nooit met de hand bijgewerkt. Eén PR in de github.io-repo, één in
   `.github` voor het statuut. Pas daarna de pagina, zodat de eerste echte toets op dit mechanisme deze
   pagina is.
1. **Map en frontmatter.** Aanmaken, `governance/README.md` regel 5, `python tools/build.py --check`
   groen op een lege pagina met alleen frontmatter en titel.
2. **`model.md`** uit de architectuur 0.4, geanonimiseerd: geen Leidse aantallen, geen namen, geen
   verwijzingen naar interne mappen. Nalezen op "Leiden", "DT", "TIMS", "SIMS", namen van collega's,
   de gremia vervangen door rollen (directie, tactisch overleg).
3. **`voorbeeld-risicoregister.md`** schrijven, daarna het generatorscript `tools/bouw_risicoregister.py`
   dat er de HTML van maakt. Test: aantallen per laag, elke maatregel onder precies één OR, elke
   bevinding met minstens één maatregel, prioriteitsvolgorde gelijk aan de regel, geaccepteerde
   bevinding telt niet mee. Spiegeltest tussen de markdown-lijst en de HTML-tab. De HTML rekent niet
   zelf; hij toont wat het script berekende (geen tweede rekenregel in JavaScript).
4. **`prompts.md`** en **`sjabloon-register.md`**. Elke prompt één keer echt draaien op een verzonnen
   stukje context (een fictief incidentverslag van tien regels) en de uitkomst als voorbeeld onder de
   prompt zetten, zodat de lezer ziet wat hij mag verwachten.
5. **`README.md`** schrijven, in de stijl van de kennisbank (schrijfstijl-bas, geen em-dashes, geen
   bronnenlijst in het deelbare stuk; de bronnen als `bronnen:` in de frontmatter met ids uit
   `bronnen.json`, nieuwe ids erbij als ze ontbreken).
6. **Leesversie.** `python tools/leesversie.py governance/risicogestuurd-managementsysteem`, dan
   `python tools/build.py`.
7. **Lokaal toetsen.** `python tools/test_build.py`, `node tools/test_zoeken.js` (vindt "grc" en
   "pdca" en "risicoregister" de pagina), linkcheck. Weergave: `python -m http.server` op de kennisbankmap en met
   Playwright de pagina, de leesversie en `voorbeeld-risicoregister.html` openen op desktop en op
   telefoonbreedte; schermafdruk bekijken, niet alleen de DOM. Tabs klikken, filter op kader, geen
   horizontale scroll, zijbalk-inhoudsopgave aanwezig.
8. **Anonimiseringsronde.** `anonimizer-check` lokaal of op de PR; daarnaast een eigen grep op de
   woordenlijst uit `outputs\commons\redactie_portie2.py` plus "Leiden", "Leidse", "Servicepunt71",
   namen van collega's.
9. **PR en merge.** Eén PR, expliciet stagen (geen `git add -A`), geen Co-Authored-By, geen
   auteursvermelding. Bas leest de diff vóór de merge. CI bouwt op main de indexpagina's en
   `kennisbank/llms.txt` en commit ze terug.
10. **Na de merge: de vindbaarheid toetsen.** Binnen een uur: zoekvak op de live site vindt "grc",
    "pdca" en "risicoregister"; `kennisbank/llms.txt` noemt de pagina; `sitemap.xml` op de root heeft de
    regel (stap 0); het aantal stukken in de root `llms.txt` klopt; `robots.txt` ongewijzigd; `curl -I`
    op pagina, leesversie en voorbeeldboom geeft 200. Faalt een van deze, dan is stap 0 niet af.
11. **Overdracht bijwerken.** Intake-item 02 op gepubliceerd zetten met PR-nummer, in
    `INTAKE.md` en `herkomst.tsv`; regel in `OVERDRACHT\PLAN-commons.md`. Dat is werk-domein en
    gebeurt vanaf de werk-balie of met vermelding in de stand.
12. **Roadmap en plannen-README.** Dit plan in de tabel van `plannen/README.md` op *uitgevoerd*;
    `kennisbank/ROADMAP.md` noemt het nieuwe governance-item bij de volgende peildatum.

## 6. Wat kan tegenzitten

- **Toon.** Route B is het eigen werk van de auteur. Als de tekst een pleidooi wordt, is hij niet
  bruikbaar voor een organisatie die een tool heeft of wil. Toets: zou een leverancier van een
  GRC-tool de pagina eerlijk noemen.
- **Dubbel rekenwerk.** Een prioriteitsregel in Python én in een prompt kunnen uit elkaar lopen. De
  prompt verwijst daarom naar dezelfde regel in `model.md` en het voorbeeld in de pagina is door het
  script gemaakt, niet door de prompt.
- **Sleutels.** BIO2-, BCM- en AVG-nummering verschilt per organisatie en per versie van de bron. In
  het voorbeeld dus altijd "in de stijl van", en de lezer neemt zijn eigen lijst.
- **Omvang.** README onder 2.500 woorden; wat langer wordt, hoort in `model.md`. Anders leest de
  bestuurder niet verder dan de keuzewijzer, en die is nu juist voor hem.

## 7. Besloten bij het schrijven (14-10-2026)

1. Slug `risicogestuurd-managementsysteem`; de map heette in het eerste concept `grc-sturen-op-risico`.
2. Type `aanpak` met `barrieres: [owner, treatment]`, zoals `risicoanalyse-aanvalspaden`; zo is de pagina
   vindbaar vanaf de zelfcheck zonder de koppen van een handleiding.
3. Het generatorscript gaat mee als `tools/bouw_risicoregister.py`, klein en getest, zoals
   `bouw_stelselkaart.py`.
4. Aankondigen in Discussions na de merge, met de hand, eerst met *alleen tonen*.

## 8. Externe bronnen

Al in `bronnen.json` (gecontroleerd 14-10), in de frontmatter opnemen:

- `ibd-bio2-handreiking-isms`, `ibd-bio2-infographic-wat-is-een-isms`,
  `ibd-bio2-handreiking-isms-proces-implementatie`: het managementsysteem en de PDCA-ronde.
- `ibd-bio-handreiking-risicomanagement-voor-gemeenten`,
  `ibd-risicoregister-inclusief-risicobehandelplan-en-dashboards`,
  `ibd-handreiking-risicoregister-en-risico-acceptatie-overeenkomst-rao`,
  `ibd-bio2-kans-en-impact-tabellen-gemeenten`: register, scoring en acceptatie.
- `ibd-avg-borgingsproduct-3-1-toetsingskader`, `ibd-avg-borgingsproduct-3-1-handreiking`: de privacykant.
- `cip-bio-tekst`: de BIO 2.0 zelf. `ncsc-cbw-valt-mijn-organisatie-eronder`: de zorgplicht.

Toe te voegen aan `bronnen.json` (partij bestaat in de stelselkaart of komt erbij):

- ISO 31000:2018, principes en proces van risicomanagement (NEN, samenvatting vrij leesbaar); ISO/IEC 27005
  als uitwerking voor informatiebeveiliging. De normen zelf zijn niet vrij; verwijzen naar de NEN-pagina.
- NIST Cybersecurity Framework 2.0, functie Govern (vrij, Engels): de bovenlaag voor drie disciplines.
- ISO 22301:2019 en ISO 22313 (BCM): alleen in `normen:` en als verwijzing naar NEN; geen vrije tekst.
- NCSC: handreiking risicomanagement of de Cbw-zorgplichtpagina's, voor zover niet al in het register.
- Open-source GRC-tools, als voorbeeld bij route A dat "een tool" niet per se een licentie is:
  CISO Assistant (intuitem, AGPL) en Eramba Community. Bij naam omdat ze open source zijn; geen
  commerciële aanbieders. Per tool één regel: wat het doet en wat het kost (hosting, eigen beheer).

Elke bron krijgt in het register wat het statuut vraagt (titel, partij, url, wat je eraan hebt); de
pagina zelf heeft geen bronnenlijst in de tekst, alleen de frontmatter.
