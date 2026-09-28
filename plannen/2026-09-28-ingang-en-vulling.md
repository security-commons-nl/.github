# Plan: de ingang en de vulling

Vastgesteld 28-09-2026. Volgt op [de bronnen](2026-09-25-bronnen.md) en [de normwijzer](2026-09-26-normwijzer.md).

## Waarom

De commons is de afgelopen weken breder geworden: een bronnenregister met bijna vierhonderd stukken van de
IBD, het CIP en het Rijk, een normwijzer met een adres per maatregel, een DPIA-werkwijze met sjablonen. Maar
wie binnenkomt op de voorpagina ziet daar weinig van. Er was geen zoekvak, de normwijzer stond nergens, de
kaart "Wat toon ik aan?" beschreef de normen als dataset voor bouwers, en de privacy officer stond niet in
de doelgroep. De inhoud is er; de ingang loopt achter.

Geen van de open plannen gaat over de ingang. Dit plan wel, en over het vakgebied dat het dunst gevuld is.

## Volgorde

De volgorde is die van de eigenaar: eerst vinden, dan vullen, dan de rest.

| Stap | Wat | Soort | Stand |
|---|---|---|---|
| 1 | **Zoekvak op de voorpagina.** Een vak voor de hele commons: instrumenten, kennisbank, normwijzer en de stukken van anderen, in groepen. | bouwwerk | uitgevoerd 28-09-2026 |
| 2 | **Privacy vullen.** De privacy officer in de doelgroep; wegwijzers naar wat er al ligt. | schrijfwerk | open |
| 3 | **De normwijzer op de voorpagina.** De kaart "Wat toon ik aan?" en vraag 3 van de keten wijzen naar de normwijzer; de normverankering gaat daarin op. | bouwwerk | open |
| 4 | **Een voordeur per rol.** CISO, ISO, privacy officer, bestuurder: per rol drie stukken om mee te beginnen. | bouwwerk | open |
| 5 | **Jaarritme.** Wat komt wanneer terug: ENSIA, de Cbw-meldplicht, de managementreview, de begroting. Per moment de stukken die helpen. | schrijfwerk | open |
| 6 | **Eerste honderd dagen.** Een route voor een nieuwe CISO of ISO: wat je in welke week doet, met de stukken erbij. | schrijfwerk | open |
| 7 | **Status eerlijker.** Veel stukken staan op concept terwijl ze in gebruik zijn; de status zegt nu te weinig. | redactie | open |
| 8 | **Tweede herkomst.** Bijna alle eigen stukken komen uit een organisatie. Een tweede bron per vakgebied maakt de commons van ons allemaal. | werving | open |

## Stap 1: het zoekvak (uitgevoerd)

Een vak bovenaan de voorpagina, voor de kaarten. De index is `normen/zoekindex.json`, gebouwd door
`tools/bouw_normwijzer.py` uit dezelfde bronnen als de normwijzer en elke nacht opnieuw: alle stukken van de
kennisbank (met samenvatting en vakgebied), het bronnenregister (met de zoekwoorden per partij, zodat "vng
beleid" de sjablonen van de IBD vindt) en alle maatregelen (met artikel, thema en trefwoorden). De
instrumenten leest het script uit de kaarten op de pagina.

Zoeken zoals in de kennisbank: accenten en koppeltekens tellen niet, elk woord moet voorkomen, korte woorden
alleen aan het begin van een woord, en de synoniemen uit het register. Een normnummer (`bio 8.5`) zet die
maatregel bovenaan. Treffers in vier groepen: instrumenten, kennisbank, normwijzer, bij anderen; per groep
acht, de rest achter een knop. Een zoekvraag in het adres (`?q=dpia`) is deelbaar.

Waarom de index bij de normwijzer en niet bij de kennisbank: de normwijzer voegt kennisbank, register en
normen al samen. Een tweede plek die dat doet, gaat vroeg of laat uit de pas lopen.

## Stap 2: privacy vullen

Het vakgebied privacy telt twee stukken, allebei over de DPIA. Werk:

- de privacy officer in de doelgroepregel van de voorpagina;
- wegwijzers volgens B15 voor het verwerkingsregister, datalekken, verwerkersovereenkomsten en de rechten
  van betrokkenen: kort, met de weg naar wat de IBD en anderen al hebben;
- de verwerking van uitgevoerde camera-DPIA's tot een maatregelencatalogus (fase O van
  [dpiacheck](2026-09-03-dpiacheck.md), issue [.github#20](https://github.com/security-commons-nl/.github/issues/20)).

## Tijdgebonden

Een paar klussen kunnen alleen zolang de bronnen bereikbaar zijn, tot half november 2026. Die gaan voor
bouwwerk dat altijd kan:

- fase O van dpiacheck (de camera-DPIA's);
- stap 6, eerste honderd dagen;
- de stelselkaart losmaken van de bron waar hij nu uit komt;
- de ronde langs de stukken achter inlog in het bronnenregister.
