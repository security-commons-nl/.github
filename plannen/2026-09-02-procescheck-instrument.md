# Bouwplan: procescheck als instrument (BIA en BIV in de browser)

**Doel:** procescheck ombouwen van een applicatie (React, FastAPI, PostgreSQL, Azure AD) naar een
instrument in de vorm van de zelfcheck en de CSIR Assessment Tool: één pagina die in de browser rekent,
met de kritieke processen, hun applicaties, de BIA/BIV-classificatie, RTO/RPO en de businesscontext als
één dossier dat de organisatie zelf bewaart.

**Aanleiding:** fase 4 van het plan *lichte commons* (02-09-2026). procescheck is inhoudelijk een formulier
met regels: zes vragen op een schaal van vijf, een rekenregel die daaruit de klasse afleidt, en een
dashboard dat telt. Dat is precies wat het CSIR-patroon doet. Wat het nu een applicatie maakt (database,
inlog, exportserver, auditlog voor meerdere gebruikers) is geen inhoud maar hosting, en hosting is de
drempel die de commons wil weghalen. Bovendien ontsluit de ombouw de koppeling uit `aanvalspaden#4`: een
object met industriële automatisering als systeem onder een proces, twee JSON-dossiers die naar elkaar
verwijzen.

**Architectuur:** dezelfde repo, dezelfde naam en URL. De applicatiecode gaat na livegang van `main` af
(tag `v0-applicatie` op de laatste applicatiecommit; de historie blijft). Mapstructuur en bouwketen zijn
die van `csir-assessment-tool/register/`, en dit plan verwijst daarnaar in plaats van alles te herhalen:
lees `2026-09-01-csir-keten.md` hoofdstuk 2, 5, 6, 8, 9, 10 en 14 als het uitgewerkte voorbeeld.

**Tech stack:** Python 3.12 (bouwscript, referentie, tests), vanilla JS en CSS, pytest, Playwright. Geen
dependencies in de pagina.

**Status:** geschreven 02-09-2026 op de feiten in de repo (frontend 5.886 regels, backend 3.316 regels).
Wacht op afstemming met de mede-auteur en daarna op uitvoering.

---

## 0. Besluiten (de spec)

1. **Inhoud en rekenregels blijven exact wat ze zijn.** De zes vragen, de vijf antwoordklassen met hun
   toelichting, de afleiding van RTO/RPO/WRT/MTPD uit de klassen, de aggregatie en de dashboardregels
   komen letterlijk uit de huidige code (hoofdstuk 1). Wat verandert is waar het draait, niet wat het
   rekent. De bron wordt `procescheck.json`, gehaald uit `frontend/src/pages/Bia/BiaPage.tsx` en
   `Docs/MTPD-RTO-WRT-RPO-classificatie.md`, met een test die de teksten tegen die bestanden legt zolang
   ze in de historie staan.
2. **Eén dossier per organisatie, met alle processen erin.** Niet één proces per bestand: het dashboard
   telt over processen heen, en de kroonjuwelenlijst is een selectie uit de hele lijst. Het dossier is
   JSON, opgeslagen en teruggelezen door de gebruiker, met de vingerafdruk van de bron erin.
3. **Wat vervalt:** inlog (Azure AD), de auditlog (die bestaat voor meerdere gebruikers op één database; in
   een dossier op je eigen schijf is git of een gedateerde kopie de audit trail), de exportserver (xlsx,
   docx, pptx) en de Docker-omgeving. Wat ervoor in de plaats komt: opslaan als JSON en een printbare
   uitdraai per sectie.
4. **Wat erbij komt, klein:** per applicatie een `soort` (`applicatie` of `object met industriële
   automatisering`) en een optionele verwijzing naar een CSIR-dossier (bestandsnaam en vingerafdruk). Dat
   is de haak van `aanvalspaden#4`; hij kost twee velden en verplicht tot niets.
5. **De kroonjuwelenlijst is een uitdraai.** Stap 1 van `risicoanalyse-aanvalspaden` vraagt maximaal tien
   kroonjuwelen met eigenaar en de systemen eronder; het dossier levert die tabel op basis van
   `is_critical` en de klasse, in de vorm van `sjabloon-matrix.md`. Zo wordt procescheck de bron voor
   diepte 1 zonder dat er iets aan elkaar geknoopt hoeft te worden.
6. **blast-radius gaat hierin op** (besluit 02-09, plan *lichte commons* fase 6): een landschapsexport (CSV of
   JSON, het formaat van `blast-radius/testdata/landschap.json`) is te importeren in het dossier als de laag
   componenten onder de applicaties; een tab *Blast radius* toont per component wat er omvalt, als lijst en
   als SVG, en de uitdraai neemt de keten proces → applicatie → component mee. De parser en de rekenregel
   komen uit `blastradius/`; de CLI-repo wordt gearchiveerd zodra dit live is.
7. **Mede-auteur eerst.** Vasilis Theocharis is mede-auteur van procescheck. Het plan gaat naar hem vóór
   er gebouwd wordt; zijn opmerkingen komen in hoofdstuk 7.

## 1. Wat er nu is (uit de code, 02-09-2026)

**Schaal.** Vijf klassen, 1 is het ergst: 1 Catastrofaal · 2 Kritiek / zeer ernstig · 3 Gemiddeld ·
4 Gering · 5 Verwaarloosbaar (`biaShared.tsx`, `SCORE_LABELS`).

**Vragen.** Zes in gebruik (`BiaPage.tsx`, `B_QUESTIONS`, `I_QUESTIONS`, `V_QUESTIONS`), elk met een
toelichting per klasse; het datamodel heeft ruimte voor 22 (`b1..b8`, `i1..i7`, `v1..v7`) maar
de overige zestien zijn nergens in gebruik en gaan niet mee.

| Sleutel | Vraag (verkort) | Levert |
|---|---|---|
| `b1` | Maximale uitvalduur voordat onaanvaardbare gevolgen optreden | RTO-klasse |
| `b2` | Maximale hoeveelheid dataverlies die acceptabel is | RPO-klasse |
| `b3` | Tijd om na herstel de achterstand in te halen | WRT-klasse |
| `b4` | Maximale tijd dat het proces stil kan liggen, alles bij elkaar | MTPD-klasse |
| `i1` | Impact als informatie onjuist, onvolledig of gemanipuleerd is | I-score |
| `v1` | Impact als informatie ongeautoriseerd wordt ingezien of verspreid (openbaar tot geheim) | V-score |

**Rekenregels** (`biaShared.tsx` `highestSeverity`, `BiaPage.tsx` regel 209-230 en 367):
- `B = min(b1, b2, b3, b4)` over de ingevulde waarden (de laagste klasse is de ernstigste); `I = i1`;
  `V = v1`. Ontbreekt alles, dan geen score.
- `procesklasse = min(B, I, V)`.
- RTO, RPO, WRT en MTPD zijn de klasselabels bij `b1`, `b2`, `b3`, `b4` (`PARAM_MAP`), met de tabel uit
  `Docs/MTPD-RTO-WRT-RPO-classificatie.md` als uitleg. Het losse RTO/RPO-model (`rto_value`, `rto_unit`,
  `rpo_value`, `rpo_unit`, `explanation`) blijft als expliciete overschrijving; "RTO/RPO gedefinieerd"
  betekent volgens de backend: `b1` en `b2` ingevuld (`dashboard.py` `_has_rto_rpo`).

**Dashboardregels** (`backend/app/routers/dashboard.py`):
- Volledigheid per proces, tien controles: beschrijving, doelstelling, eigenaar, afdeling, laatste
  beoordelingsdatum, reden kritiek (als kritiek), gekoppelde applicaties, BIA/BIV, RTO/RPO, businesscontext.
- Hoog risico: een van B, I, V is 1 of 2.
- Prioriteit: kritiek zonder BIA → *critical*; hoog risico zonder RTO/RPO → *high*; kritiek en onvolledig →
  *high*; vier of meer ontbrekende velden → *medium*; anders *low*.
- Tellers: totaal, kritiek, compleet, aandacht, onvolledig; verdeling per dimensie; top-processen per
  dimensie; dekking van velden; privacy-blootstelling.

**Gegevens** (`backend/app/models/`, `frontend/src/types/index.ts`):
- Proces: `code`, `name`, `description`, `objective`, `owner`, `department`, `is_critical`,
  `critical_reason`, `last_assessment_date`, `notes`.
- Applicatie: `code`, `name`, `description`, `business_owner`, `technical_owner`, `notes`, `review_date`;
  m:n met processen.
- BIA: de zes scores plus per score een `_arg` (onderbouwing), `interviewer_name`, `interview_date`,
  `general_description`, `chain_dependencies`, `owner_deviation_motivation`, `notes`.
- RTO/RPO: waarde en eenheid voor beide, `explanation`.
- Businesscontext: het canvas (`key_partners`, `key_activities`, `key_resources`, `value_proposition`,
  `customer_relationships`, `channels`, `customer_segments`, `cost_structure`, `revenue_streams`),
  `legal_basis`, `stakeholders`, `chain_position`, en de velden voor privacy en continuïteit die de export
  onder *Privacy* en *Continuïteit* zet.

**Export** (`ExportPage.tsx`): secties processen, applicaties, koppelingen, canvas, wettelijk en
stakeholders, privacy, continuïteit, ketenarchitectuur; formaten xlsx, docx, pptx via de backend.

## 2. Doelstructuur

```
procescheck/
├── README.md · CONTRIBUTING.md · LICENSE (EUPL-1.2, al zo sinds 30-08)
├── procescheck.json             DE BRON: schaal, zes vragen met toelichtingen, parameterlabels, dashboardregels als data
├── werkwijze.md                 de vijf doelen uit Docs/Requirements application.md, herschreven naar de instrumentvorm
├── verantwoording.md            waar de vragen vandaan komen (Template BIA & BIV-Classificatie.xlsx), wat eigen invulling is
├── Docs/MTPD-RTO-WRT-RPO-classificatie.md   blijft, wordt de uitleg bij b1..b4
├── instrument/
│   ├── LEESMIJ.md
│   ├── haal_bron.py             eenmalig: vragen en teksten uit BiaPage.tsx (tag v0-applicatie) naar procescheck.json
│   ├── reken.py                 referentie: scores, klasse, parameterlabels, volledigheid, prioriteit, tellers
│   ├── bouw.py                  → instrument/dist/index.html (CSP, één script, één stylesheet)
│   ├── bron/index.html · app.css · app.js
│   └── tests/ test_bron.py · test_reken.py · test_bouw.py · test_app.py · fixtures/doorloop-2026-09.json
├── site/                        gedeelde site-build voor /uitleg/
└── .github/workflows/ ci.yml · pages.yml · statuut.yml
```

Weg van `main` na livegang: `backend/`, `frontend/`, `docker-compose.yml`, `Docs/Azure-Deployment-Handleiding.md`.

## 3. De pagina

Tabbladen, in deze volgorde, met dezelfde id-conventie als de CSIR-tool (`#tab-<naam>`, `#scherm-<naam>`):

| Tab | Wat | Uit welke code |
|---|---|---|
| Processen | lijst met code, naam, eigenaar, afdeling, kritiek (ja/nee + reden), klasse (B/I/V en procesklasse), volledigheid; toevoegen, wijzigen, verwijderen | `ProcessesPage`, `Process` |
| Applicaties | lijst met code, naam, eigenaren, `soort`, koppeling aan processen, optionele CSIR-verwijzing | `Application`, `process_application` |
| BIA en BIV | per proces: de zes vragen met de vijf antwoorden en hun toelichting als hulptekst, per vraag een onderbouwing, de afgeleide B/I/V en procesklasse, RTO/RPO/WRT/MTPD als labels met de tabel erbij, expliciete RTO/RPO-overschrijving, interviewgegevens | `BiaPage`, `biaShared`, `Docs/MTPD…` |
| Businesscontext | per proces het canvas, wettelijke basis, stakeholders, ketenpositie, privacy, continuïteit | `BusinessContext` |
| Dashboard | de tellers en de prioriteitenlijst, met `data-teller`-attributen | `dashboard.py` |
| Uitdraai | per sectie van de oude export een hoofdstuk, plus **Kroonjuwelen**: de kritieke processen gesorteerd op klasse, met eigenaar en de applicaties eronder, in de kolommen van `sjabloon-matrix.md` | `ExportPage`, methode stap 1 |

Dossierbalk zoals de CSIR-tool: opslaan (JSON), laden, afdrukken, wissen, statusregel.

## 4. Dossierformaat

```json
{
  "formaat": "procescheck-dossier", "versie": 1, "bron_versie": "2026-09", "bron_sha256": "…", "bijgewerkt": "…",
  "organisatie": {"naam": "", "peildatum": ""},
  "processen": [{"code": "P01", "naam": "", "beschrijving": "", "doelstelling": "", "eigenaar": "", "afdeling": "",
                 "kritiek": false, "reden_kritiek": "", "laatste_beoordeling": "", "notities": "",
                 "applicaties": ["A01"],
                 "bia": {"b1": null, "b2": null, "b3": null, "b4": null, "i1": null, "v1": null,
                         "onderbouwing": {"b1": "", "b2": "", "b3": "", "b4": "", "i1": "", "v1": ""},
                         "interviewer": "", "interviewdatum": "", "beschrijving": "", "ketenafhankelijkheden": "",
                         "afwijking_eigenaar": "", "notities": ""},
                 "rto_rpo": {"rto": null, "rto_eenheid": "", "rpo": null, "rpo_eenheid": "", "toelichting": ""},
                 "context": {"canvas": {}, "wettelijke_basis": "", "stakeholders": "", "ketenpositie": "",
                             "privacy": {}, "continuiteit": {}}}],
  "applicaties": [{"code": "A01", "naam": "", "beschrijving": "", "eigenaar_business": "", "eigenaar_technisch": "",
                   "soort": "applicatie", "csir_dossier": {"bestand": "", "vingerafdruk": ""}, "notities": "",
                   "reviewdatum": ""}]
}
```

Sleutels zijn de codes; codes zijn uniek binnen het dossier en de pagina bewaakt dat. B, I, V en de
procesklasse staan niet in het dossier: ze zijn afgeleid en worden bij het laden herrekend, zodat een
dossier nooit een klasse kan bevatten die niet uit de antwoorden volgt.

## 5. Tests

Dezelfde vier bestanden als bij de CSIR-tool, met dezelfde definitie van klaar. Wat specifiek is:

- `test_bron.py`: de zes vragen, hun zes maal vijf toelichtingen en de vijf klasselabels zijn woordelijk
  gelijk aan `BiaPage.tsx` en `biaShared.tsx` op tag `v0-applicatie` (de test leest die bestanden met
  `git show v0-applicatie:frontend/src/pages/Bia/BiaPage.tsx`); de parametertabel is gelijk aan
  `Docs/MTPD-RTO-WRT-RPO-classificatie.md`.
- `test_reken.py`: `B = min` over ingevulde waarden, ontbrekende waarden tellen niet mee; procesklasse =
  min(B, I, V); hoog risico bij 1 of 2; de vier prioriteiten in de volgorde van `dashboard.py`; de tien
  volledigheidscontroles; tellers gelijk aan een doorloop-fixture.
- `test_bouw.py`: als bij de CSIR-tool, plus: `app.js` bevat geen vraagtekst en geen klasselabel.
- `test_app.py`: proces aanmaken, zes vragen invullen, klasse op het scherm gelijk aan `reken.py`;
  applicatie koppelen; dashboard gelijk aan de referentie; opslaan, laden, wissen, herladen; uitdraai bevat
  de kroonjuwelentabel met alleen de kritieke processen, gesorteerd op klasse.

## 6. Volgorde

0. Plan naar de mede-auteur. Zijn opmerkingen in hoofdstuk 7.
1. Tag `v0-applicatie` op de huidige `main`.
2. `haal_bron.py` en `procescheck.json`; `test_bron.py` groen.
3. `reken.py`; `test_reken.py` groen met een voorlopige fixture.
4. Pagina, in de volgorde van de tabs; per tab de bijbehorende browsertests groen.
5. Uitdraai en kroonjuwelen; `test_app.py` volledig groen.
6. Workflows, `LEESMIJ.md`, README (B11), `werkwijze.md`, `verantwoording.md`; Pages live op
   `/procescheck/` met `/uitleg/`.
7. Applicatiecode van `main`; profiel: *Leesbare versie* wordt *Live tool*; status blijft *prototype* tot
   iemand het echt gebruikt.
8. `aanvalspaden#4` uitvoeren: de CSIR-tool krijgt een verwijzingsveld naar een procescheck-dossier.

## 7. Open bij de mede-auteur

- De zestien ongebruikte vraagslots (`b5..b8`, `i2..i7`, `v2..v7`): waren die bedoeld voor een uitbreiding
  die nog komt, of restanten van het Excel-sjabloon? Dit plan laat ze weg.
- De auditlog: is er een gebruiker die hem nodig heeft, of was hij er omdat een database er een vraagt?
- Eén dossier per organisatie (dit plan) of per proces? Het eerste maakt het dashboard mogelijk, het tweede
  maakt delen per proces makkelijker. Beide kunnen ook: per proces exporteren uit het organisatiedossier.
