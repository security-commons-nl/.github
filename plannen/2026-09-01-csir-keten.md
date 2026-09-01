# Bouwplan: de CSIR-keten in de browser (classificeren, bepalen, uitwerken)

**Doel:** de twee Excel-bestanden rond de Cybersecurity Implementatierichtlijn Objecten (CSIR) samenbrengen
tot één instrument dat in de browser draait, zoals de zelfcheck van `aanvalspaden`: het
objectclassificatie-formulier (stap 0) en het control-register van Vasilis (stap 1 en 2) worden één keten
van drie vragen rond één dossier. Geen server, geen account, geen telemetrie, geen dependency in de pagina.

**Aanleiding:** `csir-control-register` is op 01-09-2026 gepubliceerd als Excel-werkboek (eerste repo in
de commons die geheel door een andere auteur is opgezet). Een werkboek is voor de Excel-gebruiker prima,
maar het staat niet op de voorkant als iets dat je opent en gebruikt, het is per object een kopie, en de
classificatie ervoor zit in een los formulier uit 2015. De commons heeft voor precies dit patroon al een
werkende vorm: één zelfstandig HTML-bestand met de bron als JSON erin en een Content-Security-Policy die
de offlinebelofte afdwingt.

**Architectuur:** een map `register/` in de bestaande repo `csir-control-register`, naast het werkboek. Eén
bronbestand `csir.json` op de repo-root, eenmalig uit de twee werkboeken gehaald en daarna de enige
waarheid. Het Excel-werkboek blijft zolang het er is een download en een export; een test bewaakt dat
het niet van de JSON afdrijft. Valt het werkboek ooit weg, dan vervalt alleen die test.

**Tech stack:** Python 3.12 (bouwscript, referentie-implementatie, tests), openpyxl (alleen voor
`haal_bron.py` en `test_bron.py`), pytest, Playwright (browsertests), vanilla JS en CSS in de pagina.
Geen bundler. Zelfde patroon als `aanvalspaden/check/`; lees die map eerst, alles hier is daar een
variant van.

**Status:** geschreven 01-09-2026 na een spar met Bas; de auteur van het werkboek is op de hoogte en
akkoord met de aanpak. Wacht op uitvoering. Dit plan is geschreven om zonder verdere toelichting
gebouwd te kunnen worden: waar iets niet in dit plan staat, volg je `aanvalspaden/check/`.

---

## 0. Besluiten (de spec)

1. **Eén keten, drie modules, één dossier.** Classificeren (functiebox), Bepalen (welke controls en
   maatregelen gelden op dit niveau), Uitwerken (invulling, bewijs, verantwoordelijke, afwijking, en
   de handleidingen uit de kennisbank erbij). Eén JSON-dossier loopt door alle drie heen.
2. **`csir.json` is de bron, het werkboek is een export.** Vanaf dag één. Wie een eistekst corrigeert,
   doet dat in `csir.json` (via `haal_bron.py` als het werkboek nog leidend is voor de auteur, anders
   rechtstreeks) en nooit alleen in het xlsx. Een test blokkeert als json en xlsx uit elkaar lopen.
3. **De pagina bevat geen eigen kopie van eisteksten, codes of drempels.** Alles komt uit
   `window.__BRON__`. Een test blokkeert als `app.js` een control-code, maatregelcode of eistekst bevat.
4. **Rekenregels zijn woordelijk de Excel-formules.** Waar Excel en gezond verstand verschillen (het
   afgeronde gemiddelde bij de classificatie), volgt de tool Excel en toont hij de alternatieve lezing
   ernaast. Wijzigen van een rekenregel is een besluit van de auteur, niet van de bouwer.
5. **Offline en dicht.** CSP `default-src 'none'`, script en stylesheet op sha256, geen enkele externe
   verwijzing behalve gewone links (`<a href>`) naar `security-commons-nl.github.io` en
   `github.com/security-commons-nl`. Opslaan is een download, laden is een bestandskeuze; er gaat niets
   naar een server.
6. **Geen AI-laag.** Besloten 01-09-2026. Module 3 is de koppeling naar de kennisbank plus de invulvelden.
   Een AI-concept per maatregel zou een verbinding vereisen en de situatiebeschrijving van een
   tunnel of gemaal naar buiten sturen; dat is niet aan de orde.
7. **Tests zijn de definition of done.** Niets is klaar zonder groene test op precies dat onderdeel
   (hoofdstuk 10). De browsertests vergelijken met een Python-referentie (`reken.py`) én met een
   in Excel ingevulde doorloop.
8. **Statuut geldt.** Kruimelpad (B10), README-kop (B11), status in de projectentabel (B8, B9, B12),
   Nederlands, geen auteursvermelding, geen AI-attributie in commits. Auteursrecht op de eisteksten
   ligt bij Rijkswaterstaat en Het Waterschapshuis; dat staat in `csir.json`, in de voettekst van de
   pagina en in de README.

## 1. Wat er nu is (feiten, gecontroleerd op 01-09-2026)

**`werkboek/csir-control-register.xlsx`** (111 kB, versie 1.3, geen macro's), zeven bladen:

| Blad | Inhoud | Kolommen |
|---|---|---|
| Instellingen | object (C5), functiebox (C6, validatie A..E), effectief niveau (C7, formule), ketenregel: C12 Ja/Nee, drie bestuurde objecten B15:C17 met niveau D15:D17, hoogste keten-niveau D18; bevestigd door B20/C20, datum B21/C21; tabel functiebox → niveau B25:C29; metadata B36:C40 | workbook-namen `Object`=C5, `Functiebox`=C6, `Niveau`=C7 |
| Toelichting | uitleg en legenda | tekst |
| Dashboard | tellers per blad en per paragraaf | B6:O25, alles formules |
| VSP Proceseisen | 89 controls, rij 4..92 | A Nr · B BIO-bron (ISO 27001:2013 Annex A-nummer, niet uniek: 63 verschillende) · C Control-eis (letterlijk) · D Aangeroepen §2 · E Bijlage (CSR) · F Van toepassing · G Status · H Invulling / bewijs · I Verantwoordelijke · J Comply-or-explain / opmerkingen · K Korte omschrijving (niet normatief) |
| VSE Systeemeisen | 38 controls, rij 4..41 | zelfde kolommen |
| Maatregelen | 268 maatregelen, rij 4..271 | A Paragraaf · B Thema · C Groep · D Code (uniek) · E Maatregel (letterlijk) · F..I N1..N4 (`X` = geldt) · J Geldt (formule) · K In scope? (formule) · L Status · M Invulling / bewijs · N Verantwoordelijke · O Opmerkingen · Q..T verborgen hulpkolommen |
| Bijlagen | 27 bijlagen, rij 4..30 | A Bijlage (CSR 1..24, A, B, C) · B Titel · C Type · D Aangeroepen door (# controls) · E Van toepassing · F Status · G Opmerkingen |

Validatielijsten (letterlijk, met deze spelling):
- Van toepassing (controls F, bijlagen E): `Ja`, `Nee`, `N.v.t. (buiten scope)`. Controls staan voorgevuld op `Ja`.
- Status (controls G, maatregelen L, bijlagen F): `Nog te doen`, `In uitvoering`, `Geïmplementeerd`, `Explain (afwijking)`, `N.v.t.`.
- Functiebox: `A`, `B`, `C`, `D`, `E`. Keten: `Ja`, `Nee`.

Paragrafen en thema's (15, samen 268 maatregelen):

| § | Thema | Aantal |
|---|---|---|
| §2.1.1 | Fysieke toegangsbeveiliging, IA-gerelateerde ruimten | 32 |
| §2.1.2 | Fysieke toegangsbeveiliging, terreinen en gebouwen | 33 |
| §2.2 | Logische toegang | 31 |
| §2.3 | Beveiligingsincidenten en incident response | 15 |
| §2.4.1 | Netwerkkoppelingen | 16 |
| §2.4.2 | Cryptografie | 7 |
| §2.5.1 | Bescherming tegen kwetsbaarheden, anti-malware | 10 |
| §2.5.2 | Bescherming tegen kwetsbaarheden, hardening | 10 |
| §2.5.3 | Bescherming tegen kwetsbaarheden, patching | 8 |
| §2.6 | Logging en monitoring | 33 |
| §2.7.1 | Bewustwording en training, medewerkers | 27 |
| §2.7.2 | Bewustwording en training, managers | 6 |
| §2.8 | Gecontroleerd wijzigen | 15 |
| §2.9 | Beheer en onderhoud | 18 |
| §2.10 | Back-ups | 7 |

Per niveau gelden 193 (N1), 198 (N2), 230 (N3) en 234 (N4) maatregelen. Van de 127 controls roepen er
32 een paragraaf aan (kolom D); de andere 95 hebben daar niets staan. Kolom D bevat altijd precies één
waarde, soms op het niveau van de ouder (`§2.4`, `§2.5`, `§2.7`). Kolom E bevat `1`..`24` (bedoeld is
`CSR n`), `A`, `B`, `C` of combinaties gescheiden door ` / ` (bijvoorbeeld `B / C`).

**`Object Classificatie.xlsx`** (het formulier, één blad, aangemaakt 2015, herkomst waterschappen):
zes gevolgcriteria met per criterium vijf drempels (ernst 1..5), een kopblok (organisatie, proces,
object/objectgroep, locatie, ingevuld door, team, datum), keuzelijst hoofdtaak (H44:H51), situatiebeschrijving,
onderbouwing per criterium, opmerkingen. Formules: `R26 = E26+G26+I26+K26+M26+O26` (som van de zes
scores) en `S26 = ROUND(R26/6; 0)` (afgerond gemiddelde). De tabel ernst → functiebox → niveau staat in
R21:S25: 1=E→1, 2=D→1, 3=C→2, 4=B→3, 5=A→4. Het formulier komt in de repo als
`werkboek/objectclassificatie.xlsx`.

De criteria (kolomkoppen rij 19, uitleg rij 20, drempels rij 21..25; letterlijk overnemen in `haal_bron.py`):

| id | Titel | Kolom uitleg | Kolom drempels |
|---|---|---|---|
| `veiligheid` | Veiligheid medewerker en/of publiek | E20 | F21:F25 |
| `maatschappij` | Maatschappelijke gevolgen | G20 | H21:H25 |
| `financieel` | Financiële (economische) en/of herstelschade | I20 | J21:J25 |
| `cascade` | Cascade/domino effecten | K20 | L21:L25 |
| `ecologie` | Ecologische schade | M20 | N21:N25 |
| `imago` | Imago en politieke schade | O20 | P21:P25 |

Ernstlabels B21:C25: 1 Klein, 2 Matig, 3 Behoorlijk, 4 Ernstig, 5 Catastrofaal.

## 2. Doelstructuur van de repo

```
csir-control-register/
├── README.md                        (B11-kop; Snel starten: eerst online, dan download)
├── CONTRIBUTING.md · LICENSE · werkwijze.md · verantwoording.md   (bestaand)
├── csir.json                        DE BRON (gegenereerd door register/haal_bron.py, in git)
├── werkboek/
│   ├── csir-control-register.xlsx   (bestaand; export, blijft downloadbaar)
│   └── objectclassificatie.xlsx     (het formulier, nieuw in de repo)
├── register/
│   ├── LEESMIJ.md                   (wat, hoe bouwen, hoe testen; analoog aan check/LEESMIJ.md)
│   ├── haal_bron.py                 xlsx → csir.json, met --check
│   ├── haal_handelingsperspectief.py  kopie uit de kennisbank → register/handelingsperspectief.json, met --check
│   ├── handelingsperspectief.json   (kopie, in git)
│   ├── paragrafen-barrieres.json    handgeschreven koppeling §2.x → barrières (hoofdstuk 7)
│   ├── reken.py                     referentie-implementatie van alle rekenregels (alleen stdlib)
│   ├── bouw.py                      → register/dist/index.html (of <doelmap>/index.html)
│   ├── bron/
│   │   ├── index.html               sjabloon met __CSS__, __SCRIPT__, __SCRIPT_HASH__, __STYLE_HASH__
│   │   ├── app.css
│   │   └── app.js
│   ├── dist/                        (gebouwd; in .gitignore)
│   └── tests/
│       ├── test_bron.py · test_reken.py · test_bouw.py · test_app.py
│       └── fixtures/doorloop-2026-09.json
├── site/                            (bestaand: docs-build, blijft; uitvoer verhuist naar dist/uitleg/)
└── .github/workflows/
    ├── ci.yml                       (nieuw)
    ├── pages.yml                    (vervangt de caller van pages-docs.yml)
    └── statuut.yml                  (bestaand)
```

`.gitignore` krijgt `register/dist/`, `dist/`, `node_modules/`, `__pycache__/`, `.pytest_cache/`.

## 3. Datamodel: `csir.json`

Sleutels in deze volgorde. Strings zonder afkappen; regeleindes uit het xlsx blijven `\n`.

```json
{
  "versie": "2026-09",
  "bron": {
    "richtlijn": "Cybersecurity Implementatierichtlijn Objecten (CSIR) 3.0, definitief concept 14-09-2021",
    "gestripte_variant": "CSIR 3.4, gestripte variant voor aanbestedingen; hoofdstuk 2 en de bijlagen zijn identiek",
    "uitgever": "Rijkswaterstaat en Het Waterschapshuis",
    "auteursrecht": "De eisteksten, maatregelteksten, niveaumarkeringen en drempels zijn woordelijk overgenomen uit de CSIR; het auteursrecht daarop ligt bij Rijkswaterstaat en Het Waterschapshuis. EUPL-1.2 dekt alleen de opzet van dit register.",
    "werkboek_versie": "1.3",
    "werkboek_sha256": "<sha256 van werkboek/csir-control-register.xlsx>",
    "classificatie_sha256": "<sha256 van werkboek/objectclassificatie.xlsx>",
    "gegenereerd_door": "register/haal_bron.py; wijzig de bron, niet dit bestand met de hand"
  },
  "functiebox_niveau": {"A": 4, "B": 3, "C": 2, "D": 1, "E": 1},
  "classificatie": {
    "ernst": [
      {"score": 1, "label": "Klein",        "functiebox": "E", "niveau": 1},
      {"score": 2, "label": "Matig",        "functiebox": "D", "niveau": 1},
      {"score": 3, "label": "Behoorlijk",   "functiebox": "C", "niveau": 2},
      {"score": 4, "label": "Ernstig",      "functiebox": "B", "niveau": 3},
      {"score": 5, "label": "Catastrofaal", "functiebox": "A", "niveau": 4}
    ],
    "criteria": [
      {"id": "veiligheid", "titel": "Veiligheid medewerker en/of publiek", "uitleg": "<E20>",
       "drempels": {"1": "<F21>", "2": "<F22>", "3": "<F23>", "4": "<F24>", "5": "<F25>"}}
      // ... zes stuks, volgorde en ids uit hoofdstuk 1
    ],
    "hoofdtaken": ["Transporteren afvalwater", "Zuiveren afvalwater", "Verwerken en afzetten slib",
                   "Beheer hoeveelheid water", "Beheer waterkeringen", "(Vaar)wegen", "Kantoren",
                   "Tunnel", "Gemaal", "Brug", "Sluis", "Verkeersregelinstallatie", "Parkeergarage",
                   "Overige (Beschrijf bij opmerking)"],
    "rekenregel_standaard": "gemiddelde",
    "toelichting_rekenregel": "Het formulier neemt het afgeronde gemiddelde van de zes scores (ROUND(som/6;0), half naar boven). De tool toont daarnaast de strengste lezing (hoogste score). Welke lezing de CSIR bedoelt is een open vraag aan de auteur; tot die tijd volgt de tool het formulier."
  },
  "paragrafen": [
    {"id": "§2.1.1", "ouder": "§2.1",  "thema": "<uit kolom B Maatregelen>", "maatregelen": 32},
    {"id": "§2.2",   "ouder": "§2.2",  "thema": "Logische toegang", "maatregelen": 31}
    // ... alle 15 uit hoofdstuk 1, in de volgorde van het blad
  ],
  "controls": [
    {"id": "VSP-1", "blad": "VSP", "nr": 1, "bio_bron": "5.1.1", "eis": "<C>",
     "aangeroepen": ["§2.2"], "bijlagen": ["CSR 3"], "kort": "<K>"}
    // ... 89 VSP, dan 38 VSE; id = blad + "-" + nr
  ],
  "maatregelen": [
    {"code": "FR1", "paragraaf": "§2.1.1", "thema": "<B>", "groep": "<C>", "tekst": "<E>", "niveaus": [1]}
    // ... 268; niveaus = de n waarvoor kolom F..I een "X" heeft, oplopend
  ],
  "bijlagen": [
    {"id": "CSR 1", "titel": "<B>", "type": "Richtlijn", "aangeroepen_door": 1}
    // ... 27; aangeroepen_door is een getal of null (bijlage A heeft "—")
  ]
}
```

Normalisatie in `haal_bron.py`:
- `aangeroepen`: waarde uit kolom D, gesplitst op `,`, `;` en `/`, elk deel gestript; lege cel → `[]`.
  Elk deel moet matchen op `^§2\.\d+(\.\d+)?$`, anders stopt het script met een foutmelding.
- `bijlagen`: kolom E gesplitst op `/`, gestript; een deel dat alleen cijfers is wordt `CSR <n>`;
  `A`, `B`, `C` blijven. Lege cel → `[]`.
- `ouder(id)`: telt de punten in het id; twee of meer punten → alles tot en met het tweede segment
  (`§2.5.1` → `§2.5`); anders het id zelf. Dit is letterlijk Excel-kolom Q.
- `niveaus`: per maatregel de lijst van n in 1..4 waarvoor de cel in kolom F+n-1 gelijk is aan `X`
  (hoofdletter, gestript).
- Teksten: `str(cel).strip()`; geen verdere bewerking. Cellen met een formule (C5 en K5 op VSE) worden
  met `data_only=True` gelezen, zodat de berekende tekst komt; als dat `None` oplevert, stopt het script
  en meldt het welke cel (dan moet het xlsx één keer in Excel zijn opgeslagen).
- `--check`: genereert in het geheugen en vergelijkt met het bestaande `csir.json` (na `json.loads`,
  niet op bytes); exit 0 bij gelijk, exit 1 met de eerste drie verschillen bij ongelijk.
- Het script schrijft met `ensure_ascii=False`, `indent=1`, en `newline="\n"`.

## 4. Rekenregels (`register/reken.py`, en één-op-één in `app.js`)

Alle functies puur, zonder toestand. In `app.js` staan dezelfde functies met dezelfde namen in een
object `reken`, zodat een reviewer ze naast elkaar kan leggen.

```
rond_half_omhoog(x)                     Excel ROUND: floor(x + 0.5) voor x >= 0. NIET Python round().

klassificeer(scores, ernst)             scores: dict id -> 1..5 of None (leeg)
  als een score None is: uitkomst {"compleet": false, ...} zonder functiebox
  som         = som van de zes scores
  gemiddelde  = rond_half_omhoog(som / 6)                 (1..5)
  hoogste     = max(scores)
  per lezing r in ("gemiddelde", "hoogste"): functiebox = ernst[r].functiebox, niveau = ernst[r].niveau
  retour {"compleet": true, "som", "gemiddelde", "hoogste", "gemiddelde_functiebox", "gemiddelde_niveau",
          "hoogste_functiebox", "hoogste_niveau"}

niveau_van_functiebox(fb, tabel)        tabel = functiebox_niveau; lege of onbekende fb → {"niveau": 1, "voorlopig": true}
                                        anders {"niveau": tabel[fb], "voorlopig": false}

effectief_niveau(instellingen, tabel)
  eigen  = niveau_van_functiebox(instellingen.functiebox)
  keten  = 0
  als instellingen.keten.actief:
      keten = max(tabel[o.functiebox] voor o in instellingen.keten.objecten als o.functiebox in tabel; anders 0)
  retour {"eigen": eigen.niveau, "keten": keten, "effectief": max(eigen.niveau, keten), "voorlopig": eigen.voorlopig}
  (Excel C7: MAX(eigen, D18); D18 = IF(C12="Ja", MAX(D15:D17), 0). Let op: als de functiebox leeg is
   maar de keten een niveau geeft, is het effectieve niveau het ketenniveau en toch "voorlopig".)

ouder(paragraaf)                        zie hoofdstuk 3

geldt(maatregel, niveau)                niveau in maatregel.niveaus

aanroepende_controls(paragraaf, controls)
  alle controls c waarvoor paragraaf in c.aangeroepen OF ouder(paragraaf) in c.aangeroepen
  (Excel telt A en Q apart op; als A == Q telt Excel dubbel, maar alleen > 0 en == 0 doen ertoe,
   dus een set is gelijkwaardig)

scope(maatregel, niveau, controls, dossier)
  als niet geldt(maatregel, niveau):                          "Niet op dit niveau"
  C = aanroepende_controls(maatregel.paragraaf, controls)
  R = aantal c in C met dossier.controls[c.id].vt == "Ja"
  S = aantal c in C
  T = aantal c in C met dossier.controls[c.id].vt == ""     (leeg; "Nee" en "N.v.t. (buiten scope)" tellen niet als leeg)
  als R > 0:                                                  "In scope"
  als S > 0 en T == 0:                                        "Buiten scope"
  anders:                                                     "Nog te bepalen"
  (Dus: een paragraaf die door geen enkele control wordt aangeroepen (S == 0) is altijd "Nog te bepalen".
   Dat is Excel-gedrag en blijft zo.)

dashboard(bron, dossier)
  niveau = effectief_niveau(...).effectief
  per blad in ("VSP", "VSE"):
     rijen  = controls van dat blad
     vt     = aantal met dossier.vt == "Ja"
     per status s in (Nog te doen, In uitvoering, Geïmplementeerd, Explain (afwijking), N.v.t.):
        tel[s] = aantal met vt == "Ja" EN dossier.status == s
     pct_impl  = 0 als (vt - tel[N.v.t.]) == 0, anders tel[Geïmplementeerd] / (vt - tel[N.v.t.])
     pct_afgeh = 0 als (vt - tel[N.v.t.]) == 0, anders (tel[Geïmplementeerd] + tel[Explain (afwijking)]) / (vt - tel[N.v.t.])
  rij "maatregelen":
     basis  = maatregelen waarvoor geldt(m, niveau)
     vt     = aantal basis
     tel[s] = aantal in basis met dossier.maatregelen[code].status == s
     percentages als hierboven
  rij "totaal": sommen van de drie rijen; percentages opnieuw berekend uit de sommen (niet gemiddeld)
  controls_ja / controls_nee / controls_nvt / controls_leeg: tellingen over alle 127 controls op vt
  scope_in / scope_buiten / scope_nog: tellingen over alle 268 maatregelen op scope(...)
     (Excel K telt "Niet op dit niveau" nergens mee; die categorie blijft buiten deze drie)
  per paragraaf p uit bron.paragrafen:
     op_niveau = aantal maatregelen in p met geldt
     geimpl    = aantal daarvan met status == "Geïmplementeerd"
     pct       = null als op_niveau == 0, anders geimpl / op_niveau
```

Percentages worden als getal 0..1 teruggegeven; de pagina toont ze als geheel procent (`Math.round(x*100) + "%"`).

## 5. Dossierformaat (opslaan, laden, localStorage)

Sleutel in `localStorage`: `csir-dossier`. Bestandsnaam bij opslaan:
`csir-dossier-<slug van objectnaam of "object">-<JJJJ-MM-DD>.json`. Slug: kleine letters, `a-z0-9`,
overige tekens → `-`, meervoudige `-` samengevoegd, maximaal 40 tekens.

```json
{
  "formaat": "csir-dossier",
  "versie": 1,
  "bron_versie": "2026-09",
  "bron_sha256": "<vingerafdruk van csir.json, zie hieronder>",
  "bijgewerkt": "2026-09-01T20:15:00",
  "object": {"naam": "", "organisatie": "", "proces": "", "locatie": "", "hoofdtaak": "",
             "situatie": "", "ingevuld_door": "", "team": "", "datum": ""},
  "classificatie": {
    "scores": {"veiligheid": null, "maatschappij": null, "financieel": null, "cascade": null, "ecologie": null, "imago": null},
    "onderbouwing": {"veiligheid": "", "maatschappij": "", "financieel": "", "cascade": "", "ecologie": "", "imago": ""},
    "opmerkingen": ""
  },
  "instellingen": {
    "functiebox": "",
    "functiebox_bron": "",
    "keten": {"actief": false,
              "objecten": [{"naam": "", "functiebox": ""}, {"naam": "", "functiebox": ""}, {"naam": "", "functiebox": ""}],
              "bevestigd_door": "", "datum": ""}
  },
  "controls":    {"VSP-1": {"vt": "Ja", "status": "", "bewijs": "", "verantwoordelijke": "", "opmerking": ""}},
  "maatregelen": {"FR1":   {"status": "", "bewijs": "", "verantwoordelijke": "", "opmerking": ""}},
  "bijlagen":    {"CSR 1": {"vt": "", "status": "", "opmerking": ""}}
}
```

- Een nieuw dossier bevat alle 127 controls met `vt: "Ja"` (Excel-voorinvulling) en verder lege velden;
  maatregelen en bijlagen mogen ontbreken en gelden dan als leeg. `functiebox_bron` is `"classificatie"`
  als de functiebox via de knop uit module 1 is overgenomen, `"handmatig"` als hij op Instellingen is gekozen.
- `bron_sha256` = sha256 over `json.dumps(kern, ensure_ascii=False, sort_keys=True, separators=(",", ":"))`
  met `kern = {"controls", "maatregelen", "bijlagen", "classificatie", "functiebox_niveau"}` uit `csir.json`.
  `bouw.py` berekent hem en zet hem in `window.__BRON__.vingerafdruk`; de pagina zet hem in het dossier.
  Zo werkt de vergelijking platform- en volgorde-onafhankelijk (zelfde reden als in
  `aanvalspaden/tools/haal_handelingsperspectief.py`).
- Laden: bestand kiezen, `JSON.parse`, controleren `formaat == "csir-dossier"` en `versie == 1`; anders een
  melding en niets overschrijven. Verschilt `bron_sha256` van de huidige bron, dan laadt de pagina wel,
  maar toont in `#dossier-status`: "Dit dossier is gemaakt met bronversie <x>; deze pagina gebruikt <y>.
  Controleer de tellers." Onbekende control- of maatregelsleutels worden genegeerd en geteld in die melding.
- Opslaan: `new Blob([JSON.stringify(dossier, null, 1)], {type: "application/json"})`, `URL.createObjectURL`,
  een `<a download>` klikken, daarna `URL.revokeObjectURL`. Dit werkt onder de CSP (een download is geen
  fetch en geen navigatie waar `default-src` over gaat); `test_app` controleert het.
- Wissen: bevestigingsdialoog (`confirm`), daarna `localStorage.removeItem` en een vers dossier.
- Elke wijziging schrijft direct naar `localStorage` (geen opslaan-knop nodig voor de browser zelf).

## 6. De pagina: schermen, elementen, gedrag

Kop (zoals `check/bron/index.html`): kruimelpad `Security Commons NL › CSIR-keten`, naam, subregel
"Werkt offline · je dossier blijft op dit apparaat". Daaronder een vaste balk met de dossierknoppen en
de tabs. Voettekst: bron en methode op GitHub, licentie, auteursrechtregel (letterlijk uit
`bron.auteursrecht`), "Offline gebruiken? Sla deze pagina op met Ctrl+S."

Tabs (`<button role="tab">`), elk met een `<section>`; precies één zichtbaar. Ids:

| Tab-id | Sectie-id | Inhoud |
|---|---|---|
| `#tab-classificatie` | `#scherm-classificatie` | module 1 |
| `#tab-instellingen` | `#scherm-instellingen` | object, functiebox, keten |
| `#tab-dashboard` | `#scherm-dashboard` | tellers |
| `#tab-vsp` | `#scherm-vsp` | 89 controls |
| `#tab-vse` | `#scherm-vse` | 38 controls |
| `#tab-maatregelen` | `#scherm-maatregelen` | 268 maatregelen met filters en handreiking |
| `#tab-bijlagen` | `#scherm-bijlagen` | 27 bijlagen |
| `#tab-uitdraai` | `#scherm-uitdraai` | de dossier-uitdraai (print) |

Dossierbalk: `#knop-opslaan`, `#knop-laden` (opent verborgen `#bestand-laden` van type file, accept `.json`),
`#knop-wissen`, `#knop-afdrukken` (roept `window.print()` aan na het tonen van `#scherm-uitdraai`),
statusregel `#dossier-status` (toont objectnaam, effectief niveau, laatst bijgewerkt, en waarschuwingen).

**Scherm classificatie.** Kopvelden: `#obj-organisatie`, `#obj-proces`, `#obj-naam` (zelfde veld als op
Instellingen; één waarde in het dossier), `#obj-locatie`, `#obj-hoofdtaak` (select uit `hoofdtaken`),
`#obj-ingevuld-door`, `#obj-team`, `#obj-datum`, `#obj-situatie` (textarea). Per criterium een blok met
titel, uitleg, en een `<select data-criterium="<id>">` met opties leeg, 1..5, waarbij elke optie de
ernstlabel en de drempel toont ("3 · Behoorlijk · < 50.000 personen"); daaronder
`<textarea data-onderbouwing="<id>">`. Uitkomstblok: `#klas-som`, `#klas-gemiddelde` (score plus label),
`#klas-functiebox`, `#klas-niveau`, en de tweede lezing `#klas-hoogste`, `#klas-hoogste-functiebox`,
`#klas-hoogste-niveau` met de tekst uit `toelichting_rekenregel`. Zolang niet alle zes gescoord zijn,
tonen de uitkomstvelden "nog niet compleet". Knop `#knop-classificatie-overnemen`: zet
`instellingen.functiebox` op `gemiddelde_functiebox`, `functiebox_bron` op `"classificatie"` en springt
naar Instellingen. `#klas-opmerkingen` (textarea).

**Scherm instellingen.** `#obj-naam` (gespiegeld), `#obj-functiebox` (select leeg, A..E; wijzigen zet
`functiebox_bron` op `"handmatig"`), `#keten-actief` (select Nee/Ja), drie rijen
`[data-keten-naam="1|2|3"]` en `[data-keten-fb="1|2|3"]`, `#keten-bevestigd`, `#keten-datum`.
Uitkomst: `#niveau-eigen`, `#niveau-keten`, `#niveau-effectief`; `#waarschuwing-functiebox` zichtbaar
(zonder `hidden`) zolang `voorlopig` waar is, met de tekst "Vul eerst de functiebox in; niveau 1 is een
voorlopige waarde, geen vastgesteld niveau." De tabel functiebox → niveau en het ketenregel-citaat
(§0.3) staan als hulptekst op dit scherm; het citaat komt uit `csir.json` niet, maar uit het sjabloon
(het is toelichting, geen eis).

**Schermen VSP en VSE.** Eén tabel per blad, elke rij `<tr data-control="VSP-1">` met kolommen: Nr,
BIO-bron, Control-eis (volledige tekst, `white-space: pre-line`), Aangeroepen §2, Bijlagen, Van toepassing
(`select.vt`), Status (`select.status`), Invulling / bewijs (`input.bewijs`), Verantwoordelijke
(`input.verantwoordelijke`), Opmerking (`input.opmerking`). De korte omschrijving staat als `title` op de
eis-cel en niet als eigen kolom (niet normatief, statuutvriendelijk klein). Boven de tabel een
`input#zoek-vsp` / `input#zoek-vse` (filter op tekst in eis, BIO-bron en code) en een teller
`#teller-vsp` / `#teller-vse` ("x van 89 zichtbaar").

**Scherm maatregelen.** Filters boven de tabel: `#filter-geldt` (checkbox, standaard aan: "alleen wat op
niveau <n> geldt"), `#filter-scope` (select: alle, In scope, Buiten scope, Nog te bepalen, Niet op dit
niveau), `#filter-paragraaf` (select: alle, dan de 15 paragrafen met thema), `#filter-status` (select:
alle, de vijf statussen, leeg), `#zoek-maatregelen`. Teller `#teller-maatregelen` ("x van 268 zichtbaar").
De tabel is gegroepeerd per paragraaf: een groepskop `<tr class="paragraaf" data-paragraaf="§2.2">` met
id, thema, aantal op dit niveau en de handreiking (hoofdstuk 7), daaronder de rijen
`<tr data-maatregel="FR1">` met: Code, Groep, Maatregel (tekst), Niveaus (bijvoorbeeld "1 2 3 4" met het
actuele niveau vet), Geldt (`td.geldt`: "Ja" of "—"), Scope (`td.scope`: een van de vier waarden, als
tekst; kleur via een class `scope-in`, `scope-buiten`, `scope-nog`, `scope-niet`), Status
(`select.status`), Invulling / bewijs, Verantwoordelijke, Opmerking. Rijen die niet gelden krijgen class
`grijs` (zoals in Excel) en zijn met `#filter-geldt` uit standaard verborgen.

**Scherm bijlagen.** Tabel `<tr data-bijlage="CSR 1">`: Bijlage, Titel, Type, Aangeroepen door, Van
toepassing (`select.vt`), Status (`select.status`), Opmerking.

**Scherm dashboard.** Alle waarden in elementen met `data-teller`:

| `data-teller` | Betekenis |
|---|---|
| `vsp.vt`, `vsp.todo`, `vsp.bezig`, `vsp.klaar`, `vsp.explain`, `vsp.nvt`, `vsp.pct_impl`, `vsp.pct_afgeh` | rij VSP |
| `vse.*` | idem VSE |
| `maatregelen.*` | rij maatregelen op dit niveau (kop "Maatregelen (niv. n)") |
| `totaal.*` | somrij |
| `controls.ja`, `controls.nee`, `controls.nvt`, `controls.leeg` | van-toepassing-verdeling over 127 controls |
| `scope.in`, `scope.buiten`, `scope.nog` | scope-verdeling over de maatregelen |
| `paragraaf.<id>.op_niveau`, `paragraaf.<id>.geimpl`, `paragraaf.<id>.pct` | per paragraaf, `<id>` letterlijk (`§2.1.1`) |

Percentages als "42%"; `pct` van een paragraaf zonder maatregelen op dit niveau als "—". Boven het
dashboard dezelfde waarschuwing als op Instellingen als de functiebox leeg is.

**Scherm uitdraai.** Wordt bij tonen opnieuw opgebouwd uit het dossier. Vaste volgorde, elk met een `<h2>`:
1. Object en classificatie: kopvelden, per criterium score, label en onderbouwing, som, gemiddelde,
   functiebox, niveau, tweede lezing, opmerkingen.
2. Niveau en keten: functiebox (met bron), keten actief, de bestuurde objecten, effectief niveau,
   bevestigd door en datum.
3. Dashboard: dezelfde tellers als het dashboardscherm, als tabel.
4. Controls van toepassing: alle controls met vt `Ja`, per blad, met status, bewijs en verantwoordelijke.
   Daaronder, apart, de controls op `Nee` en `N.v.t. (buiten scope)` met de opmerking (de onderbouwing).
5. Maatregelen die gelden: per paragraaf de maatregelen met `geldt`, met scope, status, bewijs en
   verantwoordelijke.
6. Afwijkingen (comply-or-explain): alle controls, maatregelen en bijlagen met status `Explain (afwijking)`,
   met code, tekst (eerste 200 tekens), bewijs en opmerking. Dit is de lijst die in bijlage C van het
   Cybersecurity Dossier hoort.
7. Bijlagen: alle 27 met vt en status.
8. Voet: bronversie, vingerafdruk, datum bijgewerkt, auteursrechtregel.

`@media print`: kop, tabs, filters, dossierbalk en alle andere schermen verborgen; `#scherm-uitdraai`
zichtbaar ongeacht de actieve tab; A4 staand, tabellen `font-size: 9pt`, `page-break-inside: avoid` op
rijen, `<h2>` met `page-break-before: always` vanaf hoofdstuk 3.

**Algemeen gedrag.**
- Elke invoer schrijft naar het dossier in het geheugen, daarna `localStorage`, daarna herberekening
  van niveau, scope, dashboard en tellers. Herberekening is goedkoop (268 + 127 rijen); geen debounce nodig.
- Wijzigt het effectieve niveau, dan veranderen `td.geldt`, `td.scope`, de grijze rijen en de
  dashboardkop meteen (het punt waar Excel de gebruiker vraagt het filter te herhalen; hier hoeft dat niet).
- Geen inline `style`-attributen (de CSP verbiedt ze); een voortgangsbalk is een `<progress>`.
- Toetsenbord: tabs bereikbaar met Tab en Enter; tabellen zijn gewone `<table>` met `<th scope="col">`.
- Geen `fetch`, geen `XMLHttpRequest`, geen `import`, geen externe font, geen afbeelding behalve
  `data:`-favicon.

## 7. Module 3: de handreiking uit de kennisbank

De CSIR verwijst met de BIO-bronkolom naar de ISO 27001:2013 Annex A-nummering (bijvoorbeeld `9.1.1`,
`12.4.1`). De normverankering van de commons (`aanvalspaden/mappingen/bio2.json`) gebruikt BIO 2.0, dus de
ISO 27002:2022-nummering (`5.15`, `8.15`). Die twee sluiten zonder een 2013 → 2022-crosswalk niet op
elkaar aan. Daarom koppelt ronde 1 niet per control maar per maatregelparagraaf, met de hand, aan
barrières uit `paden.json`; de handleidingen volgen dan uit `handelingsperspectief.json`. De relatie heet
`hoort-bij`, nooit "voldoet aan": een handleiding zegt hoe je iets inricht, niet dat je klaar bent.

`register/paragrafen-barrieres.json`:

```json
{
  "versie": "2026-09",
  "toelichting": "Per maatregelparagraaf van de CSIR de barrieres uit paden.json waarvan de handleidingen in de kennisbank helpen bij het uitwerken. De relatie is hoort-bij. Een lege lijst is een schrijfopdracht, geen omissie. De koppeling op controlniveau vereist een ISO 27001:2013 naar 27002:2022-crosswalk en is ronde 2.",
  "regels": [
    {"paragraaf": "§2.1.1", "barrieres": [], "reden": "Fysieke beveiliging van IA-ruimten; de aanvalspaden gaan over de digitale kant. Handleiding gevraagd."},
    {"paragraaf": "§2.1.2", "barrieres": [], "reden": "Fysieke beveiliging van terreinen en gebouwen; zie §2.1.1."},
    {"paragraaf": "§2.2",   "barrieres": ["pr", "fallback", "legacy", "model", "jit", "key", "localadmin", "session", "remote", "unmanaged"], "reden": "Logische toegang: sterke authenticatie, geen zwakkere terugvalroute, gescheiden en tijdelijke beheerrechten, sessiebescherming en afgeschermde beheerinterfaces."},
    {"paragraaf": "§2.3",   "barrieres": ["crisis", "idresponse", "mailresponse", "exploitresponse", "ddosresponse", "owner"], "reden": "Incidenten en response: geoefende crisisaanpak, werkende responsroutes en een risicohouder die het kent."},
    {"paragraaf": "§2.4.1", "barrieres": ["segment", "remote", "assets", "origin", "upstream"], "reden": "Netwerkkoppelingen: segmentering, afgeschermd beheer, zicht op wat vanaf internet bereikbaar is."},
    {"paragraaf": "§2.4.2", "barrieres": [], "reden": "Cryptografie; geen barriere in de set gaat hierover. Handleiding gevraagd."},
    {"paragraaf": "§2.5.1", "barrieres": ["edr", "execution", "browser"], "reden": "Anti-malware: bewaakte endpoints, beperkte uitvoering van onbekende software, beperkte browser en gegevensdragers."},
    {"paragraaf": "§2.5.2", "barrieres": ["adminhard", "localadmin", "execution", "legacy"], "reden": "Hardening: beheerwerkplek op orde, geen lokale beheerrechten, uitvoering beperkt, verouderde methoden dicht."},
    {"paragraaf": "§2.5.3", "barrieres": ["patch", "vuln"], "reden": "Patching: tijdig bijwerken en kwetsbaarheden opsporen."},
    {"paragraaf": "§2.6",   "barrieres": ["adminmonitor", "edr", "session"], "reden": "Logging en monitoring: bewaking van beheerrechten, endpoints en sessies."},
    {"paragraaf": "§2.7.1", "barrieres": [], "reden": "Bewustwording medewerkers; de kennisbank heeft een item awareness-digitale-veiligheid maar dat hangt aan geen barriere. Ronde 2: koppelen via een eigen sleutel."},
    {"paragraaf": "§2.7.2", "barrieres": ["owner", "treatment"], "reden": "Bewustwording managers: de risicohouder kent de risico's en heeft restrisico's expliciet geaccepteerd of belegd."},
    {"paragraaf": "§2.8",   "barrieres": [], "reden": "Gecontroleerd wijzigen; geen barriere in de set. Handleiding gevraagd."},
    {"paragraaf": "§2.9",   "barrieres": ["review", "residual", "technicalvendor", "dependencies", "critical"], "reden": "Beheer en onderhoud, veelal uitbesteed: leveranciersbeoordeling, restrisico's, technische risico's, afhankelijkheden en kritieke processen."},
    {"paragraaf": "§2.10",  "barrieres": ["backup", "restore"], "reden": "Back-ups: beschermd tegen een aanvaller in productie en aantoonbaar herstelbaar."}
  ]
}
```

`register/haal_handelingsperspectief.py` is een kopie van `aanvalspaden/tools/haal_handelingsperspectief.py`
met andere paden (`DOEL = ROOT / "register" / "handelingsperspectief.json"`; kandidaten
`ROOT.parent / "kennisbank" / "handelingsperspectief.json"` en `ROOT / "_kennisbank" / ...`). Het
kopieert de export van de kennisbank en zet de vingerafdruk erbij; `--check` meldt of de kopie klopt.

`bouw.py` zet in `window.__BRON__.handreiking` per paragraaf een lijst `{titel, rol, url}` (uit de
export, alleen die drie velden, gesorteerd: `fundering` eerst, dan `verdieping`, dan `alternatief`, binnen
een rol op titel), plus `reden` en `barrieres` uit `paragrafen-barrieres.json`. In de pagina staat de
handreiking in de groepskop van elke paragraaf als `<details data-handreiking="§2.2">` met samenvatting
"Handleidingen uit de kennisbank (n)" en daarin de links (`<a href=url rel="noopener">titel</a>` met de
rol als label). Is de lijst leeg, dan staat er: "Nog geen handleiding in de kennisbank voor dit onderwerp.
<reden> Schrijf mee:" met een link naar `https://github.com/security-commons-nl/kennisbank/issues/new/choose`.

## 8. Bouwen: `register/bouw.py`

Letterlijk `aanvalspaden/check/bouw.py`, met deze verschillen:

- Leest `csir.json`, `register/paragrafen-barrieres.json` en `register/handelingsperspectief.json`.
  Ontbreekt het handelingsperspectief, dan stopt de bouw met een foutmelding (geen stille pagina
  zonder handreiking; zelfde keuze als in aanvalspaden).
- Bouwt `data = csir.json` plus `data["handreiking"]` (hoofdstuk 7) plus `data["vingerafdruk"]`
  (hoofdstuk 5).
- Sjabloon `register/bron/index.html` met dezelfde vier placeholders; JSON met `</` → `<\/`.
- Schrijft `register/dist/index.html` of `<doelmap>/index.html`; print grootte in kB.
- Verwachte grootte: 350 tot 500 kB. Boven 800 kB is iets mis (waarschijnlijk dubbele data).

CSP in het sjabloon, letterlijk:
`default-src 'none'; script-src 'sha256-__SCRIPT_HASH__'; style-src 'sha256-__STYLE_HASH__'; img-src data:; form-action 'none'; base-uri 'none'`

## 9. Workflows

**`.github/workflows/ci.yml`** (nieuw), twee jobs, beide op push naar main en op pull_request:

```
bron:
  checkout; checkout security-commons-nl/kennisbank naar _kennisbank
  setup-python 3.12; pip install pytest openpyxl
  python register/haal_bron.py --check
  python register/haal_handelingsperspectief.py --check
  python -m pytest register/tests/test_bron.py register/tests/test_reken.py -v
app:
  checkout; checkout kennisbank naar _kennisbank
  setup-python 3.12; pip install pytest openpyxl playwright; python -m playwright install --with-deps chromium
  python register/bouw.py
  python -m pytest register/tests/test_bouw.py register/tests/test_app.py -v
  upload-artifact: register/dist/index.html (if-no-files-found: error)
```

Gebruik dezelfde action-versies als `aanvalspaden/.github/workflows/ci.yml` op het moment van bouwen.

**`.github/workflows/pages.yml`** vervangt de huidige caller van `pages-docs.yml` (die is voor
documentatierepo's; dit wordt een toolrepo, net als aanvalspaden). Triggers: push op main,
workflow_dispatch. Permissies en concurrency zoals nu. Job `bouwen`:

```
checkout; checkout kennisbank naar _kennisbank
setup-node 24 (cache npm); npm ci; node site/build.mjs          # docs → dist/index.html + dist/werkboek/...
mkdir -p dist/uitleg && mv dist/index.html dist/uitleg/index.html
setup-python 3.12
python register/haal_handelingsperspectief.py --check
python register/bouw.py dist                                      # de keten → dist/index.html
test -s dist/index.html && test -s dist/uitleg/index.html
cp dist/index.html dist/csir-keten.html                           # dezelfde pagina als download
cp csir.json dist/csir.json
cp werkboek/objectclassificatie.xlsx dist/werkboek/
upload-pages-artifact: dist
```

Job `publiceren` zoals in aanvalspaden. Resultaat: `/csir-control-register/` is de keten,
`/csir-control-register/uitleg/` de docs-pagina met de tabs Start, Werkwijze, Verantwoording. De tabs
Werkwijze en Verantwoording in de kop van de keten zijn gewone links naar
`uitleg/#werkwijze` en `uitleg/#verantwoording`; de knop "Werkboek (Excel)" linkt naar
`werkboek/csir-control-register.xlsx`. Controleer na de eerste deploy dat de link in
`site/config.json` of `build.mjs` naar de canonieke URL nog klopt (die verwijst mogelijk naar de root).

## 10. Tests

Alle tests in `register/tests/`; `conftest.py` bouwt één keer naar `tmp_path` en leest `csir.json`.
Browsertests slaan zichzelf over als Playwright of Chromium ontbreekt (zelfde `pytest.skip`-constructie
als `check/tests/test_app.py`). Namen zijn bindend; de omschrijving is wat de test moet bewijzen.

**`test_bron.py`** (leest `csir.json` én het xlsx zelfstandig met openpyxl, onafhankelijk van `haal_bron.py`):

| Test | Bewijst |
|---|---|
| `test_aantallen` | 89 VSP-controls, 38 VSE, 268 maatregelen, 27 bijlagen, 15 paragrafen, 6 criteria met elk 5 drempels, 5 ernstrijen |
| `test_maatregelen_per_niveau` | aantal maatregelen met n in `niveaus`: 193, 198, 230, 234 voor n = 1..4 |
| `test_maatregelen_per_paragraaf` | de tabel uit hoofdstuk 1 (32, 33, 31, 15, 16, 7, 10, 10, 8, 33, 27, 6, 15, 18, 7) |
| `test_control_eisen_woordelijk` | voor elke control: `eis` == xlsx kolom C (gestript), `kort` == kolom K, `bio_bron` == kolom B |
| `test_maatregelteksten_woordelijk` | voor elke maatregel: `tekst` == kolom E, `code` == D, `paragraaf` == A, `thema` == B, `groep` == C, `niveaus` == de X-en in F..I |
| `test_bijlagen_woordelijk` | id, titel, type en aangeroepen_door gelijk aan A..D |
| `test_classificatie_woordelijk` | criteria-uitleg en drempels gelijk aan E20..P25 van het formulier; ernsttabel gelijk aan B21:C25 en R21:S25 |
| `test_sleutels_uniek` | control-ids, maatregelcodes en bijlage-ids zijn uniek; criteria-ids zijn precies de zes uit hoofdstuk 1 |
| `test_aangeroepen_paragrafen_bestaan` | elke waarde in `controls[].aangeroepen` is een paragraaf-id of een `ouder` van een paragraaf-id; 32 controls hebben er precies één, 95 hebben `[]` |
| `test_bijlage_verwijzingen_bestaan` | elke waarde in `controls[].bijlagen` komt voor in `bijlagen[].id` |
| `test_functiebox_tabel` | `functiebox_niveau` == {A:4, B:3, C:2, D:1, E:1} en gelijk aan Instellingen B25:C29 |
| `test_vingerafdrukken_kloppen` | `bron.werkboek_sha256` en `bron.classificatie_sha256` zijn de sha256 van de twee xlsx-bestanden |
| `test_auteursrecht_staat_erin` | `bron.auteursrecht` noemt "Rijkswaterstaat" en "Het Waterschapshuis" |
| `test_haal_bron_check_slaagt` | `subprocess` `python register/haal_bron.py --check` exit 0 |

**`test_reken.py`** (alleen `reken.py`, geen browser):

| Test | Bewijst |
|---|---|
| `test_rond_half_omhoog` | 2.5 → 3, 3.5 → 4, 2.49 → 2, 1.0 → 1 (en Python `round(2.5)` zou 2 geven; die val expliciet noemen in de docstring) |
| `test_functiebox_naar_niveau` | A→4, B→3, C→2, D→1, E→1; leeg → 1 met `voorlopig` waar; "Z" → 1 voorlopig |
| `test_ketenregel` | eigen B, keten Ja met bestuurd A → 4; keten Nee → 3; keten Ja met alleen lege bestuurde objecten → 3; eigen leeg met keten Ja bestuurd C → effectief 2 en `voorlopig` waar |
| `test_classificatie_gemiddelde` | scores 2,3,1,5,2,2 → som 15, gemiddelde 3, functiebox C, niveau 2; hoogste 5 → A, 4 |
| `test_classificatie_randen` | alles 1 → E/1; alles 5 → A/4; 1,1,1,1,1,2 → gemiddelde 1 → E; 3,3,3,3,3,4 → 19/6 = 3.17 → 3 → C |
| `test_classificatie_incompleet` | één score None → `compleet` onwaar en geen functiebox |
| `test_ouder` | §2.5.1 → §2.5; §2.5 → §2.5; §2.10 → §2.10; §2.1.2 → §2.1 |
| `test_aanroepende_controls_via_ouder` | een control met aangeroepen `§2.5` telt mee voor een maatregel in `§2.5.1`, `§2.5.2` en `§2.5.3`; een control met `§2.5.1` telt niet mee voor `§2.5.2` |
| `test_scope_vier_uitkomsten` | met een minimale eigen bron (twee controls, drie maatregelen): niet geldt → "Niet op dit niveau"; aanroepende control Ja → "In scope"; alle aanroepende controls Nee → "Buiten scope"; één aanroepende control leeg en geen Ja → "Nog te bepalen"; paragraaf zonder aanroepende controls → "Nog te bepalen" |
| `test_scope_nvt_telt_niet_als_leeg` | control op "N.v.t. (buiten scope)" en verder geen Ja → "Buiten scope" (niet "Nog te bepalen") |
| `test_dashboard_nieuw_dossier` | vers dossier op niveau 2: vsp.vt 89, vse.vt 38, maatregelen.vt 198, totaal.vt 325; alle statusstellers 0; percentages 0; controls.ja 127; scope.in > 0 en scope.in + scope.buiten + scope.nog == aantal maatregelen dat geldt op niveau 2 |
| `test_dashboard_percentages` | vt 10, nvt 2, geïmplementeerd 4, explain 2 → pct_impl 0.5, pct_afgeh 0.75; vt 2, nvt 2 → beide 0 |
| `test_dashboard_gelijk_aan_doorloop` | voor `fixtures/doorloop-2026-09.json`: elke waarde in `verwacht` gelijk aan `dashboard()`; als `bevestigd_in_excel` onwaar is, geeft de test een `pytest.warns`-achtige waarschuwing via `warnings.warn` maar faalt niet op dat veld |
| `test_reken_en_app_hebben_dezelfde_functies` | de namen van de functies in `reken.py` komen letterlijk voor in `app.js` als `reken.<naam>` (regex); zo blijft de spiegel zichtbaar |

**`test_bouw.py`** (op de gebouwde pagina):

| Test | Bewijst |
|---|---|
| `test_alle_eisen_en_maatregelen_staan_in_de_pagina` | elke `eis`, elke `tekst` en elke bijlagetitel komt (JSON-geëscaped) voor in de HTML |
| `test_geen_enkele_externe_verwijzing` | geen `src=`, `@import`, `url(` of `fetch(` naar `http`; `href` naar `http` alleen naar `https://security-commons-nl.github.io/` of `https://github.com/security-commons-nl/` |
| `test_csp_sluit_alles_af_en_klopt_met_de_inhoud` | de CSP-regel is letterlijk die uit hoofdstuk 8 en de twee hashes zijn de sha256 van de inhoud van de ene `<script>` en de ene `<style>` |
| `test_precies_een_script_en_een_stylesheet` | één `<script>`, één `<style>`, geen `style=`-attribuut |
| `test_de_app_bevat_geen_eigen_kopie_van_de_bron` | `app.js` bevat geen enkele maatregelcode uit `csir.json`, geen control-id, geen eistekst van 30 tekens of langer, en niet de string "Rijkswaterstaat" |
| `test_pagina_werkt_zonder_javascript_uitleg` | er is een `<noscript>` met uitleg en een verwijzing naar `csir.json` |
| `test_bouw_is_herhaalbaar` | twee keer bouwen geeft byte-gelijke uitvoer |
| `test_kruimelpad_wijst_terug_naar_de_hoofdpagina` | `<nav class="kruimel">` met link naar `https://security-commons-nl.github.io/` |
| `test_voetregel_bron_licentie_verbetering` | de voet linkt naar de repo, noemt EUPL-1.2 en bevat `bron.auteursrecht` letterlijk (B10) |
| `test_handreiking_staat_erin` | voor elke paragraaf in `paragrafen-barrieres.json` met barrières staat minstens één handleiding-url in de pagina; voor elke paragraaf zonder staat de reden in de pagina |
| `test_vingerafdruk_in_de_pagina` | `window.__BRON__.vingerafdruk` gelijk aan de berekening uit hoofdstuk 5 |

**`test_app.py`** (Playwright, Chromium, `file://` op de gebouwde pagina; elke test begint met een
schone `localStorage`):

| Test | Bewijst |
|---|---|
| `test_startscherm_toont_classificatie_en_tabs` | `#scherm-classificatie` zichtbaar, acht tabs aanwezig, `#dossier-status` toont "niveau 1 (voorlopig)" |
| `test_classificatie_rekent_en_neemt_over` | selects op 2,3,1,5,2,2 → `#klas-som` "15", `#klas-gemiddelde` bevat "3", `#klas-functiebox` "C", `#klas-niveau` "2", `#klas-hoogste-functiebox` "A"; klik `#knop-classificatie-overnemen` → `#obj-functiebox` waarde "C", `#niveau-effectief` "2", `#waarschuwing-functiebox` verborgen |
| `test_classificatie_incompleet_toont_geen_functiebox` | vijf van zes gescoord → `#klas-functiebox` bevat "nog niet compleet"; de knop is `disabled` |
| `test_instellingen_functiebox_en_keten` | `#obj-functiebox` B → `#niveau-effectief` "3"; `#keten-actief` Ja en `[data-keten-fb="1"]` A → "4"; `#keten-actief` Nee → "3" |
| `test_lege_functiebox_waarschuwt` | vers dossier: `#waarschuwing-functiebox` zichtbaar, `#niveau-effectief` "1", dashboardkop toont de waarschuwing |
| `test_maatregelenfilter_volgt_het_niveau` | functiebox C (niveau 2) → `#teller-maatregelen` "198 van 268 zichtbaar"; functiebox A → "234 van 268 zichtbaar"; `#filter-geldt` uit → "268 van 268 zichtbaar" |
| `test_control_op_nee_zet_paragraaf_buiten_scope` | kies met `reken.py` een paragraaf p die door precies één control c wordt aangeroepen (direct of via ouder) en een maatregel m in p die geldt op niveau 2; zet c op "Nee" → `tr[data-maatregel=m] td.scope` "Buiten scope"; terug op "Ja" → "In scope"; op leeg → "Nog te bepalen" |
| `test_dashboard_gelijk_aan_referentie` | laad `fixtures/doorloop-2026-09.json` via `#knop-laden`; lees alle `[data-teller]` uit en vergelijk met `reken.dashboard()` op dezelfde fixture (percentages als geheel procent) |
| `test_opslaan_geeft_een_dossierbestand` | wijzig drie velden; `page.expect_download()` rond klik op `#knop-opslaan`; bestandsnaam matcht `^csir-dossier-.+-\d{4}-\d{2}-\d{2}\.json$`; inhoud parseert, `formaat` "csir-dossier", `versie` 1, de drie velden staan erin |
| `test_laden_herstelt_de_stand` | opslaan → `#knop-wissen` (dialoog accepteren) → velden leeg → laden van het bestand → de drie velden terug, `#niveau-effectief` gelijk |
| `test_laden_weigert_verkeerd_bestand` | laad een JSON zonder `formaat` → `#dossier-status` bevat "geen dossier"; de stand is ongewijzigd |
| `test_laden_meldt_andere_bronversie` | laad een dossier met afwijkende `bron_sha256` → `#dossier-status` bevat "bronversie"; de stand is wél geladen |
| `test_herladen_bewaart` | wijzig velden, `page.reload()`, velden staan er nog |
| `test_wissen_leegt_de_opslag` | na wissen: `localStorage.getItem("csir-dossier")` is null en `#obj-naam` leeg |
| `test_uitdraai_bevat_afwijkingen` | zet één control en één maatregel op "Explain (afwijking)" met een opmerking; open `#tab-uitdraai`; hoofdstuk "Afwijkingen" bevat beide codes en beide opmerkingen; hoofdstuk 1 bevat de objectnaam |
| `test_afdrukken_toont_uitdraai` | `page.emulate_media(media="print")`: `#scherm-uitdraai` zichtbaar, `#scherm-maatregelen` en de tabs niet |
| `test_handreiking_zichtbaar_bij_paragraaf` | `[data-handreiking="§2.2"]` bevat minstens één link met `href` beginnend met `https://security-commons-nl.github.io/kennisbank/`; `[data-handreiking="§2.4.2"]` bevat "Nog geen handleiding" |
| `test_browser_geeft_dezelfde_uitslag_als_excel` | zelfde als `test_dashboard_gelijk_aan_referentie` maar tegen het blok `verwacht` in de fixture; slaat over met een duidelijke reden zolang `bevestigd_in_excel` onwaar is |
| `test_geen_console_fouten` | tijdens alle bovenstaande handelingen geen `console.error` en geen `pageerror` (verzamel via `page.on`) |

## 11. De fixture: `register/tests/fixtures/doorloop-2026-09.json`

Eén dossier plus een blok `verwacht`:

```json
{
  "dossier": { ...een volledig dossier volgens hoofdstuk 5... },
  "verwacht": { "vsp.vt": 87, "vsp.todo": 3, "...": "...", "paragraaf.§2.2.op_niveau": 22, "...": "..." },
  "bevestigd_in_excel": false,
  "toelichting": "De waarden in verwacht zijn afgelezen van het Dashboard-blad van het werkboek nadat dezelfde invoer daar is gedaan; datum en naam van wie afgelezen heeft staan hier zodra bevestigd_in_excel waar is."
}
```

Inhoud van het dossier (zo gekozen dat elke rekentak geraakt wordt):
- object "Gemaal Voorbeeld", functiebox uit classificatie met scores 3,4,2,5,1,3 (som 18, gemiddelde 3,
  box C, niveau 2), keten actief met één bestuurd object op B (niveau 3) → effectief niveau 3.
- controls: 3 op "Nee" (kies drie die een paragraaf aanroepen, verspreid over VSP en VSE), 2 op
  "N.v.t. (buiten scope)", 1 leeg, de rest "Ja"; statussen: 20 "Geïmplementeerd", 5 "In uitvoering",
  4 "Explain (afwijking)", 3 "N.v.t.", 6 "Nog te doen", rest leeg.
- maatregelen: op niveau 3 tien "Geïmplementeerd", drie "Explain (afwijking)", twee "N.v.t.", verspreid
  over minstens vier paragrafen; twee statussen op maatregelen die op niveau 3 niet gelden (die mogen
  nergens meetellen).
- bijlagen: CSR 15 en B op "Ja", "Geïmplementeerd".

Werkwijze om `verwacht` te vullen: de bouwer vult met openpyxl dezelfde waarden in een kopie van het
werkboek (alleen waarden, in de invoerkolommen), Bas of de auteur opent die kopie in Excel, leest het
Dashboard af en zet de getallen in `verwacht`; daarna `bevestigd_in_excel: true`. Tot dat moment vult
de bouwer `verwacht` met de uitkomst van `reken.py` en blijft `bevestigd_in_excel` onwaar; de tests
draaien dan wél, maar de Excel-vergelijking slaat over met die reden. Dit is de enige stap in dit plan
die een mens met Excel vereist.

## 12. Statuut, README, projectentabel, balie

- **README** (B11): kop blijft; "Status: prototype." blijft tot CI groen is en het instrument bij minstens
  één organisatie in gebruik is; dan wordt het in de projectentabel "in gebruik" en herhaalt de README
  dat (B12). "Snel starten" wordt: 1) open de keten online (link), 2) classificeer, 3) loop de controls
  langs, 4) sla je dossier op; "Liever Excel?" met de download van beide werkboeken. De cijfers
  (127, 268, 27) blijven. Een alinea "Waar de teksten vandaan komen" verwijst naar `csir.json` als bron
  en het werkboek als export.
- **Projectentabel** (`.github/profile/README.md`, B9): de rij `csir-control-register` krijgt in "Direct
  openen" `[Live tool](https://security-commons-nl.github.io/csir-control-register/)` in plaats van
  "Leesbare versie", en "Wat is het?" wordt: "De CSIR-keten in de browser: classificeer een object
  (functiebox, weerstandsniveau, ketenregel), bepaal welke van de 127 controls en 268 maatregelen gelden,
  en werk ze uit tot een dossier met bewijs en afwijkingen. Werkt offline; Excel-werkboek als download."
  De voorpagina volgt binnen een uur (cron in de site-build).
- **Aankondiging:** een Discussion in *Aankondigingen* zodra de keten live staat; met de hand, want de
  aankondig-workflow van de kennisbank is voor kennisbankitems en het token ontbreekt nog.
- **Balie (`X:\SECURITY-COMMONS-NL\CLAUDE.md`):** sectie "csir-control-register (prototype)" plus
  routing-triggers: CSIR, objectclassificatie, functiebox, weerstandsniveau, IA/PA/OT, tunnel, gemaal,
  brug, sluis, verkeersregelinstallatie, Cybersecurity Dossier → `csir-control-register/`.
- **Commits:** Nederlands, map-prefix (`register:`, `bron:`, `ci:`, `readme:`), geen AI-attributie,
  expliciet stagen, nooit `git add -A`. Het werkboek van Vasilis wordt in dit plan niet gewijzigd.

## 13. Bouwvolgorde (elke stap heeft een "klaar als")

1. **Bron.** `werkboek/objectclassificatie.xlsx` toevoegen; `register/haal_bron.py` schrijven;
   `csir.json` genereren. Klaar als `test_bron.py` groen is.
2. **Referentie.** `register/reken.py`. Klaar als `test_reken.py` groen is, met een voorlopige fixture
   (hoofdstuk 11, `bevestigd_in_excel: false`).
3. **Handreiking.** `paragrafen-barrieres.json` (letterlijk hoofdstuk 7), `haal_handelingsperspectief.py`,
   de kopie. Klaar als `--check` exit 0 geeft en elke barrière in het bestand in `paden.json` bestaat
   (voeg die controle toe aan `test_bron.py` als `test_barrieres_bestaan`: elke barrière in
   `paragrafen-barrieres.json` komt voor als `barriere` in `handelingsperspectief.json` of in de lijst
   `zonder_handleiding` daarvan; die export is de referentie, `paden.json` staat niet in deze repo).
4. **Sjabloon en bouw.** `bron/index.html`, lege `app.css`/`app.js` met alleen `console.log`,
   `bouw.py`. Klaar als `test_bouw.py` groen is op de nog lege app (de tests over eisen-in-de-pagina en
   handreiking slagen dan al, want dat is data).
5. **App: state en instellingen.** Dossier, localStorage, tabs, scherm Instellingen, `reken` in
   `app.js`. Klaar als `test_instellingen_functiebox_en_keten`, `test_lege_functiebox_waarschuwt`,
   `test_herladen_bewaart`, `test_wissen_leegt_de_opslag` groen zijn.
6. **App: classificatie.** Klaar als de twee classificatietests groen zijn.
7. **App: controls en maatregelen.** Tabellen, filters, scope, grijs. Klaar als
   `test_maatregelenfilter_volgt_het_niveau` en `test_control_op_nee_zet_paragraaf_buiten_scope` groen zijn.
8. **App: dashboard en bijlagen.** Klaar als `test_dashboard_gelijk_aan_referentie` groen is.
9. **App: opslaan, laden, uitdraai, print.** Klaar als de zes dossier- en uitdraaitests groen zijn.
10. **Handreiking in de pagina.** Klaar als `test_handreiking_zichtbaar_bij_paragraaf` groen is.
11. **Workflows.** `ci.yml`, `pages.yml`, `.gitignore`, `register/LEESMIJ.md`. Klaar als beide workflows
    groen zijn op GitHub en `/csir-control-register/` de keten toont met werkende links naar `uitleg/`
    en het werkboek.
12. **Excel-bevestiging.** Fixture-kopie van het werkboek vullen, laten aflezen, `verwacht` vullen,
    `bevestigd_in_excel: true`. Klaar als `test_browser_geeft_dezelfde_uitslag_als_excel` niet meer overslaat en groen is.
13. **README, projectentabel, aankondiging, balie.** Klaar als `repo-compliance.yml` groen is en de
    voorpagina "Live tool" toont.

Volledige testrun na elke stap: `python -m pytest register/tests/ -v`. Alles groen is de definitie van klaar.

## 14. Valkuilen (uit eerdere bouwrondes in deze commons)

- **Afronden.** Excel `ROUND(2,5;0)` is 3; Python `round(2.5)` is 2; JavaScript `Math.round(2.5)` is 3
  maar `Math.round(-2.5)` is -2. Gebruik overal `Math.floor(x + 0.5)` respectievelijk `math.floor(x + 0.5)`.
- **`</script>` in de data.** Eisteksten kunnen `<` bevatten. `json.dumps(...).replace("</", "<\\/")`
  zoals in `check/bouw.py`; vergeet dit niet, de pagina breekt anders stil.
- **Windows.** Schrijf bestanden binair of met `newline="\n"`; git zet CRLF om en de sha256 over bytes
  klopt dan op de ene machine wel en de andere niet. Hash daarom over de geparste inhoud (hoofdstuk 5),
  nooit over bytes. Geen paden als `/tmp` in scripts; gebruik `pathlib` relatief aan het script.
- **Inline styles.** De CSP verbiedt `style="..."`. Kleur en zichtbaarheid alleen via classes en het
  `hidden`-attribuut.
- **Excel-formulecellen.** VSE C5 en K5 zijn formules; lees met `data_only=True` en controleer op `None`.
- **De 95 controls zonder paragraaf.** Ze tellen mee in de dashboardrijen VSP/VSE, maar sturen geen scope.
  Dat is geen fout; het is hoe het werkboek werkt.
- **`§` in ids.** `data-teller="paragraaf.§2.1.1.pct"` bevat een `§` en punten; selecteer met
  `[data-teller="..."]` (attribuutselector met aanhalingstekens), nooit met `#` of `.`.
- **Grote tabellen.** 268 rijen met vijf invoervelden is 1.340 elementen; bouw de tabel één keer en werk
  per rij bij (`querySelector` op `data-maatregel`), niet de hele tabel opnieuw bij elke toetsaanslag.
- **Twee schrijvers in de werkmap.** Stage alleen wat je zelf hebt geraakt. Het werkboek van de auteur
  blijft van hem: als `haal_bron.py --check` faalt omdat hij het werkboek heeft bijgewerkt, genereer je
  `csir.json` opnieuw en commit je dat met de reden; je past het xlsx niet aan.

## 15. Buiten scope, ronde 2

- Excel-export van de invulling (SheetJS of een bouwstap buiten de browser).
- Meerdere objecten in één pagina, areaaloverzicht, dossierwisselaar.
- Koppeling per control aan de kennisbank via een ISO 27001:2013 → 27002:2022-crosswalk (dan kan de
  BIO-bronkolom rechtstreeks aan `aanvalspaden/mappingen/bio2.json` worden gehangen).
- Handleidingen voor §2.1, §2.4.2, §2.7.1 en §2.8 (fysiek, cryptografie, bewustwording, wijzigingsbeheer):
  schrijfopdrachten voor de kennisbank; ze staan als "gevraagd" in de pagina.
- Een AI-laag. Besloten van niet (hoofdstuk 0, punt 6).
- Het werkboek genereren uit `csir.json`. Alleen als de auteur daarom vraagt.

## 16. Open vragen aan de auteur (blokkeren de bouw niet)

1. **Gemiddelde of hoogste?** Het formulier neemt het afgeronde gemiddelde van de zes gevolgscores. Is dat
   de CSIR-regel of een lokale keuze? De tool volgt het formulier en toont de strengste lezing ernaast.
2. **Hoofdtaken.** De lijst is waterschapstaal; het plan voegt gemeentelijke objecttypen toe. Akkoord, en
   ontbreekt er iets?
3. **Excel-bevestiging van de fixture** (hoofdstuk 11): wie leest het Dashboard af?
4. **Publicatievorm van de eisteksten.** Als JSON in een HTML-pagina zijn ze machinaal leesbaarder dan in
   een xlsx-download. Zelfde publicatie, zelfde auteursrechtregel; bewust meenemen.
