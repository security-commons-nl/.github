# Bouwplan: `dpiacheck`, de invulhulp van het Rijk gevuld met gemeentelijke ervaring

**Doel:** één pagina die lokaal rekent en een privacy officer van pre-scan tot concept-DPIA brengt, met
wat er nu nergens is: bij elke soort verwerking de risico's en maatregelen die in uitgevoerde DPIA's
telkens terugkeren, als voorstel dat de gebruiker per regel bevestigt of verwerpt. Het formulier en de
rekenlogica zijn van het Rijk; de vulling, de catalogus en de hulp van AI zijn van de commons. Het
instrument levert nooit een afgeronde DPIA. Wat niet bevestigd is, verschijnt als open vraag.

**Aanleiding:** de privacy officer van een gemeentelijke organisatie heeft toestemming gegeven om haar
uitgevoerde DPIA's te anonimiseren en de opbrengst ervan in de commons aan te bieden. Het gaat om 114
verwerkingen over acht jaar, waaronder 27 over cameratoezicht. De waarde zit niet in die documenten
(een DPIA is contextgebonden en mag niet gekopieerd worden) maar in wat ze hebben opgeleverd: welke
risico's telkens bovendrijven en welke maatregelen telkens nodig blijken. Honderden gemeenten doen die
beoordeling nu elk apart voor dezelfde standaardprocessen.

**Koers (besloten 03-09-2026 na landschapsonderzoek, hoofdstuk 1):** leunen op het Rijk voor alles wat
het Rijk goed heeft, en zelf bouwen wat er niet is. Het Ministerie van Binnenlandse Zaken publiceert
onder EUPL-1.2 een invulhulp voor pre-scan, DPIA en IAMA (`MinBZK/par-dpia-form`), browser-only en zonder
account, met de vragenlijsten als YAML. Die vragenlijsten en die rekenlogica worden hier een bewaakte
kopie, zoals de commons dat met de BIO en de Wpg doet. Wat ontbreekt bij het Rijk is de inhoud: bij
*Maatregelen* staat een leeg tekstvak. Dat vak vult dit instrument. Het plan begon als een volledig
eigen instrument; die versie is na het onderzoek losgelaten (hoofdstuk 1, *Wat dit betekent*).

**Architectuur:** vierde instrument op de leest van `procescheck`, `csir-assessment-tool` en
`applicatiecheck`: bron als data, één HTML-bestand met CSP op de hashes, een Python-referentie naast de
JavaScript met dezelfde functienamen, een dossier als JSON bij de gebruiker, tests die de bron tegen het
origineel leggen. Met AI-hulp op eigen sleutel volgens het vaste patroon. Live op `/dpiacheck/`. Waar dit
plan "als bij procescheck" zegt, is [dat plan](2026-09-02-procescheck-instrument.md) de referentie; voor
de AI-laag [het AI-hulp-plan](2026-09-03-ai-hulp.md); voor de bewaakte kopie
[het normen-plan](2026-09-02-normen.md).

**Tech stack:** Python 3.12 (referentie, bouw, oogst, tests), vanilla JS en CSS, pytest, Playwright. Geen
dependencies in de pagina. De YAML van het Rijk wordt bij de bouw naar JSON omgezet; de pagina leest geen
YAML.

**Status:** vastgesteld 03-09-2026, geen open punten. Staat in de wachtrij achter *meting* en
*applicatiecheck F1* (volgorde uit het plan [lichte commons](2026-09-02-lichte-commons.md)). Fase O
bepaalt of de rest doorgaat.

---

## 0. Besluiten (de spec)

### Leunen op het Rijk

1. **Het formulier is van het Rijk.** `sources/prescan.yaml` (versie 2.0) en `sources/dpia.yaml`
   (versie 3.0, het Rijksmodel DPIA) uit `MinBZK/par-dpia-form` komen als **bewaakte kopie** in deze
   repo: `instrument/haal_rijk.py` haalt ze op van een vastgepinde commit, `--check` blokkeert in CI als
   de kopie afwijkt. Wijzigen gebeurt bij het Rijk, nooit hier. Wat het Rijk bijwerkt (de AP-lijst, de
   EDPB-criteria, het model), halen wij op. Dat is het antwoord op de vraag wie de vragenlijst in 2028
   actueel houdt.
2. **De rekenlogica is van het Rijk.** Het `assessments`-blok in `prescan.yaml` bepaalt of een DPIA
   verplicht (nieuwe wetgeving, risicoscore boven vier, minstens één AP-categorie, minstens twee
   EDPB-criteria) of aanbevolen is (precies één EDPB-criterium), en signaleert daarnaast DTIA, KIA en
   IAMA. Die expressies worden hier geëvalueerd, niet herschreven. Er is geen uitkomst *niet nodig*, ook
   niet bij het Rijk; het uitblijven van een treffer wordt zo genoemd.
3. **Standalone, zonder enige afhankelijkheid van het Rijk op het moment van gebruik.** De kopie zit in
   de repo, de bouw zet YAML om naar JSON, en de pagina laadt niets van buiten. Statuut B14. Verdwijnt de
   bron, dan werkt het instrument nog; alleen het bijwerken stopt, en dat is dan zichtbaar in de
   peildatum op de pagina.
4. **Het dossier is het bestandsformaat van het Rijk.** Hun tool exporteert en importeert JSON volgens
   `schemas/assessment-output.v2.schema.json`: een `metadata`-blok met de urn en versie van de
   vragenlijst, en `answers` gesleuteld op de task-id's (`0.1`, `2.1.3`, herhaalbare taken gegroepeerd
   met `_index`). Dit instrument schrijft en leest precies dat formaat, met de eigen laag in een apart
   blok ernaast (hoofdstuk 5). Een dossier uit `dpiacheck` opent dus in de rijkstool en andersom.
5. **Geen wijziging van hun vragen, wel een eigen laag eromheen.** Wat dit instrument toevoegt staat
   naast de vragen van het Rijk, nooit erin: familie, catalogus, voorstellen, tellers, AI-hulp. Een
   gebruiker kan de rijksvragen zonder onze laag doorlopen; de laag is aan te zetten en draagt zijn
   herkomst.
6. **Terugbijdragen als het werkt.** Zodra de catalogus voor cameratoezicht in het veld heeft gestaan,
   wordt hij aangeboden aan `MinBZK/par-dpia-form` als keuzelijst bij hun taak *Maatregelen*, via een pull
   request en volgens hun CONTRIBUTING. Principe 1: samenwerken is sterker dan inkopen. Neemt het Rijk
   het niet over, dan verandert er hier niets.

### De eigen laag

7. **Eén maatregelencatalogus, niet één lijst per familie.** De maatregelen staan als platte lijst met een
   eigen id-ruimte in `dpia.json`; families verwijzen ernaar. Een maatregel als *toegang is beperkt tot
   wie de gegevens voor zijn taak nodig heeft* geldt bij cameratoezicht en bij het sociaal domein, en
   staat dan één keer met beide families erbij. Zo werkt het controlregister van de CSIR-tool ook. Dit is
   de voorwaarde voor besluit 17: kiezen uit een gesloten catalogus is te controleren, vrij formuleren
   niet.
8. **De catalogus hangt aan de vragen van het Rijk.** Elke maatregel verwijst naar de task-id van het
   veld waar hij thuishoort (de taak *Maatregelen* in het hoofdstuk Maatregelen; risico's naar *Risico's
   voor de betrokkenen*). Zo verschijnt een voorstel op de plek waar de gebruiker het invult, en niet in
   een eigen scherm ernaast.
9. **Het instrument levert nooit een afgeronde DPIA.** Elke uitdraai draagt de status *concept* en bevat
   een lijst open vragen die even prominent staat als de ingevulde regels. Artikel 35 verlangt een eigen
   beoordeling; een document dat er af uitziet maakt van die beoordeling een afvinkoefening.
10. **De uitdraai draagt de last, niet een banner.** Geen waarschuwing boven elke stap. De kop zegt
    *concept*, de open vragen staan tussen de ingevulde regels, en elke voorgevulde regel toont waar hij
    vandaan komt. Daarnaast één verantwoordingspagina, zoals procescheck die heeft.
11. **Elke voorgevulde regel is een voorstel met herkomst.** Nooit "dit is de maatregel", altijd "bij
    *n* vergelijkbare verwerkingen is dit zo beoordeeld". Vier standen: `voorstel`, `bevestigd`,
    `verworpen`, `eigen`. Alleen `bevestigd` en `eigen` komen als tekst in de uitdraai; wat `voorstel`
    blijft, wordt een open vraag. Dit geldt voor een voorstel van de tool en van de AI gelijk.
12. **De maatregel gaat de bron in, het antwoord nooit.** In de brondocumenten staat per maatregel of de
    organisatie eraan voldoet, met toelichting. Die kolom is een kwetsbaarhedenlijst van een aanwijsbare
    organisatie en verlaat de tenant niet. Ook het restrisico en de acceptatie ervan blijven achter.
13. **Elke maatregel staat als norm in de tegenwoordige tijd, nooit als opdracht en nooit als los
    naamwoord.** De belangrijkste veiligheidsregel van dit plan, machinaal afgedwongen (hoofdstuk 9).
    Een maatregel in de gebiedende wijs verraadt een gebrek van de bronorganisatie zonder één naam te
    noemen: *"beëindig de directe internettoegang van de camera's"* zegt dat die camera's aan het
    internet hingen. De norm *"camera's hebben geen directe internettoegang"* schrijft hetzelfde voor en
    zegt niets over wie het nog niet op orde had. Bronnen wisselen tussen gebiedende wijs, naamwoordelijke
    opsommingen en normen; alles wordt naar het derde register genormaliseerd.
14. **Geen leveranciers, geen systemen, geen organisatie.** Die worden functieomschrijvingen: "de
    leverancier van het camerabeheer", "het zaaksysteem". Statuut A9 en A3.
15. **Herkomst is een getal, geen bewering.** Bij elke familie en elke maatregel staat hoeveel
    beoordelingen eronder liggen en uit hoeveel organisaties. De eerste vulling komt uit één regio; de
    teller zegt dat, zodat niemand het voor een landelijke standaard aanziet.

### AI-hulp

16. **AI-hulp volgens het vaste patroon.** Aparte pagina met eigen Content-Security-Policy, sleutel
    alleen in `sessionStorage`, toestemming per sessie, voorstel in plaats van schrijven, Mistral-medium
    standaard. Precies zoals in procescheck; waar dit plan zwijgt, geldt het AI-hulp-plan.
17. **De AI kiest uit de catalogus, verzint nooit een maatregel.** Een voorstel verwijst naar bestaande
    `maatregel`-id's; een id dat niet bestaat laat de citaatcontrole vallen; vrije tekst als maatregel
    wordt geweigerd. Zo blijft de vormregel van besluit 13 overeind voor alles wat de gebruiker ziet.
18. **De AI raakt de noodzaak en evenredigheid niet aan.** Maatregelen voorstellen en een familie
    herkennen is herkenwerk. De beoordeling van subsidiariteit en proportionaliteit is het juridische
    oordeel dat artikel 35 bij de verwerkingsverantwoordelijke legt. Daar is geen opdracht voor.
    Principe 4: AI is adviserend, nooit beslissend.

### Overig

19. **Eén instrument, gefaseerd gebouwd, live na de eerste vulling met label `concept`.** Pre-scan en
    catalogus gaan eerst live; de gevulde DPIA-stap volgt als die twee in het veld hebben gestaan.
20. **De eerste vulling is cameratoezicht.** 27 verwerkingen in de bron, de maatregelenoverlap is
    gemeten (hoofdstuk 1), en de bibliotheek van de Informatiebeveiligingsdienst heeft er geen enkele
    over. De overige families volgen als dit werkt.
21. **De Leidse set is de bron; de bibliotheek van de Informatiebeveiligingsdienst is een verwijzing.**
    Die bibliotheek staat onder een voorwaarde (overnemen mag, veranderen niet) die zich niet verdraagt
    met het normaliseren van maatregelen. Ze wordt in het instrument genoemd als plek voor voorbeelden,
    en er wordt niets uit overgenomen. Voor cameratoezicht is dat geen verlies (hoofdstuk 1).
22. **Afbakening met `applicatiecheck`: verwerking tegenover techniek.** `dpiacheck` stelt de eis,
    `applicatiecheck` levert het bewijs. Ze verwijzen naar elkaar en delen geen bron. Een applicatie
    *levert bewijs voor* een maatregel, nooit "voldoet aan" de DPIA.
23. **Eén oogstslag, twee producten.** Het oogsten levert `dpia.json` en het kennisbank-item op
    (hoofdstuk 7 en 8).
24. **De naam.** `dpiacheck`, in de familie van `procescheck` en `applicatiecheck`.

## 1. Wat er nu is

**In de commons:** niets. De sectie `privacy/` van de kennisbank is leeg. De kennisbank telt 52 items,
waarvan 48 in `security/`.

**Bij het Rijk** (bron geverifieerd 03-09-2026, YAML opgehaald en doorgelezen):

| | `prescan.yaml` 2.0 | `dpia.yaml` 3.0 |
|---|---|---|
| Vragen | 57 in 8 blokken | 210 in 21 hoofdstukken |
| Veldtypen | `open_text`, `select_option`, `checkbox_option`, `radio_option`, `task_group` | idem |
| Dekt | alle 17 AP-categorieën, de EDPB-lijst, bijzondere gegevens, omvang, doorgifte, basisregistraties, algoritmes, kinderrechten | het volledige Rijksmodel: beschrijving, doeleinden, partijen, locaties, kader, bewaartermijnen, rechtsgrond, doelbinding, noodzaak en evenredigheid, acht rechten van betrokkenen, risico's, maatregelen met restrisico en beheerder, FG-advies, ondertekening |
| Rekent | ja, `assessments`-blok met expressies (besluit 2) | nee, invullen |
| Rijksspecifiek | de naam en twee links naar het model | idem |
| Standalone | ja, `pnpm build:standalone` levert één HTML | idem |

Bij *Maatregelen* vraagt het Rijk: "beoordeel welke technische, organisatorische en juridische
maatregelen in redelijkheid kunnen worden getroffen". Een leeg vak. Dat is het gat.

**Bij de Informatiebeveiligingsdienst:** een bibliotheek met 26 geanonimiseerde uitgevoerde gemeentelijke
DPIA's, een handreiking met sjabloon, een lijst van 27 hoogrisicoprocessen en een tool achter een login.
De voorwaarde op de bibliotheek: overnemen mag, veranderen niet, herpubliceren is ongewenst. Van de 26
overlappen er ongeveer 12 met Leiden. Cameratoezicht in de publieke ruimte en in gebouwen: 0 daar, 27 in
Leiden. Openbare ruimte en sensoren: 0 daar, 16 in Leiden. Dienstverlening, KCC en AI: 0 daar, 10 in
Leiden.

**Bij de bronorganisatie**, geteld 03-09-2026: 114 mappen, 789 bestanden (370 Word, 215 pdf, 91 mail,
78 Excel). Zes camera-DPIA's vergeleken: de twee best gevulde delen 12 van 16 maatregelen; 2 van de 6
hebben een bruikbare maatregelentabel. De herhaalbaarheid is aantoonbaar, de bron is ongelijk van
kwaliteit. Oogsten is redactiewerk.

**Wat dit betekent.** De eerste versie van dit plan bouwde een volledig eigen instrument met eigen
plichttoets, eigen vragenlijst en eigen uitdraai. Dat rustte op de aanname dat zoiets niet bestond. Het
bestaat, open source en op dezelfde leest. Doorbouwen was duplicatie van het formulier; alleen een
kennisbankstuk maken liet de tijdwinst voor vakgenoten liggen. De koers werd daarom: het formulier en de
rekenlogica van het Rijk als bewaakte kopie, en zelf alleen bouwen wat ontbreekt. Dat is kleiner dan het
eerste plan, het houdt de vragenlijst actueel zonder eigen onderhoud, en het levert een instrument dat
het Rijk zou kunnen overnemen in plaats van ermee te concurreren.

## 2. Doelstructuur

```
dpiacheck/
├── dpia.json                 ← de eigen laag: families, risico's, maatregelencatalogus
├── rijk/
│   ├── prescan.yaml          ← bewaakte kopie, vastgepinde commit
│   ├── dpia.yaml             ← idem
│   └── BRON.md               ← commit, datum, licentie, wat er (niet) mee is gedaan
├── instrument/
│   ├── haal_rijk.py          ← kopieert uit MinBZK/par-dpia-form, met --check
│   ├── reken.py              ← referentie: expressie-evaluator, familiematch, maatregelen_bij, dossierstand, uitdraai
│   ├── bron/
│   │   ├── index.html
│   │   └── app.js            ← spiegelt reken.py als reken.<naam>
│   ├── bouw.py               ← YAML → JSON, dist/index.html met CSP-hashes
│   ├── oogst/                ← fase O: leest de brondocumenten, levert een concept-catalogus
│   ├── tests/
│   └── LEESMIJ.md
├── ai/
│   ├── opdrachten.json       ← de drie opdrachten (hoofdstuk 6)
│   ├── kern.py               ← gespiegeld in kern.js
│   └── bron/index.html       ← aparte pagina, eigen CSP
├── dist/index.html
├── verantwoording.md
└── site/
```

## 3. De bron

**`rijk/`** (besluit 1). Twee YAML-bestanden, byte voor byte gelijk aan een vastgepinde commit van
`MinBZK/par-dpia-form`. `BRON.md` legt vast: de commit, de datum, de licentie (EUPL-1.2), en dat er niets
in is gewijzigd. `haal_rijk.py --check` blokkeert de bouw als de kopie afwijkt. Bijwerken naar een nieuwe
commit is een bewuste stap met een regel in `CHANGELOG.md`, nooit automatisch, want een nieuwe versie
van het model kan vraag-id's verschuiven en daarmee bestaande dossiers raken.

**`dpia.json`**, drie secties.

**`families`.** De verwerkingsfamilies. Zeven uit de brondocumenten, cameratoezicht eerst:

| Familie | In de bron | Eerste vulling |
|---|---|---|
| Cameratoezicht en beeldherkenning | 27 | ja |
| Sociaal domein en uitkeringen | 35 | later |
| Openbare ruimte en sensoren | 16 | later |
| Fraude, ondermijning en handhaving | 15 | later |
| Bedrijfsvoering en generieke software | 12 | later |
| Dienstverlening en burgercontact | 10 | later |
| Schulden en geldzorgen | 7 | later |

Per familie: id, naam, omschrijving, trefwoorden voor de match, welke AP-categorieën uit `prescan.yaml`
doorgaans raken (als voorstel voor taak `3.1`), de id's van risico's en maatregelen, de tellers. Een
familie zonder vulling staat in de bron, is op het scherm zichtbaar leeg, en zegt waarom.

**`risicos`.** De risico's die telkens terugkomen, generiek geformuleerd, met de betrokkenen die het
raakt, de families, de teller, en de task-id van het rijksveld waar ze als voorstel verschijnen.

**`maatregelen`.** De catalogus (besluit 7). Per maatregel:

| Veld | Wat erin staat |
|---|---|
| `id` | stabiel, bijvoorbeeld `M-014` |
| `tekst` | de norm in de tegenwoordige tijd (besluit 13) |
| `thema` | toegang, bewaren, beveiliging, transparantie, leverancier, kwaliteit |
| `beschermt_tegen` | id's uit `risicos` |
| `normen` | AVG-artikel, en waar mogelijk BIO 2.0 |
| `families` | waar hij is waargenomen |
| `rijk_taak` | de task-id in `dpia.yaml` waar hij als voorstel verschijnt (besluit 8) |
| `bronnen` | de teller: hoeveel beoordelingen, uit hoeveel organisaties |

## 4. Rekenregels (`instrument/reken.py`, gespiegeld in `app.js`)

1. **`evalueer(expressie, antwoorden, scores)`.** Het Rijk gebruikt de bibliotheek JEXL met vijf
   geregistreerde functies (`answers`, `bool`, `countSelectedOptions`, `weightedCountMap`,
   `criteriaCheck`), één transform (`| count`) en de context `scores`. Alle expressies staan in
   `prescan.yaml` (`dpia.yaml` heeft er geen): tien `calculation`-blokken die de scores vullen en vier
   `assessments`. De gebruikte subset is klein: die functies, de operatoren `||`, `&&`, `==`, `!=`, `>`,
   `>=`, `+`, `in`, de ternaire `? :` en haakjes. Daarvoor komt een **eigen evaluator** in `reken.py` en
   `app.js`, geen `eval`, geen bibliotheek in de pagina. JEXL zelf draait alleen in de tests, als
   dev-dependency, om de eigen evaluator tegen het origineel te leggen (hoofdstuk 9). Een nieuwe
   rijksversie die een functie toevoegt, laat `haal_rijk.py --check` stranden op de parseertest.
2. **`plichttoets(antwoorden)`.** Loopt de `assessments` uit `prescan.yaml` af met `evalueer` en geeft
   per assessment (DPIA, DTIA, KIA, IAMA) het niveau en de criteria die het dragen, met hun
   `explanation`. Nooit een uitkomst zonder motivering, en geen uitkomst *niet nodig* (besluit 2).
3. **`familiematch(antwoorden, families)`.** Deterministisch op de trefwoorden, toegepast op de
   beschrijving in taak `0.2` van de pre-scan. De gebruiker kiest zelf.
4. **`maatregelen_bij(familie, bron)`.** De catalogusregels van die familie, gesorteerd op teller, met
   hun `rijk_taak`. De deterministische tegenhanger van de AI-opdracht.
5. **`dossierstand(dossier)`.** Per rijkshoofdstuk het aantal regels per stand en de open vragen.
6. **`uitdraai(dossier, rijk, bron)`.** Het conceptdocument in de volgorde van `dpia.yaml`: per veld het
   antwoord, per bevestigde regel de tekst, per openstaande regel de vraag. Nooit een voorstel als
   vastgestelde tekst.

Geen enkele functie oordeelt over de verwerking van de gebruiker.

## 5. Dossierformaat

JSON bij de gebruiker. Peildatum, de commit van `rijk/` waarop het dossier is gemaakt, de gekozen
familie, en de antwoorden gesleuteld op de task-id's van het Rijk (besluit 4). Per voorgestelde regel het
maatregel- of risico-id, de stand en eventuele eigen tekst. **Geen** organisatienaam of leveranciersnaam
als verplicht veld, nooit de API-sleutel, en niets uit `dpia.json` of `rijk/` zelf, alleen verwijzingen.

**Het formaat is dat van het Rijk** (besluit 4), met één toevoeging:

```json
{
  "$schema": ".../schemas/assessment-output.v2.schema.json",
  "metadata": { "urn": "urn:nl:dpia:3.0", "createdAt": "...", "completedTasks": ["0", "1"] },
  "answers":  { "0.1": "...", "2.1": [ { "_index": 0, "2.1.1": "..." } ] },
  "dpiacheck": {
    "rijk_commit": "<sha>", "peildatum": "2026-09", "familie": "cameratoezicht",
    "voorstellen": [ { "id": "M-014", "rijk_taak": "19.1.3", "stand": "bevestigd" } ]
  }
}
```

De rijkstool negeert het blok `dpiacheck` en leest de rest; dit instrument leest beide. Zo blijft het
bestand uitwisselbaar zonder dat de eigen laag verloren gaat. Verborgen antwoorden worden bij export
weggelaten, zoals het Rijk dat ook doet.

## 6. De pagina en de AI-hulp

Drie stappen, in de volgorde van het Rijk.

**Stap 1, pre-scan.** De 57 vragen uit `prescan.yaml`, met de uitkomst en motivering uit de
`assessments`. Daarnaast, aan te zetten: de familiekeuze en een voorstel voor de AP-categorieën op basis
van die familie. Wie alleen dit doet, heeft zijn pre-scan volgens het rijksmodel.

**Stap 2, wat komt er op me af.** De familie met haar risico's en de maatregelen uit de catalogus, met
tellers en met de plek in het rijksmodel waar ze thuishoren. Wie hier stopt heeft een leeslijst.

**Stap 3, de DPIA.** De 210 vragen uit `dpia.yaml`. Bij *Risico's voor de betrokkenen* en *Maatregelen*
staan de voorstellen uit stap 2 klaar, in de stand `voorstel`. Bevestigen, verwerpen of zelf schrijven.
Download als concept met de open vragen erin. Bestaat pas na fase 5.

**AI-hulp** (`ai/opdrachten.json`), drie opdrachten met een gesloten antwoordruimte:

| Opdracht | In | Uit | Controle |
|---|---|---|---|
| `prescan-invullen` | de beschrijving van de eigen verwerking | per pre-scanvraag een voorgesteld antwoord | elk voorstel citeert een zinsnede uit de eigen tekst; zonder citaat vervalt het |
| `familie-kiezen` | dezelfde beschrijving | familie-id's met een reden | het id moet bestaan |
| `maatregelen-kiezen` | beschrijving plus familie | `maatregel`-id's met per stuk een reden | het id moet in de catalogus staan; vrije tekst wordt geweigerd (besluit 17) |

Elke uitkomst komt binnen als `voorstel`. Geen knop die alles ineens overneemt. Geen opdracht voor
noodzaak of evenredigheid (besluit 18), geen opdracht die tekst herschrijft.

## 7. Fase O: de oogst

**Vooraf aan alle code.** Alleen cameratoezicht (besluit 20).

1. Inventariseer per map welk document de DPIA zelf is, en of het een maatregelentabel en een
   risicotabel bevat. Lever een telling.
2. **Klaar als** bekend is: aantal verwerkingen, aantal met bruikbare tabellen, overlap tussen de
   lijsten. **Afbreekcriterium:** bij minder dan vijf bruikbare bronnen stopt dit plan; dan is er geen
   ervaring om te delen en is het instrument een lege rijksvragenlijst met een ander logo.
3. De scrub, in deze volgorde: antwoordkolom en restrisico weg (besluit 12), leveranciers en systemen
   naar functieomschrijvingen (besluit 14), elke maatregel naar een norm in de tegenwoordige tijd
   (besluit 13), gelijke maatregelen samengevoegd tot één catalogusregel met teller (besluit 7), en per
   regel de `rijk_taak` (besluit 8). De `anonimizer` doet de eerste slag op namen, de vormtoets uit
   hoofdstuk 9 de tweede, de eindredactie is menselijk en wordt afgetekend.
4. **Klaar als** `dpia.json` een vulling voor cameratoezicht heeft die de vormtoets doorstaat.

De oogst draait op materiaal dat in de tenant blijft. Geen brondocument komt in een repo, ook niet
tijdelijk (A9).

## 8. Het kennisbank-item

Uit dezelfde oogst één item in `kennisbank/privacy/`, type `aanpak`: wat je moet weten als je aan een
DPIA op cameratoezicht begint, met verwijzing naar `dpiacheck` en naar de bibliotheek van de
Informatiebeveiligingsdienst voor voorbeelden. Eén item nu, per latere familie één. Niet honderd: de
volgorde in een sectie is redactioneel (B4) en de kennisbank is een geredigeerde leeslijst.

## 9. Tests

Als bij procescheck. Omdat er geen tweede lezer op de scrub zit, draagt de machinale toets meer gewicht.

**`test_rijk.py`.** `haal_rijk.py --check` groen; de YAML valideert tegen
`schemas/assessment-definition.v1.schema.json` uit hun repo; elke `rijk_taak` in `dpia.json` bestaat als
task-id in `dpia.yaml`.

**`test_evalueer.py`.** Elke expressie uit `prescan.yaml` (de tien `calculation`-blokken en de vier
`assessments`) parseert; een onbekende functie of operator is een fout, geen waarschuwing. Per
assessment minstens één doorloop die `required`, `recommended` en geen treffer oplevert, met de
verwachte `explanation`; de risicoscore precies op de drempel van vier; de doorgifte-expressie op alle
drie de uitkomsten. **Spiegeltest:** dezelfde antwoordensets door de eigen evaluator in Python, door de
eigen evaluator in JavaScript en door JEXL zelf (dev-dependency in de tests); de drie uitkomsten zijn
gelijk. Wijkt de JS-spiegel af van de Python-referentie, dan is dat een fout in de spiegel en niet in de
test.

**`test_dossier.py`.** Een dossier valideert tegen `assessment-output.v2.schema.json` uit hun repo, met
en zonder het blok `dpiacheck`; een dossier zonder dat blok wordt gelezen als leeg dossier met alleen
rijksantwoorden.

**`test_bron.py`** blokkeert de bouw bij:

1. **Gebiedende wijs** aan het begin van een maatregeltekst (`beëindig`, `zorg`, `sluit`, `richt`,
   `implementeer`, `stel in`, `pas aan`, `herzie`, `voer in`, `maak`, `bepaal`).
2. **Naamwoordelijke opsomming** zonder werkwoord (heuristiek: geen persoonsvorm in de zin).
3. **Gebreksformuleringen**: `nog niet`, `ontbreekt`, `alsnog`, `wordt niet`, `is niet ingericht`,
   `deels`.
4. **Verboden termen**: leveranciers, systemen, plaatsen, organisaties uit de bron. De lijst staat buiten
   de repo en wordt als pad meegegeven, zodat de namen zelf nooit in de repo landen.
5. **Persoonsgegevens**: de regexlaag van de `anonimizer`. Nul treffers.
6. **Schema en samenhang**: unieke id's, elke maatregel een teller, een normverankering, minstens één
   risico en een `rijk_taak`; elke familie verwijst alleen naar bestaande id's.

Verder `test_uitdraai.py` (een leeg dossier levert alleen open vragen; een voorstel wordt nooit
vastgestelde tekst; de kop zegt altijd *concept*), `test_ai.py` (de citaatcontrole), Playwright (de drie
stappen, een voorstel laden, downloaden, herladen) en een fixture-doorloop.

## 10. Bouwvolgorde

| Fase | Wat | Klaar als |
|---|---|---|
| O | Oogst en scrub, cameratoezicht (hoofdstuk 7) | vulling doorstaat de vormtoets en is afgetekend; bij minder dan vijf bruikbare bronnen stopt het plan |
| R | Bewaakte kopie van het Rijk (`prescan.yaml`, `dpia.yaml`, beide schema's), `BRON.md` | `haal_rijk.py --check` groen, YAML valideert tegen hun definitieschema |
| 1 | Evaluator en pre-scan, stap 1 | alle expressies uit `prescan.yaml` rekenen, met tests |
| 2 | Families, risico's, catalogus, stap 2 | tellers zichtbaar, `rijk_taak` klopt |
| 3 | Leesversie, verantwoording, statuut, projectentabel, pagina (B13) | `/dpiacheck/` **live**, label `concept` |
| 4 | Het kennisbank-item cameratoezicht | item in `privacy/`, B4-volgorde gezet |
| 5 | De DPIA-stap met voorstellen en uitdraai, stap 3 | een leeg dossier levert een document van open vragen |
| 6 | AI-hulp, drie opdrachten | citaatcontrole getest, sleutel alleen in `sessionStorage`, aparte CSP |
| 7 | Terugbijdrage aan het Rijk (besluit 6) | pull request ingediend volgens hun CONTRIBUTING |
| 8 | Volgende families | per familie fase O opnieuw |

## 11. Valkuilen

- **Schijnzekerheid is het echte risico.** Een voorinvulling die compleet oogt, vervangt het denkwerk
  dat de wet eist. Dat geldt dubbel voor de AI-laag.
- **De gebiedende wijs is de lek, niet de naam.** Besluit 13 en de vormtoets bestaan daarom, en worden
  nooit met een uitzondering omzeild.
- **De set is herkenbaar.** Honderdveertien verwerkingen in één regio met noembare systemen. Een
  gebreksformulering is daarmee niet anoniem maar aanwijsbaar.
- **Hun vraag-id's kunnen verschuiven.** Een nieuwe versie van het rijksmodel kan id's hernummeren. Elk
  dossier draagt daarom de commit waarop het is gemaakt, en bijwerken van `rijk/` is een bewuste stap
  met een migratienotitie.
- **De evaluator is een subset, geen JEXL.** Hij doet precies wat de expressies van het Rijk vandaag
  vragen. Een nieuwe rijksversie met een nieuwe functie of operator moet de parseertest laten stranden;
  stilzwijgend `false` teruggeven is het gevaarlijkste wat een plichttoets kan doen.
- **De verleiding om hun vragen te verbeteren.** Dat is de snelste manier om onverenigbaar te worden
  met de rijksketen en om het onderhoud alsnog naar je toe te trekken. Een betere vraag is een issue bij
  het Rijk, geen wijziging hier.
- **De tellers zijn geen decoratie.** Zonder zichtbare herkomst wordt materiaal uit één regio gelezen als
  een landelijke standaard.
- **De AI mag niet formuleren wat de catalogus niet kent.** Zodra vrije tekst als maatregel wordt
  toegelaten, vervalt de controleerbaarheid en de vormregel.

## 12. Buiten scope

Het publiceren van de brondocumenten in welke vorm dan ook. Een register van uitgevoerde DPIA's per
organisatie. Het beoordelen of een verwerking rechtmatig, noodzakelijk of evenredig is, door de tool of
door de AI. Wijzigingen aan de vragen van het Rijk. Materiaal uit de bibliotheek van de
Informatiebeveiligingsdienst. De IAMA. Een gedeelde opslag van dossiers. De overige zes families, tot
fase 8.
