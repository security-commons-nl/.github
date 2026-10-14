# Plan: de beleidsset op maat, gegenereerd uit contextvragen op BIO 2.0

Vastgesteld 12-10-2026, herzien 14-10-2026 (zie *Herziening*). Werkt stap 8 van
[de ingang en de vulling](2026-09-28-ingang-en-vulling.md) uit (tweede herkomst). Waar een AI-agent het stuk
afmaakt, is dat de agent van de gebruiker zelf, met een eigen sleutel bij een eigen leverancier: het patroon
van [AI-hulp met eigen sleutel](2026-09-03-ai-hulp.md). De commons host geen agent (statuut B14).

## Herziening 14-10-2026

De beleidsset die op 12-10-2026 in de kennisbank kwam (kennisbank #60 en #64), is op 14-10-2026
teruggetrokken (kennisbank #74). De meeste stukken waren onder BIO 1 vastgesteld. Een toets ernaast die laat
zien wat ontbreekt, helpt een gemeente die moet toetsen, maar niet een gemeente die vandaag beleid nodig
heeft. Die heeft actuele stukken nodig.

Twee dingen veranderen daarom:

1. **De set komt terug op BIO 2.0.** Elk van de 21 domeinen krijgt een stuk dat op de overheidsmaatregelen
   van BIO 2.0 versie 1.3 is geschreven. De oude set, de IBD-templates en de toets zijn het bronmateriaal; de
   historie staat in git. Materiaal dat de IBD met gemeenten heeft gemaakt, wordt meegenomen zodra het er is.
2. **De contextvragen bepalen de tekst.** Eerst was het doel: varianten van verschillende organisaties naast
   elkaar, met de vragen als sorteerfilter. Nu wordt elk stuk zelf opgebouwd uit vaste regels en
   regelblokken die afhangen van het antwoord op een contextvraag. Wie de vragen beantwoordt, krijgt een
   eigen set. Varianten van andere organisaties blijven welkom, maar ze zijn niet meer de enige weg naar maatwerk.

Het generatiedeel is deterministisch: geen taalmodel, geen gehoste dienst, dezelfde antwoorden geven
dezelfde tekst. Dat houdt het toetsbaar en past binnen B14. Een taalmodel kan daarna het stuk afmaken
(stap 8), met de sleutel van de gebruiker.

## Hoe het werkt

Per domein staat in de kennisbank één **bouwsteen**: een markdownbestand met de beleidstekst, waarin

- elke beleidsregel eindigt op de nummers van de overheidsmaatregelen die hij invult, zoals `[8.13.01]`;
- een blok `::: als hosting=saas` tot `:::` alleen meekomt bij dat antwoord;
- een invulveld `[[eigenaar back-up: de rol die de back-up bewaakt]]` zegt wat de organisatie zelf moet invullen.

Een generator zet een profiel (de antwoorden op de zestien vragen uit `profiel.json`) en de bouwstenen om in
een beleidsset. Zonder antwoorden levert hij de leesversie: alle blokken, elk met de vraag en het antwoord
waar het bij hoort. Dat is de ingang *bladeren*; de vragen blijven een filter, geen poort.

De generator bestaat twee keer: in Python voor de build en de tests, in JavaScript voor de pagina waar de
gebruiker de vragen beantwoordt en de set downloadt. Een spiegeltest houdt ze gelijk.

**De toets is een test.** Voor elk mogelijk antwoordprofiel op de vragen die een domein raakt, moet de
gegenereerde tekst elke overheidsmaatregel van dat domein met minstens één regel invullen. Ontbreekt er één,
dan faalt de build. Dekking is daarmee geen oordeel achteraf meer, maar een eigenschap van de bron.

## Stappen

| Stap | Wat | Resultaat | Stand |
|---|---|---|---|
| 1 | Toets, sjablonen en voorbeeld fysieke toegang | De eerste set, met de gaten zichtbaar | uitgevoerd 12-10-2026 (kennisbank #60), teruggetrokken 14-10-2026 |
| 2 | Profielschema: zestien contextvragen in `profiel.json` | Vragen met vaste antwoordruimte per domein | uitgevoerd 12-10-2026 (kennisbank #64); blijft |
| 3 | Bouwsteenformaat en generator (Python), met de dekkingstest per profiel | Een bouwsteen is te toetsen en om te zetten | open |
| 4 | De 21 bouwstenen schrijven op BIO 2.0 versie 1.3, met de oude set en de IBD-templates als bron | Een volledige set die elke overheidsmaatregel dekt, voor elk profiel | open |
| 5 | Generatorpagina (JavaScript) met spiegeltest; download per stuk en als geheel, in markdown en HTML | Een gebruiker beantwoordt de vragen en krijgt een eigen set | open |
| 6 | Terug online in de kennisbank, met `llms.txt`-regels zodat een eigen AI-agent bouwstenen en profiel vindt | Ook een agent kan de set op maat maken | open |
| 7 | IBD-materiaal en stukken van andere organisaties verwerken als regel of blok in de bouwsteen | Meer dan één herkomst | doorlopend |
| 8 | AI-hulp bij het afmaken van de invulvelden volgens [AI-hulp met eigen sleutel](2026-09-03-ai-hulp.md) | Wie geen eigen agent heeft, krijgt dezelfde hulp | open |

## Randvoorwaarden

- Eén indeling: de 21 thema's uit `bio2.json` van de normen-repo (het veld `thema`), dezelfde als het
  controleraamwerk en het [plan van aanpak BIO 2.0](https://security-commons-nl.github.io/kennisbank/governance/bio2-implementeren/).
- De tekst van de overheidsmaatregelen wordt niet overgenomen (CIP, CC BY-NC-SA), van de ISO-tekst ook niet.
  Een regel zegt wat de organisatie doet, in eigen woorden; het nummer verwijst naar de bron.
- Herkomst als organisatietype, nooit als naam (statuut).
- Een vraag die een domein raakt, moet in dat domein ook tekst veranderen. Een vraag die nergens tekst
  verandert, gaat uit het profiel of krijgt het doel *matching*.

## Wat dit niet is

Geen poort: zonder antwoorden is alles te lezen. Geen taalmodel dat beleid schrijft: de generator stelt
vaste tekst samen, de organisatie vult in en stelt vast. Geen tweede indeling naast de 21 domeinen. Geen
vervanging van de IBD-templates; die blijven een bron.
