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
