# Besluiten van de organisatie

Append-only. Elke wijziging aan het [redactiestatuut](REDACTIESTATUUT.md) of aan de opzet van de commons
krijgt hier een regel: datum, wat er is besloten, en waarom. Nieuwste bovenaan. Besluiten die alleen over
één repo gaan, staan in die repo.

Dit log begint op 29-08-2026, toen bleek dat het statuut er wel naar verwees maar het nergens stond.

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

**Nog te doen:** de inbrenger van de casus is over de verhuizing en de naam geinformeerd nadat het besluit
was genomen (statuut A4 gaat over publiceren; het stuk stond al gepubliceerd).

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
