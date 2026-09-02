# Redactiestatuut security-commons-nl

Vastgesteld 28-08-2026, B3 en B10 aangevuld op 29-08-2026, B4 op 30-08-2026, A11 toegevoegd op 31-08-2026, B13 op 02-09-2026. Geldt voor alle repo's van de organisatie. De inhoudsregels (A) gelden overal
letterlijk; de structuurregels (B) gelden overal in vorm, met per repo één afspraak over wat de eerste
laag betekent (zie B1). Waar een repo een script heeft dat deze regels controleert, verwijst elke melding
naar het regelnummer hieronder.

Dit statuut vult [PRINCIPLES.md](PRINCIPLES.md) (waarom we dit doen), [CONTRIBUTING.md](CONTRIBUTING.md)
(hoe je bijdraagt) en [DOCUMENTATION-STANDARD.md](DOCUMENTATION-STANDARD.md) (documentatie bij software) aan.

## A. Inhoud

**A1. Geen auteursvermelding.** Alles hier komt van vakgenoten; dat hoeft er niet bij. Geen namen, geen
"vakgenoot", geen "aangedragen door", geen `auteur:` in frontmatter, geen kopje "Auteur". Wat wel mag:
de herkomst als rol of organisatietype, als dat de lezer helpt ("in gebruik bij de CISO-organisatie van een
gemeente"). Wie deelt, hoeft daar zijn naam niet aan te verbinden. Dat verlaagt de drempel voor iedereen.

**A2. Persoonsnamen in de inhoud.** Alleen publieke functionarissen in hun publieke hoedanigheid (een
minister, een directeur van een instituut, een wethouder in een citaat uit een publiek stuk). Alle anderen
worden een functiebeschrijving. Fictieve namen in lesmateriaal mogen, met de vermelding "verzonnen".

**A3. Organisatienamen.** Publiek bekende casussen en bronnen mogen (een gemeente in een publiek
incidentrapport, NCSC, AP, VNG, IBD). De organisatie waar een stuk vandaan komt wordt nooit genoemd, tenzij
die organisatie zelf publiceert of schriftelijk instemt. De eigen organisaties van bijdragers worden nooit
als herkomst genoemd.

**A4. Toestemming.** Andermans werk alleen met toestemming van de auteur. De toestemming zelf staat niet in
de repo; wel de zin "gedeeld met toestemming". Waar de toestemming is vastgelegd bepaalt de plaatser, en
dat is nooit git.

**A5. Links.** Externe links alleen naar instituties, normen, wetten, overheidspublicaties, GitHub-repo's en
gedocumenteerde tooling. Geen links naar sociale media (LinkedIn, X, Substack, Medium, Facebook, Instagram),
persoonlijke blogs of profielen. Een bron van sociale media wordt tekst: "via LinkedIn", zonder link en
zonder naam. Interne links relatief, zodat ze op GitHub en op de website werken.

**A6. Datums.** Alleen een datum die de geldigheid van de inhoud bepaalt: `peildatum` (dataset,
dreigingsbeeld) of `versie` (document dat de bron zelf nummert). Die staat in de frontmatter, formaat
`JJJJ-MM-DD` of `JJJJ-MM`. Geen "opgenomen op", "gevonden op" of "aangedragen op" in de tekst; dat is
git-metadata. Een changelog in een README ("bijgewerkt na review") mag, omdat die over de inhoud gaat.

**A7. AI-gebruik.** Wordt niet per stuk vermeld; dat is consistent met A1. Wat wel geldt: een mens heeft
elk stuk gelezen en begrepen voordat het op `main` staat. Principe 4 (AI is adviserend) blijft leidend.

**A8. Git-historie.** Wordt niet herschreven om namen of herkomst te verwijderen; fix vooruit in een nieuwe
commit. Uitzondering: persoonsgegevens van derden of geheimen (sleutels, wachtwoorden). Dan wél
history-rewrite, rotatie van het geheim, en een regel in het besluitenlog van de repo.

**A9. Interne stukken.** Documenten van de eigen organisaties (pdf's, xlsx, interne memo's) komen in geen
enkele repo, ook niet "even tijdelijk". Eerst anonimiseren tot een sjabloon of casus, dan pas plaatsen.

**A10. Taal.** Nederlands. Engelse vaktermen blijven Engels (SSDLC, passkeys, red teaming, blue team).

**A11. Vragen.** De commons publiceert niet alleen wat we weten, ook wat we zoeken. Een vraag valt
onder dezelfde inhoudsregels als een gedeeld stuk: geen naam nodig (A1), personen worden functies (A2),
en de organisatie van de vrager wordt nooit genoemd (A3). Vragen onder een schuilnaam mag expliciet en
hoeft niet te worden toegelicht; in dit vakgebied is een hulpvraag ook een uitspraak over wat je zelf
nog niet geregeld hebt, en die drempel hoort niet bij ons te liggen. **Om dezelfde reden beschrijft een
vraag het vraagstuk op sectorniveau en nooit de situatie van een organisatie, ook niet die van onszelf.**
Geen "wij hebben dit niet opgelost" en geen "daar hebben we weinig van": dat is voor wie kwaad wil een
kant-en-klare inventarisatie. Schrijf wat er in het veld ontbreekt, en beschrijf de eigen positie alleen
in wat er al gedeeld is. Nodig een lezer ook niet uit om zijn eigen gaten te benoemen. Wat een vraag wel moet bevatten:
waar je zelf al staat, wat je zoekt, en wat er met het antwoord gebeurt. Zonder dat laatste weet
niemand waarom hij zou antwoorden. Een beantwoorde vraag verdwijnt niet maar wijst naar het stuk dat
eruit voortkwam; dat is het bewijs dat het werkt. Een vraag die een jaar open staat wordt herschreven
of weggehaald, want een lijst met onbeantwoorde vragen leest binnen een half jaar als een kerkhof.

## B. Structuur

**B1. Item = map met README.** Elk stuk is precies één map met een `README.md`, exact twee lagen diep:
`categorie/item/`. Wat "categorie" betekent, staat per repo vast:

| Repo | Eerste laag |
|---|---|
| kennisbank | vakgebied: `security`, `privacy`, `bcm`, `governance`; items van type `handleiding` dragen `barrieres:` uit `paden.json` en zijn de bron van het handelingsperspectief |
| dreigingsanalyse | maandversie (`vJJJJ.MM`) |
| aanvalspaden | `check/` (de zelfcheck), `methode/`, `meting/` (volgt); `paden.json` op de root is de bron |
| overige repo's | volgt `DOCUMENTATION-STANDARD.md` (software) of één regel in de eigen README |

Geen losse bestanden in een categorie-map behalve `README.md` en gegenereerde `index.html`. Geen derde laag.
Mapnamen: kleine letters, cijfers en koppeltekens; geen spaties, geen versies of woorden als "definitief".

**B2. Frontmatter, acht velden, vast.** Elke item-README begint met:

```yaml
---
titel: Leesbare naam van het item
vakgebied: security | privacy | bcm | governance      # per repo: de eerste-laag-waarde
type: beleid | sjabloon | lesmateriaal | dataset | referentie | aanpak | rapportage | handleiding
normen: [BIO2, ISO 27001, AVG, NIS2, CRA, AI Act, GIBIT 2025, ISO 22301]   # mag leeg: []
peildatum: JJJJ-MM-DD          # óf versie: "1.3 (herzien BIO2), 2026-08"; één van beide
herkomst: rol of organisatietype, geen naam
status: concept | in gebruik | sjabloon | gearchiveerd
samenvatting: twee tot vier zinnen; dit wordt de kaarttekst op de website
---
```

`auteur` bestaat niet (A1). `licentie` alleen als het item afwijkt van EUPL-1.2 (B5). Bij type
`handleiding` komen daar drie velden bij: `barrieres` (verplicht, `vraag_id`'s uit `paden.json`),
`rol` (`fundering`, `alternatief` of `verdieping`) en `pijler` (het item waar de handleiding uit
voortkomt). Andere velden niet.

**B3. Bestandsvormen.** Markdown is de bron. Elk tekstitem heeft daarnaast een self-contained HTML-leesversie
(geen externe fonts of scripts, print op A4, plakbaar in Word). Binaire bestanden (docx, pptx, xlsx, pdf)
alleen als er geen redelijke markdown-vorm is, en dan met een README die zegt wat erin zit.
Wat in de map van een item staat, staat als **link** in de README en op de leesversie. Een bijlage die
alleen als bestandsnaam wordt genoemd, bestaat niet voor een lezer die op de pagina binnenkomt: hij ziet
de beschrijving en kan er niet bij. Verwijzingen wijzen naar bestanden die bestaan en blijven binnen de
eigen repo. In de kennisbank blokkeert `tools/build.py` op alle drie.

**B4. Indexpagina's worden gegenereerd.** De overzichtspagina's (`index.html` per categorie en op de root)
zijn output van een script dat eerst alle regels controleert en dan bouwt. Handmatig bewerken is
zinloos: de volgende run overschrijft. Het script blokkeert bij elke overtreding en noemt bestand, regel
en regelnummer. Het draait lokaal vóór een commit en als GitHub Action bij elke push naar `main`.
De **volgorde van de items** op die pagina's is redactioneel en staat als genummerde lijst onder
`## Volgorde` in de README van de sectie. Alfabetisch sorteren zet toevallige mapnamen bovenaan; deze
lijst zet er een oordeel in: wat je morgen kunt toepassen bovenaan, naslag in het midden, verwijzingen
naar het werk van anderen onderaan. Zelfde principe als B9 voor de projectentabel. Ontbreekt een item in
de lijst, of staat er een naam die niet bestaat, dan blokkeert de build.

**B5. Licentie.** EUPL-1.2 voor alles. Wijkt een bron af (CC-BY, MIT, "alleen met toestemming"), dan is
`licentie:` in de frontmatter verplicht en staat er een zin in de README.

**B6. Commits.** Nederlands, één onderwerp per commit, map als prefix: `security: Security Annex toegevoegd`.
Geen AI-attributie of sessie-verwijzingen in de commitboodschap (A7).

**B7. Bijdragen.** Een issue of discussion is een volwaardige bijdrage; maintainers zetten het om. "Maak maar
een PR" is nooit het antwoord.

**B8. Statuslabels.** Elk project draagt precies één van vier labels, met deze criteria. Het label staat op
het org-profiel; dat profiel is de enige bron (B9).

| Label | Criterium |
|---|---|
| **in gebruik** | Draait echt (gehost, of geinstalleerd bij een organisatie) en heeft tests of CI die groen staan. Iemand gebruikt het vandaag. |
| **prototype** | Werkt en is te draaien, maar zonder belofte over volledigheid, onderhoud of ondersteuning. |
| **concept** | Ontwerp, plan of documentatie; geen werkende code. Ook een mockup valt hieronder. |
| **gearchiveerd** | Niet meer onderhouden. Blijft leesbaar, krijgt hooguit kritieke beveiligingsfixes. |

Bij twijfel geldt het lagere label. Een project dat zichzelf hoger labelt dan de criteria toelaten, is een
belofte aan een lezer die je niet waarmaakt.

Een repo die geen project is maar infrastructuur (een proxy, de site-build) draagt in zijn README het
label `infrastructuur`, staat niet in de projectentabel maar in de alinea "Onderliggende infrastructuur"
eronder, en wordt wel gecontroleerd op de README-kop en de licentie (B11, B5).

**B9. Het org-profiel is de enige projectenlijst.** `.github/profile/README.md` bevat de projectentabel; de
voorpagina, `llms.txt`, `sitemap.xml` en de root-`CLAUDE.md` worden daaruit gegenereerd of afgeleid. Een
project bestaat pas als het in die tabel staat, met label en doelgroep. De volgorde van de tabel is
redactioneel: de eerste drie rijen met een live link zijn de uitgelichte kaarten op de voorpagina. Repo's
die geen project zijn (infrastructuur, gearchiveerd, opgegaan in een ander project) staan in de alinea's
onder de tabel, met de reden erbij; `repo-compliance.yml` eist dat elke repo op een van die plekken staat.

**B10. Elke pagina wijst terug.** Elke pagina op Pages begint met een kruimelpad naar de hoofdpagina en
naar het niveau erboven, bijvoorbeeld: Security Commons NL > Kennisbank > Security > Passkeys invoeren. Een
losse tool krijgt minimaal Security Commons NL > naam van het project. Reden: veel lezers komen via een
zoekmachine binnen op een diepe pagina en moeten van daaruit de rest kunnen vinden. In de kennisbank zet
`tools/build.py` het kruimelpad automatisch en bewaakt `--check` dat het er staat; in een losse tool staat
het in de eigen opmaak. Elke leesversie **sluit af** met een voetregel naar de bronbestanden van dat item,
de licentie en de plek om een verbetering voor te stellen. Zonder die regel is een itempagina een
doodlopend eind: wel de tekst, geen route naar de map met de bijlagen, terwijl de gegenereerde
overzichtspagina's zo'n voet al hadden.

**B11. Elke repo heeft dezelfde kop.** De README van elke levende repo begint met: de naam als `#`-kop, een
zin wat het is en voor wie, een regel `Status: <label>.` met daarachter in gewone woorden wat werkt en wat
niet, en daarna de koppen `## Voor wie`, `## Snel starten`, `## Bijdragen` en `## Licentie`, in die
volgorde. Meer mag, minder niet. Een aparte `docs/`-map is alleen nodig als de README anders langer dan
ongeveer 1500 woorden wordt. Reden: een bezoeker die van de voorpagina doorklikt naar GitHub moet in tien
seconden zien wat het is, of het werkt en hoe hij begint. `repo-compliance.yml` controleert dit.

**B12. Status staat op een plek.** Het label in de projectentabel is de bron. De regel `Status:` in de
README van de repo herhaalt dat label letterlijk; `repo-compliance.yml` vergelijkt beide en wordt rood
als ze verschillen. Wie een status wijzigt, wijzigt eerst de tabel.

**B13. Elk project heeft een pagina.** Elke repo in de projectentabel publiceert een pagina op
`security-commons-nl.github.io/<naam>/`, ongeacht status. Minimaal is dat de leesversie van de README,
gebouwd met de gedeelde site-build; een tool of kennisbank publiceert zijn eigen pagina. De kolom *Direct
openen* in de projectentabel zegt wat een lezer aantreft: *Live tool*, *Leesbare versie* of *Ontwerp*; een
rij met alleen een ontwerp staat niet in de eerste drie rijen, want dat zijn de uitgelichte kaarten. Reden:
de site is de etalage, GitHub de werkplaats. Een project dat alleen op GitHub bestaat is onvindbaar voor
wie via de voorpagina of een zoekmachine binnenkomt, en een concept op de site nodigt uit tot meedenken.
Infrastructuurrepo's (B8) vallen buiten deze regel. De uitrol naar bestaande repo's staat in
[het plan van 02-09-2026](plannen/2026-09-02-elk-project-een-pagina.md).

## Wijzigen van dit statuut

Voorstel via issue of PR op deze repo (`.github`). Een wijziging krijgt een datum bovenaan en een regel in
[het besluitenlog van de organisatie](BESLUITEN.md). Scripts die regels controleren, worden in
dezelfde wijziging bijgewerkt.
