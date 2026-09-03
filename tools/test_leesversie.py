"""De gedeelde leesversie-build: bouwt hij een andere repo, en blijft hij binnen de belofte?

De build in site/ is sinds 03-09-2026 de enige kopie. Repo's zonder eigen build roepen hem aan via
pages-docs.yml, die deze repo uitcheckt en SITE_ROOT op de aanroepende repo zet. Deze tests draaien
hem tegen een tijdelijke repo, zodat een wijziging hier niet pas bij de eerstvolgende deploy van een
andere repo omvalt.

Node is nodig; zonder node slaan de tests zichzelf over.
"""
from __future__ import annotations

import json
import os
import pathlib
import re
import shutil
import subprocess

import pytest

HIER = pathlib.Path(__file__).resolve().parent
REPO = HIER.parent
BUILD = REPO / "site" / "build.mjs"

README = """# voorbeeldtool

Doet iets nuttigs met bestanden die je al hebt.

Status: prototype. Werkt en heeft tests.

## Voor wie

Voor ISO's die een keer willen nakijken wat er in hun publicaties staat.

## Snel starten

1. Kloon de repo.
2. Draai het script.

Zie ook [CONTRIBUTING.md](CONTRIBUTING.md) en de [licentie](LICENSE), plus de
[dataset](data.json) die meegaat.
"""


def node_aanwezig() -> bool:
    return shutil.which("node") is not None and (REPO / "node_modules" / "marked").exists()


@pytest.fixture(scope="module")
def gebouwd(tmp_path_factory) -> tuple[pathlib.Path, str]:
    if not node_aanwezig():
        pytest.skip("node of node_modules/marked ontbreekt (npm ci in deze repo)")
    doel = tmp_path_factory.mktemp("voorbeeldtool")
    (doel / "README.md").write_text(README, encoding="utf-8")
    (doel / "data.json").write_text('{"a": 1}', encoding="utf-8")
    (doel / "site").mkdir()
    (doel / "site" / "config.json").write_text(json.dumps({
        "repoUrl": "https://github.com/security-commons-nl/voorbeeldtool",
        "title": "voorbeeldtool · Security Commons NL",
        "description": "Een tool om de gedeelde build mee te toetsen.",
        "siteTitle": "voorbeeldtool",
        "tabs": [{"file": "README.md", "id": "start", "label": "Start"}],
        "assets": ["data.json"],
    }, ensure_ascii=False), encoding="utf-8")

    omgeving = dict(os.environ, SITE_ROOT=str(doel))
    uit = subprocess.run(["node", str(BUILD)], cwd=REPO, env=omgeving, capture_output=True)
    melding = uit.stdout.decode("utf-8", "replace") + uit.stderr.decode("utf-8", "replace")
    assert uit.returncode == 0, melding
    return doel, (doel / "dist" / "index.html").read_text(encoding="utf-8")


def test_bouwt_in_de_aanroepende_repo(gebouwd):
    """De uitvoer landt bij de repo die gebouwd wordt, niet bij de build."""
    doel, html = gebouwd
    assert (doel / "dist" / "index.html").exists()
    assert not (REPO / "dist").exists(), "de build heeft in zijn eigen repo geschreven"
    assert "voorbeeldtool" in html
    assert "Doet iets nuttigs" in html


def test_opmaak_komt_uit_de_build(gebouwd):
    """De css en het paginascript zitten in de pagina; de aanroepende repo levert alleen tekst."""
    _, html = gebouwd
    assert "<style>" in html and "--blauw" in html
    assert "<script>" in html
    assert 'class="site-kicker"' in html, "kruimelpad ontbreekt (statuut B10)"


def test_geen_tabbalk_bij_een_enkele_tab(gebouwd):
    """Een tabbalk met een tab is ruis; die verscheen wel in twee van de vijf oude kopieen."""
    _, html = gebouwd
    assert 'class="tab"' not in html


def test_downloads_gaan_mee_en_de_rest_naar_github(gebouwd):
    """Een relatieve link mag alleen blijven als het bestand meegaat; anders wijst hij naar GitHub.

    Dit is de fout die op 03-09-2026 op /normen/ zat: zeven links naar bestanden in de repo gaven een
    404 op Pages omdat ze wel werden omgezet maar niet meegekopieerd.
    """
    doel, html = gebouwd
    assert (doel / "dist" / "data.json").exists()
    assert 'href="data.json"' in html
    for naam in ("CONTRIBUTING.md", "LICENSE"):
        assert f'href="{naam}"' not in html
        assert f"/blob/main/{naam}" in html
    relatief = [h for h in re.findall(r'href="([^"]+)"', html)
                if not h.startswith(("http://", "https://", "#", "/", "mailto:"))]
    for pad in relatief:
        assert (doel / "dist" / pad).exists(), f"dode link: {pad}"


def test_zonder_site_root_bouwt_hij_zijn_eigen_repo():
    """De kopieen in de andere repo's draaien zonder SITE_ROOT; dat pad moet blijven werken."""
    bron = BUILD.read_text(encoding="utf-8")
    assert "process.env.SITE_ROOT" in bron
    assert "join(SITE_DIR, '..')" in bron, "de terugval op de eigen repo is weg"
