# SOCIAL-BROWSER-OPS.md — korsia browser + ura OTP (Faza A4, D-066)

Kjo korsi është E BRISHTË dhe pjesërisht e KUFIZUAR. Lexoje para se të prekësh
TikTok/X. Ndërtuar më 2026-08-05 sipas planit "Halim avancim i plotë".

## Çfarë është GATI tani (i sigurt, i përdorshëm)

### Ura OTP — `~/scripts/otp_bridge.py`
Lexon kode një-përdorimëshe nga pajisja Android e lidhur (emulator-5554 ose
telefoni) përmes `adb` — SMS inbox + njoftime. Vetëm LEXIM.
```
python3 ~/scripts/otp_bridge.py latest --keyword tiktok --max-age 300
python3 ~/scripts/otp_bridge.py latest --from Google
python3 ~/scripts/otp_bridge.py sms --limit 10
```
Kthen JSON me `code`, `source`, `from`, `text`, `ts`. Përdore VETËM për të
plotësuar një login që Kllosha e ka autorizuar; KURRË mos e përcill kodin te
email/Telegram/palë e tretë.

### Browser i OpenClaw + profili real i Firefox-it
Vegla e brendshme browser mund të përdorë profilin ekzistues të Firefox-it, i
cili shpesh ka cookies të vlefshme → anashkalon login-in (dhe 2FA-në) për
llogari ku sesioni s'ka skaduar. Kjo është rruga e preferuar për veprime UI ku
s'ka API.

## Çfarë është I KYÇUR pas lejes eksplicite të Kllosha-s

**Postimi automatik në TikTok dhe X (Twitter) përmes browser-it NUK ndërtohet
dhe NUK aktivizohet pa një "PO, ndërtoje" të qartë nga Kllosha.** Arsyet:

- **Kushtet e Shërbimit:** automatizimi i UI-t të TikTok/X me browser i shkel
  Kushtet e tyre → rrezik pezullimi/mbylljeje të llogarisë.
- **Antibot:** TikTok tashmë e ka bllokuar login-in me antibot (shih
  `social-media-state.json`). Automatizimi është i pasigurt dhe i paqëndrueshëm.
- **X API** kushton (~$100/muaj) — nëse duhet vërtet X, rruga e drejtë është API
  me pagesë, jo browser.

### Kur Kllosha thotë "PO" për një platformë:
1. Konfirmo cilën platformë dhe pse (vlera > rreziku i pezullimit).
2. Ndërto veprim gjysmë-autonom me MBIKËQYRJE: Halimi përgatit postimin, e tregon
   (PO/JO), pastaj e publikon me browser duke përdorur profilin Firefox; OTP-në,
   nëse kërkohet, e merr me `otp_bridge.py`.
3. Kurrë vëllim i lartë / veprime të shpejta si bot — imito ritëm njerëzor,
   një veprim në kërkesë.
4. Regjistro çdo veprim (shih A5: `~/scripts/action_audit.py`).

## Preferenca e arkitekturës
API zyrtare > profili Firefox me cookies > automatizim login-i nga zero.
Për rrjetet sociale të biznesit (NaturalBeauty) përdor Graph API (Faza A2), JO
këtë korsi. Kjo korsi është zgjidhja e fundit, vetëm kur s'ka API dhe Kllosha e
ka miratuar shprehimisht.
