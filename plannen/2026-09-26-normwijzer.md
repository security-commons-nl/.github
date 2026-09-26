# Bouwplan: de normwijzer, van norm naar handeling en terug

Vastgesteld 26-09-2026. Hoort bij [de crosswalk](2026-08-30-crosswalk.md), [normen](2026-09-02-normen.md) en
statuut B15 (verwijzen naar wat anderen al hebben).

## Waarom

De bouwstenen bestaan, maar de gebruiker moet ze zelf verbinden. Een maatregel in `normen` is een nummer
en een titel zonder adres. De crosswalk zegt welke barriere bewijs levert voor welke maatregel, maar wat je
eraan kunt doen staat in de kennisbank, en de ruim 380 stukken van IBD en CIP in het bronnenregister kennen de
norm niet. Van de 89 ISO-maatregelen in de BIO hebben er 44 een barriere; de rest is wit, terwijl juist daar
de handreikingen van de IBD liggen. En de omgekeerde vraag, "ik doe dit, welke norm is dat", kan alleen via
de zelfcheck.

## Het doel

Per maatregel een vast adres, met in deze volgorde: wat de norm vraagt (met een link naar de bron), wat je
eraan kunt doen (practices van het CIP, handleidingen uit de kennisbank, stukken van anderen), en welk bewijs
je dan hebt (de barrieres, met sterkte en reden). En een zoekvak voor de omgekeerde vraag: typ wat je doet,
zie de normen.

## Vorm

Een pagina `normwijzer.html` in de repo `normen`, met een adres per maatregel via het anker
(`/normen/normwijzer.html#bio2/8.5`). Een instrument in de zin van B14: alles zit in de pagina, er wordt
niets van buiten geladen. De data wordt bij het bouwen uit drie repo's gehaald (`normen`,
`aanvalspaden/mappingen`, `kennisbank`) en een geplande workflow houdt hem dagelijks bij.

Waarom een pagina en geen map met een pagina per maatregel: de gedeelde Pages-build kopieert losse bestanden,
en een anker is net zo goed te citeren en te delen.

## Fasen

| Fase | Wat | Stand |
|---|---|---|
| 0 | Adres per maatregel: BIO via BIO Practices (CIP), NIST via de CSF-referentietool van NIST, AVG via EUR-Lex, Wpg via de NOREA-handreiking | in uitvoering |
| 1 | De normwijzer: per maatregel de vier blokken, voor BIO, NIST, AVG en Wpg | in uitvoering |
| 2 | Stukken van anderen aan maatregelen hangen: de practices van het CIP per overheidsmaatregel, daarna voorstellen voor het bronnenregister die een mens afvinkt | practices in uitvoering, register open |
| 3 | De kennisbank praat terug: op elk stuk een blok *Bewijs voor* met de maatregelen op nummer | in uitvoering |
| 4 | Andersom: een zoekvak dat barrieres, handleidingen en stukken van anderen doorzoekt en de normen erachter toont | in uitvoering |
| 5 | De Cbw als ingang: per verplichting uit artikel 21 NIS2 de BIO-maatregelen, via de mapping NIS2 naar ISO 27002 die het CIP publiceert | later |

## Regels die blijven gelden

- De relatie is en blijft "levert bewijs voor", nooit "voldoet aan". De test die dat bewaakt, loopt ook over
  de normwijzer.
- Geen normtekst van ISO, NEN of het CIP op de pagina: nummer, titel, thema en een link.
- De mappingen zijn een voorstel tot een vakgenoot ze heeft getoetst; de pagina zegt dat.
- Elk adres gaat door de linkcheck.
