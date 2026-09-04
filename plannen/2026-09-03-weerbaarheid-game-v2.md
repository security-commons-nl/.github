# Bouwplan: de weerbaarheidsgame naar v2

**Status:** geschreven 03-09-2026, op verzoek van Bas ("werkt, maar nog niet optimaal; moderner, iets
uitgebreider"). De drie open vragen zijn dezelfde dag beantwoord (hoofdstuk 8), dus het plan is
uitvoerbaar; nog niets gebouwd. De game draait sinds maart 2026 live en wordt gebruikt
in bestuursgesprekken, dus dit is een verbouwing van iets dat werkt, geen herstart.

Geschreven om door een minder sterk model uitgevoerd te kunnen worden, in de vorm van
[het procescheck-plan](2026-09-02-procescheck-instrument.md) en
[het meting-plan](2026-09-03-meting.md). Waar hier "als bij procescheck" staat, is dat plan de
referentie.

---

## 1. Wat er nu staat

Eén bestand, `weerbaarheid-game.html`, 238 kB en 4.239 regels, met één `<script>` en één `<style>`.
Negen gemeentelijke diensten (crisis-alert, noodsteunpunten, lokale zorg, drinkwater, uitkering, afval,
paspoort, crisisbeheersing, informatievoorziening), elk met vijf ketenstappen k0 tot en met k4, met de
SPOF altijd op k2. Per dienst twee reactieve maatregelen en een preventieve, elk rood, oranje of groen.
Twee knoppen: *Simuleer incident* en *Activeer DR*. Een totaalscherm met alle diensten tegelijk.

Wat er goed aan is en dus blijft: het tandwielbeeld, de taal van de inwoner ("Uw paspoort is niet
beschikbaar") en het feit dat een bestuurder binnen tien seconden snapt wat hij ziet. De ontwerpnotitie
`weerbaarheid-game.md` is scherp en blijft de bron van de vorm.

Wat er niet goed aan is, feitelijk vastgesteld:

| Wat | Waarom het knelt |
|---|---|
| De negen diensten en alle statussen staan hard in de HTML | Een andere gemeente kan de game niet met haar eigen cijfers draaien zonder in code te editen. De statussen komen uit de rapportages van één organisatie, in maart 2026. |
| Alleen beschikbaarheid | De game kent één soort schade: de dienst valt uit. Een datalek, een onrechtmatige verwerking of een integriteitsprobleem komt niet voor. Voor een FG of een privacy officer is er niets te zien. |
| Geen dossier, geen uitdraai | Elk ander instrument in de commons levert een dossier en een A4 voor het college. Deze niet: na het gesprek blijft er niets over. |
| Losstaand van de keten | procescheck kent de processen en hun RTO, de zelfcheck en de meting kennen de barrieres. De game weet daar niets van, terwijl ze over hetzelfde gaan. |
| Geen CSP, geen tests, geen bron-vingerafdruk | De vaste vorm van de commons (statuut B14) vraagt dat wel; deze pagina is van voor die afspraak. |
| Animatie zonder rem | Geen `prefers-reduced-motion`, geen toetsenbordbediening. In een raadzaal met een beamer en een tolk is dat een probleem. |

---

## 2. Besluiten (de spec)

1. **De inhoud gaat uit de code naar `spel.json`.** Diensten, ketenstappen, maatregelen, scenario's en
   teksten worden data met een vingerafdruk, precies als `procescheck.json` en `meting/regels.json`. De
   negen diensten van nu worden het meegeleverde voorbeeld, herkenbaar als voorbeeld.
2. **Eén bestand blijft één bestand.** `bouw.py` zet bron, opmaak en script in `dist/index.html` met een
   CSP op sha256-hashes en `default-src 'none'`. Geen bundler, geen afhankelijkheden.
3. **De game krijgt een dossier.** `localStorage` plus een JSON die je opslaat en terugleest, met de
   organisatienaam, de peildatum, de eigen diensten en de statussen. Dezelfde vorm als de andere
   instrumenten, dus ook: laden weigert een ander formaat, en een andere bronversie geeft een melding.
4. **Vier scenario's in plaats van één knop.** *Uitval van een systeem* (wat er nu is), *ransomware*
   (meerdere ketens tegelijk, herstel duurt dagen), *leverancier valt uit* (alle diensten met dezelfde
   leverancier), *datalek* (de dienst draait door, maar de gegevens liggen op straat). Elk scenario
   heeft zijn eigen doorwerking en zijn eigen zin voor de inwoner.
5. **Naast beschikbaarheid komt vertrouwelijkheid.** Per dienst een tweede as: welke gegevens gaan er
   om, en wat is de schade als die uitlekken. Dat is het scenario datalek, en het maakt de game bruikbaar
   voor de FG. Geen aparte tool: dezelfde ketting, andere schade.
6. **De game leest uit de keten.** Drie importknoppen, allemaal optioneel: een procescheck-dossier
   (processen, kritiek ja/nee, RTO en RPO worden diensten met hun hersteltijd), een
   zelfcheck-uitslag of meting-export (de status van een barriere kleurt de bijbehorende maatregel), en
   een eigen `spel.json`. Zonder import werkt de game met het voorbeeld.
7. **Elk gesprek levert een A4.** Een uitdraai met wat er is gespeeld, welke diensten omvielen, welke
   maatregelen ontbraken en welke besluiten het college nam, met datum en organisatienaam. Print-CSS als
   bij de andere instrumenten.
8. **De game rekent geen risico's uit.** Geen score, geen rangorde, geen matrix. Hij toont een keten en
   laat zien wat er stukgaat; het oordeel is van het college. Dat was al zo en blijft zo, en het hoort
   expliciet in de verantwoording.
9. **Toegankelijk in een raadzaal.** `prefers-reduced-motion` respecteren (dan geen animatie maar
   stappen), alles met het toetsenbord bedienbaar, contrast volgens WCAG AA, en een presentatiemodus
   zonder bedieningselementen. Kleur is nooit de enige drager van betekenis: rood, oranje en groen
   krijgen ook een woord.
10. **De negen diensten blijven, en er komen er drie bij.** Belastingen en invordering, vergunningen en
    toezicht, en verkiezingen. Dat is geen willekeur: de eerste twee raken de meeste inwoners na
    uitkering en paspoort, en verkiezingen zijn periodiek onvermijdelijk en politiek zichtbaar.

---

## 3. Het bronformaat (`spel.json`)

```json
{
  "versie": "2026-09",
  "herkomst": "voorbeeld, gebaseerd op de continuiteitsrapportages van een gemeentelijke organisatie",
  "scenarios": [
    {"id": "uitval", "naam": "Systeem valt uit", "uitleg": "...", "raakt": "beschikbaarheid"},
    {"id": "ransomware", "naam": "Ransomware", "uitleg": "...", "raakt": "beschikbaarheid",
     "treft": "alle diensten met dezelfde host", "hersteltijd": "dagen tot weken"},
    {"id": "leverancier", "naam": "Leverancier valt uit", "raakt": "beschikbaarheid",
     "treft": "diensten met dezelfde leverancier"},
    {"id": "datalek", "naam": "Gegevens op straat", "raakt": "vertrouwelijkheid"}
  ],
  "diensten": [
    {
      "id": "paspoort", "naam": "Paspoort aanvragen",
      "inwoner": "Uw paspoort is beschikbaar",
      "inwoner_uitval": "Uw paspoort is niet beschikbaar. Geen alternatief.",
      "inwoner_datalek": "Uw persoonsgegevens uit de aanvraag liggen op straat.",
      "keten": [
        {"stap": "k0", "naam": "Baliemedewerker", "soort": "mens"},
        {"stap": "k1", "naam": "ID-verificatie", "soort": "proces"},
        {"stap": "k2", "naam": "BRP-koppeling", "soort": "systeem", "spof": true,
         "leverancier": "RvIG", "host": "datacenter"},
        {"stap": "k3", "naam": "Drukker", "soort": "keten"},
        {"stap": "k4", "naam": "Paspoort uitgifte", "soort": "dienst"}
      ],
      "gegevens": {"soort": "persoonsgegevens", "bijzonder": false,
                   "aantal_betrokkenen": "alle aanvragers", "schade": "identiteitsfraude"},
      "maatregelen": [
        {"id": "tijdelijk-reisdoc", "naam": "Tijdelijk reisdocument", "soort": "reactief",
         "status": "deels", "barriere": "fallback"},
        {"id": "rijksfallback", "naam": "Rijksfallback", "soort": "reactief", "status": "deels"},
        {"id": "continuiteitsplan", "naam": "Continuiteitsplan", "soort": "preventief",
         "status": "nee", "stap": "k4", "barriere": "crisis"}
      ]
    }
  ]
}
```

Drie afspraken bij dat formaat:

- **`status` is `ja`, `deels` of `nee`**, niet groen/oranje/rood. Kleur is presentatie; de bron zegt wat
  het is. Een maatregel zonder status is `onbekend` en toont grijs met het woord erbij.
- **`barriere` is de sleutel uit `paden.json`.** Alleen daarmee kan een zelfcheck- of meting-uitslag de
  maatregel kleuren. Een maatregel zonder barriere werkt gewoon, maar wordt nooit automatisch gevuld.
- **`host` en `leverancier` maken de scenario's mogelijk.** Ransomware treft alle diensten met dezelfde
  `host`; leverancieruitval alle diensten met dezelfde `leverancier`. Zonder die velden valt alleen de
  eigen keten om, zoals nu.

---

## 4. De pagina

Vier schermen, met de bestaande vorm als vertrekpunt.

**1. Overzicht.** De twaalf diensten als kaarten met een statusbol en de zin die de inwoner merkt. Boven
de kaarten de organisatienaam en de peildatum, en de knop *Eigen gegevens laden*.

**2. Keten (per dienst).** Het tandwielbeeld zoals het nu is, met per stap de soort (mens, proces,
systeem, keten, dienst) en de SPOF gemarkeerd. Rechts de maatregelen met hun status in woord en kleur.
Onderin de scenariokiezer: vier knoppen in plaats van de huidige twee, plus *Herstel*.

**3. Totaalbeeld.** Alle diensten tegelijk, met per scenario wat er simultaan omvalt. Dit is het
what-if-scherm dat er al is, met de drie nieuwe scenario's erbij. Bij *datalek* kleurt niet de keten
maar de gegevensbalk, met het aantal betrokkenen erbij.

**4. Uitdraai.** Organisatie en peildatum, wat er is gespeeld, welke diensten omvielen, welke maatregelen
ontbraken (`status: nee`), welke besluiten zijn genoteerd, en de bronversie met vingerafdruk. Print-CSS
op A4, `@media print` als bij de andere instrumenten.

**Besluitvakje.** Onder elk ketenscherm een tekstveld *Besluit van het college*. Wat daar staat komt in
de uitdraai. Dat is het verschil tussen een demonstratie en een vergaderstuk.

---

## 5. Tests

Als bij de andere instrumenten: een Python-referentie voor wat gerekend wordt, en de pagina ernaast.

| Test | Waarop |
|---|---|
| `test_bron` | `spel.json` valideert tegen het schema; elke dienst heeft vijf stappen en precies een SPOF; elke `barriere` bestaat in `paden.json`; elke `status` is ja, deels, nee of onbekend |
| `test_scenario` | ransomware raakt alle diensten met dezelfde host en geen andere; leverancieruitval idem; datalek raakt de gegevens en niet de keten; uitval raakt alleen de eigen keten |
| `test_import_procescheck` | een procescheck-dossier levert diensten met naam, kritiek en RTO; een dossier van een andere tool wordt geweigerd |
| `test_import_zelfcheck` | een `zelfcheck-antwoorden`-bestand kleurt de maatregelen met een barriere en laat de rest ongemoeid |
| `test_bouw` | een script, een stijl, hashes in het CSP, geen `fetch`, geen externe verwijzing, geen stuurtekens in de bron |
| `test_app` (Playwright) | een scenario spelen verandert de keten zoals de referentie zegt; het besluitvakje komt in de uitdraai; dossier opslaan, laden en wissen; met `prefers-reduced-motion` geen animatie maar wel dezelfde eindtoestand; alles bedienbaar met tab en enter |
| `test_toegankelijk` | elke statuskleur heeft een woord ernaast; contrast van de vier statuskleuren voldoet aan WCAG AA |

---

## 6. Wat dit niet doet

- **Geen risicoscore.** De game toont, het college oordeelt.
- **Geen koppeling met echte monitoring.** De statussen komen uit je eigen rapportages of uit een
  meting-export, niet uit een live systeem. De commons draait geen agent.
- **Geen persoonsgegevens in het dossier.** Het dossier bevat diensten en statussen, geen namen. In de
  uitdraai staat dat er expliciet bij, zodat niemand het als verwerkingsregister gaat gebruiken.
- **Geen nieuwe huisstijl.** De vorm die er is werkt in de raadzaal; dit plan raakt de inhoud, de
  bediening en de toegankelijkheid.

---

## 7. Stappen

1. **Bron eruit.** `spel.json` schrijven uit de huidige HTML (negen diensten, statussen, teksten), met
   `haal_bron.py` dat de omzetting eenmalig doet en met `--check` bewijst dat de bron gelijk is aan wat
   er stond. Klaar als `test_bron` groen is.
2. **Bouw en pagina.** `bouw.py` en `bron/` als bij procescheck; de bestaande HTML wordt de sjabloon.
   Klaar als de gebouwde pagina hetzelfde doet als nu, met CSP en zonder externe verwijzingen.
3. **Scenario's en de tweede as.** De vier scenario's, de gegevensbalk en de drie nieuwe diensten.
   Klaar als `test_scenario` groen is.
4. **Dossier en uitdraai.** Opslaan, laden, wissen, besluitvakjes, A4. Klaar als `test_app` groen is.
5. **Imports.** procescheck-dossier en zelfcheck-antwoorden. Klaar als de twee importtests groen zijn.
6. **Toegankelijkheid.** Reduced motion, toetsenbord, contrast, presentatiemodus.
7. **Afronden.** LEESMIJ, verantwoording, README, ROADMAP opschonen (fase 2 en 3 zijn hiermee gedekt),
   `BESLUITEN.md` van de repo, en de projectentabel: de game blijft *in gebruik*, maar de regel
   verwijst naar v2.

Schatting: drie sessies. Stap 1 en 2 zijn het meeste werk, want daar wordt 4.239 regels HTML uit elkaar
gehaald zonder dat het gesprek in de raadzaal erop achteruit gaat.

---

## 8. Besluiten (03-09-2026)

De drie vragen die hier open stonden, zijn beantwoord. Bas gaf de keuze uit handen; hieronder staat wat
er is besloten en waarom.

**1. De drie nieuwe diensten worden belastingen en invordering, vergunningen en toezicht, en
verkiezingen.** Na uitkering en paspoort raken die de meeste inwoners, en verkiezingen zijn periodiek
onvermijdelijk en politiek zichtbaar: een dienst waarvan het college de datum al kent, maakt het gesprek
concreet. Daarmee komt de game op twaalf diensten. Het formaat verandert er niet van; wie een dienst wil
toevoegen zet een blok in `spel.json`.

**2. De voorbeeldcijfers blijven, maar zichtbaar als voorbeeld, en je eigen organisatie begint leeg.**
Een demonstratie met alles op `onbekend` zegt een bestuurder niets: grijze tandwielen maken geen gesprek
los. Tegelijk is het risico reeel dat een CISO de game opent, hem aan zijn college laat zien, en de
statussen van een andere organisatie presenteert als de zijne. Daarom twee dingen:

- de meegeleverde set (`spel-voorbeeld.json`) draagt een balk bovenaan het scherm en op de uitdraai:
  *voorbeeldcijfers uit de rapportages van een gemeentelijke organisatie, maart 2026*;
- zodra je een organisatienaam invult, springt de game naar een lege set: alle statussen op `onbekend`,
  met de knop *voorbeeldcijfers overnemen* als je ze bewust als vertrekpunt wilt.

Zo blijft de demonstratie overtuigend en kan niemand per ongeluk andermans cijfers tonen.

**3. De naam blijft `weerbaarheid-game`; de ondertitel wordt scherper.** "Game" belooft inderdaad een
spel terwijl het een gespreksinstrument is, maar de repo staat op 23 plekken buiten zijn eigen map
genoemd (architectuur, projectentabel, kennisbank, llms.txt, sitemap, de voorpagina) en de URL
`/weerbaarheid-game/` wordt gebruikt in bestuursgesprekken. Een dode link bij een bestuurder weegt
zwaarder dan een naam die net niet klopt.

Wat wel verandert: op de pagina en in de projectentabel heet hij *weerbaarheidsgame, gespreksinstrument
voor college en directie*. Bij de oplevering van v2 kan de repo alsnog hernoemd worden, met een redirect
vanaf het oude pad; dan verandert het instrument toch, en is een nieuwe naam te verdedigen. Nu niet.
