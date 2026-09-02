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
`aanvalspaden/meting/`, waarin `security-posture-tool` en `iamscan` opgaan; besluit 02-09-2026); het instrument levert bewijs, het beheert het niet (dat is `grc-platform`);
het is de eerste concrete uitwerking van `policy-as-code` voor één kader en één eenheid, geen regeltaal
voor de hele norm; het stelt vast, de kennisbank legt uit hoe. Kader voor de indeling is de gekochte
applicatie (CIP BIO Thema-uitwerking Softwarepakketten); zelfbouw (Applicatieontwikkeling) komt later,
anders verdubbelt de indeling. Eerste toepassing: een zaaksysteem, JOIN Zaak & Document.

**Rol in de commons.** Sinds het besluit van 02-09-2026 over de scanners is dit de
**referentie-implementatie van de bewijs-vorm** (`ARCHITECTUUR.md`): regels als JSON, een parser per bron,
een bevinding met bewijs en bron, vier bewijssoorten, dossier als JSON. `aanvalspaden/meting/` en
`procescheck` nemen die vorm over, zonder gedeelde bibliotheek. Wat hier expliciet en saai is opgeschreven,
wordt daar gekopieerd; liever iets te expliciet dan iets te slim.

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

**Bron is `normen` (uitgevoerd 02-09-2026, issue `applicatiecheck#2`).** `tools/haal_normen.py` haalt
`bio2.json` uit `normen` en `--check` blokkeert in CI als de kopie achterloopt; `bewijs.json` noemt de
vingerafdruk `143d785a8931`. Daarbij is de **tekst van de overheidsmaatregel uit de repo verwijderd**
(41.824 tekens): het CIP publiceert onder CC BY-NC-SA 4.0 en dat is niet te verenigen met herdistributie
onder EUPL-1.2 (besluit van dezelfde dag). Wat blijft is nummer, titel en thema; een test blokkeert de
terugval. Gevolg voor het ontwerp: het dossier toont het **nummer en de titel** van een maatregel en
verwijst voor de tekst naar de CIP-publicatie. Dat is een verschil met de CSIR Assessment Tool, die de
eisteksten wel woordelijk mag tonen (andere rechthebbende, ander regime), en het betekent dat de uitdraai
van applicatiecheck geen eisenbron voor een aanbesteding is.

**Gesignaleerd in `normen` bij de omzetting:** zestig van de 148 titels dragen nog de afbreekregels van de
oorspronkelijke CIP-tabel (`"Rollen en verantwoordelijkheden bij \ninformatiebeveiliging"`) en twee een losse
afsluitende apostrof (`"User endpoint devices'"`). De titelvergelijking hier normaliseert daarop; opschonen
hoort in `normen` te gebeuren, niet in een kopie.

**`bewijs.json`** is het eerste product: per overheidsmaatregel de bewijssoort(en), de bron (eigen of
leverancier), wat het bewijs moet bevatten, een ASVS-verwijzing waar die helpt, en een motivering. Het is
met de hand bijgehouden en `tools/bouw_indeling.py` genereert er `indeling.md` uit, de tweede tab op de
pagina. Stand na de bevestigingsronde van 02-09-2026: 148 rijen, status *bevestigd*: 33 met A of B (29 met A als eerste soort, 4 met B), 21 met C, 94 D; 5.03.01 (functiescheiding) is na laag 2 naar A gegaan, met de lijst van onverenigbare rollen als invoer.

Hoe de eerste indeling is gemaakt, in vijf lagen:

| Laag | Bron | Wat het oplevert |
|---|---|---|
| 1 | `bio2.json`: hoofdstuk en thema (`iv_standaard`) | 5, 6 en 7 grotendeels D; 8.x per thema een voorlopige soort |
| 2 | CIP Thema-uitwerking Softwarepakketten: domeinen Beleid, Uitvoering, Control | Beleid en Control zijn D; Uitvoering levert de kandidaten voor A, B, C |
| 3 | OpenCRE: ISO-nummer naar ASVS-eisen (V2, V3, V4, V6, V7, V14) | per A/B-maatregel wat het bewijs moet bevatten |
| 4 | IBD RASCI-tabel BIO-controls | D waar de R buiten beheer en leverancier ligt |
| 5 | menselijke pas, per maatregel, met een zaaksysteem in het hoofd | status *bevestigd* |

Laag 1, 3 en 4 zijn op 02-09 toegepast uit kennis van de kaders; laag 5 is dezelfde dag gedaan, per
familie in plaats van per rij, en heeft de status op *bevestigd* gezet. Laag 2 is dezelfde dag gedaan
met de Thema-uitwerking Softwarepakketten **v2.0 (mei 2026, BIO2 1.3 verwerkt)**: 57 rijen dragen nu een
CIP-objectnummer (veld `cip`, kolom op de pagina), er is geen rij teruggezet naar *voorlopig*, en drie
dingen zijn scherper geworden: CIP U.08 zegt letterlijk dat authenticatie in het pakket alleen relevant
is als de infrastructuur (de identity provider) er niet in voorziet, wat de SSO-lezing van 5.17 bevestigt;
CIP U.11.4 zegt dat de bewaartermijn van logging tot uitdrukking komt in de configuratie-instellingen van
het pakket (8.15.04 als A); CIP U.10.2 maakt functiescheiding (5.03.01) toetsbaar op de rollenexport zodra
de lijst van onverenigbare autorisaties er is (kandidaat voor A, nog niet omgezet). De CIP-tekst is
CC BY-NC-SA: alleen objectnummers en parafrase, geen overgenomen tekst. Een test bewaakt dat elke maatregel precies één keer voorkomt, dat A/B/C zeggen wat het
bewijs is en dat `indeling.md` gelijk loopt.

Wat laag 5 heeft vastgelegd, en wat de regels van F1 dus moeten volgen:

- **Uitgangspunt: SaaS bij de leverancier, SSO via de centrale identity provider.** Eigen hosting en
  lokale authenticatie staan als variant in de motivering, niet als aparte rijen.
- **MFA (5.17) telt via SSO:** de applicatie bewijst dat alle inlog via de identity provider loopt en dat
  er geen lokale wachtwoordaccounts zijn (A); het MFA-beleid zelf is een schermafbeelding van de identity
  provider (C).
- **De log is de audit-export uit de applicatie zelf,** niet de kopie in de SIEM; de aansluiting op de
  SIEM is 8.16.03 (C).
- **Rollen en rechten komen uit een export van de beheeromgeving** (A); bestaat die niet, dan valt de
  rij terug op C.
- **8.05.01 krijgt twee regels:** leverancierstoegang (de BIO2-tekst) en inloginstellingen (de
  ISO-lezing).
- **De pagina doet geen netwerkverkeer:** transportversleuteling komt uit de configuratie (A) en een
  extern scanrapport komt binnen als document (C).
- **8.08.01 rekent achterstand uit:** versie uit de export, laatste release met datum en bron-URL door de
  gebruiker ingevoerd.
- **Van D naar A:** 8.32.01 (verschil tussen twee exports), 8.12.01 (export- en downloadbeperkingen),
  5.12.01 (classificatieniveaus), 5.28.01 (logretentie drie jaar), 5.14.01 (koppelingenlijst).
- **Naar leverancier:** 8.31.01 (testomgeving is bij SaaS een dienst).

**Gesignaleerd in de bron** (cisochat, niet hier te repareren): 5.18.01 en 5.18.02 herhalen de MFA-tekst
van 5.17; 5.16.01 en 5.16.02 dragen een tekst over AdES en internetfacing-registratie die niet bij
identiteitsbeheer lijkt te horen; 5.24.01 draagt een ketentekst; 5.24.08 (CVD) heeft geen thema en geen
tekst; 8.21.02 is verminkt. Daarnaast verwijst de CIP-uitwerking naar BIO2 8.24.04 en 8.24.05, terwijl de
dataset voor 8.24 alleen .01 kent: nagaan of de dataset daar overheidsmaatregelen mist. De indeling is op
de ISO-titel gedaan waar de tekst afwijkt, met de afwijking in de motivering. Voorstel: issue op cisochat.

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
Eerste regels: 8.15.01, 8.15.02, 8.17.01 (B), 5.17.01, 5.18.01, 8.05.01, 8.09.01, 8.32.01 (A).

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
| F0 | `bronnen/bio2.json`, `bewijs.json`, `indeling.md`, tests, CI, bevestigingsronde, CIP ernaast (**gedaan 02-09-2026**) | concept |
| F1 | `regels.json` met de eerste zeven regels, `toets.py`, generieke CSV/JSON-parser, fixtures | concept |
| F2 | JOIN-parser (audit-export en rollen) op synthetische fixture, PII-scrub op het logsample | concept |
| F3 | de pagina met aanleveren, toetsen, dossier; Playwright-tests; rij in de projectentabel naar *Live tool* | **prototype** |
| F4 | AI voor C met eigen sleutel, status *wacht op bevestiging* | prototype |

## 8. Open vragen

- Hoeveel van de 33 A/B-maatregelen zijn na laag 5 nog A/B, en welke worden *handmatig* omdat de
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
| F0: laag 5 (bevestigen per familie) | gedaan, 02-09-2026 |
| F0: laag 2 (CIP Softwarepakketten v2.0 ernaast) | gedaan, 02-09-2026 |
| F0: bron naar `normen`, CIP-tekst eruit (issue #2) | gedaan, 02-09-2026 |
| F1 t/m F4 | te doen; uitvoeringsplan stap voor stap staat in deel 2 hieronder (02-09-2026) |

---

# Deel 2: uitvoering, stap voor stap (F1 t/m F4)

> **Voor wie dit uitvoert (mens of model):** dit deel is geschreven voor iemand die de commons niet kent en
> geen ontwerpkeuzes hoeft te maken. Elke taak heeft exacte bestanden, exacte code, een test die eerst
> faalt, en een commit. Werk de taken in volgorde af; sla er geen over. Lees eerst deel 1 (het waarom) en
> `csir-assessment-tool/register/LEESMIJ.md` (het patroon dat hier wordt gekopieerd). Gebruik de
> superpowers-skill `executing-plans` of `subagent-driven-development` en vink de stappen af.

**Doel:** Applicatiecheck van concept naar prototype: regels als data, een referentie-implementatie in
Python, parsers, een offline pagina met dossier, en AI alleen voor bewijssoort C.

**Architectuur:** parsers zetten aangeleverde bestanden om in één plat `feiten`-object; regels uit
`regels.json` toetsen alleen feiten; `toets.py` is de referentie en `check/bron/app.js` spiegelt hem
functie voor functie; de pagina is één HTML met CSP `default-src 'none'`, gebouwd door `check/bouw.py`.

**Tech stack:** Python 3.12 zonder dependencies (pytest voor tests, playwright voor browsertests),
vanilla JS en CSS, geen bundler. Node alleen voor de bestaande leesversie (`site/build.mjs`).

**Spec:** deel 1 van dit document, plus `applicatiecheck/README.md` en `applicatiecheck/bewijs.json`.

## Globale regels (gelden voor elke taak)

- Taal: Nederlands in code-commentaar, tests, teksten en commits. Engelse vaktermen blijven Engels.
- Commits: Nederlands, map als prefix, één onderwerp per commit, geen AI-attributie (statuut B6, A7).
  Stage alleen de bestanden die je hebt aangeraakt; nooit `git add -A`.
- Geen echte export van een productiesysteem in de repo, ook niet geanonimiseerd. Fixtures zijn
  verzonnen (statuut A9).
- Geen ISO 27002-tekst in de repo; de BIO2-tekst komt uit `bronnen/bio2.json` (statuut, normen-besluit).
- De pagina mag geen netwerkverkeer doen, behalve de ene AI-aanroep in F4 na een klik van de gebruiker.
- Uitkomsten heten letterlijk: `aangetoond`, `gedeeltelijk`, `niet aangetoond`, `geen bewijs`,
  `handmatig`, `niet aantoonbaar`, `niet van toepassing`. Nergens "voldoet".
- Alle tests draaien met `python -m pytest tests/ -v` vanuit `applicatiecheck/`. Rood = niet klaar.
- Bestandspaden in dit deel zijn relatief aan `X:\SECURITY-COMMONS-NL\applicatiecheck\`.

## Bestandsboom na F4

```
applicatiecheck/
├── README.md                    bestaat; krijgt in F3 de link naar de tool
├── bewijs.json                  bestaat (F0)
├── indeling.md                  bestaat, gegenereerd (F0)
├── regels.json                  F1: de regels als data
├── bronnen/bio2.json            bestaat (F0)
├── toets.py                     F1: referentie-implementatie van de toetstypen
├── patronen.py                  F2: PII-patronen (BSN, IBAN, e-mail, telefoon, wachtwoord)
├── parsers/
│   ├── __init__.py              F1
│   ├── feiten.py                F1: het feiten-schema en de validatie
│   ├── generiek.py              F1: CSV/JSON naar feiten
│   └── join.py                  F2: JOIN-auditexport en JOIN-rollen naar feiten
├── check/
│   ├── bouw.py                  F3: één HTML uit bron/ + de JSON-bronnen
│   ├── bron/index.html          F3
│   ├── bron/app.css             F3
│   ├── bron/app.js              F3: spiegel van toets.py + de pagina
│   ├── bron/patronen.js         F2: spiegel van patronen.py
│   └── bron/ai.js               F4: de Mistral-aanroep, alleen voor C
├── tests/
│   ├── test_bewijs.py           bestaat
│   ├── test_regels.py           F1
│   ├── test_toets.py            F1
│   ├── test_parsers.py          F1, F2
│   ├── test_patronen.py         F2
│   ├── test_bouw.py             F3
│   ├── test_app.py              F3: Playwright, vergelijkt scherm met toets.py
│   └── fixtures/
│       ├── generiek-config.json F1
│       ├── generiek-log.csv     F1
│       ├── generiek-log.kolommen.json  F1
│       ├── feiten-verwacht.json F1: wat de parser uit de twee bovenstaande moet maken
│       ├── join-audit.tsv       F2
│       ├── join-rollen.tsv      F2
│       └── doorloop-2026-09.json F3: een compleet dossier met verwachte uitkomsten
├── site/config.json             bestaat; F3 voegt niets toe (de tool staat op /check/)
└── .github/workflows/ci.yml     bestaat; F3 voegt een browserjob toe
```

## De datamodellen (lees dit vóór F1)

### Feiten (wat een parser oplevert)

Eén plat object. Ontbreekt een sleutel, dan is het feit er niet; een regel die het nodig heeft geeft
dan `geen bewijs`. Alle tijdstippen zijn ISO 8601 met tijdzone (`2026-09-01T10:00:00+02:00`).

```json
{
  "formaat": "applicatiecheck-feiten",
  "versie": 1,
  "applicatie": {"naam": "Voorbeeld Zaaksysteem", "versie": "6.21"},
  "bronbestanden": [
    {"naam": "export.json", "soort": "configuratie", "sha256": "…", "peildatum": "2026-09-01"},
    {"naam": "audit.csv", "soort": "log", "sha256": "…", "peildatum": "2026-09-01"}
  ],
  "instellingen": {
    "sso_afgedwongen": true,
    "sessie_timeout_minuten": 15,
    "lockout_pogingen": 5,
    "https_only": true,
    "geen_terugval": true,
    "laatste_release": "6.21",
    "laatste_release_datum": "2026-08-15",
    "onverenigbare_rollen": [["aanvrager", "goedkeurder"]]
  },
  "vorige_instellingen": null,
  "accounts": [
    {"id": "u1", "type": "persoon", "rollen": ["beheerder"], "lokaal_wachtwoord": false,
     "laatste_inlog": "2026-08-30T09:00:00+02:00", "einddatum": null}
  ],
  "rollen": [{"id": "beheerder", "beheer": true}],
  "logtypen": [{"naam": "audit", "aan": true, "retentie_dagen": 1095}],
  "logregels": [
    {"tijdstip": "2026-09-01T10:00:00+02:00", "identiteit": "u1", "actie": "wijzig",
     "object": "zaak/123", "resultaat": "ok", "oorsprong": "10.0.0.5"}
  ],
  "koppelingen": [{"naam": "ZGW", "authenticatie": "oauth2", "versleuteld": true}]
}
```

`type` van een account is `persoon`, `leverancier` of `service`. `vorige_instellingen` is `null` of een
object met dezelfde vorm als `instellingen` (een eerdere export, voor 8.32.01).

### Regels (`regels.json`)

```json
{
  "formaat": "applicatiecheck-regels",
  "versie": 1,
  "toetstypen": ["velden_aanwezig", "geen_patroon", "tijdstempel_geldig", "waarde_gelijk",
                 "waarde_minimaal", "waarde_maximaal", "lijst_leeg", "bron_aanwezig",
                 "verschil_met_vorige", "geen_onverenigbare_rollen"],
  "regels": [
    {"id": "8.15.01-velden", "maatregel": "8.15.01", "soort": "B", "naam": "Logregel bevat de zes velden",
     "eis": "Elke logregel bevat tijdstip, identiteit, actie, object, resultaat en oorsprong.",
     "toets": {"type": "velden_aanwezig", "over": "logregels",
               "velden": ["tijdstip", "identiteit", "actie", "object", "resultaat", "oorsprong"],
               "drempel": 1.0}}
  ]
}
```

Betekenis per toetstype (dit is de spec van `toets.py`; `app.js` doet exact hetzelfde):

| type | velden in `toets` | uitkomst |
|---|---|---|
| `velden_aanwezig` | `over` (lijstnaam), `velden`, `drempel` (0..1) | aandeel records waarin álle velden niet-leeg zijn: ≥ drempel → aangetoond; > 0 → gedeeltelijk; 0 → niet aangetoond. Lijst ontbreekt of leeg → geen bewijs |
| `geen_patroon` | `over`, `patronen` (namen uit `patronen.py`) | 0 treffers in alle tekstvelden → aangetoond; anders niet aangetoond, `waarde` = aantal treffers per patroon |
| `tijdstempel_geldig` | `over`, `veld`, `drempel` | elk record: veld is ISO 8601 mét tijdzone; volgorde niet-dalend; aandeel geldig ≥ drempel → aangetoond; > 0 → gedeeltelijk; anders niet aangetoond |
| `waarde_gelijk` | `pad` (bv. `instellingen.sso_afgedwongen`), `waarde` | gelijk → aangetoond; anders niet aangetoond; pad ontbreekt → geen bewijs |
| `waarde_minimaal` | `pad`, `waarde` (getal) | ≥ → aangetoond; anders niet aangetoond |
| `waarde_maximaal` | `pad`, `waarde` (getal) | ≤ → aangetoond; anders niet aangetoond |
| `lijst_leeg` | `over`, `waar` (lijst van voorwaarden) | records die aan álle voorwaarden voldoen: geen → aangetoond; wel → niet aangetoond, `waarde` = de ids. Lijst ontbreekt → geen bewijs |
| `bron_aanwezig` | `soort` (`configuratie`/`log`) | er is een bronbestand van die soort → aangetoond; anders geen bewijs |
| `verschil_met_vorige` | (geen) | `vorige_instellingen` aanwezig → aangetoond, `waarde` = lijst gewijzigde sleutels; anders geen bewijs |
| `geen_onverenigbare_rollen` | (geen) | leest `instellingen.onverenigbare_rollen` en `accounts`; geen account met beide rollen van een paar → aangetoond; anders niet aangetoond, `waarde` = ids. Lijst ontbreekt → geen bewijs |

Voorwaarden in `waar` (voor `lijst_leeg`), elk een object met één van deze vormen:
`{"veld": "type", "is": "leverancier"}` · `{"veld": "einddatum", "leeg": true}` ·
`{"veld": "lokaal_wachtwoord", "is": true}` · `{"veld": "rollen", "niet_leeg": true}` ·
`{"veld": "laatste_inlog", "ouder_dan_dagen": 90}` (ten opzichte van de peildatum die `toets_alles`
meekrijgt).

### Uitkomst van een regel

```json
{"regel": "8.15.01-velden", "maatregel": "8.15.01", "uitkomst": "gedeeltelijk",
 "waarde": 0.8, "toelichting": "4 van 5 logregels bevatten alle zes velden"}
```

### Uitkomst per maatregel (`uitkomst_maatregel`)

Soort D → `niet aantoonbaar`. Soort C zonder regels → `handmatig`. A/B met regels: de slechtste
regeluitkomst in de volgorde `niet aangetoond` < `geen bewijs` < `gedeeltelijk` < `aangetoond`, met
één uitzondering: zijn álle regels `geen bewijs`, dan `geen bewijs`. Een maatregel zonder regels maar
met soort A of B → `handmatig` (nog geen regel uitdrukbaar).

### Dossier (wat de pagina opslaat, F3)

```json
{
  "formaat": "applicatiecheck-dossier",
  "versie": 1,
  "bron_versie": "BIO2 v1.3 definitief - 9 januari 2026",
  "applicatie": {"naam": "…", "versie": "…", "organisatie": "…", "hosting": "saas", "sso": true},
  "peildatum": "2026-09-01",
  "ingevuld_door": "…",
  "bronbestanden": [{"naam": "…", "soort": "…", "sha256": "…"}],
  "maatregelen": [
    {"id": "8.15.01", "soort": ["B"], "uitkomst": "aangetoond",
     "regels": [{"regel": "8.15.01-velden", "uitkomst": "aangetoond", "waarde": 1.0, "toelichting": "…"}],
     "status": "aangetoond", "verantwoordelijke": "…", "onderbouwing": "",
     "bevestigd_door_mens": false}
  ]
}
```

`status` is de menselijke keuze per maatregel en start gelijk aan `uitkomst`; de gebruiker mag hem
zetten op `niet van toepassing` of `explain` met een `onderbouwing`. `uitkomst` blijft wat de regel zei.

De **tekst** van een maatregel staat niet in het dossier en niet in de pagina: alleen nummer, titel en
thema uit `bronnen/bio2.json`. Reden staat in deel 1 (CC BY-NC-SA). De pagina zet achter elke maatregel
een verwijzing naar de CIP-publicatie, geen citaat.

---

## F1 · Regels als data en de referentie-implementatie

### Taak 1: het feiten-schema en de validatie

**Files:**
- Create: `parsers/__init__.py` (leeg)
- Create: `parsers/feiten.py`
- Test: `tests/test_parsers.py`

**Interfaces:**
- Produces: `parsers.feiten.leeg() -> dict` (een geldig, leeg feiten-object) en
  `parsers.feiten.valideer(feiten: dict) -> list[str]` (lijst fouten; leeg = geldig) en
  `parsers.feiten.sha256_van(bytes) -> str`.

- [ ] **Stap 1: schrijf de falende test**

```python
# tests/test_parsers.py
"""Parsers zetten aangeleverde bestanden om in één plat feiten-object; regels lezen alleen dat."""
from __future__ import annotations

import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
FIX = ROOT / "tests" / "fixtures"

from parsers import feiten  # noqa: E402


def test_leeg_feiten_object_is_geldig():
    f = feiten.leeg()
    assert f["formaat"] == "applicatiecheck-feiten" and f["versie"] == 1
    assert feiten.valideer(f) == []


def test_validatie_meldt_ontbrekende_kop_en_verkeerde_types():
    f = feiten.leeg()
    del f["formaat"]
    f["accounts"] = "geen lijst"
    fouten = feiten.valideer(f)
    assert any("formaat" in x for x in fouten)
    assert any("accounts" in x for x in fouten)


def test_validatie_eist_tijdzone_in_tijdstippen():
    f = feiten.leeg()
    f["logregels"] = [{"tijdstip": "2026-09-01T10:00:00", "identiteit": "u1", "actie": "a",
                       "object": "o", "resultaat": "ok", "oorsprong": "x"}]
    assert any("tijdzone" in x for x in feiten.valideer(f))
    f["logregels"][0]["tijdstip"] = "2026-09-01T10:00:00+02:00"
    assert feiten.valideer(f) == []


def test_sha256_van_bytes():
    assert feiten.sha256_van(b"abc") == "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"
```

- [ ] **Stap 2: draai de test, verwacht rood**

Run: `python -m pytest tests/test_parsers.py -v`
Verwacht: FAIL, `ModuleNotFoundError: No module named 'parsers'`

- [ ] **Stap 3: schrijf de implementatie**

```python
# parsers/__init__.py
"""Parsers: van aangeleverd bestand naar het feiten-object dat de regels lezen."""
```

```python
# parsers/feiten.py
"""Het feiten-object: de enige vorm waar regels op werken.

Een parser vult dit object; een regel leest het. Wat hier niet in staat, bestaat voor een regel niet,
en dan is de uitkomst 'geen bewijs' en nooit een aanname. Alle tijdstippen zijn ISO 8601 met tijdzone.
"""
from __future__ import annotations

import datetime as dt
import hashlib

FORMAAT = "applicatiecheck-feiten"
VERSIE = 1
LIJSTEN = ("bronbestanden", "accounts", "rollen", "logtypen", "logregels", "koppelingen")
LOGVELDEN = ("tijdstip", "identiteit", "actie", "object", "resultaat", "oorsprong")
ACCOUNTTYPEN = ("persoon", "leverancier", "service")


def leeg() -> dict:
    """Een geldig feiten-object zonder inhoud."""
    f = {"formaat": FORMAAT, "versie": VERSIE, "applicatie": {"naam": "", "versie": ""},
         "instellingen": {}, "vorige_instellingen": None}
    for naam in LIJSTEN:
        f[naam] = []
    return f


def sha256_van(inhoud: bytes) -> str:
    return hashlib.sha256(inhoud).hexdigest()


def tijdstip_geldig(tekst) -> bool:
    """ISO 8601 met tijdzone; zonder tijdzone is een tijdstip niet vergelijkbaar en dus ongeldig."""
    if not isinstance(tekst, str):
        return False
    try:
        waarde = dt.datetime.fromisoformat(tekst.replace("Z", "+00:00"))
    except ValueError:
        return False
    return waarde.tzinfo is not None


def valideer(f: dict) -> list[str]:
    """Lijst van fouten; leeg betekent geldig. Meldt alles tegelijk, niet alleen de eerste."""
    fouten: list[str] = []
    if f.get("formaat") != FORMAAT:
        fouten.append(f"formaat moet '{FORMAAT}' zijn")
    if f.get("versie") != VERSIE:
        fouten.append(f"versie moet {VERSIE} zijn")
    if not isinstance(f.get("instellingen"), dict):
        fouten.append("instellingen moet een object zijn")
    if f.get("vorige_instellingen") is not None and not isinstance(f["vorige_instellingen"], dict):
        fouten.append("vorige_instellingen moet null of een object zijn")
    for naam in LIJSTEN:
        if not isinstance(f.get(naam), list):
            fouten.append(f"{naam} moet een lijst zijn")
    if isinstance(f.get("logregels"), list):
        for i, regel in enumerate(f["logregels"]):
            if not isinstance(regel, dict):
                fouten.append(f"logregels[{i}] moet een object zijn")
                continue
            if "tijdstip" in regel and regel["tijdstip"] not in ("", None) \
                    and not tijdstip_geldig(regel["tijdstip"]):
                fouten.append(f"logregels[{i}].tijdstip is geen ISO 8601 met tijdzone")
    if isinstance(f.get("accounts"), list):
        for i, acc in enumerate(f["accounts"]):
            if isinstance(acc, dict) and acc.get("type") not in ACCOUNTTYPEN:
                fouten.append(f"accounts[{i}].type moet een van {ACCOUNTTYPEN} zijn")
    return fouten
```

- [ ] **Stap 4: draai de test, verwacht groen**

Run: `python -m pytest tests/test_parsers.py -v`
Verwacht: 4 passed

- [ ] **Stap 5: commit**

```bash
git add parsers/__init__.py parsers/feiten.py tests/test_parsers.py
git commit -m "parsers: feiten-schema met validatie"
```

### Taak 2: patronen voor `geen_patroon` (minimale versie; F2 breidt uit)

**Files:**
- Create: `patronen.py`
- Test: `tests/test_patronen.py`

**Interfaces:**
- Produces: `patronen.PATRONEN: dict[str, callable]` met sleutels `bsn`, `iban`, `email`, `telefoon`,
  `wachtwoord`; elke callable neemt een `str` en geeft een `list[str]` treffers. En
  `patronen.zoek(tekst: str, namen: list[str]) -> dict[str, list[str]]`.

- [ ] **Stap 1: schrijf de falende test**

```python
# tests/test_patronen.py
"""De deterministische PII-patronen: wat er nooit in een log mag staan."""
from __future__ import annotations

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import patronen  # noqa: E402


def test_bsn_alleen_met_geldige_elfproef():
    assert patronen.PATRONEN["bsn"]("bsn 111222333 en 123456789") == ["111222333"]
    assert patronen.PATRONEN["bsn"]("versie 1234567890") == []


def test_iban_nl():
    assert patronen.PATRONEN["iban"]("betaal naar NL91ABNA0417164300 aub") == ["NL91ABNA0417164300"]


def test_email_en_telefoon():
    assert patronen.PATRONEN["email"]("mail a.b@voorbeeld.nl nu") == ["a.b@voorbeeld.nl"]
    assert patronen.PATRONEN["telefoon"]("bel 06-12345678 of 0711234567") == ["06-12345678", "0711234567"]


def test_wachtwoord_sleutelwoorden():
    assert patronen.PATRONEN["wachtwoord"]("password=geheim123") == ["password=geheim123"]
    assert patronen.PATRONEN["wachtwoord"]("wachtwoord gewijzigd door u1") == []


def test_zoek_bundelt_per_naam():
    uit = patronen.zoek("bsn 111222333, NL91ABNA0417164300", ["bsn", "iban"])
    assert uit == {"bsn": ["111222333"], "iban": ["NL91ABNA0417164300"]}
```

- [ ] **Stap 2: draai de test, verwacht rood**

Run: `python -m pytest tests/test_patronen.py -v`
Verwacht: FAIL, `ModuleNotFoundError: No module named 'patronen'`

- [ ] **Stap 3: schrijf de implementatie**

```python
# patronen.py
"""Deterministische patronen voor wat nooit in een log hoort: BSN, IBAN, e-mail, telefoon, wachtwoord.

Zelfde patronen als anonimizer-browser/src/lib/patronen.ts (daar in TypeScript); check/bron/patronen.js
is de spiegel voor de pagina. Een regel 'geen_patroon' telt treffers; elke treffer is een bevinding.
Alleen standaardbibliotheek.
"""
from __future__ import annotations

import re

_EMAIL = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")
_TELEFOON = re.compile(r"(?<!\w)(?:\+31[\s-]?\(?0?\)?|0)(?:[\s-]?\d){8,10}(?!\w)")
_IBAN_NL = re.compile(r"\bNL\d{2}\s?[A-Z]{4}\s?\d{4}\s?\d{4}\s?\d{2}\b")
_BSN_KANDIDAAT = re.compile(r"(?<!\d)(\d{9})(?!\d)")
# Sleutelwoord gevolgd door een scheidingsteken en een waarde: 'password=...', 'pwd: ...'.
_WACHTWOORD = re.compile(r"\b(?:password|passwd|pwd|wachtwoord|secret|token)\s*[:=]\s*\S+", re.I)


def is_geldig_bsn(nummer: str) -> bool:
    """Elfproef: som van cijfer maal gewicht (9..2, laatste -1) deelbaar door 11."""
    if len(nummer) != 9 or not nummer.isdigit() or nummer == "000000000":
        return False
    gewichten = [9, 8, 7, 6, 5, 4, 3, 2, -1]
    return sum(int(c) * g for c, g in zip(nummer, gewichten)) % 11 == 0


def _bsn(tekst: str) -> list[str]:
    return [m.group(1) for m in _BSN_KANDIDAAT.finditer(tekst) if is_geldig_bsn(m.group(1))]


PATRONEN = {
    "bsn": _bsn,
    "iban": lambda t: _IBAN_NL.findall(t),
    "email": lambda t: _EMAIL.findall(t),
    "telefoon": lambda t: [m.group(0) for m in _TELEFOON.finditer(t)],
    "wachtwoord": lambda t: _WACHTWOORD.findall(t),
}


def zoek(tekst: str, namen: list[str]) -> dict[str, list[str]]:
    """Treffers per patroonnaam; onbekende naam is een fout, geen stilte."""
    uit: dict[str, list[str]] = {}
    for naam in namen:
        if naam not in PATRONEN:
            raise KeyError(f"onbekend patroon: {naam}")
        uit[naam] = PATRONEN[naam](tekst)
    return uit
```

- [ ] **Stap 4: draai de test, verwacht groen**

Run: `python -m pytest tests/test_patronen.py -v`
Verwacht: 5 passed. (Faalt `test_bsn`: controleer dat `111222333` de elfproef haalt: 9+16+7+12+10+8+9+6-3 = 74? Nee: 1·9+1·8+1·7+2·6+2·5+2·4+3·3+3·2+3·(-1) = 9+8+7+12+10+8+9+6-3 = 66, 66 % 11 = 0, geldig.)

- [ ] **Stap 5: commit**

```bash
git add patronen.py tests/test_patronen.py
git commit -m "patronen: BSN, IBAN, e-mail, telefoon en wachtwoord als deterministische patronen"
```

### Taak 3: `regels.json` met de eerste regels, en de test die het schema bewaakt

**Files:**
- Create: `regels.json`
- Test: `tests/test_regels.py`

**Interfaces:**
- Produces: `regels.json` zoals in *De datamodellen*; regel-ids `8.15.01-velden`, `8.15.02-geen-pii`,
  `8.17.01-tijdstempels`, `5.17.01-sso`, `5.17.01-geen-lokale-wachtwoorden`, `5.18.01-inactieve-accounts`,
  `8.05.01-leveranciersaccounts`, `8.05.01-sessie-timeout`, `8.05.01-lockout`, `8.09.01-export-als-baseline`,
  `8.32.01-verschil`, `5.03.01-functiescheiding`.

- [ ] **Stap 1: schrijf de falende test**

```python
# tests/test_regels.py
"""regels.json: elke regel wijst naar een bestaande maatregel met soort A of B, en gebruikt een bekend toetstype."""
from __future__ import annotations

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
REGELS = json.loads((ROOT / "regels.json").read_text(encoding="utf-8"))
BEWIJS = {r["id"]: r for r in json.loads((ROOT / "bewijs.json").read_text(encoding="utf-8"))["maatregelen"]}

VERPLICHT = {"id", "maatregel", "soort", "naam", "eis", "toets"}


def test_kop():
    assert REGELS["formaat"] == "applicatiecheck-regels" and REGELS["versie"] == 1
    assert len(REGELS["regels"]) >= 12


def test_elke_regel_compleet_en_uniek():
    ids = [r["id"] for r in REGELS["regels"]]
    assert len(ids) == len(set(ids))
    for r in REGELS["regels"]:
        assert VERPLICHT <= set(r), r.get("id")
        assert r["id"].startswith(r["maatregel"] + "-"), r["id"]
        assert r["toets"]["type"] in REGELS["toetstypen"], r["id"]


def test_regel_past_bij_bewijs_json():
    for r in REGELS["regels"]:
        m = BEWIJS[r["maatregel"]]
        assert r["soort"] in m["soort"], f"{r['id']}: bewijs.json zegt {m['soort']}"
        assert r["soort"] in ("A", "B"), r["id"]


def test_toetsvelden_per_type():
    nodig = {
        "velden_aanwezig": {"over", "velden", "drempel"}, "geen_patroon": {"over", "patronen"},
        "tijdstempel_geldig": {"over", "veld", "drempel"}, "waarde_gelijk": {"pad", "waarde"},
        "waarde_minimaal": {"pad", "waarde"}, "waarde_maximaal": {"pad", "waarde"},
        "lijst_leeg": {"over", "waar"}, "bron_aanwezig": {"soort"},
        "verschil_met_vorige": set(), "geen_onverenigbare_rollen": set(),
    }
    for r in REGELS["regels"]:
        t = r["toets"]
        assert nodig[t["type"]] <= set(t), r["id"]
```

- [ ] **Stap 2: draai de test, verwacht rood**

Run: `python -m pytest tests/test_regels.py -v`
Verwacht: FAIL, `FileNotFoundError: regels.json`

- [ ] **Stap 3: schrijf `regels.json`**

```json
{
  "formaat": "applicatiecheck-regels",
  "versie": 1,
  "toelichting": "Regels als data. Een regel toetst feiten (parsers/feiten.py), nooit een ruw bestand. De betekenis van elk toetstype staat in toets.py en in het bouwplan.",
  "toetstypen": ["velden_aanwezig", "geen_patroon", "tijdstempel_geldig", "waarde_gelijk", "waarde_minimaal", "waarde_maximaal", "lijst_leeg", "bron_aanwezig", "verschil_met_vorige", "geen_onverenigbare_rollen"],
  "regels": [
    {"id": "8.15.01-velden", "maatregel": "8.15.01", "soort": "B", "naam": "Logregel bevat de zes velden",
     "eis": "Elke logregel bevat tijdstip, identiteit, actie, object, resultaat en oorsprong.",
     "toets": {"type": "velden_aanwezig", "over": "logregels", "velden": ["tijdstip", "identiteit", "actie", "object", "resultaat", "oorsprong"], "drempel": 1.0}},
    {"id": "8.15.02-geen-pii", "maatregel": "8.15.02", "soort": "B", "naam": "Geen gevoelige gegevens in de log",
     "eis": "Een logregel bevat geen wachtwoorden, tokens, burgerservicenummers of rekeningnummers.",
     "toets": {"type": "geen_patroon", "over": "logregels", "patronen": ["bsn", "iban", "wachtwoord"]}},
    {"id": "8.17.01-tijdstempels", "maatregel": "8.17.01", "soort": "B", "naam": "Tijdstempels bruikbaar en in volgorde",
     "eis": "Elke logregel heeft een tijdstempel met tijdzone en de regels staan in tijdsvolgorde.",
     "toets": {"type": "tijdstempel_geldig", "over": "logregels", "veld": "tijdstip", "drempel": 0.99}},
    {"id": "5.17.01-sso", "maatregel": "5.17.01", "soort": "A", "naam": "Inloggen alleen via de identity provider",
     "eis": "SSO is afgedwongen; de applicatie accepteert geen inlog buiten de identity provider om.",
     "toets": {"type": "waarde_gelijk", "pad": "instellingen.sso_afgedwongen", "waarde": true}},
    {"id": "5.17.01-geen-lokale-wachtwoorden", "maatregel": "5.17.01", "soort": "A", "naam": "Geen persoonsaccounts met lokaal wachtwoord",
     "eis": "Geen enkel persoonsaccount heeft een lokaal wachtwoord.",
     "toets": {"type": "lijst_leeg", "over": "accounts", "waar": [{"veld": "type", "is": "persoon"}, {"veld": "lokaal_wachtwoord", "is": true}]}},
    {"id": "5.18.01-inactieve-accounts", "maatregel": "5.18.01", "soort": "A", "naam": "Geen inactieve accounts met rechten",
     "eis": "Geen account met rollen is langer dan 90 dagen niet ingelogd.",
     "toets": {"type": "lijst_leeg", "over": "accounts", "waar": [{"veld": "rollen", "niet_leeg": true}, {"veld": "laatste_inlog", "ouder_dan_dagen": 90}]}},
    {"id": "8.05.01-leveranciersaccounts", "maatregel": "8.05.01", "soort": "A", "naam": "Leveranciersaccounts hebben een einddatum",
     "eis": "Elk leveranciersaccount heeft een einddatum.",
     "toets": {"type": "lijst_leeg", "over": "accounts", "waar": [{"veld": "type", "is": "leverancier"}, {"veld": "einddatum", "leeg": true}]}},
    {"id": "8.05.01-sessie-timeout", "maatregel": "8.05.01", "soort": "A", "naam": "Sessie verloopt bij inactiviteit",
     "eis": "Een sessie wordt na ten hoogste 30 minuten inactiviteit beëindigd.",
     "toets": {"type": "waarde_maximaal", "pad": "instellingen.sessie_timeout_minuten", "waarde": 30}},
    {"id": "8.05.01-lockout", "maatregel": "8.05.01", "soort": "A", "naam": "Lockout na mislukte pogingen",
     "eis": "Na ten hoogste 10 mislukte inlogpogingen wordt het account of de bron geblokkeerd.",
     "toets": {"type": "waarde_maximaal", "pad": "instellingen.lockout_pogingen", "waarde": 10}},
    {"id": "8.09.01-export-als-baseline", "maatregel": "8.09.01", "soort": "A", "naam": "De configuratie is vastgelegd",
     "eis": "Er is een configuratie-export met hash en peildatum; dat is de baseline.",
     "toets": {"type": "bron_aanwezig", "soort": "configuratie"}},
    {"id": "8.32.01-verschil", "maatregel": "8.32.01", "soort": "A", "naam": "Wijzigingen sinds de vorige export zijn zichtbaar",
     "eis": "Het verschil tussen de huidige en de vorige configuratie-export is vastgesteld.",
     "toets": {"type": "verschil_met_vorige"}},
    {"id": "5.03.01-functiescheiding", "maatregel": "5.03.01", "soort": "A", "naam": "Geen account met onverenigbare rollen",
     "eis": "Geen account heeft twee rollen die als onverenigbaar zijn aangemerkt.",
     "toets": {"type": "geen_onverenigbare_rollen"}}
  ]
}
```

- [ ] **Stap 4: draai de test, verwacht groen**

Run: `python -m pytest tests/test_regels.py -v`
Verwacht: 4 passed. Faalt `test_regel_past_bij_bewijs_json` op `5.17.01`: controleer in `bewijs.json` dat
`5.17.01` soort `["A", "C"]` heeft (F0 heeft dat zo gezet); de regel is soort A, dat past.

- [ ] **Stap 5: commit**

```bash
git add regels.json tests/test_regels.py
git commit -m "regels: eerste twaalf regels als data, met schema-test"
```

### Taak 4: `toets.py`, de referentie-implementatie

**Files:**
- Create: `toets.py`
- Test: `tests/test_toets.py`

**Interfaces:**
- Consumes: `patronen.zoek`, `parsers.feiten.tijdstip_geldig`.
- Produces: `toets.toets_regel(regel: dict, feiten: dict, peildatum: str) -> dict`,
  `toets.toets_alles(regels: dict, feiten: dict, peildatum: str) -> list[dict]`,
  `toets.uitkomst_maatregel(soort: list[str], regeluitkomsten: list[dict]) -> str`,
  `toets.dossier_uitkomsten(bewijs: dict, regels: dict, feiten: dict, peildatum: str) -> dict[str, dict]`
  (per maatregel-id: `{"soort", "uitkomst", "regels"}`). Constanten `UITKOMSTEN` en `SPIEGEL` (de namen
  die `app.js` moet spiegelen).

- [ ] **Stap 1: schrijf de falende test**

```python
# tests/test_toets.py
"""De toetstypen, los van de pagina. app.js spiegelt deze functies onder dezelfde namen."""
from __future__ import annotations

import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import toets  # noqa: E402
from parsers import feiten as F  # noqa: E402

PEIL = "2026-09-01"


def basis() -> dict:
    f = F.leeg()
    f["bronbestanden"] = [{"naam": "export.json", "soort": "configuratie", "sha256": "0" * 64, "peildatum": PEIL}]
    f["instellingen"] = {"sso_afgedwongen": True, "sessie_timeout_minuten": 15, "lockout_pogingen": 5,
                         "onverenigbare_rollen": [["aanvrager", "goedkeurder"]]}
    f["accounts"] = [
        {"id": "u1", "type": "persoon", "rollen": ["beheerder"], "lokaal_wachtwoord": False,
         "laatste_inlog": "2026-08-30T09:00:00+02:00", "einddatum": None},
        {"id": "u2", "type": "persoon", "rollen": ["aanvrager"], "lokaal_wachtwoord": False,
         "laatste_inlog": "2026-03-01T09:00:00+02:00", "einddatum": None},
        {"id": "lev1", "type": "leverancier", "rollen": ["beheerder"], "lokaal_wachtwoord": True,
         "laatste_inlog": "2026-08-30T09:00:00+02:00", "einddatum": None},
    ]
    f["logregels"] = [
        {"tijdstip": "2026-09-01T10:00:00+02:00", "identiteit": "u1", "actie": "wijzig",
         "object": "zaak/1", "resultaat": "ok", "oorsprong": "10.0.0.5"},
        {"tijdstip": "2026-09-01T10:01:00+02:00", "identiteit": "u1", "actie": "lees",
         "object": "zaak/2", "resultaat": "ok", "oorsprong": ""},
    ]
    return f


def regel(type_, **velden):
    return {"id": "t", "maatregel": "8.15.01", "soort": "B", "naam": "t", "eis": "t",
            "toets": {"type": type_, **velden}}


def test_velden_aanwezig_gedeeltelijk_en_geen_bewijs():
    f = basis()
    r = regel("velden_aanwezig", over="logregels", velden=list(F.LOGVELDEN), drempel=1.0)
    uit = toets.toets_regel(r, f, PEIL)
    assert uit["uitkomst"] == "gedeeltelijk" and uit["waarde"] == 0.5
    f["logregels"] = []
    assert toets.toets_regel(r, f, PEIL)["uitkomst"] == "geen bewijs"


def test_geen_patroon_telt_treffers():
    f = basis()
    f["logregels"][1]["object"] = "bsn 111222333"
    uit = toets.toets_regel(regel("geen_patroon", over="logregels", patronen=["bsn", "iban"]), f, PEIL)
    assert uit["uitkomst"] == "niet aangetoond" and uit["waarde"] == {"bsn": 1, "iban": 0}


def test_tijdstempel_geldig_eist_tijdzone_en_volgorde():
    f = basis()
    r = regel("tijdstempel_geldig", over="logregels", veld="tijdstip", drempel=0.99)
    assert toets.toets_regel(r, f, PEIL)["uitkomst"] == "aangetoond"
    f["logregels"][1]["tijdstip"] = "2026-09-01T09:00:00+02:00"   # eerder dan de vorige
    assert toets.toets_regel(r, f, PEIL)["uitkomst"] == "gedeeltelijk"
    f["logregels"][1]["tijdstip"] = "2026-09-01T11:00:00"          # geen tijdzone
    assert toets.toets_regel(r, f, PEIL)["uitkomst"] == "gedeeltelijk"


def test_waarde_gelijk_minimaal_maximaal_en_ontbrekend_pad():
    f = basis()
    assert toets.toets_regel(regel("waarde_gelijk", pad="instellingen.sso_afgedwongen", waarde=True), f, PEIL)["uitkomst"] == "aangetoond"
    assert toets.toets_regel(regel("waarde_maximaal", pad="instellingen.sessie_timeout_minuten", waarde=10), f, PEIL)["uitkomst"] == "niet aangetoond"
    assert toets.toets_regel(regel("waarde_minimaal", pad="instellingen.lockout_pogingen", waarde=3), f, PEIL)["uitkomst"] == "aangetoond"
    assert toets.toets_regel(regel("waarde_gelijk", pad="instellingen.bestaat_niet", waarde=1), f, PEIL)["uitkomst"] == "geen bewijs"


def test_lijst_leeg_met_voorwaarden():
    f = basis()
    r = regel("lijst_leeg", over="accounts", waar=[{"veld": "rollen", "niet_leeg": True},
                                                  {"veld": "laatste_inlog", "ouder_dan_dagen": 90}])
    uit = toets.toets_regel(r, f, PEIL)
    assert uit["uitkomst"] == "niet aangetoond" and uit["waarde"] == ["u2"]
    r2 = regel("lijst_leeg", over="accounts", waar=[{"veld": "type", "is": "leverancier"}, {"veld": "einddatum", "leeg": True}])
    assert toets.toets_regel(r2, f, PEIL)["waarde"] == ["lev1"]
    r3 = regel("lijst_leeg", over="accounts", waar=[{"veld": "type", "is": "service"}])
    assert toets.toets_regel(r3, f, PEIL)["uitkomst"] == "aangetoond"


def test_bron_aanwezig_en_verschil_met_vorige():
    f = basis()
    assert toets.toets_regel(regel("bron_aanwezig", soort="configuratie"), f, PEIL)["uitkomst"] == "aangetoond"
    assert toets.toets_regel(regel("bron_aanwezig", soort="log"), f, PEIL)["uitkomst"] == "geen bewijs"
    assert toets.toets_regel(regel("verschil_met_vorige"), f, PEIL)["uitkomst"] == "geen bewijs"
    f["vorige_instellingen"] = dict(f["instellingen"], sessie_timeout_minuten=60, extra="x")
    uit = toets.toets_regel(regel("verschil_met_vorige"), f, PEIL)
    assert uit["uitkomst"] == "aangetoond" and uit["waarde"] == ["extra", "sessie_timeout_minuten"]


def test_geen_onverenigbare_rollen():
    f = basis()
    assert toets.toets_regel(regel("geen_onverenigbare_rollen"), f, PEIL)["uitkomst"] == "aangetoond"
    f["accounts"][1]["rollen"] = ["aanvrager", "goedkeurder"]
    uit = toets.toets_regel(regel("geen_onverenigbare_rollen"), f, PEIL)
    assert uit["uitkomst"] == "niet aangetoond" and uit["waarde"] == ["u2"]
    del f["instellingen"]["onverenigbare_rollen"]
    assert toets.toets_regel(regel("geen_onverenigbare_rollen"), f, PEIL)["uitkomst"] == "geen bewijs"


def test_uitkomst_maatregel_neemt_de_slechtste():
    u = lambda x: {"uitkomst": x}
    assert toets.uitkomst_maatregel(["D"], []) == "niet aantoonbaar"
    assert toets.uitkomst_maatregel(["C"], []) == "handmatig"
    assert toets.uitkomst_maatregel(["A"], []) == "handmatig"
    assert toets.uitkomst_maatregel(["A"], [u("aangetoond"), u("gedeeltelijk")]) == "gedeeltelijk"
    assert toets.uitkomst_maatregel(["A"], [u("aangetoond"), u("niet aangetoond")]) == "niet aangetoond"
    assert toets.uitkomst_maatregel(["A"], [u("geen bewijs"), u("geen bewijs")]) == "geen bewijs"
    assert toets.uitkomst_maatregel(["A"], [u("geen bewijs"), u("aangetoond")]) == "geen bewijs"


def test_dossier_uitkomsten_dekt_alle_148():
    bewijs = json.loads((ROOT / "bewijs.json").read_text(encoding="utf-8"))
    regels = json.loads((ROOT / "regels.json").read_text(encoding="utf-8"))
    uit = toets.dossier_uitkomsten(bewijs, regels, basis(), PEIL)
    assert len(uit) == 148
    assert uit["8.15.01"]["uitkomst"] == "gedeeltelijk"
    assert uit["5.01.01"]["uitkomst"] == "niet aantoonbaar"
    assert uit["8.15.03"]["uitkomst"] == "handmatig"       # A zonder regel


def test_spiegel_bevat_de_publieke_functies():
    assert set(toets.SPIEGEL) == {"toets_regel", "toets_alles", "uitkomst_maatregel", "dossier_uitkomsten"}
```

- [ ] **Stap 2: draai de test, verwacht rood**

Run: `python -m pytest tests/test_toets.py -v`
Verwacht: FAIL, `ModuleNotFoundError: No module named 'toets'`

- [ ] **Stap 3: schrijf de implementatie**

```python
# toets.py
#!/usr/bin/env python3
"""De toetstypen van applicatiecheck, los van de pagina.

Dit is de referentie: check/bron/app.js heeft dezelfde functies onder dezelfde namen in het object
`toets`, en de browsertests vergelijken wat op het scherm staat met wat hier uitkomt. Een regel toetst
alleen feiten (parsers/feiten.py); ontbreekt het feit, dan is de uitkomst 'geen bewijs' en nooit een
aanname. Alleen standaardbibliotheek.
"""
from __future__ import annotations

import datetime as dt
import json

import patronen
from parsers import feiten as F

UITKOMSTEN = ("aangetoond", "gedeeltelijk", "niet aangetoond", "geen bewijs",
              "handmatig", "niet aantoonbaar", "niet van toepassing")
# Van slecht naar goed; uitkomst_maatregel neemt de laagste.
RANG = {"niet aangetoond": 0, "geen bewijs": 1, "gedeeltelijk": 2, "aangetoond": 3}
SPIEGEL = ("toets_regel", "toets_alles", "uitkomst_maatregel", "dossier_uitkomsten")


def _uit(regel: dict, uitkomst: str, waarde=None, toelichting: str = "") -> dict:
    return {"regel": regel["id"], "maatregel": regel["maatregel"], "uitkomst": uitkomst,
            "waarde": waarde, "toelichting": toelichting}


def _pad(feiten: dict, pad: str):
    """'instellingen.sso_afgedwongen' -> de waarde, of None als een stap ontbreekt."""
    huidig = feiten
    for stap in pad.split("."):
        if not isinstance(huidig, dict) or stap not in huidig:
            return None
        huidig = huidig[stap]
    return huidig


def _leeg(waarde) -> bool:
    return waarde is None or waarde == "" or waarde == [] or waarde == {}


def _dagen_oud(tijdstip: str, peildatum: str) -> float | None:
    if not F.tijdstip_geldig(tijdstip):
        return None
    peil = dt.datetime.fromisoformat(peildatum + "T00:00:00+00:00")
    moment = dt.datetime.fromisoformat(tijdstip.replace("Z", "+00:00"))
    return (peil - moment).total_seconds() / 86400


def _voldoet(record: dict, voorwaarde: dict, peildatum: str) -> bool:
    waarde = record.get(voorwaarde["veld"])
    if "is" in voorwaarde:
        return waarde == voorwaarde["is"]
    if "leeg" in voorwaarde:
        return _leeg(waarde) == voorwaarde["leeg"]
    if "niet_leeg" in voorwaarde:
        return (not _leeg(waarde)) == voorwaarde["niet_leeg"]
    if "ouder_dan_dagen" in voorwaarde:
        oud = _dagen_oud(waarde, peildatum) if isinstance(waarde, str) else None
        return oud is not None and oud > voorwaarde["ouder_dan_dagen"]
    raise ValueError(f"onbekende voorwaarde: {voorwaarde}")


def _drempel(regel: dict, aandeel: float, toelichting: str) -> dict:
    drempel = regel["toets"]["drempel"]
    if aandeel >= drempel:
        return _uit(regel, "aangetoond", aandeel, toelichting)
    if aandeel > 0:
        return _uit(regel, "gedeeltelijk", aandeel, toelichting)
    return _uit(regel, "niet aangetoond", aandeel, toelichting)


def toets_regel(regel: dict, feiten: dict, peildatum: str) -> dict:
    t = regel["toets"]
    soort = t["type"]

    if soort == "velden_aanwezig":
        records = feiten.get(t["over"]) or []
        if not records:
            return _uit(regel, "geen bewijs", None, f"geen {t['over']} aangeleverd")
        goed = sum(1 for r in records if all(not _leeg(r.get(v)) for v in t["velden"]))
        aandeel = round(goed / len(records), 4)
        return _drempel(regel, aandeel, f"{goed} van {len(records)} records bevatten alle velden")

    if soort == "geen_patroon":
        records = feiten.get(t["over"]) or []
        if not records:
            return _uit(regel, "geen bewijs", None, f"geen {t['over']} aangeleverd")
        telling = {naam: 0 for naam in t["patronen"]}
        for r in records:
            tekst = " ".join(str(v) for v in r.values() if isinstance(v, (str, int)))
            for naam, treffers in patronen.zoek(tekst, t["patronen"]).items():
                telling[naam] += len(treffers)
        totaal = sum(telling.values())
        if totaal == 0:
            return _uit(regel, "aangetoond", telling, "geen treffers")
        return _uit(regel, "niet aangetoond", telling, f"{totaal} treffer(s)")

    if soort == "tijdstempel_geldig":
        records = feiten.get(t["over"]) or []
        if not records:
            return _uit(regel, "geen bewijs", None, f"geen {t['over']} aangeleverd")
        goed, vorige = 0, None
        for r in records:
            tekst = r.get(t["veld"])
            if not F.tijdstip_geldig(tekst):
                continue
            moment = dt.datetime.fromisoformat(tekst.replace("Z", "+00:00"))
            if vorige is None or moment >= vorige:
                goed += 1
            vorige = moment
        aandeel = round(goed / len(records), 4)
        return _drempel(regel, aandeel, f"{goed} van {len(records)} tijdstempels geldig en in volgorde")

    if soort in ("waarde_gelijk", "waarde_minimaal", "waarde_maximaal"):
        waarde = _pad(feiten, t["pad"])
        if waarde is None:
            return _uit(regel, "geen bewijs", None, f"{t['pad']} ontbreekt")
        if soort == "waarde_gelijk":
            ok = waarde == t["waarde"]
        elif soort == "waarde_minimaal":
            ok = isinstance(waarde, (int, float)) and waarde >= t["waarde"]
        else:
            ok = isinstance(waarde, (int, float)) and waarde <= t["waarde"]
        # json.dumps in plaats van !r: dan schrijven Python en JS allebei true/"tekst" in de toelichting.
        return _uit(regel, "aangetoond" if ok else "niet aangetoond", waarde,
                    f"{t['pad']} = {json.dumps(waarde, ensure_ascii=False)}, eis {soort.split('_')[1]} "
                    f"{json.dumps(t['waarde'], ensure_ascii=False)}")

    if soort == "lijst_leeg":
        records = feiten.get(t["over"])
        if records is None or records == []:
            return _uit(regel, "geen bewijs", None, f"geen {t['over']} aangeleverd")
        ids = [r.get("id", "?") for r in records if all(_voldoet(r, w, peildatum) for w in t["waar"])]
        if not ids:
            return _uit(regel, "aangetoond", [], "geen records voldoen aan de voorwaarden")
        return _uit(regel, "niet aangetoond", ids, f"{len(ids)} record(s): {', '.join(ids)}")

    if soort == "bron_aanwezig":
        bronnen = [b for b in feiten.get("bronbestanden", []) if b.get("soort") == t["soort"]]
        if not bronnen:
            return _uit(regel, "geen bewijs", None, f"geen bronbestand van soort {t['soort']}")
        return _uit(regel, "aangetoond", [b["sha256"] for b in bronnen],
                    f"{len(bronnen)} bestand(en) van soort {t['soort']}")

    if soort == "verschil_met_vorige":
        vorige = feiten.get("vorige_instellingen")
        if not isinstance(vorige, dict):
            return _uit(regel, "geen bewijs", None, "geen vorige export aangeleverd")
        huidig = feiten.get("instellingen", {})
        gewijzigd = sorted(k for k in set(huidig) | set(vorige) if huidig.get(k) != vorige.get(k))
        return _uit(regel, "aangetoond", gewijzigd, f"{len(gewijzigd)} sleutel(s) gewijzigd")

    if soort == "geen_onverenigbare_rollen":
        paren = _pad(feiten, "instellingen.onverenigbare_rollen")
        if not paren:
            return _uit(regel, "geen bewijs", None, "geen lijst van onverenigbare rollen ingevoerd")
        records = feiten.get("accounts") or []
        if not records:
            return _uit(regel, "geen bewijs", None, "geen accounts aangeleverd")
        ids = [r.get("id", "?") for r in records
               if any(set(paar) <= set(r.get("rollen", [])) for paar in paren)]
        if not ids:
            return _uit(regel, "aangetoond", [], "geen account met een onverenigbaar paar")
        return _uit(regel, "niet aangetoond", ids, f"{len(ids)} account(s): {', '.join(ids)}")

    raise ValueError(f"onbekend toetstype: {soort}")


def toets_alles(regels: dict, feiten: dict, peildatum: str) -> list[dict]:
    return [toets_regel(r, feiten, peildatum) for r in regels["regels"]]


def uitkomst_maatregel(soort: list[str], regeluitkomsten: list[dict]) -> str:
    eerste = soort[0]
    if eerste == "D":
        return "niet aantoonbaar"
    if not regeluitkomsten:
        return "handmatig"
    uitkomsten = [u["uitkomst"] for u in regeluitkomsten]
    if all(u == "geen bewijs" for u in uitkomsten):
        return "geen bewijs"
    return min(uitkomsten, key=lambda u: RANG[u])


def dossier_uitkomsten(bewijs: dict, regels: dict, feiten: dict, peildatum: str) -> dict[str, dict]:
    per_maatregel: dict[str, list[dict]] = {}
    for u in toets_alles(regels, feiten, peildatum):
        per_maatregel.setdefault(u["maatregel"], []).append(u)
    uit = {}
    for m in bewijs["maatregelen"]:
        lijst = per_maatregel.get(m["id"], [])
        uit[m["id"]] = {"soort": m["soort"], "uitkomst": uitkomst_maatregel(m["soort"], lijst), "regels": lijst}
    return uit
```

- [ ] **Stap 4: draai alle tests, verwacht groen**

Run: `python -m pytest tests/ -v`
Verwacht: alles passed (7 uit F0 + 4 + 5 + 4 + 10).

- [ ] **Stap 5: commit**

```bash
git add toets.py tests/test_toets.py
git commit -m "toets: referentie-implementatie van de tien toetstypen"
```

### Taak 5: de generieke parser (JSON-feiten en CSV-log met kolomkoppeling) plus fixtures

**Files:**
- Create: `parsers/generiek.py`
- Create: `tests/fixtures/generiek-config.json`, `tests/fixtures/generiek-log.csv`,
  `tests/fixtures/generiek-log.kolommen.json`, `tests/fixtures/feiten-verwacht.json`
- Modify: `tests/test_parsers.py` (tests toevoegen onderaan)

**Interfaces:**
- Consumes: `parsers.feiten.leeg`, `valideer`, `sha256_van`.
- Produces: `parsers.generiek.lees_config_json(naam: str, inhoud: bytes, peildatum: str, feiten: dict) -> dict`
  (voegt `instellingen`, `accounts`, `rollen`, `logtypen`, `koppelingen`, `applicatie` toe en registreert
  het bronbestand), `parsers.generiek.lees_log_csv(naam: str, inhoud: bytes, kolommen: dict, peildatum: str, feiten: dict) -> dict`
  (voegt `logregels` toe). `kolommen` koppelt de zes logvelden aan kolomkoppen:
  `{"tijdstip": "Datum", "identiteit": "Gebruiker", ...}`; het scheidingsteken wordt geraden uit `,`, `;`, tab.

- [ ] **Stap 1: maak de fixtures**

`tests/fixtures/generiek-config.json` (verzonnen, geen echte export):

```json
{
  "applicatie": {"naam": "Voorbeeld Zaaksysteem", "versie": "6.21"},
  "instellingen": {"sso_afgedwongen": true, "sessie_timeout_minuten": 15, "lockout_pogingen": 5,
                   "https_only": true, "geen_terugval": true,
                   "onverenigbare_rollen": [["aanvrager", "goedkeurder"]]},
  "accounts": [
    {"id": "u1", "type": "persoon", "rollen": ["beheerder"], "lokaal_wachtwoord": false, "laatste_inlog": "2026-08-30T09:00:00+02:00", "einddatum": null},
    {"id": "u2", "type": "persoon", "rollen": ["aanvrager", "goedkeurder"], "lokaal_wachtwoord": false, "laatste_inlog": "2026-02-01T09:00:00+02:00", "einddatum": null},
    {"id": "lev1", "type": "leverancier", "rollen": ["beheerder"], "lokaal_wachtwoord": true, "laatste_inlog": "2026-08-30T09:00:00+02:00", "einddatum": null}
  ],
  "rollen": [{"id": "beheerder", "beheer": true}, {"id": "aanvrager", "beheer": false}, {"id": "goedkeurder", "beheer": false}],
  "logtypen": [{"naam": "audit", "aan": true, "retentie_dagen": 1095}],
  "koppelingen": [{"naam": "ZGW", "authenticatie": "oauth2", "versleuteld": true}]
}
```

`tests/fixtures/generiek-log.csv`:

```
Datum;Gebruiker;Actie;Object;Resultaat;IP
2026-09-01T10:00:00+02:00;u1;wijzig;zaak/1;ok;10.0.0.5
2026-09-01T10:01:00+02:00;u1;lees;zaak/2;ok;
2026-09-01T10:02:00+02:00;u2;wijzig;zaak/3 bsn 111222333;ok;10.0.0.7
```

`tests/fixtures/generiek-log.kolommen.json`:

```json
{"tijdstip": "Datum", "identiteit": "Gebruiker", "actie": "Actie", "object": "Object", "resultaat": "Resultaat", "oorsprong": "IP"}
```

`tests/fixtures/feiten-verwacht.json`: het volledige feiten-object dat uit de twee bovenstaande moet
komen. Maak hem zo: kopieer `generiek-config.json`, zet er `"formaat": "applicatiecheck-feiten"`,
`"versie": 1`, `"vorige_instellingen": null` bij, en `"logregels"` met de drie regels als objecten met de
zes veldnamen (`oorsprong` van regel 2 is `""`), en `"bronbestanden"` met twee entries waarvan je de
`sha256` leeg laat (`""`); de test vult hem in vóór het vergelijken.

- [ ] **Stap 2: schrijf de falende tests (onderaan `tests/test_parsers.py`)**

```python
from parsers import generiek  # noqa: E402


def _verwacht_met_hashes() -> dict:
    v = json.loads((FIX / "feiten-verwacht.json").read_text(encoding="utf-8"))
    for b in v["bronbestanden"]:
        b["sha256"] = feiten.sha256_van((FIX / b["naam"]).read_bytes())
    return v


def test_generieke_parser_maakt_de_verwachte_feiten():
    f = feiten.leeg()
    f = generiek.lees_config_json("generiek-config.json", (FIX / "generiek-config.json").read_bytes(), "2026-09-01", f)
    kol = json.loads((FIX / "generiek-log.kolommen.json").read_text(encoding="utf-8"))
    f = generiek.lees_log_csv("generiek-log.csv", (FIX / "generiek-log.csv").read_bytes(), kol, "2026-09-01", f)
    assert feiten.valideer(f) == []
    assert f == _verwacht_met_hashes()


def test_csv_scheidingsteken_wordt_geraden():
    inhoud = b"Datum,Gebruiker,Actie,Object,Resultaat,IP\n2026-09-01T10:00:00+02:00,u1,a,o,ok,x\n"
    kol = json.loads((FIX / "generiek-log.kolommen.json").read_text(encoding="utf-8"))
    f = generiek.lees_log_csv("x.csv", inhoud, kol, "2026-09-01", feiten.leeg())
    assert f["logregels"] == [{"tijdstip": "2026-09-01T10:00:00+02:00", "identiteit": "u1", "actie": "a",
                               "object": "o", "resultaat": "ok", "oorsprong": "x"}]


def test_ontbrekende_kolom_is_een_fout_geen_stilte():
    import pytest
    kol = {"tijdstip": "Bestaat niet", "identiteit": "Gebruiker", "actie": "Actie", "object": "Object",
           "resultaat": "Resultaat", "oorsprong": "IP"}
    with pytest.raises(ValueError, match="Bestaat niet"):
        generiek.lees_log_csv("generiek-log.csv", (FIX / "generiek-log.csv").read_bytes(), kol, "2026-09-01", feiten.leeg())
```

- [ ] **Stap 3: draai de test, verwacht rood**

Run: `python -m pytest tests/test_parsers.py -v`
Verwacht: FAIL, `ImportError: cannot import name 'generiek'`

- [ ] **Stap 4: schrijf de implementatie**

```python
# parsers/generiek.py
"""Generieke parser: JSON dat al de feiten-vorm heeft, en een CSV-log met een kolomkoppeling.

Het vangnet voor elke applicatie zonder eigen parser. De gebruiker zegt welke kolom welk logveld is;
de parser raadt alleen het scheidingsteken. Een ontbrekende kolom is een fout, geen leeg veld.
"""
from __future__ import annotations

import csv
import io
import json

from parsers import feiten as F


def _registreer(naam: str, inhoud: bytes, soort: str, peildatum: str, f: dict) -> None:
    f["bronbestanden"].append({"naam": naam, "soort": soort, "sha256": F.sha256_van(inhoud), "peildatum": peildatum})


def lees_config_json(naam: str, inhoud: bytes, peildatum: str, f: dict) -> dict:
    data = json.loads(inhoud.decode("utf-8"))
    for sleutel in ("applicatie", "instellingen"):
        if sleutel in data:
            f[sleutel] = data[sleutel]
    for sleutel in ("accounts", "rollen", "logtypen", "koppelingen"):
        if sleutel in data:
            f[sleutel] = list(data[sleutel])
    if "vorige_instellingen" in data:
        f["vorige_instellingen"] = data["vorige_instellingen"]
    _registreer(naam, inhoud, "configuratie", peildatum, f)
    return f


def _scheidingsteken(kopregel: str) -> str:
    return max((",", ";", "\t"), key=kopregel.count)


def lees_log_csv(naam: str, inhoud: bytes, kolommen: dict, peildatum: str, f: dict) -> dict:
    tekst = inhoud.decode("utf-8-sig")
    kopregel = tekst.split("\n", 1)[0]
    lezer = csv.DictReader(io.StringIO(tekst), delimiter=_scheidingsteken(kopregel))
    koppen = lezer.fieldnames or []
    for veld in F.LOGVELDEN:
        if kolommen.get(veld) not in koppen:
            raise ValueError(f"kolom '{kolommen.get(veld)}' voor {veld} staat niet in {naam}")
    for rij in lezer:
        f["logregels"].append({veld: (rij.get(kolommen[veld]) or "").strip() for veld in F.LOGVELDEN})
    _registreer(naam, inhoud, "log", peildatum, f)
    return f
```

- [ ] **Stap 5: draai de tests, verwacht groen**

Run: `python -m pytest tests/test_parsers.py -v`
Verwacht: 7 passed. Faalt de vergelijking met `feiten-verwacht.json`: druk beide af
(`print(json.dumps(f, indent=1, ensure_ascii=False))`) en corrigeer de fixture, niet de parser, tenzij de
parser een veld verkeerd vult.

- [ ] **Stap 6: commit**

```bash
git add parsers/generiek.py tests/test_parsers.py tests/fixtures/generiek-config.json tests/fixtures/generiek-log.csv tests/fixtures/generiek-log.kolommen.json tests/fixtures/feiten-verwacht.json
git commit -m "parsers: generieke JSON- en CSV-parser met fixtures"
```

### Taak 6: `doorloop.py`, de commandoregel-doorloop (bewijs dat F1 werkt zonder pagina)

**Files:**
- Create: `doorloop.py`
- Modify: `tests/test_toets.py` (één test erbij)
- Modify: `README.md` (sectie *Snel starten*)

**Interfaces:**
- Produces: `python doorloop.py --config <json> --log <csv> --kolommen <json> --peildatum 2026-09-01`
  drukt per maatregel de uitkomst af en schrijft `uitkomsten.json` (de vorm van `dossier_uitkomsten`).
  Functie `doorloop.draai(config_pad, log_pad, kolommen_pad, peildatum) -> dict`.

- [ ] **Stap 1: schrijf de falende test (onderaan `tests/test_toets.py`)**

```python
def test_doorloop_op_de_fixtures():
    import doorloop
    fix = ROOT / "tests" / "fixtures"
    uit = doorloop.draai(fix / "generiek-config.json", fix / "generiek-log.csv",
                         fix / "generiek-log.kolommen.json", PEIL)
    assert uit["8.15.01"]["uitkomst"] == "gedeeltelijk"          # regel 2 mist oorsprong
    assert uit["8.15.02"]["uitkomst"] == "niet aangetoond"       # bsn in regel 3
    assert uit["5.17.01"]["uitkomst"] == "aangetoond"
    assert uit["5.18.01"]["uitkomst"] == "niet aangetoond"       # u2 inactief
    assert uit["5.03.01"]["uitkomst"] == "niet aangetoond"       # u2 aanvrager + goedkeurder
    assert uit["8.32.01"]["uitkomst"] == "geen bewijs"
```

- [ ] **Stap 2: draai de test, verwacht rood**

Run: `python -m pytest tests/test_toets.py::test_doorloop_op_de_fixtures -v`
Verwacht: FAIL, `ModuleNotFoundError: No module named 'doorloop'`

- [ ] **Stap 3: schrijf de implementatie**

```python
# doorloop.py
#!/usr/bin/env python3
"""Doorloop op de commandoregel: export en log erin, uitkomst per maatregel eruit.

Bewijst dat regels, parsers en toets werken zonder de pagina. Wat hier uitkomt, moet de pagina (F3)
letterlijk ook laten zien.

    python doorloop.py --config export.json --log audit.csv --kolommen kolommen.json --peildatum 2026-09-01
"""
from __future__ import annotations

import argparse
import json
import pathlib

import toets
from parsers import feiten as F
from parsers import generiek

HIER = pathlib.Path(__file__).resolve().parent


def draai(config_pad, log_pad, kolommen_pad, peildatum: str) -> dict:
    f = F.leeg()
    f = generiek.lees_config_json(pathlib.Path(config_pad).name, pathlib.Path(config_pad).read_bytes(), peildatum, f)
    if log_pad:
        kol = json.loads(pathlib.Path(kolommen_pad).read_text(encoding="utf-8"))
        f = generiek.lees_log_csv(pathlib.Path(log_pad).name, pathlib.Path(log_pad).read_bytes(), kol, peildatum, f)
    fouten = F.valideer(f)
    if fouten:
        raise SystemExit("feiten ongeldig: " + "; ".join(fouten))
    bewijs = json.loads((HIER / "bewijs.json").read_text(encoding="utf-8"))
    regels = json.loads((HIER / "regels.json").read_text(encoding="utf-8"))
    return toets.dossier_uitkomsten(bewijs, regels, f, peildatum)


def main() -> int:
    p = argparse.ArgumentParser(description="Applicatiecheck op de commandoregel")
    p.add_argument("--config", required=True)
    p.add_argument("--log")
    p.add_argument("--kolommen")
    p.add_argument("--peildatum", required=True)
    p.add_argument("--uit", default="uitkomsten.json")
    a = p.parse_args()
    uit = draai(a.config, a.log, a.kolommen, a.peildatum)
    pathlib.Path(a.uit).write_text(json.dumps(uit, ensure_ascii=False, indent=1), encoding="utf-8")
    telling: dict[str, int] = {}
    for m in uit.values():
        telling[m["uitkomst"]] = telling.get(m["uitkomst"], 0) + 1
    for k, v in sorted(telling.items()):
        print(f"{v:4d}  {k}")
    print(f"geschreven: {a.uit}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Stap 4: draai alle tests en de doorloop zelf**

Run: `python -m pytest tests/ -v` (alles groen) en daarna
`python doorloop.py --config tests/fixtures/generiek-config.json --log tests/fixtures/generiek-log.csv --kolommen tests/fixtures/generiek-log.kolommen.json --peildatum 2026-09-01`
Verwacht: een telling met o.a. `94 niet aantoonbaar`, en `uitkomsten.json` in de map. Voeg
`uitkomsten.json` toe aan `.gitignore`.

- [ ] **Stap 5: README bijwerken**

Vervang in `README.md` onder `## Snel starten` de eerste zin "Er is nog niets te draaien." door:

```
Er is nog geen pagina, wel een doorloop op de commandoregel: `python doorloop.py --config <export.json>
--log <audit.csv> --kolommen <kolommen.json> --peildatum JJJJ-MM-DD` geeft per maatregel de uitkomst.
De fixtures in `tests/fixtures/` laten zien welke vorm de bestanden hebben.
```

- [ ] **Stap 6: commit**

```bash
git add doorloop.py tests/test_toets.py README.md .gitignore
git commit -m "doorloop: uitkomst per maatregel op de commandoregel"
```

**F1 is klaar als:** `python -m pytest tests/ -v` groen is, `doorloop.py` op de fixtures draait, en CI
op GitHub groen staat. Label blijft *concept*.

---

## F2 · JOIN-parser en PII-scrub

### Taak 7: de JOIN-parser op een synthetische fixture

**Files:**
- Create: `parsers/join.py`
- Create: `tests/fixtures/join-audit.tsv`, `tests/fixtures/join-rollen.tsv`
- Modify: `tests/test_parsers.py`

**Interfaces:**
- Produces: `parsers.join.KOLOMMEN_AUDIT: dict` en `parsers.join.KOLOMMEN_ROLLEN: dict` (de enige plek
  waar JOIN-kolomnamen staan), `parsers.join.herken(kopregel: str) -> str | None` (`"audit"`, `"rollen"`
  of `None`), `parsers.join.lees_audit(naam, inhoud, peildatum, feiten) -> dict`,
  `parsers.join.lees_rollen(naam, inhoud, peildatum, feiten) -> dict`.

> **Let op:** de kolomnamen hieronder zijn een aanname op basis van de publieke Decos-documentatie
> (auditgegevens: alle aanmaak-, wijzig- en verwijderacties; export tab-gescheiden; retentie per
> audittype). Controleer ze vóór deze taak tegen
> https://wiki.decos.com/nl/jzd/admin/features/auditdata (in een browser; geautomatiseerd ophalen geeft
> 403) of bij een JOIN-beheerder, en pas alleen `KOLOMMEN_AUDIT` en `KOLOMMEN_ROLLEN` aan. De fixture
> blijft verzonnen.

- [ ] **Stap 1: maak de fixtures**

`tests/fixtures/join-audit.tsv` (tab-gescheiden; schrijf echte tabs):

```
Datum	Tijd	Gebruiker	Handeling	Itemtype	Item	Resultaat	Werkstation
01-09-2026	10:00:00	u1	Wijzigen	Zaak	Z-2026-000123	Geslaagd	WS-005
01-09-2026	10:01:00	u1	Openen	Document	D-2026-000456	Geslaagd	WS-005
01-09-2026	10:02:00	lev1	Verwijderen	Zaak	Z-2026-000789	Geslaagd	WS-099
```

`tests/fixtures/join-rollen.tsv`:

```
Gebruikersnaam	Volledige naam	Gebruikersrollen	Laatste aanmelding	Extern	Lokaal wachtwoord	Geldig tot
u1	Gebruiker Een	Beheerder	30-08-2026 09:00	Nee	Nee	
u2	Gebruiker Twee	Aanvrager;Goedkeurder	01-02-2026 09:00	Nee	Nee	
lev1	Leverancier Een	Beheerder	30-08-2026 09:00	Ja	Ja	
```

- [ ] **Stap 2: schrijf de falende tests (onderaan `tests/test_parsers.py`)**

```python
from parsers import join  # noqa: E402


def test_join_herkent_zijn_exports_aan_de_kopregel():
    assert join.herken((FIX / "join-audit.tsv").read_text(encoding="utf-8").split("\n")[0]) == "audit"
    assert join.herken((FIX / "join-rollen.tsv").read_text(encoding="utf-8").split("\n")[0]) == "rollen"
    assert join.herken("Datum;Gebruiker;Actie") is None


def test_join_audit_naar_logregels_met_tijdzone():
    f = join.lees_audit("join-audit.tsv", (FIX / "join-audit.tsv").read_bytes(), "2026-09-01", feiten.leeg())
    assert feiten.valideer(f) == []
    assert f["logregels"][0] == {"tijdstip": "2026-09-01T10:00:00+02:00", "identiteit": "u1", "actie": "Wijzigen",
                                 "object": "Zaak Z-2026-000123", "resultaat": "Geslaagd", "oorsprong": "WS-005"}
    assert f["bronbestanden"][0]["soort"] == "log"


def test_join_rollen_naar_accounts():
    f = join.lees_rollen("join-rollen.tsv", (FIX / "join-rollen.tsv").read_bytes(), "2026-09-01", feiten.leeg())
    assert feiten.valideer(f) == []
    u2 = [a for a in f["accounts"] if a["id"] == "u2"][0]
    assert u2 == {"id": "u2", "type": "persoon", "rollen": ["Aanvrager", "Goedkeurder"], "lokaal_wachtwoord": False,
                  "laatste_inlog": "2026-02-01T09:00:00+02:00", "einddatum": None}
    lev = [a for a in f["accounts"] if a["id"] == "lev1"][0]
    assert lev["type"] == "leverancier" and lev["lokaal_wachtwoord"] is True
    assert {r["id"] for r in f["rollen"]} == {"Beheerder", "Aanvrager", "Goedkeurder"}
```

- [ ] **Stap 3: draai de test, verwacht rood**

Run: `python -m pytest tests/test_parsers.py -v`
Verwacht: FAIL, `ImportError: cannot import name 'join'`

- [ ] **Stap 4: schrijf de implementatie**

```python
# parsers/join.py
"""JOIN Zaak & Document (Decos): de audit-export en de gebruikersrollen-export naar feiten.

Alle JOIN-specifieke kennis staat in de twee KOLOMMEN-dicts; de rest is vertalen. Datums in JOIN zijn
Nederlands (dd-mm-jjjj) zonder tijdzone; de export komt uit een Nederlandse installatie, dus
Europe/Amsterdam. In september is dat +02:00; de tijdzone wordt per datum bepaald.
"""
from __future__ import annotations

import csv
import datetime as dt
import io
from zoneinfo import ZoneInfo

from parsers import feiten as F

TIJDZONE = ZoneInfo("Europe/Amsterdam")

# Aanname op basis van de publieke Decos-documentatie; controleren en alleen hier aanpassen.
KOLOMMEN_AUDIT = {"datum": "Datum", "tijd": "Tijd", "identiteit": "Gebruiker", "actie": "Handeling",
                  "itemtype": "Itemtype", "item": "Item", "resultaat": "Resultaat", "oorsprong": "Werkstation"}
KOLOMMEN_ROLLEN = {"id": "Gebruikersnaam", "rollen": "Gebruikersrollen", "laatste_inlog": "Laatste aanmelding",
                   "extern": "Extern", "lokaal_wachtwoord": "Lokaal wachtwoord", "einddatum": "Geldig tot"}


def herken(kopregel: str) -> str | None:
    koppen = set(kopregel.strip().split("\t"))
    if set(KOLOMMEN_AUDIT.values()) <= koppen:
        return "audit"
    if set(KOLOMMEN_ROLLEN.values()) <= koppen:
        return "rollen"
    return None


def _tijdstip(datum: str, tijd: str) -> str:
    """'01-09-2026' + '10:00:00' (of '10:00') -> ISO 8601 met de tijdzone van dat moment."""
    tijd = tijd.strip() or "00:00:00"
    if tijd.count(":") == 1:
        tijd += ":00"
    naief = dt.datetime.strptime(f"{datum.strip()} {tijd}", "%d-%m-%Y %H:%M:%S")
    return naief.replace(tzinfo=TIJDZONE).isoformat()


def _rijen(inhoud: bytes) -> list[dict]:
    return list(csv.DictReader(io.StringIO(inhoud.decode("utf-8-sig")), delimiter="\t"))


def _registreer(naam: str, inhoud: bytes, soort: str, peildatum: str, f: dict) -> None:
    f["bronbestanden"].append({"naam": naam, "soort": soort, "sha256": F.sha256_van(inhoud), "peildatum": peildatum})


def lees_audit(naam: str, inhoud: bytes, peildatum: str, f: dict) -> dict:
    k = KOLOMMEN_AUDIT
    for rij in _rijen(inhoud):
        f["logregels"].append({
            "tijdstip": _tijdstip(rij[k["datum"]], rij.get(k["tijd"], "")),
            "identiteit": rij[k["identiteit"]].strip(),
            "actie": rij[k["actie"]].strip(),
            "object": f"{rij[k['itemtype']].strip()} {rij[k['item']].strip()}".strip(),
            "resultaat": rij[k["resultaat"]].strip(),
            "oorsprong": rij.get(k["oorsprong"], "").strip(),
        })
    _registreer(naam, inhoud, "log", peildatum, f)
    return f


def _ja(waarde: str) -> bool:
    return waarde.strip().lower() in ("ja", "yes", "true", "1")


def lees_rollen(naam: str, inhoud: bytes, peildatum: str, f: dict) -> dict:
    k = KOLOMMEN_ROLLEN
    rollen: set[str] = set()
    for rij in _rijen(inhoud):
        lijst = [r.strip() for r in rij[k["rollen"]].split(";") if r.strip()]
        rollen.update(lijst)
        laatste = rij.get(k["laatste_inlog"], "").strip()
        eind = rij.get(k["einddatum"], "").strip()
        f["accounts"].append({
            "id": rij[k["id"]].strip(),
            "type": "leverancier" if _ja(rij.get(k["extern"], "")) else "persoon",
            "rollen": lijst,
            "lokaal_wachtwoord": _ja(rij.get(k["lokaal_wachtwoord"], "")),
            "laatste_inlog": _tijdstip(*laatste.split(" ", 1)) if laatste else None,
            "einddatum": _tijdstip(eind, "") if eind else None,
        })
    f["rollen"] = [{"id": r, "beheer": r.lower().startswith("beheer")} for r in sorted(rollen)]
    _registreer(naam, inhoud, "configuratie", peildatum, f)
    return f
```

- [ ] **Stap 5: draai de tests, verwacht groen**

Run: `python -m pytest tests/test_parsers.py -v`
Verwacht: 10 passed. Op Windows kan `ZoneInfo("Europe/Amsterdam")` falen zonder tzdata: `pip install
tzdata` en voeg `tzdata` toe aan de CI-installatie in `.github/workflows/ci.yml` (regel `pip install
--upgrade pip pytest tzdata`).

- [ ] **Stap 6: commit**

```bash
git add parsers/join.py tests/test_parsers.py tests/fixtures/join-audit.tsv tests/fixtures/join-rollen.tsv .github/workflows/ci.yml
git commit -m "parsers: JOIN audit- en rollenexport op een synthetische fixture"
```

### Taak 8: `doorloop.py` herkent JOIN-bestanden

**Files:**
- Modify: `doorloop.py`
- Modify: `tests/test_toets.py`

- [ ] **Stap 1: schrijf de falende test (onderaan `tests/test_toets.py`)**

```python
def test_doorloop_met_join_bestanden():
    import doorloop
    fix = ROOT / "tests" / "fixtures"
    uit = doorloop.draai_bestanden([fix / "join-rollen.tsv", fix / "join-audit.tsv"], PEIL)
    assert uit["8.15.01"]["uitkomst"] == "aangetoond"
    assert uit["5.18.01"]["uitkomst"] == "niet aangetoond"   # u2 sinds februari niet ingelogd
    assert uit["8.05.01"]["regels"][0]["waarde"] == ["lev1"]  # leverancier zonder einddatum
```

- [ ] **Stap 2: draai de test, verwacht rood**

Run: `python -m pytest tests/test_toets.py::test_doorloop_met_join_bestanden -v`
Verwacht: FAIL, `AttributeError: module 'doorloop' has no attribute 'draai_bestanden'`

- [ ] **Stap 3: voeg `draai_bestanden` toe aan `doorloop.py`** (boven `main`, en laat `draai` staan)

```python
from parsers import join  # bovenaan bij de imports


def draai_bestanden(paden: list, peildatum: str) -> dict:
    """Herkent per bestand de parser: JOIN aan de kopregel, anders JSON als configuratie."""
    f = F.leeg()
    for pad in paden:
        pad = pathlib.Path(pad)
        inhoud = pad.read_bytes()
        kop = inhoud.decode("utf-8-sig", errors="replace").split("\n", 1)[0]
        soort = join.herken(kop)
        if soort == "audit":
            f = join.lees_audit(pad.name, inhoud, peildatum, f)
        elif soort == "rollen":
            f = join.lees_rollen(pad.name, inhoud, peildatum, f)
        elif pad.suffix.lower() == ".json":
            f = generiek.lees_config_json(pad.name, inhoud, peildatum, f)
        else:
            raise SystemExit(f"{pad.name}: niet herkend; gebruik --log met --kolommen voor een CSV-log")
    fouten = F.valideer(f)
    if fouten:
        raise SystemExit("feiten ongeldig: " + "; ".join(fouten))
    bewijs = json.loads((HIER / "bewijs.json").read_text(encoding="utf-8"))
    regels = json.loads((HIER / "regels.json").read_text(encoding="utf-8"))
    return toets.dossier_uitkomsten(bewijs, regels, f, peildatum)
```

En in `main`: voeg `p.add_argument("bestanden", nargs="*")` toe; als `a.bestanden` niet leeg is, gebruik
`draai_bestanden(a.bestanden, a.peildatum)`, anders het bestaande pad.

- [ ] **Stap 4: draai alle tests, verwacht groen; commit**

```bash
git add doorloop.py tests/test_toets.py
git commit -m "doorloop: JOIN-bestanden herkennen aan de kopregel"
```

### Taak 9: `patronen.js`, de spiegel voor de pagina (voorbereiding op F3)

**Files:**
- Create: `check/bron/patronen.js`
- Modify: `tests/test_patronen.py`

- [ ] **Stap 1: schrijf de falende test (onderaan `tests/test_patronen.py`)**

```python
def test_patronen_js_spiegelt_python(tmp_path):
    """Node draait de JS-versie op dezelfde invoer; de uitkomst moet gelijk zijn aan Python."""
    import json
    import shutil
    import subprocess
    if not shutil.which("node"):
        import pytest
        pytest.skip("node niet beschikbaar")
    js = (ROOT / "check" / "bron" / "patronen.js").read_text(encoding="utf-8")
    invoer = ["bsn 111222333 en 123456789", "NL91ABNA0417164300", "a.b@voorbeeld.nl", "bel 06-12345678",
              "password=geheim123", "wachtwoord gewijzigd"]
    script = js + "\nconst uit = process.argv[2] ? JSON.parse(process.argv[2]).map(t => patronen.zoek(t, ['bsn','iban','email','telefoon','wachtwoord'])) : [];\nconsole.log(JSON.stringify(uit));\n"
    pad = tmp_path / "run.js"
    pad.write_text(script, encoding="utf-8")
    uit = subprocess.run(["node", str(pad), json.dumps(invoer)], capture_output=True, text=True, check=True)
    verwacht = [patronen.zoek(t, ["bsn", "iban", "email", "telefoon", "wachtwoord"]) for t in invoer]
    assert json.loads(uit.stdout) == verwacht
```

- [ ] **Stap 2: draai de test, verwacht rood** (`FileNotFoundError: patronen.js`)

- [ ] **Stap 3: schrijf `check/bron/patronen.js`**

```javascript
// Spiegel van patronen.py: dezelfde patronen, dezelfde namen, dezelfde uitkomst.
// Geen module-syntax: dit bestand wordt door check/bouw.py in dezelfde scripttag als app.js gezet.
var patronen = (function () {
  'use strict';
  var EMAIL = /\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b/g;
  var TELEFOON = /(?<!\w)(?:\+31[\s-]?\(?0?\)?|0)(?:[\s-]?\d){8,10}(?!\w)/g;
  var IBAN_NL = /\bNL\d{2}\s?[A-Z]{4}\s?\d{4}\s?\d{4}\s?\d{2}\b/g;
  var BSN_KANDIDAAT = /(?<!\d)(\d{9})(?!\d)/g;
  var WACHTWOORD = /\b(?:password|passwd|pwd|wachtwoord|secret|token)\s*[:=]\s*\S+/gi;

  function isGeldigBsn(nummer) {
    if (nummer.length !== 9 || !/^\d{9}$/.test(nummer) || nummer === '000000000') return false;
    var gewichten = [9, 8, 7, 6, 5, 4, 3, 2, -1], totaal = 0;
    for (var i = 0; i < 9; i++) totaal += parseInt(nummer[i], 10) * gewichten[i];
    return totaal % 11 === 0;
  }
  function alle(re, tekst, groep) {
    re.lastIndex = 0;
    var uit = [], m;
    while ((m = re.exec(tekst)) !== null) uit.push(groep ? m[groep] : m[0]);
    return uit;
  }
  var PATRONEN = {
    bsn: function (t) { return alle(BSN_KANDIDAAT, t, 1).filter(isGeldigBsn); },
    iban: function (t) { return alle(IBAN_NL, t); },
    email: function (t) { return alle(EMAIL, t); },
    telefoon: function (t) { return alle(TELEFOON, t); },
    wachtwoord: function (t) { return alle(WACHTWOORD, t); }
  };
  function zoek(tekst, namen) {
    var uit = {};
    namen.forEach(function (naam) {
      if (!PATRONEN[naam]) throw new Error('onbekend patroon: ' + naam);
      uit[naam] = PATRONEN[naam](tekst);
    });
    return uit;
  }
  return { PATRONEN: PATRONEN, zoek: zoek, isGeldigBsn: isGeldigBsn };
})();
```

- [ ] **Stap 4: draai de test, verwacht groen; commit**

```bash
git add check/bron/patronen.js tests/test_patronen.py
git commit -m "check: patronen.js als spiegel van patronen.py, met node-vergelijkingstest"
```

**F2 is klaar als:** alle tests groen, `python doorloop.py tests/fixtures/join-rollen.tsv tests/fixtures/join-audit.tsv --peildatum 2026-09-01` een telling geeft, en de JOIN-kolomnamen in `parsers/join.py` zijn geverifieerd of expliciet als aanname gemarkeerd in een commentaarregel met datum.

---

## F3 · De pagina: aanleveren, toetsen, dossier

> **Werkwijze:** kopieer eerst `csir-assessment-tool/register/bouw.py`, `bron/index.html`, `bron/app.css` en
> `tests/test_bouw.py` naar `check/` en pas ze aan zoals hieronder. Schrijf `app.js` nieuw; de
> CSIR-`app.js` is een voorbeeld van stijl (object `reken` met gespiegelde functies, geen inline styles,
> `hidden`-attribuut voor zichtbaarheid), niet van inhoud.

### Taak 10: `check/bouw.py` en de bouwtest

**Files:**
- Create: `check/bouw.py`, `check/bron/index.html`, `check/bron/app.css`, `check/bron/app.js` (voorlopig alleen `var toets = {};`)
- Test: `tests/test_bouw.py`

**Interfaces:**
- Produces: `check.bouw.bouw(doel: pathlib.Path) -> pathlib.Path` schrijft `index.html` met
  `window.__BRON__ = {bio2, bewijs, regels}` plus `patronen.js` plus `app.js` in één scripttag, `app.css` in
  één styletag, en de CSP `default-src 'none'; script-src 'sha256-…'; style-src 'sha256-…'; img-src data:; form-action 'none'; base-uri 'none'`.

- [ ] **Stap 1: schrijf de falende test**

```python
# tests/test_bouw.py
"""De gebouwde pagina: alles erin wat erin hoort, niets wat naar buiten wijst, en een CSP die klopt."""
from __future__ import annotations

import base64
import hashlib
import json
import pathlib
import re
import sys

import pytest

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "check"))
import bouw as bouwer  # noqa: E402

TOEGESTANE_LINKS = ("https://security-commons-nl.github.io/", "https://github.com/security-commons-nl/")


@pytest.fixture(scope="module")
def html(tmp_path_factory) -> str:
    return bouwer.bouw(tmp_path_factory.mktemp("dist")).read_text(encoding="utf-8")


def in_pagina(tekst: str, html: str) -> bool:
    return json.dumps(tekst, ensure_ascii=False)[1:-1].replace("</", "<\\/") in html


def test_alle_maatregelen_en_regels_zitten_erin(html):
    bio2 = json.loads((ROOT / "bronnen" / "bio2.json").read_text(encoding="utf-8"))
    regels = json.loads((ROOT / "regels.json").read_text(encoding="utf-8"))
    for m in bio2["maatregelen"]:
        assert in_pagina(m["id"], html) and in_pagina(m["titel"], html), m["id"]
    for r in regels["regels"]:
        assert in_pagina(r["eis"], html), r["id"]


def test_geen_tekst_van_het_cip_in_de_pagina(html):
    """Nummers en titels wel, de tekst van de overheidsmaatregel niet; zie deel 1 (CC BY-NC-SA)."""
    for veld in ("overheidsmaatregel", "iso_maatregel"):
        assert f'"{veld}"' not in html, veld


def test_geen_externe_verwijzing(html):
    for patroon in ("src=", "@import", "url(", "fetch(", "XMLHttpRequest", "<iframe", '<link rel="stylesheet"'):
        assert patroon not in html, patroon
    for adres in re.findall(r"https?://[^\"'<>\s)]+", html):
        assert adres.startswith(TOEGESTANE_LINKS), adres


def test_csp_klopt_met_de_inhoud(html):
    script = re.search(r"<script>(.*?)</script>", html, re.S).group(1)
    stijl = re.search(r"<style>(.*?)</style>", html, re.S).group(1)
    h = lambda s: base64.b64encode(hashlib.sha256(s.encode("utf-8")).digest()).decode()
    csp = re.search(r'Content-Security-Policy" content="([^"]+)"', html).group(1)
    assert csp == (f"default-src 'none'; script-src 'sha256-{h(script)}'; style-src 'sha256-{h(stijl)}'; "
                   "img-src data:; form-action 'none'; base-uri 'none'")
    assert html.count("<script>") == 1 and html.count("<style>") == 1


def test_kruimelpad_en_voetregel(html):
    assert 'href="https://security-commons-nl.github.io/"' in html
    assert "Applicatiecheck" in html and "EUPL-1.2" in html
```

- [ ] **Stap 2: draai de test, verwacht rood** (`ModuleNotFoundError: bouw`)

- [ ] **Stap 3: schrijf `check/bouw.py`**

```python
#!/usr/bin/env python3
"""Bouwt Applicatiecheck: één zelfstandig HTML-bestand uit de JSON-bronnen en check/bron/.

Zelfde patroon als csir-assessment-tool/register/bouw.py: bron als JSON in dezelfde scripttag als de
app, één stylesheet, en een Content-Security-Policy met de sha256 van allebei. Alleen standaardbibliotheek.

    python check/bouw.py            # schrijft check/dist/index.html
    python check/bouw.py <doelmap>
"""
from __future__ import annotations

import base64
import hashlib
import json
import pathlib
import sys

HIER = pathlib.Path(__file__).resolve().parent
REPO = HIER.parent
BRON = HIER / "bron"


def sha256_csp(inhoud: str) -> str:
    return "sha256-" + base64.b64encode(hashlib.sha256(inhoud.encode("utf-8")).digest()).decode()


def lees_json(naam: str) -> dict:
    return json.loads((REPO / naam).read_text(encoding="utf-8"))


def bouw(doel: pathlib.Path) -> pathlib.Path:
    data = {"bio2": lees_json("bronnen/bio2.json"), "bewijs": lees_json("bewijs.json"), "regels": lees_json("regels.json")}
    css = (BRON / "app.css").read_text(encoding="utf-8").strip()
    js = "\n".join((BRON / n).read_text(encoding="utf-8").strip() for n in ("patronen.js", "app.js"))
    sjabloon = (BRON / "index.html").read_text(encoding="utf-8")
    json_bron = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    script = "window.__BRON__ = " + json_bron + ";\n" + js
    html = (sjabloon.replace("__CSS__", css).replace("__SCRIPT__", script)
            .replace("__SCRIPT_HASH__", sha256_csp(script).removeprefix("sha256-"))
            .replace("__STYLE_HASH__", sha256_csp(css).removeprefix("sha256-")))
    for rest in ("__CSS__", "__SCRIPT__", "__SCRIPT_HASH__", "__STYLE_HASH__"):
        assert rest not in html, rest
    doel.mkdir(parents=True, exist_ok=True)
    uit = doel / "index.html"
    uit.write_bytes(html.encode("utf-8"))
    return uit


if __name__ == "__main__":
    bestand = bouw(pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else HIER / "dist")
    print(f"{bestand}: {bestand.stat().st_size / 1024:.0f} kB, zelfstandig en offline")
```

`check/bron/index.html` (het skelet; de secties krijgen in taak 11 hun inhoud):

```html
<!doctype html>
<html lang="nl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; script-src 'sha256-__SCRIPT_HASH__'; style-src 'sha256-__STYLE_HASH__'; img-src data:; form-action 'none'; base-uri 'none'">
<title>Applicatiecheck · Security Commons NL</title>
<style>
__CSS__
</style>
</head>
<body>
<header class="kop">
  <nav aria-label="Kruimelpad"><a href="https://security-commons-nl.github.io/">Security Commons NL</a> › <a href="https://security-commons-nl.github.io/applicatiecheck/">Applicatiecheck</a> › Toets</nav>
  <h1>Applicatiecheck</h1>
  <p class="lead">Toon uit de applicatie zelf aan wat de BIO2 van een kritische applicatie vraagt. Alles rekent in je browser; er gaat niets naar buiten.</p>
  <nav class="stappen" aria-label="Stappen">
    <button type="button" class="stap actief" data-stap="aanleveren">1. Aanleveren</button>
    <button type="button" class="stap" data-stap="toetsen">2. Toetsen</button>
    <button type="button" class="stap" data-stap="dossier">3. Dossier</button>
  </nav>
</header>
<main>
  <section id="aanleveren" class="paneel"></section>
  <section id="toetsen" class="paneel" hidden></section>
  <section id="dossier" class="paneel" hidden></section>
</main>
<footer>
  <p>Licentie: <a href="https://github.com/security-commons-nl/applicatiecheck/blob/main/LICENSE">EUPL-1.2</a> · Bron en verbeteringen: <a href="https://github.com/security-commons-nl/applicatiecheck">GitHub</a> · Deze pagina is gebouwd uit <code>bewijs.json</code>, <code>regels.json</code> en <code>bronnen/bio2.json</code>.</p>
</footer>
<script>
__SCRIPT__
</script>
</body>
</html>
```

`check/bron/app.css`: kopieer `csir-assessment-tool/register/bron/app.css` en voeg onderaan toe:

```css
/* Applicatiecheck: uitkomstkleuren als class, nooit inline (CSP). */
.uitkomst-aangetoond { color: #1b6e3a; }
.uitkomst-gedeeltelijk { color: #9a6b00; }
.uitkomst-niet-aangetoond { color: #a33; }
.uitkomst-geen-bewijs, .uitkomst-handmatig, .uitkomst-niet-aantoonbaar { color: #666; }
.paneel[hidden] { display: none; }
```

`check/bron/app.js`, voorlopig: `var toets = {};` (taak 11 vult hem).

- [ ] **Stap 4: draai de test, verwacht groen; commit**

```bash
git add check/bouw.py check/bron/index.html check/bron/app.css check/bron/app.js tests/test_bouw.py
git commit -m "check: bouwscript en skelet van de pagina met CSP"
```

### Taak 11: `app.js`, deel 1: de spiegel van `toets.py` (zonder UI), getest via node

**Files:**
- Modify: `check/bron/app.js`
- Modify: `tests/test_toets.py`

**Interfaces:**
- Produces: globaal object `toets` met `toets_regel(regel, feiten, peildatum)`, `toets_alles(regels, feiten, peildatum)`,
  `uitkomst_maatregel(soort, regeluitkomsten)`, `dossier_uitkomsten(bewijs, regels, feiten, peildatum)`;
  exact dezelfde uitkomstobjecten als Python (`regel`, `maatregel`, `uitkomst`, `waarde`, `toelichting`).

- [ ] **Stap 1: schrijf de falende test (onderaan `tests/test_toets.py`)**

```python
def test_app_js_spiegelt_toets_py(tmp_path):
    """Node draait de JS-toets op de fixture-feiten; per maatregel moet uitkomst én regelwaarde gelijk zijn."""
    import json
    import shutil
    import subprocess
    import pytest
    if not shutil.which("node"):
        pytest.skip("node niet beschikbaar")
    import doorloop
    fix = ROOT / "tests" / "fixtures"
    from parsers import generiek
    f = F.leeg()
    f = generiek.lees_config_json("generiek-config.json", (fix / "generiek-config.json").read_bytes(), PEIL, f)
    kol = json.loads((fix / "generiek-log.kolommen.json").read_text(encoding="utf-8"))
    f = generiek.lees_log_csv("generiek-log.csv", (fix / "generiek-log.csv").read_bytes(), kol, PEIL, f)
    bewijs = json.loads((ROOT / "bewijs.json").read_text(encoding="utf-8"))
    regels = json.loads((ROOT / "regels.json").read_text(encoding="utf-8"))
    py = toets.dossier_uitkomsten(bewijs, regels, f, PEIL)

    js = "\n".join((ROOT / "check" / "bron" / n).read_text(encoding="utf-8") for n in ("patronen.js", "app.js"))
    script = js + "\nconst [bewijs, regels, feiten, peil] = JSON.parse(require('fs').readFileSync(process.argv[2], 'utf8'));\nconsole.log(JSON.stringify(toets.dossier_uitkomsten(bewijs, regels, feiten, peil)));\n"
    (tmp_path / "run.js").write_text(script, encoding="utf-8")
    (tmp_path / "in.json").write_text(json.dumps([bewijs, regels, f, PEIL]), encoding="utf-8")
    uit = subprocess.run(["node", str(tmp_path / "run.js"), str(tmp_path / "in.json")], capture_output=True, text=True, check=True)
    assert json.loads(uit.stdout) == py
```

- [ ] **Stap 2: draai de test, verwacht rood** (`TypeError: toets.dossier_uitkomsten is not a function`)

- [ ] **Stap 3: schrijf `check/bron/app.js`, deel 1**

Vertaal `toets.py` één op één. Regels voor de vertaling, zodat de uitkomsten byte-gelijk zijn:
- `round(x, 4)` → `Math.round(x * 10000) / 10000`.
- `dt.datetime.fromisoformat` met tijdzone → `new Date(tekst)`; geldig als `!isNaN(d)` en de tekst eindigt
  op `Z` of `[+-]\d\d:\d\d` (dat is de tijdzone-eis).
- `_dagen_oud`: `(Date.parse(peildatum + "T00:00:00+00:00") - Date.parse(tijdstip)) / 86400000`.
- `sorted(...)` → `.sort()` op strings; `set(huidig) | set(vorige)` → `Object.keys` van beide samengevoegd en ontdubbeld.
- `_leeg`: `null`, `undefined`, `""`, lege array, leeg object.
- Fouten: `throw new Error(...)` met dezelfde Nederlandse tekst.
- Geen `fetch`, geen `import`, geen ES-modules; `'use strict'` in een IIFE die `toets` als globaal object teruggeeft, net als `patronen.js`.

```javascript
// Spiegel van toets.py. Zelfde functies, zelfde namen, zelfde uitkomsten; test_app_js_spiegelt_toets_py bewaakt dat.
var toets = (function () {
  'use strict';
  var RANG = { 'niet aangetoond': 0, 'geen bewijs': 1, 'gedeeltelijk': 2, 'aangetoond': 3 };
  var SPIEGEL = ['toets_regel', 'toets_alles', 'uitkomst_maatregel', 'dossier_uitkomsten'];

  function uit(regel, uitkomst, waarde, toelichting) {
    return { regel: regel.id, maatregel: regel.maatregel, uitkomst: uitkomst,
             waarde: waarde === undefined ? null : waarde, toelichting: toelichting || '' };
  }
  function pad(feiten, p) {
    var huidig = feiten, stappen = p.split('.');
    for (var i = 0; i < stappen.length; i++) {
      if (huidig === null || typeof huidig !== 'object' || !(stappen[i] in huidig)) return null;
      huidig = huidig[stappen[i]];
    }
    return huidig;
  }
  function leeg(w) {
    return w === null || w === undefined || w === '' || (Array.isArray(w) && w.length === 0) ||
      (typeof w === 'object' && !Array.isArray(w) && Object.keys(w).length === 0);
  }
  function tijdstipGeldig(t) {
    return typeof t === 'string' && /(Z|[+-]\d\d:\d\d)$/.test(t) && !isNaN(Date.parse(t));
  }
  function dagenOud(t, peildatum) {
    if (!tijdstipGeldig(t)) return null;
    return (Date.parse(peildatum + 'T00:00:00+00:00') - Date.parse(t)) / 86400000;
  }
  function rond4(x) { return Math.round(x * 10000) / 10000; }
  function voldoet(record, w, peildatum) {
    var waarde = record[w.veld];
    if ('is' in w) return waarde === w.is;
    if ('leeg' in w) return leeg(waarde) === w.leeg;
    if ('niet_leeg' in w) return (!leeg(waarde)) === w.niet_leeg;
    if ('ouder_dan_dagen' in w) { var oud = typeof waarde === 'string' ? dagenOud(waarde, peildatum) : null; return oud !== null && oud > w.ouder_dan_dagen; }
    throw new Error('onbekende voorwaarde: ' + JSON.stringify(w));
  }
  function drempel(regel, aandeel, toelichting) {
    var d = regel.toets.drempel;
    if (aandeel >= d) return uit(regel, 'aangetoond', aandeel, toelichting);
    if (aandeel > 0) return uit(regel, 'gedeeltelijk', aandeel, toelichting);
    return uit(regel, 'niet aangetoond', aandeel, toelichting);
  }

  function toets_regel(regel, feiten, peildatum) {
    var t = regel.toets, soort = t.type, records, i, r;
    if (soort === 'velden_aanwezig') {
      records = feiten[t.over] || [];
      if (!records.length) return uit(regel, 'geen bewijs', null, 'geen ' + t.over + ' aangeleverd');
      var goed = 0;
      for (i = 0; i < records.length; i++) { r = records[i]; if (t.velden.every(function (v) { return !leeg(r[v]); })) goed++; }
      return drempel(regel, rond4(goed / records.length), goed + ' van ' + records.length + ' records bevatten alle velden');
    }
    if (soort === 'geen_patroon') {
      records = feiten[t.over] || [];
      if (!records.length) return uit(regel, 'geen bewijs', null, 'geen ' + t.over + ' aangeleverd');
      var telling = {}; t.patronen.forEach(function (n) { telling[n] = 0; });
      records.forEach(function (rec) {
        var tekst = Object.keys(rec).map(function (k) { return rec[k]; })
          .filter(function (v) { return typeof v === 'string' || (typeof v === 'number' && Number.isInteger(v)); })
          .map(String).join(' ');
        var tr = patronen.zoek(tekst, t.patronen);
        Object.keys(tr).forEach(function (n) { telling[n] += tr[n].length; });
      });
      var totaal = Object.keys(telling).reduce(function (s, k) { return s + telling[k]; }, 0);
      if (totaal === 0) return uit(regel, 'aangetoond', telling, 'geen treffers');
      return uit(regel, 'niet aangetoond', telling, totaal + ' treffer(s)');
    }
    if (soort === 'tijdstempel_geldig') {
      records = feiten[t.over] || [];
      if (!records.length) return uit(regel, 'geen bewijs', null, 'geen ' + t.over + ' aangeleverd');
      var ok = 0, vorige = null;
      for (i = 0; i < records.length; i++) {
        var tekst2 = records[i][t.veld];
        if (!tijdstipGeldig(tekst2)) continue;
        var moment = Date.parse(tekst2);
        if (vorige === null || moment >= vorige) ok++;
        vorige = moment;
      }
      return drempel(regel, rond4(ok / records.length), ok + ' van ' + records.length + ' tijdstempels geldig en in volgorde');
    }
    if (soort === 'waarde_gelijk' || soort === 'waarde_minimaal' || soort === 'waarde_maximaal') {
      var waarde = pad(feiten, t.pad);
      if (waarde === null) return uit(regel, 'geen bewijs', null, t.pad + ' ontbreekt');
      var goed2;
      if (soort === 'waarde_gelijk') goed2 = waarde === t.waarde;
      else if (soort === 'waarde_minimaal') goed2 = typeof waarde === 'number' && waarde >= t.waarde;
      else goed2 = typeof waarde === 'number' && waarde <= t.waarde;
      return uit(regel, goed2 ? 'aangetoond' : 'niet aangetoond', waarde,
                 t.pad + ' = ' + JSON.stringify(waarde) + ', eis ' + soort.split('_')[1] + ' ' + JSON.stringify(t.waarde));
    }
    if (soort === 'lijst_leeg') {
      records = feiten[t.over];
      if (!records || !records.length) return uit(regel, 'geen bewijs', null, 'geen ' + t.over + ' aangeleverd');
      var ids = records.filter(function (rec) { return t.waar.every(function (w) { return voldoet(rec, w, peildatum); }); })
        .map(function (rec) { return rec.id === undefined ? '?' : rec.id; });
      if (!ids.length) return uit(regel, 'aangetoond', [], 'geen records voldoen aan de voorwaarden');
      return uit(regel, 'niet aangetoond', ids, ids.length + ' record(s): ' + ids.join(', '));
    }
    if (soort === 'bron_aanwezig') {
      var bronnen = (feiten.bronbestanden || []).filter(function (b) { return b.soort === t.soort; });
      if (!bronnen.length) return uit(regel, 'geen bewijs', null, 'geen bronbestand van soort ' + t.soort);
      return uit(regel, 'aangetoond', bronnen.map(function (b) { return b.sha256; }), bronnen.length + ' bestand(en) van soort ' + t.soort);
    }
    if (soort === 'verschil_met_vorige') {
      var vorigeI = feiten.vorige_instellingen;
      if (vorigeI === null || typeof vorigeI !== 'object') return uit(regel, 'geen bewijs', null, 'geen vorige export aangeleverd');
      var huidigI = feiten.instellingen || {};
      var sleutels = Object.keys(huidigI).concat(Object.keys(vorigeI)).filter(function (k, idx, arr) { return arr.indexOf(k) === idx; });
      var gewijzigd = sleutels.filter(function (k) { return JSON.stringify(huidigI[k]) !== JSON.stringify(vorigeI[k]); }).sort();
      return uit(regel, 'aangetoond', gewijzigd, gewijzigd.length + ' sleutel(s) gewijzigd');
    }
    if (soort === 'geen_onverenigbare_rollen') {
      var paren = pad(feiten, 'instellingen.onverenigbare_rollen');
      if (!paren || !paren.length) return uit(regel, 'geen bewijs', null, 'geen lijst van onverenigbare rollen ingevoerd');
      records = feiten.accounts || [];
      if (!records.length) return uit(regel, 'geen bewijs', null, 'geen accounts aangeleverd');
      var ids2 = records.filter(function (rec) {
        var rollen = rec.rollen || [];
        return paren.some(function (paar) { return paar.every(function (rol) { return rollen.indexOf(rol) !== -1; }); });
      }).map(function (rec) { return rec.id === undefined ? '?' : rec.id; });
      if (!ids2.length) return uit(regel, 'aangetoond', [], 'geen account met een onverenigbaar paar');
      return uit(regel, 'niet aangetoond', ids2, ids2.length + ' account(s): ' + ids2.join(', '));
    }
    throw new Error('onbekend toetstype: ' + soort);
  }
  function toets_alles(regels, feiten, peildatum) { return regels.regels.map(function (r) { return toets_regel(r, feiten, peildatum); }); }
  function uitkomst_maatregel(soort, regeluitkomsten) {
    if (soort[0] === 'D') return 'niet aantoonbaar';
    if (!regeluitkomsten.length) return 'handmatig';
    var u = regeluitkomsten.map(function (x) { return x.uitkomst; });
    if (u.every(function (x) { return x === 'geen bewijs'; })) return 'geen bewijs';
    return u.reduce(function (a, b) { return RANG[a] <= RANG[b] ? a : b; });
  }
  function dossier_uitkomsten(bewijs, regels, feiten, peildatum) {
    var per = {};
    toets_alles(regels, feiten, peildatum).forEach(function (u) { (per[u.maatregel] = per[u.maatregel] || []).push(u); });
    var out = {};
    bewijs.maatregelen.forEach(function (m) {
      var lijst = per[m.id] || [];
      out[m.id] = { soort: m.soort, uitkomst: uitkomst_maatregel(m.soort, lijst), regels: lijst };
    });
    return out;
  }
  return { toets_regel: toets_regel, toets_alles: toets_alles, uitkomst_maatregel: uitkomst_maatregel,
           dossier_uitkomsten: dossier_uitkomsten, SPIEGEL: SPIEGEL };
})();
```

Waarom de vergelijking byte-gelijk kan zijn: `toets.py` schrijft in de toelichting van `waarde_*` de
waarden met `json.dumps` (dus `true`, `"tekst"`), precies wat `JSON.stringify` in JS geeft; en Python
`1.0` en JS `1` zijn na `json.loads` gelijk.

- [ ] **Stap 4: draai alle tests, verwacht groen; commit**

```bash
git add check/bron/app.js tests/test_toets.py
git commit -m "check: app.js spiegelt toets.py, bewaakt met een node-vergelijking"
```

### Taak 12: `app.js`, deel 2: de drie stappen en het dossier, met Playwright-tests

**Files:**
- Modify: `check/bron/app.js` (UI-deel eronder, in een tweede IIFE)
- Create: `tests/fixtures/doorloop-2026-09.json`
- Create: `tests/test_app.py`
- Modify: `check/bron/index.html` (inhoud van de drie secties)

**Interfaces:**
- DOM-ids die de tests gebruiken: `#app-naam`, `#app-versie`, `#app-organisatie`, `#peildatum`,
  `#hosting` (select: `saas`/`eigen`), `#sso` (checkbox), `#bestanden` (`<input type="file" multiple>`),
  `#kolommen` (textarea, JSON-kolomkoppeling voor een CSV-log), `#onverenigbaar` (textarea, één paar per
  regel als `rol1;rol2`), `#toets-knop`, `#tabel-uitkomsten` (per maatregel een `<tr data-id="8.15.01" data-uitkomst="…">`),
  `#telling` (met `data-teller="aangetoond|gedeeltelijk|niet-aangetoond|geen-bewijs|handmatig|niet-aantoonbaar"`),
  `#dossier-json` (textarea met het dossier), `#opslaan-knop`, `#laden-bestand`, `#uitdraai-knop`.
- Globaal object `app` met `feitenVanBestanden(lijst: {naam, inhoud: string}[], kolommen, peildatum) -> feiten`
  (dezelfde herkenning als `doorloop.draai_bestanden`: JOIN aan de kopregel, `.json` als configuratie,
  anders CSV met kolommen), `maakDossier(meta, feiten, uitkomsten) -> dossier`, `laadDossier(json) -> void`.

- [ ] **Stap 1: maak de doorloop-fixture**

`tests/fixtures/doorloop-2026-09.json`: een compleet dossier zoals *De datamodellen* het beschrijft,
gemaakt uit de generieke fixtures. Maak hem met een klein eenmalig script (niet committen) dat
`doorloop.draai` aanroept en per maatregel `{"id", "soort", "uitkomst", "regels", "status": uitkomst,
"verantwoordelijke": "", "onderbouwing": "", "bevestigd_door_mens": false}` schrijft, met
`applicatie` = `{"naam": "Voorbeeld Zaaksysteem", "versie": "6.21", "organisatie": "Gemeente Voorbeeld", "hosting": "saas", "sso": true}`,
`peildatum` = `2026-09-01`, `ingevuld_door` = `"A. Voorbeeld"`, `bronbestanden` uit de feiten.

- [ ] **Stap 2: schrijf de falende browsertests**

```python
# tests/test_app.py
"""De pagina in een echte browser: aanleveren, toetsen, dossier opslaan en terugladen.

Wat op het scherm staat moet gelijk zijn aan toets.py op dezelfde bestanden. Overslaan als Playwright
ontbreekt; CI installeert hem.
"""
from __future__ import annotations

import json
import pathlib
import sys

import pytest

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "check"))
FIX = ROOT / "tests" / "fixtures"

import bouw as bouwer  # noqa: E402
import doorloop  # noqa: E402

sync_api = pytest.importorskip("playwright.sync_api", reason="playwright niet beschikbaar")


@pytest.fixture(scope="module")
def bestand(tmp_path_factory) -> str:
    return bouwer.bouw(tmp_path_factory.mktemp("dist")).as_uri()


@pytest.fixture(scope="module")
def browser():
    with sync_api.sync_playwright() as pw:
        b = pw.chromium.launch()
        yield b
        b.close()


@pytest.fixture
def pagina(browser, bestand):
    p = browser.new_page()
    p.goto(bestand)
    yield p
    p.close()


def aanleveren(p):
    p.fill("#app-naam", "Voorbeeld Zaaksysteem")
    p.fill("#app-versie", "6.21")
    p.fill("#app-organisatie", "Gemeente Voorbeeld")
    p.fill("#peildatum", "2026-09-01")
    p.select_option("#hosting", "saas")
    p.check("#sso")
    p.fill("#kolommen", (FIX / "generiek-log.kolommen.json").read_text(encoding="utf-8"))
    p.set_input_files("#bestanden", [str(FIX / "generiek-config.json"), str(FIX / "generiek-log.csv")])
    p.click("#toets-knop")


def test_scherm_is_gelijk_aan_toets_py(pagina):
    aanleveren(pagina)
    verwacht = doorloop.draai(FIX / "generiek-config.json", FIX / "generiek-log.csv",
                              FIX / "generiek-log.kolommen.json", "2026-09-01")
    rijen = pagina.locator("#tabel-uitkomsten tr[data-id]")
    assert rijen.count() == 148
    for i in range(rijen.count()):
        rij = rijen.nth(i)
        assert rij.get_attribute("data-uitkomst") == verwacht[rij.get_attribute("data-id")]["uitkomst"]
    telling = {}
    for m in verwacht.values():
        telling[m["uitkomst"]] = telling.get(m["uitkomst"], 0) + 1
    for naam, aantal in telling.items():
        assert pagina.locator(f'#telling [data-teller="{naam.replace(" ", "-")}"]').inner_text() == str(aantal)


def test_dossier_opslaan_en_terugladen(pagina, tmp_path):
    aanleveren(pagina)
    pagina.click('[data-stap="dossier"]')
    dossier = json.loads(pagina.input_value("#dossier-json"))
    assert dossier["formaat"] == "applicatiecheck-dossier" and dossier["versie"] == 1
    assert dossier["applicatie"]["naam"] == "Voorbeeld Zaaksysteem" and dossier["peildatum"] == "2026-09-01"
    assert len(dossier["maatregelen"]) == 148
    assert all(len(b["sha256"]) == 64 for b in dossier["bronbestanden"])
    # status aanpassen, opslaan, terugladen in een verse pagina
    pagina.select_option('#dossier tr[data-id="5.01.01"] select', "niet van toepassing")
    pagina.fill('#dossier tr[data-id="5.01.01"] textarea', "Beleid staat organisatiebreed vast.")
    aangepast = json.loads(pagina.input_value("#dossier-json"))
    m = [x for x in aangepast["maatregelen"] if x["id"] == "5.01.01"][0]
    assert m["status"] == "niet van toepassing" and m["uitkomst"] == "niet aantoonbaar"
    pad = tmp_path / "dossier.json"
    pad.write_text(json.dumps(aangepast), encoding="utf-8")
    pagina.reload()
    pagina.set_input_files("#laden-bestand", str(pad))
    pagina.click('[data-stap="dossier"]')
    herladen = json.loads(pagina.input_value("#dossier-json"))
    assert herladen == aangepast


def test_fixture_dossier_laadt_en_klopt(pagina):
    pagina.set_input_files("#laden-bestand", str(FIX / "doorloop-2026-09.json"))
    pagina.click('[data-stap="toetsen"]')
    fixture = json.loads((FIX / "doorloop-2026-09.json").read_text(encoding="utf-8"))
    for m in fixture["maatregelen"]:
        assert pagina.locator(f'#tabel-uitkomsten tr[data-id="{m["id"]}"]').get_attribute("data-uitkomst") == m["uitkomst"]


def test_geen_netwerkverkeer(browser, bestand):
    p = browser.new_page()
    verzoeken = []
    p.on("request", lambda r: verzoeken.append(r.url))
    p.goto(bestand)
    aanleveren(p)
    assert verzoeken == [bestand] or all(u.startswith("file:") for u in verzoeken)
    p.close()
```

- [ ] **Stap 3: draai de tests, verwacht rood** (`pip install playwright && python -m playwright install chromium` eerst; dan falen ze op ontbrekende elementen)

- [ ] **Stap 4: bouw de UI in `app.js` (tweede IIFE onder `toets`) en de secties in `index.html`**

De secties, letterlijk in `index.html` (vervang de drie lege `<section>`-elementen):

```html
  <section id="aanleveren" class="paneel">
    <h2>1. Aanleveren</h2>
    <div class="veld"><label for="app-naam">Applicatie</label><input id="app-naam" type="text"></div>
    <div class="veld"><label for="app-versie">Versie</label><input id="app-versie" type="text"></div>
    <div class="veld"><label for="app-organisatie">Organisatie</label><input id="app-organisatie" type="text"></div>
    <div class="veld"><label for="peildatum">Peildatum</label><input id="peildatum" type="date"></div>
    <div class="veld"><label for="hosting">Hosting</label><select id="hosting"><option value="saas">SaaS bij de leverancier</option><option value="eigen">Eigen hosting</option></select></div>
    <div class="veld"><label><input id="sso" type="checkbox"> Inloggen via de centrale identity provider (SSO)</label></div>
    <div class="veld"><label for="bestanden">Bestanden: configuratie-export (JSON), logsample (CSV/TSV), JOIN-exports</label><input id="bestanden" type="file" multiple></div>
    <div class="veld"><label for="kolommen">Kolomkoppeling voor een CSV-log (JSON: logveld → kolomkop)</label><textarea id="kolommen" rows="3">{"tijdstip": "", "identiteit": "", "actie": "", "object": "", "resultaat": "", "oorsprong": ""}</textarea></div>
    <div class="veld"><label for="onverenigbaar">Onverenigbare rollen (één paar per regel, gescheiden met ;)</label><textarea id="onverenigbaar" rows="3"></textarea></div>
    <div class="veld"><label for="laden-bestand">Of: een eerder dossier laden</label><input id="laden-bestand" type="file" accept=".json"></div>
    <p id="aanleveren-fout" class="fout" hidden></p>
    <button id="toets-knop" type="button">Toetsen</button>
  </section>
  <section id="toetsen" class="paneel" hidden>
    <h2>2. Toetsen</h2>
    <p id="telling"></p>
    <table id="tabel-uitkomsten"><thead><tr><th>Nr</th><th>Titel</th><th>Soort</th><th>Uitkomst</th><th>Regels</th></tr></thead><tbody></tbody></table>
  </section>
  <section id="dossier" class="paneel" hidden>
    <h2>3. Dossier</h2>
    <p>Per maatregel: de uitkomst van de regel, en jouw status met onderbouwing. De uitkomst verandert niet; de status is de menselijke keuze.</p>
    <table id="tabel-dossier"><thead><tr><th>Nr</th><th>Titel</th><th>Uitkomst</th><th>Status</th><th>Verantwoordelijke</th><th>Onderbouwing</th></tr></thead><tbody></tbody></table>
    <div class="veld"><label for="dossier-json">Dossier (JSON)</label><textarea id="dossier-json" rows="8" readonly></textarea></div>
    <button id="opslaan-knop" type="button">Dossier opslaan (JSON)</button>
    <button id="uitdraai-knop" type="button">Uitdraaien</button>
  </section>
```

Gedrag van de UI-IIFE (schrijf dit uit; de namen zijn bindend):

1. `stapToon(naam)`: zet `hidden` op alle `.paneel` behalve `#naam`, en `.actief` op de knop; koppel aan elke `.stap`-knop.
2. `lees(file) -> Promise<string>` met `FileReader.readAsText`.
3. `herkenEnParse(naam, inhoud, kolommen, peildatum, feiten)`: kopregel = eerste regel; als de kopregel alle
   waarden van `KOLOMMEN_AUDIT` bevat (kopieer de twee dicts uit `parsers/join.py` letterlijk naar JS als
   `JOIN.KOLOMMEN_AUDIT` / `JOIN.KOLOMMEN_ROLLEN`) → JOIN-audit; alle van `KOLOMMEN_ROLLEN` → JOIN-rollen;
   naam eindigt op `.json` → configuratie (zelfde velden overnemen als `generiek.lees_config_json`);
   anders CSV met `kolommen` (scheidingsteken = het vaakst voorkomende van `,` `;` tab in de kopregel;
   ontbrekende kolom → `throw new Error("kolom '…' voor … staat niet in …")`). JOIN-datums: `dd-mm-jjjj`
   + tijd naar ISO met `+02:00` bij maand 4 t/m 10 en `+01:00` anders (zomertijd op maandniveau; de
   Python-kant gebruikt de echte tijdzone, dus de browsertests gebruiken de generieke fixtures voor de
   scherm-vergelijking en de JOIN-fixture alleen via `doorloop.py`).
4. `sha256(tekst) -> Promise<string>` via `crypto.subtle.digest('SHA-256', new TextEncoder().encode(tekst))`
   (werkt offline, valt niet onder de CSP). Elk bronbestand krijgt `{naam, soort, sha256, peildatum}`.
5. `feitenVanBestanden(lijst, kolommen, peildatum)`: start met een leeg feiten-object (zelfde vorm als
   `parsers.feiten.leeg()`), verwerk elk bestand, zet `instellingen.sso_afgedwongen` op de waarde van
   `#sso` als de export hem niet zelf zet, en `instellingen.onverenigbare_rollen` uit `#onverenigbaar`
   (elke regel `a;b` → `["a","b"]`) als er iets is ingevuld.
6. Klik op `#toets-knop`: lees de velden, lees de bestanden, bouw feiten, `uitkomsten = toets.dossier_uitkomsten(BRON.bewijs, BRON.regels, feiten, peildatum)`,
   vul `#tabel-uitkomsten` (één `<tr data-id data-uitkomst>` per maatregel in de volgorde van `bewijs.json`,
   met class `uitkomst-<uitkomst met spaties als streepjes>` op de uitkomstcel en per regel de toelichting),
   vul `#telling` met `<span data-teller="…">n</span>` per uitkomst (koppeltekens in plaats van spaties),
   bouw het dossier (`maakDossier`) en toon stap 2. Fouten in `#aanleveren-fout` (tekst, `hidden` weg).
7. `maakDossier(meta, feiten, uitkomsten)`: exact het dossier-schema; `bron_versie` uit
   `BRON.bio2.bron.versie`; per maatregel `status` = `uitkomst`, `verantwoordelijke` = `""`, `onderbouwing` = `""`,
   `bevestigd_door_mens` = `false`. Sla het dossier in een variabele `huidig` en schrijf
   `JSON.stringify(huidig, null, 1)` in `#dossier-json`.
8. `#tabel-dossier`: per maatregel een rij met `<select>` (opties: alle `UITKOMSTEN` plus `explain`),
   `<input>` verantwoordelijke, `<textarea>` onderbouwing; elke wijziging werkt `huidig` bij (en zet
   `bevestigd_door_mens` op `true` voor die rij) en schrijft `#dossier-json` opnieuw.
9. `#opslaan-knop`: maak een `Blob` van `#dossier-json`, `URL.createObjectURL`, een tijdelijke `<a download="applicatiecheck-<naam>-<peildatum>.json">`, klik, `revokeObjectURL`.
10. `#laden-bestand`: lees JSON, `laadDossier(json)`: valideer `formaat`/`versie`, zet `huidig`, vul de
    invoervelden uit `applicatie`/`peildatum`, vul beide tabellen uit `huidig.maatregelen` (uitkomst uit het
    dossier, niet opnieuw getoetst), toon stap 3.
11. `#uitdraai-knop`: `window.print()`; in `app.css` een `@media print` die de knoppen en `#dossier-json`
    verbergt en beide tabellen toont.

- [ ] **Stap 5: draai alle tests, verwacht groen**

Run: `python -m pytest tests/ -v`
Verwacht: alles groen, inclusief de vier browsertests. Faalt `test_scherm_is_gelijk_aan_toets_py` op één
maatregel: vergelijk de regeluitkomst in de browser (`console.log` in de rij) met `doorloop.py`; het
verschil zit vrijwel altijd in datumparsing of in `leeg()`.

- [ ] **Stap 6: commit**

```bash
git add check/bron/app.js check/bron/index.html check/bron/app.css tests/test_app.py tests/fixtures/doorloop-2026-09.json
git commit -m "check: de pagina met aanleveren, toetsen en dossier, bewaakt met browsertests"
```

### Taak 13: publiceren op `/applicatiecheck/check/`, CI met browserjob, label naar prototype

**Files:**
- Modify: `.github/workflows/pages.yml` (vervang de herbruikbare aanroep door eigen stappen)
- Modify: `.github/workflows/ci.yml` (browserjob erbij)
- Modify: `README.md` (Status en Snel starten)
- Modify (andere repo, gated door statuut B12): `.github/profile/README.md` in `security-commons-nl/.github`

- [ ] **Stap 1: `pages.yml`** (de tool moet naast de leesversie in dezelfde artifact)

```yaml
name: Build and deploy Pages

on:
  push:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: pages
  cancel-in-progress: true

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v6
      - uses: actions/setup-node@v6
        with:
          node-version: 24
          cache: npm
      - uses: actions/setup-python@v6
        with:
          python-version: "3.12"
      - run: npm ci
      - run: node site/build.mjs          # leesversie -> dist/
      - run: python check/bouw.py dist/check   # de tool -> dist/check/index.html
      - uses: actions/upload-pages-artifact@v5
        with:
          path: dist
  deploy:
    needs: build
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - id: deployment
        uses: actions/deploy-pages@v5
```

- [ ] **Stap 2: `ci.yml`**: voeg een job `check` toe (na `bewijs`), gekopieerd van de job `check` in
  `aanvalspaden/.github/workflows/ci.yml`, met deze stappen: checkout; setup-python 3.12;
  `pip install pytest tzdata playwright && python -m playwright install --with-deps chromium`; setup-node 24;
  `python check/bouw.py`; `python -m pytest tests/ -v`; upload-artifact van `check/dist/index.html`.
  De job `bewijs` blijft zoals hij is.

- [ ] **Stap 3: README**: `Status: concept. …` wordt
  `Status: prototype. De toets werkt in de browser op een configuratie-export en een logsample (generiek en JOIN); dossier opslaan en uitdraaien werkt. Geen belofte over onderhoud.`
  In *Snel starten* bovenaan: `1. Open de [toets](https://security-commons-nl.github.io/applicatiecheck/check/) in je browser.` en de stappen 2 t/m 4 (aanleveren, toetsen, dossier) in de stijl van de CSIR-README.

- [ ] **Stap 4: projectentabel** (statuut B12: eerst de tabel, dan de README): in
  `security-commons-nl/.github`, `profile/README.md`, de rij van applicatiecheck: `concept` → `prototype`,
  `[Ontwerp](…/applicatiecheck/)` → `[Live tool](https://security-commons-nl.github.io/applicatiecheck/check/)`.
  Commit daar: `profiel: applicatiecheck naar prototype, live tool`. Push, wacht tot de statuut-run van
  applicatiecheck groen is (hij vergelijkt beide).

- [ ] **Stap 5: commit en push in applicatiecheck; controleer live**

```bash
git add .github/workflows/pages.yml .github/workflows/ci.yml README.md
git commit -m "check: tool gepubliceerd op /check/, browserjob in CI, status prototype"
git push
```

Daarna: `curl -s -o /dev/null -w '%{http_code}' https://security-commons-nl.github.io/applicatiecheck/check/` moet `200` geven en `gh run list -R security-commons-nl/applicatiecheck --limit 3` alleen `success`.

**F3 is klaar als:** de tool live staat, alle CI-jobs groen zijn, de projectentabel *prototype* zegt en de statuut-run groen is.

---

## F4 · AI voor bewijssoort C, met eigen sleutel

### Taak 14: `ai.js`: één aanroep, alleen na een klik, alleen voor C, altijd *wacht op bevestiging*

**Files:**
- Create: `check/bron/ai.js`
- Modify: `check/bouw.py` (ai.js in de scripttag; CSP krijgt `connect-src https://api.mistral.ai`)
- Modify: `check/bron/index.html` (sleutelveld en per C-maatregel een knop)
- Modify: `tests/test_bouw.py`, `tests/test_app.py`

**Interfaces:**
- Produces: globaal `ai` met `extraheer(sleutel, maatregel, tekst) -> Promise<{feiten: object, toelichting: string}>`
  en `prompt(maatregel) -> string`. De aanroep: `POST https://api.mistral.ai/v1/chat/completions`, headers
  `Authorization: Bearer <sleutel>`, `Content-Type: application/json`, body
  `{"model": "mistral-small-latest", "temperature": 0, "response_format": {"type": "json_object"}, "messages": [{"role": "system", "content": prompt(maatregel)}, {"role": "user", "content": tekst}]}`.
  Het antwoord is JSON `{"feiten": {...}, "toelichting": "..."}`.

- [ ] **Stap 1: test op de bouw (onderaan `tests/test_bouw.py`)**

```python
def test_csp_laat_alleen_mistral_toe_als_verbinding(html):
    csp = re.search(r'Content-Security-Policy" content="([^"]+)"', html).group(1)
    assert "connect-src https://api.mistral.ai" in csp
    assert "default-src 'none'" in csp


def test_ai_alleen_na_klik_en_alleen_voor_c(html):
    assert "api.mistral.ai" in html
    assert 'id="ai-sleutel"' in html
    assert "sessionStorage" in html and "localStorage" not in html
```

Pas `test_geen_externe_verwijzing` aan: `fetch(` is nu toegestaan in precies één functie; vervang de
assert door: het aantal voorkomens van `fetch(` in de scripttag is exact 1, en het enige adres buiten de
commons is `https://api.mistral.ai/v1/chat/completions`.

- [ ] **Stap 2: draai de test, verwacht rood**

- [ ] **Stap 3: implementeer**

`check/bron/ai.js`:

```javascript
// AI alleen voor bewijssoort C: een document of schermafbeelding (als tekst) naar feiten. Nooit een oordeel.
// Eén aanroep, na een klik, met de sleutel van de gebruiker (sessionStorage, dus weg bij sluiten van het tabblad).
var ai = (function () {
  'use strict';
  var URL_MISTRAL = 'https://api.mistral.ai/v1/chat/completions';

  function prompt(maatregel) {
    return 'Je leest bewijs voor BIO2-maatregel ' + maatregel.id + ' (' + maatregel.titel + '). ' +
      'Haal er alleen feiten uit die er letterlijk in staan en geef ze terug als JSON met twee sleutels: ' +
      '"feiten" (een object met korte sleutel-waardeparen, bijvoorbeeld {"mfa_beleid_idp": true, "bron": "schermafbeelding Entra"}) ' +
      'en "toelichting" (één zin, Nederlands, wat je hebt gezien). Oordeel niet of de maatregel is aangetoond; ' +
      'dat doet de regel. Staat er niets bruikbaars in, geef dan {"feiten": {}, "toelichting": "geen bruikbaar bewijs gevonden"}.';
  }

  function extraheer(sleutel, maatregel, tekst) {
    return fetch(URL_MISTRAL, {
      method: 'POST',
      headers: { 'Authorization': 'Bearer ' + sleutel, 'Content-Type': 'application/json' },
      body: JSON.stringify({
        model: 'mistral-small-latest', temperature: 0, response_format: { type: 'json_object' },
        messages: [{ role: 'system', content: prompt(maatregel) }, { role: 'user', content: tekst }]
      })
    }).then(function (r) {
      if (!r.ok) throw new Error('Mistral antwoordde ' + r.status);
      return r.json();
    }).then(function (j) {
      var inhoud = JSON.parse(j.choices[0].message.content);
      return { feiten: inhoud.feiten || {}, toelichting: inhoud.toelichting || '' };
    });
  }
  return { extraheer: extraheer, prompt: prompt, URL_MISTRAL: URL_MISTRAL };
})();
```

`check/bouw.py`: neem `ai.js` op in de scripttag (`for n in ("patronen.js", "app.js", "ai.js")`) en wijzig de
CSP in `index.html` naar
`default-src 'none'; script-src 'sha256-__SCRIPT_HASH__'; style-src 'sha256-__STYLE_HASH__'; img-src data:; connect-src https://api.mistral.ai; form-action 'none'; base-uri 'none'`
(en pas `test_csp_klopt_met_de_inhoud` aan op die string).

`index.html`, in `#aanleveren` onder het SSO-veld:

```html
    <div class="veld"><label for="ai-sleutel">Mistral-sleutel (optioneel, alleen voor document-bewijs; blijft in dit tabblad)</label><input id="ai-sleutel" type="password" autocomplete="off"></div>
```

In de UI-IIFE: bewaar de sleutel in `sessionStorage` onder `applicatiecheck-mistral`; in `#tabel-dossier`
krijgt elke maatregel met soort `C` een `<textarea class="c-tekst">` (geplakte tekst van het document of
de schermafbeelding, bijvoorbeeld via OCR elders) en een knop `<button class="ai-knop" data-id="…">Lees met AI</button>`
die alleen actief is als er een sleutel is. Klik: `ai.extraheer(sleutel, maatregel, tekst)` → in `huidig`
bij die maatregel `ai: {feiten, toelichting, status: "wacht op bevestiging"}`; de rij toont de toelichting
en een checkbox *Bevestigd*; pas na aanvinken wordt `bevestigd_door_mens` `true` en `status` mag door de
gebruiker op `aangetoond` worden gezet. De regeluitkomst (`uitkomst`) verandert nooit door AI.

- [ ] **Stap 4: browsertest zonder echte sleutel (onderaan `tests/test_app.py`)**

```python
def test_ai_knop_zonder_sleutel_is_uit_en_met_sleutel_gaat_er_precies_een_verzoek(browser, bestand):
    p = browser.new_page()
    verzoeken = []
    p.route("https://api.mistral.ai/**", lambda route: (verzoeken.append(route.request.post_data),
        route.fulfill(status=200, content_type="application/json",
                      body=json.dumps({"choices": [{"message": {"content": json.dumps({"feiten": {"mfa_beleid_idp": True}, "toelichting": "MFA-beleid gezien"})}}]}))))
    p.goto(bestand)
    aanleveren(p)
    p.click('[data-stap="dossier"]')
    knop = p.locator('.ai-knop[data-id="8.13.04"]')
    assert knop.is_disabled()
    p.fill("#ai-sleutel", "testsleutel")
    p.fill('#dossier tr[data-id="8.13.04"] .c-tekst', "Hersteltest uitgevoerd op 15-08-2026, geslaagd.")
    knop.click()
    p.wait_for_selector('#dossier tr[data-id="8.13.04"] .ai-toelichting')
    assert len(verzoeken) == 1 and "mistral-small-latest" in verzoeken[0]
    d = json.loads(p.input_value("#dossier-json"))
    m = [x for x in d["maatregelen"] if x["id"] == "8.13.04"][0]
    assert m["ai"]["status"] == "wacht op bevestiging" and m["bevestigd_door_mens"] is False
    assert m["uitkomst"] == "handmatig"
    p.close()
```

- [ ] **Stap 5: draai alle tests, verwacht groen; commit en push**

```bash
git add check/bron/ai.js check/bouw.py check/bron/index.html check/bron/app.js tests/test_bouw.py tests/test_app.py
git commit -m "check: AI-extractie voor bewijssoort C met eigen sleutel, altijd wacht op bevestiging"
git push
```

**F4 is klaar als:** alle tests groen, de live pagina zonder sleutel geen enkel verzoek doet
(`test_geen_netwerkverkeer` blijft groen), en de README onder *Drie ontwerpregels* een zin heeft over de
sleutel in `sessionStorage` en de ene toegestane verbinding in de CSP.

---

## Zelfcontrole van dit deel (gedaan bij het schrijven)

- **Dekking van deel 1:** bewijsmodel (F0, bestaat) · regels als data met gesloten toetsset (taak 3, 4) ·
  referentie in Python en spiegel in JS met een test dat beide gelijk zijn (taak 4, 11) · generieke parser
  en JOIN-parser op synthetische fixtures (taak 5, 7) · logsample als structuurtoets met PII-scan (taak 2, 9,
  regel 8.15.02) · pagina met drie stappen, dossier-schema, opslaan en uitdraaien, CSP (taak 10, 12) ·
  publicatie en label prototype (taak 13) · AI alleen voor C, eigen sleutel, wacht op bevestiging (taak 14).
- **Bewust niet in dit deel:** het dossier-schema delen met de CSIR-tool (afstemmen met de auteur, A4),
  de proxy als AI-route (apart besluit), de omzetting naar `normen` als bron (volgt het normen-plan).
- **Namen die overal gelijk moeten zijn:** `toets_regel`, `toets_alles`, `uitkomst_maatregel`,
  `dossier_uitkomsten` (Python en JS); `patronen.zoek`; de zeven uitkomsten; de feiten-sleutels
  `instellingen`, `vorige_instellingen`, `accounts`, `rollen`, `logtypen`, `logregels`, `koppelingen`,
  `bronbestanden`; de regel-ids uit taak 3.
