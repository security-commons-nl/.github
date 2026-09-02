# Bouwplan: Ontvlechting van de voorpagina (github.io) en de werkplaats (github.com)

**Doel:** De GitHub-organisatiepagina (`github.com/security-commons-nl`) en de publieke website (`security-commons-nl.github.io`) functioneel en technisch ontvlechten.

**Aanleiding:** Het organisatieprofiel (`profile/README.md`) diende tot nu toe twee doelen tegelijk: de GitHub-overzichtspagina én de brontekst voor de website-build. Daardoor stond er op GitHub een 120 regels lange lap tekst met een enorme tabel vóórdat een bezoeker ook maar één repository te zien kreeg. Voor wie op GitHub komt (ontwikkelaars, beheerders, bijdragers) stonden de repositories in de weg; voor wie de tools zoekt (CISO's, ISO's, bestuurders) is de website op Pages de etalage.

**Architectuur:**
1. **Centrale projectenlijst:** `.github/PROJECTEN.md` wordt de enige projectenlijst (statuut B9). Bevat de tabel met status, categorie/vorm (B14), beschrijving, links en doelgroepen.
2. **Werkplaats (`github.com`):** `profile/README.md` wordt een compacte visitekaart van ~25 regels met een duidelijke verwijzing naar de website. Daaronder toont GitHub direct de repositories.
3. **Voorkant (`github.io`):** De website krijgt een eigen inhoudsbestand (`site/content.md`). `build.mjs` bouwt de voorpagina uit `content.md` gecombineerd met de kaarten uit `PROJECTEN.md`, overzichtelijk gegroepeerd naar vorm (Browser-instrumenten, Kennis, Normbronnen, Scripts).

**Status:** In uitvoering (03-09-2026).
