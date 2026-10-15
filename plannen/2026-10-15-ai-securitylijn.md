# Plan: AI-securitylijn, vier sporen na het VNG-webinar

**Doel:** de kennisbank een samenhangende lijn geven over de beveiliging van AI, met vier sporen: verwijzen
naar wat VNG, IBD, TNO en CPB al hebben; nieuwe stukken schrijven waar niemand ze heeft; de instrumenten
van Amsterdam en Utrecht als gedeeld materiaal binnenhalen; en het lege kwadrant vullen, verdediging mét
AI, met agent-patronen, use-cases en een keuzeblad voor inzet.

**Aanleiding:** het VNG-webinar "AI & digitale veiligheid: de beveiliging van AI" van 15 oktober 2026, met
Frans de Waal en Daan Boerlage (Amsterdam, Utrecht, VNG). Het webinar sloot af met: "We willen
gezamenlijke instrumenten ontwikkelen om risico-afwegingen uit te voeren en juiste maatregelen te
identificeren." Uit de chat kwamen 35 vragen en bijdragen van deelnemers, waaronder de vraag om een
kennisplatform, de vraag of tools gedeeld kunnen worden en de vraag om gezamenlijk generieke use-cases te
classificeren. Dat is wat de commons is. De roadmap van de kennisbank noemt als grootste open punt "meer
dan één herkomst"; dit plan brengt twee gemeenten en VNG als partner in beeld.

**Besluiten bij het sparren (Bas, 15-10-2026):** vier sporen, spoor 4 (verdediging met AI) erbij op
verzoek; agent-patronen en inzetkeuzes worden geschreven vanuit de CISO-praktijk, het webinar en openbare
bronnen; de bestaande AI-stukken (agent-bevoegdheid, open-source AI onder de Cbw, AI-incident melden,
aanbieder-toets, AI-gebruik in beeld) blijven de kern en krijgen verwijzingen, geen herschrijving. Bas
heeft zich bij VNG aangemeld om mee te denken (AIenAlgoritmen@VNG.NL) en doet dat tot zijn vertrek bij
Leiden op 1 december 2026 (naar het NCSC); wat vóór die datum moet landen staat bovenaan.

**Stand:** issue [kennisbank#83](https://github.com/security-commons-nl/kennisbank/issues/83), met de fasen als afvinklijst.

**Wat niet mee gaat:** materiaal van de deelnemende gemeenten zonder hun akkoord; gemeentespecifieke
configuraties; commerciële frameworks of productnamen als norm (open-source tooling mag bij naam, besluit
14-10-2026); alles wat het VNG AI Governancekader of de IBD al heeft, dat wordt verwezen, niet
gedupliceerd (B15, plan bronnen van 25-09-2026).

---

## 1. Wat er is en wat het webinar erbij legt

De kennisbank heeft vijf AI-stukken, alle op status `concept`:

| Stuk | Dekt | Gat dat het webinar zichtbaar maakte |
|---|---|---|
| `security/agent-bevoegdheid` | Gedelegeerde taakbevoegdheid, zes velden, audit | Koppeling aan de lagenstapel (data, model, orchestratie en agent, applicatie, business) ontbreekt |
| `security/open-source-ai-binnenhalen` | Zelf gebouwde keten onder de Cbw, zes maatregelen | Ingekochte AI (SaaS, Copilot) valt erbuiten; de gele vraag "welke specifieke maatregelen voor AI" is voor die groep onbeantwoord |
| `security/ai-incident-melden` | Drie meldplichten, vijf scenario's | Geen |
| `governance/aanbieder-onder-de-ai-act` | Aanbieder of deployer, hoog risico, klikbare toets | De kwaliteitstraat van Amsterdam en Utrecht zet "AI-aanbieder" alleen bij de inkoopstap; wie zelf samenstelt is ook aanbieder, dat verdient een verwijzing over en weer |
| `ai-gebruik-in-beeld` (eigen repo) | Feitelijk gebruik meten uit telemetrie | Geen; het is het antwoord op tip 1 van de sprekers ("zorg dat je inzicht krijgt in waar AI is en komt") |

Daarnaast raakt `security/security-annex-leveranciers` artikel 19 (AI): meldplicht vooraf, geen training op
gemeentedata zonder toestemming, inzicht op verzoek, 90 dagen aankondiging bij wijziging. Wat erin
ontbreekt, en in de chat gevraagd werd: een verbod op inzet van AI in de dienstverlening zónder expliciete
toestemming van de gemeente.

Wat de sprekers lieten zien en wat de commons niet heeft:

- Het **vierluik** van AIVD en TNO: aanval op GenAI, aanval met GenAI, verdediging van GenAI, verdediging
  met GenAI. De commons-stukken zitten alle in "verdediging van". "Verdediging met" is leeg.
- De **lagenstapel**: platform en infrastructuur, data, modellen, orchestratie en agent, applicatie,
  business en dienstverlening, met quality assurance over alle lagen.
- Het **stoplichtenkader**: per project elf toetsen (AI-risicoanalyse, business case, privacy risk
  assessment, DPIA, IAMA, ethisch assessment, AI-inkoopvoorwaarden en non-functionals, architectuur,
  informatiebeheer, bias- en profileringstoets, OR) met een status per kolom; advies aan de proceseigenaar.
- De **aansluitvoorwaarden algoritmen en AI**: per GIBIT-artikel een risico (betrouwbaarheid,
  beschikbaarheid, kwaliteit, performance; transparantie, uitlegbaarheid; datalekken, manipulatie;
  aansprakelijkheid, copyright; rechtvaardigheid, discriminatie; veiligheid), de eisen en een categorie
  hoog, beperkt of laag. Staat op het VNG AI Governancekader.
- De **proefopstelling**: een open-source agent, getraind op risico's en mitigerende maatregelen, scant de
  code van een leverancier, rapporteert, adviseert correcte code; mens aan het begin en aan het eind.
- Het **functioneringsgesprek AI** en red teaming met het TNO-instrument *Prompt for Vulnerabilities in
  LLM-based Applications with Extensions*; de TNO AI Security Hazard Advisor (TAISHA) als to-do.

## 2. Spoor 1: verwijzen, niet dupliceren

Bronnen die bij de bestaande stukken komen, in het bronnenregister (B15) en als regel onder het stuk:

| Bron | Bij welk stuk | Herkomst |
|---|---|---|
| VNG AI Governancekader, kenniskaart Inkoopvoorwaarden (aanvullende voorwaarden Utrecht en Amsterdam) | security-annex art. 19; aanbieder-toets | chat, Paul de Haan |
| VNG AI Governancekader, kenniskaart Instrumenten en kaders voor implementatie, monitoring en beheer van AI en algoritmen (`aigovernance.vng.nl/knowledge_card/Instrumenten-en-kaders-voor-monitoring-en-beheer-van-AI-en-algoritmen`) | nieuw stuk rode vlaggen (spoor 2); ai-gebruik-in-beeld | chat, Ruben van Riel |
| IBD, vier kennisproducten AI en algoritmen (werkgroep met gemeenten) | alle AI-stukken, als eerste verwijzing | chat, Jerôme Schepers |
| CPB, "Scoren zonder doel te treffen? Een handreiking voor het meten van de effectiviteit van algoritmische processen" | ai-gebruik-in-beeld (de stap na "wat draait er": "werkt het") | chat, Mathijs Groen |
| Handreiking bij een onaangekondigde AI-component in lopende softwarecontracten, open.overheid.nl (`eae6482f-3fc4-42b4-acb3-7d60ce8fa336`) | security-annex art. 19 | chat |
| OWASP LLM Top 10 en OWASP Agentic Top 10; MITRE ATLAS; NIST AI RMF 1.0; ISO/IEC 42001; OECD AI Principles; International AI Safety Report 2025 en 2026 | nieuw stuk adversarial AI (spoor 2); frameworks-pagina | slides |
| NCSC, pagina Artificial Intelligence; Rijksoverheid, toezicht op Europese AI-regels | aanbieder-toets; ai-incident-melden | slides |
| TNO TAISHA; TNO Prompt for Vulnerabilities in LLM-based Applications with Extensions | nieuw stuk agent-patronen (spoor 4) | slides |

Elke verwijzing wordt vóór landing gecontroleerd op bereikbaarheid (curl 200) en op licentie; de
VNG-kenniskaart is gecheckt op 15-10-2026.

## 3. Spoor 2: nieuwe stukken

Geprioriteerd op wat in de chat gevraagd werd en nergens staat. Alle als `aanpak` in `security/`, status
`concept`, herkomst "CISO-praktijk bij gemeenten, naar aanleiding van het VNG-webinar van 15-10-2026".

| # | Stuk | Kern | Vraag uit de chat |
|---|---|---|---|
| 1 | **Copilot en vergelijkbare assistenten: de configuratiekeuzes** | Wat je zelf kunt zetten als de voorwaarden eenzijdig zijn: webzoeken aan of uit, gevoeligheidslabels en DLP, welke connectoren, welke tenant, welke logging; per keuze wat het afdekt en wat het kost. Meet eerst wat aanstaat (ai-gebruik-in-beeld). | "Staat de webzoekfunctionaliteit via Bing aan of uit, en hoe maken jullie die afweging?" |
| 2 | **Adversarial AI voor de gebruiksverantwoordelijke** | Inversie, data- en modelpoisoning, prompt-injectie: wat ze zijn, waar in de lagenstapel ze binnenkomen, wat je als deployer kunt doen en wat alleen de aanbieder kan. Gekoppeld aan OWASP LLM Top 10, OWASP Agentic Top 10 en MITRE ATLAS. | de gele slide-vraag "welke specifieke maatregelen voor AI" |
| 3 | **Rode vlaggen bij AI-monitoring** | Welke signalen je uit logging haalt: afwijkend volume, nieuwe connectoren, bevoegdheidsgebruik buiten de taak, uitvoer naar extern, modelwissel door de leverancier. Met de query-aanpak van ai-gebruik-in-beeld en centrale logverzameling. | "Monitoring op iets intelligents vraagt een intelligente monitoringstool. Welke rode vlaggen?" |
| 4 | **Generieke use-cases met classificatie** | Catalogus van gemeentelijke AI-use-cases uit het algoritmeregister (105 bij gemeenten, 102 in implementatie), per use-case de aanbieder-of-deployer-uitkomst, de risicoklasse en de toetsen die erbij horen. Werkplaats-lijst, gemeenten vullen aan. | "Waarom identificeren we niet gezamenlijk de generieke use-cases?" |
| 5 | **Annex-aanvulling artikel 19** | Eén nieuw lid: geen inzet van AI in de dienstverlening zonder voorafgaande expliciete toestemming van opdrachtgever; plus de verwijzing naar de handreiking van open.overheid.nl. Kleine wijziging, versie 1.4. | "Kun je in een contract opnemen dat AI-inzet zonder toestemming niet mag?" |
| 6 | **Cbw-maatregelen voor ingekochte AI** | Tegenhanger van open-source-ai-binnenhalen: de zorgplicht van artikel 21 vertaald naar SaaS en platformdiensten; wat je van de leverancier vraagt en wat je zelf bewijst. | de gele slide-vraag, voor de groep die niet zelf bouwt |
| 7 | **Baten en lasten per AI-toepassing** | Een eenvoudig blad: geclaimde tijdsbesparing tegenover de tijd die de borging kost (de stoplichten, het functioneringsgesprek, de monitoring), met de CPB-handreiking als meetkader. Geen model, een invulblad. | "Hoe voorkomen jullie meer tijd kwijt te zijn met borgen dan met inzetten?" |

Laag geprioriteerd, wel genoteerd: AI en OT (koppeling ISA95/IEC 62264, één chatvraag); FRIA (eerst
nagaan of de privacy-lijn het dekt); een bronnenpagina met de frameworks-balk van de sprekers.

## 4. Spoor 3: samenwerken met Amsterdam, Utrecht en VNG

Drie instrumenten van de sprekers die als gedeeld materiaal in de commons kunnen, mits zij dat willen:

1. **Het stoplichtenkader** als sjabloon (`governance`, type `sjabloon`): de elf kolommen, de status per
   kolom, het advies aan de proceseigenaar. De commons voegt toe wat er nu niet in zit: per kolom welk
   commons-stuk of welke kenniskaart je gebruikt.
2. **De aansluitvoorwaarden-tabel** (risico, eis, categorie per GIBIT-artikel). Het raamwerk staat op het
   Governancekader; de vraag is of de ingevulde eisen per risico openbaar zijn. Zo ja: verwijzen. Zo nee:
   de commons vult ze vanuit de eigen stukken en biedt dat terug aan.
3. **De toets-agent** uit de proefopstelling. De slide zegt "open source". Vraag: welk model, waar draait
   het, is de skill zelf open, en mag hij in de werkplaats van de commons. Dit is tegelijk het eerste
   patroon van spoor 4.

Route: de VNG-werkgroep (AIenAlgoritmen@VNG.NL). Bas brengt de commons daar in met de vraag: wat van jullie
mag open, en wat van ons helpt jullie. Instemming van de eigenaar vóór elke landing (vaste regel).

## 5. Spoor 4: verdediging mét AI

Het lege kwadrant. Drie stukken.

### 5.1 Agent-patronen voor beveiligingswerk (`security/agent-patronen-beveiliging`, aanpak)

Vijf patronen, elk met: wat de agent doet, wat de mens doet, waar de scheiding zit, in welke laag van de
stapel het draait, welke bevoegdheid het krijgt (verwijzing agent-bevoegdheid), en wat het bewijs is.

| Patroon | Wat de agent doet | Wat de mens doet | Bron |
|---|---|---|---|
| Toets-agent | Toetst code of configuratie van een leverancier aan de mitigerende maatregelen, rapporteert, stelt correctie voor | Stelt de eisen vast, bespreekt met de leverancier, beslist | proefopstelling Amsterdam/Utrecht |
| Risico-voorbereider | Stelt kandidaat-risico's voor uit standaardlijsten (OWASP, ATLAS, aansluitvoorwaarden) voor een beschreven toepassing | Weegt, schrapt, vult aan, besluit | chat: "kan risico-identificatie aan een agent?" |
| Voorschriften-navigator | Loopt stap voor stap de vragen van Cbw, AVG en AI Act langs en geeft per stap de bron | Beantwoordt, de uitkomst is een classificatie met onderbouwing | chat; bestaat deels als aanbieder-toets (beleid-assistent is gearchiveerd, idee leeft als issue .github#19) |
| Monitoring-agent | Leest logging, markeert rode vlaggen (stuk 3 van spoor 2), alleen leesrechten | Beoordeelt elke vlag, past de vlaggenlijst aan | chat: "intelligente monitoringstool" |
| Leveranciersantwoord-toetser | Legt antwoorden van een leverancier op de annex of de aansluitvoorwaarden naast de eis en markeert waar het antwoord de vraag ontwijkt | Voert het gesprek | leveranciersbeoordeling |

Vaste paragraaf per patroon: **wie keurt de agent**. Antwoord op "slager keurt eigen vlees": een ander
model of een andere leverancier dan wat getoetst wordt, alleen leesrechten waar dat kan, de mens beslist op
de uitkomst, en periodiek een steekproef met de hand. Analoog aan pentester en bouwer.

### 5.2 Use-cases en ideeën (werkplaats, geen af stuk)

Open lijst in de werkplaats, per regel: doel, laag in de stapel, welke data erin gaat, welk patroon, status
(idee, proef, in gebruik), herkomst. Start met de vijf patronen hierboven en met wat uit het webinar kwam.
Gemeenten voegen toe via het aanleverformulier. Dit is het antwoord op "kunnen tools gedeeld worden".

### 5.3 Keuzes bij inzet (`security/ai-inzet-keuzeblad`, aanpak met invulblad)

De vragen die je vóór elke agent beantwoordt, als keuzeblad dat je invult en bewaart:

1. Waar draait het: lokaal, eigen tenant, of cloud van een derde. Met de afweging van Jerôme Schepers: het
   risico van hoe je inzet tegenover het risico van achterlopen.
2. Open of gesloten model; bij open: versie-pinning en wachttijd (open-source-ai-binnenhalen).
3. Welke data erin gaat en wat er nooit in gaat. Infra-informatie in een cloud-agent is een
   aanvalsstrategie voor wie meeleest; dus geen productie-infra in prompts, anonimiseren (anonimizer).
4. Welke bevoegdheid: de zes velden van agent-bevoegdheid.
5. Wie keurt de agent, en hoe vaak opnieuw.
6. Wanneer stop je: de rode vlaggen waarbij de agent uit gaat.
7. Wat het kost tegenover wat het bespaart (spoor 2, stuk 7).

Uitkomst: een ingevuld blad per agent, net als bij de aanbieder-toets een besluit met onderbouwing.

## 6. Volgorde

Tijdshorizon: tot 1 december 2026, Bas' vertrek bij Leiden. Wat vóór die datum moet, staat bovenaan.

| Fase | Wat | Waarom eerst |
|---|---|---|
| 0 | Spoor 1 volledig: alle verwijzingen bij de bestaande stukken, bronnenregister gevuld, links gecheckt | Klein, meteen waarde, maakt de commons geloofwaardig richting VNG |
| 1 | Spoor 2 stuk 5 (annex 1.4) en stuk 1 (Copilot-keuzes) | Hardste chatvragen zonder antwoord; annex is een kleine wijziging |
| 2 | Spoor 4 compleet: agent-patronen, use-case-lijst, keuzeblad | Het lege kwadrant; de reden dat Bas meedenkt bij VNG |
| 3 | Spoor 3 via de VNG-werkgroep: stoplichtenkader, aansluitvoorwaarden, toets-agent | Afhankelijk van anderen, dus parallel starten, landing later |
| 4 | Spoor 2 stukken 2, 3, 4, 6, 7 | Groter schrijfwerk, kan ook na vertrek door anderen |

Elke fase sluit met een regel in `kennisbank/ROADMAP.md` en een issue met label `plan` in de kennisbank-repo.

## 7. Open vragen

- Reactie VNG op de aanmelding: pas daarna weet je of spoor 3 een werkgroep is of een mailwisseling.
- Status van de ingevulde aansluitvoorwaarden: openbaar of alleen het raamwerk.
- Dekt de privacy-lijn FRIA al, of hoort dat bij governance.
- Of de proefopstelling-skill echt open is en onder welke licentie.
