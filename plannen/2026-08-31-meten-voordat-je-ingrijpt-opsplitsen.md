# Bouwplan: *Meten voordat je ingrijpt* opsplitsen naar wat het echt is

> **Voor de uitvoerder.** Taak voor taak uitvoeren, zonder eigen interpretatie. Elke taak heeft een doel,
> genummerde stappen met exacte paden, een test met de verwachte uitkomst, en een commit. **Een taak is
> pas klaar als de test groen is en de commit is gedaan.** Staat er "STOP", stop dan en meld wat je zag.

**Peildatum:** 31-08-2026. **Aanleiding:** het item is met 33.000 tekens en zestien hoofdstukken vier
soorten stuk tegelijk, en de lezer ziet niet welk deel voor hem is. Het draagt `type: aanpak`, maar het
gedraagt zich als een paraplu waar handleidingen onder hangen. Dat verband bestaat alleen in de
frontmatter en is op de site nergens zichtbaar.

---

## 1. Wat er nu mis is

Zes dingen, in volgorde van hoe hard ze de lezer raken. Het zesde speelt niet in dit item maar in de
SOC-cluster ernaast; het heeft dezelfde wortel en dezelfde oplossing, dus het lift mee.

**1.1 Vier soorten stuk in een map.** De hoofdstukken zijn niet van dezelfde orde:

| Soort | Hoofdstukken | Omvang | Voor wie |
|---|---|---|---|
| Methode | Drie uitgangspunten, Volgorde van aanpak, De methode | 4.800 | iedereen |
| Bestuursverhaal | Managementsamenvatting, Regie en accountability, Veilig faciliteren | 11.100 | bestuur, CISO |
| Technische handleiding | Netwerk en firewall, Killchain (ClickFix) | 10.000 | security, netwerk |
| Doorverwijzing | Werkplekanalyse, Identiteit en e-mail | 950 | (verwijst door) |
| Naslag | Herbruikbare query's, Werken met een LLM, Hoe dit samenhangt | 1.600 | beheer |

Wie het opent moet zelf uitzoeken welk van die vijf hij te pakken heeft. De tabel *Wat je hier vindt*
probeert dat op te lossen, en dat die tabel nodig is, is het bewijs van het probleem.

**1.2 Een halve verhuizing die je aan het stuk ziet.** Werkplekanalyse en Identiteit zijn uitgetrokken tot
eigen handleidingen; wat er staat is nu een doorverwijzing van 460 tekens, ingeklemd tussen hoofdstukken
van 5.767 tekens met echte inhoud. Het stuk vertelt zo zijn eigen verbouwing.

**1.3 `pijler` bestaat alleen in de frontmatter.** `werkplekanalyse-e5` en `identiteit-en-mail-meten`
dragen `pijler: meten-voordat-je-ingrijpt`. `tools/build.py` controleert op regel 257 of die map bestaat,
maar toont het veld nergens: niet op de kaart, niet op de sectiepagina, niet op de leesversie. Een lezer
die op een van de twee handleidingen landt, komt nooit te weten dat er een groter verhaal boven hangt.
Een veld dat alleen gecontroleerd wordt en nooit getoond, is administratie.

**1.4 Twee technische hoofdstukken zijn blijven zitten terwijl ze handleidingen zijn.** Netwerk en
firewall (5.767 tekens) en Killchain (4.196) hebben precies de vorm van de andere handleidingen: een
gap, een werkwijze, en aan het eind iets wat je kunt laten zien. Ze hangen ook aan barrieres:
`segment` (beperk lateral movement) en `edr`/`execution`. Ze zijn alleen nooit uitgetrokken.

**1.5 Het bestuursmateriaal hangt aan geen enkele barriere,** en dat kan ook niet: het gaat over de keuze
tussen lockdown en veilig faciliteren, over regie beleggen en over een resultaatverplichting bij
leveranciers. Dat is het gesprek met de directie, geen maatregel die je inricht. Het staat nu tussen de
technische hoofdstukken alsof het van dezelfde orde is.

**1.6 De SOC-cluster heeft een keuze zonder keuzehulp.** Barriere `soc` heeft vijf handleidingen:
`centrale-logverzameling` (fundering) en vier alternatieven (`co-managed-siem`, `uitbestede-soc`,
`mdr-dienst`, `regionaal-soc`), elk 4.500 tot 5.100 tekens. Dat er vier routes naast elkaar staan is
juist de waarde van het advies, maar de lezer die moet kiezen krijgt alleen een lijstje onderaan de
fundering; hij moet vier pagina's naast elkaar openen en zelf de vergelijking maken. Wat verschilt
(regie, wat je zelf in huis moet hebben, kostenprofiel, afhankelijkheid van een leverancier) staat
nergens naast elkaar. En het verband tussen de vijf bestaat, net als bij 1.3, nergens zichtbaar: er is
geen `pijler` gezet, dus ook na taak 1 tonen ze elkaar niet.

**Bijvangst.** Het hoofdstuk Netwerk en firewall is nooit geredigeerd: `he datacenter`, `Verkeerdat`,
`onvetrouwde`, en een zin die halverwege van constructie wisselt ("directe aandacht of in het datacenter
deze als een onvertrouwde securityzone is ingericht"). Dat repareer je in taak 3 terwijl je het toch
aanraakt.

---

## 2. Wat het moet worden

Vier stukken in plaats van een, elk met een etiket dat klopt:

| Nieuw | Type | Barrieres | Uit welke hoofdstukken |
|---|---|---|---|
| `meten-voordat-je-ingrijpt/` (blijft) | `aanpak` | geen | Uitgangspunten, Volgorde, De methode, Wat je hier vindt (herschreven als wegwijzer), Herbruikbare query's, Werken met een LLM, Hoe dit samenhangt, Herkomst |
| `netwerkanalyse-uit-data/` (nieuw) | `handleiding` | `segment` (verdieping) | Netwerk, firewall en core-routers |
| `killchain-naast-je-controls/` (nieuw) | `handleiding` | `edr`, `execution` (verdieping) | Killchain en chokepoints (ClickFix) |
| `sturen-op-weerbaarheid/` (nieuw) | `aanpak` | geen | Managementsamenvatting, Regie en accountability, Veilig faciliteren |

En `pijler` wordt zichtbaar: het item dat de pijler is, toont zijn kinderen; de kinderen tonen hun pijler.

Waarom `meten-voordat-je-ingrijpt` blijft bestaan en niet opgaat in de rest: de methode is het idee waar
alles onder hangt, en het is de enige plek waar staat waarom je eerst meet. Zonder dat stuk zijn de vier
handleidingen losse trucs. Het krimpt van 33.000 naar ongeveer 10.000 tekens en wordt daarmee leesbaar in
een kwartier, wat het nu niet is. De methode van 3.800 tekens is veruit het grootste blijvende deel;
wil je verder omlaag, dan moet ook de methode korter, en die redactiekeuze maakt dit plan bewust niet.

Waarom `sturen-op-weerbaarheid` een `aanpak` blijft en geen handleiding wordt: er is geen barriere waar
"kies tussen lockdown en veilig faciliteren" bewijs voor levert. Het is een bestuurlijk gesprek, geen
maatregel. Een `aanpak` zonder barrieres is precies het juiste etiket, en dat mag sinds 30-08.

---

## 3. Taken

### Taak 1: `pijler` zichtbaar maken

**Doel.** Een lezer op een handleiding ziet bij welke pijler hij hoort; een lezer op de pijler ziet welke
handleidingen eronder hangen. Doe dit eerst: zonder deze taak is het opsplitsen in taak 2 tot 4 een
verzameling losse stukken.

**Stappen.**

1. In `kennisbank/tools/build.py`, functie `meta_regel` (die de metaregel onder een kaart samenstelt;
   daar staan ook `barrieres` en `rol`): voeg toe dat een item met `pijler` het deel
   `hoort bij: <titel van de pijler>` krijgt. Haal die titel uit de frontmatter van
   `<vak>/<pijler>/README.md`, niet uit de mapnaam.
2. Voeg aan `build.py` een functie `kinderen_van(mapnaam, items) -> list[dict]` toe die uit een al
   gesorteerde itemlijst alles teruggeeft met `pijler == mapnaam`. Roep haar aan met de lijst die
   `main` na `zet_op_volgorde` heeft; dan is de volgorde vanzelf de redactionele.
3. In de leesversie van een pijler-item: zet onder de titel een blok met de kinderen. Er is geen functie
   die een leesversie opbouwt; leesversies zijn bestaande `index.html`-bestanden waarin `main` blokken
   bijwerkt tussen markeringen. Volg exact het patroon van `zet_kruimelpad` en `zet_bronvoet`: een
   functie `zet_pijlerblok(pad, kinderen, alleen_check)` met de markeringen `<!-- pijler-kinderen -->`
   en `<!-- /pijler-kinderen -->`, elk op een eigen regel, aangeroepen in `main` in dezelfde lus waar
   `zet_kruimelpad` wordt aangeroepen. Zo stapelt herbouwen niets.
4. Tests in `kennisbank/tools/test_handleidingen.py`, klasse `Export` of een nieuwe klasse `Pijler`:
   a. een item met `pijler` krijgt het pijlerlabel op zijn kaart;
   b. `kinderen_van` geeft de kinderen in de volgorde van `README.md`, niet alfabetisch;
   c. een pijler zonder kinderen levert geen leeg blok op;
   d. herbouwen stapelt het blok niet (bouw twee keer, tel de markeringen).

**Test.**
```bash
cd X:/SECURITY-COMMONS-NL/kennisbank && python -m pytest tools/ -q && python tools/build.py
grep -c "pijler-kinderen" security/meten-voordat-je-ingrijpt/index.html
```
Verwacht: tests groen, en de laatste `grep` geeft `2` (open- en sluitmarkering elk op een eigen regel,
dus precies een blok). Draai de build daarna nog een keer en controleer dat het `2` blijft.

**Commit.** `tools: een pijler toont zijn handleidingen, een handleiding zijn pijler`

---

### Taak 2: Netwerkanalyse wordt een eigen handleiding

**Doel.** `security/netwerkanalyse-uit-data/` bestaat, hangt aan barriere `segment` met rol `verdieping`,
en het hoofdstuk is uit het pijler-item verdwenen.

**Stappen.**

1. Maak `kennisbank/security/netwerkanalyse-uit-data/README.md` met deze frontmatter:
   ```
   titel: Netwerk en firewall analyseren uit data
   vakgebied: security
   type: handleiding
   normen: [BIO2]
   versie: 2026-09
   herkomst: gegeneraliseerd uit een casus bij een gemeentelijke organisatie
   status: in gebruik
   samenvatting: (schrijf twee of drie zinnen op basis van de eerste alinea's van het hoofdstuk; verzin niets bij)
   barrieres: [segment]
   rol: verdieping
   pijler: meten-voordat-je-ingrijpt
   ```
   `samenvatting` is een verplicht veld (statuut B2); zonder die regel blokkeert de build meteen.
   **STOP als `netwerksegmentatie` niet meer de fundering van `segment` is.** Controleer met
   `grep -A1 "^barrieres: \[segment\]" security/netwerksegmentatie/README.md`. Staat daar geen
   `rol: fundering`, meld het en ga niet verder: dan klopt `verdieping` hier mogelijk niet.
2. Neem de inhoud over van `## Netwerk, firewall en core-routers analyseren uit data` tot en met het
   subhoofdstuk `### Volgorde` dat erbij hoort (tot de kop `## Killchain`). Zet de subkoppen een niveau
   omhoog: `###` wordt `##`, `####` wordt `###`.
3. Voeg de verplichte koppen toe die een handleiding nodig heeft: `## Bewijs` en `## Zo leg je het uit`.
   Voor Bewijs: de regelexport met hit-counts, de routeringstabel naast de bedoelde segmentatie, de lijst
   versmalde regels met datum, en het overzicht van beheerinterfaces dat vanaf internet bereikbaar is.
   Verzin niets bij: gebruik wat in het hoofdstuk staat.
4. Repareer de taalfouten uit §1: `he datacenter`, `Verkeerdat`, `onvetrouwde`, en de kromme zin over
   Citrix. Verander niets aan de inhoudelijke strekking.
5. Vervang in `meten-voordat-je-ingrijpt/README.md` het hele hoofdstuk door een doorverwijzing van
   maximaal vier regels, in dezelfde vorm als die van Werkplekanalyse nu.
6. `python tools/leesversie.py security/netwerkanalyse-uit-data`, dan het item toevoegen aan
   `## Volgorde` in `security/README.md` (achter `microsegmentatie`, want daar hoort het thematisch),
   dan `python tools/build.py`.

**Test.**
```bash
cd X:/SECURITY-COMMONS-NL/kennisbank && python tools/build.py --check && python -m pytest tools/ -q
python -c "import json;d=json.load(open('handelingsperspectief.json',encoding='utf-8'));print([h['item'] for h in d['handleidingen'] if h['barriere']=='segment'])"
```
Verwacht: statuut groen, tests groen, en drie items bij `segment` (netwerksegmentatie, microsegmentatie,
netwerkanalyse-uit-data).

**Commit.** `Netwerkanalyse uit data wordt een eigen handleiding`

---

### Taak 3: Killchain wordt een eigen handleiding

**Doel.** `security/killchain-naast-je-controls/` bestaat, hangt aan `edr` met rol `verdieping`.

**Stappen.**

1. Zelfde werkwijze als taak 2, met:
   ```
   titel: De killchain naast je controls leggen
   samenvatting: (twee of drie zinnen op basis van het hoofdstuk)
   barrieres: [edr, execution]
   rol: verdieping
   pijler: meten-voordat-je-ingrijpt
   ```
   `execution` hoort erbij: de ketentabel dekt de Execution-fase expliciet (CLM, Win+R, AMSI). Bij beide
   barrieres bestaat al een fundering (`edr-inrichten`, `werkplekanalyse-e5`), dus `verdieping` botst
   nergens.
2. Neem `## Killchain en chokepoints (ClickFix)` over, inclusief de MITRE-tabel, `### Preventie versus
   detectie`, `### Restrisico's die je bewust accepteert`, `### Impact-anker` en `### Bronnen (publiek)`.
3. `## Bewijs`: de ingevulde ketentabel met per fase het chokepoint en of het preventie of detectie is,
   plus de lijst bewust geaccepteerde restrisico's met wie ze heeft geaccepteerd en wanneer.
4. **Let op de bestaande koppeling.** `aanvalspaden/tests/test_kennisbank_koppeling.py` pint vast hoe
   AP09 in `paden.json` eruitziet en noemt dit kennisbank-item alleen in zijn docstring en in de
   constante `KENNISBANKITEM` (regel 27), zodat de foutmelding de lezer naar de juiste plek stuurt. De
   test leest het item zelf NIET; hij kan dus niet rood worden door deze verhuizing. Werk de docstring
   en `KENNISBANKITEM` bij naar het nieuwe pad.
   De tabel zelf borg je met een diff: bewaar voor het knippen de tabelregels van het hoofdstuk
   (alle regels die met een sluisteken beginnen), doe hetzelfde na het plakken in het nieuwe item, en
   **STOP als de diff een verschil toont in de killchain-rijen:** de tabel moet ongewijzigd verhuizen.
5. Doorverwijzing achterlaten, leesversie, `## Volgorde` (achter `edr-inrichten`), build.

**Test.**
```bash
cd X:/SECURITY-COMMONS-NL/kennisbank && python tools/build.py --check
cd X:/SECURITY-COMMONS-NL/aanvalspaden && python -m pytest tests/ -q
```
Verwacht: allebei groen, inclusief `test_kennisbank_koppeling`.

**Commit.** In kennisbank: `De killchain naast je controls wordt een eigen handleiding`. In aanvalspaden:
`Test: de killchain-koppeling wijst naar zijn nieuwe plek`.

---

### Taak 4: Het bestuursverhaal wordt `sturen-op-weerbaarheid`

**Doel.** De drie bestuurshoofdstukken staan in een eigen item met een eigen doelgroep.

**Stappen.**

1. Maak `kennisbank/security/sturen-op-weerbaarheid/README.md`:
   ```
   titel: Sturen op weerbaarheid in plaats van op maatregelen
   vakgebied: security
   type: aanpak
   normen: [BIO2]
   versie: 2026-09
   herkomst: gegeneraliseerd uit een casus bij een gemeentelijke organisatie
   status: in gebruik
   samenvatting: (twee of drie zinnen: voor wie het is en welke drie vragen het beantwoordt)
   pijler: meten-voordat-je-ingrijpt
   ```
   Geen `barrieres` en geen `rol`: er is geen barriere waar dit bewijs voor levert, en dat is geen
   omissie maar de aard van het stuk. Zet dat in een zin onder de titel.
2. Neem over: `## Managementsamenvatting` (met alle subkoppen), `## Regie en accountability`,
   `## Veilig faciliteren als langetermijnstrategie`. Koppen een niveau omhoog waar dat nodig is.
3. Schrijf een openingsalinea van maximaal zes regels die zegt voor wie dit is (bestuur, directie, CISO)
   en welke drie vragen het beantwoordt: waarom dit onderwerp, wie is waarvoor verantwoordelijk, en
   kiezen we lockdown of veilig faciliteren.
4. Haal de drie hoofdstukken volledig uit `meten-voordat-je-ingrijpt/README.md`. Hier komt **geen**
   doorverwijzing per hoofdstuk voor terug; het nieuwe item komt in de wegwijzer van taak 5.
5. Leesversie, `## Volgorde` (direct achter `meten-voordat-je-ingrijpt`), build.

**Test.**
```bash
cd X:/SECURITY-COMMONS-NL/kennisbank && python tools/build.py --check && wc -c security/meten-voordat-je-ingrijpt/README.md
```
Verwacht: statuut groen, en het pijler-item is onder de 13.500 tekens. (Rekensom: 33.000 min de drie
verhuisde hoofdstukken plus twee korte doorverwijzingen is ongeveer 12.800; verder krimpen gebeurt pas
in taak 5.)

**Commit.** `Sturen op weerbaarheid wordt een eigen stuk voor bestuur en directie`

---

### Taak 5: De pijler wordt een wegwijzer

**Doel.** `meten-voordat-je-ingrijpt` is nog ongeveer 10.000 tekens en doet nog een ding: de methode
uitleggen en de weg wijzen.

**Stappen.**

1. Vervang de tabel `## Wat je hier vindt` door een tabel die alleen nog naar de vier kinderen wijst plus
   naar `sturen-op-weerbaarheid`, met per rij: voor wie, en welke vraag het beantwoordt. De rijen die naar
   een anker binnen het stuk zelf wezen, bestaan niet meer.
2. Verwijder de vier doorverwijzingshoofdstukken (Werkplekanalyse, Identiteit, Netwerk, Killchain) als
   eigen `##`-koppen. Ze staan in de tabel; twee keer verwijzen is ruis.
3. Herschrijf `## Volgorde van aanpak` zodat de vijf stappen naar de kinderen wijzen in plaats van naar
   ankers in hetzelfde bestand.
4. Controleer `## Hoe dit samenhangt met de andere stukken` en `## Herbruikbare query's`: die verwijzen
   naar hoofdstukken die er niet meer zijn.
5. Werk de `samenvatting` in de frontmatter bij: die belooft nu netwerk, regie en strategie in dit stuk.
6. Build, en draai de linkcontrole.

**Test.**
```bash
cd X:/SECURITY-COMMONS-NL/kennisbank && python tools/build.py --check && wc -c security/meten-voordat-je-ingrijpt/README.md
cd X:/SECURITY-COMMONS-NL/.github && python tools/linkcheck.py ..
grep -c "](#" ../kennisbank/security/meten-voordat-je-ingrijpt/README.md
```
Verwacht: statuut groen, het item onder de 11.000 tekens, linkcheck `0 dood`, en elke overgebleven
ankerlink wijst naar een kop die nog bestaat. Dat laatste toets je door alle `](#...)`-ankers uit het
bestand te halen en te vergelijken met de koppen (kleine letters, spaties en leestekens worden
koppelstreepjes); de lijst ankers zonder bijpassende kop moet leeg zijn.

**Commit.** `De pijler wijst de weg in plaats van alles zelf te vertellen`

---

### Taak 6: Naloop

**Stappen.**

1. `aanvalspaden`: `python tools/haal_handelingsperspectief.py`, dan `python mappingen/bouw.py`, dan
   `python -m pytest tests/ mappingen/tests/ -q`. Commit de bijgewerkte kopie.
2. `.github/ARCHITECTUUR.md`: de peildatum op de datum van uitvoering. De dekking blijft 35 van de 44:
   `segment`, `edr` en `execution` hadden al een fundering, dus er komen koppelingen bij (van 50 naar
   53), geen gedekte barrieres. Pas alleen aantallen koppelingen aan waar die genoemd worden.
3. `.github/BESLUITEN.md`: een regel bovenaan over het opsplitsen, met als onderbouwing dat een stuk dat
   vier soorten materiaal bevat, de lezer laat zoeken naar zijn eigen deel, en dat `pijler` een verband
   was dat alleen in de frontmatter bestond.
4. Voorpagina opnieuw genereren en committen (commando's staan in het rationalisatieplan, §0.2).
5. **Bal bij de eigenaar:** het item draagt `herkomst: gegeneraliseerd uit een casus bij een gemeentelijke
   organisatie`. Statuut A4 vraagt om een ja van de inbrenger voordat je publiceert. Dat punt staat open
   sinds 29-08-2026. Het opsplitsen verandert de inhoud niet, maar wel waar hij staat; **meld dat aan Bas
   en vraag of de inbrenger dit moet weten.** Verwerk zelf niets zonder antwoord.

**Klaar als:** alle tests groen, linkcheck `0 dood`, CI groen op kennisbank en aanvalspaden, en het
pijler-item onder de 11.000 tekens.

---

### Taak 7: De SOC-cluster krijgt een fundering die helpt kiezen

**Doel.** Wie voor barriere `soc` moet kiezen tussen zelf doen, co-managed, uitbesteden, MDR of
regionaal, vindt de vergelijking op een plek; de vijf items tonen dat ze bij elkaar horen. Deze taak kan
pas na taak 1 (het pijler-mechanisme) en staat verder los van taak 2 tot en met 6.

**Waarom geen zesde item.** Een aparte keuzewijzer zou het probleem herhalen dat dit plan oplost: nog
een stuk dat de lezer eerst moet vinden. De fundering is al de plek waar iedereen begint (zonder
logverzameling valt er niets te monitoren), dus daar hoort de keuze thuis.

**Stappen.**

1. Zet in de vier alternatieven `pijler: centrale-logverzameling` in de frontmatter. Door taak 1 tonen
   ze dan hun pijler, en toont de fundering zijn vier routes.
2. Voeg aan `security/centrale-logverzameling/README.md` een kop `## Kiezen tussen de routes` toe, op de
   plek van het huidige lijstje met de vier verwijzingen (dat lijstje vervalt; het pijlerblok en de
   tabel nemen het over). Een vergelijkingstabel met per route een rij en vier kolommen:
   wie draait de dienst, wat je zelf in huis moet hebben, waar de regie ligt, en wanneer deze route de
   logische is. **Vul de tabel uitsluitend met wat al in de vier items staat** (elk heeft de koppen
   Wanneer wel, wanneer niet en Wat het kost en wat het oplevert); verzin geen cijfers of oordelen bij.
   Sluit af met een zin die zegt dat de routes elkaar uitsluiten en de fundering niet: logverzameling
   heb je in elke route nodig.
3. Controleer de vier alternatieven op onderlinge consistentie terwijl je ze toch leest: zeggen twee
   items iets tegenstrijdigs over dezelfde route (bijvoorbeeld over wie de wacht draait of wat je zelf
   moet kunnen), meld dat dan en kies niet zelf een kant. **STOP bij een inhoudelijke tegenstrijdigheid.**
4. Werk de `samenvatting` van `centrale-logverzameling` bij: die belooft nu alleen de fundering, niet de
   keuzehulp.
5. Leesversie van de vijf items opnieuw genereren waar de README wijzigde, `python tools/build.py`, en
   de export controleren: de rollen veranderen niet (een fundering, vier alternatieven).

**Test.**
```bash
cd X:/SECURITY-COMMONS-NL/kennisbank && python tools/build.py --check && python -m pytest tools/ -q
grep -c "pijler-kinderen" security/centrale-logverzameling/index.html
python -c "import json;d=json.load(open('handelingsperspectief.json',encoding='utf-8'));print(sorted((h['item'],h['rol']) for h in d['handleidingen'] if h['barriere']=='soc'))"
```
Verwacht: statuut en tests groen, `grep` geeft `2`, en de export toont ongewijzigd een fundering en vier
alternatieven.

**Commit.** `De SOC-fundering helpt kiezen tussen de vier routes`

---

## 4. Als er iets misgaat

- **Een verplaatst hoofdstuk verwijst naar een anker in het oude bestand:** vervang door een link naar het
  nieuwe item, niet door de tekst te kopieren. Kopieren maakt een tweede waarheid.
- **`build.py` meldt dat een pijler niet bestaat:** de mapnaam in `pijler:` moet exact de mapnaam zijn,
  niet de titel.
- **Een test faalt op iets wat je niet hebt aangeraakt:** STOP, meld de test en de foutmelding. Pas geen
  tests aan om ze groen te krijgen, behalve waar dit plan dat expliciet zegt (taak 3, stap 4).
- **Twijfel over of een hoofdstuk mee moet:** de vraag is wie het leest. Bestuur en directie naar
  `sturen-op-weerbaarheid`, security en beheer naar een handleiding, iedereen naar de pijler.
