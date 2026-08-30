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

Vijf dingen, in volgorde van hoe hard ze de lezer raken.

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

**Bijvangst.** Het hoofdstuk Netwerk en firewall is nooit geredigeerd: `he datacenter`, `Verkeerdat`,
`onvetrouwde`, en een zin die halverwege van constructie wisselt ("directe aandacht of in het datacenter
deze als een onvertrouwde securityzone is ingericht"). Dat repareer je in taak 3 terwijl je het toch
aanraakt.

---

## 2. Wat het moet worden

Vier stukken in plaats van een, elk met een etiket dat klopt:

| Nieuw | Type | Barrieres | Uit welke hoofdstukken |
|---|---|---|---|
| `meten-voordat-je-ingrijpt/` (blijft) | `aanpak` | geen | Uitgangspunten, Volgorde, De methode, Wat je hier vindt (herschreven als wegwijzer), Werken met een LLM, Herkomst |
| `netwerkanalyse-uit-data/` (nieuw) | `handleiding` | `segment` (verdieping) | Netwerk, firewall en core-routers |
| `killchain-naast-je-controls/` (nieuw) | `handleiding` | `edr` (verdieping) | Killchain en chokepoints (ClickFix) |
| `sturen-op-weerbaarheid/` (nieuw) | `aanpak` | geen | Managementsamenvatting, Regie en accountability, Veilig faciliteren |

En `pijler` wordt zichtbaar: het item dat de pijler is, toont zijn kinderen; de kinderen tonen hun pijler.

Waarom `meten-voordat-je-ingrijpt` blijft bestaan en niet opgaat in de rest: de methode is het idee waar
alles onder hangt, en het is de enige plek waar staat waarom je eerst meet. Zonder dat stuk zijn de vier
handleidingen losse trucs. Het krimpt van 33.000 naar ongeveer 7.000 tekens en wordt daarmee leesbaar in
een kwartier, wat het nu niet is.

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

1. In `kennisbank/tools/build.py`, functie `kaart` (rond regel 465, waar `barrieres` en `rol` aan `delen`
   worden toegevoegd): voeg toe dat een item met `pijler` het label `pijler: <titel van de pijler>`
   krijgt. Haal die titel uit de frontmatter van `<vak>/<pijler>/README.md`, niet uit de mapnaam.
2. Voeg aan `build.py` een functie `kinderen_van(vak, mapnaam) -> list[dict]` toe die alle items
   teruggeeft met `pijler == mapnaam`, gesorteerd op de redactionele volgorde uit `<vak>/README.md`.
3. In de leesversie van een pijler-item: zet onder de titel een blok met de kinderen. Doe dit in
   `bouw_item` (of waar de leesversie wordt samengesteld) tussen het kruimelpad en de inhoud, met
   markering `<!-- pijler-kinderen -->` en `<!-- /pijler-kinderen -->` zodat herbouwen niets stapelt,
   net als bij het kruimelpad.
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
Verwacht: tests groen, en de laatste `grep` geeft `2` (open- en sluitmarkering, dus precies een blok).

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
   barrieres: [segment]
   rol: verdieping
   pijler: meten-voordat-je-ingrijpt
   ```
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
   barrieres: [edr]
   rol: verdieping
   pijler: meten-voordat-je-ingrijpt
   ```
2. Neem `## Killchain en chokepoints (ClickFix)` over, inclusief de MITRE-tabel, `### Preventie versus
   detectie`, `### Restrisico's die je bewust accepteert`, `### Impact-anker` en `### Bronnen (publiek)`.
3. `## Bewijs`: de ingevulde ketentabel met per fase het chokepoint en of het preventie of detectie is,
   plus de lijst bewust geaccepteerde restrisico's met wie ze heeft geaccepteerd en wanneer.
4. **Let op de bestaande koppeling.** `aanvalspaden/tests/test_kennisbank_koppeling.py` bewaakt of AP09
   in `paden.json` niet uit elkaar loopt met de killchain-tabel in dit item. Die test wijst nu naar
   `meten-voordat-je-ingrijpt`. Werk het pad in die test bij naar het nieuwe item en draai hem.
   **STOP als die test na het bijwerken rood blijft:** dan is de tabel bij het verhuizen veranderd, en dat
   mag niet.
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
Verwacht: statuut groen, en het pijler-item is onder de 12.000 tekens.

**Commit.** `Sturen op weerbaarheid wordt een eigen stuk voor bestuur en directie`

---

### Taak 5: De pijler wordt een wegwijzer

**Doel.** `meten-voordat-je-ingrijpt` is nog ongeveer 7.000 tekens en doet nog een ding: de methode
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
Verwacht: statuut groen, het item onder de 8.000 tekens, linkcheck `0 dood`, en geen enkele ankerlink
meer die naar een verdwenen hoofdstuk wijst (controleer de gevonden ankers met de hand tegen de koppen).

**Commit.** `De pijler wijst de weg in plaats van alles zelf te vertellen`

---

### Taak 6: Naloop

**Stappen.**

1. `aanvalspaden`: `python tools/haal_handelingsperspectief.py`, dan `python mappingen/bouw.py`, dan
   `python -m pytest tests/ mappingen/tests/ -q`. Commit de bijgewerkte kopie.
2. `.github/ARCHITECTUUR.md`: de stand van het handelingsperspectief bijwerken (het worden er twee meer
   dan de 35 van 30-08) en de peildatum op de datum van uitvoering.
3. `.github/BESLUITEN.md`: een regel bovenaan over het opsplitsen, met als onderbouwing dat een stuk dat
   vier soorten materiaal bevat, de lezer laat zoeken naar zijn eigen deel, en dat `pijler` een verband
   was dat alleen in de frontmatter bestond.
4. Voorpagina opnieuw genereren en committen (commando's staan in het rationalisatieplan, §0.2).
5. **Bal bij de eigenaar:** het item draagt `herkomst: gegeneraliseerd uit een casus bij een gemeentelijke
   organisatie`. Statuut A4 vraagt om een ja van de inbrenger voordat je publiceert. Dat punt staat open
   sinds 29-08-2026. Het opsplitsen verandert de inhoud niet, maar wel waar hij staat; **meld dat aan Bas
   en vraag of de inbrenger dit moet weten.** Verwerk zelf niets zonder antwoord.

**Klaar als:** alle tests groen, linkcheck `0 dood`, CI groen op kennisbank en aanvalspaden, en het
pijler-item onder de 8.000 tekens.

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
