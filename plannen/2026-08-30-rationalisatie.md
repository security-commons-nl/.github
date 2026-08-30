# Bouwplan: een ruggengraat, de handleidingen erlangs

> **Voor de uitvoerder.** Dit plan is geschreven om taak voor taak uit te voeren zonder eigen
> interpretatie. Elke taak heeft: een doel, genummerde stappen met exacte paden en commando's, een test
> met de verwachte uitkomst, en een commit. **Een taak is pas klaar als de test groen is en de commit is
> gedaan.** Sla geen stap over, vul niets "later" in, en begin niet aan de volgende taak als de test van
> de huidige rood is. Staat er "STOP", stop dan en meld wat je zag.
>
> Lees eerst §0 (feiten), §1 (regels) en §3 (referentietabellen). De achtergrond van de besluiten staat
> in `2026-08-30-architectuur-en-backlog.md` en hoeft niet gelezen te worden om te kunnen bouwen.

**Doel.** Wie de zelfcheck doet, ziet per barriere wat hij moet doen, hoe hij dat doet en wat hij daarmee
aantoont. De barriere wordt de enige inhoudelijke ruggengraat van de commons. `security-shop` gaat als
inhoud op in de kennisbank en gaat als repo dicht. `Handelingsperspectief` gaat weg. De site vertelt de
keten. Alle onderlinge links kloppen, en een script bewijst dat.

**Peildatum plan:** 30-08-2026. **Uitkomst na uitvoering:** 35 van de 44 barrieres met een handleiding,
negen bewust open, een kennisbank die op type groepeert, een projectentabel zonder `security-shop`, en een
linkcontrole die over alle repo's heen groen is.

---

## 0. Vaste feiten

### 0.1 Werkmap en repo's

Alles staat in `X:\SECURITY-COMMONS-NL\`. Die map zelf is **geen** git-repo; elke submap wel. Gebruik
Git Bash voor alle commando's. Paden hieronder zijn relatief aan `X:\SECURITY-COMMONS-NL\` tenzij anders
gezegd.

| Repo (map) | GitHub | Rol in dit plan |
|---|---|---|
| `kennisbank/` | `security-commons-nl/kennisbank` | krijgt de handleidingen; wordt de bron van het handelingsperspectief |
| `aanvalspaden/` | `security-commons-nl/aanvalspaden` | leest het handelingsperspectief; de pagina `/normen/` |
| `security-shop/` | `security-commons-nl/security-shop` | leverancier van 55 patronen; gaat daarna dicht |
| `.github/` | `security-commons-nl/.github` | statuut, profiel (projectentabel), architectuur, dit plan |
| `security-commons-nl.github.io/` | `security-commons-nl/security-commons-nl.github.io` | de voorpagina, gegenereerd uit het profiel |
| `Handelingsperspectief/` | `security-commons-nl/Handelingsperspectief` (gearchiveerd) | wordt verwijderd |

### 0.2 Commando's die je steeds nodig hebt

```bash
# Kennisbank controleren (blokkeert bij elke statuutovertreding) en indexpagina's bouwen
cd X:/SECURITY-COMMONS-NL/kennisbank && python tools/build.py           # bouwt
cd X:/SECURITY-COMMONS-NL/kennisbank && python tools/build.py --check   # alleen controleren
cd X:/SECURITY-COMMONS-NL/kennisbank && python tools/test_build.py      # tests van het bouwscript

# Aanvalspaden: alle tests (bron, mapping, crosswalk-pagina in de browser, zelfcheck)
cd X:/SECURITY-COMMONS-NL/aanvalspaden && python -m pytest tests/ mappingen/tests/ check/tests/ -q
cd X:/SECURITY-COMMONS-NL/aanvalspaden && python mappingen/bouw.py      # bouwt /normen/

# Statuutcontrole van een repo (draai vanuit .github)
cd X:/SECURITY-COMMONS-NL/.github && python tools/repo_compliance.py ../<repo> --profiel profile/README.md

# Voorpagina opnieuw genereren na een wijziging in het profiel
cp X:/SECURITY-COMMONS-NL/.github/profile/README.md X:/SECURITY-COMMONS-NL/security-commons-nl.github.io/org-profile/profile/README.md
cd X:/SECURITY-COMMONS-NL/security-commons-nl.github.io && node site/build.mjs && python -m pytest site/test_voorpagina.py -q

# Leesversie (index.html) maken uit een README.md van een kennisbank-item: zie Taak 1, stap 6
```

`X:\TOOLS\pandoc\pandoc.exe` is pandoc 3.9. Python 3.14 en node 24 zijn aanwezig. Playwright met
Chromium is geinstalleerd (de browsertests slaan over als het ontbreekt; dat is dan een rode vlag).

### 0.3 De enige bronnen

- **Barrieres:** `aanvalspaden/paden.json`. Het `vraag_id` van een chokepoint is de barriere. 44 stuks,
  lijst in §3.1. Je verandert dit bestand niet.
- **Handelingsperspectief:** na Taak 1 is de **kennisbank** de bron (frontmatter `barrieres:` per
  handleiding). `aanvalspaden/mappingen/handelingsperspectief.json` is dan een gegenereerde kopie.
- **Projectenlijst:** `.github/profile/README.md`, de tabel onder `## Alle projecten`. Voorpagina,
  `llms.txt` en `sitemap.xml` volgen daaruit. Er is geen tweede lijst.

---

## 1. Regels

1. **Redactiestatuut** (`.github/REDACTIESTATUUT.md`) geldt letterlijk. In het kort: Nederlands; geen
   persoonsnamen, geen organisatienamen als herkomst, geen e-mailadressen, geen links naar sociale media;
   **geen em-dashes** (schrijf een komma, punt of dubbele punt); Engelse vaktermen blijven Engels; elk
   item is `categorie/item/README.md` met acht frontmattervelden en een `index.html`-leesversie.
2. **Commits:** Nederlands, een onderwerp per commit, map als prefix (`security: ...`, `tools: ...`,
   `mappingen: ...`, `profiel: ...`). Stage alleen paden die je zelf hebt geraakt: `git add <pad>`,
   **nooit** `git add -A` of `git add .`. Geen `Co-Authored-By`, geen AI-vermelding.
3. **Tests eerst.** Elke taak eindigt met de test uit die taak. Rood betekent: repareren, niet doorgaan.
4. **Nooit een bestand overschrijven dat je niet hebt gelezen.** Lees eerst, wijzig gericht.
5. **Rode "in gebruik/EBUSY"-fout bij schrijven:** twee seconden wachten, een keer opnieuw.
6. **Onomkeerbare acties doe je niet.** Een repo verwijderen op GitHub (Taak 6) doet een mens in de
   webinterface. Jij bereidt voor, controleert en meldt.
7. **Bij twijfel over inhoud: STOP en meld.** Een handleiding herschrijven mag je; een technische bewering
   verzinnen die niet in het patroon staat mag je niet.
8. **Fictieve voorbeelden** in tekst: organisatie "Gemeente Duinstad", domein `duinstad.nl`, mensen
   alleen als rol ("de CISO"). Nooit echte gemeenten.

---

## 2. De besluiten (waarom, in een zin per stuk)

1. De barriere (`vraag_id`) is de enige inhoudelijke ruggengraat; elke handleiding draagt `barrieres:`.
2. `handleiding` wordt een type in de kennisbank; de sectiepagina groepeert op type.
3. Meer handleidingen per barriere mogen, elk met `rol: fundering | alternatief | verdieping`.
4. `security-shop` gaat op in de kennisbank; wat geen barriere raakt wordt een issue met label `idee`.
5. `Handelingsperspectief` wordt verwijderd nadat de links zijn rechtgezet (herroept een deel van het
   besluit van 29-08-2026, dat de repo als doorverwijzing hield).
6. `Meten voordat je ingrijpt` wordt een pijler met twee handleidingen eronder.
7. Voorpagina en projectentabel vertellen de keten in vier vragen.
8. Bouwplannen en architectuur staan op GitHub, niet op een schijf.

---

## 3. Referentietabellen

### 3.1 De 44 barrieres

Uit `aanvalspaden/paden.json`. Kolom *nu* is de stand op 30-08-2026 in
`aanvalspaden/mappingen/handelingsperspectief.json`.

| vraag_id | Titel (uit paden.json) | Nu |
|---|---|---|
| `pr` | Dwing phishingbestendige authenticatie af | handleiding (volledig) |
| `fallback` | Verwijder zwakke fallback- en herstelroutes | handleiding (volledig) |
| `idresponse` | Test response op identity- en app-compromise | handleiding (gedeeltelijk) |
| `legacy` | Blokkeer legacy authentication | handleiding (gedeeltelijk) |
| `devicecode` | Blokkeer Device Code Flow, behalve beheerde uitzonderingen | gevraagd |
| `consent` | Beperk app-toestemming en richt gecontroleerde admin consent in | gevraagd |
| `model` | Scheid privileged access technisch van dagelijks gebruik | gevraagd |
| `adminhard` | Hard de beheerwerkplek en dwing de toegestane toegang af | gevraagd |
| `jit` | Verwijder permanente rollen en gebruik PIM/JIT | gevraagd |
| `elevation` | Dwing herauthenticatie af bij privileged elevation | gevraagd |
| `key` | Vereis een aparte fysieke FIDO2-key voor elevation | handleiding (gedeeltelijk) |
| `adminmonitor` | Monitor privileged activiteiten en rolwijzigingen | gevraagd |
| `unmanaged` | Dwing toegang vanaf beheerde, compliant laptops af | gevraagd |
| `session` | Beperk tokenmisbruik met apparaatbinding en sessiebeleid | gevraagd |
| `execution` | Beperk software- en scriptuitvoering met application control en ASR | handleiding (volledig) |
| `browser` | Hard browsers en beperk extensies en gegevensdragers | handleiding (gedeeltelijk) |
| `edr` | Borg EDR, tamper protection en snelle endpointisolatie | handleiding (gedeeltelijk) |
| `mail` | Dwing een sterke e-mailbaseline af | handleiding (gedeeltelijk) |
| `dmarc` | Richt SPF, DKIM en DMARC-handhaving volledig in | gevraagd |
| `mailresponse` | Test mail-remediation en het phishing/BEC-playbook | gevraagd |
| `localadmin` | Verwijder lokale administratorrechten | handleiding (gedeeltelijk) |
| `patch` | Borg OS- en third-party-patching met controle op dekking | gevraagd |
| `segment` | Beperk lateral movement met segmentatie en minimale rechten | gevraagd |
| `vuln` | Borg continu kwetsbaarhedenbeheer en spoedpatching | gevraagd |
| `remote` | Scherm publieke beheerinterfaces af | gevraagd |
| `pentest` | Laat extern pentesten en verifieer herstel van bevindingen | gevraagd |
| `exploitresponse` | Test detectie en response op externe exploits | handleiding (gedeeltelijk) |
| `assets` | Ontdek en bewaak het externe aanvalsoppervlak | gevraagd |
| `webtest` | Test web/API-beveiliging en herstel kwetsbaarheden | gevraagd |
| `l7` | Richt WAF, rate limiting en Layer-7-bescherming in | gevraagd |
| `origin` | Sluit rechtstreekse toegang tot de origin af | gevraagd |
| `upstream` | Borg upstream DDoS-mitigatie en robuuste DNS | gevraagd |
| `ddosresponse` | Oefen DDoS-response met provider en SOC | gevraagd |
| `backup` | Bescherm back-ups met onveranderbaarheid en gescheiden beheer | gevraagd |
| `restore` | Test herstel tegen de afgesproken RTO en RPO | gevraagd |
| `crisis` | Oefen het ransomware- en crisisherstelplan | gevraagd |
| `critical` | Stel kritieke processen en herstelprioriteiten vast | gevraagd |
| `dependencies` | Breng kritieke systemen en leveranciers in samenhang in beeld | gevraagd |
| `review` | Beoordeel kritieke leveranciers periodiek en risicogestuurd | handleiding (gedeeltelijk) |
| `technicalvendor` | Toets technische maatregelen van kritieke leveranciers | handleiding (volledig) |
| `residual` | Maak significante leveranciersrestrisico's expliciet | handleiding (gedeeltelijk) |
| `owner` | Leg leveranciersrisico's voor aan de risicohouder | gevraagd |
| `treatment` | Leg risicoacceptatie of maatregelen met eigenaar en termijn vast | gevraagd |
| `soc` | Borg 24/7 opvolging en escalatie van kritieke meldingen | gevraagd |

### 3.2 Welk shop-patroon wordt welke handleiding

De patronen staan in `security-shop/mockup/index.html`, in het JavaScript-blok `const PATTERNS = [`
(regel 834 tot 2934). Elk patroon is een object met velden `slug`, `naam`, `role`, `one`, `gap`,
`wanneer`, `hoe`, `stappen` (lijst), `voordelen` (lijst), `nadelen` (lijst), `kosten`, `mapping`
(`bio`, `nis2`, `avg`), `comm` (`directie`, `im`, `mt`). Taak 3 stap 1 dumpt ze naar markdown.

Kolom *mapnaam* is de nieuwe map in `kennisbank/security/`. Kolom *rol* is de rol in
`handelingsperspectief`. Werkvolgorde = de volgorde van deze tabel (dat is de backlogvolgorde).

| # | slug in de mockup | mapnaam in de kennisbank | barrieres | rol |
|---|---|---|---|---|
| 1 | `centrale-logverzameling` | `centrale-logverzameling` | `soc` | fundering |
| 2 | `co-managed-siem` | `co-managed-siem` | `soc` | alternatief |
| 3 | `uitbestede-soc-mssp` | `uitbestede-soc` | `soc` | alternatief |
| 4 | `mdr-dienst` | `mdr-dienst` | `soc` | alternatief |
| 5 | `regionaal-soc` | `regionaal-soc` | `soc` | alternatief |
| 6 | `tiered-administration` | `tiered-administration` | `model` | fundering |
| 7 | `paw-beheerwerkplek` | `beheerwerkplek` | `adminhard` | fundering |
| 8 | `pim-jit` | `just-in-time-beheerrechten` | `jit` | fundering |
| 9 | `logging-retentie-forensics` | `logging-en-retentie` | `adminmonitor` | fundering |
| 10 | `bastion-hosts` | `bastion-hosts` | `remote` | fundering |
| 11 | `virtual-patching` | `waf-en-virtual-patching` | `l7` | fundering |
| 12 | `ddos-scrubbing` | `ddos-scrubbing` | `upstream` | fundering |
| 13 | `vulnerability-scanning` | `kwetsbaarheden-scannen` | `vuln` | fundering |
| 14 | `exposure-management` | `exposure-management` | `vuln` | verdieping |
| 15 | `attack-surface-management` | `aanvalsoppervlak-bewaken` | `assets` | fundering |
| 16 | `endpoint-hardening` | `patchen-met-dekking` | `patch` | fundering |
| 17 | `immutable-backups` | `onveranderbare-backups` | `backup` | fundering |
| 18 | `recovery-oefening` | `hersteltest` | `restore` | fundering |
| 19 | `crisis-tabletops` | `crisisoefening` | `crisis` | fundering |
| 20 | `cyber-crisiscommunicatie` | `crisiscommunicatie` | `crisis` | verdieping |
| 21 | `browser-session-protection` | `sessiebescherming` | `session` | fundering |
| 22 | `hardening-cloud-portalen` | `cloudportalen-harden` | `consent` | fundering |
| 23 | `least-privilege-iam-cloud` | `least-privilege-cloud` | `consent` | verdieping |
| 24 | `ir-procedures` | `incident-response-procedures` | `mailresponse` | fundering |
| 25 | `netwerksegmentatie` | `netwerksegmentatie` | `segment` | fundering |
| 26 | `microsegmentatie` | `microsegmentatie` | `segment` | verdieping |
| 27 | `pentest-periodiek` | `periodiek-pentesten` | `pentest` | fundering |
| 28 | `ssdlc` + `dependency-scanning` (samenvoegen) | `web-en-api-testen` | `webtest` | fundering |
| 29 | `ketenafhankelijkheidsanalyse` | `ketenafhankelijkheden` | `dependencies` | fundering |
| 30 | `edr-xdr` | `edr-inrichten` | `edr` | fundering |
| 31 | `application-control` | `application-control` | `execution` | fundering |
| 32 | `phishingbestendige-mfa-beheeraccounts` | `fido2-voor-beheerders` | `key` | fundering |
| 33 | `mfa-handhaving-sanering` | `mfa-handhaving` | `fallback`, `legacy` | verdieping |
| 34 | `leveranciersassurance` | `leveranciersbeoordeling` | `review` | fundering |
| 35 | `pentest-exit-leveranciers` | `pentest-en-exit-bij-leveranciers` | `technicalvendor` | verdieping |

Patronen die **niet** worden overgezet maar een issue worden (Taak 3 stap 9):
`vier-ogen-kritieke-wijzigingen`, `bio-nis2-assurance`, `awareness-trust-abuse`, `sbom-beheer`,
`code-signing`, `tenantisolatie-cloudsoevereiniteit`, `identity-eisen-leveranciers`,
`secrets-management`, `api-authenticatie`, `api-rate-limiting`, `api-misbruikdetectie`, `cspm`,
`saas-monitoring`, `east-west-monitoring`, `ueba-anomaliedetectie`, `threat-hunting`,
`threat-intel-correlatie`.

Patronen die al een kennisbank-item hebben en alleen de communicatieregels leveren (Taak 3 stap 8):
`wachtwoordloos-passkeys` naar *Passkeys invoeren*; `security-annex-inkoop` naar *Security Annex voor
leveranciers*.

Barrieres die na dit plan **bewust open** blijven (negen), met de reden die in `gevraagd` blijft staan:
`critical`, `ddosresponse`, `devicecode`, `dmarc`, `elevation`, `origin`, `owner`, `treatment`,
`unmanaged`. Voor geen van deze negen staat een patroon in de shop; `ddos-scrubbing` gaat over
mitigatie inkopen (`upstream`), niet over de response oefenen (`ddosresponse`).

### 3.3 Frontmatter van een handleiding (kopieer letterlijk, vul de waarden in)

```yaml
---
titel: <Titel in de gebiedende wijs, zoals de barriere: "Richt centrale logverzameling in">
vakgebied: security
type: handleiding
normen: [BIO2]
versie: 2026-09
herkomst: patroon uit de security-shop-catalogus van security-commons-nl, herschreven als handleiding
status: concept
samenvatting: <twee tot vier zinnen: welke barriere, wat je aan het eind hebt staan, en welk bewijs dat oplevert>
barrieres: [<vraag_id>, <vraag_id>]
rol: <fundering | alternatief | verdieping>
---
```

Voor de twee handleidingen uit *Meten voordat je ingrijpt* (Taak 2) is `herkomst` gelijk aan die van
de pijler: `gegeneraliseerd uit een casus bij een gemeentelijke organisatie`, en komt er een veld
`pijler: meten-voordat-je-ingrijpt` bij.

### 3.4 Body van een handleiding (vaste koppen, in deze volgorde)

```markdown
# <Titel, gelijk aan frontmatter>

> **Barriere:** <titel uit §3.1>. <Een zin uit `one` van het patroon.>

## Wanneer wel, wanneer niet
<uit `wanneer` en `gap`>

## Zo richt je het in
<uit `hoe`, gevolgd door de genummerde `stappen`>

## Wat het kost en wat het oplevert
<uit `kosten`, `voordelen`, `nadelen`; als lijstjes>

## Bewijs
<Wat je aan het eind kunt laten zien. Begin met de tekst van het veld `bewijs` van de barriere in
paden.json, en maak concreet welke export, rapportage of configuratie dat is.>

## Zo leg je het uit
**Aan de directie.** <uit `comm.directie`>
**Aan de informatiemanager.** <uit `comm.im`>
**Aan het MT.** <uit `comm.mt`>

## Hoe dit samenhangt
Deze handleiding hoort bij barriere `<vraag_id>` uit de [zelfcheck aanvalspaden](https://security-commons-nl.github.io/aanvalspaden/).
Wat je hiermee aantoont in BIO 2.0, NIST CSF, het Wpg-kader en de AVG staat op
[Van aanvalspad naar norm](https://security-commons-nl.github.io/aanvalspaden/normen/).
<Als er alternatieven of verdiepingen zijn voor dezelfde barriere: noem ze hier met relatieve links.>

## Licentie
[EUPL-1.2](../../LICENSE).
```

**De koppen *Bewijs* en *Zo leg je het uit* zijn verplicht**; een test in Taak 1 blokkeert erop.

---

## 4. Taken

### Taak 0: Wat al klaarstaat naar GitHub

**Doel.** De architectuur en de bouwplannen staan in een repo in plaats van op een schijf.

**Stappen.**

1. Controleer wat er klaarstaat:
   ```bash
   cd X:/SECURITY-COMMONS-NL/.github && git status --short
   cd X:/SECURITY-COMMONS-NL/aanvalspaden && git status --short
   ```
   Verwacht in `.github`: `ARCHITECTUUR.md`, `architectuur-landschap.svg`, `architectuur-scharnier.svg`
   als nieuw. Verwacht in `aanvalspaden`: `docs/` met drie bestanden als nieuw. Ontbreekt iets: STOP.
2. Haal lokale paden uit `aanvalspaden/docs/2026-08-28-bouwplan-keten.md`. Open het bestand en vervang:
   - elke `X:\SECURITY-COMMONS-NL\` en `X:/SECURITY-COMMONS-NL/` door `<werkmap>/`
   - `X:\TOOLS\pandoc\pandoc.exe` door `pandoc`
   - de regel die begint met `- Werkmap:` door
     `- Werkmap: de map waarin alle repo's van security-commons-nl naast elkaar staan.`
   Controle: `grep -n "X:" aanvalspaden/docs/*.md` geeft geen regels terug.
3. Maak de map voor organisatiebrede plannen en zet dit plan erin:
   ```bash
   mkdir -p X:/SECURITY-COMMONS-NL/.github/plannen
   cp X:/SECURITY-COMMONS-NL/2026-08-30-bouwplan-rationalisatie.md X:/SECURITY-COMMONS-NL/.github/plannen/2026-08-30-rationalisatie.md
   cp X:/SECURITY-COMMONS-NL/2026-08-30-architectuur-en-backlog.md X:/SECURITY-COMMONS-NL/.github/plannen/2026-08-30-architectuur-en-backlog.md
   ```
   Open `.github/plannen/2026-08-30-architectuur-en-backlog.md` en vervang de twee afbeeldingspaden
   `2026-08-30-architectuur-commons.svg` door `../architectuur-landschap.svg` en
   `2026-08-30-scharnier-barriere.svg` door `../architectuur-scharnier.svg`. Verwijder de laatste
   sectie `## Waar dit stuk zelf hoort` (het stuk staat nu waar het hoort).
4. Voeg aan `.github/profile/README.md`, direct onder de regel die begint met
   `Dat is de voorkant: alle kennis en tools op één pagina`, deze alinea toe:
   ```
   Hoe het geheel in elkaar zit, welke repositories er zijn en hoe ze samenhangen, staat in
   [ARCHITECTUUR.md](https://github.com/security-commons-nl/.github/blob/main/ARCHITECTUUR.md).
   ```
5. Verwijder de verouderde tweede projectenlijst op de schijf: `rm X:/SECURITY-COMMONS-NL/README.md`.
   (Dat bestand staat in geen enkele repo.)
6. Commit en push, per repo:
   ```bash
   cd X:/SECURITY-COMMONS-NL/.github
   git add ARCHITECTUUR.md architectuur-landschap.svg architectuur-scharnier.svg plannen/ profile/README.md
   git commit -m "architectuur: het landschap, het scharnier en de plannen staan nu in de repo"
   git push
   cd X:/SECURITY-COMMONS-NL/aanvalspaden
   git add docs/
   git commit -m "docs: de bouwplannen van de keten staan nu in de repo, zonder lokale paden"
   git push
   ```

**Test.**
```bash
cd X:/SECURITY-COMMONS-NL/.github && python tools/repo_compliance.py ../aanvalspaden --profiel profile/README.md
```
Verwacht: `Repo voldoet aan het statuut`. En `gh run list -R security-commons-nl/aanvalspaden --limit 3`
toont drie keer `success` binnen twee minuten.

**Klaar als:** beide pushes gedaan, CI groen, `ls X:/SECURITY-COMMONS-NL/README.md` geeft "No such file".

---

### Taak 1: De kennisbank kan handleidingen dragen

**Doel.** Type `handleiding` bestaat, `barrieres:` wordt gevalideerd tegen `paden.json`, de sectiepagina
groepeert op type, en `tools/build.py` exporteert `handelingsperspectief.json`. Plus een script dat een
leesversie maakt, zodat elke handleiding op dezelfde manier wordt gebouwd.

**Stappen.**

1. Open `kennisbank/tools/build.py`. Wijzig regel 38 tot 41 zo:
   ```python
   TYPES = ["beleid", "sjabloon", "lesmateriaal", "dataset", "referentie", "aanpak", "rapportage", "handleiding"]
   STATUSSEN = ["concept", "in gebruik", "sjabloon", "gearchiveerd"]
   VERPLICHT = ["titel", "vakgebied", "type", "normen", "herkomst", "status", "samenvatting"]
   TOEGESTAAN = set(VERPLICHT) | {"peildatum", "versie", "licentie", "barrieres", "rol", "pijler"}
   ROLLEN = ["fundering", "alternatief", "verdieping"]
   ```
2. Voeg direct onder `ROOT_MAPPEN_OK` toe:
   ```python
   # De barrieres komen uit paden.json in de aanvalspaden-repo. Lokaal staat die ernaast; in CI wordt
   # hij naar _aanvalspaden uitgecheckt. Een handleiding mag alleen naar een barriere verwijzen die bestaat.
   PADEN_KANDIDATEN = (ROOT.parent / "aanvalspaden" / "paden.json", ROOT / "_aanvalspaden" / "paden.json")


   def barrieres() -> dict[str, str]:
       """vraag_id -> titel, uit paden.json. Leeg als het bestand nergens staat (dan meldt --check dat)."""
       import json
       for pad in PADEN_KANDIDATEN:
           if pad.is_file():
               data = json.loads(pad.read_text(encoding="utf-8"))
               uit = {}
               for blad in data["bladeren"]:
                   for cp in blad["chokepoints"]:
                       uit.setdefault(cp["vraag_id"], cp["titel"])
               for rv in data.get("randvoorwaarden", []):
                   uit.setdefault(rv["vraag_id"], rv["titel"])
               return uit
       return {}
   ```
3. Zoek in `controleer_item` de plek waar de frontmatter is gelezen en gevalideerd (na de controle op
   `VERPLICHT` en `TOEGESTAAN`). Voeg daar toe:
   ```python
       if fm.get("type") == "handleiding":
           bar = fm.get("barrieres")
           if not isinstance(bar, list) or not bar:
               fout(readme, "B2", "type handleiding vereist barrieres: [vraag_id, ...] uit paden.json")
           else:
               bekend = barrieres()
               if not bekend:
                   fout(readme, "B2", "paden.json niet gevonden; zet de aanvalspaden-repo ernaast of in _aanvalspaden")
               for b in bar:
                   if b not in bekend:
                       fout(readme, "B2", f"barriere '{b}' bestaat niet in paden.json")
           if fm.get("rol") not in (None, *ROLLEN):
               fout(readme, "B2", f"rol moet een van {ROLLEN} zijn")
           if fm.get("pijler"):
               if not (ROOT / vak / fm["pijler"] / "README.md").is_file():
                   fout(readme, "B2", f"pijler '{fm['pijler']}' bestaat niet in {vak}/")
           body_lc = body.lower()
           for kop in ("## bewijs", "## zo leg je het uit"):
               if kop not in body_lc:
                   fout(readme, "B3", f"een handleiding heeft de kop '{kop[3:].title()}' nodig")
   ```
   (`fm` is de frontmatter-dict, `body` de tekst na de frontmatter, `readme` het pad. Kijk hoe die in
   `controleer_item` heten en gebruik die namen.) Barrieres die alleen in `paden.json` staan als
   randvoorwaarde tellen mee; de helper hierboven doet dat al.
4. Groeperen op type in `bouw_sectie`. Vervang de regel
   `kaarten = "".join(kaart(i, "", False).replace(f'href="{vak}/', 'href="') for i in items)` en de regel
   erna (`grid = ...`) door:
   ```python
       def blok(kop: str, sub: list[dict]) -> str:
           if not sub:
               return ""
           ks = "".join(kaart(i, "", False).replace(f'href="{vak}/', 'href="') for i in sub)
           return f'<h3 class="groep">{e(kop)}</h3>\n<div class="grid">\n\n{ks}\n</div>\n'

       handleidingen = [i for i in items if i.get("type") == "handleiding"]
       overig = [i for i in items if i.get("type") != "handleiding"]
       grid = (blok("Aanpakken, sjablonen en naslag", overig)
               + blok("Handleidingen: een maatregel inrichten, per barriere uit de zelfcheck", handleidingen))
       if not items:
           grid = '<p class="h2sub">Nog geen stukken. Heb je iets liggen? Zie hieronder.</p>'
   ```
   Voeg in de CSS-string van `pagina()` (zoek `.itemtitle{`) deze regel toe:
   `h3.groep{font-size:13px;letter-spacing:.06em;text-transform:uppercase;color:#5c6570;margin:26px 0 8px}`.
5. Toon de barrieres op de kaart. In `meta_regel(fm, met_vak)`: als `fm.get("barrieres")`, voeg aan de
   metaregel toe `" · barriere: " + ", ".join(barrieres().get(b, b) for b in fm["barrieres"])`, en als
   `fm.get("rol")` ook `f" · {fm['rol']}"`.
6. Maak `kennisbank/tools/leesversie.py`:
   ```python
   """Maakt de leesversie (index.html) van een item uit zijn README.md.

   Gebruik:  python tools/leesversie.py security/<item>
   Daarna:   python tools/build.py   (zet kruimelpad, bronvoet, favicon en inhoudsopgave)

   pandoc --standalone levert de standaardopmaak die alle leesversies delen. De frontmatter gaat er
   eerst af, anders zet pandoc hem als metadata boven de tekst.
   """
   import pathlib, re, shutil, subprocess, sys

   ROOT = pathlib.Path(__file__).resolve().parent.parent
   item = ROOT / sys.argv[1]
   readme = item / "README.md"
   tekst = readme.read_text(encoding="utf-8")
   tekst = re.sub(r"\A---\n.*?\n---\n", "", tekst, count=1, flags=re.S)
   titel = re.search(r"^# (.+)$", tekst, re.M).group(1).strip()
   pandoc = shutil.which("pandoc") or r"X:\TOOLS\pandoc\pandoc.exe"
   uit = subprocess.run(
       [pandoc, "--from", "gfm", "--to", "html5", "--standalone", "--metadata", f"title={titel}",
        "--metadata", "lang=nl"],
       input=tekst, capture_output=True, text=True, encoding="utf-8", check=True,
   )
   (item / "index.html").write_text(uit.stdout, encoding="utf-8")
   print(f"{item / 'index.html'}: {len(uit.stdout) // 1024} kB; draai nu python tools/build.py")
   ```
7. Export van het handelingsperspectief. Voeg aan `build.py`, vlak voor `def main()`, toe:
   ```python
   def schrijf_handelingsperspectief(items: dict[str, list[dict]]) -> bool:
       """De kennisbank is de bron: per handleiding de barrieres en de rol. aanvalspaden kopieert dit."""
       import json
       bekend = barrieres()
       hl = []
       for vak in VAKGEBIEDEN:
           for fm in items[vak]:
               if fm.get("type") != "handleiding":
                   continue
               for b in fm["barrieres"]:
                   hl.append({
                       "barriere": b,
                       "item": f"{vak}/{fm['_map'].name}",
                       "titel": fm["titel"],
                       "rol": fm.get("rol", "fundering"),
                       "url": f"{SITE}/{vak}/{fm['_map'].name}/",
                   })
       hl.sort(key=lambda h: (h["barriere"], ["fundering", "alternatief", "verdieping"].index(h["rol"]), h["titel"]))
       gedekt = {h["barriere"] for h in hl}
       data = {
           "versie": "gegenereerd door kennisbank/tools/build.py; wijzig de frontmatter van de items, niet dit bestand",
           "handleidingen": hl,
           "zonder_handleiding": sorted(b for b in bekend if b not in gedekt),
       }
       return schrijf(ROOT / "handelingsperspectief.json", json.dumps(data, ensure_ascii=False, indent=2) + "\n")
   ```
   En in `main()`, direct na de regel `if schrijf(ROOT / "index.html", bouw_root(secties, items)):` en
   het bijbehorende `gewijzigd.append("index.html")`, voeg toe:
   ```python
       if schrijf_handelingsperspectief(items):
           gewijzigd.append("handelingsperspectief.json")
   ```
   Voeg `"handelingsperspectief.json"` toe aan `ROOT_BESTANDEN_OK`.
8. CI: open `kennisbank/.github/workflows/build-index.yml`. Voeg direct na de eerste
   `- uses: actions/checkout@...`-stap toe:
   ```yaml
         - uses: actions/checkout@v7
           with:
             repository: security-commons-nl/aanvalspaden
             path: _aanvalspaden
   ```
   Voeg `_aanvalspaden/` toe aan `kennisbank/.gitignore` en aan `ROOT_MAPPEN_OK` in `build.py`.
9. Tests. Voeg aan `kennisbank/tools/test_build.py` een testklasse toe, naar het voorbeeld van de
   bestaande klassen (gebruik de bestaande helper `self.item(readme, pagina)` die een tijdelijk item
   aanmaakt en `self.meldingen()` die de fouten teruggeeft):
   - `test_handleiding_zonder_barrieres_is_een_fout`: README met `type: handleiding` zonder
     `barrieres:` geeft een melding met `barrieres`.
   - `test_onbekende_barriere_is_een_fout`: `barrieres: [bestaatniet]` geeft een melding met
     `bestaat niet in paden.json`.
   - `test_handleiding_zonder_bewijskop_is_een_fout`: body zonder `## Bewijs` geeft een melding.
   - `test_geldige_handleiding_geeft_geen_melding`: `barrieres: [pr]`, `rol: fundering`, body met de
     twee verplichte koppen: geen meldingen.
   - `test_export_bevat_elke_handleiding_per_barriere`: bouw twee tijdelijke handleidingen op dezelfde
     barriere met verschillende rol; `schrijf_handelingsperspectief` levert twee regels voor die barriere,
     fundering eerst.
10. Documenteer. Voeg aan `kennisbank/CONTRIBUTING.md` een sectie `## Een handleiding toevoegen` toe met
    de frontmatter uit §3.3, de vaste koppen uit §3.4 en de twee commando's (`leesversie.py`,
    `build.py`). Voeg aan `kennisbank/README.md` onder `## Wat staat hier` een alinea toe: handleidingen
    zijn instructies per barriere uit de zelfcheck; ze dragen `barrieres:` en zijn de bron van
    *Hoe pak ik het aan* op de normverankering, met de link `https://security-commons-nl.github.io/aanvalspaden/normen/`.
11. Voeg `handleiding` toe aan de opsomming van types in `.github/REDACTIESTATUUT.md` regel B2, en
    voeg aan de B1-tabel bij `kennisbank` toe: `; items van type handleiding dragen barrieres: en zijn
    de bron van het handelingsperspectief`.

**Test.**
```bash
cd X:/SECURITY-COMMONS-NL/kennisbank && python tools/test_build.py && python tools/build.py
```
Verwacht: alle tests `ok`; daarna `Redactiestatuut: geen overtredingen (9 items).` en
`Gebouwd: ... handelingsperspectief.json`. Open `kennisbank/handelingsperspectief.json`: het bevat
`"handleidingen": []` (er is nog geen item van type handleiding) en 44 namen onder
`zonder_handleiding`. Is dat aantal niet 44: STOP.

**Commit.**
```bash
cd X:/SECURITY-COMMONS-NL/kennisbank
git add tools/build.py tools/test_build.py tools/leesversie.py .github/workflows/build-index.yml .gitignore CONTRIBUTING.md README.md handelingsperspectief.json
git commit -m "tools: type handleiding met barrieres uit paden.json; sectiepagina groepeert; export handelingsperspectief"
git push
cd X:/SECURITY-COMMONS-NL/.github && git add REDACTIESTATUUT.md && git commit -m "statuut: type handleiding en de kennisbank als bron van het handelingsperspectief" && git push
```

**Klaar als:** CI van de kennisbank groen (`gh run list -R security-commons-nl/kennisbank --limit 2`).

---

### Taak 2: Meten voordat je ingrijpt wordt een pijler met twee handleidingen

**Doel.** Twee zelfstandige handleidingen, een gekrompen pijler, en geen enkele link meer naar de
gearchiveerde repo.

**Stappen.**

1. Lees `kennisbank/security/meten-voordat-je-ingrijpt/README.md` volledig.
2. Maak `kennisbank/security/werkplekanalyse-e5/README.md`. Frontmatter volgens §3.3 met:
   `titel: Werkplekanalyse op het Microsoft-platform`, `herkomst: gegeneraliseerd uit een casus bij een
   gemeentelijke organisatie`, `status: in gebruik`, `barrieres: [execution, browser, localadmin]`,
   `rol: fundering`, `pijler: meten-voordat-je-ingrijpt`. Body volgens §3.4, waarbij *Zo richt je het in*
   de volledige sectie `## Werkplekanalyse op het Microsoft-platform (E5)` uit de pijler is, ongewijzigd.
   *Bewijs*: de queryresultaten (welke uitvoering feitelijk voorkomt) plus de afgedwongen ASR- en
   application-control-configuratie met dekking. *Zo leg je het uit*: schrijf drie regels op basis van
   de sectie *Managementsamenvatting* van de pijler; verzin niets. *Hoe dit samenhangt*: verwijs terug
   naar de pijler met `[Meten voordat je ingrijpt](../meten-voordat-je-ingrijpt/)` en zeg dat het
   uitgangspunt (meet eerst, grijp daarna in) daar staat.
3. Verplaats de zes KQL-bestanden:
   ```bash
   cd X:/SECURITY-COMMONS-NL/kennisbank
   git mv security/meten-voordat-je-ingrijpt/data security/werkplekanalyse-e5/data
   ```
   Zet in de nieuwe README onder *Zo richt je het in* een tabel met de zes bestanden als links
   (`[clickfix-detectie.kql](data/clickfix-detectie.kql)` enzovoort, allemaal). De build blokkeert anders
   op B3.
4. Maak `kennisbank/security/identiteit-en-mail-meten/README.md` op dezelfde manier uit de sectie
   `## Identiteit en e-mail`, met `titel: Identiteit en e-mail meten voordat je afdwingt`,
   `barrieres: [mail, pr, fallback]`, `rol: verdieping`, `pijler: meten-voordat-je-ingrijpt`.
5. Krimp de pijler. In `meten-voordat-je-ingrijpt/README.md`: vervang de sectie
   `## Werkplekanalyse op het Microsoft-platform (E5)` door een alinea van drie regels die zegt wat erin
   zat en linkt naar `[Werkplekanalyse op het Microsoft-platform](../werkplekanalyse-e5/)`. Idem voor
   `## Identiteit en e-mail` met een link naar `../identiteit-en-mail-meten/`. Vervang in de sectie
   `## Herbruikbare query's` de links naar `data/...` door links naar `../werkplekanalyse-e5/data/...`.
   Pas de frontmatter-`samenvatting` aan: noem de twee handleidingen.
6. Repareer de twee links naar de gearchiveerde repo. Open
   `security/risicoanalyse-aanvalspaden/index.html`, zoek `github.io/Handelingsperspectief/` (twee
   keer, rond regel 356 en 448) en vervang de hele `href="..."` door `href="../meten-voordat-je-ingrijpt/"`
   en de linktekst `Handelingsperspectief` door `Meten voordat je ingrijpt`. Controleer daarna dat de
   README van dat item dezelfde link al heeft (dat is zo); zo niet, ook daar.
7. Volgorde: open `security/README.md`, sectie `## Volgorde`. Zet de nieuwe items direct na
   `Meten voordat je ingrijpt`:
   ```
   1. [Meten voordat je ingrijpt](meten-voordat-je-ingrijpt/)
   2. [Werkplekanalyse op het Microsoft-platform](werkplekanalyse-e5/)
   3. [Identiteit en e-mail meten voordat je afdwingt](identiteit-en-mail-meten/)
   ```
   en hernummer de rest.
8. Leesversies:
   ```bash
   cd X:/SECURITY-COMMONS-NL/kennisbank
   python tools/leesversie.py security/werkplekanalyse-e5
   python tools/leesversie.py security/identiteit-en-mail-meten
   python tools/leesversie.py security/meten-voordat-je-ingrijpt
   python tools/build.py
   ```
9. Voeg aan `kennisbank/tools/test_build.py` toe: `test_geen_link_naar_gearchiveerde_repos`: loop over
   alle `*.md` en `index.html` onder de vakgebieden; geen enkele bevat `github.io/Handelingsperspectief`
   of `github.com/security-commons-nl/Handelingsperspectief`.

**Test.**
```bash
cd X:/SECURITY-COMMONS-NL/kennisbank && python tools/test_build.py && python tools/build.py --check
grep -rl "Handelingsperspectief" security/ governance/ ; echo "exit $?"
```
Verwacht: tests ok, geen overtredingen (11 items), en `grep` geeft geen bestanden (exit 1).
`handelingsperspectief.json` heeft nu 6 regels onder `handleidingen` en 38 namen onder
`zonder_handleiding`. (Zes: execution, browser, localadmin, mail, pr, fallback. `pr` en `fallback`
staan hier als verdieping; *Passkeys invoeren* wordt in Taak 3 de fundering.)

**Commit.**
```bash
git add security/werkplekanalyse-e5 security/identiteit-en-mail-meten security/meten-voordat-je-ingrijpt security/risicoanalyse-aanvalspaden/index.html security/README.md security/index.html index.html tools/test_build.py handelingsperspectief.json
git commit -m "security: meten-voordat-je-ingrijpt wordt een pijler met twee handleidingen eronder"
git push
```

---

### Taak 3: De shop-patronen worden handleidingen

**Doel.** 35 handleidingen uit 36 patronen (§3.2), in de volgorde van de tabel. Twee bestaande items
krijgen de communicatieregels erbij. Zeventien patronen worden issues.

**Stappen.**

1. Dump alle patronen naar markdown-concepten. Maak `security-shop/tools/dump.py`:
   ```python
   """Zet de patronen uit de mockup om naar markdown-concepten, een bestand per patroon, in _dump/.

   De concepten zijn grondstof: elke handleiding wordt daaruit met de hand geschreven volgens de vaste
   koppen. Dit script schrijft geen kennisbank-items.
   """
   import json, pathlib, re

   HIER = pathlib.Path(__file__).resolve().parent.parent
   t = (HIER / "mockup" / "index.html").read_text(encoding="utf-8")
   i = t.find("const PATTERNS"); j = t.find("];", i)
   blok = t[i:j]

   def veld(naam, bron):
       m = re.search(naam + r':\s*"((?:[^"\\]|\\.)*)"', bron)
       return m.group(1).replace('\\"', '"') if m else ""

   def lijst(naam, bron):
       m = re.search(naam + r":\s*\[(.*?)\]", bron, re.S)
       return re.findall(r'"((?:[^"\\]|\\.)*)"', m.group(1)) if m else []

   uit = HIER / "_dump"; uit.mkdir(exist_ok=True)
   n = 0
   for p in re.split(r"\n\s*\{\s*\n", blok):
       if "slug:" not in p:
           continue
       slug = veld("slug", p)
       comm = re.search(r"comm:\{(.*?)\n\s*\}", p, re.S)
       comm = comm.group(1) if comm else ""
       md = [f"# {veld('naam', p)}", "", f"slug: {slug}", f"rol in de shop: {veld('role', p)}",
             f"bio: {', '.join(lijst('bio', p))}", "", "## one", veld("one", p), "", "## gap", veld("gap", p),
             "", "## wanneer", veld("wanneer", p), "", "## hoe", veld("hoe", p), "", "## stappen"]
       md += [f"{k}. {s}" for k, s in enumerate(lijst("stappen", p), 1)]
       md += ["", "## voordelen"] + [f"- {s}" for s in lijst("voordelen", p)]
       md += ["", "## nadelen"] + [f"- {s}" for s in lijst("nadelen", p)]
       md += ["", "## kosten", veld("kosten", p), "", "## comm.directie", veld("directie", comm),
              "", "## comm.im", veld("im", comm), "", "## comm.mt", veld("mt", comm), ""]
       (uit / f"{slug}.md").write_text("\n".join(md), encoding="utf-8")
       n += 1
   print(f"{n} patronen naar {uit}")
   ```
   Draai `cd X:/SECURITY-COMMONS-NL/security-shop && python tools/dump.py`. Verwacht: `55 patronen`.
   Voeg `_dump/` toe aan `security-shop/.gitignore`. Controleer een concept met de hand:
   `_dump/centrale-logverzameling.md` heeft drie stappen en drie comm-regels. Zo niet: STOP.
2. Per rij in §3.2, in volgorde, en **een handleiding per commit**:
   a. Lees `_dump/<slug>.md`.
   b. Maak `kennisbank/security/<mapnaam>/README.md` met de frontmatter uit §3.3 en de body uit §3.4.
      Herschrijf, kopieer niet: de shop-tekst is geschreven als catalogus ("dit patroon..."), een
      handleiding spreekt de lezer aan ("je richt in..."). Elke technische bewering blijft zoals in het
      patroon; voeg geen beweringen toe.
   c. *Bewijs* begint met de tekst van het veld `bewijs` van het chokepoint in `paden.json` (zoek op
      `vraag_id`); maak daarna concreet wat je exporteert.
   d. *Hoe dit samenhangt*: bij een barriere met meerdere handleidingen (bijvoorbeeld `soc`), noem de
      andere met relatieve links (`[Co-managed SIEM](../co-managed-siem/)`). Werk die verwijzingen ook
      in de al geschreven handleidingen bij zodra er een alternatief bijkomt.
   e. `python tools/leesversie.py security/<mapnaam>` en `python tools/build.py`.
   f. Zet de map in `security/README.md` onder `## Volgorde`, onder de laatste handleiding.
   g. Commit: `git add security/<mapnaam> security/README.md security/index.html index.html handelingsperspectief.json`
      en `git commit -m "security: handleiding <mapnaam> (<barriere>)"`. Push na elke vijf.
3. Bij rij 16 (`endpoint-hardening` wordt `patchen-met-dekking`, barriere `patch`): het patroon gaat
   over hardening in het algemeen. Neem alleen het deel over patchen en bijgewerkt houden; verwijs voor
   ASR en lokale rechten naar `../werkplekanalyse-e5/` en `../application-control/`.
4. Bij rij 24 (`ir-procedures` wordt `incident-response-procedures`, barriere `mailresponse`): geef
   `barrieres: [mailresponse, idresponse, exploitresponse]` met `rol: fundering`. Dat is de enige
   handleiding met drie barrieres; *Bewijs* noemt dan drie geteste playbooks.
5. Bij rij 28: voeg de stappen van `ssdlc` en `dependency-scanning` samen tot een handleiding over
   testen van web en API in de ontwikkelketen. Laat SBOM en code signing weg (die worden issues).
6. Bij rij 33 (`mfa-handhaving-sanering`): `barrieres: [fallback, legacy]`, `rol: verdieping`. De
   fundering voor die twee is *Passkeys invoeren*; zie stap 8.
7. Na rij 35: controleer `kennisbank/handelingsperspectief.json`. `zonder_handleiding` bevat precies
   deze negen: `critical`, `ddosresponse`, `devicecode`, `dmarc`, `elevation`, `origin`, `owner`,
   `treatment`, `unmanaged`. Iets anders: STOP
   en meld welke barriere ontbreekt of te veel is.
8. Bestaande items verrijken. Open `security/passkeys-invoeren/README.md`: voeg aan de frontmatter toe
   `barrieres: [pr, fallback, legacy, key]` en `rol: fundering`; verander `type: aanpak` in
   `type: handleiding`; voeg de koppen *Bewijs* (de dekkingsrapportage van de authentication strength
   en het ontbreken van zwakkere methoden) en *Zo leg je het uit* toe, die laatste met de drie
   comm-regels uit `_dump/wachtwoordloos-passkeys.md`. Doe hetzelfde voor
   `security/security-annex-leveranciers/README.md` met `barrieres: [technicalvendor, review, residual]`,
   `rol: fundering`, comm-regels uit `_dump/security-annex-inkoop.md`. Type blijft daar `sjabloon`?
   Nee: een sjabloon met barrieres is een handleiding; zet `type: handleiding`. Leesversies opnieuw
   maken, build, commit `security: passkeys en security-annex dragen nu hun barrieres`.
   Open `security/blue-team-opzetten/README.md`: dit blijft `aanpak` (het is een methode, geen
   maatregel) en krijgt geen `barrieres:`. De dekking van `idresponse` en `exploitresponse` komt nu uit
   `incident-response-procedures`.
9. Issues voor wat geen barriere raakt. Voor elk van de zeventien slugs in §3.2 (lijst *niet
   overgezet*):
   ```bash
   gh issue create -R security-commons-nl/kennisbank --label idee \
     --title "Handleiding gevraagd: <naam uit het patroon>" \
     --body-file security-shop/_dump/<slug>.md
   ```
   Als het label `idee` niet bestaat in de kennisbank: eerst
   `gh label create idee -R security-commons-nl/kennisbank -d "Ruw idee, nog niet opgepakt." -c 0E8A16`.
   Verwacht: zeventien issues. Controleer met `gh issue list -R security-commons-nl/kennisbank --label idee | wc -l`.

**Test (na elke handleiding).**
```bash
cd X:/SECURITY-COMMONS-NL/kennisbank && python tools/build.py --check
```
Verwacht: geen overtredingen. Het aantal items in de melding loopt op tot 46 (9 + 2 + 35).

**Test (aan het eind van de taak).**
```bash
cd X:/SECURITY-COMMONS-NL/kennisbank && python tools/test_build.py && python tools/build.py
python -c "import json;d=json.load(open('handelingsperspectief.json',encoding='utf-8'));print(len(d['handleidingen']),'regels;',len({h['barriere'] for h in d['handleidingen']}),'barrieres gedekt;',len(d['zonder_handleiding']),'open')"
```
Verwacht: `... 35 barrieres gedekt; 9 open`.

---

### Taak 4: Aanvalspaden leest het handelingsperspectief in plaats van het te schrijven

**Doel.** `aanvalspaden/mappingen/handelingsperspectief.json` is een bewaakte kopie van de export uit de
kennisbank; het datamodel kent meerdere handleidingen per barriere met een rol; de pagina toont ze.

**Stappen.**

1. Nieuw formaat. Het bestand krijgt de structuur van de export uit Taak 1 stap 7 (`handleidingen` met
   `barriere`, `item`, `titel`, `rol`, `url`; en `zonder_handleiding`). De velden `gevraagd` en
   `geen_handleiding_nodig` uit de oude versie vervallen; de teksten *zou moeten dekken* verhuizen naar
   een nieuw bestand `mappingen/gevraagd.json` met per open barriere `cluster` en `zou_moeten_dekken`
   (neem ze over uit de huidige `handelingsperspectief.json`, alleen voor de negen open barrieres).
2. Kopieerscript. Maak `aanvalspaden/mappingen/bronnen/haal_handelingsperspectief.py`:
   ```python
   """Kopieert handelingsperspectief.json uit de kennisbank en legt de herkomst vast.

   Gebruik: python mappingen/bronnen/haal_handelingsperspectief.py [pad naar kennisbank]
   """
   import hashlib, json, pathlib, subprocess, sys
   HIER = pathlib.Path(__file__).resolve().parent
   bron_repo = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else HIER.parents[2] / "kennisbank"
   bron = bron_repo / "handelingsperspectief.json"
   data = json.loads(bron.read_text(encoding="utf-8"))
   commit = subprocess.run(["git", "-C", str(bron_repo), "log", "-1", "--format=%H"], capture_output=True, text=True).stdout.strip()
   data["bron"] = {"herkomst": "security-commons-nl/kennisbank, handelingsperspectief.json", "commit": commit,
                   "sha256": hashlib.sha256(bron.read_bytes()).hexdigest()}
   (HIER.parent / "handelingsperspectief.json").write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
   print(f"{len(data['handleidingen'])} handleidingen, {len(data['zonder_handleiding'])} open, commit {commit[:8]}")
   ```
   Draai het. Verwacht: `... 9 open`.
3. Helper. In `aanvalspaden/tools/mappingen.py`:
   - vervang `handleiding_van(barriere)` door `handleidingen_van(barriere) -> list[dict]`, gesorteerd
     op rol (fundering, alternatief, verdieping);
   - `gevraagd_van(barriere)` leest uit `mappingen/gevraagd.json`;
   - `schrijfopdrachten()` groepeert alleen nog de barrieres in `zonder_handleiding`, met de cluster
     uit `gevraagd.json`;
   - `dekking_handelingsperspectief()` telt `met_handleiding` als het aantal unieke barrieres in
     `handleidingen`, en `gevraagd` als `len(zonder_handleiding)`.
4. Bouw. In `mappingen/bouw.py`, `bouw_handelingsperspectief`: `handleidingen` wordt een dict van
   barriere naar **lijst**; `opdrachten` komt uit `schrijfopdrachten()`; voeg `gevraagd` toe uit
   `gevraagd.json`.
5. Pagina. In `mappingen/bron/app.js`, weergave *Hoe pak ik het aan*: per barriere een blok met de
   handleidingen als lijst (rol als vlag: fundering groen, alternatief blauw, verdieping grijs) en per
   handleiding een link naar `url`. Het "schrijf mee"-blok alleen voor barrieres in
   `zonder_handleiding`.
6. Tests. Pas `tests/test_handelingsperspectief.py` aan op het nieuwe formaat: elke barriere staat in
   `handleidingen` of in `zonder_handleiding`, nooit in beide; elke regel heeft `barriere`, `item`,
   `titel`, `rol`, `url`; bij meer regels per barriere is precies een `fundering`. Voeg
   `test_kopie_is_gelijk_aan_de_bron` toe: als `../kennisbank/handelingsperspectief.json` bestaat, is
   de sha256 gelijk aan `bron.sha256`. Pas `mappingen/tests/test_kennisbank_verwijzingen.py` aan:
   controleer per regel dat `item/README.md` bestaat en de kop `## Bewijs` heeft; de paragraafcontrole
   vervalt. Pas de browsertests aan: `test_elke_openstaande_opdracht_nodigt_uit_met_een_werkende_link`
   telt nu 9 blokken.
7. CI: in `aanvalspaden/.github/workflows/ci.yml`, job `mappingen`, na de checkout van `_kennisbank`,
   voeg een stap toe: `run: python mappingen/bronnen/haal_handelingsperspectief.py _kennisbank && git diff --exit-code mappingen/handelingsperspectief.json`
   met als naam `Kopie van het handelingsperspectief loopt niet achter`.
8. `mappingen/LEESMIJ.md` en `README.md`: sectie *Hoe pak ik het aan* herschrijven: de kennisbank is de
   bron, dit is een kopie, tellingen 35 van 44, negen open.

**Test.**
```bash
cd X:/SECURITY-COMMONS-NL/aanvalspaden && python mappingen/bouw.py && python -m pytest tests/ mappingen/tests/ check/tests/ -q
```
Verwacht: alles groen; de bouwregel meldt vier kaders en de pagina laadt in de browsertests.

**Commit.**
```bash
git add mappingen/handelingsperspectief.json mappingen/gevraagd.json mappingen/bronnen/haal_handelingsperspectief.py tools/mappingen.py mappingen/bouw.py mappingen/bron/app.js mappingen/bron/app.css tests/test_handelingsperspectief.py mappingen/tests/ .github/workflows/ci.yml mappingen/LEESMIJ.md README.md CHANGELOG.md BESLUITEN.md
git commit -m "mappingen: handelingsperspectief komt uit de kennisbank; meerdere handleidingen per barriere met een rol"
git push
```
Voeg vooraf aan `BESLUITEN.md` een regel toe (datum van uitvoering): de kennisbank is de bron van het
handelingsperspectief, aanvalspaden de afnemer, met de reden dat een handleiding maar op een plek
onderhouden moet worden.

---

### Taak 5: Security-shop sluiten, statuut en profiel bijwerken

**Doel.** De shop verwijst door en is gearchiveerd; het statuut kent geen ZTMM meer; de projectentabel
heeft geen rij `security-shop`.

**Stappen.**

1. Pas alleen na Taak 3 stap 7 (alle 35 handleidingen staan). Vervang `security-shop/README.md` door:
   ```markdown
   # security-shop

   Opgegaan in de kennisbank als handleidingen per barriere.

   Status: gearchiveerd. De 55 patronen uit deze catalogus zijn herschreven tot handleidingen in de
   [kennisbank](https://security-commons-nl.github.io/kennisbank/security/), elk gekoppeld aan een
   barriere uit de zelfcheck aanvalspaden. Wat geen barriere raakte, staat als idee in de
   [issues van de kennisbank](https://github.com/security-commons-nl/kennisbank/issues?q=label%3Aidee).

   ## Voor wie

   Lees de handleidingen op hun nieuwe plek.

   ## Snel starten

   Ga naar [Hoe pak ik het aan](https://security-commons-nl.github.io/aanvalspaden/normen/): per
   barriere de handleidingen, met de alternatieven ernaast.

   ## Bijdragen

   Via de kennisbank.

   ## Licentie

   EUPL-1.2, zie [LICENSE](LICENSE).
   ```
   Commit `readme: opgegaan in de kennisbank`, push. Daarna archiveren:
   `gh repo archive security-commons-nl/security-shop --yes`. De mockup op Pages blijft bereikbaar.
2. `.github/REDACTIESTATUUT.md`: verwijder in de B1-tabel de regel
   `| security-shop | ZTMM-pillar of cross-cutting capability |`.
3. `.github/profile/README.md`: verwijder de rij die begint met `| [security-shop]`. Voeg aan de alinea
   `**Gearchiveerd:**` toe: `en [security-shop](https://github.com/security-commons-nl/security-shop)
   (catalogus van patronen, opgegaan in de kennisbank als handleidingen per barriere)`.
4. `.github/BESLUITEN.md`: twee regels bovenaan (datum van uitvoering): (a) security-shop opgegaan in de
   kennisbank, reden: een tweede taxonomie over hetzelfde onderwerp, zonder tests of bijdragen, terwijl
   de inhoud precies de ontbrekende handleidingen was; (b) Handelingsperspectief wordt verwijderd,
   herroeping van het deel van 29-08-2026 dat de repo als doorverwijzing hield, reden: alle links zijn
   rechtgezet en een doorverwijzing zonder onderhoud wordt een dode link met een verkeerde naam.
5. `.github/ARCHITECTUUR.md`: in de groep *Instrumenten* `security-shop` weghalen en aan
   *gearchiveerd* toevoegen; in de tabel van *De barriere als scharnier* de rij *Hoe pak ik het aan*
   veranderen in `kennisbank (bron), gekopieerd naar aanvalspaden/mappingen/` met stand `35 van de 44`;
   peildatum bovenaan op de datum van uitvoering. Werk `architectuur-landschap.svg` bij: het blok
   `security-shop` uit de strook INSTRUMENTEN halen, in de strook GEARCHIVEERD een regel `security-shop`
   met `naar kennisbank, als handleidingen` erbij, en in het blok `handelingsperspectief` de regel
   `14 van 44, 11 opdrachten` vervangen door `35 van 44, kennisbank is de bron`. Werk
   `architectuur-scharnier.svg` bij: de regel `LIVE SINDS 30-08-2026 · 14 van 44 barrieres` wordt
   `LIVE · 35 van 44 barrieres · bron: kennisbank`. Controleer beide met
   `python -c "import xml.etree.ElementTree as E;E.parse('architectuur-landschap.svg');E.parse('architectuur-scharnier.svg');print('ok')"`.
6. Commit `.github`: `git add REDACTIESTATUUT.md profile/README.md BESLUITEN.md ARCHITECTUUR.md architectuur-landschap.svg architectuur-scharnier.svg` en
   `git commit -m "profiel: security-shop opgegaan in de kennisbank; architectuur en statuut bijgewerkt"`, push.
7. Voorpagina opnieuw genereren (commando's in §0.2) en committen in `security-commons-nl.github.io`:
   `git add llms.txt sitemap.xml && git commit -m "llms.txt en sitemap: opnieuw gegenereerd na wijziging in de projectentabel" && git push`.

**Test.**
```bash
cd X:/SECURITY-COMMONS-NL/.github && for r in kennisbank aanvalspaden security-shop; do python tools/repo_compliance.py ../$r --profiel profile/README.md; done
cd X:/SECURITY-COMMONS-NL/security-commons-nl.github.io && python -m pytest site/test_voorpagina.py -q
grep -c "security-shop" X:/SECURITY-COMMONS-NL/security-commons-nl.github.io/dist/index.html
```
Verwacht: drie keer `Repo voldoet aan het statuut`; test groen; de laatste `grep` geeft `1` (alleen in
de gearchiveerd-alinea).

---

### Taak 6: Handelingsperspectief verwijderen

**Doel.** De gearchiveerde repo bestaat niet meer, en niets verwijst er nog naar.

**Stappen.**

1. Voorwaarden, alle drie controleren:
   a. Taak 2 is af (de test `test_geen_link_naar_gearchiveerde_repos` bestaat en is groen).
   b. Over alle repo's heen:
      ```bash
      cd X:/SECURITY-COMMONS-NL && grep -rl "Handelingsperspectief" --include="*.md" --include="*.html" --include="*.txt" --include="*.xml" --include="*.json" . 2>/dev/null | grep -v node_modules | grep -v "/\.git/" | grep -v "^./Handelingsperspectief/" | grep -v "^./2026-" | grep -v "plannen/"
      ```
      Verwacht: geen uitvoer. Is er uitvoer: repareer die verwijzingen eerst (vervang door de pijler),
      commit in de betreffende repo, en herhaal.
   c. Het open punt uit het besluit van 29-08-2026 ("de inbrenger van de casus bijpraten") is gedaan.
      Dat kun jij niet controleren: **vraag het aan de eigenaar en wacht op ja.**
2. Meld aan de eigenaar: "Handelingsperspectief kan weg. Intern verwijst niets er meer naar. Verwijderen
   doe je op https://github.com/security-commons-nl/Handelingsperspectief/settings onderaan, Delete this
   repository. Dat is onomkeerbaar." **Verwijder zelf niets.**
3. Na bevestiging dat de repo weg is: `rm -rf X:/SECURITY-COMMONS-NL/Handelingsperspectief` en in
   `.github/profile/README.md` de vermelding van Handelingsperspectief uit de gearchiveerd-alinea halen
   (het item bestaat niet meer, dus ook niet als archief). Commit `profiel: Handelingsperspectief
   verwijderd`, push, voorpagina opnieuw genereren en committen.

**Test.**
```bash
curl -s -o /dev/null -w "%{http_code}\n" https://github.com/security-commons-nl/Handelingsperspectief
```
Verwacht: `404`. En de grep uit stap 1b geeft geen uitvoer.

---

### Taak 7: De site vertelt de keten

**Doel.** Wie op de voorpagina komt, ziet de vier vragen en waar het antwoord staat.

**Stappen.**

1. `.github/profile/README.md`, sectie `## Direct aan de slag`. Vervang de alinea die begint met
   `Alles hieronder werkt vandaag` door:
   ```
   Alles hieronder werkt vandaag, in je browser, zonder account en zonder factuur. De kern is een keten
   van vier vragen rond de achttien aanvalspaden van de publieke sector:

   1. **Hoe sta ik ervoor?** De [zelfcheck](https://security-commons-nl.github.io/aanvalspaden/): een uur, alleen te doen, achttien paden en drie acties voor morgen.
   2. **Hoe pak ik het aan?** Per barriere een [handleiding in de kennisbank](https://security-commons-nl.github.io/aanvalspaden/normen/), met de alternatieven ernaast, en een uitnodiging waar er nog geen is.
   3. **Wat toon ik hiermee aan?** De [normverankering](https://security-commons-nl.github.io/aanvalspaden/normen/): BIO 2.0, ISO 27001, NIST CSF 2.0, het Wpg-kader en de AVG, en waar de zelfcheck ophoudt.
   4. **Wat zegt mijn eigen data?** De meting, in ontwikkeling in `security-posture-tool`.

   Begin bij de [kennisbank](https://security-commons-nl.github.io/kennisbank/) als je iets zoekt om te lezen
   of te hergebruiken, en bij de [weerbaarheidsgame](https://security-commons-nl.github.io/weerbaarheid-game/)
   als je het gesprek met bestuurders voert.
   ```
2. In de projectentabel, rij `aanvalspaden`: vervang `Eén instrument in drie diepten` door
   `Eén instrument rond vier vragen` en `Met de normverankering erbij` door `Met de normverankering en
   de handleidingen per barriere erbij`.
3. Kennisbank-voorpagina: in `kennisbank/tools/build.py`, `bouw_root`, voeg na het blok *Direct te lezen*
   een regel toe:
   `<p class="h2sub">Handleidingen per barriere uit de zelfcheck staan bij <a href="security/#handleidingen">Security</a>, en met de alternatieven ernaast op <a href="https://security-commons-nl.github.io/aanvalspaden/normen/">Van aanvalspad naar norm</a>.</p>`
   en geef in `bouw_sectie` de `h3.groep` van de handleidingen `id="handleidingen"`.
4. `aanvalspaden/README.md`, dieptetabel: voeg een vierde regel toe *Handleiding* met "Hoe pak ik het
   aan?", "Kennisbank, per barriere" en de link naar `/normen/`.
5. Commit in `.github` (`profiel: de voorpagina vertelt de keten in vier vragen`), voorpagina opnieuw
   genereren en committen in `security-commons-nl.github.io`, commit in `kennisbank`
   (`tools: kennisbank-voorpagina verwijst naar de handleidingen`), commit in `aanvalspaden`
   (`readme: de vierde vraag`).

**Test.**
```bash
cd X:/SECURITY-COMMONS-NL/security-commons-nl.github.io && node site/build.mjs && python -m pytest site/test_voorpagina.py -q && grep -c "aanvalspaden/normen/" dist/index.html
```
Verwacht: test groen en `2` (twee keer de link, bij vraag 2 en 3).

---

### Taak 8: Eindcontrole van alle links, over alle repo's heen

**Doel.** Bewijs dat elke interne link (naar een pagina op `security-commons-nl.github.io` of een repo op
`github.com/security-commons-nl`) ergens op uitkomt. Dit is de laatste poort; zonder groen is het plan
niet af.

**Stappen.**

1. Maak `.github/tools/linkcheck.py`:
   ```python
   """Controleert elke link naar de commons zelf, over alle repo's in de werkmap heen.

   Gebruik: python tools/linkcheck.py <werkmap>       (de map met alle repo's naast elkaar)
   Exit 1 als een link nergens op uitkomt. Externe sites worden niet gecontroleerd.
   """
   import pathlib, re, sys, urllib.request

   WERKMAP = pathlib.Path(sys.argv[1]).resolve()
   SITE = "https://security-commons-nl.github.io/"
   REPO = "https://github.com/security-commons-nl/"
   LINK = re.compile(r'(?:href="|\]\()(https://(?:security-commons-nl\.github\.io|github\.com/security-commons-nl)/[^)"#\s]*)')
   BESTANDEN = ("*.md", "*.html", "*.txt", "*.xml", "*.json", "*.js")
   OVERSLAAN = ("node_modules", ".git", "_dump", "dist", "_kennisbank", "_aanvalspaden")

   def lokaal(url: str) -> pathlib.Path | None:
       """Vertaal een site- of repo-URL naar een pad in de werkmap; None als dat niet kan."""
       if url.startswith(SITE):
           rest = url[len(SITE):].strip("/")
           if not rest:
               return WERKMAP / "security-commons-nl.github.io" / "dist" / "index.html"
           repo, _, pad = rest.partition("/")
           kandidaat = WERKMAP / repo / (pad or "")
           if repo == "aanvalspaden":
               return None  # gebouwde site; via HTTP controleren
           return kandidaat / "index.html" if kandidaat.is_dir() else kandidaat
       if url.startswith(REPO):
           rest = url[len(REPO):].strip("/")
           repo, _, pad = rest.partition("/")
           if pad.startswith(("issues", "discussions", "pulls", "settings")):
               return None  # GitHub-functie, via HTTP
           pad = re.sub(r"^(blob|tree)/main/", "", pad)
           return WERKMAP / repo / pad if pad else WERKMAP / repo
       return None

   def http_ok(url: str) -> bool:
       try:
           req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "linkcheck"})
           return urllib.request.urlopen(req, timeout=15).status < 400
       except Exception:
           return False

   fouten = []
   gezien = {}
   for patroon in BESTANDEN:
       for pad in WERKMAP.rglob(patroon):
           if any(o in pad.parts for o in OVERSLAAN):
               continue
           for url in set(LINK.findall(pad.read_text(encoding="utf-8", errors="replace"))):
               if url not in gezien:
                   doel = lokaal(url)
                   gezien[url] = doel.exists() if doel is not None else http_ok(url)
               if not gezien[url]:
                   fouten.append(f"{pad.relative_to(WERKMAP)}: {url}")
   for f in sorted(set(fouten)):
       print("DOOD:", f)
   print(f"{len(gezien)} unieke links, {len(set(fouten))} dood")
   sys.exit(1 if fouten else 0)
   ```
2. Draai: `cd X:/SECURITY-COMMONS-NL/.github && python tools/linkcheck.py ..`. Verwacht: `... 0 dood`.
   Elke regel `DOOD:` is werk: repareer de link in de genoemde bron, commit in die repo, en draai
   opnieuw tot het nul is.
3. Draai daarna de volledige testreeks nog een keer, in deze volgorde:
   ```bash
   cd X:/SECURITY-COMMONS-NL/kennisbank && python tools/test_build.py && python tools/build.py --check
   cd X:/SECURITY-COMMONS-NL/aanvalspaden && python -m pytest tests/ mappingen/tests/ check/tests/ -q
   cd X:/SECURITY-COMMONS-NL/.github && for r in kennisbank aanvalspaden security-shop weerbaarheid-game grc-platform; do python tools/repo_compliance.py ../$r --profiel profile/README.md; done
   cd X:/SECURITY-COMMONS-NL/security-commons-nl.github.io && python -m pytest site/test_voorpagina.py -q
   ```
4. Controleer live, in een browser (Playwright), dat de vier vragen op de voorpagina staan en dat
   *Hoe pak ik het aan* op `/normen/` 35 barrieres met handleiding toont en 9 met een "schrijf mee"-knop:
   ```bash
   cd X:/SECURITY-COMMONS-NL/aanvalspaden && python -W ignore -c "
   from playwright.sync_api import sync_playwright
   with sync_playwright() as p:
       b=p.chromium.launch(); pg=b.new_page()
       pg.goto('https://security-commons-nl.github.io/aanvalspaden/normen/'); pg.wait_for_selector('.bedien button')
       pg.get_by_role('button', name='Hoe pak ik het aan').click(); pg.wait_for_timeout(400)
       print('schrijf-mee-knoppen:', pg.locator('.blok.gevraagd a.knop').count())
       print('telling:', pg.locator('.telling .groot').all_inner_texts())
       pg.goto('https://security-commons-nl.github.io/'); print('vier vragen:', pg.locator('main').inner_text().count('Hoe pak ik het aan')>0)
       b.close()"
   ```
   Verwacht: `schrijf-mee-knoppen: 9`, telling begint met `35`, `vier vragen: True`.
5. Commit `linkcheck.py` in `.github` (`tools: linkcontrole over alle repo's`), en voeg aan
   `.github/README`-loze root niets toe; documenteer het commando in `CONTRIBUTING.md` onder een kop
   `## Links controleren`.
6. Werk `.github/plannen/2026-08-30-rationalisatie.md` bij: zet `[x]` bij elke afgeronde taak en zet
   bovenaan de regel `**Uitgevoerd op: <datum>. Alle tests en de linkcontrole groen.**` Commit
   `plannen: rationalisatie uitgevoerd`.

**Klaar als:** linkcheck `0 dood`, alle vier de testblokken groen, de live controle klopt, en alle
repo's gepusht met groene CI (`gh run list -R security-commons-nl/<repo> --limit 1` voor kennisbank,
aanvalspaden, .github en security-commons-nl.github.io).

---

## 5. Als er iets misgaat

- **`build.py --check` meldt `paden.json niet gevonden`:** de aanvalspaden-repo staat niet naast de
  kennisbank. Controleer `ls X:/SECURITY-COMMONS-NL/aanvalspaden/paden.json`.
- **Een handleiding uit de shop bevat een bewering die je niet kunt plaatsen** (een productnaam, een
  cijfer, een norm die niet in §3.1 of de BIO-mapping van het patroon staat): laat hem weg en schrijf in
  de commitboodschap `weggelaten: <bewering>`. Verzin geen vervanging.
- **Een test faalt op iets wat je niet hebt aangeraakt:** STOP, meld de test en de foutmelding. Pas
  geen tests aan om ze groen te krijgen, behalve waar dit plan dat expliciet zegt.
- **`gh` geeft een scope-fout** (`read:project`, `delete_repo`): dat is verwacht; de betreffende
  handeling is voor een mens. Meld het en ga door met de rest.
- **De sha256-test in Taak 4 faalt na een kennisbank-commit:** draai
  `python mappingen/bronnen/haal_handelingsperspectief.py` opnieuw in aanvalspaden en commit de kopie.
  Dat is de bedoeling: de kopie volgt de bron.
- **Twijfel over wat "de eigenaar" wil:** de besluiten in §2 zijn de opdracht. Alles wat daar niet
  onder valt, is een vraag, geen aanname.
