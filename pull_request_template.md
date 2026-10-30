<!--
Standaard PR-template voor alle repositories onder security-commons-nl.
Vul alleen in wat relevant is — velden die niet van toepassing zijn mag je weglaten.
-->

## Wat doet deze PR?

<!-- 1-3 zinnen. Wat verandert er functioneel? -->

## Welk probleem lost dit op?

<!-- Link naar issue (bv. "Closes #42") of korte beschrijving van het probleem -->

## Hoe is het getest?

- [ ] Unit tests toegevoegd of bijgewerkt
- [ ] Bestaande tests draaien (CI is groen)
- [ ] Handmatig getest — licht hieronder toe:

<!-- Bij gedragswijziging: beschrijf hoe je het hebt gevalideerd -->

## Checklist

- [ ] Documentatie bijgewerkt als gedrag zichtbaar is voor gebruikers (`docs/gebruik.md`, `docs/architectuur.md`, `docs/configuratie.md`)
- [ ] Geen persoonsgegevens of organisatie-specifieke informatie in de wijziging (gebruik [anonimizer](https://github.com/security-commons-nl/anonimizer-local) bij twijfel)
- [ ] Commit-messages beschrijven het *waarom*, niet alleen het *wat*
- [ ] Bij inhoud in de kennisbank: `python tools/build.py` gedraaid en wat hij maakte meegecommit (leesversies; een waarschuwing over `llms.txt` of `sitemap.xml` mag, die werkt de CI na de merge bij)
- [ ] Nieuw stuk in de kennisbank: veld `route` ingevuld (een route-id uit `routes.json`, of `geen`); bij een route ook de stap in `site/routes.json` van de site
- [ ] `site/routes.json` gewijzigd: in de kennisbank `python tools/haal_routes.py` gedraaid en de kopie meegecommit (na de merge van de site)
- [ ] Instrument met status *in gebruik* gewijzigd: versie of peildatum op de pagina bijgewerkt; tests in CI groen (statuut C5)
- [ ] Code die het profiel leest of schrijft: alleen antwoord-id's uit `profiel.json`, geen naam of vrije tekst
- [ ] Nieuw project: opgenomen in `PROJECTEN.md` (voorpagina, `llms.txt` en sitemap volgen daaruit)
- [ ] Getallen in handgeschreven tekst (`ARCHITECTUUR.md`, roadmap) bijgewerkt of met peildatum
- [ ] Als deze PR de API, het schema of een zichtbare workflow wijzigt: overwogen of het breaking is en eventueel een migratienotitie toegevoegd
