# Verkenning: de risicolaag tussen CSIR, procescheck en de aanvalspaden

**Doel:** uitzoeken of de ontbrekende risicolaag in de CSIR Assessment Tool een nieuw instrument vereist,
of een brug tussen drie dingen die er al staan.

**Aanleiding:** de CSIR Assessment Tool ging op 01-09-2026 live en loopt van classificatie tot en met de
lijst te implementeren maatregelen. Wat er niet in zit is de risicokant. Dat is een bewuste keuze van de
auteur; `csir-assessment-tool/CONTRIBUTING.md` zegt het zelf: *"Het register dekt bewust geen
risicoanalyse. Heb je een werkbare manier om die eraan te koppelen, dan is dat de meest waardevolle
bijdrage die er is."*

**Uitkomst van deze verkenning:** de brug hoeft niet bedacht te worden. De CSIR wijst hem zelf aan, en de
kennisbank heeft er al een methode voor liggen waarin alleen de CSIR nog ontbreekt. Wat wel bedacht moet
worden is een korrelverschil: de CSIR denkt in objecten, de rest van de commons in processen.

**Status:** verkenning, 02-09-2026. Geen bouwbesluit. Hoofdstuk 6 stelt een eerste stap voor die klein
genoeg is om te doen zonder dat de rest vaststaat.

---

## 1. De CSIR vraagt zelf om een risicoanalyse

Op twee plekken, en allebei zijn ze al in `csir.json` aanwezig.

**Bijlage C heet letterlijk "Best practice voor risico-inschatting bij CSIR-afwijkingen (explain)"**
(`csir.json`, `bijlagen`, id `C`, type *Best practice*, aangeroepen door 2 controls). Die twee zijn:

| Control | BIO-bron | Eis (verkort) |
|---|---|---|
| **VSP-7** | 5.1.1.1 | Comply or explain aanhouden; afwijkingen en uitgestelde implementaties vastleggen in het Cybersecurity Dossier als non compliancy |
| **VSP-8** | 5.1.1.1 | Die afwijkingen dienen **aan de hand van een risicoafweging** eventueel ook in de explain-administratie te worden overgenomen |

Dat is de naad. De tool legt de explain al vast (status `Explain (afwijking)` plus een onderbouwing in
vrije tekst), maar er zit geen methode onder die vrije tekst. De richtlijn zegt dat daar een risicoafweging
hoort, en levert er zelf een bijlage voor.

De tweede plek is harder. **VSP-59** (BIO 14.1.1.1) eist een risicoanalyse conform NEN-ISO/IEC 27005 of
gelijkwaardig vóór het ontwerpproces, en vervolgt: *"In de exploitatiefase dient de risicoanalyse ten
minste jaarlijks uitgevoerd en opgevolgd te worden met maatregelen."* Dat is een control die je vandaag in
de tool op *Geïmplementeerd* kunt zetten zonder dat er ergens een plek is om hem uit te voeren.

In totaal noemen 11 van de 127 controls en 13 van de 268 maatregelen het woord risico, verspreid over negen
van de vijftien paragrafen. Risicogestuurd werken is in de CSIR geen bijzaak: VSP-11 en VSP-12 eisen dat
leveranciers meewerken aan risicogestuurd (pen)testen en monitoren, en VSP-48 vraagt om risicogestuurde
monitoring door SIEM of SOC.

## 2. De methode ligt er al, de CSIR staat er alleen niet in

`kennisbank/security/risicoanalyse-aanvalspaden/` is expliciet geschreven als *"de leeswijzer over de
commons heen"*. De slottabel wijst per stap een project aan:

| Stap in de methode | Project dat hem invult |
|---|---|
| 1. Kroonjuwelen | procescheck (BIA/BIV), blast-radius |
| 2. Aanvalspaden | de zelfcheck, `meten-voordat-je-ingrijpt` voor pad 2 |
| 3. Dekking met bewijs | security-posture-tool, iamscan |
| 4. Risicolijst en gesprek | `security-annex-leveranciers`, `blue-team-opzetten` |
| 5. Vertaling naar de norm | de normverankering op `/aanvalspaden/normen/` |

De CSIR ontbreekt in die tabel. De som van de methode is:

> risico = aanvalspad (begaanbaar?) × kroonjuweel (wat raakt het?) × dekking (zien we het, reageren we,
> houden we het tegen?)

Die drie factoren bestaan alle drie al als data. Wat ontbreekt is de rij voor objecten.

## 3. Waar de sleutels zitten

| Vraag | CSIR Assessment Tool | procescheck | aanvalspaden |
|---|---|---|---|
| Wat is het waard? | 6 gevolgcriteria → functiebox → niveau 1-4 | `BiaAssessment` (B1-B8, I1-I7, V1-V7, elk met `_arg`), `Process.is_critical` + `critical_reason`, `RtoRpo` | kroonjuwelen (stap 1, maximaal tien) |
| Wat hangt eronder? | niets | `Process.applications` (m:n via `process_application`), `BusinessContext.chain_position`, `BiaAssessment.chain_dependencies` | blast-radius |
| Wat is de dreiging? | niets | niets | 18 bladeren, 5 clusters, 44 barrieres |
| Zien, reageren, voorkomen? | status per maatregel, door de invuller verklaard | niets | `drp` per chokepoint (57× P, 17× R, 2× D) en een `bewijs`-eis bij alle 76 chokepoints |
| Wat toon ik aan? | de BIO-bronkolom (ISO 27001:2013) | niets | `mappingen/` naar BIO 2.0, ISO 27002:2022, NIST CSF 2.0, Wpg en AVG |

De scherpste koppeling zit in het classificatiecriterium **`cascade`**: *"Aantal geraakte andere eigen
primaire processen en/of keten processen. Andere vitale sectoren die ook uitvallen."* De drempels lopen van
*"Geen cascade / domino effecten"* (1) via *"Volledige uitval van meerdere processen in de keten"* (4) naar
*"Gedeeltelijke of volledige uitval van één of meerdere vitale sectoren"* (5).

Dat scoort iemand vandaag op gevoel. Het is precies wat procescheck modelleert (`Process.applications`,
`BusinessContext.chain_position`) en wat blast-radius uitrekent. Hetzelfde geldt, zwakker, voor de criteria
`maatschappij` en `financieel` tegenover de BIA-scores. De CSIR heeft er zelfs een bijlage voor die om de
onderliggende registratie vraagt: **CSR 16, "Registratie assets in een configuratiemanagement-database
(CMDB)"**.

## 4. Het gat zit in alle drie, niet alleen ertussen

Dit is de vondst die de volgorde van het werk bepaalt.

- **In de kennisbank.** De twee barrieres die precies over risicogovernance gaan hebben geen handleiding.
  `owner` (*"Kent de verantwoordelijke risicohouder deze risico's?"*) en `treatment` (*"Zijn restrisico's
  expliciet geaccepteerd of voorzien van een actie?"*) staan allebei in `zonder_handleiding` van
  `handelingsperspectief.json`. De zelfcheck stelt de vraag dus wel en de kennisbank beantwoordt hem niet.
- **In procescheck.** De modellen zijn `Process`, `Application`, `BiaAssessment`, `RtoRpo`,
  `BusinessContext` en `AuditLog`. Er is geen risico-entiteit. Wel bestaat `BiaAssessment.
  owner_deviation_motivation`, wat aan de explain-kant van de CSIR verwant is.
- **In de CSIR-tool.** Zie hoofdstuk 1.

Wie de brug bouwt zonder eerst de twee handleidingen te schrijven, bouwt een koppeling naar een leeg vak.

## 5. De ontwerpvraag die alles bepaalt: object of proces

De CSIR-tool denkt in **objecten** (tunnel, gemaal, brug, sluis, verkeersinstallatie). procescheck en de
aanvalspaden denken in **processen** en in de organisatie als geheel. Een gemaal is geen proces, en
"uitkeringen betalen" is geen object. Die korrel moet overgestoken worden, en dat is het echte werk. De
dataformaten zijn het probleem niet.

Er is één natuurlijk scharnier. `Process.applications` in procescheck is een m:n-relatie, en een object met
industriële automatisering is in die termen een asset onder een of meer processen. Koppel je aan een object
zijn processen, dan rolt `cascade` eruit in plaats van dat je hem raadt, en krijgt de risicolijst per object
meteen een proceseigenaar. Dat is dezelfde beweging die `raakt-mij` (issue `.github#3`) maakt voor
kwetsbaarheidsmeldingen: vier assen, waarvan *Impact* uit proceskriticiteit komt.

Drie routes, met hun prijs:

| Route | Wat het is | Prijs |
|---|---|---|
| **A. Object als asset onder een proces** | Het object krijgt een verwijzing naar procesnamen; cascade en eigenaar volgen daaruit | Vereist dat de organisatie procescheck of een equivalente proceslijst heeft. Zonder dat is het veld leeg |
| **B. Object als eigen kroonjuweel** | Het object is zelf een rij in de matrix uit de methode, naast de tien processen | Geen afhankelijkheid, maar de cascade-vraag blijft handwerk en de eigenaar blijft impliciet |
| **C. Geen koppeling, alleen de explain verrijken** | Bijlage C invullen in de tool zelf, met de aanvalspaden als kolom | Kleinst, maar levert geen kroonjuwelenkoppeling op |

Route B en C sluiten elkaar niet uit; C is een deel van B.

## 6. Voorstel voor de eerste stap

Niet een vierde tool bouwen. **Bijlage C invullen in de tool die er al staat** (route C), en de twee
ontbrekende handleidingen schrijven.

Concreet: staat een maatregel of control op `Explain (afwijking)`, dan verschijnt een blok dat de vier
vragen stelt die de CSIR daar zelf stelt.

1. **Welk aanvalspad wordt hiermee begaanbaar?** Keuze uit de 18 bladeren van `paden.json`, of "geen".
2. **Wat raakt dat?** Vrij veld voor proces of dienst, met de objectnaam voorgevuld.
3. **Wie is de risicohouder?** Naam en rol. Niet de CISO; barriere `owner` zegt waarom.
4. **Tot wanneer geaccepteerd, of welke actie?** Datum plus besluit. Barriere `treatment`.

Die vier landen in de dossier-uitdraai onder het hoofdstuk Afwijkingen, dat er al is. Daarmee wordt VSP-7
en VSP-8 echt afgedekt in plaats van afgevinkt, en is bijlage C niet langer een bijlage waar niemand iets
mee doet.

Wat dit kost: `paden.json` erbij in `csir.json` (alleen id, titel en cluster van de 18 bladeren, ongeveer 2
kB), vier velden per afwijking in het dossierformaat, één blok in de pagina en een uitbreiding van het
uitdraaihoofdstuk. Geen nieuwe repo, geen server, en de offlinebelofte blijft staan.

Wat dit niet doet: de kroonjuwelenkoppeling. Die vraagt eerst een besluit over route A of B, en dat besluit
hoort bij de auteur van de tool en bij wie procescheck onderhoudt.

## 7. Volgorde

1. **De twee handleidingen schrijven** (`owner`, `treatment`) in de kennisbank. Zonder die twee koppelt
   stap 2 naar een leeg vak. Dit is bovendien werk dat op zichzelf waarde heeft: de zelfcheck stelt de
   vragen nu al aan iedereen die hem doet.
2. **Bijlage C invullen in de CSIR Assessment Tool** (hoofdstuk 6). Zelfstandig bruikbaar.
3. **Route A of B kiezen** voor de kroonjuwelenkoppeling, met de auteur en met procescheck erbij.
4. **De CSIR als rij toevoegen** aan de leeswijzertabel van `risicoanalyse-aanvalspaden`, zodra 2 en 3
   staan. Eerder heeft die rij niets om naar te wijzen.

## 8. Open vragen

- **Bij de auteur van de tool:** past bijlage C in de tool zelf, of hoort de risicoafweging buiten het
  register te blijven? Zijn CONTRIBUTING nodigt uit, maar noemt geen vorm.
- **Bij procescheck:** is een risico-entiteit daar gewenst, of hoort die in `grc-platform` (waar issue
  `grc-platform#16` een risicomatrix-grid voorstelt)? Twee risicoregisters in één commons is er een te veel.
- **Normkant:** de CSIR verwijst met zijn BIO-bronkolom naar de ISO 27001:2013-nummering, de
  normverankering gebruikt BIO 2.0 (ISO 27002:2022). Zolang die crosswalk ontbreekt, kan een koppeling
  alleen op paragraafniveau, zoals nu al gebeurt in `paragrafen-barrieres.json`.

## Bronnen

Alles hieronder is nagelezen op 02-09-2026, niet uit het hoofd overgenomen.

| Vindplaats | Wat er staat |
|---|---|
| `csir-assessment-tool/csir.json` | bijlage C, CSR 16, controls VSP-7, VSP-8, VSP-11, VSP-12, VSP-48, VSP-59; classificatiecriterium `cascade` met de vijf drempels |
| `csir-assessment-tool/CONTRIBUTING.md` | "Het register dekt bewust geen risicoanalyse" |
| `kennisbank/security/risicoanalyse-aanvalspaden/README.md` | de som, de vier stappen, D/R/P met bewijs, de leeswijzertabel |
| `aanvalspaden/paden.json` | 18 bladeren, 5 clusters, 44 barrieres, `drp` en `bewijs` per chokepoint, `randvoorwaarden` |
| `csir-assessment-tool/register/handelingsperspectief.json` | `zonder_handleiding` bevat `owner` en `treatment` |
| `procescheck/backend/app/models/` | `process.py`, `bia.py`, `rto_rpo.py`, `business_context.py`, `application.py`, `audit.py` |
| `.github` issues #3 (`raakt-mij`) en `grc-platform#16` | aangrenzende voorstellen voor weging en risicomatrix |
| `kennisbank/security/ketenafhankelijkheden/`, `kennisbank/bcm/kritieke-processen-vaststellen/` | bestaande kennis over de ketenkant en de kritieke processen |
