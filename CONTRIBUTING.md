# Bijdragen aan security-commons-nl

Welkom. Dit is een kenniscommons voor CISO's en ISO's in de publieke sector. Iedereen die werkende kennis wil delen of verbeteren is welkom.

## Drie manieren om bij te dragen

### 1. Issue openen
Heb je een document, aanpak of idee, maar weet je niet precies hoe je het moet indienen? Open een issue. We helpen je verder.

→ Gebruik de template **"Bijdrage aanbieden"** als je iets wilt toevoegen.
→ Gebruik **"Fout of verbetering"** als iets niet klopt of beter kan.

### 2. Pull Request
Heb je een bestand klaarstaan? Fork de repo, voeg je bestand toe op de juiste plek, en stuur een pull request.

**Mapstructuur kennisbank:**
```
kennisbank/
├── security/    ← informatiebeveiliging (BIO, ISO 27001, etc.)
├── privacy/     ← privacy en gegevensbescherming (AVG, ISO 27701)
├── bcm/         ← bedrijfscontinuïteit (ISO 22301, BIA, etc.)
└── overig/      ← aanbestedingen, governance, overige kennis
```

**Bestandsnaamgeving:** beschrijvend en zonder spaties, bijv. `bia-template-gemeente.docx` of `privacybeleid-voorbeeld.pdf`.

**Anonimiseren:** zorg dat je document geen namen, emailadressen of andere persoonsgegevens bevat. Gebruik de [anonimizer](https://github.com/security-commons-nl/anonimizer) als die beschikbaar is, of vervang handmatig door functieomschrijvingen.

### 3. Meediscussiëren
Ga naar [Discussions](../../discussions) voor vragen, ervaringen en ideeën. Geen git-kennis vereist.

## Documentatie bij software-repos

Elke software-repo heeft een minimale documentatiestructuur. Zie [DOCUMENTATION-STANDARD.md](DOCUMENTATION-STANDARD.md) voor de volledige standaard.

Kort gezegd: een PR die **gedrag wijzigt dat zichtbaar is voor gebruikers**, bevat ook een update van de relevante docs (`docs/gebruik.md`, `docs/architectuur.md` of `docs/configuratie.md`). PRs die dit missen worden teruggestuurd.

Bij het aanmaken van een nieuwe software-repo: volg de structuur in [DOCUMENTATION-STANDARD.md](DOCUMENTATION-STANDARD.md) vanaf het eerste commit.

## Review

Pull requests worden beoordeeld door de maintainers. We kijken naar:
- Inhoudelijke relevantie
- Anonimisering (geen persoonsgegevens)
- Plaatsing in de juiste map
- Documentatie bijgewerkt (bij software-repos)

## Vragen?

Open een issue of start een discussie. We reageren zo snel mogelijk.
