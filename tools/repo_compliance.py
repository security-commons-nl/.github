#!/usr/bin/env python3
"""Controleert één repo tegen het redactiestatuut.

  B5   LICENSE aanwezig en EUPL-1.2
  B9   de repo staat in de projectentabel of in een alinea eronder (gearchiveerd, infrastructuur)
  B11  README-kop: #-kop, Status-regel, en de vier koppen in de vaste volgorde
  B12  het label in de README is het label uit het profiel
  A5   geen links naar sociale media in markdown
  C5   een instrument met status 'in gebruik' haalt de meetbare delen van de lat: tests in CI, een versie of
       peildatum op de pagina, de status op de pagina gelijk aan de tabel, en een kruimelpad naar de voorpagina
       (B10). Wat alleen met het oog te toetsen is (huisstijl, telefoonbreedte, consolefouten) zit hier niet in.

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
# C5: wat telt als een test in CI, een versie op de pagina, en waar de pagina staat.
TESTSTAP = re.compile(r"^\s*(?:-\s*)?run:\s*.*\b(pytest|npm (?:run )?test|vitest|playwright test|node \S*test\S*)", re.M | re.I)
VERSIE = re.compile(r"versie\W{0,3}(?:<[^>]*>\s*)?(?:\d+\.\d+(?:\.\d+)?|\d{4}-\d{2}(?:-\d{2})?)"
                    r"|VERSIE(?:_APP)?\s*=\s*['\"]\d", re.I)
PAGINA_SOORTEN = {".html", ".js", ".mjs", ".ts"}
NIET_PAGINA = {"tests", "test", ".github", "__pycache__"}


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


def vorm_in_profiel(profiel: str, naam: str) -> str | None:
    """De kolom Vorm uit de projectentabel (instrument, kennis, dataset, script), of None."""
    for regel in profiel.splitlines():
        cellen = [c.strip() for c in regel.strip().strip("|").split("|")]
        if len(cellen) >= 7 and re.match(r"\[" + re.escape(naam) + r"\]\(", cellen[0]):
            return cellen[2].lower()
    return None


def paginabronnen(repo: Path) -> list[Path]:
    """De bestanden waaruit de pagina van een instrument bestaat: html en scripts, zonder tests en bouwresten."""
    uit = []
    for p in repo.rglob("*"):
        rel = p.relative_to(repo).parts
        if p.is_file() and p.suffix in PAGINA_SOORTEN and not (OVERSLAAN | NIET_PAGINA) & set(rel) \
                and ".test." not in p.name and not p.name.startswith("test_"):
            uit.append(p)
    return uit


def controleer_lat(repo: Path, status: str) -> list[str]:
    """C5, de meetbare delen. Alleen voor een instrument met status 'in gebruik' (B8)."""
    fouten = []
    workflows = list((repo / ".github" / "workflows").glob("*.y*ml")) if (repo / ".github" / "workflows").is_dir() else []
    if not any(TESTSTAP.search(w.read_text(encoding="utf-8", errors="replace")) for w in workflows):
        fouten.append("[C5] geen teststap in .github/workflows (pytest, npm test, vitest, playwright of node ...test)")
    teksten = [p.read_text(encoding="utf-8", errors="replace") for p in paginabronnen(repo)]
    if not any(VERSIE.search(t) for t in teksten):
        fouten.append("[C5] geen versie of peildatum op de pagina (bijvoorbeeld 'versie 1.2.0' of een constante VERSIE = '2026-10-30')")
    if not any(re.search(r"status:\s*" + re.escape(status), t, re.I) for t in teksten):
        fouten.append(f"[C5] de pagina noemt de status niet als 'status: {status}'")
    if not any('href="https://security-commons-nl.github.io/"' in t for t in teksten):
        fouten.append("[B10] geen kruimelpad naar https://security-commons-nl.github.io/ op de pagina")
    return fouten


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
    if verwacht == "in gebruik" and vorm_in_profiel(profiel, naam) == "instrument":
        fouten.extend(controleer_lat(repo, verwacht))

    for bestand in markdown_bestanden(repo):
        if not bestand.exists():
            continue
        # In een codeblok staan commando's en testfixtures, geen links die een lezer aanklikt. Een
        # test die controleert DAT A5 vuurt, heeft daar een voorbeeld-URL voor nodig; die als
        # overtreding melden maakt het statuut onmogelijk om te testen.
        in_codeblok = False
        for i, regel in enumerate(bestand.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            if regel.lstrip().startswith("```"):
                in_codeblok = not in_codeblok
                continue
            if in_codeblok:
                continue
            if SOCIAAL.search(regel):
                fouten.append(f"[A5] {bestand.relative_to(repo)}:{i}: link naar sociale media")
    return fouten


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("repo")
    ap.add_argument("--profiel", "--projecten", dest="projecten", required=True,
                    help="Pad naar PROJECTEN.md (of profile/README.md)")
    a = ap.parse_args()
    fouten = controleer(Path(a.repo), Path(a.projecten).read_text(encoding="utf-8"))
    for f in fouten:
        print(f)
    if fouten:
        print(f"\n{len(fouten)} overtreding(en). Regels: https://github.com/security-commons-nl/.github/blob/main/REDACTIESTATUUT.md")
        return 1
    print("Repo voldoet aan het statuut (B5, B9, B11, B12, A5, en C5 voor een instrument in gebruik).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
