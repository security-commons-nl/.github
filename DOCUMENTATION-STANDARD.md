# Documentatiestandaard: de README-kop

Elke levende repo begint hetzelfde, zodat een bezoeker die van de voorpagina doorklikt in tien seconden
ziet wat het is, of het werkt en hoe hij begint. Dit is statuutregel B11; `repo-compliance.yml`
controleert het in elke repo.

## De kop

    # naam

    Een zin: wat het is en voor wie.

    Status: <in gebruik | prototype | concept | gearchiveerd | infrastructuur>. <Wat werkt, wat niet.>

    ## Voor wie
    ## Snel starten
    ## Bijdragen
    ## Licentie

Het label achter `Status:` is letterlijk het label uit de projectentabel op het org-profiel (B12);
`infrastructuur` is voor repo's die geen project zijn (B8). Onder `## Bijdragen` volstaat een verwijzing
naar de CONTRIBUTING van de organisatie; onder `## Licentie` de regel "EUPL-1.2, zie LICENSE".

## Meer mag, minder niet

Alles wat een repo verder wil vertellen (architectuur, configuratie, voorbeelden) komt na deze koppen, of
in een `docs/`-map als de README anders langer dan ongeveer 1500 woorden wordt. Een `docs/`-map is geen
eis; een README die klopt wel.

## Taal

Documentatie in het Nederlands. Code, variabelen en commentaar in het Engels.

## Wanneer bijwerken

Een wijziging die zichtbaar is voor gebruikers, wijzigt ook de README. Een statuswijziging begint in de
projectentabel; de README volgt, en de controle wordt rood zolang ze verschillen.
