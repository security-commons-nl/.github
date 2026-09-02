# security-commons-nl

> Open kennis en tooling voor digitale weerbaarheid, gemaakt door en voor publieke organisaties. Gratis,
> open source, van ons allemaal.

<!-- kant -->
### ➜ [security-commons-nl.github.io](https://security-commons-nl.github.io/)

Dat is de voorkant: alle kennis en tools op één pagina, direct te openen in je browser. Hier op GitHub
staat de broncode eronder, voor wie wil meelezen of meebouwen.
<!-- /kant -->

## Direct aan de slag

Voor CISO's, ISO's en bestuurders bij gemeenten, provincies, waterschappen en uitvoeringsorganisaties.
Alles hieronder werkt vandaag, in je browser, zonder account en zonder factuur. De kern is een keten
van vier vragen rond de achttien aanvalspaden van de publieke sector:

1. **Hoe sta ik ervoor?** De [zelfcheck](https://security-commons-nl.github.io/aanvalspaden/): een uur, alleen te doen, achttien paden en drie acties voor morgen.
2. **Hoe pak ik het aan?** Per barriere een [handleiding in de kennisbank](https://security-commons-nl.github.io/kennisbank/security/#handleidingen), met de alternatieven ernaast, en een uitnodiging waar er nog geen is.
3. **Wat toon ik hiermee aan?** De [normverankering](https://security-commons-nl.github.io/aanvalspaden/normen/): BIO 2.0, ISO 27001, NIST CSF 2.0, het Wpg-kader en de AVG, en waar de zelfcheck ophoudt.
4. **Wat zegt mijn eigen data?** De meting, in ontwikkeling in `security-posture-tool`.

Begin bij de [kennisbank](https://security-commons-nl.github.io/kennisbank/) als je iets zoekt om te lezen
of te hergebruiken, en bij de [weerbaarheidsgame](https://security-commons-nl.github.io/weerbaarheid-game/)
als je het gesprek met bestuurders voert.

## Alle projecten

| Project | Status | Wat is het? | Direct openen | Doelgroep |
|---|---|---|---|---|
| [kennisbank](https://github.com/security-commons-nl/kennisbank) | in gebruik | Werkende kennis uit de publieke sector, security, privacy, continuïteit en alles wat er tussen zit | [Leesbare versie](https://security-commons-nl.github.io/kennisbank/) | Security-, privacy- en continuïteitsprofessionals |
| [aanvalspaden](https://github.com/security-commons-nl/aanvalspaden) | prototype | Eén instrument rond vier vragen: zelfcheck (een uur, welke aanvalspaden staan open), risicoanalyse (met de lijn, kroonjuwelen en bewijs, risicolijst met eigenaar) en meting; één bron voor de aanvalspaden van de publieke sector. Met de normverankering en de handleidingen per barriere erbij: welke maatregel uit BIO 2.0, ISO 27001 en het Wpg-toetsingskader wordt aantoonbaar met dat bewijs, en waar de zelfcheck ophoudt | [Live tool](https://security-commons-nl.github.io/aanvalspaden/) | CISO's en ISO's bij publieke organisaties |
| [weerbaarheid-game](https://github.com/security-commons-nl/weerbaarheid-game) | in gebruik | Interactief bestuursdashboard dat de digitale kwetsbaarheid van een organisatie zichtbaar maakt | [Live tool](https://security-commons-nl.github.io/weerbaarheid-game/) | College van B&W, directies, bestuurders |
| [anonimizer-local](https://github.com/security-commons-nl/anonimizer-local) | in gebruik | AI-tool om gevoelige gegevens uit documenten te verwijderen, CLI voor batchverwerking en hergebruik van memory | | CISO's, ISO's en andere power users die regelmatig documenten anonimiseren |
| [anonimizer-browser](https://github.com/security-commons-nl/anonimizer-browser) | in gebruik | Browser-versie van de anonimizer: geen installatie nodig, alles draait in je eigen browser | [Live tool](https://security-commons-nl.github.io/anonimizer-browser/) | Beleidsmedewerkers, juristen en iedereen die ad-hoc één document wil anonimiseren |
| [security-posture-tool](https://github.com/security-commons-nl/security-posture-tool) | prototype | Evidence-based security posture langs Defense-in-Depth, diepte 2 (meting) van de aanvalspaden-keten | | Blue teams en interventieteams |
| [ai-gebruik-in-beeld](https://github.com/security-commons-nl/ai-gebruik-in-beeld) | in gebruik | Draaiboek om AI-gebruik in de organisatie feitelijk te meten (CISO + FG): meetregimes, bronnen met bewijslast, run-log, plus 15 KQL-query's | [Leesbare versie](https://security-commons-nl.github.io/ai-gebruik-in-beeld/) | CISO's, FG's en securityteams bij publieke organisaties |
| [cisochat](https://github.com/security-commons-nl/cisochat) | concept | vCISO-dirigent: een AI die redeneert als een CISO (langs NIST CSF), adviseert en open-source security-tooling orkestreert, inclusief beleidsondersteuning, mens beslist | | Security-professionals in de publieke sector |
| [policy-as-code](https://github.com/security-commons-nl/policy-as-code) | concept | Beleid en normen (BIO 2.0, ISO 27001, AVG) als uitvoerbare, toetsbare regels in plaats van alleen tekst, automatisch controleren of de praktijk aan de norm voldoet | | CISO's, ISO's en platformteams bij publieke organisaties |
| [applicatiecheck](https://github.com/security-commons-nl/applicatiecheck) | concept | Toont uit de applicatie zelf aan wat de BIO2 van een kritische applicatie vraagt: configuratie-export en logsample deterministisch getoetst, AI alleen voor het lezen van bewijs, mens beslist. Eerste toepassing: een zaaksysteem | [Ontwerp](https://security-commons-nl.github.io/applicatiecheck/) | ISO's en CISO's bij publieke organisaties die een kritische applicatie toetsen |
| [procescheck](https://github.com/security-commons-nl/procescheck) | prototype | BIA en BIV-classificatie per bedrijfsproces, met RTO en RPO, de businesscontext en de blast radius: wat valt om als een component uitvalt | [Live tool](https://security-commons-nl.github.io/procescheck/) | CISO's, informatiebeveiligers en proceseigenaren |
| [publicatiescan](https://github.com/security-commons-nl/publicatiescan) | in gebruik | Scant je eigen openbare publicaties (bekendmakingen inclusief bijlagen, raadsinformatie, terinzageleggingen, website) op onbedoeld gepubliceerde persoonsgegevens. Deterministische detectie via elfproef en mod-97; OCR optioneel en on-prem | | CISO's, ISO's, privacy officers en griffiemedewerkers bij publieke organisaties |
| [iamscan](https://github.com/security-commons-nl/iamscan) | prototype | Read-only analyse van je Linux-servers: wie kan waar root worden, uit passwd, sudoers en SSH-sleutels. Deterministisch, elke bevinding met de configregel erbij | | CISO's, ISO's, beheer- en auditteams bij publieke organisaties |
| [csir-assessment-tool](https://github.com/security-commons-nl/csir-assessment-tool) | prototype | De CSIR (Cybersecurity Implementatierichtlijn Objecten) toegepast op één object met industriële automatisering, in drie stappen: classificeer het object langs zes gevolgcriteria, bepaal welke van de 127 controls en 268 maatregelen op dat weerstandsniveau gelden, en werk ze uit tot een dossier met bewijs en onderbouwde afwijkingen. Eisteksten woordelijk uit de richtlijn, dus bruikbaar als eisenbron bij aanbesteding en contract. Rekent in je eigen browser; het Excel-werkboek staat als download ernaast | [Live tool](https://security-commons-nl.github.io/csir-assessment-tool/) | CISO's, ISO's, objectbeheerders en projectleiders bij publieke organisaties die tunnels, gemalen, bruggen of sluizen beheren |
| [normen](https://github.com/security-commons-nl/normen) | in gebruik | De normbronnen als dataset: BIO 2.0 (148 overheidsmaatregelen: nummer, titel, thema), NIST CSF 2.0, het Wpg-toetsingskader en de AVG, elk als één JSON in één schema met herkomst en vingerafdruk. Zonder normtekst van ISO of CIP: het nummer is van iedereen, de tekst niet. De aanvalspaden en applicatiecheck lezen hieruit; wie een norm in een tool wil laden, hoeft hem niet meer uit een PDF te halen | [Leesbare versie](https://security-commons-nl.github.io/normen/) | Bouwers van instrumenten, en CISO's, ISO's en privacy officers die een norm willen doorzoeken of hergebruiken |

**Gearchiveerd:** [blast-radius](https://github.com/security-commons-nl/blast-radius)
(wat valt om als een component uitvalt; opgegaan in procescheck op 03-09-2026, waar dezelfde
analyse op de processen zit die je daar al hebt staan),
[hosting-bouwblokken](https://github.com/security-commons-nl/hosting-bouwblokken)
(referentiearchitecturen en IaC om applicaties te hosten; de commons host niets meer, besluit 02-09-2026),
[grc-platform](https://github.com/security-commons-nl/grc-platform) (ISMS/PIMS/BCMS-applicatie;
de commons levert sinds 02-09-2026 alleen instrumenten en scripts, zie het besluitenlog) en
[anonimizer-web](https://github.com/security-commons-nl/anonimizer-web) (Flask-UI, vervangen door
anonimizer-browser) en [beleid-assistent](https://github.com/security-commons-nl/beleid-assistent) (opgegaan in cisochat als
capability beleidsondersteuning) en [security-shop](https://github.com/security-commons-nl/security-shop) (catalogus van patronen, opgegaan in de kennisbank als handleidingen per barriere). **Onderliggende infrastructuur:** [anonimizer-proxy](https://github.com/security-commons-nl/anonimizer-proxy)
(Cloudflare Worker die de Mistral-API forwardt voor anonimizer-browser, zodat een gebruiker geen eigen API-sleutel nodig heeft) en
[security-commons-nl.github.io](https://github.com/security-commons-nl/security-commons-nl.github.io)
(de site-build en de voorpagina) en [.github](https://github.com/security-commons-nl/.github)
(het redactiestatuut, de principes, de architectuur en deze projectentabel).

De statuslabels volgen de criteria in het [redactiestatuut](https://github.com/security-commons-nl/.github/blob/main/REDACTIESTATUUT.md)
(B8): *in gebruik* draait echt en heeft groene tests of CI · *prototype* werkt, zonder belofte · *concept* is ontwerp
of plan zonder werkende code · *gearchiveerd* wordt niet meer onderhouden.

**Tooling van anderen.** Open tools en kennisbanken van buiten de commons die we bruikbaar vinden, met per bron wat het is, wanneer je het inzet en welke wegingen erbij horen: [Externe referenties: security-tooling en kennisbanken](https://security-commons-nl.github.io/kennisbank/security/referenties-tooling/) in de kennisbank.

## Waarom dit bestaat

Publieke organisaties werken voor informatiebeveiliging, privacy en continuiteit intensief samen met
marktpartijen. Dat is waardevol, maar wie de inrichting van zijn governance aan de markt overlaat, geeft de
regie uit handen. Daarom bouwen we samen: een organisatie die het wiel opnieuw uitvindt is kwetsbaar, tien
die kennis en tooling delen vormen een beweging. Publiek geld betekent publieke code. AI is een middel,
nooit een doel, en altijd controleerbaar. De volledige principes staan in
[PRINCIPLES.md](https://github.com/security-commons-nl/.github/blob/main/PRINCIPLES.md).

## Halen en brengen

Niet alles staat hier omdat wij het weten. Sommige dingen zoeken we nog, en die staan er ook.

**Loop je ergens tegenaan?** Leg je vraag neer in
[Discussions](https://github.com/security-commons-nl/.github/discussions), categorie *Hulpvraag uit de
praktijk*. Geen theoretische vraag maar een echte: wat heb je geprobeerd, waar loop je vast, en wat zoek
je precies. Een voorbeeld dat werkt is meer waard dan tien pagina's beleid.

**Je hoeft daar je naam niet bij te zetten.** Een schuilnaam is prima en je hoeft niet te zeggen voor
welke organisatie je werkt. Dat is geen uitzondering maar de regel: een hulpvraag in dit vak is ook een
uitspraak over wat je zelf nog niet op orde hebt, en die drempel hoort niet bij jou te liggen (statuut
A11).

**Heb je iets dat werkt?** Deel het, ook als het half af is of alleen een werkafspraak op een A4.
Anonimiseren doen we samen, daar hebben we gereedschap voor. Zie
[CONTRIBUTING.md](https://github.com/security-commons-nl/.github/blob/main/CONTRIBUTING.md) voor hoe dat
gaat, ook zonder GitHub-account of Git-ervaring.

En verder: dit is geen verkooppraatje, er is niets te kopen. Begin met kijken, draai het lokaal, geef
feedback of bouw mee.

In voorbereiding, als richting en niet als toezegging: websitecompliance, digitale soevereiniteit,
code-repoveiligheid en aanvalsoppervlak (OSINT). Een tool verschijnt hierboven in de lijst zodra hij
werkt; tot die tijd bestaat hij niet.

## Onderliggende infrastructuur

Eén repo bevat geen op zichzelf staand product, maar maakt een ander wel mogelijk:

- [anonimizer-proxy](https://github.com/security-commons-nl/anonimizer-proxy), minimale Cloudflare Worker die de Mistral-API forward't, zodat anonimizer-browser werkt zonder dat eindgebruikers een eigen Mistral-account hoeven aan te maken. Forward-only, geen opslag, geen logging van inhoud. Zie de [DPA-template](DPA-template.md) voor de verwerkersrol.

## Over dit platform

Hoe het geheel in elkaar zit, welke repositories er zijn en hoe ze samenhangen, staat in
[ARCHITECTUUR.md](https://github.com/security-commons-nl/.github/blob/main/ARCHITECTUUR.md).

Deze community staat momenteel op GitHub. Op termijn zullen we overstappen naar een EU-gebaseerd alternatief (zoals [Codeberg](https://codeberg.org)), in lijn met onze principes van digitale soevereiniteit.

---

*Een initiatief van de publieke sector, voor de publieke sector.*
