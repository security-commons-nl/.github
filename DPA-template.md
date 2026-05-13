# Verwerkersovereenkomst — anonimizer-proxy

> Template voor publieke organisaties die gebruik willen maken van de gedeelde Mistral-proxy van `security-commons-nl`. Vul aan met de eigen gegevens, druk af, onderteken, mail terug naar de contactpersoon in `security-commons-nl/.github`.

**Versie:** 1.0
**Laatst gewijzigd:** 2026-05-13

---

## Partijen

| Rol | Naam | Vertegenwoordigd door |
|---|---|---|
| **Verwerkingsverantwoordelijke** | (vul gemeente / organisatie in) | (naam + functie) |
| **Verwerker** | security-commons-nl, namens [contact-naam] | (naam + functie) |

---

## 1. Voorwerp van de verwerking

De verwerker beheert een Cloudflare Worker met de naam **anonimizer-proxy**. Deze worker forward't HTTP-requests van eindgebruikers naar de Mistral chat-completions API en stuurt de respons terug. Doel: de eindgebruiker hoeft geen eigen Mistral-account te hebben om de [anonimizer-browser](https://github.com/security-commons-nl/anonimizer-browser) tool te gebruiken.

## 2. Aard en doel

| Aspect | Inhoud |
|---|---|
| **Aard** | Bytewise doorgifte van HTTP request body (tekst) en respons (JSON). |
| **Doel** | Mogelijk maken dat documenten geanonimiseerd kunnen worden zonder dat de eindgebruiker een eigen LLM-account hoeft te beheren. |
| **Soort gegevens** | De inhoud die door de eindgebruiker wordt verstuurd. Dit kán persoonsgegevens bevatten omdat de tool juist bedoeld is om die uit documenten te detecteren. |
| **Betrokkenen** | Personen die in de aangeboden documenten genoemd worden (medewerkers, inwoners, derden). |

## 3. Duur

Eén HTTP-request per verwerking. Geen opslag, geen state, geen vervolgrequests. Zodra de Mistral-respons aan de eindgebruiker is teruggegeven, is de verwerking afgelopen.

## 4. Verplichtingen van de verwerker

De verwerker:

1. **Logt geen request- of response-bodies.** Alleen geaggregeerde metrics (aantal requests per dag, latency-percentielen, foutpercentage) — geen documentinhoud.
2. **Beperkt het verwerkingsoppervlak:**
   - Alleen `POST /v1/chat/completions` wordt geforward;
   - Alleen `model: mistral-large-latest` en `response_format: json_object` worden upstream toegestaan;
   - Maximaal 4 messages per request.
3. **Implementeert technische maatregelen:**
   - TLS 1.2+ in beide richtingen (browser → worker → Mistral);
   - Mistral API-key in Cloudflare Worker secret-store, niet in source code;
   - Rate-limiting per IP (default 20 requests/minuut) tegen misbruik;
   - CORS-policy beperkt tot de officiële frontend-origin.
4. **Schakelt geen subverwerkers in** anders dan:
   - **Cloudflare Inc.** (hosting van de Worker, EU-edge);
   - **Mistral AI SAS, Frankrijk** (de daadwerkelijke LLM).
5. **Verleent de gemeente bij audit-verzoek inzage in:**
   - De source code van de proxy ([github.com/security-commons-nl/anonimizer-proxy](https://github.com/security-commons-nl/anonimizer-proxy));
   - De Cloudflare observability-configuratie (om vast te stellen dat bodies niet gelogd worden);
   - De Mistral-DPA met security-commons-nl.

## 5. Wat de verwerker NIET doet

Voor maximale helderheid: dit is een uitputtende lijst van wat de proxy buiten scope laat.

- Geen opslag van inhoud (geen database, geen filesystem, geen cache)
- Geen analyse, profiling, of training op de doorgegeven tekst
- Geen doorgifte naar andere LLM-providers dan Mistral
- Geen koppeling van requests aan natuurlijke personen anders dan via een tijdelijke IP-rate-limit counter (max 1 minuut, niet gelogd)
- Geen retentie van metrics op IP-niveau langer dan 7 dagen
- Geen commercieel hergebruik van wat dan ook

## 6. Doorgifte buiten de EU

| Subverwerker | Locatie | Adequaatheidsbesluit / SCC |
|---|---|---|
| Cloudflare Inc. | Workers draaien op de EU-edge dichtstbij de eindgebruiker. | EU Standard Contractual Clauses van toepassing op verwerking. |
| Mistral AI SAS | Frankrijk. | Geen doorgifte buiten EU. |

Concreet betekent dit dat in normaal gebruik documenten **niet** de EU verlaten.

## 7. Datalek-meldplicht

De verwerker meldt elk vermoedelijk datalek binnen 24 uur per e-mail aan de in onderdeel 1 genoemde contactpersoon van de verwerkingsverantwoordelijke, met de volgende minimale informatie: aard, betrokkenen, tijdstip, getroffen maatregelen.

## 8. Beëindiging

De verwerkingsverantwoordelijke kan deze overeenkomst per direct opzeggen door de eigen IP-range op de blocklist te laten plaatsen, of door over te stappen op de BYOK-modus in de frontend (eigen Mistral-key). De verwerker verwijdert dan eventuele residuele rate-limit counters binnen 7 dagen.

---

## Ondertekening

| | Verwerker | Verwerkingsverantwoordelijke |
|---|---|---|
| **Plaats** | | |
| **Datum** | | |
| **Naam** | | |
| **Functie** | | |
| **Handtekening** | | |

---

## Bijlage A — Wijzigingsproces

Wijzigingen aan deze template (bv. nieuwe subverwerker, gewijzigde rate-limit) worden:

1. Gepubliceerd als pull request in [security-commons-nl/.github](https://github.com/security-commons-nl/.github);
2. Geannonceerd in [de discussions-feed](https://github.com/orgs/security-commons-nl/discussions);
3. Pas effectief 30 dagen na publicatie, zodat gemeenten kunnen reviewen.

Door deze template te ondertekenen ga je akkoord dat toekomstige niet-materiële wijzigingen via dit proces lopen. Materiële wijzigingen (nieuwe subverwerker, doorgifte buiten EU, ander LLM) vereisen een nieuwe ondertekening.
