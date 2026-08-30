# Portfolio-review security-commons-nl

Werkdocument, 28-08-2026. Niet in een repo: het noemt vindplaatsen van persoonsgegevens (bestand en regel).
Bron: drie verkenningen over alle 24 mappen onder `X:\SECURITY-COMMONS-NL`, read-only, plus de uitvoering
van stap A dezelfde dag. Toets: [redactiestatuut](.github/REDACTIESTATUUT.md) (A1-A10, B1-B7).

## 1. Kernbeeld

1. **"Actief" onderscheidt niets.** 13 van de 17 projecten op het org-profiel dragen dat label; `grc-platform`
   (527 commits, 4 CI-workflows, ~300 tests) en `ai-gebruik-in-beeld` (2 commits) krijgen dezelfde badge. De
   enige repo die zich "skelet" noemt (`security-posture-tool`) heeft tests én CI, maar de CI draait de tests niet.
2. **Het statuut werd op zeven publieke plekken overtreden**, inclusief het org-profiel zelf. Stap A heeft die
   opgeruimd (§4).
3. **Twee mappen zijn geen commons maar werk of LIVIQ**, niet gepubliceerd, wel op deze schijf:
   `kill-chain-analysis` en `jargon-tolk` (§5, stap B).
4. **Vijf overlap-clusters** waar hetzelfde twee of drie keer is gebouwd (§3).

## 2. Status per repo

Oordeel: klopt · te optimistisch · te bescheiden · onduidelijk. "Laatste commit" per 28-08-2026, vóór stap A.

| Repo | Claim | Werkelijk | Oordeel |
|---|---|---|---|
| grc-platform | Actief, "functioneel" | 527 commits, tests, 4x CI, stil sinds 27-05; README/ROADMAP noemen drie verschillende testtellingen | klopt, cijfers rommelig |
| kennisbank | Actief | 28-08 heringericht: statuut, build.py, Action | klopt |
| anonimizer-local | Actief | 43 commits, 116 tests, CI, 11-08 | klopt |
| anonimizer-browser | Actief, v0.1 | 82 tests, CI, Pages, 27-08 | klopt, eerder bescheiden |
| anonimizer-proxy | (infra, geen label) | 2 commits, mei; onduidelijk of live; browser-README biedt hem niet aan | onduidelijk |
| anonimizer-web | Gearchiveerd | klopt; ROADMAP spreekt het tegen; CI draait nog | klopt, opruimen |
| publicatiescan | geen label | 97 tests, org-CI, README 350 regels; ontbreekt in root-CLAUDE.md | te bescheiden |
| blast-radius | prototype v0.1 | tests (36), geen CI; tweeling van iamscan | klopt |
| iamscan | prototype v0.1 | tests (40), geen CI; tweeling van blast-radius | klopt |
| security-posture-tool | v0.1-skelet | 22 connectors, 10 testbestanden, CI met py_compile i.p.v. pytest; README beschrijft lege mappen | te bescheiden |
| kill-chain-analysis | levende bouw-agenda | geen git, stil sinds mei, werk-PII | werk-artefact |
| dreigingsanalyse | ter review, v2026.05 | 3 bestanden, nul inhoud, geen remote | te optimistisch |
| security-shop | mockup | 1 commit, mockup live op Pages | klopt, dunste actieve |
| cisochat | concept, geen code | 38 commits docs; ROADMAP spreekt README tegen | klopt |
| beleid-assistent | concept, "gebouwd en getest in productie" | 2 json, nul code, stil sinds 22-04 | te optimistisch |
| hosting-bouwblokken | in ontwikkeling | 10 Terraform-bestanden, eerlijke ROADMAP, stil sinds 22-04 | klopt |
| procescheck | Actief | 20 commits, geen tests, oude org, GPL, 15 binaire werkdocumenten | te optimistisch |
| weerbaarheid-game | Actief, live | één HTML met hardcoded data, live | klopt |
| Handelingsperspectief | Actief | schoon, Pages; README-titel nog "voor gemeenten" | klopt |
| ai-gebruik-in-beeld | Actief | 2 commits; ROADMAP al ingehaald | onduidelijk |
| policy-as-code | Idee | 1 commit, alleen README | klopt, voorbeeldig eerlijk |
| security-commons-nl.github.io | niet in lijst | infra; `llms.txt` beschrijft alleen Handelingsperspectief | klopt, verouderd |
| .github | "geldt voor alle repo's" | doc-compliance door 3 van 17 repo's aangeroepen | te optimistisch |
| jargon-tolk | concept, geen repo | één context.md | klopt; commons of LIVIQ? |

## 3. Overlap: vijf clusters

| Cluster | Wat dubbel is | Voorstel |
|---|---|---|
| PII-detectie | `anonimizer-local` (Python), `anonimizer-browser` (TS-port, "handmatig synchroon houden"), `publicatiescan` (eigen regex): BSN-elfproef, IBAN mod-97, e-mail, postcode drie keer | Eén gedeelde, geteste patronenspecificatie (JSON-fixture die beide suites inlezen). Repo's blijven. |
| Dreiging → dekking | `kill-chain-analysis` (tooling, werk-PII, geen git), `security-posture-tool` (tooling, tests, CI, heeft al `test_kill_chain.py`), `dreigingsanalyse` (docs, leeg) | Posture-tool is de drager. Kill-chain naar werk of geschoond als module erin. Dreigingsanalyse als bronlaag onder security-shop, of archiveren. |
| Advies-AI | `cisochat` en `beleid-assistent` (zelfde stack, beide nul code), `security-shop` (patronen, mockup); drie eigen BIO2-mappings; drie plekken die zero trust uitleggen | Beleid-assistent opgaan in cisochat als capability, `bio2.json` als gedeelde bron; security-shop de catalogus waar beide uit putten. |
| GRC-satellieten | `procescheck` (BIA/BIV, de laag onder grc-platform), `policy-as-code` (idee, wordt tweede normenmodel), `blast-radius` (laag onder procescheck) | Procescheck als module in grc-platform, daarna archiveren. Policy-as-code een discussion in grc-platform tot er één werkende regel is. |
| Site-build en rapport-skelet | `site/build.mjs` in Handelingsperspectief, ai-gebruik-in-beeld en github.io; rapportgenerator en `--ai`-laag in blast-radius en iamscan | Eén reusable workflow in `.github`; gedeelde rapportgenerator of één repo met twee subcommando's. |

Netto: van 17 vermelde projecten naar ongeveer 11 die elk iets eigens zijn, plus twee die geen commons zijn.

## 4. Stap A: statuut-overtredingen, uitgevoerd 28-08

Tien commits, tien repo's, gepusht. Tests groen waar ze bestaan (anonimizer-local 116, anonimizer-browser 82).

| Repo | Commit | Wat |
|---|---|---|
| .github | 52d42ea | LinkedIn-links uit org-profiel en SECURITY.md (A5) |
| anonimizer-local | fa5be68 (na rewrite) | fictieve namen in prompts en tests; **7 groundtruth-bestanden van echte beleidsdocumenten uit git én uit de historie** (namen van collega's, leveranciers, KVK, telefoon; A2, A8-uitzondering) |
| anonimizer-browser | be2378e | idem in prompt en fixtures (A2) |
| grc-platform | c3c3a03 | persoonsnaam uit ROADMAP, testmail, migratie-strings, preset (A2, A3) |
| weerbaarheid-game | da517bc | herkomstorganisatie uit CONTRIBUTING en ontwerp (A3) |
| hosting-bouwblokken | 2cbe971 | herkomst als organisatietype (A3) |
| dreigingsanalyse | 076b8c9 | auteursregels en mailadres weg (A1); geen remote |
| security-shop | 29acb45 | auteursregel weg (A1) |
| cisochat | f936a72 | vijf bronvermeldingen zonder naam en link (A2, A5) |
| procescheck | 7c59c8b | 15 binaire werkdocumenten weg (A9), licentie EUPL-1.2 (B5), `Vas-leiden` en prod-server weg (A3) |

Nagekomen bij A: de licentiewissel van procescheck is teruggedraaid (5eed981), het auteursrecht ligt bij de oorspronkelijke auteur; GPL v3 is de eerste B5-uitzondering.
GitHub kan onbereikbare objecten van anonimizer-local nog even cachen (support kan purgen).

## 5. Stap B: muur, uitgevoerd 28-08

Uitgevoerd na keuze van de eigenaar: B1a (integraal terug naar de tenant), B2a (naar LIVIQ), B3 (naar de tenant).
`kill-chain-analysis` → `Purple teaming Leiden - General\Tooling\kill-chain-analysis-aegis\` (184 bestanden);
`jargon-tolk\context.md` → `X:\LIVIQ\demos\jargon-tolk\`; `anonimizer-local\memory.json` (+ backups) en de echte
`standaard.yaml` → `Tooling\anonimizer-context\`. In de repo is `standaard.yaml` nu een sjabloon met
placeholders. Root-`CLAUDE.md` van de commons bijgewerkt (projecten, routing, werkafspraak "alleen commons").
Ook meegenomen: laatste sporen van de regio in publicatiescan-tests en -commentaar, LIVIQ-verwijzing in
cisochat-ontwerp, licentienoot in procescheck-README (GPL v3 blijft: auteursrecht bij oorspronkelijke auteur).

| Map | Wat erin staat | Voorstel |
|---|---|---|
| kill-chain-analysis | teamnamen, werkmail, opdrachtgever met functie, leverancier met contractnummer en live-gangdatum, OneDrive-paden uit de tenant, eigenaren in use-cases; geen git | ✅ Terug naar de tenant. Ooit publiceren: eerst `config/org.yaml` als enige plek voor organisatie-specifieks, README en CLAUDE.md schonen, `archive/` weg, dan git, met de bouwer erbij. |
| jargon-tolk | eigenaar bij naam, tweede naam, klantnaam (HHNK), LIVIQ-route, ATLAS-kaartverwijzing | ✅ Naar LIVIQ (`demos\jargon-tolk`). Bij een go als commons: eerst regel 4, 13, 69, 86 strippen. |
| anonimizer-local/memory.json | FG- en KVK-nummers en adressen van de vier gemeenten; correct in `.gitignore` | ✅ Naar de tenant (`Toolingnonimizer-context`), samen met de echte `standaard.yaml`; in de repo staat een sjabloon. |

## 6. Stap C: portfolio, uitgevoerd 28-08

Gedaan: statuslabels, org-profiel als bron, CI-uitrol, ROADMAP-opschoning, archivering.
Niet gedaan: de vijf samenvoegingen uit paragraaf 3 (zie "Wat open blijft" onderaan).

| Onderdeel | Wat er is gebeurd |
|---|---|
| Statuslabels (B8) | Vier labels met criteria in het statuut; alle 17 projecten opnieuw gelabeld. Van 13x "Actief" naar 8x in gebruik, 5x prototype, 4x concept, plus anonimizer-web als gearchiveerd. |
| Org-profiel als bron (B9) | `llms.txt` krijgt een gegenereerd projectenblok tussen markers; de handgeschreven secties (bronbestanden, datasets, KQL) blijven. `sitemap.xml` behoudt bestaande entries met geverifieerde lastmod en vult alleen aan. |
| Dode links | Twee links waren binnen een dag doodgegaan door de herindeling van vandaag (blue-team-hernoeming, `overig` naar `governance`). Gerepareerd, plus de Annex toegevoegd. |
| Linkcheck | Nieuwe workflow in github.io: elke URL in `llms.txt` en `sitemap.xml` moet 200 geven. Draait op push, PR en wekelijks. Vangt hernoemingen in andere repo's. |
| Leesversie heet index.html | De map-URL van een item gaf 404 omdat de HTML anders heette. Twee bestanden hernoemd; `kennisbank/tools/build.py` blokkeert het nu (B3). |
| CI uitgerold | blast-radius en iamscan: tests en doc-compliance via de org-workflows, plus CONTRIBUTING. Handelingsperspectief en ai-gebruik-in-beeld: doc-compliance, plus CONTRIBUTING. security-posture-tool: pytest in plaats van py_compile. |
| Twee bugs die de CI meteen vond | (1) `pytest tests/` vond het eigen pakket niet in blast-radius en iamscan; opgelost met `python -m pytest`. (2) security-posture-tool riep `TemplateResponse` aan met de oude Starlette-signatuur, verwijderd in Starlette 1.0: de app werkte niet met actuele dependencies. Negen aanroepen omgezet, 127 tests groen. |
| ROADMAPs | anonimizer-web: verwijderd (sprak het archief tegen). cisochat: vervangen door verwijzing naar de vCISO-blueprint. ai-gebruik-in-beeld: het "korte" punt was al opgeleverd. security-posture-tool: README en ROADMAP in lijn met de 29 connectors en 127 tests die er staan. |
| anonimizer-web | Stond al gearchiveerd op GitHub. Kort ge-unarchiveerd om de opschoning te pushen, daarna weer gearchiveerd. |
| Links naar `anonimizer` | De repo heet `anonimizer-local`; zeven bestanden verwezen nog naar de oude naam. |

### Samenvoegingen, uitgevoerd 28-08 (na akkoord: 1, 2, 3, 4; niet 5)

| # | Wat | Uitkomst |
|---|---|---|
| 1 | Site-build delen | Herbruikbare org-workflow `pages-docs.yml`; Handelingsperspectief en ai-gebruik-in-beeld roepen hem aan (caller van 10 regels). `build.mjs` in beide identiek, configuratie in `site/config.json`. Bijvangst: ai-gebruik-in-beeld had de meta-description van Handelingsperspectief en een dode link naar `draaiboek.md`; beide gefixt. Pages-builds groen. |
| 2 | Rapport-skelet blast-radius/iamscan | Gemeten overlap: `ai.py` 43%, `cli.py` 42%, `report.py` 8%. Geen bestand boven de drempel van 80%, dus geen code gedeeld (dat zou een extra repo of pip-dependency vragen voor vooral haakjes). Wel de conventies vastgelegd in beide CONTRIBUTING's: flag-kern, "AI doet de duiding, niet de cijfers", self-contained HTML. |
| 3 | PII-patronen als één specificatie | Canonieke fixture `anonimizer-local/tests/fixtures/pii-patronen.json` (76 gevallen, 9 categorieën, alleen fictieve data), kopie plus sha256 in anonimizer-browser en publicatiescan, per repo een test die de eigen detectie tegen de fixture zet en een sync-test op de hash. Suites groen: 193, 160, 199. De README-belofte "handmatig synchroon houden" is nu een test. |
| 4 | beleid-assistent in cisochat | Concept en architectuur naar `cisochat/docs/capabilities/beleidsassistent/`, `bio2.json` (148 controls) en `domeinen.json` naar `cisochat/data/` als gedeelde bron, capability-sectie in de cisochat-README. beleid-assistent: README verwijst door, repo gearchiveerd op GitHub, van het org-profiel naar de gearchiveerd-regel. |
| 5 | procescheck in grc-platform | Niet gedaan, op besluit van de eigenaar: eerst het gesprek met de auteursrechthebbende. |

policy-as-code blijft een eigen repo (besluit eigenaar: wordt binnenkort uitgewerkt).

### Wat open blijft na C

De vijf samenvoegingen uit paragraaf 3 zijn niet uitgevoerd. Het zijn beslissingen, geen opruimwerk:

1. **procescheck in grc-platform** en daarna archiveren. Het auteursrecht ligt bij de oorspronkelijke
   auteur; dit kan niet zonder diens instemming.
2. **beleid-assistent opgaan in cisochat.** Betekent een repo opheffen. `data/bio2.json` (148 controls)
   moet dan behouden blijven als gedeelde bron.
3. **PII-patronen als één geteste specificatie** voor anonimizer-local, anonimizer-browser en
   publicatiescan. Nu drie implementaties, met een handmatige sync-afspraak.
4. **Site-build als reusable workflow** in plaats van drie kopieën van `site/build.mjs`.
5. **Rapport-skelet delen** tussen blast-radius en iamscan, of samenvoegen tot één repo met twee
   subcommando's.

Afgehandeld: `dreigingsanalyse` is gearchiveerd en opgegaan in de nieuwe kennisbank-methode
**Risicoanalyse langs aanvalspaden** (`kennisbank/security/risicoanalyse-aanvalspaden/`, concept, 28-08).
Die methode is tegelijk de leeswijzer over de commons heen: per stap verwijst ze naar het project dat hem
invult, wat de samenhang levert die paragraaf 3 miste.


### De oorspronkelijke voorstellen

1. **Vier statuslabels met criteria**: *in gebruik* (tests+CI of gehost, én in gebruik) · *prototype* (werkt,
   geen belofte) · *concept* (docs, geen code) · *gearchiveerd*. Toewijzing op basis van §2.
2. **Org-profiel wordt de enige bron.** `llms.txt`, `sitemap.xml`, `tools.md` en root-`CLAUDE.md` worden eruit
   gegenereerd, zoals de kennisbank-index uit frontmatter. Root-`CLAUDE.md` mist nu publicatiescan, blast-radius,
   iamscan en jargon-tolk en noemt `anonimizer/` waar de map `anonimizer-local` heet.
3. **De vijf samenvoegingen uit §3**, in volgorde van laagste risico: site-build delen · rapport-skelet delen ·
   PII-patronen delen · beleid-assistent in cisochat · procescheck in grc-platform.
4. **CI uitrollen**: `python-ci` en `doc-compliance` uit `.github` aanroepen in blast-radius, iamscan,
   security-posture-tool (pytest i.p.v. py_compile), Handelingsperspectief, ai-gebruik-in-beeld.
5. **ROADMAPs** die achterlopen of tegenspreken (anonimizer-web, cisochat, ai-gebruik-in-beeld,
   security-posture-tool): bijwerken of verwijderen. Regel: alleen een ROADMAP als er iets te plannen valt.
6. **anonimizer-web** echt archiveren op GitHub (read-only), zodat CI stopt.
7. **`.github`-statuten**: PRINCIPLES, CONTRIBUTING, DOCUMENTATION-STANDARD en REDACTIESTATUUT overlappen;
   één leesvolgorde op het profiel volstaat, samenvoegen hoeft niet.
