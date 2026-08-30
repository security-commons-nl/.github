#!/usr/bin/env python3
"""Controleert elke link naar de commons zelf, over alle repo's in de werkmap heen.

Een dode link naar buiten is vervelend; een dode link naar je eigen site is een gebroken belofte. Deze
controle kijkt daarom alleen naar links naar `security-commons-nl.github.io` en naar repo's in de
organisatie. Wat lokaal te vinden is, wordt op schijf gecontroleerd; de rest via een HTTP-verzoek.

Gebruik:
    python tools/linkcheck.py <werkmap>       (de map met alle repo's naast elkaar)

Exit 1 als een link nergens op uitkomt. Externe sites worden niet gecontroleerd.
Alleen standaardbibliotheek; geen pip nodig.
"""
from __future__ import annotations

import pathlib
import re
import sys
import urllib.request

WERKMAP = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
SITE = "https://security-commons-nl.github.io/"
REPO = "https://github.com/security-commons-nl/"
LINK = re.compile(r'(?:href="|\]\()(https://(?:security-commons-nl\.github\.io|github\.com/security-commons-nl)/[^)"#\s]*)')
# Codeblokken in markdown bevatten commando's en testfixtures, geen links die een lezer aanklikt. Een
# voorbeeldrepo in een plan hoort niet te bestaan; die als dode link melden verbergt de echte.
CODEBLOK = re.compile(r"^```.*?^```", re.M | re.S)
BESTANDEN = ("*.md", "*.html", "*.txt", "*.xml", "*.json", "*.js")
# Gebouwde en geleende mappen: die bevatten kopieen, en een fout daarin hoort in de bron thuis.
OVERSLAAN = ("node_modules", ".git", "_dump", "dist", "_kennisbank", "_aanvalspaden", "__pycache__",
             "org-profile", ".pytest_cache")
# Repo's waarvan de site door CI wordt gebouwd; die staan niet als bestand op schijf.
GEBOUWD = {"aanvalspaden", "weerbaarheid-game", "anonimizer-browser", "procescheck", "grc-platform",
           "security-shop", "blast-radius", "ai-gebruik-in-beeld"}


def lokaal(url: str) -> pathlib.Path | None:
    """Vertaal een site- of repo-URL naar een pad in de werkmap; None als dat niet kan."""
    if url.startswith(SITE):
        rest = url[len(SITE):].strip("/")
        if not rest:
            return WERKMAP / "security-commons-nl.github.io" / "dist" / "index.html"
        repo, _, pad = rest.partition("/")
        if repo in GEBOUWD:
            return None  # gebouwde site; via HTTP controleren
        kandidaat = WERKMAP / repo / (pad or "")
        return kandidaat / "index.html" if kandidaat.is_dir() else kandidaat
    if url.startswith(REPO):
        rest = url[len(REPO):].strip("/")
        repo, _, pad = rest.partition("/")
        # Functies van GitHub zelf. Een HEAD hierop zegt niets: /issues/new en /edit/ geven zonder
        # inlog een 404 terwijl ze voor een ingelogde lezer prima werken. We controleren daarom of de
        # repo bestaat, niet of de functie een pagina teruggeeft.
        if pad.startswith(("issues", "discussions", "pulls", "settings", "compare", "releases")):
            return WERKMAP / repo if (WERKMAP / repo).is_dir() else None
        pad = re.sub(r"^(blob|tree|edit|raw)/main/", "", pad)
        doel = WERKMAP / repo / pad if pad else WERKMAP / repo
        return doel if (WERKMAP / repo).is_dir() else None
    return None


def http_ok(url: str) -> bool:
    try:
        req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "linkcheck"})
        with urllib.request.urlopen(req, timeout=20) as r:
            return r.status < 400
    except Exception:
        return False


def main() -> int:
    fouten: list[str] = []
    gezien: dict[str, bool] = {}
    for patroon in BESTANDEN:
        for pad in WERKMAP.rglob(patroon):
            if any(o in pad.parts for o in OVERSLAAN):
                continue
            tekst = pad.read_text(encoding="utf-8", errors="replace")
            if pad.suffix == ".md":
                tekst = CODEBLOK.sub("", tekst)
            for url in sorted(set(LINK.findall(tekst))):
                if "<" in url:
                    continue  # placeholder in een sjabloon, geen link
                if url not in gezien:
                    doel = lokaal(url)
                    gezien[url] = doel.exists() if doel is not None else http_ok(url)
                if not gezien[url]:
                    fouten.append(f"{pad.relative_to(WERKMAP)}: {url}")
    for f in sorted(set(fouten)):
        print("DOOD:", f)
    print(f"{len(gezien)} unieke links, {len(set(fouten))} dood")
    return 1 if fouten else 0


if __name__ == "__main__":
    raise SystemExit(main())
