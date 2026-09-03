# Bouwplan: de AI-hulp doortrekken naar meting, zelfcheck en CSIR

**Status:** geschreven 03-09-2026, na de oplevering van de meting en de uitlegpagina
[/ai-hulp/](https://security-commons-nl.github.io/ai-hulp/). Dit plan werkt stap 8 uit van
[2026-09-03-ai-hulp.md](2026-09-03-ai-hulp.md) ("CSIR, aanvalspaden, meting: volgt per tool"). Dat plan
is de referentie: waar hier "als bij procescheck" staat, bedoel ik de bouw die daar in detail staat en
die live draait op `/procescheck/ai/`. Volgorde vastgesteld met Bas op 03-09: meting, dan zelfcheck,
dan CSIR.

Geschreven om door een minder sterk model uitgevoerd te kunnen worden. Wat hier niet staat, volg je uit
het AI-hulp-plan en het procescheck-plan.

---

## 0. Besluiten (de spec)

1. **De kern wordt gekopieerd, niet herschreven.** `kern.js` (schema-controle, chunking, samenvoegen,
   csv en xlsx lezen, citaatcontrole, vergelijken en toepassen) is in procescheck de bron van waarheid.
   Elke andere tool krijgt een **byte-identieke kopie** plus een test die dat bewijst. Twee
   implementaties van de citaatcontrole is één te veel: dan verschilt de hallucinatiecheck per tool.
2. **Ophalen gaat met een script, niet met de hand.** Per repo `ai/haal_kern.py` naar het voorbeeld van
   `tools/haal_normen.py` in aanvalspaden: `--check` faalt als de kopie afwijkt van de bron, en zonder
   vlag haalt hij hem op. De bron is `procescheck/ai/bron/kern.js` als buurmap, anders de raw-URL van
   `main`. CI draait `--check`.
3. **Per tool één `opdrachten.json`.** Dat is het enige inhoudelijke verschil tussen de AI-pagina's:
   prompts, schema's, toegestane invoer en voorbeelden. Data, geen code.
4. **De pagina staat op `/<tool>/ai/`**, met dezelfde CSP als bij procescheck
   (`connect-src https: http://localhost:* http://127.0.0.1:*`), de sleutel alleen in
   `sessionStorage`, toestemming per sessie, en een knop *AI-hulp* in de dossierbalk van de tool. De
   tool zelf blijft op `default-src 'none'` en kent geen `fetch`.
5. **De AI beoordeelt nooit.** Geen verdicts, geen classificaties, geen statussen die de tool zelf
   uitrekent. De AI zet invoer om in de vorm die de tool verwacht; de mens beslist per regel.
6. **Elk item draagt een letterlijk citaat** (`bronregel`) en gaat door `kern.citaat_klopt`. Een item
   dat de controle niet haalt, komt in het voorstel te staan als *onzeker* en wordt niet
   voorgeselecteerd.
7. **AI-herkomst is zichtbaar tot in de uitdraai.** Elk overgenomen veld draagt `herkomst_ai` met
   datum, leverancier, model en de sha256 van de invoer. In de uitdraai staat het als eigen kolom of
   voetnoot. Dat is niet cosmetisch: bewijs dat door een taalmodel is omgezet, is zwakker bewijs, en
   dat moet een lezer kunnen zien.
8. **De zelfcheck krijgt geen tweede importweg.** De AI-pagina van de zelfcheck levert hetzelfde
   formaat als de meting al levert (`zelfcheck-antwoorden`, met `bron: "ai"`), zodat de knop
   *Antwoorden uit meting laden* het zonder wijziging aankan. Alleen de statusregel en de notitie
   verschillen ("uit AI-voorstel" in plaats van "uit meting").
9. **CSIR wordt geport, niet gekopieerd.** Die repo bouwt met node (`site/build.mjs`), niet met
   `bouw.py`. `kern.js` en `ai.js` zijn gewoon JavaScript en gaan mee zoals ze zijn; de bouw van de
   AI-pagina komt in de bestaande node-build. Er komt in CSIR **geen** `kern.py`: de gelijkheid met
   procescheck wordt daar met de byte-vergelijking bewaakt (besluit 1 en 2).
10. **De uitleg staat één keer,** op `/ai-hulp/` op de site. Elke AI-pagina verwijst ernaar, geen enkele
    tool herhaalt het verhaal. Die pagina is 03-09 opgeleverd.

---

## 1. Wat je hergebruikt

| Uit procescheck | Hoe |
|---|---|
| `ai/bron/kern.js` | byte-identieke kopie via `ai/haal_kern.py` |
| `ai/bron/ai.js` | kopie, met bovenaan de tool-specifieke constanten (opslagsleutels, titel, doel-URL) |
| `ai/bron/ai.css` | kopie |
| `ai/bron/index.html` | sjabloon; alleen kruimelpad, titel, de opdrachtenlijst en de teksten verschillen |
| `ai/bouw.py` | kopie (niet voor CSIR, zie hoofdstuk 4) |
| `ai/kern.py` | alleen in repo's die al een Python-referentie hebben (aanvalspaden heeft die) |
| `ai/tests/*` | kopie van de opzet; de fixtures en vastgelegde antwoorden zijn per tool nieuw |
| `ai/LEESMIJ.md` | kopie met de tool-specifieke opdrachten erin |

De sleutel voor het opnemen van fixture-antwoorden (`tests/fixtures/neem_op.py`) draait één keer met een
echte sleutel uit een omgevingsvariabele. Daarna staan de antwoorden in git en draaien de tests zonder
sleutel en zonder netwerk. Nooit een sleutel in de repo, nooit in secrets.

---

## 2. Meting (eerst)

De meting leest exports met een vast kolomcontract: `regels.json` noemt per bron de verplichte kolommen
(`kolommen`) en de kolommen die meetellen als ze er staan (`optioneel`). In de praktijk levert een
CMDB, een AD-uitdraai of een beheertool net andere kolomnamen, andere datumnotaties en een extra
kopregel. Dat handwerk neemt de AI-hulp over.

### 2.1 Twee opdrachten

**`contract`: een tabel omzetten naar het contract van een bron.**

- Invoer: `csv`, `xlsx`, `tekst`, `md` (een geplakte tabel mag).
- De gebruiker kiest eerst de doelbron uit een lijst die uit `regels.json` komt (30 bronnen, met hun
  titel en kolommen). Die keuze gaat als parameter in de prompt: het model krijgt de doelkolommen
  letterlijk mee, met de uitleg per bron uit `regels.json`.
- Systeemprompt (kern): "Je krijgt een tabel uit een beheersysteem. Zet die om naar de kolommen die
  hieronder staan. Neem waarden woordelijk over; reken niets om behalve datums, die je naar
  JJJJ-MM-DD zet. Een kolom die je niet kunt vullen laat je leeg. Voeg geen rijen toe en laat geen
  rijen weg."
- Schema: `{items: [{rij: {<doelkolom>: string, ...}, bronregel: string}], onzeker: [string]}`. De
  doelkolommen komen uit de gekozen bron; het schema wordt in de browser opgebouwd, zodat er niet
  dertig schema's in `opdrachten.json` hoeven te staan.
- De citaatcontrole: per rij moet `bronregel` woordelijk in de invoer voorkomen. Een verzonnen rij valt
  daarmee om.

**`document`: een rapport samenvatten naar de vijf documentitems.** Nee. Dit doen we niet, en de reden
hoort in het plan: de documentitems (6.3, 8.3, 9.1, 9.2, 9.3) toetsen op trefwoorden en een datum in de
**eigen tekst** van het rapport. Laat je een model die tekst herschrijven, dan toets je de samenvatting
van een model in plaats van het rapport. Daar wordt de meting niet beter van, en de toets wordt
misleidend. Plak het rapport zelf.

### 2.2 Wat de tool ermee doet

`meting/bron/app.js` krijgt een knop *Voorstel laden* naast *Dossier laden*. Het voorstel bevat de
omgezette tabel, niet een uitkomst. De tool:

1. bouwt uit `items` een CSV-tekst in het contract van de doelbron;
2. laat zien wat er staat (eerste tien rijen, aantal rijen, welke kolommen leeg bleven) en welke rijen
   de citaatcontrole niet haalden;
3. toetst pas na *Overnemen* met `reken.toets(bron, tekst, peildatum, REGELS)`, precies zoals bij een
   gekozen bestand;
4. schrijft de meting weg met `bestand: "AI-voorstel: <naam van de invoer>"`, de sha256 van de
   **omgezette** tabel, en `herkomst_ai` met leverancier, model en de sha256 van de oorspronkelijke
   invoer.

In de uitdraai staat bij zo'n meting "omgezet met AI" in de kolom Bestand. Wie het bewijs later wil
kunnen verdedigen, kan de omgezette tabel downloaden; die knop komt ernaast.

### 2.3 Grens

De meting rekent geen status per pad uit (besluit 12 uit het meting-plan) en de AI verandert daar niets
aan. Een AI-voorstel raakt alleen `metingen`, nooit `iamscan`, nooit de peildatum, nooit de
organisatienaam.

---

## 3. Zelfcheck (daarna)

### 3.1 Eén opdracht: `antwoorden`

- Invoer: `tekst`, `txt`, `md`, `pdf-tekst` (geplakt). Een beleidsplan, een architectuurdocument, een
  ISMS-hoofdstuk, een auditrapport.
- Het model krijgt de vragen van de zelfcheck mee: per vraag het id, de vraagtekst en de exacte
  antwoordopties uit `paden.json` (`onderdelen[].vragen[].opties[].id`). Dat is ongeveer 12 kB en gaat
  in de systeemprompt.
- Systeemprompt (kern): "Je krijgt een document over de beveiliging van een Nederlandse
  overheidsorganisatie. Bepaal per vraag welk antwoord het document ondersteunt. Kies alleen een
  antwoord als het document er iets over zegt; anders laat je de vraag weg. Zet in bronregel een
  letterlijk citaat dat het antwoord ondersteunt."
- Schema: `{items: [{vraag_id: string, antwoord: string, bronregel: string}], onzeker: [string]}`.
- Nabewerking in de browser, met `kern`: een `vraag_id` die niet bestaat valt eruit, een `antwoord` dat
  geen geldige optie-id is valt eruit, en een citaat dat de controle niet haalt valt eruit. Wat
  overblijft gaat in het bestandsformaat `zelfcheck-antwoorden` met `bron: "ai"` en per vraag een
  `herkomst`-regel met het citaat.

### 3.2 Wat de tool ermee doet

Niets nieuws. De knop *Antwoorden uit meting laden* leest dit formaat al: hij vult alleen vragen die
leeg of onbekend zijn, laat eigen antwoorden staan, en zet per gevulde vraag een notitie. Twee kleine
wijzigingen in `check/bron/app.js`:

- de notitie wordt "uit AI-voorstel <datum>: <citaat, ingekort tot 120 tekens>" als `bron == "ai"`;
- de statusregel noemt de leverancier en het model, en zegt hoeveel vragen zijn overgeslagen omdat ze
  al ingevuld waren.

De bestaande test `test_antwoorden_uit_meting_laden` krijgt een tweeling voor `bron: "ai"`.

### 3.3 Waarom dit mag

Een zelfcheck is een oordeel van de invuller, en dat blijft zo: de AI vult alleen lege vragen, met een
citaat erbij, en de invuller ziet per vraag waar het vandaan komt. Wie het niet vertrouwt, laat de
vraag leeg staan en de status wordt `unknown`. Dat is precies het gedrag dat `tools/score.py` al
aanhoudt.

---

## 4. CSIR (als laatste)

### 4.1 Wat er anders is

De CSIR-tool bouwt met node: `site/build.mjs`, `site/page.js`, `site/transforms.mjs`, met `csir.json`
als bron. Er is geen `bouw.py` en geen Python-referentie. Daarom:

- De AI-pagina wordt gebouwd door een nieuwe functie in `site/build.mjs` (of `site/ai.mjs` dat daaruit
  wordt aangeroepen) die dezelfde drie dingen doet als `ai/bouw.py`: `opdrachten.json`, `kern.js` en
  `ai.js` in één bestand zetten, de sha256-hashes in de CSP invullen, en falen als er een placeholder
  overblijft. Node heeft `crypto.createHash('sha256')`; de vorm van de hash is dezelfde.
- De gelijkheid van `kern.js` met procescheck wordt bewaakt met `ai/haal_kern.py --check` (het script is
  Python, de repo heeft al Python voor de tests) of met een node-variant. Kies één en documenteer die.
- Uitvoer: `dist/ai/index.html`, en in de Pages-bouw `site/ai/index.html`.

### 4.2 Twee opdrachten

**`classificatie`: van objectbeschrijving naar een voorstel voor de zes gevolgcriteria.**

- Invoer: `tekst`, `txt`, `md` (een functionele beschrijving, een projectplan, een objectdossier).
- Het model krijgt de zes criteria met hun ernstniveaus uit `csir.json` (`classificatie.criteria` en
  `classificatie.ernst`).
- Schema: `{items: [{criterium: string, ernst: string, bronregel: string}], onzeker: [string]}`.
- De tool rekent daarna zelf de functiebox en het weerstandsniveau uit (`functiebox_niveau`), zoals nu.
  De AI stelt alleen de zes ernstwaarden voor, en de mens kan elke waarde omzetten.

**`leveranciersdocument`: van een security-plan naar status en bewijs per control.**

- Invoer: `tekst`, `txt`, `md`, `pdf-tekst`.
- Het model krijgt de controls van de gekozen paragraaf mee (niet alle 127 in één keer: dat is te veel
  en levert slechte antwoorden). De gebruiker kiest de paragraaf, de pagina stuurt per paragraaf één
  aanroep.
- Schema: `{items: [{control: string, status: string, bewijs: string, bronregel: string}], onzeker: []}`,
  waarbij `status` een van de vaste keuzes uit `csir.json` (`keuzes.status`) is.
- Grens: de AI stelt nooit *van toepassing* vast. Welke controls van toepassing zijn, volgt uit de
  classificatie en is een besluit van de organisatie.

---

## 5. De gedeelde kern in de praktijk

`ai/haal_kern.py` per repo, met dit gedrag:

```
python ai/haal_kern.py            haalt kern.js op en schrijft ai/bron/kern.js
python ai/haal_kern.py --check    faalt met een diff als de kopie afwijkt
```

Bron, in deze volgorde: `../procescheck/ai/bron/kern.js` als de buurmap er staat, anders
`https://raw.githubusercontent.com/security-commons-nl/procescheck/main/ai/bron/kern.js`. De kopie
draagt bovenaan een commentaarregel met de datum en de sha256 van de bron, zodat je in één oogopslag
ziet of hij achterloopt. Die regel telt niet mee in de vergelijking.

Wijzigt de citaatcontrole? Dan pas je hem in procescheck aan, draait `haal_kern.py` in de andere repo's
en commit dat mee. Loopt een kopie achter, dan valt de CI van die repo om, niet die van procescheck.

---

## 6. Tests per tool

Als bij procescheck (41 tests), met per tool minstens dit:

| Test | Waarop |
|---|---|
| `test_kern_is_gelijk` | `ai/bron/kern.js` byte-identiek aan de bron; anders overslaan als de bron ontbreekt |
| `test_opdrachten_schema` | elke opdracht heeft id, titel, uitleg, invoer, doel, systeemprompt en schema; het schema is geldige JSON Schema met `additionalProperties: false` |
| `test_schema_dekt_het_datamodel` | elk veld in het schema bestaat in de tool (bij meting: elke doelkolom komt uit `regels.json`; bij de zelfcheck: elk `vraag_id` en elke optie-id komt uit `paden.json`; bij CSIR: elk criterium en elke status komt uit `csir.json`) |
| `test_vastgelegd_antwoord_wordt_verwerkt` | het opgenomen modelantwoord door de kern halen levert de verwachte items, en de citaatcontrole slaagt |
| `test_verzonnen_citaat_valt_om` | één woord in de `bronregel` veranderen en het item is onzeker |
| `test_geen_netwerk_in_de_tool` | de tool doet tijdens een volledige doorloop geen enkele aanroep buiten `file://` |
| `test_sleutel_lekt_niet` | de sleutel staat niet in `localStorage`, niet in het voorstel, niet in een download, niet in de gebouwde pagina |
| `test_voorstel_weigert_andere_tool` | een voorstel met een andere `tool` wordt geweigerd |
| `test_overnemen_verandert_alleen_wat_je_kiest` | in de browser: één regel overnemen laat de rest ongemoeid, en `herkomst_ai` staat erbij |
| `test_uitdraai_toont_ai_herkomst` | de uitdraai noemt bij een overgenomen veld dat het uit een AI-voorstel komt |

De browsertests draaien met Playwright en een gestubde `fetch`: het vastgelegde antwoord komt uit de
fixture, er gaat niets naar buiten. Dat is de reden dat de opgenomen antwoorden in git staan.

---

## 7. Workflows

Per repo een extra CI-job *AI-hulp* met dezelfde installatie als de app-job, plus:

```
python ai/haal_kern.py --check
python ai/bouw.py            (CSIR: node site/build.mjs, die de AI-pagina meeneemt)
python -m pytest ai/tests -v
```

In `pages.yml` na de tool: `python ai/bouw.py dist/ai` en `test -s dist/ai/index.html`. Geen sleutel in
secrets, nergens.

---

## 8. Uitleg en statuut

- Per tool in de README onder *Snel starten* één stap: wat de AI-hulp overneemt, met de zin "eigen
  sleutel, eigen leverancier; de tool zelf gaat nergens heen" en een verwijzing naar `/ai-hulp/`.
- Per tool in `werkwijze.md` of `verantwoording.md` een kopje *AI-hulp*: wat het doet, wat het nooit
  doet, en waarom een AI-omzetting zwakker bewijs is dan een rechtstreekse export (dat laatste vooral
  bij de meting).
- `ai/LEESMIJ.md` per tool: het patroon en hoe je een opdracht toevoegt.
- `REDACTIESTATUUT.md` B14 is op 03-09 al verduidelijkt (opt-in AI-hulp mag, mits aparte pagina, eigen
  sleutel zonder opslag, voorstel in plaats van schrijven, toestemming per sessie). Geen nieuwe
  statuutwijziging nodig.
- `BESLUITEN.md` per repo: het besluit dat de tool een AI-hulp krijgt, met de grens erbij (wat de AI
  niet mag beoordelen).
- De site: `/ai-hulp/` is opgeleverd op 03-09 en noemt de tools in de volgorde van dit plan. Zodra een
  tool live gaat, wordt die regel op de pagina bijgewerkt.

---

## 9. Valkuilen

- **De prompt met de vragenlijst is groot.** Bij de zelfcheck gaat er 12 kB systeemprompt mee. Tel dat
  mee in de toestemmingstekst ("dit kost x aanroepen van ongeveer y tekens"), anders schrikt de
  gebruiker van zijn factuur.
- **Een AI-omzetting is geen export.** Bij de meting is de verleiding groot om de omgezette tabel als
  gewone meting te behandelen. Doe dat niet: `herkomst_ai` en de zichtbaarheid in de uitdraai zijn de
  prijs voor het gemak.
- **Optie-ids zijn geen labels.** Een model kiest graag "ja" waar de optie-id `yes` heet, of het label
  in plaats van de id. Filter dat in de browser en reken die gevallen bij `onzeker`, niet bij de
  antwoorden.
- **Een lokaal model levert slechter JSON.** Ollama haalt `response_format: json_schema` vaak niet. De
  terugval op `json_object` staat er al; test met een lokaal model voordat je in de uitleg belooft dat
  het werkt.
- **Byte-gelijkheid en regeleindes.** De kopie van `kern.js` moet LF blijven, anders faalt de
  vergelijking op Windows. Zet het in `.gitattributes` van de repo waar de kopie landt.
- **Twee schrijvers.** Loopt er een tweede sessie in dezelfde repo, spreek dan af wie commit. Dat kostte
  op 03-09 bijna een dubbele commit.

---

## 10. Stappen

1. **Meting. Gedaan 03-09-2026**, live op `/aanvalspaden/meting/ai/`, 25 tests. Drie dingen liepen
   anders dan hier voorzien, en dat staat in `meting/ai/LEESMIJ.md`: het samenvoegen van stukken kan
   niet met `kern.voeg_stukken_samen` (die ontdubbelt op een sleutelveld dat een omgezette tabel niet
   heeft), de citaatcontrole gebeurt op de AI-pagina en gaat als oordeel per rij mee in het voorstel
   (de tool krijgt de invoer niet, alleen de sha256), en het vastgelegde antwoord is met de hand
   geschreven omdat er geen opname met een echte sleutel is gedaan; `neem_op.py` staat klaar.
2. **Zelfcheck.** Zelfde kopieerstap in dezelfde repo (kern staat er dan al); `opdrachten.json` met de
   opdracht `antwoorden`; de twee kleine wijzigingen in de importmelding; tests, waaronder de tweeling
   van `test_antwoorden_uit_meting_laden`. Klaar als `/aanvalspaden/ai/` live staat.
3. **CSIR.** De node-build uitbreiden met de AI-pagina; `kern.js` ophalen en de gelijkheid bewaken;
   `opdrachten.json` met `classificatie` en `leveranciersdocument`; per paragraaf één aanroep; tests;
   CI; Pages. Klaar als `/csir-assessment-tool/ai/` live staat.
4. **Afronden.** De regel op `/ai-hulp/` bijwerken naar de stand ("staat bij procescheck, de meting, de
   zelfcheck en de CSIR-tool"), en in `ARCHITECTUUR.md` de AI-hulp als patroon noemen in plaats van als
   eigenschap van procescheck.

Applicatiecheck krijgt geen AI-hulp in dit plan: die tool wacht eerst op F1 (de ontbrekende
bewijsvoering). Zodra die er is, is de vorm hier dezelfde.
