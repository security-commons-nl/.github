# Architectuur van Security Commons NL

Hoe het geheel in elkaar zit: welke repositories er zijn, hoe ze samenhangen, en waar het werk staat
dat nog gedaan moet worden. Bedoeld voor wie wil meebouwen en eerst wil begrijpen waar iets thuishoort.

Dit stuk beschrijft de structuur. Waarom we dit doen staat in [PRINCIPLES.md](PRINCIPLES.md), hoe we
schrijven in [REDACTIESTATUUT.md](REDACTIESTATUUT.md), en hoe je bijdraagt in
[CONTRIBUTING.md](CONTRIBUTING.md). De projectentabel op het
[organisatieprofiel](profile/README.md) is de enige projectenlijst; wijkt dit stuk daarvan af, dan
heeft het profiel gelijk.

**Peildatum: 30 augustus 2026.** De rationalisatie uit
[het plan](plannen/2026-08-30-rationalisatie.md) is begonnen: taak 0 tot en met 2 zijn af, en de
eerste cluster handleidingen staat.

---

## Het landschap

![Architectuur van Security Commons NL](architectuur-landschap.svg)

Tweeëntwintig repositories, waarvan drie gearchiveerd. Ze vallen uiteen in zes groepen, met daaronder
drie harde datakoppelingen die het geheel bij elkaar houden.

### De ruggengraat: de aanvalspaden-keten

`paden.json` is de enige bron voor achttien aanvalspaden, 76 chokepoints en de **44 barrieres** die
daaronder liggen. Alles wat de keten doet, hangt aan die 44.

| Schakel | Wat het beantwoordt | Waar |
|---|---|---|
| Zelfcheck | Hoe sta ik ervoor? | `aanvalspaden/check/` |
| Risicoanalyse | Wat betekent dat voor mijn kroonjuwelen? | `kennisbank/security/risicoanalyse-aanvalspaden/` |
| Meting | Wat zegt mijn eigen data? | `security-posture-tool` |
| Normverankering | Wat toon ik hiermee aan? | `aanvalspaden/mappingen/` (30-08-2026) |
| Handelingsperspectief | Hoe doe ik het? | de **kennisbank** is de bron; `aanvalspaden` kopieert (30-08-2026) |

### De zes groepen

**Voorkant.** `security-commons-nl.github.io` is de etalage. De voorpagina, `llms.txt` en `sitemap.xml`
worden gegenereerd uit de projectentabel in `.github/profile/README.md`; die tabel is de enige
projectenlijst (statuut B9).

**Kennis.** `kennisbank`, zestien items over vier vakgebieden, waarvan zeven van het type
`handleiding`. Een handleiding draagt het veld `barrieres:` en is daarmee de bron van het
handelingsperspectief: `tools/build.py` exporteert `handelingsperspectief.json`, en `aanvalspaden`
kopieert dat. Zo staat een handleiding op een plek in plaats van twee. Stand: zes van de 44 barrieres
gedekt, 38 open.

**Keten.** `aanvalspaden` en `security-posture-tool`, hierboven beschreven.

**Instrumenten.** `grc-platform` (ISMS/PIMS/BCMS), `procescheck` (BIA en BIV), `security-shop` (patronen
per gap), `weerbaarheid-game` (het bestuurlijke gesprek), `cisochat` (vCISO-dirigent, en tevens houder
van de gedeelde BIO2-dataset), `policy-as-code` (beleid als uitvoerbare regels).

**Scanners.** Kleine CLI's die een concrete vraag beantwoorden uit data die je al hebt: `iamscan` (wie
kan root worden), `blast-radius` (wat valt om), `publicatiescan` (persoonsgegevens in eigen
publicaties), `ai-gebruik-in-beeld` (draaiboek om AI-gebruik te meten).

**Anonimiseren.** `anonimizer-local` (CLI), `anonimizer-browser` (in de browser) en `anonimizer-proxy`
(de Worker eronder). Dit is de sluis waarlangs materiaal de kennisbank in komt.

**Governance en infra.** `.github` draagt het redactiestatuut, de principes en de projectentabel.
`hosting-bouwblokken` levert referentiearchitecturen voor wie dit spul zelf wil draaien.

### De drie harde koppelingen

Dit zijn de plekken waar twee repo's echt op elkaar leunen. Alle drie zijn ze bewaakt, want een kopie
zonder bewaking wordt binnen een half jaar een tweede waarheid.

1. `aanvalspaden/paden.json` → `security-posture-tool`, als kopie met een `paden.sha256` die bewaakt dat
   hij niet achterloopt.
2. `cisochat/data/bio2.json` → `aanvalspaden/mappingen/bronnen/bio2.json`, gegenereerd, met de
   commit-hash van de bron erin.
3. `.github/profile/README.md` → de voorpagina, `llms.txt`, `sitemap.xml` en de root-`CLAUDE.md`,
   gegenereerd bij elke build.

---

---

## De barriere als scharnier

![De barriere als scharnier](architectuur-scharnier.svg)

De achttien aanvalspaden delen **44 unieke barrieres**, en die zijn de spil van de hele keten. Aan
diezelfde sleutel hangen vier vragen:

| Vraag | Waar het antwoord staat | Stand |
|---|---|---|
| Hoe sta ik ervoor? | `aanvalspaden/check/` | live |
| Wat zegt mijn eigen data? | `security-posture-tool` | prototype |
| Wat toon ik hiermee aan? | `aanvalspaden/mappingen/` | live, 333 regels over vier kaders |
| Hoe pak ik het aan? | `kennisbank`, items van type `handleiding` | live, 6 van de 44 barrieres |

Omdat elke laag dezelfde sleutel gebruikt, kost een nieuwe laag geen nieuw datamodel. De zelfcheck
geeft per aanbevolen actie een `vraag_id`; dat is exact de sleutel waar de normverankering en het
handelingsperspectief aan hangen. Koppelen is daarmee optellen, niet bouwen.

Een barriere kan **meerdere** handleidingen hebben, elk met een rol: een `fundering` en daarnaast
`alternatief` of `verdieping`. Voor 24/7 opvolging zijn dat er vijf: centrale logverzameling als
fundering, en vier manieren om de opvolging te organiseren. Zo krijgt de lezer een keuze in plaats van
een voorschrift.

Wat er per laag **niet** is, telt even zwaar als wat er wel is. De normverankering laat zien welke
maatregelen een dreigingsgerichte zelfcheck niet raakt; het handelingsperspectief laat zien voor welke
barrieres nog geen handleiding bestaat. Beide lijsten zijn afgeleid, dus ze lopen niet achter.


---

## Waar werk staat

Twee plekken, en het onderscheid is niet willekeurig.

| | Wat het is | Waar | Wie onderhoudt |
|---|---|---|---|
| **Sprong** | Iets dat er nog helemaal niet is: een nieuwe tool, een spelvorm, een aanpak | Issue met label `idee` | een mens bedenkt het |
| **Gat** | Iets dat ontbreekt in een structuur die er al staat | gegenereerd, op de site | een script rekent het uit |

Een sprong is niet af te leiden: geen script stelt ooit voor om een spelvorm te bouwen die deelnemers
hun eigen kroonjuwelen laat benoemen. Een gat wel: "er is geen handleiding voor barriere `segment`"
volgt rechtstreeks uit `paden.json` en de kennisbank.

Daarom is er geen projectbord meer. Een gat dat je met de hand op een bord zet, loopt achter zodra
iemand het dicht, en dan houd je twee waarheden bij. Wat een script kan zien, houdt een script bij.

---

## Onderhoud

Een architectuurplaat die niet meebeweegt is binnen een half jaar misleidend. Twee dingen houden dit
stuk eerlijk:

1. **De projectentabel is de bron.** Komt er een repo bij, dan gaat die eerst in
   `profile/README.md`. Dit stuk volgt.
2. **De peildatum staat bovenaan.** Klopt hij niet meer met wat het profiel zegt, dan is dit stuk aan
   herziening toe.

Verbeteringen zijn welkom via een issue of een pull request.
