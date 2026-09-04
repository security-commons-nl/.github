# Bouwplan: de weerbaarheidsgame naar v2

**Status:** geschreven 03-09-2026 op verzoek van Bas ("werkt, maar nog niet optimaal; moderner, iets
uitgebreider"), en diezelfde avond herschreven. De eerste versie beschreef de tool vanuit de
ontwerpnotitie van maart en de ROADMAP, niet vanuit de werkende tool. Dat gaf een te arm beeld: de game
is verder dan die stukken zeggen. Hoofdstuk 1 en 2 komen nu uit een echte doorloop in de browser, en de
besluiten zijn daarop bijgesteld. Wat in de eerste versie stond en niet klopte, staat in hoofdstuk 9,
zodat niemand er opnieuw intrapt.

Geschreven om door een minder sterk model uitgevoerd te kunnen worden, in de vorm van
[het procescheck-plan](2026-09-02-procescheck-instrument.md) en [het meting-plan](2026-09-03-meting.md).
De drie vragen die open stonden, zijn beantwoord (hoofdstuk 10); het plan is uitvoerbaar.

---

## 1. Wat er nu staat, na een doorloop in de browser

Eén bestand, `weerbaarheid-game.html`, 228 kB en 4.249 regels, met één `<script>` en één `<style>`.
`index.html` stuurt door. Wat erin zit:

**Drie pijlers, negen diensten.** *Weerbare Stad* (crisis-alert, noodsteunpunten, lokale zorg), *Vitale
Basisvoorzieningen* (drinkwater, uitkering, afval) en *Weerbare Gemeente* (paspoort, crisisorganisatie,
informatievoorziening). Je klikt van pijler naar dienst.

**Een voorbereidingsfase met een budget.** Per dienst krijg je acht maatregelen te zien en mag je er
drie kiezen ("Je hebt budget voor 3 maatregelen. Kies verstandig"). Sommige helpen, andere klinken goed
en doen niets: *Nieuw crisisportaal bouwen* werkt niet als het internet uitvalt. Die keuze bepaalt wat
er straks beschikbaar is. Je kunt de fase overslaan met *huidige situatie*.

**Negentien scenario's, niet negen.** Per dienst zijn er twee of drie: bij afval een storing in de
tag-server én een brand in het wagendepot; bij paspoort een BRP-storing, een brand en een epidemie. Elk
scenario heeft zijn eigen keten (`ketenOverride`), zijn eigen maatregelen met een effectiviteit in
procenten, en zijn eigen afloop.

**Een keten van vijf tandwielen** met de SPOF gemarkeerd, een la met maatregelen onderaan die je naar
een noodzone sleept of klikt.

**Complicaties op een klok.** Negentien stuks, met een vertraging: acht seconden na de start raakt de
diesel op en zakt je noodoplossing van 50 naar 20 procent; na vijftien seconden zijn de sleutels van het
depot zoek en staat alles stil. Er loopt een spelklok en een escalatiereeks.

**Een zijbalk met maatschappelijke druk** (een percentage met een woord erbij, van rustig tot kritiek),
de stand van de dienst voor de inwoner, en een meldingenlogboek.

**Een keten-walkthrough**: vijf stappen die tandwiel voor tandwiel uitleggen wat er gebeurt. Plus een
knop *Uitleg*, een presentatiemodus (*Volledig scherm*, grotere letters, bediening weg) en een
printstylesheet die het huidige scherm met zijbalk en scorekaart op papier zet.

Wat er goed aan is en dus blijft: het tandwielbeeld, de taal van de inwoner ("Uw paspoort is niet
beschikbaar"), de budgetkeuze die laat voelen dat je niet alles kunt, en de complicaties die laten zien
dat een noodoplossing zelf ook stukgaat. Een bestuurder snapt binnen tien seconden wat hij ziet.

---

## 2. Wat er niet goed aan is

| Wat | Waarom het knelt |
|---|---|
| De negen diensten, negentien scenario's en al hun statussen staan hard in de HTML | Een andere organisatie kan de game niet met haar eigen cijfers draaien zonder in 4.249 regels code te editen. De cijfers komen uit de rapportages van één organisatie, maart 2026. |
| Eén soort schade: de dienst valt uit | Elk scenario gaat over beschikbaarheid. Een datalek, een onrechtmatige verwerking of gegevens die niet meer kloppen komen niet voor. Voor een FG of privacy officer valt er niets te zien, terwijl dat de helft van het gesprek is. |
| Er blijft niets over na het gesprek | `localStorage` bewaart alleen of je de tutorial hebt gezien. Er is geen dossier en geen besluitenlijst, en de print zet het scherm op papier zonder wat er is besloten. Elk ander instrument in de commons levert een dossier en een A4. |
| Losstaand van de keten | procescheck kent de processen en hun RTO, de zelfcheck en de meting kennen de barrieres. De game weet daar niets van, terwijl het over hetzelfde gaat. |
| Geen CSP, geen bron-vingerafdruk, geen test op de rekenkant | De vaste vorm van de commons (statuut B14) vraagt dat wel; deze pagina is van voor die afspraak. Sinds 03-09 zijn er wel twaalf browsertests op drie schermmaten. |
| Nul `aria`-attributen, nul `tabindex`, geen `prefers-reduced-motion` | Alles gaat met de muis en met kleur. In een raadzaal met een beamer, en voor wie meekijkt met een schermlezer of moeite heeft met beweging, is dat een probleem. |

Dat laatste is gemeten, niet geschat: er staat geen enkel `aria-`, geen `tabindex` en geen
`prefers-reduced-motion` in het bestand.

---

## 3. Besluiten (de spec)

1. **De inhoud gaat uit de code naar `spel.json`.** Pijlers, diensten, ketens, scenario's, maatregelen,
   complicaties en teksten worden data met een vingerafdruk, precies als `procescheck.json` en
   `meting/regels.json`. Wat er nu is wordt het meegeleverde voorbeeld, herkenbaar als voorbeeld.
2. **Eén bestand blijft één bestand.** `bouw.py` zet bron, opmaak en script in `dist/index.html` met een
   CSP op sha256-hashes en `default-src 'none'`. Geen bundler, geen afhankelijkheden.
3. **Wat er is, blijft.** De budgetfase, de negentien scenario's, de complicaties op een klok, de
   maatschappelijke druk, de walkthrough, de presentatiemodus en de print blijven zoals ze werken. Dit
   is een verbouwing, geen herbouw: alles hieronder komt erbij of eronder.
4. **Naast beschikbaarheid komt vertrouwelijkheid.** Per dienst een tweede as: welke gegevens gaan er
   om, hoeveel betrokkenen, en wat is de schade als die uitlekken. Dat wordt een nieuw scenariotype
   `datalek`: de keten draait door, maar de zijbalk toont wat er op straat ligt en de druk loopt op een
   andere manier op. Geen aparte tool; dezelfde ketting, andere schade.
5. **De game krijgt een dossier.** `localStorage` plus een JSON die je opslaat en terugleest: de
   organisatienaam, de peildatum, welke maatregelen je koos, welke scenario's je speelde, wat de afloop
   was en welke besluiten het college nam. Laden weigert een ander formaat en meldt een andere
   bronversie, als bij de andere instrumenten.
6. **Elk gesprek levert een A4.** De print wordt een uitdraai: organisatie en datum, de gespeelde
   scenario's met hun afloop, de maatregelen die ontbraken, en de besluiten uit de besluitvakjes. De
   huidige printstylesheet is het vertrekpunt.
7. **Een besluitvakje onder elk ketenscherm.** *Besluit van het college*: wat daar staat komt in de
   uitdraai. Dat is het verschil tussen een demonstratie en een vergaderstuk.
8. **De game leest uit de keten.** Twee importknoppen, allebei optioneel: een procescheck-dossier
   (processen met hun RTO en RPO worden diensten met hun hersteltijd) en een zelfcheck- of
   meting-export (de status van een barriere kleurt de bijbehorende maatregel). Zonder import werkt de
   game met het voorbeeld.
9. **De game rekent geen risico's uit.** Geen score per organisatie, geen rangorde, geen matrix. Hij
   toont een keten en laat zien wat er stukgaat; het oordeel is van het college. Dat was al zo en blijft
   zo, en het hoort expliciet in de verantwoording.
10. **Toegankelijk in een raadzaal.** `prefers-reduced-motion` respecteren (dan geen draaiende
    tandwielen maar stappen), alles met het toetsenbord bedienbaar, `aria-live` op de meldingen en de
    druk, contrast volgens WCAG AA. Kleur is nooit de enige drager van betekenis: rood, oranje en groen
    krijgen ook een woord. Dit is de grootste inhaalslag, want er staat nu niets.
11. **Er komen drie diensten bij:** belastingen en invordering, vergunningen en toezicht, verkiezingen.
    Daarmee komt de game op twaalf diensten. Zie hoofdstuk 10.

---

## 4. Het bronformaat (`spel.json`)

De structuur volgt wat er in de code al staat, met drie toevoegingen: `gegevens` per dienst (voor het
datalek), `barriere` per maatregel (voor de koppeling met de zelfcheck) en `status` in woorden.

```json
{
  "versie": "2026-09",
  "herkomst": "voorbeeldcijfers uit de continuiteitsrapportages van een gemeentelijke organisatie, maart 2026",
  "pijlers": [
    {"id": "stad", "naam": "Weerbare Stad", "kleur": "#3b5bdb",
     "uitleg": "Diensten gericht op inwoners, bedrijven en maatschappelijke organisaties",
     "diensten": ["crisis", "noodsteun", "zorg"]}
  ],
  "diensten": [
    {
      "id": "paspoort", "naam": "Paspoort aanvragen", "icoon": "🛂", "pijler": "gemeente",
      "sub": "Inwoners kunnen geen reisdocument krijgen",
      "gegevens": {"soort": "persoonsgegevens", "bijzonder": false,
                   "betrokkenen": "alle aanvragers", "schade": "identiteitsfraude"},
      "budget": 3,
      "voorbereiding": [
        {"id": "p1", "naam": "Tijdelijke reisdocumenten op voorraad", "helpt": true,
         "uitleg": "Werkt als de BRP-koppeling uitvalt."},
        {"id": "p2", "naam": "Nieuw aanvraagportaal bouwen", "helpt": false,
         "uitleg": "Een portaal helpt niet als de bron eronder plat ligt."}
      ],
      "scenarios": [
        {
          "id": "paspoort-brp", "label": "BRP-koppeling uit", "raakt": "beschikbaarheid",
          "incident": "De landelijke BRP-koppeling is onbereikbaar",
          "keten": [
            {"id": "k0", "naam": "Baliemedewerker", "soort": "mens"},
            {"id": "k2", "naam": "BRP-koppeling", "soort": "systeem", "spof": true,
             "leverancier": "RvIG", "host": "datacenter",
             "uitleg": "De koppeling haalt de persoonsgegevens op bij de landelijke voorziening."}
          ],
          "maatregelen": [
            {"id": "m1", "naam": "Tijdelijk reisdocument", "soort": "reactief", "status": "deels",
             "effectiviteit": 60, "effect_label": "60% van de aanvragen", "barriere": "fallback",
             "uitleg": "Een noodreisdocument voor wie morgen moet vliegen."}
          ],
          "complicaties": [
            {"id": "c1", "label": "Voorraad op", "na_seconden": 12, "degradeert": "m1",
             "nieuwe_effectiviteit": 20, "melding": "De voorraad noodreisdocumenten is op."}
          ],
          "afloop": {
            "ok":    {"icoon": "🛂", "titel": "Aanvraag verwerkt", "tekst": "..."},
            "deels": {"icoon": "📄", "titel": "Alleen noodreisdocumenten", "tekst": "..."},
            "fail":  {"icoon": "🚫", "titel": "Geen uitgifte", "tekst": "..."}
          }
        },
        {
          "id": "paspoort-lek", "label": "Aanvraaggegevens op straat", "raakt": "vertrouwelijkheid",
          "incident": "Een export met aanvraaggegevens is gelekt",
          "gevolg": {"betrokkenen": "8.400 aanvragers", "meldplicht": true,
                     "inwoner": "Uw paspoortgegevens liggen op straat."}
        }
      ]
    }
  ]
}
```

Vier afspraken bij dat formaat:

- **`status` is `ja`, `deels` of `nee`,** niet groen/oranje/rood. Kleur is presentatie; de bron zegt wat
  het is. Een maatregel zonder status is `onbekend` en toont grijs met het woord erbij.
- **`barriere` is de sleutel uit `paden.json`.** Alleen daarmee kan een zelfcheck- of meting-uitslag de
  maatregel kleuren. Een maatregel zonder barriere werkt gewoon, maar wordt nooit automatisch gevuld.
- **`raakt` bepaalt het scenariotype.** `beschikbaarheid` gedraagt zich als nu; `vertrouwelijkheid`
  laat de keten draaien en toont de schade in de zijbalk.
- **Tandwielgrootte is presentatie, geen data.** De huidige velden `sf` en `teeth` staan nu per stap in
  de code; die verhuizen naar de bouw, afgeleid van de positie in de keten. Wie een dienst toevoegt,
  hoort niet over tandwieltanden na te denken.

---

## 5. De schermen

De vier schermen die er zijn blijven, met deze wijzigingen.

**Overzicht (pijlers).** Ongewijzigd, met de organisatienaam en de peildatum erbij, en de balk
*voorbeeldcijfers* zolang je geen eigen organisatie hebt ingevuld.

**Pijler (diensten).** Ongewijzigd. De dienstkaarten rekten uit tot de hoogste kolom; dat is 03-09
gerepareerd.

**Voorbereiding (budget).** Ongewijzigd, met per maatregel de herkomst als hij uit een import komt.

**Keten (scenario).** Hier komt het meeste bij: de scenariokiezer krijgt de datalek-scenario's erbij, de
zijbalk toont bij een datalek wat er op straat ligt in plaats van de dienststatus, en onder het scherm
komt het besluitvakje. De walkthrough blijft; die viel 03-09 buiten beeld en is gerepareerd.

**Uitdraai (nieuw, print).** Organisatie en datum, de gespeelde scenario's met hun afloop, de gekozen en
ontbrekende maatregelen, de besluiten, en de bronversie met vingerafdruk.

---

## 6. Tests

Er staan sinds 03-09 twaalf browsertests in `tests/test_scherm.py` (de naam, de kaarthoogtes, de
walkthrough binnen beeld op drie schermmaten, en een volledige doorloop). Daar komt bij:

| Test | Waarop |
|---|---|
| `test_bron` | `spel.json` valideert tegen het schema; elk scenario heeft een keten met precies een SPOF; elke `barriere` bestaat in `paden.json`; elke `status` is ja, deels, nee of onbekend |
| `test_scenario` | een complicatie degradeert de juiste maatregel op het juiste moment; een datalek laat de keten draaien maar verandert de zijbalk; het budget laat nooit meer keuzes toe dan `budget` |
| `test_import_procescheck` | een procescheck-dossier levert diensten met naam, kritiek en RTO; een dossier van een andere tool wordt geweigerd |
| `test_import_zelfcheck` | een `zelfcheck-antwoorden`-bestand kleurt de maatregelen met een barriere en laat de rest ongemoeid |
| `test_bouw` | een script, een stijl, hashes in het CSP, geen `fetch`, geen externe verwijzing, geen stuurtekens in de bron |
| `test_dossier` | opslaan, laden, wissen; een ander formaat wordt geweigerd; een andere bronversie geeft een melding |
| `test_uitdraai` | de besluiten uit de vakjes staan in de uitdraai, met de gespeelde scenario's en de ontbrekende maatregelen |
| `test_toegankelijk` | met `prefers-reduced-motion` geen animatie maar dezelfde eindtoestand; elke bediening haalbaar met tab en enter; elke statuskleur heeft een woord ernaast; contrast voldoet aan WCAG AA |

---

## 7. Wat dit niet doet

- **Geen risicoscore.** De game toont, het college oordeelt.
- **Geen koppeling met echte monitoring.** De statussen komen uit je eigen rapportages of uit een
  meting-export, niet uit een live systeem. De commons draait geen agent.
- **Geen persoonsgegevens in het dossier.** Het dossier bevat diensten, keuzes en besluiten, geen namen.
  In de uitdraai staat dat er expliciet bij, zodat niemand het als verwerkingsregister gaat gebruiken.
- **Geen nieuwe huisstijl.** De vorm die er is werkt in de raadzaal; dit plan raakt de inhoud, de
  bediening en de toegankelijkheid.

---

## 8. Stappen

1. **Bron eruit.** `spel.json` schrijven uit de huidige HTML: drie pijlers, negen diensten, negentien
   scenario's, alle maatregelen en complicaties. `haal_bron.py` doet de omzetting eenmalig en bewijst
   met `--check` dat de bron gelijk is aan wat er stond. Dit is het meeste werk; reken op een sessie.
   Klaar als `test_bron` groen is en de pagina uit `spel.json` hetzelfde doet als nu.
2. **Bouw en CSP.** `bouw.py` en `bron/` als bij procescheck; de bestaande HTML wordt de sjabloon.
   Klaar als de gebouwde pagina de twaalf bestaande browsertests haalt.
3. **Vertrouwelijkheid.** Het scenariotype `datalek`, het veld `gegevens` per dienst, de zijbalk die
   daarop reageert, en per dienst een lek-scenario. Klaar als `test_scenario` groen is.
4. **Dossier, besluitvakjes en uitdraai.** Klaar als `test_dossier` en `test_uitdraai` groen zijn.
5. **Imports** uit procescheck en de zelfcheck.
6. **Toegankelijkheid.** Reduced motion, toetsenbord, `aria-live`, contrast. Klaar als
   `test_toegankelijk` groen is.
7. **Drie diensten erbij** (hoofdstuk 10), nu de bron data is en dat een blok JSON is.
8. **Afronden.** LEESMIJ, verantwoording, README, ROADMAP opschonen (fase 2 en 3 zijn hiermee gedekt),
   `BESLUITEN.md`, en de projectentabel.

Schatting: drie sessies, waarvan de eerste bijna helemaal opgaat aan stap 1.

---

## 9. Wat er in de eerste versie van dit plan niet klopte

Voor wie de vorige versie las, en als waarschuwing voor de volgende keer: een tool beoordelen op zijn
ontwerpnotitie is niet hetzelfde als hem doorlopen.

- De eerste versie zei "twee knoppen: *Simuleer incident* en *Activeer DR*". Er is een
  voorbereidingsfase met een budget, negentien scenario's en complicaties op een klok.
- De eerste versie stelde "vier scenario's in plaats van een knop" voor. Er zijn er al negentien; wat
  ontbreekt is niet het aantal maar de tweede schadesoort.
- De eerste versie stelde een presentatiemodus voor. Die bestaat.
- De eerste versie zei "geen uitdraai". Er is een printstylesheet die het scherm op papier zet; wat
  ontbreekt is dat er besluiten en gespeelde scenario's in staan.
- De eerste versie zei "negen diensten in vijf ketenstappen met de SPOF op k2". De SPOF verschuift per
  scenario, want elk scenario heeft zijn eigen keten.

---

## 10. Besluiten (03-09-2026)

De drie vragen die dit plan openliet, zijn beantwoord. Bas gaf de keuze uit handen; hieronder staat wat
er is besloten en waarom. Ze staan ook in `BESLUITEN.md` van de repo.

**1. De drie nieuwe diensten worden belastingen en invordering, vergunningen en toezicht, en
verkiezingen.** Na uitkering en paspoort raken die de meeste inwoners, en verkiezingen zijn periodiek
onvermijdelijk en politiek zichtbaar: een dienst waarvan het college de datum al kent, maakt het gesprek
concreet.

**2. De voorbeeldcijfers blijven, maar zichtbaar als voorbeeld, en je eigen organisatie begint leeg.**
Een demonstratie met alles op `onbekend` zegt een bestuurder niets. Tegelijk mag niemand per ongeluk de
cijfers van een andere organisatie aan zijn college tonen. Dus: de meegeleverde set draagt een balk
*voorbeeldcijfers, maart 2026* op het scherm en op de uitdraai, en zodra je een organisatienaam invult
staat alles op `onbekend`, met een knop om de voorbeeldcijfers bewust over te nemen.

**3. De naam blijft `weerbaarheid-game`; de ondertitel is scherper.** De repo wordt op 23 plekken buiten
zijn eigen map genoemd en de URL wordt gebruikt in bestuursgesprekken; een dode link bij een bestuurder
weegt zwaarder dan een naam die net niet klopt. Op 03-09 is de tool zelf hernoemd: hij heette op elk
scherm *Weerbaarheids-Dashboard*, en heet nu *Weerbaarheidsgame*, met in de titel *gespreksinstrument
voor college en directie*. Hernoemen van de repo kan alsnog bij de oplevering van v2, met een redirect.
