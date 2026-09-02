# Bouwplan: de lichte commons (geen applicaties meer, alleen instrumenten die je opent)

**Doel:** elk project in de commons is iets wat een CISO opent, niet iets wat een organisatie installeert.
Geen server, geen database, geen accounts, geen gehoste staat. Wat dat niet haalt wordt omgebouwd naar de
vorm van de zelfcheck en de CSIR Assessment Tool; wat dat niet kan, neemt afscheid.

**Aanleiding:** de commons bewijst het zelf. Alles wat de afgelopen week live ging is client-side
(zelfcheck, normverankering, Cbw-toets, CSIR Assessment Tool); alles wat "prototype" of "concept" heet
heeft een backend. De IMS-pilot met VNG staat geparkeerd op de hostingdrempel, het codeplatform bij BZK
heeft geen CI/CD. De zware kant staat stil op infrastructuur, niet op inhoud. Van de twee anonimizers is de
Flask-versie gearchiveerd en leeft de browserversie. Een tool die een DPIA, een inkooptraject en een
beheerder vraagt voordat iemand hem kan proberen, haalt precies de drempel niet weg waarvoor de commons
bestaat.

**Architectuur:** een criterium (hoofdstuk 1), een vaste vorm (hoofdstuk 2), en per repo een oordeel
(hoofdstuk 3). Dit plan is de tweede rationalisatieronde: de eerste (28-08) ging over overlap, deze gaat
over het runtime-model. Elke ombouw krijgt daarna een eigen bouwplan; dit plan legt de volgorde en de
definitie van klaar vast.

**Status:** besluit van 02-09-2026, geschreven diezelfde dag. Fase 0 kan meteen; de ombouwen volgen in de
volgorde van hoofdstuk 4.

---

## 1. Het criterium

Een project in de projectentabel voldoet aan een van twee vormen:

1. **Instrument.** Een pagina op `security-commons-nl.github.io/<naam>/` die volledig in de browser
   rekent. Geen server, geen account, geen telemetrie, geen staat buiten het apparaat van de gebruiker.
   Dit is de norm en de enige vorm die in de projectentabel *Live tool* heet.
2. **Script.** Een programma dat lokaal draait op data die je al hebt, zonder server en zonder eigen
   opslag: een CLI die een export leest en een uitkomst schrijft. Staat in de tabel als *Leesbare versie*
   met een download, nooit als *Live tool*. Toegestaan waar een browser het niet kan (bestanden ophalen
   van buiten, batchverwerking, zware OCR), en dan zegt de README waarom.

Wat er niet meer in past: een applicatie met een backend, een database, authenticatie of gedeelde staat
tussen gebruikers. Zo'n project wordt omgebouwd naar vorm 1 of 2, of gearchiveerd.

**Eén uitzondering, met naam en toenaam:** `anonimizer-proxy`, een minimale Cloudflare Worker die een
AI-aanroep doorgeeft voor wie geen eigen sleutel heeft. Dat is infrastructuur (statuut B8), geen
project, en hij is opt-in: elk instrument werkt zonder. Een tweede uitzondering komt er alleen na een
besluit in `BESLUITEN.md`.

**Wat dit betekent voor het register.** De commons houdt geen risicoregister, geen ISMS en geen dossiers
bij. Elk instrument levert een dossier als JSON dat de gebruiker zelf bewaart en meeneemt naar zijn eigen
managementsysteem. Dat is geen gemis maar het punt: de commons levert de methode en het instrument, de
organisatie houdt haar eigen administratie.

## 2. De vaste vorm van een instrument

Drie keer gebouwd, drie keer hetzelfde gebleken (`aanvalspaden/check/`, `aanvalspaden/mappingen/`,
`csir-assessment-tool/register/`). Dit is de vorm; een nieuw instrument volgt hem, en een ombouw brengt
een bestaand project ernaartoe.

| Onderdeel | Regel |
|---|---|
| Bron | Eén JSON-bestand in git met de inhoud (vragen, regels, eisen, drempels), met herkomst en een vingerafdruk. De app bevat niets uit zichzelf; een test blokkeert als er toch een tekst of code in de app staat |
| Pagina | Eén HTML-bestand: bron en app in één scripttag, één stylesheet, Content-Security-Policy met de sha256 van beide en `default-src 'none'`. De pagina is ook de download |
| Rekenen | Een referentie-implementatie in Python naast de app in JavaScript, met dezelfde functienamen; de browsertests vergelijken de twee |
| Dossier | De invoer van de gebruiker als JSON-bestand dat hij opslaat en weer inleest, met de vingerafdruk van de bron erin, zodat een oud dossier tegen een nieuwe bron opvalt |
| AI | Alleen opt-in, met eigen sleutel of via `anonimizer-proxy`, nooit in dezelfde pagina als de rest, en met de waarschuwing erbij wat er dan het apparaat verlaat |
| Tests | Bron tegen origineel, bouw (CSP, geen externe verwijzing, herhaalbaar), app in Chromium; groen is de definitie van klaar |
| Uitleg | README, werkwijze en verantwoording via de gedeelde site-build op `/<naam>/uitleg/`; de tool zelf op `/<naam>/` |
| Statuut | Kruimelpad en voetregel (B10), README-kop (B11), status uit de projectentabel (B12), pagina op het domein (B13) |

De bouwplannen van de zelfcheck (`2026-08-28-aanvalspaden-keten.md`) en de CSIR-tool
(`2026-09-01-csir-keten.md`) zijn de uitgewerkte voorbeelden; een ombouwplan verwijst ernaar in plaats van
het opnieuw te beschrijven.

## 3. Oordeel per repo

Peildatum 02-09-2026, 23 repo's waarvan 3 al gearchiveerd. Grondslag per repo: wat er in de werkmap
staat, niet wat de README belooft.

### Voldoet al

| Repo | Vorm | Opmerking |
|---|---|---|
| `aanvalspaden` | instrument | zelfcheck en normverankering, het voorbeeld |
| `csir-assessment-tool` | instrument | het tweede voorbeeld |
| `anonimizer-browser` | instrument | TypeScript met een bouwstap, rekent in de browser |
| `weerbaarheid-game` | instrument | één HTML-bestand |
| `kennisbank` | kennis + instrument | de Cbw-toets is een instrument ín een item |
| `ai-gebruik-in-beeld` | kennis | draaiboek plus query's |
| `applicatiecheck` | instrument (concept) | ontwerp zegt het al: "in de browser, met de bron in JSON, geen server, geen account" |
| `policy-as-code` | concept | regels als JSON en een toetser in de browser is de logische vorm; nog geen code |
| `publicatiescan` | script | moet URL's ophalen en OCR draaien; dat kan een browser niet. Blijft CLI, zegt dat in de README |
| `anonimizer-local` | script | batchverwerking met eigen sleutel; de browserversie is het instrument |
| `security-commons-nl.github.io`, `.github`, `anonimizer-proxy` | infrastructuur | buiten de tabel (B8) |

### Ombouwen

| Repo | Nu | Wordt | Waarom dit de moeite is |
|---|---|---|---|
| `procescheck` | React + FastAPI + PostgreSQL + Azure AD | BIA en BIV per proces als één pagina, dossier als JSON | Het is een formulier met regels, precies het CSIR-patroon. En het ontsluit de koppeling object-onder-proces (`aanvalspaden#4`): twee JSON-dossiers die naar elkaar verwijzen op een sleutel. **Mede-auteur: Vasilis; afstemmen vóór het bouwplan** |
| `security-posture-tool` | FastAPI + SQLite, haalt zelf uit Entra, CSV-upload | **gaat op in** `aanvalspaden/meting/` (diepte 2): exports inlezen in de browser, bevindingen op `paden.json`, in de bewijs-vorm van applicatiecheck | Besluit 28-08 zei al: verhuist naar `aanvalspaden/meting/`. Aangescherpt 02-09: geen eigen repo meer; de eigen `architecture.md` (rule engine, connectors, zeven lagen) is oogst voor het meting-plan, niet het ontwerp ervan. De Entra-koppeling vervalt; de gebruiker exporteert zelf |
| `blast-radius` | Python CLI, graaf uit een CI-export | **gaat op in** `procescheck`: de landschapsexport als import, de keten proces → applicatie → component als tab en uitdraai | Aangescherpt 02-09. De vraag "wat valt er om" is cascade, en cascade woont bij de processen; de risicoanalyse-methode wijst blast-radius al toe aan stap 1 (kroonjuwelen, systemen eronder). Repo archiveren zodra procescheck live is |
| `iamscan` | Python CLI, leest een Linux-dump | **gaat op in** `aanvalspaden/meting/`: de Linux-dump als bron, de regels op AP05 en AP11 (tier-0, service-accounts, lokale beheerrechten) | Aangescherpt 02-09. Eén vraag op één export is geen project maar een bron plus regelset. Repo archiveren zodra meting live is |

### Afscheid

| Repo | Wat het is | Waarom | Wat eerst |
|---|---|---|---|
| `grc-platform` | ISMS/PIMS/BCMS met tenants, RLS, AI-agents, 17 migraties | Wordt nooit één pagina; dit is de definitie van een applicatie. 0 sterren, 0 forks, 1 watcher: niemand buiten ons draait het | **Oogst:** de ISMS-stappen met `waarom_nu` en `uitleg` uit de seed-migraties (`003`, `005`, `008`) zijn kennis, geen code; beoordelen wat naar de kennisbank kan. **Gedaan 02-09:** kloon met volledige historie (555 commits, 19 branches) plus git-bundle en LEESMIJ in `X:\ARCHIEF\grc-platform*`; op GitHub gearchiveerd; tien levende verwijzingen bijgewerkt. Vasilis (59 commits) is op aanwijzing van Bas niet apart geïnformeerd. De oogst van de seed-inhoud is nog niet gedaan en kan altijd nog uit het archief |
| `cisochat` | Documentatie en ontwerp voor een vCISO-agent; geen code | Een agent is per definitie een gehoste applicatie met AI | **Verhuizen:** `data/bio2.json` is de bron van de normverankering (harde koppeling 2 in `ARCHITECTUUR.md`); die bron gaat naar `aanvalspaden/mappingen/bronnen/` en de koppeling draait om. `docs/vciso/research/` (tooling-onderzoek per CSF-functie) gaat naar het kennisbankitem `referenties-tooling`. Het vCISO-idee zelf blijft als issue `idee` |
| `hosting-bouwblokken` | Referentiearchitecturen en IaC om applicaties te hosten | Als de commons geen applicaties meer levert, is er niets meer te hosten | **Oogst:** de referentiearchitecturen zijn kennis; beoordelen of ze als item onder `security` in de kennisbank verder leven. Daarna archiveren. **Keuze aan Bas** (hoofdstuk 6) |

`dreigingsanalyse` staat niet op GitHub en blijft lokaal; geen actie.

## 4. Volgorde

Eerst afscheid, dan ombouwen. Afscheid ruimt verwijzingen op en maakt de projectentabel eerlijk; ombouwen
gaat op volgorde van wat het ontsluit.

**Fase 0. Vastleggen.** Deze regel in `BESLUITEN.md` (gebeurt met dit plan). Statuut B14 als voorstel via
issue op `.github` (de wijzigingsprocedure van het statuut), tekst in hoofdstuk 5. `ARCHITECTUUR.md`:
het criterium en de vorm erin, de groep Instrumenten herschreven, en de zin dat grc-platform het
risicoregister is eruit (die stond er sinds vanochtend en is met dit besluit onjuist). Vasilis wordt
niet apart geïnformeerd over grc-platform (aanwijzing Bas 02-09); voor procescheck wel, bij fase 4.

**Fase 1. grc-platform.** Oogst beoordelen → archiveren op GitHub → verwijzingen uit levende documenten
halen. Dat zijn er tien: `.github/ARCHITECTUUR.md`, `.github/CONTRIBUTING.md` (de rij "Feedback op het
GRC-platform"), `.github/profile/README.md` (naar de alinea Gearchiveerd), `CLAUDE.md` van de werkmap
(sectie en routingregel "ISMS/PIMS/BCMS ... → grc-platform"), `kennisbank/security/risicoanalyse-aanvalspaden/`
(regel 160: "een platform als grc-platform" wordt "je eigen managementsysteem"),
`weerbaarheid-game/ROADMAP.md` (fase 3, koppeling met de API: schrappen), `ai-gebruik-in-beeld/ROADMAP.md`
(regel 9), `applicatiecheck/README.md` (regel 57), `policy-as-code/README.md` (regel 45),
`security-posture-tool/README.md` (regel 61; vervalt bij de ombouw). De plannen en het besluitenlog
blijven staan: dat is historie.

**Fase 2. Repo `normen` en cisochat.** Besluit 02-09 (tweede regel in `BESLUITEN.md`): de normbronnen
krijgen een eigen dataset-repo `normen`. `bio2.json` verhuist daarheen (zonder het veld `iso_maatregel`),
samen met `nist-csf.json`, `wpg.json` en `avg.json` uit `aanvalspaden/mappingen/bronnen/`; de generatoren
en de vingerafdruk-bewaking draaien om, van `normen` naar elke afnemer. Eigen bouwplan:
`2026-09-02-normen.md`, uitgevoerd op 02-09 (applicatiecheck via `applicatiecheck#2`; cisochat archiveren volgt). Onderzoeksdocumenten
naar `referenties-tooling`. vCISO-idee als issue `idee` in `.github`. Archiveren. Routingregels in
`CLAUDE.md` die naar `cisochat\docs\vciso\research\` wijzen, naar het kennisbankitem.

**Fase 3. hosting-bouwblokken.** Keuze Bas 02-09: archief, zonder oogst. **Gedaan 02-09:** kloon plus bundle en
LEESMIJ in `X:\ARCHIEF\hosting-bouwblokken*`, op GitHub gearchiveerd, profiel en architectuur bij.

**Fase 4. procescheck → instrument.** Eigen bouwplan, met Vasilis. Bron: de BIA-vragen (B1-B8, I1-I7,
V1-V7 met onderbouwing), de MTPD/RTO/WRT/RPO-klassen uit `Docs/`, de businesscontext. Dossier: één proces
per bestand, of één organisatie met meerdere processen; dat is een ontwerpkeuze voor dat plan. Daarna
`aanvalspaden#4` uitvoeren: het object uit de CSIR-tool verwijst naar een proces uit dit dossier.

**Fase 5. Meting: security-posture-tool en iamscan gaan op in `aanvalspaden/meting/`.** Eigen bouwplan,
pas nadat applicatiecheck F1 heeft laten zien hoe de bewijs-vorm eruitziet (regels als data, parser per
bron, bewijssoorten, dossier); meting volgt die vorm en niet de eigen `architecture.md` van de posture-tool.
Bron: de 37 checklistitems met hun `pad` en `chokepoint` (`paden_map.py`), plus de iamscan-regels op AP05 en
AP11. Invoer: exports (CSV/JSON) uit Entra, Intune, nmap, Nessus, en de Linux-dump van `collect.sh`; geen
eigen ophalen. Uitkomst: bevindingen per chokepoint met bewijs, in de vorm van diepte 1. Daarna beide repo's
archiveren.

**Fase 6. blast-radius gaat op in procescheck.** Onderdeel van het procescheck-plan (fase 4): de
landschapsexport als import in het dossier, de keten proces → applicatie → component als tab en als
uitdraai. Geen eigen bouwplan; repo archiveren zodra procescheck live is.

**Fase 7. Diepte 1.** De matrix kroonjuwelen × clusters als instrument in `aanvalspaden`, met het dossier
van fase 4 als bron voor de rijen. Was al gepland (besluit 28-08); door dit plan is het per definitie
client-side.

## 5. Voorstel voor statuut B14

> **B14. Een project is een instrument of een script, nooit een applicatie.** Een instrument rekent
> volledig in de browser, zonder server, account of telemetrie, en is het enige dat in de projectentabel
> *Live tool* heet. Een script draait lokaal op data die de gebruiker al heeft, zonder server en zonder
> eigen opslag, en staat in de tabel als *Leesbare versie* met een download; de README zegt waarom het
> geen instrument is. Een applicatie met backend, database, authenticatie of gedeelde staat hoort niet in
> de commons. Infrastructuur die een instrument opt-in ondersteunt (B8) is de uitzondering en wordt met
> naam in `BESLUITEN.md` vastgelegd. Reden: een tool die een DPIA, inkoop en een beheerder vraagt voordat
> iemand hem kan proberen, haalt de drempel niet weg waarvoor de commons bestaat; wat je opent, gebruik je
> vandaag.

`repo-compliance.yml` krijgt er geen controle bij: of iets een server nodig heeft is niet uit een README
af te leiden. De projectentabel en dit plan zijn de controle.

## 6. Open bij Bas

1. **hosting-bouwblokken:** oogsten en archiveren, of laten staan als naslag?
2. **grc-platform, de oogst:** wil je dat ik de seed-inhoud (ISMS-stappen met uitleg) beoordeel op
   kennisbankwaarde vóór het archiveren, of is archiveren met de lokale kopie genoeg?
3. **Volgorde van fase 4 en 5:** procescheck eerst (ontsluit de risicokoppeling) of de posture-tool eerst
   (was al besloten)? Dit plan zet procescheck eerst.

## 7. Wat dit plan niet doet

- Geen framework, geen sjabloonrepo, geen gedeelde JavaScript-bibliotheek. De vorm staat in hoofdstuk 2 en
  in twee uitgewerkte bouwplannen; dat is genoeg om te kopiëren. Een gedeelde bibliotheek wordt een
  dependency, en dependencies zijn precies wat de vorm vermijdt.
- Geen herschrijven van wat al voldoet.
- Geen verwijderen van repo's. Archiveren is omkeerbaar en houdt de historie; de lokale kopie op `X:\`
  houdt de werkmap.

## Bronnen

`ARCHITECTUUR.md` (peildatum 02-09), `REDACTIESTATUUT.md` (B8, B13), `aanvalspaden/BESLUITEN.md`
(28-08: drie diepten; diepte 2 blijft voorlopig in security-posture-tool), `plannen/2026-08-28-portfolio-review.md`
en `2026-08-30-rationalisatie.md` (de eerste ronde), `applicatiecheck/README.md` (regel 45 en 92),
`security-posture-tool/v0.1/README.md` (Entra-pull, CSV-upload, SQLite), `cisochat/README.md` (status
concept) en `cisochat/data/bio2.json`, `hosting-bouwblokken/README.md`, `grc-platform` via de GitHub-API
(sterren, forks, bijdragers) en `backend/alembic/versions/` (seed-migraties), de stand van ATLAS van
01-09 (VNG-1 geparkeerd op de hostingdrempel; codeplatform zonder CI/CD).
