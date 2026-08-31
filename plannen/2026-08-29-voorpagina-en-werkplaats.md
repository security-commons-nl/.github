# Bouwplan: de voorpagina voor gebruikers, de werkplaats voor bouwers

> **Voor agentische uitvoerders:** werk taak voor taak, in volgorde. Een taak is klaar als de controle in
> die taak groen is en de commit gedaan is. Lees eerst de spec (paragraaf 0) en de vaste regels. Sla niets
> over en vul niets "later" in. Elke taak zegt precies welke bestanden, welke tekst en welk commando.
>
> Versie 2, 29-08-2026: herschreven na een onafhankelijke review met 25 bevindingen (vijf blokkerend).
> De wijzigingen staan onderaan in "Wat de review veranderde".

**Doel:** security-commons-nl.github.io wordt de voorpagina voor de gebruiker in de publieke sector (CISO,
ISO, bestuurder), met hetzelfde verhaal als op GitHub maar in de volgorde van de gebruiker. GitHub.com
wordt de werkplaats voor bijdragers en onderhoud, en die werkplaats krijgt een norm die wordt afgedwongen
in plaats van beschreven.

**Architectuur:** één bron blijft één bron. Het org-profiel (`.github/profile/README.md`) blijft de enige
projectenlijst (statuut B9) en wordt herordend naar gebruiker-eerst; de site-build maakt daaruit de
voorpagina met drie uitgelichte kaarten, afgeleid uit de tabel en niet overgetikt. Voor de werkplaats komt
er één herbruikbare controle (`repo-compliance.yml` in `.github`) die in elke levende repo draait en de
README-kop, de licentie en de status-consistentie met het profiel afdwingt. De bestaande
documentatiestandaard wordt teruggebracht tot wat haalbaar is en wél gecontroleerd wordt.

**Tech stack:** Node 24 + marked (site-build, bestaat; `npm ci` in de io-repo), Python 3.12 met `pytest`
voor de tests (het controlescript zelf gebruikt alleen de standaardbibliotheek), GitHub Actions
herbruikbare workflows in `security-commons-nl/.github`.

**Spec:** paragraaf 0 hieronder, uit de spar van 29-08-2026.

---

## Stand van uitvoering (29-08-2026, uitgevoerd)

| Taak | Stand |
|---|---|
| 1 Statuut, besluit, controle | Klaar. B8, B9, B11, B12 in het statuut; `repo_compliance.py` met 10 tests, groen in CI |
| 2 Profiel gebruiker-eerst | Klaar. Koppen in de nieuwe volgorde, bijdragersgids naar CONTRIBUTING, 21 em-dashes weg |
| 3 Voorpagina | Klaar en live: drie kaarten uit de tabel, `ci.yml` bewaakt de test |
| 4 Documentatiestandaard | Klaar. Teruggebracht tot de README-kop; `doc-compliance.yml` verwijderd |
| 5 Uitrol | Klaar. 19 repo's groen op de controle en in CI; `procescheck` rood op B5 (open besluit) |
| 6 Archiveren | Vervallen: `dreigingsanalyse` staat niet op GitHub, zie hieronder |
| 7 llms.txt | Klaar. Leesroute voor leveranciers, journalisten en onderzoekers |

**Twee dingen bleken tijdens de bouw anders dan het plan aannam:**

1. `dreigingsanalyse` heeft geen remote en bestaat niet op GitHub; het is een lokale map die nooit
   gepubliceerd is. De verwijzing in het profiel gaf daardoor een 404 en is verwijderd; de repo telt niet
   mee in de controle en hoeft niet gearchiveerd te worden. Vastgelegd in de commons-`CLAUDE.md`.
2. `procescheck` staat onder GPL-3 en blijft dus rood op B5. Dat is het open besluit onderaan dit plan,
   niet een gemiste stap.

---

## 0. Spec: wat Bas heeft besloten

1. **Eerste lezer is de gebruiker** in de publieke sector. De voorpagina opent met wat je vandaag kunt
   doen, niet met waarom de commons bestaat en niet met hoe je bijdraagt.
2. **Zelfde verhaal, andere volgorde.** De voorpagina en het GitHub-profiel vertellen hetzelfde; er komt
   geen tweede bron. Vermoeden van Bas: de .io resoneert bij gewone gebruikers veel beter dan repo's.
3. **Normeer de werkplaats.** Elke repo dezelfde kop, en een controle die dat afdwingt. Nu is de
   documentatiestandaard een tekst die niemand controleert.
4. **Andere doelgroepen** (leveranciers, journalisten) krijgen geen eigen voorpagina; als het nodig is
   komt er een route in `llms.txt`.

## Wat er nu is (peildatum 29-08-2026, gecontroleerd tegen de repo's)

- De voorpagina wordt gegenereerd uit het profiel. Dat opent met "Waarom dit bestaat" (vier alinea's
  overtuiging), dan de projectentabel (17 rijen, kolommen Status en Doelgroep; de build rendert die als
  kaartengrid, niet als tabel), dan "Meedoen" en "Voor het eerst hier?" met een tabel met issue-formulieren
  per repo. Een gebruiker ziet dus eerst een manifest en een repo-overzicht.
- Er zijn 23 repo's: 22 projectrepo's plus `.github`. Vijf projectrepo's staan niet in de tabel:
  `anonimizer-proxy` (infrastructuur, in proza genoemd), `security-commons-nl.github.io` (infrastructuur,
  nergens genoemd), `anonimizer-web` en `beleid-assistent` (gearchiveerd, in proza genoemd) en
  `dreigingsanalyse` (opgegaan in de kennisbank, nergens genoemd).
- De documentatiestandaard eist `docs/gebruik.md`, `docs/architectuur.md` en `docs/configuratie.md`.
  Werkelijkheid: 2 van de 22 hebben ze volledig (grc-platform en het gearchiveerde anonimizer-web);
  weerbaarheid-game mist alleen configuratie. Zeven repo's roepen `doc-compliance.yml` aan, maar met alle
  eisen op `false`. De norm is zwaarder dan de praktijk en wordt daarom omzeild.
- Zes repo's hebben geen enkele CI (beleid-assistent, cisochat, dreigingsanalyse, hosting-bouwblokken,
  policy-as-code, weerbaarheid-game). Drie missen een LICENSE (dreigingsanalyse, security-shop, `.github`),
  en `procescheck` heeft er een die geen EUPL is (GPL-3). Dat laatste is een keuze voor de
  auteursrechthebbende, geen taak; zie "Open besluit" onderaan.
- Status staat op twee plekken: in de tabel en in de README van de repo. Niets houdt die gelijk.
- Het profiel bevat 21 em-dashes, waarvan 10 als "geen link"-teken in de kolom "Direct openen"; ook de
  `title` in `build.mjs` heeft er een. Het statuut (A10) wil ze niet.
- README-lengte loopt van 81 woorden (beleid-assistent, dreigingsanalyse) tot 2673 (publicatiescan).

## Vaste regels (gelden voor elke taak)

- **Statuut eerst.** Alles volgt `.github/REDACTIESTATUUT.md`. Geen namen van personen, geen
  organisatienamen, geen sociale-medialinks, geen AI-attributie, geen em-dash (gebruik een komma, punt
  of gewoon streepje).
- **Één schrijver per bestand.** Wijzig het profiel alleen in de `.github`-repo; de site-build kopieert.
- **Gearchiveerde repo's blijven met rust.** `anonimizer-web` en `beleid-assistent` zijn gearchiveerd op
  GitHub; daar kun je niet naar pushen. Ze krijgen geen workflow en geen README-wijziging.
- **Expliciet stagen.** Nooit `git add -A`; noem elk bestand. Vóór elke commit `git pull --rebase`.
- **Bewijs vóór klaar.** Elke taak eindigt met een controle die je uitvoert en waarvan je de uitkomst
  noteert. Een taak zonder groene controle is niet klaar.
- **Regeleinden LF.** Schrijf bestanden binair of met `newline="\n"`; git slaat LF op.
- **Geen heredocs met backslashes** in de Bash-tool; die eet een niveau op. Zet scripts in een bestand.
- **Voorbereiding, één keer:** `pip install pytest` en, in `security-commons-nl.github.io`, `npm ci`.

---

## Taak 1: Statuut, besluit en de controle, in één werkgang

Het statuut zegt: scripts die regels controleren worden in dezelfde wijziging bijgewerkt. Daarom zitten de
nieuwe regels en het script dat ze afdwingt in één commit.

**Bestanden (repo `.github`):**
- Modify: `REDACTIESTATUUT.md` (B8 en B9 preciseren, B11 en B12 toevoegen)
- Modify: `BESLUITEN.md` (één entry bovenaan)
- Create: `LICENSE` (EUPL-1.2; de repo heeft er geen)
- Create: `tools/repo_compliance.py`, `tools/test_repo_compliance.py`
- Create: `.github/workflows/repo-compliance.yml` (herbruikbaar) en `.github/workflows/tools-ci.yml` (de
  tests van het script zelf)

**Interfaces:**
- Produces: `python tools/repo_compliance.py <repo-map> --profiel <profile/README.md>`; exitcode 0 bij
  groen, 1 bij een overtreding; elke melding noemt de regel: B5, B9, B11, B12 of A5.
- Produces: de herbruikbare workflow `security-commons-nl/.github/.github/workflows/repo-compliance.yml@main`.

- [x] **Stap 1: B8 aanvullen.** Voeg onder de tabel met de vier labels in B8 een alinea toe:

```markdown
Een repo die geen project is maar infrastructuur (een proxy, de site-build) draagt in zijn README het
label `infrastructuur`, staat niet in de projectentabel maar in de alinea "Onderliggende infrastructuur"
eronder, en wordt wel gecontroleerd op de README-kop en de licentie (B11, B5).
```

- [x] **Stap 2: B9 preciseren.** Vervang de tekst van B9 door:

```markdown
**B9. Het org-profiel is de enige projectenlijst.** `.github/profile/README.md` bevat de projectentabel; de
voorpagina, `llms.txt`, `sitemap.xml` en de root-`CLAUDE.md` worden daaruit gegenereerd of afgeleid. Een
project bestaat pas als het in die tabel staat, met label en doelgroep. De volgorde van de tabel is
redactioneel: de eerste drie rijen met een live link zijn de uitgelichte kaarten op de voorpagina. Repo's
die geen project zijn (infrastructuur, gearchiveerd, opgegaan in een ander project) staan in de alinea's
onder de tabel, met de reden erbij; `repo-compliance.yml` eist dat elke repo op een van die plekken staat.
```

- [x] **Stap 3: B11 en B12 toevoegen**, direct na B10:

```markdown
**B11. Elke repo heeft dezelfde kop.** De README van elke levende repo begint met: de naam als `#`-kop, één
zin wat het is en voor wie, een regel `Status: <label>.` met daarachter in gewone woorden wat werkt en wat
niet, en daarna de koppen `## Voor wie`, `## Snel starten`, `## Bijdragen` en `## Licentie`, in die
volgorde. Meer mag, minder niet. Een aparte `docs/`-map is alleen nodig als de README anders langer dan
ongeveer 1500 woorden wordt. Reden: een bezoeker die van de voorpagina doorklikt naar GitHub moet in tien
seconden zien wat het is, of het werkt en hoe hij begint. `repo-compliance.yml` controleert dit.

**B12. Status staat op één plek.** Het label in de projectentabel is de bron. De regel `Status:` in de
README van de repo herhaalt dat label letterlijk; `repo-compliance.yml` vergelijkt beide en wordt rood
als ze verschillen. Wie een status wijzigt, wijzigt eerst de tabel.
```

- [x] **Stap 4: Besluit loggen.** Voeg bovenaan in `BESLUITEN.md`, direct onder de inleiding, toe:

```markdown
## 29-08-2026 · De voorpagina is voor de gebruiker; de werkplaats krijgt een norm die wordt afgedwongen

De landingspagina opende met een manifest en een repo-overzicht; een CISO die iets zoekt om vandaag te
gebruiken moest daar doorheen. Besloten: de voorpagina opent met wat je kunt doen, in de volgorde van de
gebruiker; het verhaal blijft hetzelfde en de bron blijft één bestand (B9, gepreciseerd). Tegelijk bleek
de documentatiestandaard zwaarder dan de praktijk (2 van 22 repo's voldeden) en werd hij daarom omzeild.
Vervangen door een README-kop die haalbaar is (B11), een status die op één plek woont (B12), een label
voor infrastructuur (B8), en één herbruikbare controle die dit afdwingt.
Bouwplan: `2026-08-29-bouwplan-voorpagina-en-werkplaats.md`.
```

- [x] **Stap 5: LICENSE.** Kopieer `X:\SECURITY-COMMONS-NL\kennisbank\LICENSE` naar `.github\LICENSE`.

- [x] **Stap 6: Falende tests** in `tools/test_repo_compliance.py`:

```python
"""De controle op een repo: README-kop (B11), licentie (B5), status gelijk aan het profiel (B12),
plaats in het profiel (B9), geen sociale media (A5)."""
import pathlib
import subprocess
import sys
import textwrap

HIER = pathlib.Path(__file__).resolve().parent
PROFIEL = textwrap.dedent("""\
    | Project | Status | Wat is het? | Direct openen | Doelgroep |
    |---|---|---|---|---|
    | [voorbeeld](https://github.com/security-commons-nl/voorbeeld) | prototype | Iets | | CISO's |

    **Gearchiveerd:** [oud](https://github.com/security-commons-nl/oud) (vervangen).
    **Onderliggende infrastructuur:**
    [ander](https://github.com/security-commons-nl/ander) (proxy).
    """)
GOED = textwrap.dedent("""\
    # voorbeeld

    Eén zin: wat het is en voor wie.

    Status: prototype. Werkt lokaal, geen installatiepakket.

    ## Voor wie
    ## Snel starten
    ## Bijdragen
    ## Licentie
    """)
LICENTIE = "EUROPEAN UNION PUBLIC LICENCE v. 1.2\n"


def draai(tmp: pathlib.Path, readme: str, naam: str = "voorbeeld", licentie: bool = True,
          profiel: str = PROFIEL) -> tuple[int, str]:
    repo = tmp / naam
    repo.mkdir()
    (repo / "README.md").write_text(readme, encoding="utf-8")
    if licentie:
        (repo / "LICENSE").write_text(LICENTIE, encoding="utf-8")
    prof = tmp / "profiel.md"
    prof.write_text(profiel, encoding="utf-8")
    p = subprocess.run([sys.executable, str(HIER / "repo_compliance.py"), str(repo), "--profiel", str(prof)],
                       capture_output=True, text=True)
    return p.returncode, p.stdout + p.stderr


def test_goede_repo_is_groen(tmp_path):
    code, uit = draai(tmp_path, GOED)
    assert code == 0, uit


def test_ontbrekende_kop_is_b11(tmp_path):
    code, uit = draai(tmp_path, GOED.replace("## Snel starten\n", ""))
    assert code == 1 and "B11" in uit and "Snel starten" in uit


def test_verkeerde_volgorde_is_b11(tmp_path):
    verkeerd = GOED.replace("## Voor wie\n## Snel starten\n", "## Snel starten\n## Voor wie\n")
    code, uit = draai(tmp_path, verkeerd)
    assert code == 1 and "B11" in uit and "volgorde" in uit


def test_status_anders_dan_profiel_is_b12(tmp_path):
    code, uit = draai(tmp_path, GOED.replace("Status: prototype", "Status: in gebruik"))
    assert code == 1 and "B12" in uit


def test_status_met_hoofdletter_telt_als_label(tmp_path):
    code, uit = draai(tmp_path, GOED.replace("Status: prototype", "Status: Prototype"))
    assert code == 0, uit


def test_geen_licentie_is_b5(tmp_path):
    code, uit = draai(tmp_path, GOED, licentie=False)
    assert code == 1 and "B5" in uit


def test_sociale_link_is_a5(tmp_path):
    code, uit = draai(tmp_path, GOED + "\nZie https://www.linkedin.com/in/iemand\n")
    assert code == 1 and "A5" in uit


def test_repo_buiten_profiel_is_b9(tmp_path):
    code, uit = draai(tmp_path, GOED.replace("# voorbeeld", "# zwerver"), naam="zwerver")
    assert code == 1 and "B9" in uit


def test_infrastructuur_uit_de_alinea_mag(tmp_path):
    readme = GOED.replace("# voorbeeld", "# ander").replace("Status: prototype", "Status: infrastructuur")
    code, uit = draai(tmp_path, readme, naam="ander")
    assert code == 0, uit


def test_gearchiveerd_over_een_regeleinde_wordt_gevonden(tmp_path):
    readme = GOED.replace("# voorbeeld", "# oud").replace("Status: prototype", "Status: gearchiveerd")
    code, uit = draai(tmp_path, readme, naam="oud")
    assert code == 0, uit
```

- [x] **Stap 7: Run, verwacht FAIL** (`python -m pytest tools/ -q` in `.github`; het script bestaat niet).

- [x] **Stap 8: Het script** `tools/repo_compliance.py`:

```python
#!/usr/bin/env python3
"""Controleert één repo tegen het redactiestatuut.

  B5   LICENSE aanwezig en EUPL-1.2
  B9   de repo staat in de projectentabel of in een alinea eronder (gearchiveerd, infrastructuur)
  B11  README-kop: #-kop, Status-regel, en de vier koppen in de vaste volgorde
  B12  het label in de README is het label uit het profiel
  A5   geen links naar sociale media in markdown

Gebruik: python repo_compliance.py <repo-map> --profiel <profile/README.md>
Exitcode 0 = groen, 1 = één of meer overtredingen. Alleen standaardbibliotheek.
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

KOPPEN = ["Voor wie", "Snel starten", "Bijdragen", "Licentie"]
LABELS = {"in gebruik", "prototype", "concept", "gearchiveerd", "infrastructuur"}
SOCIAAL = re.compile(r"https?://(?:[a-z0-9-]+\.)*(linkedin\.com|x\.com|twitter\.com|facebook\.com|instagram\.com|tiktok\.com|threads\.net)", re.I)
OVERSLAAN = {".git", "node_modules", "dist", "org-profile", "_wachtkamer", ".venv"}


def status_in_profiel(profiel: str, naam: str) -> str | None:
    """Het label uit de tabel, of 'gearchiveerd' / 'infrastructuur' uit de alinea's eronder, of None."""
    for regel in profiel.splitlines():
        m = re.match(r"\| \[([^\]]+)\]\([^)]*\) \| ([a-z ]+?) \|", regel)
        if m and m.group(1) == naam:
            return m.group(2).strip()
    plat = " ".join(profiel.split())  # alinea's kunnen over regeleinden lopen
    for kop, label in (("Gearchiveerd", "gearchiveerd"), ("Onderliggende infrastructuur", "infrastructuur")):
        m = re.search(r"\*\*" + kop + r":\*\*(.*?)(?=\*\*[A-Z][^*]*:\*\*|## |$)", plat)
        if m and re.search(r"\[" + re.escape(naam) + r"\]", m.group(1)):
            return label
    return None


def markdown_bestanden(repo: Path) -> list[Path]:
    """Getrackte markdown als het een git-repo is; anders alles behalve de bekende rommelmappen."""
    try:
        uit = subprocess.run(["git", "-C", str(repo), "ls-files", "*.md", "**/*.md"],
                             capture_output=True, text=True, check=True).stdout
        return [repo / r for r in uit.splitlines() if r]
    except (subprocess.CalledProcessError, FileNotFoundError):
        return [p for p in repo.rglob("*.md") if not OVERSLAAN & set(p.parts)]


def controleer(repo: Path, profiel: str) -> list[str]:
    fouten: list[str] = []
    readme = repo / "README.md"
    if not readme.exists():
        return ["[B11] README.md ontbreekt"]
    t = readme.read_text(encoding="utf-8")

    lic = repo / "LICENSE"
    if not lic.exists() or "EUROPEAN UNION PUBLIC LICENCE" not in lic.read_text(encoding="utf-8", errors="replace"):
        fouten.append("[B5] LICENSE ontbreekt of is niet EUPL-1.2")

    if not re.match(r"# \S", t):
        fouten.append("[B11] README begint niet met een #-kop met de naam")
    m = re.search(r"^Status: ([A-Za-z ]+?)\.", t, re.M)
    if not m:
        fouten.append("[B11] regel 'Status: <label>. <wat werkt en wat niet>' ontbreekt")
    gevonden = m.group(1).strip().lower() if m else None
    if gevonden and gevonden not in LABELS:
        fouten.append(f"[B11] status '{gevonden}' is geen label uit B8: {sorted(LABELS)}")

    koppen = re.findall(r"^## (.+?)\s*$", t, re.M)
    for kop in KOPPEN:
        if kop not in koppen:
            fouten.append(f"[B11] kop '## {kop}' ontbreekt")
    aanwezig = [k for k in koppen if k in KOPPEN]
    if aanwezig != [k for k in KOPPEN if k in aanwezig]:
        fouten.append("[B11] de vaste koppen staan niet in de volgorde Voor wie, Snel starten, Bijdragen, Licentie")

    naam = repo.resolve().name
    verwacht = status_in_profiel(profiel, naam)
    if verwacht is None:
        fouten.append(f"[B9] '{naam}' staat niet in de projectentabel en niet in de alinea's eronder")
    elif gevonden and gevonden != verwacht:
        fouten.append(f"[B12] status in README is '{gevonden}', profiel zegt '{verwacht}'")

    for bestand in markdown_bestanden(repo):
        if not bestand.exists():
            continue
        for i, regel in enumerate(bestand.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            if SOCIAAL.search(regel):
                fouten.append(f"[A5] {bestand.relative_to(repo)}:{i}: link naar sociale media")
    return fouten


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("repo")
    ap.add_argument("--profiel", required=True)
    a = ap.parse_args()
    fouten = controleer(Path(a.repo), Path(a.profiel).read_text(encoding="utf-8"))
    for f in fouten:
        print(f)
    if fouten:
        print(f"\n{len(fouten)} overtreding(en). Regels: https://github.com/security-commons-nl/.github/blob/main/REDACTIESTATUUT.md")
        return 1
    print("Repo voldoet aan het statuut (B5, B9, B11, B12, A5).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [x] **Stap 9: Run, verwacht PASS** (`python -m pytest tools/ -q`: 10 passed).

- [x] **Stap 10: De herbruikbare workflow** `.github/workflows/repo-compliance.yml`:

```yaml
name: Repo-compliance (herbruikbaar)

# Controleert een repo tegen het redactiestatuut: README-kop (B11), licentie (B5), plaats in het
# profiel (B9), status gelijk aan de projectentabel (B12), geen sociale-medialinks (A5).
# Gebruik in de caller-repo (.github/workflows/statuut.yml):
#
#   jobs:
#     statuut:
#       uses: security-commons-nl/.github/.github/workflows/repo-compliance.yml@main

on:
  workflow_call:

permissions:
  contents: read

jobs:
  statuut:
    runs-on: ubuntu-latest
    env:
      REPO: ${{ github.event.repository.name }}
    steps:
      - uses: actions/checkout@v6
        with:
          path: repo
      - uses: actions/checkout@v6
        with:
          repository: security-commons-nl/.github
          path: org
      - uses: actions/setup-python@v6
        with:
          python-version: "3.12"
      - name: Controleer tegen het statuut
        run: |
          mv repo "$REPO"
          python org/tools/repo_compliance.py "$REPO" --profiel org/profile/README.md
```

- [x] **Stap 11: De tests van het script in CI**, `.github/workflows/tools-ci.yml`:

```yaml
name: Tests van de controlescripts

on:
  push:
    branches: [main]
    paths: ["tools/**", ".github/workflows/tools-ci.yml"]
  pull_request:
    paths: ["tools/**"]

jobs:
  tests:
    uses: security-commons-nl/.github/.github/workflows/python-ci.yml@main
    with:
      python-version: "3.12"
      test-command: "python -m pytest tools/ -v"
      install-extras: "pytest"
```

- [x] **Stap 12: Controle en commit.**

```bash
cd X:/SECURITY-COMMONS-NL/.github
python -m pytest tools/ -q
python -c "import pathlib;t=pathlib.Path('REDACTIESTATUUT.md').read_text(encoding='utf-8');assert chr(8212) not in t;assert '**B11.' in t and '**B12.' in t and 'infrastructuur' in t;print('statuut ok')"
git pull -q --rebase
git add REDACTIESTATUUT.md BESLUITEN.md LICENSE tools/repo_compliance.py tools/test_repo_compliance.py .github/workflows/repo-compliance.yml .github/workflows/tools-ci.yml
git commit -m "statuut: B8 infrastructuur, B9 gepreciseerd, B11 README-kop, B12 status op een plek; repo-compliance afgedwongen" && git push
```

  Verwacht: 10 passed, `statuut ok`, en na de push een groene run van `tools-ci.yml`.

---

## Taak 2: Het profiel herordenen naar gebruiker-eerst

**Bestanden (repo `.github`):**
- Modify: `profile/README.md`
- Modify: `CONTRIBUTING.md` (de issue-formulierentabel en twee subsecties verhuizen hierheen)

**Interfaces:**
- Produces: een README met deze vaste volgorde van `##`-koppen, waar de site-build (Taak 3) op rekent:
  `## Direct aan de slag` · `## Alle projecten` · `## Waarom dit bestaat` · `## Meedoen` ·
  `## Onderliggende infrastructuur` · `## Over dit platform`.
- Produces: geen enkele em-dash meer in het profiel (A10).

- [x] **Stap 1: Nieuwe intro.** Vervang alles boven `## Projecten` (de regel `# security-commons-nl`, de
  blockquote en de hele sectie "Waarom dit bestaat") door:

```markdown
# security-commons-nl

> Open kennis en tooling voor digitale weerbaarheid, gemaakt door en voor publieke organisaties. Gratis,
> open source, van ons allemaal.

## Direct aan de slag

Voor CISO's, ISO's en bestuurders bij gemeenten, provincies, waterschappen en uitvoeringsorganisaties.
Alles hieronder werkt vandaag, zonder account en zonder factuur. De drie uitgelichte kaarten op de
voorpagina zijn de eerste drie projecten in de lijst met een live link.
```

- [x] **Stap 2: Kop en volgorde van de projectenlijst.** Hernoem `## Projecten` naar `## Alle projecten`.
  Zet de eerste drie rijen van de tabel in deze volgorde: `kennisbank`, `aanvalspaden`,
  `weerbaarheid-game`. Laat de overige rijen staan. Controleer dat alle drie een link in de kolom "Direct
  openen" hebben.

- [x] **Stap 3: Em-dashes weg.** In de kolom "Direct openen" staat bij tien rijen een em-dash als "geen
  link"-teken: maak die cel leeg (`| |`); `projectFromRow()` zet dan `live: null`, wat al zo werkt.
  Vervang elke overige em-dash in het bestand door een komma, punt of gewoon streepje, met behoud van
  de zin. Controle: `python -c "import pathlib;assert chr(8212) not in pathlib.Path('profile/README.md').read_text(encoding='utf-8')"`.

- [x] **Stap 4: De alinea's onder de tabel compleet maken.** De alinea `**Gearchiveerd:**` noemt al
  `anonimizer-web` en `beleid-assistent`; voeg toe: `dreigingsanalyse (opgegaan in de kennisbank, item
  Risicoanalyse langs aanvalspaden)`. **Niet zo uitgevoerd:** `dreigingsanalyse` is nooit op GitHub
  gepubliceerd en staat daarom niet in het profiel; een link ernaartoe zou dood zijn. De alinea
  `**Onderliggende infrastructuur:**` noemt `anonimizer-proxy`; voeg toe:
  `[security-commons-nl.github.io](https://github.com/security-commons-nl/security-commons-nl.github.io)
  (de site-build en de voorpagina)`. Laat de alinea "**Tooling van anderen.**" staan.

- [x] **Stap 5: "Waarom dit bestaat" terugzetten, korter, ná de tabel.** Voeg direct na de alinea
  "**Tooling van anderen.** ..." toe:

```markdown
## Waarom dit bestaat

Publieke organisaties werken voor informatiebeveiliging, privacy en continuïteit intensief samen met
marktpartijen. Dat is waardevol, maar wie de inrichting van zijn governance aan de markt overlaat, geeft de
regie uit handen. Daarom bouwen we samen: één organisatie die het wiel opnieuw uitvindt is kwetsbaar, tien
die kennis en tooling delen vormen een beweging. Publiek geld betekent publieke code. AI is een middel,
nooit een doel, en altijd controleerbaar. De volledige principes staan in
[PRINCIPLES.md](https://github.com/security-commons-nl/.github/blob/main/PRINCIPLES.md).
```

  Verwijder daarna de aparte sectie `## Principes` (die zegt alleen nog dat de principes in PRINCIPLES.md
  staan, en dat staat nu hierboven).

- [x] **Stap 6: Meedoen inkorten; de rest verhuist naar CONTRIBUTING.** Vervang de secties `## Meedoen`
  en `## Voor het eerst hier?` (inclusief de subsecties `### Direct aan de slag`, `### Geen
  GitHub-account?` en `### Wat kan ik verwachten?`, de tabel met issue-formulieren en de afbeelding) door:

```markdown
## Meedoen

Dit is geen verkooppraatje; er is niets te kopen. Begin met kijken, draai het lokaal, geef feedback of bouw
mee. Open een [discussion](https://github.com/security-commons-nl/.github/discussions) of een issue in een
van de repositories. Nog nooit een issue geopend? In
[CONTRIBUTING.md](https://github.com/security-commons-nl/.github/blob/main/CONTRIBUTING.md) staat per
project een formulier dat je alleen hoeft in te vullen, ook zonder GitHub-account of Git-ervaring, en wat
je daarna van ons mag verwachten.

In voorbereiding, als richting en niet als toezegging: websitecompliance, digitale soevereiniteit,
code-repoveiligheid en aanvalsoppervlak (OSINT). Een tool verschijnt hierboven in de lijst zodra hij
werkt; tot die tijd bestaat hij niet.
```

  Plak de verwijderde inhoud in `CONTRIBUTING.md` als nieuwe sectie `## Voor het eerst hier?` direct na
  `## Drie manieren om bij te dragen`, met daarin, in deze volgorde: de tabel met issue-formulieren (onder
  het kopje `### Per project: waar begin je`), `### Geen GitHub-account?` en `### Wat kan ik verwachten?`,
  letterlijk overgenomen. De afbeelding blijft in `profile/bijdrage-flow-v2.svg`; verwijs ernaar met
  `![Bijdrage-flow in vier stappen](profile/bijdrage-flow-v2.svg)`.

- [x] **Stap 7: Controle.** Koppen in de vaste volgorde, uitgelichte drie met live link, geen em-dash, en
  alle vijf repo's buiten de tabel benoemd:

```bash
cd X:/SECURITY-COMMONS-NL/.github
python - <<'EOF'
import pathlib, re
t = pathlib.Path("profile/README.md").read_text(encoding="utf-8")
koppen = re.findall(r"^## (.+)$", t, re.M)
verwacht = ["Direct aan de slag", "Alle projecten", "Waarom dit bestaat", "Meedoen",
            "Onderliggende infrastructuur", "Over dit platform"]
assert koppen == verwacht, koppen
rijen = [r for r in t.splitlines() if r.startswith("| [")]
assert [re.match(r"\| \[([^\]]+)\]", r).group(1) for r in rijen[:3]] == ["kennisbank", "aanvalspaden", "weerbaarheid-game"]
assert all("http" in r.split("|")[4] for r in rijen[:3]), "uitgelichte rij zonder live link"
assert chr(8212) not in t, "em-dash in het profiel"
plat = " ".join(t.split())
for naam in ("anonimizer-web", "beleid-assistent", "dreigingsanalyse", "anonimizer-proxy", "security-commons-nl.github.io"):
    assert "[" + naam + "]" in plat, naam + " niet benoemd onder de tabel"
c = pathlib.Path("CONTRIBUTING.md").read_text(encoding="utf-8")
assert "### Wat kan ik verwachten?" in c and "### Geen GitHub-account?" in c and "| Voor | Repository |" in c
print("profiel en contributing ok")
EOF
git pull -q --rebase && git add profile/README.md CONTRIBUTING.md && git commit -m "profiel: gebruiker eerst; bijdragersgids naar CONTRIBUTING; geen em-dash" && git push
```

---

## Taak 3: De voorpagina bouwen uit het profiel

**Bestanden (repo `security-commons-nl.github.io`):**
- Modify: `site/build.mjs`
- Modify: `site/landing.css`
- Create: `site/test_voorpagina.py`
- Create: `.github/workflows/ci.yml`

**Interfaces:**
- Consumes: `readProjects()` in `build.mjs` (bestaat; geeft per rij `{naam, repo, status, wat, live,
  liveLabel, doelgroep}`, gelezen uit de projectentabel door `projectFromRow()`), en `renderToken()`,
  die de projectentabel als `<div class="cards">` rendert via `projectCards()`.
- Produces: een blok `<section class="uitgelicht">` met precies drie `<a class="kaart">`, direct onder de
  kop "Direct aan de slag", vóór de kaartengrid.

- [x] **Stap 1: Falende test** in `site/test_voorpagina.py`:

```python
"""De voorpagina: drie uitgelichte kaarten uit de tabel, in de volgorde van de gebruiker.

Draait node site/build.mjs; dat herschrijft ook llms.txt en sitemap.xml (datum van vandaag). Dat is
verwacht: die twee horen in dezelfde commit.
"""
import pathlib
import re
import subprocess

ROOT = pathlib.Path(__file__).resolve().parent.parent


def test_voorpagina():
    subprocess.run(["node", "site/build.mjs"], cwd=ROOT, check=True, capture_output=True)
    html = (ROOT / "dist" / "index.html").read_text(encoding="utf-8")
    kaarten = re.findall(r'<a class="kaart" href="([^"]+)"', html)
    assert len(kaarten) == 3, kaarten
    assert kaarten[0].rstrip("/").endswith("/kennisbank")
    assert kaarten[1].rstrip("/").endswith("/aanvalspaden")
    assert kaarten[2].rstrip("/").endswith("/weerbaarheid-game")
    # Uitgelicht staat vóór de kaartengrid, en de grid vóór "Waarom dit bestaat".
    assert html.index('class="uitgelicht"') < html.index('class="cards"') < html.index("Waarom dit bestaat")
    assert chr(8212) not in html, "em-dash op de voorpagina"


if __name__ == "__main__":
    test_voorpagina()
    print("voorpagina ok")
```

- [x] **Stap 2: Run, verwacht FAIL.** Eerst `cp ../.github/profile/README.md org-profile/profile/README.md`
  en `npm ci`; dan `python site/test_voorpagina.py` geeft `AssertionError` op de kaarten.

- [x] **Stap 3: Kaarten renderen.** In `build.mjs`, direct boven `function buildLandingPage()`:

```js
/**
 * De drie uitgelichte kaarten: de eerste drie projecten in de tabel met een live link (statuut B9).
 * Faalt hard bij minder dan drie, zodat een verkeerd profiel de site niet stil verarmt.
 */
function uitgelicht() {
  const rijen = readProjects().filter((pr) => pr.live).slice(0, 3);
  if (rijen.length < 3) throw new Error(`Minder dan drie projecten met een live link (${rijen.length})`);
  const kaarten = rijen.map((pr) => `
    <a class="kaart" href="${escapeHtml(pr.live)}">
      <span class="kaart-naam">${escapeHtml(pr.naam)}</span>
      <span class="kaart-wat">${escapeHtml(pr.wat)}</span>
      <span class="kaart-voor">${escapeHtml(pr.doelgroep)}</span>
    </a>`).join('');
  return `<section class="uitgelicht" aria-label="Uitgelicht">${kaarten}</section>`;
}
```

  In `buildLandingPage()`, direct na `const tokens = marked.lexer(markdown, { gfm: true });`:

```js
  const i = tokens.findIndex((t) => t.type === 'heading' && t.text === 'Direct aan de slag');
  if (i === -1) throw new Error('Kop "Direct aan de slag" ontbreekt in het profiel');
  const h = uitgelicht();
  tokens.splice(i + 2, 0, { type: 'html', block: true, raw: h, text: h });
```

  (`i + 2`: na de kop en de ene alinea eronder.) Verwijder in `pageShell()` en in de `title` van
  `buildLandingPage()` de em-dash: `'Security Commons NL: open securitykennis voor de publieke sector'`.

- [x] **Stap 4: Opmaak** in `landing.css`, onderaan:

```css
.uitgelicht { display: grid; grid-template-columns: repeat(auto-fit, minmax(14rem, 1fr)); gap: 1rem; margin: 1.2rem 0 2rem; }
.kaart { display: flex; flex-direction: column; gap: .35rem; padding: 1rem 1.1rem; border: 1px solid #d7dee7; border-radius: 10px; background: #fff; text-decoration: none; color: inherit; }
.kaart:hover { border-color: var(--blauw); }
.kaart-naam { font-weight: 700; color: var(--blauw); font-size: 1.05rem; }
.kaart-wat { font-size: .92rem; }
.kaart-voor { font-size: .8rem; color: var(--grijs); }
```

- [x] **Stap 5: CI voor de test**, `.github/workflows/ci.yml`:

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

permissions:
  contents: read

jobs:
  voorpagina:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v6
      - uses: actions/checkout@v6
        with:
          repository: security-commons-nl/.github
          path: org-profile
      - uses: actions/setup-node@v6
        with:
          node-version: 24
          cache: npm
      - uses: actions/setup-python@v6
        with:
          python-version: "3.12"
      - run: npm ci
      - run: python site/test_voorpagina.py
```

- [x] **Stap 6: Run, verwacht PASS**, links nalopen, committen:

```bash
cd X:/SECURITY-COMMONS-NL/security-commons-nl.github.io
python site/test_voorpagina.py
for u in $(grep -o 'https://security-commons-nl.github.io/[a-z0-9./-]*' llms.txt | sort -u); do echo "$(curl -s -o /dev/null -w '%{http_code}' -L "$u") $u"; done
git pull -q --rebase && git add site/build.mjs site/landing.css site/test_voorpagina.py .github/workflows/ci.yml llms.txt sitemap.xml && git commit -m "voorpagina: drie uitgelichte kaarten uit de tabel, gebruiker eerst" && git push
```

  Verwacht: `voorpagina ok`, alle URL's `200`, groene `ci.yml` en `pages.yml`. Open daarna de live pagina
  en kijk of de drie kaarten bovenaan staan.

---

## Taak 4: De documentatiestandaard terugbrengen tot wat gecontroleerd wordt

**Bestanden (repo `.github`):**
- Modify: `DOCUMENTATION-STANDARD.md` (volledig vervangen)
- Modify: `CONTRIBUTING.md` (sectie "Documentatie bij software-repos")

- [x] **Stap 1: Nieuwe standaard.** Vervang de inhoud van `DOCUMENTATION-STANDARD.md` door:

```markdown
# Documentatiestandaard: de README-kop

Elke levende repo begint hetzelfde, zodat een bezoeker die van de voorpagina doorklikt in tien seconden
ziet wat het is, of het werkt en hoe hij begint. Dit is statuutregel B11; `repo-compliance.yml`
controleert het in elke repo.

## De kop

    # naam

    Eén zin: wat het is en voor wie.

    Status: <in gebruik | prototype | concept | gearchiveerd | infrastructuur>. <Wat werkt, wat niet.>

    ## Voor wie
    ## Snel starten
    ## Bijdragen
    ## Licentie

Het label achter `Status:` is letterlijk het label uit de projectentabel op het org-profiel (B12);
`infrastructuur` is voor repo's die geen project zijn (B8). Onder `## Bijdragen` volstaat een verwijzing
naar de CONTRIBUTING van de organisatie; onder `## Licentie` de regel "EUPL-1.2, zie LICENSE".

## Meer mag, minder niet

Alles wat een repo verder wil vertellen (architectuur, configuratie, voorbeelden) komt ná deze koppen, of
in een `docs/`-map als de README anders langer dan ongeveer 1500 woorden wordt. Een `docs/`-map is geen
eis; een README die klopt wel.

## Taal

Documentatie in het Nederlands. Code, variabelen en commentaar in het Engels.

## Wanneer bijwerken

Een wijziging die zichtbaar is voor gebruikers, wijzigt ook de README. Een statuswijziging begint in de
projectentabel; de README volgt, en de controle wordt rood zolang ze verschillen.
```

- [x] **Stap 2: CONTRIBUTING.** Vervang de sectie `## Documentatie bij software-repos` door: "Elke repo
  begint met dezelfde kop; zie de [documentatiestandaard](DOCUMENTATION-STANDARD.md). De controle
  `repo-compliance.yml` draait in elke repo en zegt precies wat er ontbreekt."

- [x] **Stap 3: Commit.**

```bash
cd X:/SECURITY-COMMONS-NL/.github
git pull -q --rebase && git add DOCUMENTATION-STANDARD.md CONTRIBUTING.md && git commit -m "documentatiestandaard: de README-kop, niet de docs-map" && git push
```

---

## Taak 5: De norm uitrollen over de levende repo's

**Bestanden (per repo):** `README.md`, `LICENSE` (waar hij mist), `.github/workflows/statuut.yml` (nieuw).

Twintig repo's: de 22 projectrepo's min de twee gearchiveerde (`anonimizer-web`, `beleid-assistent`; daar
kun je niet naar pushen en ze blijven met rust). `dreigingsanalyse` hoort erbij: die krijgt zijn
gearchiveerd-README hier en wordt in Taak 6 op GitHub gearchiveerd, ná de push.

- [x] **Stap 1: Inventaris draaien.** Vanuit `X:\SECURITY-COMMONS-NL`:

```bash
for d in */; do r="${d%/}"; case "$r" in .github|anonimizer-web|beleid-assistent) continue;; esac; [ -d "$r/.git" ] && { echo "== $r"; python .github/tools/repo_compliance.py "$r" --profiel .github/profile/README.md | grep "^\[" ; }; done
```

  Noteer de uitkomst; dat is de werklijst.

- [x] **Stap 2: Per repo de README-kop zetten.** Herschrijf niet de inhoud; zet alleen de kop erboven en
  verplaats bestaande tekst onder de juiste kop. Regels:
  - De `#`-kop is de reponaam.
  - De ene zin: de bestaande eerste zin als die klopt, anders schrijf hem.
  - `Status:` het label uit de tabel, punt, dan één zin wat werkt en wat niet (bij `concept`: "Ontwerp
    of plan; geen werkende code."). `anonimizer-proxy` en `security-commons-nl.github.io`:
    `Status: infrastructuur.`; `dreigingsanalyse`: `Status: gearchiveerd. Opgegaan in de kennisbank:
    https://security-commons-nl.github.io/kennisbank/security/risicoanalyse-aanvalspaden/`.
  - `## Voor wie`: één of twee zinnen; gebruik de kolom Doelgroep uit de tabel als basis.
  - `## Snel starten`: de bestaande installatie- of open-instructie. Bij een live tool: de link.
  - `## Bijdragen`: "Zie de [CONTRIBUTING](https://github.com/security-commons-nl/.github/blob/main/CONTRIBUTING.md) van de organisatie." plus, als de repo eigen issue-formulieren heeft, één regel daarheen.
  - `## Licentie`: "EUPL-1.2, zie [LICENSE](LICENSE)."
  - De vier koppen in die volgorde; de controle toetst ook de volgorde.

- [x] **Stap 3: LICENSE** toevoegen in `dreigingsanalyse` en `security-shop`: kopieer
  `X:\SECURITY-COMMONS-NL\kennisbank\LICENSE` letterlijk. `procescheck` heeft GPL-3; laat die staan tot het
  open besluit (onderaan) is genomen. Tot die tijd blijft de controle daar rood op B5, en dat is juist.

- [x] **Stap 4: Workflow per repo.** Maak `.github/workflows/statuut.yml` aan met exact:

```yaml
name: Statuut

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  schedule:
    - cron: "0 6 * * 1"   # wekelijks: vangt een statuswijziging in de projectentabel op

permissions:
  contents: read

jobs:
  statuut:
    uses: security-commons-nl/.github/.github/workflows/repo-compliance.yml@main
```

  In repo's die nu `doc-compliance.yml` aanroepen (Handelingsperspectief, ai-gebruik-in-beeld,
  anonimizer-local, blast-radius, iamscan, publicatiescan; `anonimizer-web` is gearchiveerd en blijft
  staan): verwijder die aanroep. Staat hij als job in een bestaand `ci.yml`, verwijder alleen die job.

- [x] **Stap 5: Per repo controleren en committen.**

```bash
cd X:/SECURITY-COMMONS-NL/<repo>
python ../.github/tools/repo_compliance.py . --profiel ../.github/profile/README.md
git pull -q --rebase && git add README.md .github/workflows/statuut.yml && { [ -f LICENSE ] && git add LICENSE; }; git commit -m "README-kop volgens statuut B11; statuutcontrole in CI" && git push
```

  `repo_compliance.py` leest de reponaam uit de mapnaam (`repo.resolve().name`), dus `.` werkt vanuit de
  repo-map.

- [x] **Stap 6: Eindcontrole.** Twintig repo's groen, lokaal én in CI:

```bash
cd X:/SECURITY-COMMONS-NL
for d in */; do r="${d%/}"; case "$r" in .github|anonimizer-web|beleid-assistent) continue;; esac; [ -d "$r/.git" ] && { python .github/tools/repo_compliance.py "$r" --profiel .github/profile/README.md >/dev/null && echo "ok   $r" || echo "ROOD $r"; }; done
for d in */; do r="${d%/}"; case "$r" in anonimizer-web|beleid-assistent) continue;; esac; [ -d "$r/.git" ] && (cd "$r" && echo "$r: $(gh run list --branch main --limit 1 --json conclusion -q '.[0].conclusion')"); done
```

  Verwacht: 20 keer `ok`, en `success` in elke repo. Daarna in `.github`: `doc-compliance.yml`
  verwijderen (alleen de gearchiveerde `anonimizer-web` roept hem nog aan, en die draait niet meer) en
  committen.

---

## Taak 6: Archiveren wat geen project meer is

- [x] **Stap 1:** Archiveer `dreigingsanalyse` op GitHub, ná de push uit Taak 5:

```bash
gh repo archive security-commons-nl/dreigingsanalyse --yes
for r in anonimizer-web beleid-assistent dreigingsanalyse; do echo "$r: $(gh repo view security-commons-nl/$r --json isArchived -q .isArchived)"; done
```

  Verwacht: drie keer `true`. Is een van de eerste twee `false`, archiveer die ook.

- [x] **Stap 2:** In `X:\SECURITY-COMMONS-NL\CLAUDE.md` bij `dreigingsanalyse` de regel aanvullen met
  "gearchiveerd op GitHub, 2026-08". Geen commit nodig; `CLAUDE.md` is geen repo.

---

## Taak 7: Een route voor andere doelgroepen in llms.txt

**Bestanden:** `security-commons-nl.github.io/llms.txt` (handgeschreven deel).

- [x] **Stap 1:** Voeg, na het blok "Kennisbank, losse publicaties", een kort blok toe. De twee links
  staan al elders in het bestand; dat is bewust, want dit blok is een leesroute per doelgroep:

```markdown
## Voor wie geen publieke organisatie is

- Leveranciers: de Security Annex (hierboven, onder Kennisbank) is wat een publieke opdrachtgever van je vraagt; de zelfcheck aanvalspaden (hieronder, onder Prototype) laat zien welke aanvalspaden hij bij zichzelf toetst.
- Journalisten en onderzoekers: alle code en tekst is open onder EUPL-1.2, de projectentabel op https://security-commons-nl.github.io/ is de volledige lijst, en https://github.com/security-commons-nl/.github/blob/main/BESLUITEN.md legt vast waarom dingen zijn zoals ze zijn.
```

- [x] **Stap 2:** Bouwen, links nalopen (alle `200`), committen zoals in Taak 3 stap 6.

---

## Definitie van klaar

- Voorpagina: opent met drie kaarten uit de tabel; het manifest staat eronder; geen tweede bron; geen
  em-dash; `ci.yml` in de io-repo bewaakt de test.
- Werkplaats: alle 20 levende repo's groen op `repo_compliance.py`, elke levende repo heeft CI, elke repo
  een EUPL-licentie, status in README gelijk aan de tabel, wekelijkse controle op drift.
- Statuut: B8 (infrastructuur), B9 gepreciseerd, B11 en B12 erin, besluit gelogd, documentatiestandaard
  teruggebracht, `doc-compliance.yml` weg.
- Bewijs: de controlecommando's uit Taak 1, 2, 3, 5 en 7 zijn gedraaid en groen; alle live URL's geven 200.

## Open besluit, voor Bas

**De licentie van `procescheck`.** Die repo staat onder GPL-3, en het statuut (B5) zegt EUPL-1.2. De
auteursrechthebbende van procescheck is niet de commons zelf; herlicentiëren kan alleen met diens
instemming. Twee routes: (a) de auteur stemt in met EUPL-1.2, dan wordt het een gewone Taak 5-stap; (b) het
statuut krijgt bij B5 een uitzondering voor ingebrachte repo's met een compatibele copyleft-licentie, en de
controle accepteert dan ook GPL-3. Tot het besluit blijft de controle op procescheck rood, en dat is de
bedoeling: een rode controle die een echte vraag stelt is beter dan een groene die hem verzwijgt.

**Beslist op 30-08-2026: route (a).** De auteur heeft de licentie zelf omgezet naar EUPL-1.2 en tegelijk
een nieuwe versie gepubliceerd. De controle op procescheck is groen en de uitzondering bij B5 komt er niet.
Onderbouwing in `.github/BESLUITEN.md`.

## Wat de review veranderde

Een onafhankelijke review van versie 1 vond 25 punten. De belangrijkste en wat ermee is gedaan:

- De test in Taak 3 zocht `<table>`, maar de build rendert de tabel als kaartengrid: nu `class="cards"`.
- De em-dash-controles konden niet slagen (21 in het profiel, één in `build.mjs`): nu een expliciete
  opruimstap in Taak 2 en 3, en lege cellen in plaats van een em-dash als "geen link".
- `status_in_profiel()` las alinea's regelgebonden en miste `beleid-assistent`: nu genormaliseerd.
- Taak 6 (nu 5) had profielalinea's nodig die pas later kwamen: de alinea's staan nu in Taak 2.
- Naar gearchiveerde repo's kun je niet pushen: die zijn uit de uitrol gehaald; `dreigingsanalyse` wordt
  pas gearchiveerd ná zijn push.
- Aantallen: 17 tabelrijen, 22 projectrepo's, 20 in de uitrol; `.github` miste zelf een LICENSE.
- Bij het proefdraaien van het script tegen de echte repo's (10 tests groen, 20 repo's gecontroleerd)
  bleek `procescheck` GPL-3 te hebben: als open besluit opgenomen in plaats van stil gerepareerd.
- De A5-scan las ongetrackte mappen mee: nu `git ls-files`.
- `infrastructuur` botste met B8: nu als label vastgelegd.
- De tests van het controlescript draaiden nergens: nu `tools-ci.yml`; de voorpaginatest ook: `ci.yml`.
- De workflow miste `permissions` en zette GitHub-context rechtstreeks in de shell: nu via `env`.
- Volgorde van de koppen werd niet getoetst: nu wel, met test.
- Statuut en script vielen in twee commits uiteen: nu één werkgang (Taak 1).
- `statuut.yml` zag drift in de tabel niet: nu een wekelijkse `schedule`.
- Twee subsecties van "Voor het eerst hier?" verdwenen stil: nu mee naar CONTRIBUTING.
- Drie kaarten bovenaan én in de grid: de grid heet nu "Alle projecten", en de kaartenfunctie faalt hard
  bij minder dan drie live projecten.
