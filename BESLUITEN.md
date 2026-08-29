# Besluiten van de organisatie

Append-only. Elke wijziging aan het [redactiestatuut](REDACTIESTATUUT.md) of aan de opzet van de commons
krijgt hier een regel: datum, wat er is besloten, en waarom. Nieuwste bovenaan. Besluiten die alleen over
één repo gaan, staan in die repo.

Dit log begint op 29-08-2026, toen bleek dat het statuut er wel naar verwees maar het nergens stond.

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
