# Besluiten van de organisatie

Append-only. Elke wijziging aan het [redactiestatuut](REDACTIESTATUUT.md) of aan de opzet van de commons
krijgt hier een regel: datum, wat er is besloten, en waarom. Nieuwste bovenaan. Besluiten die alleen over
één repo gaan, staan in die repo.

Dit log begint op 29-08-2026, toen bleek dat het statuut er wel naar verwees maar het nergens stond.

## 30-08-2026 · De volgorde van kennisbankitems is redactioneel (B4 aangevuld)

De overzichtspagina's sorteerden op mapnaam. Daardoor stond de awareness-sessie bovenaan omdat die met
een a begint, boven de Annex en de risicoanalyse. Het alfabet is geen oordeel.

Besloten: de volgorde staat als genummerde lijst onder `## Volgorde` in de README van de sectie, en
`tools/build.py` volgt die. Zelfde mechanisme als de projectentabel op de org-pagina (B9): één zichtbare
bron, te bespreken in een pull request. Een item dat in de lijst ontbreekt of een naam die niet bestaat
blokkeert de build, zodat een nieuw stuk niet stil onderaan belandt.

Twee alternatieven afgevallen. Een rangnummer in de frontmatter kan niet zonder B2 te wijzigen (gesloten
set van acht velden) en nodigt uit tot drift. Sorteren op statuslabel meet rijpheid, niet waarde, en kan
niet uitdrukken welk stuk het vlaggenschip is.

## 30-08-2026 · procescheck gaat naar EUPL-1.2; geen uitzondering in B5

Eén repo stond rood op de statuutcontrole: GPL v3, terwijl B5 EUPL-1.2 eist. Het auteursrecht ligt bij de
oorspronkelijke auteur, dus herlicentiëren was nooit een keuze van deze organisatie. Een eerdere poging om
het stil recht te zetten is daarom teruggedraaid.

De vraag is voorgelegd met de overweging erbij. EUPL-werk mag opgaan in een GPL-geheel, andersom niet.
Voegen we procescheck en `grc-platform` samen, dan wordt dat geheel dus GPL v3. De licentievraag en de
fusievraag zijn daarmee één vraag, en dat maakte het een keuze en geen formaliteit.

De auteur heeft de licentie zelf omgezet naar EUPL-1.2 en tegelijk een nieuwe versie gepubliceerd. De
statuutcontrole is groen. De overwogen uitzondering bij B5 komt er dus niet, en dat is winst: B5 blijft
absoluut (EUPL-1.2 voor alles), en een afwijkende licentie blijft een gesprek met de rechthebbende in
plaats van een uitzonderingsregel die de controle stiller maakt.

**Wat dit opent:** een samenvoeging met `grc-platform` kan nu zonder dat het geheel naar GPL kantelt. Die
afweging zelf staat nog open.

## 29-08-2026 · Een itempagina wijst naar zijn eigen bestanden (B3 en B10 aangevuld)

Aanleiding: de pagina van de awareness-sessie beschrijft een presentatie van veertig minuten en linkt hem
nergens. Het bestand staat er wel en is bereikbaar, maar alleen als je de URL zelf typt.

Twee oorzaken. De leesversies zijn gerenderde README's en misten de voetregel die de gegenereerde
overzichtspagina's wel hebben, dus vanaf een itempagina was er geen enkele route naar de bron: negen van
de elf pagina's kwamen niet verder dan het kruimelpad. En een bijlage die in de README als opmaakcode
staat in plaats van als link, verdwijnt op de site uit beeld.

Besloten: B3 eist voortaan dat wat in de map staat als link in de README én op de leesversie staat, en dat
verwijzingen bestaan en binnen de eigen repo blijven. B10 eist een bronvoet onder elke leesversie.
`tools/build.py` zet die voet, controleert de rest en blokkeert; `tools/test_build.py` test de controles.

Wat de nieuwe controle meteen vond: de presentatie en twee datasets stonden nergens als link, de
handleiding voor het blue team wees nog naar een bestandsnaam die na de B3-opruiming index.html heet, het
AI-beleid verwees een niveau te hoog waardoor licentie en kennisbank-link op de site doodliepen, en de
markdown-bron van de Annex en van het AI-beleid was vanaf hun eigen pagina niet te vinden.

**Wat hierbij opviel en niet is opgelost:** de leesversies komen uit drie verschillende renders (twee
sjablonen en een handgemaakte pagina) en er is geen script dat ze opnieuw maakt. Daardoor kan een
bijgewerkte README stil uit de pas lopen met de pagina, precies zoals bij het blue team gebeurde. Een
render-stap in `build.py` zou dat sluiten; dat is een eigen klus en een eigen besluit.

## 29-08-2026 · Handelingsperspectief wordt het kennisbankitem "Meten voordat je ingrijpt"

Het was het enige kennisstuk met een eigen repo en een eigen site-generator. Alle andere kennis staat in de
kennisbank en krijgt daar frontmatter met acht velden, een peildatum, een statuslabel, de statuutcontrole,
de anonimizer-scan, een kruimelpad en een leesversie; dit stuk had niets daarvan. Omvang was geen argument:
met 5.400 woorden is het kleiner dan twee bestaande items.

Ook de naam is mee verhuisd. "Handelingsperspectief" is standaardtaal in beleidsstukken en NCSC-adviezen,
zegt niets over het onderwerp en kwam in de tekst zelf geen enkele keer voor. De andere kennisbankstukken
heten naar wat je gaat doen (Passkeys invoeren, Een blue team opzetten); "Meten voordat je ingrijpt" is de
eerste zin van de methode zelf en past in dat rijtje.

De acht hoofdstukken zijn een document geworden met een leeswijzer bovenaan; de zes KQL-query's staan als
bijlagen in `data/`. De oude repo is een doorverwijzing en daarna gearchiveerd, zodat gedeelde links en de
Pages-URL blijven werken.

**Wat bewust niet is samengevoegd:** de killchain-tabel bleef staan. Die volgt de volledige keten met alle
MITRE-fasen en is een andere snit dan AP09 in `paden.json`, dat vier barrieres toetst. In plaats van
verwijderen staat er nu een expliciete uitleg bij hoe de twee zich verhouden.

**Nog te doen:** de inbrenger van de casus moet nog worden bijgepraat over de verhuizing en de naam.
Statuut A4 gaat over publiceren en het stuk stond al gepubliceerd, dus dit hield de verhuizing niet tegen,
maar het gesprek hoort er wel bij.

## 29-08-2026 · dreigingsanalyse is geen repo van de organisatie

Bij de uitrol van de README-norm bleek dat `dreigingsanalyse` geen remote heeft en niet op GitHub staat:
het is een lokale map waarvan de inhoud is opgegaan in het kennisbankitem Risicoanalyse langs
aanvalspaden. Hij is daarom uit het profiel gehaald (de verwijzing gaf een 404 op de voorpagina), telt
niet mee in de statuutcontrole en hoeft niet gearchiveerd te worden.

**Waarom dit telt:** het profiel is de enige projectenlijst (B9). Wat daar staat, moet bestaan.

## 29-08-2026 · De voorpagina is voor de gebruiker; de werkplaats krijgt een norm die wordt afgedwongen

De landingspagina opende met een manifest en een repo-overzicht; een CISO die iets zoekt om vandaag te
gebruiken moest daar doorheen. Besloten: de voorpagina opent met wat je kunt doen, in de volgorde van de
gebruiker; het verhaal blijft hetzelfde en de bron blijft een bestand (B9, gepreciseerd). Tegelijk bleek
de documentatiestandaard zwaarder dan de praktijk (2 van 22 repo's voldeden) en werd hij daarom omzeild.
Vervangen door een README-kop die haalbaar is (B11), een status die op een plek woont (B12), een label
voor infrastructuur (B8), en een herbruikbare controle die dit afdwingt.
Bouwplan: `2026-08-29-bouwplan-voorpagina-en-werkplaats.md`.

## 29-08-2026 · De toolpagina is opgeheven

`/tools/` beschreef drie eigen tools (publicatiescan, iamscan, blast-radius) plus vier tools die er nog
niet waren. Dat botste met B9: de projectentabel op het org-profiel is de enige projectenlijst. De pagina
was bovendien een derde plek waar hetzelfde verhaal stond, naast de tabel en de README van elke repo, en
liep achter: de omschrijving in `llms.txt` noemde onderwerpen die niet op de pagina stonden.

De pagina is vervangen door een doorverwijzing naar de hoofdpagina, zodat een eerder gedeelde link niet
doodloopt. Wat alleen daar stond is bewaard: de grens "toetsen, niet aanvallen" is principe 11 geworden,
en de vier richtingen die in voorbereiding zijn staan onder Meedoen op het profiel, met de zin erbij dat
een tool pas bestaat als hij in de tabel staat.

**Aanleiding:** een lezer die niet kon zien wat die pagina was, en of het over eigen of externe tooling
ging. Dat onderscheid is nu expliciet: eigen tools in de projectentabel, tooling van anderen in het
kennisbankitem Externe referenties, waar het profiel nu ook naar verwijst.

## 29-08-2026 · B10, elke pagina wijst terug

Twaalf van de vijftien pagina's op Pages hadden geen enkele link terug naar de hoofdpagina, en geen van de
kennisbankitems verwees naar zijn eigen vakgebied. Wie via een zoekmachine op een diepe pagina binnenkomt,
kwam daar dus niet verder.

Regel B10 toegevoegd: elke pagina begint met een kruimelpad naar de hoofdpagina en naar het niveau
erboven. In de kennisbank zet `tools/build.py` het kruimelpad automatisch en maakt `--check` het rood als
het ontbreekt of verouderd is; in een losse tool staat het in de eigen opmaak.

## 29-08-2026 · B3 wordt gecontroleerd, en een leesversie verwijst niet naar zichzelf

B3 eist al sinds het begin een HTML-leesversie bij elk tekstitem, maar niets controleerde dat. Twee items
hadden er geen, en een verwijzing naar zo'n item liep dood op een 404. `tools/build.py` controleert dit nu.

Daarnaast haalt de build de regel "lees dit online" uit de gegenereerde leesversie. Die hoort in de README,
waar hij de lezer op GitHub naar de leesversie wijst, maar op de leesversie zelf was het een link naar de
pagina waar je al stond.
