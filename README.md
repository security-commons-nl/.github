# .github

De spelregels van Security Commons NL: het redactiestatuut, de principes, de architectuur en de
projectentabel die op het organisatieprofiel verschijnt.

Status: infrastructuur. Deze repo bevat geen kennis en geen code voor eindgebruikers; hij legt vast hoe de
andere repo's zich gedragen. Wijkt een repo hiervan af, dan is dat werk.

## Voor wie

Iedereen die aan de commons meebouwt of wil begrijpen waarom iets is zoals het is.

## Snel starten

- [REDACTIESTATUUT.md](REDACTIESTATUUT.md): de regels waaraan elke publicatie voldoet (A1 tot A10, B1 tot B12).
- [ARCHITECTUUR.md](ARCHITECTUUR.md): welke repo's er zijn, hoe ze samenhangen, en waar het werk ligt.
- [PRINCIPLES.md](PRINCIPLES.md): waarom we dit doen.
- [BESLUITEN.md](BESLUITEN.md): append-only log van elke wijziging aan het statuut of aan de opzet.
- [profile/README.md](profile/README.md): de enige projectenlijst (statuut B9). Wijkt een ander stuk daarvan af, dan heeft het profiel gelijk.
- [plannen/](plannen/): de bouwplannen achter de commons, ook nadat ze zijn uitgevoerd.
- [profile/avatar-github.jpeg](profile/avatar-github.jpeg): het logo van de organisatie.

## Controles

```bash
python tools/repo_compliance.py ../<repo> --profiel profile/README.md   # statuut per repo
python tools/linkcheck.py ..                                           # elke link naar de commons zelf
python -m pytest tools/ -q                                             # tests van de controlescripts
```

## Werkmap opzetten

`tools/sync-org.ps1` haalt alle niet-gearchiveerde repo's van de organisatie naar de map boven `.github`,
zodat je ze naast elkaar hebt staan. Dat is wat de controles hierboven nodig hebben, en wat de
kruisverwijzingen tussen kennisbank en aanvalspaden lokaal laat werken.

```powershell
pwsh -File tools/sync-org.ps1          # of dubbelklik tools/sync-org.cmd
```

Pull-only en fast-forward-only: het script pusht nooit, merget nooit, en slaat een repo met eigen werk
over met een waarschuwing. Mappen die geen clone van de organisatie zijn, blijven met rust.

## Bijdragen

Zie [CONTRIBUTING.md](CONTRIBUTING.md).

## Licentie

EUPL-1.2, zie [LICENSE](LICENSE).
