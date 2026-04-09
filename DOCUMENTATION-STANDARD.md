# Documentatiestandaard — security-commons-nl

Elke software-repo in deze organisatie heeft minimaal dezelfde documentatiestructuur. Doel: laagdrempelig voor nieuwe contributors en gemeenten, en onderhoudbaar voor de maintainers.

## Minimumeis per software-repo

```
README.md           ← wat is het, hoe installeer je het, snelstart
docs/
├── gebruik.md      ← hoe gebruik je het (voor CISO/TIMS/eindgebruikers)
├── architectuur.md ← hoe is het gebouwd en waarom (voor contributors)
└── configuratie.md ← hoe pas je het aan voor je organisatie (als van toepassing)
```

**Uitzonderingen:**
- Repos zonder UI of software (kennisbank, anonimizer in concept-fase): geen `docs/gebruik.md` vereist
- Repos zonder configuratie-opties: geen `docs/configuratie.md` vereist

## README.md — wat er minimaal in staat

```markdown
# Naam van het project

> Één zin: wat is het en voor wie.

## Wat is het?
[Paragraaf met context en doel]

## Snel starten
[Installatie-stappen of hoe je het opent]

## Meer documentatie
- [Gebruik](docs/gebruik.md)
- [Architectuur](docs/architectuur.md)
- [Configuratie](docs/configuratie.md)  ← alleen als van toepassing
```

## docs/gebruik.md — wat er minimaal in staat

- Voor wie is dit? (CISO, ISO, IT-beheerder, bestuurder?)
- Eerste keer opstarten
- De belangrijkste workflows stap voor stap
- Bekende beperkingen

## docs/architectuur.md — wat er minimaal in staat

- Overzicht van de architectuur (diagram of tekstuele beschrijving)
- De gebruikte technologieën en waarom
- Hoe de codebase is georganiseerd
- Designkeuzes die niet vanzelf spreken

## docs/configuratie.md — wat er minimaal in staat

- Alle omgevingsvariabelen met beschrijving en voorbeeldwaarden
- Installatiestappen voor productie (inclusief HTTPS, backups)
- Hoe je de tool aanpast aan je eigen organisatie

## Screenshots

Bewust **geen** standaardeis. Screenshots verouderen snel en zijn moeilijk bij te houden. Gebruik de [demo-generator](https://github.com/security-commons-nl/grc-platform) als je automatisch schermopnames wilt maken voor externe communicatie.

## Taal

Documentatie is Nederlandstalig. Code, variabelenamen en commentaar zijn Engels (standaardpraktijk voor open source).

## Wanneer bijwerken?

Een PR die **gedrag wijzigt** dat zichtbaar is voor gebruikers, bevat ook een update van de relevante docs. Maintainers blokkeren PRs die dit missen.

---

*Verwezen vanuit [CONTRIBUTING.md](CONTRIBUTING.md).*
