# Security Commons NL: de architectuur, en waar de backlog hoort

**Aanleiding.** De zelfcheck geeft drie acties. Bij een enkele actie ligt er een handleiding in de
kennisbank (passkeys), bij de meeste niet. De vraag was: hoort bij elke verbeteractie niet gewoon een
stuk instructies, los van welke norm je ermee aantoont? Het antwoord is ja, en zodra je dat uittekent
blijkt het de ontbrekende derde laag onder een structuur die er al staat.

Dit stuk laat het landschap zien zoals het is, legt uit waarom er twee plekken voor werk zijn in plaats
van drie, en beschrijft de laag die op 30-08-2026 is gebouwd.

> **Stand 30-08-2026.** Het handelingsperspectief is gebouwd en staat live. Het GitHub Project
> *Ideeen & Backlog* is verwijderd; de drie items staan als issue met het label `idee`.

---

## 1. Het landschap

![Architectuur van Security Commons NL](../architectuur-landschap.svg)

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
| Handelingsperspectief | Hoe doe ik het? | `aanvalspaden/mappingen/handelingsperspectief.json` (30-08-2026) |

### De zes groepen

**Voorkant.** `security-commons-nl.github.io` is de etalage. De voorpagina, `llms.txt` en `sitemap.xml`
worden gegenereerd uit de projectentabel in `.github/profile/README.md`; die tabel is de enige
projectenlijst (statuut B9).

**Kennis.** `kennisbank`, negen items over vier vakgebieden. Hier wonen de handleidingen; vier ervan
dekken samen veertien barrieres, voor de andere dertig staat een schrijfopdracht open.

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

## 2. Twee plekken voor werk, niet drie

De vraag was waar de backlog hoort. Het antwoord bleek: op minder plekken dan er waren.

Er stond een GitHub Project *Ideeen & Backlog* met drie items en vijf kolommen, sinds 14 april niet
aangeraakt. Alle drie de items bestonden al als issue. Het board was dus een lege huls om drie issues
heen, en tegelijk een derde plek naast issues en wat een script kan uitrekenen. **Het is op 30-08-2026
verwijderd**; de drie ideeen staan als issue met het label `idee`, en nergens in de repo's werd naar
het project verwezen.

Wat overblijft is een scheidslijn die wel klopt:

| | Wat het is | Waar | Wie onderhoudt |
|---|---|---|---|
| **Sprong** | Iets dat er nog helemaal niet is: een game, een AI-luisteraar, een nieuwe tool | Issue met label `idee` | een mens bedenkt het |
| **Gat** | Iets dat ontbreekt in een structuur die er al staat | gegenereerd, op de site | een script rekent het uit |

Een sprong kun je nergens uit afleiden. Geen enkel script gaat ooit voorstellen dat je een animerende
haas bouwt die tijdens een risicosessie meeluistert. Een gat wel: "er is geen handleiding voor
`segment`" volgt rechtstreeks uit `paden.json` en de kennisbank. Zet je een gat toch met de hand op
een board, dan loopt het achter zodra iemand het dicht, en houd je twee waarheden bij.

**Dus: issues voor wat mensen bedenken, een gegenereerde pagina voor wat het systeem zelf ziet.**

Er is een ding dat een script niet kan, en dat hoort erbij: prioriteren tussen ongelijksoortige dingen.
"Doen we eerst de handelingsperspectief-laag of eerst diepte 1 van de zelfcheck" is een keuze, geen
berekening. Zonder board landt die keuze in een hoofd, en daar kan een medebijdrager niet bij. De
oplossing is een klein handmatig blokje bovenaan een verder gegenereerde pagina: *waar we nu aan
werken*, drie regels. Dat is het enige handwerk dat overblijft, en het is precies het stuk dat een mens
moet doen.

---

## 3. De handelingsperspectief-laag (gebouwd 30-08-2026)

### Wat het is

![De barriere als scharnier](../architectuur-scharnier.svg)

Een derde mapping naast de normverankering, met dezelfde spil en dezelfde discipline:

```
barriere  ->  norm            "wat toon je hiermee aan"      333 regels, 4 kaders
barriere  ->  handleiding     "hoe doe je het"               14 van 44, 11 opdrachten
```

`aanvalspaden/mappingen/handelingsperspectief.json`: per barriere een verwijzing naar een
kennisbank-item en de paragraaf daarbinnen, of een openstaande schrijfopdracht.

### Hoe het er nu voorstaat

| Item | Dekt barrieres |
|---|---|
| Passkeys invoeren | `pr`, `fallback` volledig; `legacy`, `key` gedeeltelijk |
| Meten voordat je ingrijpt | `execution` volledig; `browser`, `localadmin`, `mail`, `edr` gedeeltelijk |
| Security Annex voor leveranciers | `technicalvendor` volledig; `review`, `residual` gedeeltelijk |
| Een blue team opzetten | `idresponse`, `exploitresponse` gedeeltelijk |

**Veertien van de 44 barrieres**, waarvan vier volledig. Voor de andere dertig zegt de zelfcheck wel
wat je moet doen, maar nergens hoe.

### Wat de gebruiker ziet

Een vierde weergave op de crosswalk, *Hoe pak ik het aan*. Waar een handleiding ligt, staat de
verwijzing met paragraaf. Waar niets ligt, staat dit:

> **Te schrijven artikel: netwerksegmentatie**
> Beperk lateral movement met segmentatie en minimale rechten (`segment`)
> Hoe je zones bepaalt die aansluiten op je processen, hoe je regels afdwingt in plaats van
> documenteert, en welk bewijs een auditor wil zien.
> Weet jij hoe dit moet? **[Schrijf mee]**

Die knop opent een vooringevulde issue in de kennisbank, met de barrieres en het bewijs dat de
zelfcheck vraagt er al in. Een lege plek die zegt wat er zou moeten staan en waarom, met een knop
ernaast, is een uitnodiging. Een kennisbank die alleen toont wat er al ligt, is een etalage.

### De volgorde komt uit de data

De dertig gaten zijn gegroepeerd tot **elf schrijfopdrachten**, gesorteerd op gewicht: het aantal
aanvalspaden waarop een barriere staat.

| # | Artikel | Barrieres | Gewicht |
|---|---|---|---|
| 1 | opvolging en detectie | `soc`, `ddosresponse` | 19 |
| 2 | beheerrechten scheiden | `adminhard`, `jit`, `model`, `elevation`, `adminmonitor` | 7 |
| 3 | de buitenrand afschermen | `remote`, `origin`, `l7`, `upstream` | 7 |
| 4 | van scan naar gepatcht | `patch`, `vuln`, `assets` | 7 |
| 5 | herstellen als het misgaat | `backup`, `restore`, `crisis`, `critical` | 4 |
| 6 | ingangen naast de sterke inlog | `devicecode`, `consent`, `session`, `unmanaged` | 4 |
| 7 t/m 11 | risico beleggen, mail als kanaal, segmentatie, testen en hertesten, keten in beeld | zeven barrieres | 1 tot 2 |

Opvolging staat bovenaan omdat `soc` een randvoorwaarde is: die hangt aan geen enkel pad maar weegt
over alle achttien mee. Tellen op bladeren zou hem op nul zetten en naar de bodem laten zakken, terwijl
hij juist het breedst geldt.

Zodra er echte zelfcheck-uitslagen zijn, is het betere signaal hoe vaak een barriere als actie uit
`score.acties()` komt. Doen tien organisaties de check en komt `fallback` acht keer als eerste actie
bovendrijven, dan is dat het volgende artikel.

### De twee ontwerpvragen, beantwoord

**Per barriere of per artikel?** Allebei, op hun eigen plek. De **mapping** loopt per barriere, want dat
is precies en machinaal toetsbaar. De **backlog** groepeert ze tot een `cluster`, want zo ga je
schrijven: een artikel over werkplekhardening bedient er drie tegelijk. Dertig gaten worden zo elf
opdrachten.

**Hoe voorkom je dat het achterloopt?** Twee tests, op verschillende plekken omdat ze verschillende
dingen nodig hebben. `tests/test_handelingsperspectief.py` eist dat elke barriere een handleiding heeft,
gevraagd staat of met reden is vrijgesteld, en dat elke gevraagde barriere zegt wat het artikel zou
moeten dekken. `mappingen/tests/test_kennisbank_verwijzingen.py` controleert of het item, de paragraaf
en de leesversie echt bestaan; die heeft de kennisbank-repo nodig, en CI checkt hem daarvoor uit.

Dat komt naast `test_kennisbank_koppeling.py` en niet in plaats daarvan: die bewaakt of de inhoud van
AP09 niet uit elkaar loopt met de killchain-tabel in het kennisbank-item, en dat is een ander risico dan
een verwijzing die nergens op uitkomt.

---

## 4. Wat hierna kan: de staat van de commons

Het script dat de contentbacklog uitrekent, kan meer zien. Alles hieronder is afleidbaar en wordt nu
door niemand bijgehouden:

| Signaal | Waar het uit volgt |
|---|---|
| Barrieres zonder handleiding | `paden.json` tegen de kennisbank (nu 30) |
| Barrieres zonder normregel | `paden.json` tegen de mappingen (nu 0) |
| Kennisbank-items zonder leesversie | statuut B3, `tools/build.py` weet het al |
| Repo's die van het statuut afwijken | `repo_compliance.py`, draait al per repo |
| Kopieen die achterlopen | `paden.sha256` en de commit-hash in de BIO2-bron |
| Repo's zonder tests of zonder recente activiteit | de GitHub-API |

Bij elkaar is dat een pagina *de staat van de commons*: wat er te doen is, zonder dat iemand het
bijhoudt. Met bovenaan het handmatige blokje uit hoofdstuk 2, zodat ook zichtbaar is waar nu aan
gewerkt wordt.

Dat is een volgende stap, geen onderdeel van wat nu gebouwd is.

---
