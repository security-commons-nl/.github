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

## Controles

```bash
python tools/repo_compliance.py ../<repo> --profiel profile/README.md   # statuut per repo
python tools/linkcheck.py ..                                           # elke link naar de commons zelf
python -m pytest tools/ -q                                             # tests van de controlescripts
```

## Bijdragen

Zie [CONTRIBUTING.md](CONTRIBUTING.md).

## Licentie

EUPL-1.2, zie [LICENSE](LICENSE).
