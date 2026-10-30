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


def test_sociale_link_in_een_codeblok_mag(tmp_path):
    """Anders is A5 zelf niet te testen: een test die het vuren bewijst, heeft een voorbeeld-URL nodig.

    In een codeblok staat een commando of een fixture, geen link die een lezer aanklikt.
    """
    blok = "\n```python\nzie = 'https://www.linkedin.com/in/iemand'\n```\n"
    code, uit = draai(tmp_path, GOED + blok)
    assert code == 0, uit


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


# C5: de meetbare delen van de lat, alleen voor een instrument met status in gebruik.
PROFIEL_C5 = textwrap.dedent("""\
    | Project | Status | Vorm | Wat is het? | Direct openen | Doelgroep | Waarvoor |
    |---|---|---|---|---|---|---|
    | [werktuig](https://github.com/security-commons-nl/werktuig) | in gebruik | instrument | Iets | | CISO's | vaststellen |
    | [leeswerk](https://github.com/security-commons-nl/leeswerk) | in gebruik | kennis | Iets | | CISO's | aanpakken |
    """)
LAT_PAGINA = ('<nav aria-label="Kruimelpad"><a href="https://security-commons-nl.github.io/">Security Commons NL</a></nav>'
              '<footer>versie 1.0.0 (peildatum 2026-10-30) · status: in gebruik</footer>')
LAT_CI = "jobs:\n  t:\n    steps:\n      - run: npm test\n"


def maak_instrument(tmp, naam="werktuig", pagina=LAT_PAGINA, ci=LAT_CI):
    readme = GOED.replace("# voorbeeld", f"# {naam}").replace("Status: prototype.", "Status: in gebruik.")
    repo = tmp / naam
    (repo / ".github" / "workflows").mkdir(parents=True)
    (repo / "README.md").write_text(readme, encoding="utf-8")
    (repo / "LICENSE").write_text(LICENTIE, encoding="utf-8")
    if pagina is not None:
        (repo / "index.html").write_text(pagina, encoding="utf-8")
    if ci is not None:
        (repo / ".github" / "workflows" / "ci.yml").write_text(ci, encoding="utf-8")
    prof = tmp / "profiel.md"
    prof.write_text(PROFIEL_C5, encoding="utf-8")
    r = subprocess.run([sys.executable, str(HIER / "repo_compliance.py"), str(repo), "--projecten", str(prof)],
                       capture_output=True, text=True)
    return r.returncode, r.stdout


def test_instrument_dat_de_lat_haalt_is_groen(tmp_path):
    code, uit = maak_instrument(tmp_path)
    assert code == 0, uit


def test_instrument_zonder_teststap_is_c5(tmp_path):
    code, uit = maak_instrument(tmp_path, ci="jobs:\n  t:\n    steps:\n      - run: npm run build\n")
    assert code == 1 and "[C5] geen teststap" in uit, uit


def test_instrument_zonder_versie_is_c5(tmp_path):
    code, uit = maak_instrument(tmp_path, pagina=LAT_PAGINA.replace("versie 1.0.0 (peildatum 2026-10-30) · ", ""))
    assert code == 1 and "[C5] geen versie" in uit, uit


def test_versie_als_constante_telt(tmp_path):
    pagina = LAT_PAGINA.replace("versie 1.0.0 (peildatum 2026-10-30) · ", "") + "<script>const VERSIE = '2026-10-30';</script>"
    code, uit = maak_instrument(tmp_path, pagina=pagina)
    assert code == 0, uit


def test_instrument_zonder_status_op_de_pagina_is_c5(tmp_path):
    code, uit = maak_instrument(tmp_path, pagina=LAT_PAGINA.replace("status: in gebruik", "klaar"))
    assert code == 1 and "status: in gebruik" in uit, uit


def test_instrument_zonder_kruimelpad_is_b10(tmp_path):
    code, uit = maak_instrument(tmp_path, pagina=LAT_PAGINA.replace('href="https://security-commons-nl.github.io/"', 'href="/"'))
    assert code == 1 and "[B10]" in uit, uit


def test_een_versie_in_een_testbestand_telt_niet(tmp_path):
    pagina = LAT_PAGINA.replace("versie 1.0.0 (peildatum 2026-10-30) · ", "")
    code, uit = maak_instrument(tmp_path, pagina=pagina)
    (tmp_path / "werktuig" / "tests").mkdir()
    (tmp_path / "werktuig" / "tests" / "x.test.ts").write_text("versie 9.9.9", encoding="utf-8")
    r = subprocess.run([sys.executable, str(HIER / "repo_compliance.py"), str(tmp_path / "werktuig"), "--projecten",
                        str(tmp_path / "profiel.md")], capture_output=True, text=True)
    assert r.returncode == 1 and "[C5] geen versie" in r.stdout, r.stdout


def test_kennis_in_gebruik_valt_niet_onder_c5(tmp_path):
    code, uit = maak_instrument(tmp_path, naam="leeswerk", pagina=None, ci=None)
    assert code == 0, uit

