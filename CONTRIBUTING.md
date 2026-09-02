# Bijdragen aan security-commons-nl

Welkom. Dit is een kenniscommons voor CISO's en ISO's in de publieke sector. Iedereen die werkende kennis wil delen of verbeteren is welkom.

## Drie manieren om bij te dragen

### 1. Issue openen
Heb je een document, aanpak of idee, maar weet je niet precies hoe je het moet indienen? Open een issue. We helpen je verder.

→ Gebruik de template **"Bijdrage aanbieden"** als je iets wilt toevoegen.
→ Gebruik **"Fout of verbetering"** als iets niet klopt of beter kan.

### 2. Pull Request
Heb je een stuk klaarstaan? Fork de repo, zet het op de juiste plek, en stuur een pull request.
Wat "de juiste plek" is, legt het [redactiestatuut](REDACTIESTATUUT.md) vast; de build controleert
het en noemt bij een afwijking het regelnummer.

**Mapstructuur kennisbank:**
```
kennisbank/
├── security/    ← informatiebeveiliging (BIO, ISO 27001, etc.)
├── privacy/     ← privacy en gegevensbescherming (AVG, ISO 27701)
├── bcm/         ← bedrijfscontinuïteit (ISO 22301, BIA, etc.)
└── governance/  ← beleid, governance, aanbestedingen, overige kennis
```

**Eén stuk is één map** (statuut B1). Binnen een vakgebied maak je een map met een korte naam in
kleine letters en koppeltekens (`bia-sjabloon`, `passkeys-invoeren`), en daarin een `README.md`.
Losse bestanden direct in `security/` of `privacy/` worden geweigerd, en dieper dan twee lagen
mag niet.

**Frontmatter bovenaan die README** (statuut B2): acht vaste velden, `titel`, `vakgebied`, `type`,
`normen`, `peildatum` of `versie`, `herkomst`, `status` en `samenvatting`. Een veld `auteur`
bestaat niet; herkomst is een rol of een organisatietype, nooit een naam (statuut A1 en A3).

**Markdown is de bron** (statuut B3). Een docx, xlsx of pdf mag alleen als er geen redelijke
markdown-vorm is, en dan met een README die zegt wat erin zit. Wat in de map ligt, staat als link
in de README, anders kan een lezer er vanaf de pagina niet bij.

De indexpagina's genereert `tools/build.py`; die hoef je niet te maken en met de hand bewerken
heeft geen zin, want de volgende build overschrijft ze (statuut B4).

**Anonimiseren:** zorg dat je document geen namen, emailadressen of andere persoonsgegevens bevat. Gebruik de [anonimizer](https://github.com/security-commons-nl/anonimizer-local) als die beschikbaar is, of vervang handmatig door functieomschrijvingen.

### 3. Een vraag stellen
Loop je ergens tegenaan en zoek je een voorbeeld dat werkt? Ga naar [Discussions](../../discussions),
categorie *Hulpvraag uit de praktijk*. Geen git-kennis vereist, en je hoeft je naam en je organisatie er
niet bij te zetten; een schuilnaam is prima (statuut A11).

Zet er wel bij waar je zelf al staat, wat je zoekt en wat je met het antwoord gaat doen. Een vraag zonder
dat laatste blijft meestal onbeantwoord, want dan weet niemand waar zijn tijd landt.

### 4. Meediscussiëren
Ervaringen met wat er al staat zijn net zo waardevol als een nieuw stuk. Wat werkte niet, wat moest je
aanpassen voor je eigen organisatie, wat ontbrak.

## Voor het eerst hier?

Nog nooit een issue geopend? Geen probleem. In vier stappen deel je een document, idee of verbetering.

![Bijdrage-flow in vier stappen](profile/bijdrage-flow-v2.svg)

### Per project: waar begin je

Klik op een van de onderstaande knoppen, er wordt een formulier voor je klaargezet. Je hoeft alleen de vragen in te vullen die voor jou relevant zijn, wij helpen je met de rest.

| Voor | Repository | Start hier |
|---|---|---|
| Iets delen over informatiebeveiliging, privacy of continuïteit | kennisbank | [Bijdrage aanbieden](https://github.com/security-commons-nl/kennisbank/issues/new?template=bijdrage-aanbieden.yml) |
| Bestuursdashboard (game) verbeteren of scenario toevoegen | weerbaarheid-game | [Bijdrage aanbieden](https://github.com/security-commons-nl/weerbaarheid-game/issues/new?template=bijdrage-aanbieden.yml) |
| Testdocument of verbeterpunt voor anonimizer-local (de CLI) | anonimizer-local | [Bijdrage aanbieden](https://github.com/security-commons-nl/anonimizer-local/issues/new?template=bijdrage-aanbieden.yml) |
| Bug of feature-wens voor de browser-versie van de anonimizer | anonimizer-browser | [Bijdrage aanbieden](https://github.com/security-commons-nl/anonimizer-browser/issues/new/choose) |
| Ervaring met security-posture uit een interventie | security-posture-tool | [Bijdrage aanbieden](https://github.com/security-commons-nl/security-posture-tool/issues/new?template=bijdrage-aanbieden.yml) |
| Hosting-scenario of referentiearchitectuur | hosting-bouwblokken | [Bijdrage aanbieden](https://github.com/security-commons-nl/hosting-bouwblokken/issues/new?template=bijdrage-aanbieden.yml) |
| Idee voor de CISO-dirigent of beleidsondersteuning | cisochat | [Bijdrage aanbieden](https://github.com/security-commons-nl/cisochat/issues/new?template=bijdrage-aanbieden.yml) |
| Ervaring, vals-positief of nieuwe bron voor de publicatiescan | publicatiescan | [Bijdrage aanbieden](https://github.com/security-commons-nl/publicatiescan/issues/new?template=bijdrage-aanbieden.yml) |

### Geen GitHub-account?

Twee opties:

1. **Aanmelden duurt 2 minuten**, [github.com/signup](https://github.com/signup). Alleen e-mail en wachtwoord.
2. **Of vraag iemand in je netwerk** die al een account heeft om namens jou een issue te openen. De inhoud is wat telt, niet wie klikt.

### Wat kan ik verwachten?

- **Snelheid**: we reageren doorgaans binnen een week.
- **Privacy**: bevat je document persoonsgegevens? Meld het in het formulier, wij helpen je anonimiseren met de [anonimizer-local](https://github.com/security-commons-nl/anonimizer-local) vóór publicatie.
- **Erkenning**: bijdragen worden in de versiegeschiedenis zichtbaar vermeld, tenzij je anoniem wilt blijven.

## Documentatie bij software-repos

Elke repo begint met dezelfde kop; zie de [documentatiestandaard](DOCUMENTATION-STANDARD.md). De
controle `repo-compliance.yml` draait in elke repo en zegt precies wat er ontbreekt.

## Review

Pull requests worden beoordeeld door de maintainers. We kijken naar:
- Inhoudelijke relevantie
- Anonimisering (geen persoonsgegevens)
- Plaatsing in de juiste map
- Documentatie bijgewerkt (bij software-repos)

## Links controleren

Een dode link naar buiten is vervelend; een dode link naar je eigen site is een gebroken belofte. Zet de
repo's naast elkaar in een werkmap en draai vanuit `.github`:

```bash
python tools/linkcheck.py ..
```

Het script controleert elke link naar `security-commons-nl.github.io` en naar een repo van de
organisatie. Een bestand binnen een repo wordt op schijf gecontroleerd; een link naar een repo of een
pagina wordt met een HTTP-verzoek getoetst. Dat laatste is met opzet: een lokale map bewijst niets over
wat de lezer ziet, want een verwijderde repo laat zijn kloon gewoon staan.
Externe sites blijven buiten beschouwing: die gaan stuk zonder dat wij er iets aan kunnen doen.
Verwacht: `0 dood`. Elke regel `DOOD:` is werk in de genoemde bron.

## Vragen?

Open een issue of start een discussie. We reageren zo snel mogelijk.
