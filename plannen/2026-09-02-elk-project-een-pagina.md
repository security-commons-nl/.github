# Plan: elk project een pagina (B13 uitrollen)

**Doel:** elke repo in de projectentabel heeft een pagina op `security-commons-nl.github.io/<naam>/`,
minimaal de leesversie van de README, en de gedeelde site-build woont op één plek in plaats van in elke
repo een kopie.

**Aanleiding:** bij het aanmaken van `applicatiecheck` (concept, 02-09-2026) bleek dat tien van de zestien
projecten niet op het domein staan. Het besluit staat in [BESLUITEN.md](../BESLUITEN.md), de regel is
B13 in het [redactiestatuut](../REDACTIESTATUUT.md).

**Stand bij schrijven:** `applicatiecheck` heeft de pagina al, met de derde kopie van `site/build.mjs`
(na `Handelingsperspectief`, inmiddels gearchiveerd, en `ai-gebruik-in-beeld`) en een eigen afwijking:
query-tab en tabbalk verschijnen alleen als er iets in staat.

---

## 1. Wat er nu is

| Repo | Status | Pagina | Hoe |
|---|---|---|---|
| kennisbank | in gebruik | ja | eigen `tools/build.py` |
| aanvalspaden | prototype | ja | eigen `check/bouw.py`, één HTML |
| csir-assessment-tool | prototype | ja | eigen `register/bouw.py`, één HTML |
| anonimizer-browser | in gebruik | ja | Vite-build |
| ai-gebruik-in-beeld | in gebruik | ja | gedeelde site-build, kopie |
| weerbaarheid-game | in gebruik | ja | Pages vanuit branch, één HTML |
| applicatiecheck | concept | ja | gedeelde site-build, kopie met afwijking |
| grc-platform | in gebruik | **nee** | |
| procescheck | prototype | **nee** | |
| security-posture-tool | prototype | **nee** | |
| iamscan | prototype | **nee** | |
| blast-radius | prototype | **nee** | |
| publicatiescan | in gebruik | **nee** | |
| anonimizer-local | in gebruik | **nee** | |
| hosting-bouwblokken | prototype | **nee** | |
| cisochat | concept | **nee** | |
| policy-as-code | concept | **nee** | |

Infrastructuurrepo's (`anonimizer-proxy`, `security-commons-nl.github.io`, `.github`) vallen buiten B13.

## 2. De site-build op één plek

De build (`build.mjs`, `transforms.mjs`, `base.css`, `components.css`, `page.js`) verhuist naar
`.github/site/`. Wat per repo verschilt blijft in de repo: `site/config.json`, en niets anders.

De herbruikbare workflow `pages-docs.yml` checkt naast de aanroepende repo ook `.github` uit (als
`org-site`, zoals de voorpagina dat al doet met `org-profile`) en draait `node org-site/site/build.mjs`.
Daarvoor moet het script twee paden uit elkaar halen die nu samenvallen: de map met de assets (naast het
script) en de map met de inhoud en de config (de werkmap van de aanroeper). Dat is een wijziging van
enkele regels: `SITE_DIR` blijft de scriptmap, `ROOT` wordt `process.cwd()`, en `config.json` wordt uit
`ROOT/site/` gelezen.

De afwijking uit `applicatiecheck` (lege query-lijst betekent geen query-tab, één tab betekent geen
tabbalk) gaat mee naar de centrale versie; daarmee is hij niet langer een afwijking. `marked` blijft een
dependency van de aanroepende repo (`package.json` + lock), omdat `npm ci` daar draait; een repo zonder
eigen JavaScript krijgt dus alsnog een `package.json` van zes regels. Dat is de prijs van `npm ci`; een
alternatief (de dependency in `.github` installeren) maakt de workflow ingewikkelder dan de winst.

Volgorde: eerst `.github/site/` vullen en de workflow aanpassen, dan `ai-gebruik-in-beeld` en
`applicatiecheck` omzetten naar de centrale versie en hun lokale `site/*.mjs|css|js` verwijderen, met
een test dat hun `dist/index.html` gelijk blijft op de bronvermelding na. Daarna pas de tien.

## 3. De tien repo's

Per repo dezelfde drie bestanden: `.github/workflows/pages.yml` (de aanroep van `pages-docs.yml`, met
`*.md`, `site/**` en `package*.json` als triggers), `site/config.json` (één tab: `README.md`) en
`package.json` met `marked`. Daarna Pages inschakelen op de repo met `build_type: workflow`, één keer
`workflow_dispatch`, en de rij in de projectentabel krijgt in *Direct openen* het label *Leesbare versie*
(prototype, in gebruik) of *Ontwerp* (concept).

Twee bijzonderheden:

- `grc-platform` en `procescheck` hebben een README die naar `docs/` en submodules verwijst. De leesversie
  toont de README; links naar bestanden in de repo blijven naar GitHub wijzen (dat doet `rewriteLinks` al
  voor `LICENSE`; voor andere relatieve links moet hij hetzelfde gaan doen, anders zijn het dode links op
  de pagina).
- `cisochat` heeft een `docs/`-map met onderzoek; die kan als tweede tab mee zodra iemand dat wil. Eerste
  stap is alleen de README.

Volgorde: de twee concepten eerst (`policy-as-code`, `cisochat`), want daar is de winst het grootst: een
concept dat op de site staat nodigt uit tot meedenken. Dan de prototypes, dan de twee die in gebruik zijn.

## 4. De voorpagina en de controle

- `security-commons-nl.github.io/site/build.mjs` leest de kolom *Direct openen* en gebruikt elke link als
  "live"; de eerste drie rijen met een link zijn de uitgelichte kaarten. Het label staat al op de kaarten
  in de lijst (`card-open`), dus *Ontwerp* is daar zichtbaar; op de drie uitgelichte kaarten staat geen
  label, en daar hoort een ontwerp ook niet (B13). `test_voorpagina.py` krijgt een geval dat een rij met
  *Ontwerp* niet uitgelicht wordt.
- `repo_compliance.py` krijgt als laatste stap een B13-controle: de rij van de repo in de projectentabel
  heeft een link in *Direct openen*, en die link geeft 200. De controle gaat pas aan als alle tien om zijn,
  anders begint de regel met tien rode runs (zie het besluit). `test_repo_compliance.py` krijgt de
  gevallen erbij.
- `llms.txt` en `sitemap.xml` volgen vanzelf uit de tabel; de wekelijkse linkcheck vangt een pagina die
  niet bestaat.

## 5. Wat dit niet doet

Geen herontwerp van de leesversie, geen nieuwe huisstijl, geen migratie van repo's die al een eigen
pagina hebben (kennisbank, aanvalspaden, csir-assessment-tool, anonimizer-browser, weerbaarheid-game).
Die vallen al onder B13 en blijven zoals ze zijn.

## Stand

| Stap | Stand |
|---|---|
| B13 in het statuut, besluit vastgelegd | gedaan, 02-09-2026 |
| `.github/site/` en `pages-docs.yml` centraal | te doen |
| `ai-gebruik-in-beeld` en `applicatiecheck` op de centrale versie | te doen |
| tien repo's een pagina | te doen |
| label zichtbaar op de voorpagina | te doen |
| B13-controle in `repo_compliance.py` | te doen, als laatste |
