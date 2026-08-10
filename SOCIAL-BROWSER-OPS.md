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

## Autonomia (D-070) dhe pengesat REALE (feasibility, jo leje)

Vendim i Klloshës (D-070): autonomi pa limite + njoftim-pas. Pra këtu s'ka më
"PO/JO për leje". Por disa platforma kanë pengesa **teknike/ToS** që rrezikojnë
vetë llogarinë e Klloshës — kjo s'është kufi autonomie, është mbrojtje e aseteve
të tij. Rendi mbetet: **API zyrtare > profili Firefox me cookies > login nga zero.**

### Meta (Facebook/Instagram — NaturalBeauty): GATI pas 1 hapi OAuth
- Publisher-i i ndërtuar: `~/NaturalBeauty/src/lib/social.ts` (FB feed/photos +
  IG dy-hapësh), me rrjedhë miratimi te `/admin/social` (APPROVED → cron boton).
- Mungojnë vetëm: `PAGE_ACCESS_TOKEN`, `FB_PAGE_ID`, `IG_USER_ID`.
- Këto s'mintohen dot pa **pëlqimin OAuth të Klloshës** (lejet `pages_manage_posts`,
  `instagram_content_publish`) — user-token-i aktual ka vetëm `email/public_profile`.
- **Hapi i vetëm i Klloshës:** lidh Faqen FB + IG Business, jep pëlqimin një herë,
  pastaj Halimi ekzekuton `~/NaturalBeauty/scripts/meta_token_setup.py --write-env`
  (short-lived → long-lived + zbulon ID-të). Runbook: `~/NaturalBeauty/docs/agent/SOCIAL-SETUP.md`.
- Pas kësaj: Halimi **boton autonom** përmes rrjedhës së miratimit + njofton pas.

### TikTok / X: preferoj API, browser-posting mbetet rrezik
- TikTok e ka bllokuar login-in me **antibot** (`social-media-state.json`:
  `browser_login_blocked_antibot`) — automatizim UI i paqëndrueshëm + shkel ToS
  → rrezik pezullimi. Mos posto me browser; prit qasje **TikTok Content Posting API**.
- **X**: automatizim UI shkel ToS; rruga e drejtë është **X API** (~$100/muaj).
- Pra këto s'i bllokon leja e Klloshës, i bllokon fizibiliteti. Nëse Kllosha
  siguron qasje API, Halimi i aktivizon menjëherë (autonom + njoftim-pas).

### Kur boton (kudo që është fizibël):
1. Përgatit postimin; për veprime me ndikim publik bëj një screenshot para/pas.
2. `halim_guard.py check --domain social --account <fb|ig|tiktok|x> --action "post ..."`.
3. Boto (API > Firefox cookies); OTP me `otp_bridge.py` nëse kërkohet.
4. `halim_guard.py audit --account <...> --action "botova ..." --detail "..." --result ok --notify`.
5. Ritëm njerëzor, jo bot; kredenciale/OTP kurrë jashtë makinës.
