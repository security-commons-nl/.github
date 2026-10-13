# Plan: de beleidsset op maat, van één herkomst naar profielgestuurd

Vastgesteld 12-10-2026. Werkt stap 8 van [de ingang en de vulling](2026-09-28-ingang-en-vulling.md) uit
(tweede herkomst). Waar een AI-agent het stuk afmaakt, is dat de agent van de gebruiker zelf, met zijn eigen
sleutel bij zijn eigen leverancier: het patroon van [AI-hulp met eigen sleutel](2026-09-03-ai-hulp.md). De
commons host geen agent (statuut B14); cisochat, waar de beleidsassistent eerder als ontwerp lag, is op
03-09-2026 gearchiveerd.

## Waarom

De kennisbank heeft sinds 12-10-2026 een
[beleidsset informatiebeveiliging](https://security-commons-nl.github.io/kennisbank/governance/beleidsset-informatiebeveiliging/),
geordend naar de 21 domeinen waarin het controleraamwerk de BIO 2.0-maatregelen verdeelt, met per domein een
toets op de 117 overheidsmaatregelen en voor de vijf lege domeinen een sjabloon. Het is de eerste complete set
in de commons. Het is ook precies het probleem uit de roadmap: alles komt uit één samenwerking van gemeenten,
en een set uit één organisatie is een archief, geen commons.

Een gemeente die de set gebruikt, krijgt per domein iets anders: een vastgesteld stuk onder BIO 1 met de
rollen van de herkomst erin, een concept dat al op BIO 2.0 staat, of een leeg sjabloon. Wat ontbreekt is de
stap van "hier is wat één gemeente heeft" naar "hier is wat bij jouw gemeente past". Een kleine gemeente met
alles uitbesteed heeft een ander back-upbeleid nodig dan een grote met een eigen datacenter, en een
AI-agent die het stuk afmaakt moet weten welke vragen hij daarvoor moet stellen.

## Het doel

Een gebruiker beantwoordt een handvol vragen en krijgt per domein het concept dat bij zijn organisatie past,
met aanwijzingen waarmee zijn eigen AI-agent het stuk gericht afmaakt. Daarvoor zijn drie dingen nodig: een
profielschema waarmee varianten vergelijkbaar zijn, meer dan één variant per domein, en per variant een blok
dat zegt wat er nog in te vullen is en welke vraag daarbij hoort.

**Twee ingangen, de vragen zijn een filter en geen poort.** De pagina van de beleidsset heeft een ingang
*bladeren*: per domein alle varianten en het sjabloon naast elkaar, elk met het profiel van de herkomst, de
status en de dekking, direct te lezen en als markdown te downloaden. De tweede ingang, *op maat*, stelt de
vragen en sorteert en filtert dezelfde lijst op wat bij de gebruiker past. Alles wat via de vragen te vinden
is, is ook zonder vragen te vinden. De meeste bezoekers zoeken één stuk; wie eerst vragen moet beantwoorden,
haakt af. En wie zijn eigen AI-agent gebruikt, heeft het formulier niet nodig: die leest het maatwerkblok.

De kennisbank levert de inhoud: het corpus met metadata, profiel en toets. Wie er een agent op zet, doet
dat zelf: zijn eigen AI-agent leest het maatwerkblok en `llms.txt`, of een instrument biedt een opt-in
AI-pagina volgens het patroon [AI-hulp met eigen sleutel](2026-09-03-ai-hulp.md), die een voorstel levert
en geen besluit. De domeinindeling is daarvoor één: de 21 domeinen van het controleraamwerk, ook in het
profielschema en in de varianten.

## Stappen

| Stap | Wat | Resultaat | Omvang | Stand |
|---|---|---|---|---|
| 1 | Toets op de 117 overheidsmaatregelen, sjablonen voor de vijf lege domeinen en een uitgewerkt voorbeeld (fysieke toegang met controleraamwerk) publiceren | De eerste variant staat, met de gaten zichtbaar | | uitgevoerd 12-10-2026 (kennisbank #60) |
| 2 | Profielschema: zestien vragen met vaste antwoordruimte (type, grootte, samenwerking, beheer, hosting, werkplek, OT, Wpg en meer) in `profiel.json`; per variant in `varianten.json` het profiel van de herkomst en de maatregelen die het stuk dekt | Varianten zijn vergelijkbaar en selecteerbaar | 1 sessie | uitgevoerd 12-10-2026 (kennisbank #64) |
| 3 | Per stuk een blok "maatwerk": invulvelden, keuzes per profielantwoord, vervolgvragen voor een AI-agent. Daarbij hoort wat de agent leest voordat hij het stuk opent: een regel per stuk in `kennisbank/llms.txt`, een `llms-full.txt`, en een blok "voor agents" in de root-`llms.txt` (issue [github.io#10](https://github.com/security-commons-nl/security-commons-nl.github.io/issues/10)) | Een agent kan het stuk vinden en gericht afmaken | 1 sessie | open |
| 4 | De eerste variant uniform maken naar het format van het beleid fysieke toegang: per ISO-control de eisen met maatregelnummer, bijlage normen, bijlage controls, rollen als invulveld; de vijf sjablonen gevuld met een voorgestelde regel per maatregel | Variant 1 compleet voor alle 21 domeinen | 2 tot 3 sessies | open |
| 5 | Bladeren en sorteren: `build.py` genereert per domein de lijst van varianten en het sjabloon met profiel, status en dekking (ingang *bladeren*); de vragen zijn een filter en sortering bovenop diezelfde lijst (ingang *op maat*), geen aparte inhoud | De gebruiker vindt elk stuk zonder vragen, en met vragen eerst wat bij hem past | 1 sessie | open |
| 6 | Aanleverformulier voor andere organisaties: dezelfde profielkenmerken, dezelfde toets; een script geeft per aangeleverd stuk een eerste oordeel per maatregel, een mens corrigeert | Volgende inzenders hoeven niets te verzinnen | 1 sessie | open |
| 7 | Uitvraag aan gemeenten en het corpus vullen | Meer dan één herkomst per domein | doorlopend | open |
| 8 | AI-hulp bij het afmaken volgens het patroon [AI-hulp met eigen sleutel](2026-09-03-ai-hulp.md): een opt-in pagina die met de sleutel van de gebruiker een gekozen variant en de antwoorden op de maatwerkvragen omzet naar een voorstel voor het eigen stuk, op de 21 domeinen; geen gehoste agent in de commons (B14) | Wie geen eigen agent heeft, krijgt dezelfde hulp, en de gebruiker beslist per regel | 1 sessie | open |

## Randvoorwaarden

- Elke variant is tegen dezelfde 117 overheidsmaatregelen gelegd, anders zegt de selectie niets over dekking.
  De toets uit stap 1 is daarom onderdeel van het aanleveren, niet iets wat de redactie achteraf doet.
- Van maatregelen waarvoor alleen ISO 27002 geldt, wordt de normtekst niet overgenomen; alleen nummer en titel.
- Herkomst als organisatietype, nooit als naam (statuut). Het profiel beschrijft de organisatie zonder haar te
  noemen.
- Stap 2 tot en met 4 kunnen door de redactie worden gedaan; stap 7 niet. De eerste inzender van buiten
  bepaalt of het formulier van stap 6 werkt.

## Wat dit niet is

Geen poort: niemand hoeft vragen te beantwoorden om een concept of sjabloon te zien. Geen generator die beleid schrijft: de set levert concepten en vragen, de organisatie schrijft en stelt vast.
Geen tweede indeling naast de BIO 2.0-domeinen. Geen vervanging van de IBD-templates; die blijven het
vertrekpunt voor wie van nul begint.
