# Bouwplan: procescheck als instrument (BIA, BIV en blast radius in de browser)

**Doel:** procescheck ombouwen van een applicatie (React, FastAPI, PostgreSQL, Azure AD) naar een
instrument in de vorm van de zelfcheck en de CSIR Assessment Tool: één pagina die in de browser rekent,
met de kritieke processen, hun applicaties en componenten, de BIA/BIV-classificatie, RTO/RPO, de
businesscontext en de blast radius als één dossier dat de organisatie zelf bewaart.

**Aanleiding:** fase 4 en 6 van het plan *lichte commons* (02-09-2026). procescheck is inhoudelijk een
formulier met regels: zes vragen op een schaal van vijf, een rekenregel die daaruit de klasse afleidt, en
een dashboard dat telt. Wat het nu een applicatie maakt (database, inlog, exportserver, auditlog) is geen
inhoud maar hosting. `blast-radius` beantwoordt op dezelfde data de vraag "wat valt er om" en gaat hierin op
(besluit 02-09). De ombouw ontsluit bovendien `aanvalspaden#4`: een object met industriële automatisering
als systeem onder een proces.

**Architectuur:** dezelfde repo, dezelfde naam en URL. Mapstructuur, bouwketen en tests zijn die van
`csir-assessment-tool/register/`; waar dit plan "als bij de CSIR-tool" zegt, is
`2026-09-01-csir-keten.md` de uitgewerkte referentie (hoofdstuk 2, 5, 6, 8, 9, 10 en 14 daar). Alles wat
hier afwijkt of specifiek is, staat hier volledig uitgeschreven.

**Tech stack:** Python 3.12 (bouwscript, referentie, tests), vanilla JS en CSS, pytest, Playwright. Geen
dependencies in de pagina. Geen `dagre`, geen `d3`: de graaf wordt een SVG met een eigen laagindeling
(hoofdstuk 7).

**Status:** geschreven 02-09-2026 op de feiten in de repo (`procescheck` frontend 5.886 regels, backend
3.316 regels; `blast-radius` 1.252 regels). Uitvoerbaar zonder verdere afstemming; alle eerder open punten
zijn in hoofdstuk 0 beslist. Geschreven om door een minder sterk model gebouwd te kunnen worden: waar iets
niet in dit plan staat, volg je het CSIR-plan.

---

## 0. Besluiten (de spec)

1. **Inhoud en rekenregels blijven exact wat ze zijn.** De zes vragen, de vijf antwoordklassen met hun
   toelichting, de afleiding van RTO/RPO/WRT/MTPD, de aggregatie, de tien volledigheidscontroles, de
   prioriteitsregels en de reviewregel komen letterlijk uit de huidige code (hoofdstuk 1). De bron wordt
   `procescheck.json`, gehaald uit de code op tag `v0-applicatie`; een test legt de teksten daar tegenaan.
2. **De zestien ongebruikte vraagslots** (`b5..b8`, `i2..i7`, `v2..v7`) gaan niet mee. Ze worden nergens in
   de frontend gesteld; ze zijn restanten van het Excel-sjabloon. Wie ze ooit nodig heeft, voegt ze aan
   `procescheck.json` toe; de pagina rendert wat in de bron staat.
3. **Eén dossier per organisatie, met alle processen erin.** Het dashboard telt over processen heen en de
   kroonjuwelenlijst is een selectie uit de hele lijst. Per proces exporteren is een uitdraaihoofdstuk, geen
   apart bestand.
4. **Wat vervalt:** inlog (Azure AD), de auditlog (bestaat voor meerdere gebruikers op één database; een
   dossier op je eigen schijf heeft git of een gedateerde kopie als audit trail), de exportserver (xlsx,
   docx, pptx), de Docker-omgeving en de Ketenarchitectuur-pagina met `dagre` (de graaf komt terug als SVG
   in de blast radius). Wat ervoor in de plaats komt: opslaan als JSON en een printbare uitdraai per sectie.
5. **blast-radius gaat hierin op.** Een landschapsexport (JSON of CSV in het formaat van
   `blast-radius/blastradius/parsers.py`) is te importeren als de laag componenten onder de applicaties. De
   rekenregels (bereik, impact, dekking, ranglijst, single points of failure) komen letterlijk uit
   `blastradius/analysis.py` (hoofdstuk 4). De CLI-repo wordt gearchiveerd zodra dit live is.
6. **Twee velden erbij per applicatie:** `soort` (`applicatie` of `object met industriële automatisering`)
   en een optionele `csir_dossier` (bestandsnaam en vingerafdruk). Dat is de haak van `aanvalspaden#4`; het
   verplicht tot niets.
7. **De kroonjuwelenlijst is een uitdraai.** Stap 1 van `risicoanalyse-aanvalspaden` vraagt maximaal tien
   kroonjuwelen met eigenaar en de systemen eronder; het dossier levert die tabel op basis van `kritiek` en
   de klasse, in de kolommen van `sjabloon-matrix.md`.
8. **De pagina bevat geen eigen kopie van vragen, labels of regels.** Alles komt uit `window.__BRON__`;
   een test blokkeert als `app.js` een vraagtekst, klasselabel of prioriteitstekst bevat.
9. **Geen afstemming vooraf.** Bas besliste op 02-09 dat het plan wordt uitgevoerd zonder de mede-auteur te
   consulteren; de historie blijft, de tag `v0-applicatie` markeert zijn werk.

## 1. Wat er nu is (uit de code, 02-09-2026)

**Schaal** (`frontend/src/pages/Bia/biaShared.tsx`, `SCORE_LABELS`): 1 Catastrofaal · 2 Kritiek / zeer
ernstig · 3 Gemiddeld · 4 Gering · 5 Verwaarloosbaar. 1 is het ergst. Dezelfde vijf teksten staan in
`BiaPage.tsx` als `ANSWER_LABELS` (array, index 0 = score 1).

**Vragen** (`BiaPage.tsx`, arrays `B_QUESTIONS`, `I_QUESTIONS`, `V_QUESTIONS`; elk element heeft `key`,
`label`, optioneel `tooltip`, en `answers` met vijf objecten `{label, info}`):

| Sleutel | Dimensie | Vraag (verkort) | Levert |
|---|---|---|---|
| `b1` | B | Maximale uitvalduur voordat onaanvaardbare gevolgen optreden | RTO-klasse |
| `b2` | B | Maximale hoeveelheid dataverlies die acceptabel is | RPO-klasse |
| `b3` | B | Tijd om na herstel de achterstand in te halen | WRT-klasse |
| `b4` | B | Maximale tijd dat het proces stil kan liggen, alles bij elkaar | MTPD-klasse |
| `i1` | I | Impact als informatie onjuist, onvolledig of gemanipuleerd is | I-score |
| `v1` | V | Impact als informatie ongeautoriseerd wordt ingezien of verspreid | V-score |

`b1`, `b2`, `i1` en `v1` hebben een `tooltip` ("Elementen van de vraag: ..."); `b3` en `b4` niet. De
`info` per antwoord is bij `b1` en `b2` een alinea, bij `b3` en `b4` een tijdsduur, bij `i1` en `v1` een
alinea (bij `v1` de rubriceringsniveaus: Geheim, Confidentieel, Vertrouwelijk, Intern, Openbaar).

**Parameterlabels** (`biaShared.tsx`, `PARAM_MAP`): per score een tekst voor `rto` (uit `b1`), `rpo`
(`b2`), `wrt` (`b3`), `mtd` (`b4`). Dezelfde tabel staat in `backend/app/routers/export.py` als
`RTO_LABELS` en de klassenuitleg in `Docs/MTPD-RTO-WRT-RPO-classificatie.md` (vijf rijen: Catastrofaal,
Kritiek / zeer ernstig, Gemiddeld, Gering, Verwaarloosbaar; kolommen MTPD/MTD, RTO, WRT, RPO).

**Rekenregels** (`biaShared.tsx` `highestSeverity`; `BiaPage.tsx` regel 209-230 en 367):
- `B = min(b1, b2, b3, b4)` over de ingevulde waarden; `I = i1`; `V = v1`; niets ingevuld → geen score.
- `procesklasse = min(B, I, V)` over de aanwezige scores.
- "RTO/RPO gedefinieerd" = `b1` en `b2` beide ingevuld (`dashboard.py`, `_has_rto_rpo`). Het losse
  RTO/RPO-model (`rto_value`, `rto_unit`, `rpo_value`, `rpo_unit`, `explanation`; eenheid is vrije tekst)
  is een expliciete overschrijving die naast de klasselabels wordt getoond.

**Dashboardregels** (`backend/app/routers/dashboard.py`):
- Volledigheid per proces, tien controles in deze volgorde, elk met een label: Beschrijving,
  Doelstelling, Eigenaar, Afdeling, Laatste beoordelingsdatum, Reden kritiek (alleen als kritiek),
  Gekoppelde applicaties, BIA / BIV, RTO / RPO, Business context. `compleet` = 0 ontbrekend;
  `aandacht` = 1 tot 3; `onvolledig` = 4 of meer.
- Hoog risico: een van B, I, V is 1 of 2.
- Prioriteit, eerste regel die past: kritiek en geen BIA → `critical` ("Informatie ontbreekt"); hoog risico
  en geen RTO/RPO → `high` ("Hoog risico: geen RTO/RPO gedefinieerd"); kritiek en onvolledig → `high`
  (tekst "Kritisch proces, onvolledig gedocumenteerd"; in de code staat een gedachtestreepje, dat wordt
  een komma); 4 of meer ontbrekend → `medium`; anders `low`. Alleen processen met minstens één
  ontbrekend veld staan in de lijst.
- Verdeling per dimensie: aantal processen met score 1, 2, 3, 4, 5, en `niet beoordeeld` (geen BIA of geen
  score). Top per dimensie: de vijf laagste scores.
- Dekking (`_cov`): aantal en percentage processen met BIA, met RTO/RPO, met businesscontext, met minstens
  één applicatie; percentage = `round(done / total * 100)`, 0 als total 0.
- Privacy: aantal processen met `personal_data`, aantal met `special_personal_data`.
- Review (`get_review_status`): een datum is "op tijd" als hij niet ouder is dan een jaar vóór vandaag
  (`today.replace(year=today.year - 1)`, bij 29 februari 28 februari); per groep `on_time`, `total`, `pct`:
  processen (`last_assessment_date`), BIA (`interview_date`), businesscontext (`review_date`),
  applicaties (`review_date`).

**Gegevens** (`backend/app/models/`):
- Proces: `code` (uniek), `name`, `description`, `objective`, `owner`, `department`, `is_critical`,
  `critical_reason`, `last_assessment_date`, `notes`; m:n met applicaties.
- Applicatie: `code` (uniek), `name`, `description`, `business_owner`, `technical_owner`, `notes`,
  `review_date`.
- BIA: de zes scores, per score een `_arg`, `interviewer_name`, `interview_date`, `general_description`,
  `chain_dependencies`, `owner_deviation_motivation`, `notes`.
- RTO/RPO: `rto_value`, `rto_unit`, `rpo_value`, `rpo_unit`, `explanation`.
- Businesscontext: `key_partners`, `key_activities`, `key_resources`, `value_proposition`,
  `customer_relationships`, `channels`, `customer_segments`, `cost_structure`, `revenue_streams`,
  `legal_basis`, `stakeholders`, `chain_position`, `key_aspects`, `continuity_requirements`,
  `personal_data` (bool), `special_personal_data` (bool), `review_date`, `notes`.

**Export** (`frontend/src/pages/Export/ExportPage.tsx`, `backend/app/routers/export.py`): modules
dashboard (kpi, biv_verdeling, kritieke_processen, review, acties), processen (basis, details, biv,
rto_rpo), applicaties (basis, details, review, processen), bia (algemeen, beschikbaarheid, integriteit,
vertrouwelijkheid, eindscores), business-context (canvas, wettelijk, privacy, continuiteit),
ketenarchitectuur (processen, applicaties, koppelingen). Dit is de indeling van de uitdraai.

**blast-radius** (`blastradius/models.py`, `parsers.py`, `analysis.py`):
- Landschap = `nodes` (`id`, `label`, `type` ∈ `ci`, `app`, `proces`, `kritiek` bool) en `edges`
  (`from`, `to`, `relatie`, standaard `ondersteunt`). Richting: van drager naar gedragene (`app-brp` →
  `proc-paspoort`; een `ci` → een `app`).
- JSON: `{"naam", "toelichting", "nodes": [...], "edges": [...]}`. CSV: kolommen `from`, `from_label`,
  `from_type` (standaard `ci`), `from_kritiek`, `to`, `to_label`, `to_type` (standaard `proces`),
  `to_kritiek`, `relatie`; kritiek is waar bij `ja`, `true`, `1`, `yes` (hoofdletterongevoelig); een node
  die in meer regels voorkomt is één keer een node, en kritiek zodra één regel dat zegt.
- Testdata: `testdata/landschap.json`, 14 nodes (3 proces, 4 app, 7 ci), 19 edges.
- Rekenregels in hoofdstuk 4.

## 2. Doelstructuur

```
procescheck/
├── README.md · CONTRIBUTING.md · LICENSE (EUPL-1.2)
├── procescheck.json             DE BRON (hoofdstuk 3), gegenereerd door instrument/haal_bron.py, in git
├── werkwijze.md                 de vijf doelen uit Docs/Requirements application.md, herschreven naar het instrument
├── verantwoording.md            herkomst van de vragen (Template BIA & BIV-Classificatie.xlsx), wat eigen invulling is, wat van blast-radius komt
├── Docs/MTPD-RTO-WRT-RPO-classificatie.md   blijft; bron voor de parametertabel
├── instrument/
│   ├── LEESMIJ.md
│   ├── haal_bron.py             leest de code op tag v0-applicatie en schrijft procescheck.json; --check
│   ├── reken.py                 referentie van alle rekenregels, ook blast radius
│   ├── bouw.py                  → instrument/dist/index.html
│   ├── bron/index.html · app.css · app.js
│   ├── voorbeeld/landschap.json  kopie van blast-radius/testdata/landschap.json (met herkomst)
│   └── tests/ conftest.py · test_bron.py · test_reken.py · test_bouw.py · test_app.py · fixtures/doorloop-2026-09.json
├── site/                        gedeelde site-build (config.json met README, werkwijze, verantwoording)
└── .github/workflows/ ci.yml · pages.yml · statuut.yml
```

Weg van `main` na livegang (stap 8 van de volgorde): `backend/`, `frontend/`, `docker-compose.yml`,
`Docs/Azure-Deployment-Handleiding.md`, `Docs/Requirements application.md` (opgegaan in `werkwijze.md`).

## 3. De bron: `procescheck.json`

```json
{
 "versie": "2026-09",
 "bron": {
  "vragen": "frontend/src/pages/Bia/BiaPage.tsx op tag v0-applicatie (B_QUESTIONS, I_QUESTIONS, V_QUESTIONS, ANSWER_LABELS)",
  "labels": "frontend/src/pages/Bia/biaShared.tsx op tag v0-applicatie (SCORE_LABELS, PARAM_MAP)",
  "parametertabel": "Docs/MTPD-RTO-WRT-RPO-classificatie.md",
  "regels": "backend/app/routers/dashboard.py op tag v0-applicatie",
  "sjabloon": "Template BIA & BIV-Classificatie.xlsx, genoemd in de code als herkomst van de vragen",
  "blast_radius": "security-commons-nl/blast-radius, blastradius/analysis.py en parsers.py, commit <hash>",
  "gegenereerd_door": "instrument/haal_bron.py; wijzig de bron niet met de hand"
 },
 "schaal": [
  {"score": 1, "label": "Catastrofaal"}, {"score": 2, "label": "Kritiek / zeer ernstig"},
  {"score": 3, "label": "Gemiddeld"}, {"score": 4, "label": "Gering"}, {"score": 5, "label": "Verwaarloosbaar"}
 ],
 "vragen": [
  {"id": "b1", "dimensie": "B", "parameter": "rto", "vraag": "<label>", "toelichting": "<tooltip of leeg>",
   "antwoorden": [{"score": 1, "label": "Catastrofaal", "info": "<info>"}, "... tot en met 5"]},
  {"id": "b2", "dimensie": "B", "parameter": "rpo", "...": "..."},
  {"id": "b3", "dimensie": "B", "parameter": "wrt", "...": "..."},
  {"id": "b4", "dimensie": "B", "parameter": "mtpd", "...": "..."},
  {"id": "i1", "dimensie": "I", "parameter": null, "...": "..."},
  {"id": "v1", "dimensie": "V", "parameter": null, "...": "..."}
 ],
 "parameters": {
  "rto":  {"1": "Enkele uren", "2": "Maximaal 8 uur", "3": "Maximaal 2 werkdagen", "4": "Maximaal 1 week", "5": "Meer dan een week"},
  "rpo":  {"1": "Enkele uren", "2": "4 tot 8 uur", "3": "8 tot 24 uur", "4": "Maximaal 24 uur", "5": "Een week of meer"},
  "wrt":  {"1": "Enkele uren", "2": "4 tot 8 uur", "3": "2 werkdagen", "4": "1 week", "5": "Meer dan een week"},
  "mtpd": {"1": "Enkele uren", "2": "4 tot 8 uur", "3": "2 werkdagen", "4": "1 week", "5": "Meer dan een week"}
 },
 "parametertabel": [
  {"klasse": "Catastrofaal", "mtpd": "enkele uren niet acceptabel", "rto": "binnen enkele uren", "wrt": "meerdere werkdagen", "rpo": "enkele uren"},
  "... de vijf rijen uit Docs/MTPD-RTO-WRT-RPO-classificatie.md, letterlijk"
 ],
 "volledigheid": [
  {"id": "beschrijving", "label": "Beschrijving"}, {"id": "doelstelling", "label": "Doelstelling"},
  {"id": "eigenaar", "label": "Eigenaar"}, {"id": "afdeling", "label": "Afdeling"},
  {"id": "laatste_beoordeling", "label": "Laatste beoordelingsdatum"},
  {"id": "reden_kritiek", "label": "Reden kritiek", "alleen_als_kritiek": true},
  {"id": "applicaties", "label": "Gekoppelde applicaties"}, {"id": "bia", "label": "BIA / BIV"},
  {"id": "rto_rpo", "label": "RTO / RPO"}, {"id": "context", "label": "Business context"}
 ],
 "prioriteiten": [
  {"id": "critical", "regel": "kritiek_zonder_bia", "reden": "Informatie ontbreekt"},
  {"id": "high", "regel": "hoog_risico_zonder_rto_rpo", "reden": "Hoog risico: geen RTO/RPO gedefinieerd"},
  {"id": "high", "regel": "kritiek_onvolledig", "reden": "Kritisch proces, onvolledig gedocumenteerd"},
  {"id": "medium", "regel": "vier_of_meer_ontbrekend", "reden": "Onvolledig gedocumenteerd"},
  {"id": "low", "regel": "anders", "reden": "Onvolledig gedocumenteerd"}
 ],
 "keuzes": {
  "soort_applicatie": ["applicatie", "object met industriële automatisering"],
  "nodetypes": ["ci", "app", "proces"],
  "relatie_standaard": "ondersteunt",
  "kritiek_waar": ["ja", "true", "1", "yes"]
 },
 "review_termijn_dagen": 365
}
```

**`haal_bron.py`:**
- Haalt de drie bestanden op met `git show v0-applicatie:<pad>` (werkt lokaal en in CI; CI checkt uit met
  `fetch-depth: 0` zodat de tag er is). Ontbreekt de tag, dan stopt het script met een foutmelding.
- Leest `ANSWER_LABELS` (array van vijf strings, enkelvoudig aangehaald) en `SCORE_LABELS` (object
  `{1: '...', ...}`); beide moeten dezelfde vijf teksten geven, anders stoppen.
- Leest per array `B_QUESTIONS`, `I_QUESTIONS`, `V_QUESTIONS` de objecten. Aanpak: pak de tekst tussen
  `const B_QUESTIONS: BiaQuestion[] = [` en de eerstvolgende regel die alleen `]` is; splits op `key:`;
  per stuk: `key: '(\w+)'`, `label: '((?:[^'\\]|\\.)*)'`, optioneel `tooltip: '((?:[^'\\]|\\.)*)'`, en
  vijf keer `info: '((?:[^'\\]|\\.)*)'` in volgorde (score 1 tot en met 5). Ontsnappingen: `\'` wordt `'`,
  `\n` wordt een regeleinde. Precies 6 vragen en 30 antwoorden, anders stoppen.
- `parameters` uit `PARAM_MAP` in `biaShared.tsx` (sleutels `rto`, `rpo`, `wrt`, `mtd`; `mtd` wordt hier
  `mtpd`, de term uit de documentatie).
- `parametertabel` uit de markdowntabel in `Docs/MTPD-RTO-WRT-RPO-classificatie.md` (eerste tabel, vijf
  rijen, kolommen in de volgorde Klasse, MTPD / MTD, RTO, WRT, RPO).
- `volledigheid`, `prioriteiten`, `review_termijn_dagen` en `keuzes` zijn constanten in het script, met
  de regel uit `dashboard.py` als commentaar erbij; `test_bron.py` legt de labels tegen `dashboard.py`.
- `bron.blast_radius` krijgt de commit-hash van `blast-radius` op het moment van overname
  (`git -C ../blast-radius log -1 --format=%H`), of "onbekend".
- `--check`: genereert in het geheugen en vergelijkt met het bestand; exit 1 met de eerste drie verschillen.

## 4. Rekenregels (`instrument/reken.py`, gespiegeld in `app.js` als `reken.<naam>`)

```
klasse_score(scores)                 scores: lijst met getallen 1..5 of None; None telt niet mee
                                     leeg → None; anders min(scores)   (1 is het ergst)

bia(antwoorden)                      antwoorden: dict b1..b4, i1, v1 → 1..5 of None
  B = klasse_score([b1, b2, b3, b4]); I = klasse_score([i1]); V = klasse_score([v1])
  proces = klasse_score([B, I, V])
  retour {"B", "I", "V", "proces"}

parameterlabel(bron, parameter, score)   bron.parameters[parameter][str(score)]; None als score None

heeft_rto_rpo(proces)                proces.bia.b1 en proces.bia.b2 zijn allebei ingevuld

ontbrekend(proces)                   lijst labels, in de volgorde van bron.volledigheid:
  beschrijving leeg · doelstelling leeg · eigenaar leeg · afdeling leeg · laatste_beoordeling leeg ·
  (alleen als proces.kritiek) reden_kritiek leeg · geen applicaties · geen enkele bia-score ingevuld ·
  niet heeft_rto_rpo · context leeg (alle contextvelden leeg en beide booleans onwaar)

hoog_risico(proces)                  een van B, I, V is 1 of 2

prioriteit(proces)                   None als ontbrekend(proces) leeg is; anders de eerste die past:
  kritiek en geen bia-score          → "critical", reden uit bron
  hoog_risico en niet heeft_rto_rpo  → "high"
  kritiek                            → "high" (kritiek_onvolledig)
  len(ontbrekend) >= 4               → "medium"
  anders                             → "low"

op_tijd(datum, vandaag, termijn_dagen)   datum ingevuld en datum >= vandaag min een jaar
  (jaar - 1, zelfde maand en dag; 29 februari wordt 28 februari); termijn_dagen staat in de bron voor de
  uitleg, de regel zelf is "een jaar terug", zoals de code

dashboard(bron, dossier, vandaag)
  totaal, kritiek, compleet (0 ontbrekend), aandacht (1..3), onvolledig (>= 4), hoog_risico (aantal)
  verdeling[B|I|V] = {"1":n, "2":n, "3":n, "4":n, "5":n, "leeg": n}   leeg = geen score
  top[B|I|V] = de processen met de laagste score, hoogstens vijf, gesorteerd op (score, code)
  dekking[bia|rto_rpo|context|applicaties] = {"done", "total", "pct"}   pct = round(done/total*100), 0 bij total 0
  privacy = {"persoonsgegevens": n, "bijzonder": n}
  review[processen|bia|context|applicaties] = {"on_time", "total", "pct"}
  prioriteiten = [{code, naam, prioriteit, reden, ontbrekend[]}] gesorteerd: critical, high, medium, low, dan code
  kritiek_lijst = per kritiek proces: code, naam, B, I, V, heeft_bia, heeft_rto_rpo, ontbrekend

landschap(dossier)                   bouwt nodes en edges uit het dossier:
  per proces een node {id: "proces:"+code, label: naam, type: "proces", kritiek}
  per applicatie een node {id: "app:"+code, label: naam, type: "app", kritiek: False}
  per component een node {id: "ci:"+id, label, type: "ci", kritiek}
  edges: per proces per gekoppelde applicatie {from: "app:"+A, to: "proces:"+P, relatie: "ondersteunt"}
         per component_edge {from: "ci:"+from, to: ("app:" of "ci:") + to, relatie}

bereik(landschap, start)             DFS langs uitgaande edges (from → to), start zelf niet in de set;
                                     tweede uitkomst: cyclus = start wordt opnieuw bereikt
impact(landschap, node)              geraakt = bereik; processen = geraakt met type proces;
                                     kritieke = daarvan met kritiek
dekking(landschap, proces)           aantal inkomende edges vanuit een node van type app
ranglijst(landschap)                 alle nodes behalve proces, gesorteerd op
                                     (-len(kritieke), -len(processen), -len(geraakt), id)
single_points(landschap)             kritieke processen met dekking <= 1, gesorteerd op id
cyclus_waarschuwingen(landschap)     per node waarvan bereik een cyclus meldt: de tekst uit analysis.py
```

Alle functies puur; `app.js` heeft dezelfde namen in het object `reken`; een test controleert dat elke naam
uit `reken.py` (behalve helpers met een voorloopstreepje) in `app.js` als `reken.<naam> =` voorkomt.

## 5. Dossierformaat

`localStorage`-sleutel `procescheck-dossier`; bestandsnaam `procescheck-dossier-<slug organisatie>-<JJJJ-MM-DD>.json`.

```json
{
 "formaat": "procescheck-dossier", "versie": 1, "bron_versie": "2026-09", "bron_sha256": "<vingerafdruk>", "bijgewerkt": "",
 "organisatie": {"naam": "", "peildatum": ""},
 "processen": [
  {"code": "P01", "naam": "", "beschrijving": "", "doelstelling": "", "eigenaar": "", "afdeling": "",
   "kritiek": false, "reden_kritiek": "", "laatste_beoordeling": "", "notities": "",
   "applicaties": ["A01"],
   "bia": {"b1": null, "b2": null, "b3": null, "b4": null, "i1": null, "v1": null,
           "onderbouwing": {"b1": "", "b2": "", "b3": "", "b4": "", "i1": "", "v1": ""},
           "interviewer": "", "interviewdatum": "", "beschrijving": "", "ketenafhankelijkheden": "",
           "afwijking_eigenaar": "", "notities": ""},
   "rto_rpo": {"rto": "", "rto_eenheid": "", "rpo": "", "rpo_eenheid": "", "toelichting": ""},
   "context": {"partners": "", "activiteiten": "", "middelen": "", "propositie": "", "klantrelaties": "",
               "kanalen": "", "segmenten": "", "kosten": "", "opbrengsten": "", "wettelijke_basis": "",
               "stakeholders": "", "ketenpositie": "", "kernaspecten": "", "continuiteitseisen": "",
               "persoonsgegevens": false, "bijzondere_persoonsgegevens": false, "reviewdatum": "", "notities": ""}}
 ],
 "applicaties": [
  {"code": "A01", "naam": "", "beschrijving": "", "eigenaar_business": "", "eigenaar_technisch": "",
   "soort": "applicatie", "csir_dossier": {"bestand": "", "vingerafdruk": ""}, "notities": "", "reviewdatum": ""}
 ],
 "componenten": [{"id": "ci-db1", "label": "", "kritiek": false}],
 "component_edges": [{"from": "ci-db1", "to": "A01", "relatie": "ondersteunt"}],
 "landschap_bron": {"bestand": "", "geimporteerd": ""}
}
```

- Codes van processen en applicaties zijn uniek binnen het dossier; de pagina weigert een dubbele code met
  een melding. `component_edges[].to` is een applicatiecode of een component-id; een edge naar een
  onbekende code wordt bij import gemeld en overgeslagen.
- B, I, V, procesklasse, ontbrekend, prioriteit en de blast radius staan **niet** in het dossier; ze worden
  bij laden en bij elke wijziging herrekend.
- `bron_sha256` = sha256 over `json.dumps(kern, ensure_ascii=False, sort_keys=True, separators=(",", ":"))`
  met `kern` = `schaal`, `vragen`, `parameters`, `volledigheid`, `prioriteiten`. Verschil bij laden → melding
  in `#dossier-status`, laden gaat door.
- Laden weigert een bestand zonder `formaat == "procescheck-dossier"` of `versie != 1`.
- Datums als `JJJJ-MM-DD`. Opslaan, laden, wissen: als bij de CSIR-tool.

## 6. De pagina

Kop, dossierbalk en tabs als bij de CSIR-tool. Kruimelpad `Security Commons NL › procescheck`. Tabs:

| Tab-id | Sectie-id | Inhoud |
|---|---|---|
| `#tab-processen` | `#scherm-processen` | lijst + formulier |
| `#tab-applicaties` | `#scherm-applicaties` | lijst + formulier + koppeling aan processen |
| `#tab-bia` | `#scherm-bia` | per gekozen proces de zes vragen, uitkomst, RTO/RPO |
| `#tab-context` | `#scherm-context` | per gekozen proces de businesscontext |
| `#tab-blast` | `#scherm-blast` | import van componenten, ranglijst, single points, graaf |
| `#tab-dashboard` | `#scherm-dashboard` | de tellers |
| `#tab-uitdraai` | `#scherm-uitdraai` | het dossier op een rij |

Dossierbalk: `#knop-opslaan`, `#knop-laden` (+ verborgen `#bestand-laden`), `#knop-afdrukken`,
`#knop-wissen`, statusregel `#dossier-status` (organisatie, aantal processen, aantal kritiek, bijgewerkt;
meldingen met class `let-op`). Kopvelden `#org-naam`, `#org-peildatum` bovenaan het processen-scherm.

**Processen.** Tabel `#tabel-processen` met per rij `tr[data-proces="P01"]`: code, naam, eigenaar, afdeling,
kritiek (Ja/Nee), B, I, V, klasse (label uit de schaal of "—"), ontbrekend (aantal), prioriteit
(`td.prioriteit`, tekst `critical|high|medium|low` of leeg), knoppen `.bewerk` en `.verwijder`. Formulier
`#proces-form` met `#p-code`, `#p-naam`, `#p-beschrijving`, `#p-doelstelling`, `#p-eigenaar`,
`#p-afdeling`, `#p-kritiek` (checkbox), `#p-reden-kritiek`, `#p-laatste-beoordeling` (date),
`#p-notities`, `#p-applicaties` (multi-select van applicatiecodes), knoppen `#p-opslaan`, `#p-annuleren`.
Nieuw proces: `#knop-proces-nieuw`. Verwijderen vraagt bevestiging (`confirm`).

**Applicaties.** Tabel `#tabel-applicaties`, rij `tr[data-app="A01"]`: code, naam, soort, eigenaren,
aantal processen, reviewdatum. Formulier `#app-form`: `#a-code`, `#a-naam`, `#a-beschrijving`,
`#a-eigenaar-business`, `#a-eigenaar-technisch`, `#a-soort` (select uit `keuzes.soort_applicatie`),
`#a-csir-bestand`, `#a-csir-vingerafdruk`, `#a-reviewdatum`, `#a-notities`; `#a-opslaan`, `#a-annuleren`,
`#knop-app-nieuw`. Verwijderen van een applicatie haalt haar ook uit `processen[].applicaties` en uit
`component_edges` (met bevestiging die dat zegt).

**BIA en BIV.** `#bia-proces` (select met alle processen). Per vraag uit de bron een blok
`[data-vraag="b1"]` met de vraag, de toelichting (als `<details>`), een `<select>` `[data-score="b1"]` met
opties leeg en 1 tot en met 5, elke optie `score · label`, en onder de select de `info` van het gekozen
antwoord in `[data-info="b1"]`; `<textarea data-onderbouwing="b1">`. Uitkomst: `#bia-b`, `#bia-i`, `#bia-v`,
`#bia-klasse` (score en label, of "nog niet bepaald"), `#bia-rto`, `#bia-rpo`, `#bia-wrt`, `#bia-mtpd`
(parameterlabel), de parametertabel uit de bron als hulptekst. Overschrijving: `#rto-waarde`,
`#rto-eenheid`, `#rpo-waarde`, `#rpo-eenheid`, `#rto-rpo-toelichting`. Interview: `#bia-interviewer`,
`#bia-interviewdatum`, `#bia-beschrijving`, `#bia-keten`, `#bia-afwijking-eigenaar`, `#bia-notities`.

**Context.** `#context-proces` (select). Canvas als negen textarea's `[data-context="partners"]` enz. (de
sleutels uit het dossier), dan `wettelijke_basis`, `stakeholders`, `ketenpositie`, `kernaspecten`,
`continuiteitseisen`, checkboxes `#context-persoonsgegevens`, `#context-bijzonder`, `#context-reviewdatum`,
`#context-notities`.

**Dashboard.** Elk getal in een element met `data-teller`:

| `data-teller` | Betekenis |
|---|---|
| `totaal`, `kritiek`, `compleet`, `aandacht`, `onvolledig`, `hoog_risico` | de zes hoofdtellers |
| `verdeling.B.1` … `verdeling.B.5`, `verdeling.B.leeg`; idem `I`, `V` | verdeling per dimensie |
| `dekking.bia.done`, `.total`, `.pct`; idem `rto_rpo`, `context`, `applicaties` | dekking |
| `privacy.persoonsgegevens`, `privacy.bijzonder` | privacy |
| `review.processen.on_time`, `.total`, `.pct`; idem `bia`, `context`, `applicaties` | review |

Daaronder de prioriteitenlijst `#prioriteiten` met per rij `tr[data-prioriteit="P01"]`: code, naam,
`td.niveau` (critical…low), reden, ontbrekende velden; en de kritieke-processenlijst `#kritiek-lijst`
met per rij `tr[data-kritiek="P01"]`. Percentages als geheel getal met `%`; afronden met `floor(x + 0.5)`
(de val uit het CSIR-plan, hoofdstuk 14 daar).

**Blast radius.** Zie hoofdstuk 7.

**Uitdraai.** Hoofdstukken in deze volgorde, elk `<h2>`: 1 Organisatie en peildatum · 2 Dashboard (de
tellers als tabellen, de prioriteitenlijst) · 3 Kroonjuwelen (alle processen met `kritiek`, gesorteerd op
procesklasse dan code, kolommen `#`, Kroonjuweel, Eigenaar, Systemen eronder = de applicaties, met een
regel eronder "maximaal tien, zie stap 1 van Risicoanalyse langs aanvalspaden" als er meer dan tien zijn) ·
4 Processen (basis, BIV-scores, RTO/RPO) · 5 BIA per proces (de zes antwoorden met label en onderbouwing,
interviewgegevens) · 6 Businesscontext per proces · 7 Applicaties (basis, soort, CSIR-verwijzing,
gekoppelde processen) · 8 Blast radius (ranglijst, single points, cycluswaarschuwingen) · 9 Verantwoording
(bronversie, vingerafdruk, bijgewerkt). `@media print` als bij de CSIR-tool.

## 7. Blast radius in het instrument

**Import.** `#knop-landschap-laden` opent `#bestand-landschap` (accept `.json,.csv`). JSON in het formaat
van `parsers.py` `from_json`; CSV volgens `from_csv` (kolommen in hoofdstuk 1). Na het lezen:
- nodes van type `proces` en `app` worden **gematcht op id of label** met bestaande processen en
  applicaties (id gelijk aan code, of label gelijk aan naam, hoofdletterongevoelig); ongematchte proces- en
  app-nodes worden **aangemaakt** als proces (kritiek uit de node) respectievelijk applicatie, met de node-id
  als code;
- nodes van type `ci` gaan naar `componenten`;
- edges app → proces worden een koppeling in `processen[].applicaties`; edges ci → app en ci → ci gaan
  naar `component_edges`; edges met een onbekend type of onbekende node worden geteld en gemeld;
- `landschap_bron` krijgt bestandsnaam en datum.
Een tweede import voegt toe en overschrijft niets; verwijderen doe je per component (`.verwijder`) of met
`#knop-componenten-wissen` (bevestiging).

**Scherm.** Tabel `#tabel-componenten` (`tr[data-component="ci-db1"]`: id, label, kritiek als checkbox,
edges als tekst, verwijderknop). Ranglijst `#tabel-blast` over alle apps en componenten, per rij
`tr[data-blast="app:A01"]` of `tr[data-blast="ci:ci-db1"]`: label, type, `td.kritieke` (aantal),
`td.processen` (aantal), `td.geraakt` (aantal), en de lijst kritieke processen als tekst. Lijst
`#blast-spof` (`li[data-spof="proces:P01"]`) met de kritieke processen die op één applicatie steunen.
`#blast-cyclus` met de waarschuwingen (leeg = verborgen). Voorbeeld laden: `#knop-landschap-voorbeeld`
laadt `instrument/voorbeeld/landschap.json` uit `window.__BRON__.voorbeeld` (staat in de bron, geen fetch).

**Graaf.** Eén `<svg id="blast-graaf">`, drie kolommen: ci links, app midden, proces rechts (de volgorde
van `nodetypes`). Per kolom de nodes gelijkmatig verticaal verdeeld, gesorteerd op id; rechthoek met label,
kritieke processen met class `kritiek`; edges als lijnen van rechterrand bron naar linkerrand doel. Klik op
een node (`[data-node="ci:ci-db1"]`) markeert de node en alles in zijn bereik met class `geraakt`. Geen
dragging, geen zoom, geen bibliotheek. Bij meer dan 60 nodes een melding boven de graaf dat de tabel
leidend is; de graaf tekent dan alleen kritieke processen en wat ze draagt.

## 8. Bouwen

`instrument/bouw.py` als `csir-assessment-tool/register/bouw.py`: leest `procescheck.json` en
`instrument/voorbeeld/landschap.json`, zet ze in `window.__BRON__` (`voorbeeld` als extra sleutel),
berekent `vingerafdruk` (hoofdstuk 5), dezelfde CSP, dezelfde placeholders, schrijft `dist/index.html`.
Verwachte grootte: 150 tot 250 kB.

## 9. Workflows

`ci.yml` als bij de CSIR-tool, twee jobs (bron + reken; bouw + app), met twee verschillen: `checkout` met
`fetch-depth: 0` (de tag `v0-applicatie` moet er zijn voor `haal_bron.py --check` en `test_bron.py`), en
geen kennisbank-checkout (er is geen handreiking). `pages.yml`: node-build van de uitleg naar
`dist/uitleg/`, dan `python instrument/bouw.py dist`, `cp dist/index.html dist/procescheck.html`,
`cp procescheck.json dist/`. `statuut.yml` blijft.

## 10. Tests

`conftest.py`: bouwt één keer naar `tmp_path`, laadt `procescheck.json` en de fixture. Browsertests slaan
over zonder Playwright.

**`test_bron.py`** (leest de code op de tag zelf met `git show`; slaat over als de tag ontbreekt, met een
duidelijke reden):

| Test | Bewijst |
|---|---|
| `test_aantallen` | 5 schaalstappen, 6 vragen (4 B, 1 I, 1 V), 30 antwoorden, 4 parameters × 5, 5 rijen parametertabel, 10 volledigheidsvelden, 5 prioriteiten |
| `test_vragen_woordelijk` | per vraag: `vraag` == `label` in de code, `toelichting` == `tooltip` (of leeg), elke `info` == de code; ontsnappingen opgelost |
| `test_schaal_woordelijk` | de vijf labels == `ANSWER_LABELS` == `SCORE_LABELS` |
| `test_parameters_woordelijk` | `parameters` == `PARAM_MAP` (met `mtd` → `mtpd`) en == `RTO_LABELS` in `export.py` voor `rto` |
| `test_parametertabel_woordelijk` | de vijf rijen == de markdowntabel |
| `test_volledigheid_labels` | de tien labels komen letterlijk voor in `dashboard.py` (`missing.append("...")`) |
| `test_prioriteit_redenen` | "Informatie ontbreekt" en "Hoog risico: geen RTO/RPO gedefinieerd" komen letterlijk voor in `dashboard.py` |
| `test_voorbeeld_landschap` | `instrument/voorbeeld/landschap.json` heeft 14 nodes (3/4/7) en 19 edges, gelijk aan `blast-radius/testdata/landschap.json` op de genoemde commit als die repo ernaast staat (anders alleen de aantallen) |
| `test_haal_bron_check_slaagt` | `haal_bron.py --check` exit 0 |

**`test_reken.py`:**

| Test | Bewijst |
|---|---|
| `test_klasse_score` | `[3, None, 1]` → 1; `[None]` → None; `[]` → None; `[5, 4]` → 4 |
| `test_bia` | b1..b4 = 3, 2, 5, 4; i1 = 4; v1 = 1 → B 2, I 4, V 1, proces 1; alles None → alles None; alleen i1 = 3 → B None, proces 3 |
| `test_parameterlabel` | rto 2 → "Maximaal 8 uur"; mtpd 5 → "Meer dan een week"; None → None |
| `test_heeft_rto_rpo` | b1 en b2 ingevuld → waar; alleen b1 → onwaar |
| `test_ontbrekend_volgorde_en_kritiek` | leeg proces, niet kritiek → 9 labels in bronvolgorde (zonder Reden kritiek); kritiek zonder reden → 10; volledig proces → 0 |
| `test_ontbrekend_context` | context met alleen `persoonsgegevens: true` telt als ingevuld |
| `test_hoog_risico` | V 2 → waar; B 3, I 3, V 3 → onwaar; geen scores → onwaar |
| `test_prioriteit_volgorde` | kritiek zonder bia → critical (ook als ook hoog risico); niet kritiek, hoog risico, geen rto_rpo → high; kritiek, wel bia, 1 ontbrekend → high; niet kritiek, 4 ontbrekend, geen hoog risico → medium; 1 ontbrekend → low; 0 ontbrekend → None |
| `test_op_tijd` | vandaag 2026-09-02: 2025-09-02 op tijd, 2025-09-01 niet, leeg niet; vandaag 2028-02-29: cutoff 2027-02-28 |
| `test_dashboard_percentages` | done 1 total 8 → 13 (half omhoog); total 0 → 0 |
| `test_dashboard_gelijk_aan_doorloop` | alle platte tellers van de fixture gelijk aan `dashboard()` |
| `test_landschap_uit_dossier` | fixture: aantal nodes = processen + applicaties + componenten; edges = som koppelingen + component_edges; ids met voorvoegsel |
| `test_bereik_en_cyclus` | ketting ci → app → proces: bereik(ci) = {app, proces}; met een edge proces → ci erbij: cyclus waar |
| `test_impact_ranglijst_spof` | op het voorbeeldlandschap: ranglijst gelijk aan de uitkomst van `blastradius.analysis.ranglijst` (als de repo ernaast staat; anders een vaste verwachting in de test: eerste rij en aantallen), `single_points` idem |
| `test_dekking` | proces met twee apps → 2; zonder app → 0 |
| `test_reken_en_app_hebben_dezelfde_functies` | elke publieke functie uit `reken.py` staat als `reken.<naam> =` in `app.js` |

**`test_bouw.py`:** als bij de CSIR-tool (alle vraagteksten, labels, `info`'s en de parametertabel in de
pagina; geen externe verwijzing; CSP-hashes; één script en één stylesheet; geen inline `style`;
`app.js` bevat geen vraagtekst (eerste 30 tekens), geen klasselabel en geen prioriteitsreden; noscript;
herhaalbaar; kruimelpad; voetregel; vingerafdruk; kleiner dan 800 kB; `voorbeeld` zit in `__BRON__`).

**`test_app.py`** (Chromium, schone `localStorage` per test, geen consolefouten):

| Test | Bewijst |
|---|---|
| `test_startscherm` | processen-tab zichtbaar, 7 tabs, `#dossier-status` bevat "0 processen" |
| `test_proces_aanmaken_wijzigen_verwijderen` | nieuw P01 → rij verschijnt; bewerken naam → rij bijgewerkt; dubbele code → melding, geen tweede rij; verwijderen (dialoog) → rij weg |
| `test_applicatie_koppelen` | A01 aanmaken, aan P01 koppelen via `#p-applicaties` → rij P01 toont 1 applicatie; applicatie verwijderen → koppeling weg |
| `test_bia_rekent` | P01 kiezen in `#bia-proces`; b1..b4 = 3, 2, 5, 4; i1 = 4; v1 = 1 → `#bia-b` "2", `#bia-i` "4", `#bia-v` "1", `#bia-klasse` bevat "Catastrofaal", `#bia-rto` "Maximaal 2 werkdagen", `#bia-rpo` "4 tot 8 uur", `#bia-wrt` "Meer dan een week", `#bia-mtpd` "1 week"; `[data-info="v1"]` bevat "Geheim" |
| `test_bia_incompleet` | alleen i1 → `#bia-b` "—", `#bia-klasse` gelijk aan I |
| `test_dashboard_gelijk_aan_referentie` | fixture laden → alle `[data-teller]` gelijk aan `reken.dashboard()` (percentages als tekst); prioriteitenlijst gelijk in volgorde en niveau |
| `test_prioriteit_op_scherm` | kritiek proces zonder BIA → `td.prioriteit` "critical" en rij in `#prioriteiten` met reden "Informatie ontbreekt" |
| `test_landschap_import_json` | `#bestand-landschap` met het voorbeeld → 7 componenten, 3 processen en 4 applicaties aangemaakt, `#tabel-blast` heeft 11 rijen, `#blast-spof` niet leeg; ranglijst eerste rij gelijk aan `reken.ranglijst` |
| `test_landschap_import_csv` | dezelfde inhoud als CSV (fixture `landschap.csv`) → dezelfde tellers |
| `test_landschap_match_op_bestaand` | eerst P01 "Paspoort- en rijbewijsuitgifte" aanmaken, dan importeren → geen dubbel proces, koppelingen op P01 |
| `test_blast_graaf` | `#blast-graaf` bevat evenveel `[data-node]` als nodes; klik op een ci markeert zijn bereik met class `geraakt` |
| `test_opslaan_laden_wissen_herladen` | als bij de CSIR-tool, met een proces, een applicatie en een component |
| `test_laden_weigert_verkeerd_bestand`, `test_laden_meldt_andere_bronversie` | als bij de CSIR-tool |
| `test_uitdraai_kroonjuwelen` | drie processen waarvan twee kritiek met klasse 2 en 1 → hoofdstuk Kroonjuwelen toont precies die twee, klasse 1 eerst, met hun applicaties |
| `test_uitdraai_bevat_alles` | organisatienaam, elk proces, elke applicatie, de prioriteitenlijst, de ranglijst en de vingerafdruk staan in `#uitdraai-inhoud` |
| `test_afdrukken_toont_uitdraai` | print-media: alleen `#scherm-uitdraai` zichtbaar |

## 11. De fixture: `instrument/tests/fixtures/doorloop-2026-09.json`

Een dossier plus `verwacht` (platte tellers uit `reken.py`) plus `landschap.csv` ernaast:

- organisatie "Gemeente Voorbeeld", peildatum 2026-09-02;
- vier processen, zo gekozen dat elke prioriteitsregel en elke reviewuitkomst één keer voorkomt:
  - **P01** kritiek, alle velden gevuld, applicaties A01, A02, A03; BIA b1..b4 = 3, 2, 5, 4, i1 = 4, v1 = 1
    (B 2, I 4, V 1, klasse 1, hoog risico); interviewdatum 2026-06-01; context gevuld met
    `persoonsgegevens` en `bijzondere_persoonsgegevens` waar, reviewdatum 2026-06-01; laatste beoordeling
    2026-06-01. Verwacht: 0 ontbrekend, geen prioriteit, alle reviews op tijd.
  - **P02** kritiek, geen reden kritiek, applicatie A04, geen BIA, geen context, verder gevuld (laatste
    beoordeling 2026-02-01). Verwacht: ontbrekend = reden kritiek, BIA, RTO/RPO, context (4) → prioriteit
    `critical` ("Informatie ontbreekt"); dekking 1 en kritiek, dus de single point of failure.
  - **P03** niet kritiek, beschrijving en eigenaar gevuld, geen applicaties, geen context; BIA b1 = 4,
    b2 = 4, i1 = 2, verder leeg (B 4, I 2, V None, klasse 2, hoog risico; `heeft_rto_rpo` waar). Verwacht:
    ontbrekend = doelstelling, afdeling, laatste beoordelingsdatum, applicaties, context (5) → prioriteit
    `medium`.
  - **P04** niet kritiek, alleen naam en laatste beoordeling 2024-01-01 (niet op tijd), applicatie A05.
    Verwacht: ontbrekend = beschrijving, doelstelling, eigenaar, afdeling, BIA, RTO/RPO, context (7) →
    `medium`; geen hoog risico.
  - **P05**, niet kritiek, alles gevuld behalve notities, BIA 3/3/3/3 · 3 · 3, applicatie A05, alle
    datums 2026-01-15, context zonder persoonsgegevens: 0 ontbrekend, geen prioriteit. **P06**, niet
    kritiek, alles gevuld behalve de doelstelling, BIA 5/5/5/5 · 5 · 5, applicatie A05, datums
    2026-05-01, context zonder persoonsgegevens: 1 ontbrekend → `low`.
- vijf applicaties: A01 en A02 gewone applicaties; A03 `soort` object met industriële automatisering met
  `csir_dossier` gevuld; A04 en A05 gewoon; reviewdatums: A01 en A02 2026-03-01 (op tijd), A03 2025-01-01
  (niet), A04 en A05 leeg (niet);
- zes componenten met edges: ci-db1 → A01, ci-db1 → A02, ci-net1 → ci-db1, ci-srv1 → A03, ci-srv2 → A03,
  ci-los zonder edges. Verwacht: bereik(ci-net1) = {ci-db1, A01, A02, P01}; ranglijst eerste rij ci-net1
  (1 kritiek proces, 1 proces, 4 geraakt) gelijk met ci-db1 op kritiek en processen maar minder geraakt (3),
  dus ci-net1 vóór ci-db1; `single_points` = [proces:P02]; geen cyclus.
- `verwacht`: alle platte tellers uit `reken.dashboard()` en `reken.ranglijst()`, gegenereerd door een
  script `instrument/tests/fixtures/maak_doorloop.py` dat in de repo blijft, en met de hand nagelopen op:
  totaal 6, kritiek 2, compleet 2 (P01, P05), aandacht 1 (P06), onvolledig 3 (P02, P03, P04), hoog_risico 2
  (P01 op V, P03 op I), verdeling.V.1 = 1, review.processen.on_time = 4 van 6 (P01, P02, P05, P06; P03 leeg,
  P04 te oud), review.applicaties.on_time = 2 van 5, privacy.persoonsgegevens = 1, privacy.bijzonder = 1.

## 12. Statuut, README, profiel, balie

- README volgens B11; "Snel starten" begint met de pagina en noemt de landschapsimport; het vervallen van
  Docker en Azure AD staat er expliciet in. Status blijft **prototype** (B8) tot iemand het gebruikt.
- `werkwijze.md`: de vijf doelen uit de requirements, per doel waar het in het instrument zit;
  `verantwoording.md`: herkomst van de zes vragen (het Excel-sjabloon dat de code noemt), wat eigen
  invulling is (prioriteiten, kroonjuwelen, soort), en dat de blast radius uit `blast-radius` komt met
  commit-hash.
- Profiel: rij `procescheck` krijgt *Live tool* en de omschrijving "BIA en BIV per proces, RTO/RPO,
  businesscontext en blast radius in de browser; één dossier per organisatie als JSON"; `blast-radius`
  gaat naar de alinea Gearchiveerd met de reden. `ARCHITECTUUR.md`: groep Instrumenten en de zin over
  blast-radius. Werkmap-`CLAUDE.md`: sectie procescheck en de routingregel "blast radius, transitieve
  impact, single point of failure, CI-landschap → procescheck".
- `blast-radius`: `gh repo archive` na livegang, README-regel bovenaan waar het heen is.

## 13. Bouwvolgorde (elke stap heeft een "klaar als")

1. Tag `v0-applicatie` op de huidige `main` en pushen. Klaar als `git show v0-applicatie:frontend/src/pages/Bia/BiaPage.tsx` werkt.
2. `haal_bron.py`, `procescheck.json`, `instrument/voorbeeld/landschap.json`. Klaar als `test_bron.py` groen is.
3. `reken.py`. Klaar als `test_reken.py` groen is met een voorlopige fixture.
4. Sjabloon, `bouw.py`, lege app met alleen de tabs. Klaar als `test_bouw.py` groen is.
5. Processen en applicaties (opslag, formulieren, koppeling). Klaar als de drie eerste browsertests groen zijn.
6. BIA en context. Klaar als `test_bia_rekent` en `test_bia_incompleet` groen zijn.
7. Dashboard en prioriteiten. Klaar als `test_dashboard_gelijk_aan_referentie` en `test_prioriteit_op_scherm` groen zijn.
8. Blast radius: import, tabellen, graaf. Klaar als de vier landschapstests groen zijn.
9. Dossier en uitdraai. Klaar als de resterende browsertests groen zijn.
10. Workflows, `LEESMIJ.md`, README, werkwijze, verantwoording; Pages live. Klaar als `/procescheck/` de
    pagina toont en `/procescheck/uitleg/` de uitleg, en statuut groen is.
11. Applicatiecode van `main`; profiel, architectuur, werkmap-CLAUDE.md; `blast-radius` archiveren.
12. `aanvalspaden#4`: in de CSIR-tool een verwijzingsveld naar een procescheck-dossier (eigen kleine stap).

## 14. Valkuilen

- **Schaal andersom dan bij de CSIR.** Hier is 1 het ergst en is de aggregatie `min`. Noem het in de code
  en test het expliciet; een `max` sluipt er anders in.
- **Optiewaarde leeg.** Een `<select>` met `value=""` voor "geen score" moet naar `null` in het dossier,
  niet naar `0` en niet naar `""`; anders telt `min` verkeerd.
- **Datumvergelijking** als tekst `JJJJ-MM-DD` werkt lexicografisch; de cutoff van "een jaar terug" bouw je
  als string, met de 29-februari-regel.
- **Het gedachtestreepje** in de prioriteitstekst van `dashboard.py`: de bron krijgt een komma; de test op
  `dashboard.py` vergelijkt daarom alleen de twee andere redenen letterlijk.
- **Import matcht op label hoofdletterongevoelig**, maar codes zijn hoofdlettergevoelig; documenteer dat in
  de melding na import ("3 processen herkend, 1 aangemaakt").
- **Grote landschappen.** De graaf beperkt zich boven 60 nodes; de tabellen niet. Test met het voorbeeld
  (14 nodes) en met een gegenereerd landschap van 200 nodes dat de pagina niet vastloopt (een browsertest
  met een tijdslimiet van 5 seconden).
- Verder alles uit hoofdstuk 14 van het CSIR-plan: `</` in de data, Windows-regeleindes, inline styles,
  `§`-tekens in selectors, expliciet stagen.

## 15. Buiten scope

- Meerdere organisaties in één dossier; rollen en rechten; een auditlog.
- Export naar xlsx, docx of pptx.
- Een tweede laag onder componenten (bijvoorbeeld leveranciers); de blast radius kent ci, app en proces.
- De koppeling naar diepte 1 van de aanvalspaden anders dan als uitdraai (de kroonjuwelenlijst).
