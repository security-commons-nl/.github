# Bouwplan: Applicatiecheck (één applicatie tegen BIO2, uit de applicatie zelf)

**Doel:** een instrument in de browser dat voor één gekochte applicatie laat zien welke BIO2-maatregelen
de applicatie zélf kan aantonen, uit een configuratie-export (A) en een logsample (B), aangevuld met
document of schermafbeelding (C), en dat eerlijk zegt wat buiten de applicatie ligt (D). Uitkomst is een
dossier per maatregel met bewijs, peildatum en comply-or-explain, zoals de CSIR Assessment Tool dat voor
een object doet.

**Aanleiding:** of een kritische applicatie aan de BIO2 voldoet wordt getoetst met een vragenlijst aan
beheerder of leverancier, en een vinkje is geen bewijs. De applicatie weet het beter: de export zegt wat
is ingesteld, de log zegt wat er gebeurt. De commons heeft voor precies dit patroon al drie werkende
vormen (de zelfcheck van `aanvalspaden`, de CSIR Assessment Tool, `anonimizer-browser`): één
HTML-bestand, bron in JSON, niets verlaat het apparaat. Repo en pagina bestaan sinds 02-09-2026 als
concept; dit plan beschrijft wat er gebouwd wordt om het label naar *prototype* te tillen.

**Grenzen, en wat het niet is.** Eenheid is één applicatie, niet het landschap (dat is
`security-posture-tool`); het instrument levert bewijs, het beheert het niet (dat is `grc-platform`);
het is de eerste concrete uitwerking van `policy-as-code` voor één kader en één eenheid, geen regeltaal
voor de hele norm; het stelt vast, de kennisbank legt uit hoe. Kader voor de indeling is de gekochte
applicatie (CIP BIO Thema-uitwerking Softwarepakketten); zelfbouw (Applicatieontwikkeling) komt later,
anders verdubbelt de indeling. Eerste toepassing: een zaaksysteem, JOIN Zaak & Document.

**Tech stack:** Python 3.12 (bouwscript, referentie-implementatie, tests), pytest, Playwright
(browsertests), vanilla JS en CSS in de pagina, geen bundler. De leesversie van het ontwerp loopt via de
gedeelde site-build; het instrument zelf wordt één HTML-bestand met CSP, gebouwd met `python bouw.py`.
Lees `csir-assessment-tool/register/` eerst; alles hier is daar een variant van.

---

## 1. Bron en bewijsmodel (F0, gebouwd 02-09-2026)

**`bronnen/bio2.json`** is een bewaakte kopie van `cisochat/data/bio2.json`: 148 overheidsmaatregelen
met nummer, ISO-nummer, titel, thema en de tekst van de overheidsmaatregel (van CIP, openbaar). De
ISO-tekst wordt niet gekopieerd (auteursrecht). `tools/haal_bio2.py` maakt de kopie en zet de commit
van de bron erin; `--check` faalt in CI als de kopie achterloopt. Zelfde patroon als
`aanvalspaden/mappingen/bronnen/`.

**`bewijs.json`** is het eerste product: per overheidsmaatregel de bewijssoort(en), de bron (eigen of
leverancier), wat het bewijs moet bevatten, een ASVS-verwijzing waar die helpt, en een motivering. Het is
met de hand bijgehouden en `tools/bouw_indeling.py` genereert er `indeling.md` uit, de tweede tab op de
pagina. Stand bij schrijven: 148 rijen, status *voorlopig*: 28 met A of B (24 met A als eerste soort, 4 met B), 20 met C, 100 D.

Hoe de eerste indeling is gemaakt, in vijf lagen:

| Laag | Bron | Wat het oplevert |
|---|---|---|
| 1 | `bio2.json`: hoofdstuk en thema (`iv_standaard`) | 5, 6 en 7 grotendeels D; 8.x per thema een voorlopige soort |
| 2 | CIP Thema-uitwerking Softwarepakketten: domeinen Beleid, Uitvoering, Control | Beleid en Control zijn D; Uitvoering levert de kandidaten voor A, B, C |
| 3 | OpenCRE: ISO-nummer naar ASVS-eisen (V2, V3, V4, V6, V7, V14) | per A/B-maatregel wat het bewijs moet bevatten |
| 4 | IBD RASCI-tabel BIO-controls | D waar de R buiten beheer en leverancier ligt |
| 5 | menselijke pas, per maatregel, met een zaaksysteem in het hoofd | status *bevestigd* |

Laag 1, 3 en 4 zijn op 02-09 toegepast uit kennis van de kaders; laag 2 is nog niet tegen de CIP-tekst
gelegd (de site van CIP laat geen geautomatiseerd ophalen toe) en laag 5 is de eerstvolgende stap: een
sessie met de tabel ernaast, rij voor rij, en daarna wisselt de status van *voorlopig* naar
*bevestigd*. Een test bewaakt dat elke maatregel precies één keer voorkomt, dat A/B/C zeggen wat het
bewijs is en dat `indeling.md` gelijk loopt.

**Gesignaleerd in de bron** (cisochat, niet hier te repareren): 5.18.01 en 5.18.02 herhalen de MFA-tekst
van 5.17; 5.16.01 en 5.16.02 dragen een tekst over AdES en internetfacing-registratie die niet bij
identiteitsbeheer lijkt te horen; 5.24.01 draagt een ketentekst; 5.24.08 (CVD) heeft geen thema en geen
tekst; 8.21.02 is verminkt. De indeling is op de ISO-titel gedaan waar de tekst afwijkt, met de afwijking
in de motivering. Voorstel: issue op cisochat.

## 2. Regels als data (F1)

**`regels.json`**: per maatregel met soort A of B een of meer regels. Een regel is leesbaar voor een
niet-ontwikkelaar en heeft een vaste vorm:

```
{ "maatregel": "8.15.01", "soort": "B", "naam": "logregel-velden",
  "eis": "elke regel bevat actie, object, resultaat, oorsprong, identiteit, tijdstip",
  "toets": { "type": "velden_aanwezig", "velden": ["actie","object","resultaat","oorsprong","identiteit","tijdstip"], "drempel": 1.0 },
  "uitkomst": { "voldoet": "aangetoond", "deels": "gedeeltelijk", "anders": "niet aangetoond" } }
```

Toetstypen zijn een kleine, gesloten set: `velden_aanwezig`, `waarde_gelijk`, `waarde_in`,
`waarde_minimaal`, `geen_patroon` (PII, secrets), `tijdstempel_geldig`, `tijdspanne_minimaal`,
`lijst_leeg` (bijvoorbeeld inactieve accounts met rechten). Komt een maatregel niet in die set, dan is
de regel nog niet uitdrukbaar en blijft de maatregel op *handmatig* staan; dat is een eerlijker uitkomst
dan een regel die het niet echt toetst.

Uitkomsten per maatregel: *aangetoond*, *gedeeltelijk*, *niet aangetoond*, *niet aantoonbaar* (D),
*niet van toepassing* (met onderbouwing), *handmatig* (C, of nog geen regel). De formulering volgt
`aanvalspaden`: bewijs *levert bewijs voor* een maatregel, nooit "voldoet aan".

**Referentie-implementatie** `toets.py` in Python en dezelfde regels in `app.js`; een test draait beide
op dezelfde fixture en eist hetzelfde antwoord (het patroon `reken.py` ⟷ `app.js` van de CSIR-tool).
Eerste regels: 8.15.01, 8.15.02, 8.17.01 (B), 5.17.01, 5.18.01, 8.05.01, 8.09.01 (A).

## 3. Parsers (F1 generiek, F2 product)

Een parser zet een aangeleverd bestand om in **feiten**: een plat JSON-object met een vaste vocabulaire
(`accounts[]`, `rollen[]`, `instellingen{}`, `logregels[]`). Regels toetsen alleen feiten, nooit het
ruwe bestand; zo blijft een regel geldig over applicaties heen en zit al het applicatiespecifieke in
de parser.

- **Generiek (F1):** CSV en JSON met een kolomkoppeling die de gebruiker in de pagina maakt (welke kolom
  is identiteit, welke tijdstip). Vangnet voor elke applicatie zonder eigen parser.
- **JOIN (F2):** de auditgegevens van JOIN zijn als tab-gescheiden bestand te exporteren, per audittype,
  met instelbare retentie (publieke documentatie van Decos). De exacte kolomnamen komen uit die
  documentatie of van een beheerder, en gaan in een **synthetische fixture**; een echte export van een
  productiesysteem komt niet in de repo (statuut A9). Voor de configuratiekant: rollen en gebruikersrollen
  uit JOIN Admin, en de audit-instellingen (welke typen, retentie, externe auditdatabase).
- **Logsample is een structuurtoets:** de laatste 24 uur of 1000 regels. Vóór alles gaat het sample door
  de entiteitdetectie van `anonimizer-browser` (hergebruik van de TypeScript-module, of een port naar
  vanilla JS als de bundler-vrije pagina dat vraagt; dat is een beslissing bij F2). Gedragsmeting over
  maanden is werk voor SIEM en `security-posture-tool`.

## 4. De pagina (F3)

Eén HTML-bestand op `/applicatiecheck/check/` naast de leesversie, gebouwd met `python bouw.py` uit
`bronnen/bio2.json`, `bewijs.json`, `regels.json` en de pagina-onderdelen, met een CSP die netwerkverkeer
verbiedt behalve de optionele AI-aanroep. Drie stappen:

1. **Aanleveren.** Applicatienaam, versie, peildatum; bestanden slepen (export, logsample, documenten);
   de parser wordt herkend aan de inhoud of gekozen.
2. **Toetsen.** De regels lopen lokaal; per maatregel de uitkomst, het bewijs waarop hij rust (met
   sha256 van het bestand en de regel die is toegepast), en bij C en *handmatig* een invulveld.
3. **Dossier.** Per maatregel: BIO2-tekst woordelijk, bewijssoort, bewijs met hash en peildatum,
   uitkomst, verantwoordelijke, onderbouwing bij afwijking. Opslaan als JSON, later weer inladen,
   uitdraaien als HTML. Wat de applicatie niet kan aantonen (D) staat erin met de reden.

Het dossier-schema wordt waar mogelijk gedeeld met de CSIR Assessment Tool (één dossiervorm voor
objecten en applicaties). Dat raakt het werk van de auteur van die tool: afstemmen (statuut A4), niet
besluiten.

Kruimelpad en voetregel volgens B10; browsertests met Playwright vergelijken de uitslag op het scherm
met `toets.py` op dezelfde fixture.

## 5. AI (F4)

Alleen met een eigen Mistral-sleutel in v1 (zoals `anonimizer-browser` dat kan). Uitsluitend voor C:
een document of schermafbeelding omzetten naar feiten in dezelfde vocabulaire als de parsers, en voor
het formuleren van een bevindingtekst. Elk AI-resultaat krijgt de status *wacht op bevestiging* tot een
mens hem aanvinkt; pas dan telt het als bewijs. AI komt nooit in het oordeel: de uitkomst van een
maatregel is altijd een regel over feiten. De gedeelde `anonimizer-proxy` laat dezelfde origin technisch
al toe, maar of die route hier mag (gedeelde sleutel, kosten, verwerkersrol) is een apart besluit voor
`BESLUITEN.md`.

## 6. Testmateriaal

`tests/fixtures/`: een synthetische configuratie-export en een synthetisch logsample per parser, en een
doorloopdossier (zoals `doorloop-2026-09.json` bij de CSIR-tool) dat de verwachte uitkomst per
maatregel vastlegt. Geen productie-export, ook niet geanonimiseerd, in de repo; wie er een wil delen
haalt hem door de anonimizer en dan is het een fixture met een herkomstregel, geen export.

## 7. Fasering

| Fase | Wat | Label |
|---|---|---|
| F0 | `bronnen/bio2.json`, `bewijs.json`, `indeling.md`, tests, CI (**gedaan 02-09-2026**); daarna laag 2 en laag 5 van de indeling | concept |
| F1 | `regels.json` met de eerste zeven regels, `toets.py`, generieke CSV/JSON-parser, fixtures | concept |
| F2 | JOIN-parser (audit-export en rollen) op synthetische fixture, PII-scrub op het logsample | concept |
| F3 | de pagina met aanleveren, toetsen, dossier; Playwright-tests; rij in de projectentabel naar *Live tool* | **prototype** |
| F4 | AI voor C met eigen sleutel, status *wacht op bevestiging* | prototype |

## 8. Open vragen

- Hoeveel van de 28 A/B-maatregelen zijn na laag 5 nog A/B, en welke worden *handmatig* omdat de
  toetsset ze niet uitdrukt? Dat getal bepaalt of de generieke parser genoeg is voor een eerste
  gebruiker.
- Regels in JSON met een gesloten toetsset, of later een bestaande regeltaal (OPA/Rego)? We beginnen met
  JSON tot iemand aantoont dat het knelt; dat is ook de open vraag van `policy-as-code`.
- Hergebruik van de anonimizer-entiteitdetectie: als module (TypeScript, dus een bundler) of als port
  (vanilla JS, dubbel onderhoud)? Beslissen bij F2, met de anonimizer-onderhouder.
- De proxy als gedeelde AI-route: apart besluit.

## Stand

| Stap | Stand |
|---|---|
| Repo, pagina, projectentabel, B13 | gedaan, 02-09-2026 |
| F0: bron, bewijs.json, indeling, tests, CI | gedaan, 02-09-2026 |
| F0: laag 2 (CIP Softwarepakketten) en laag 5 (bevestigen per maatregel) | te doen |
| F1 t/m F4 | te doen |
