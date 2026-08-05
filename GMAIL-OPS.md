# GMAIL-OPS.md — menaxhimi i plotë i arifi.arber@gmail.com

**Krijuar:** 2026-08-05 (D-064). Ky skedar është BURIMI I VËRTETË për mënyrën
si ti (Halim) menaxhon inbox-in e Kllosha-s. `AVOKATIM-OPS.md` mbulon vetëm
korsinë e AvokatIM; ky skedar mbulon TË GJITHË mailbox-in.

## E vërteta që duhet ta dish

`arifi.arber@gmail.com` NUK është një adresë "e AvokatIM". Është llogaria
**personale dhe operacionale** e Kllosha-s (Arbër Arifi) — e njëjta adresë
përdoret për AvokatIM, bankën, TikTok, Binance, git, e gjitha. Ti e ke pasur
gjithmonë aksesin (të njëjtat kredenciale IMAP si te `ops_inbox_triage.py`);
thjesht nuk e kishe të qartë se çfarë ishte dhe nuk e menaxhoje dot (vetëm
lexoje). Tani e menaxhon plotësisht me `ops_mailbox.py`.

## Veglat (të gjitha printojnë JSON)

| Detyra | Komanda |
|---|---|
| Sa email të palexuar | `cd ~/AvokatIM/backend && .venv/bin/python scripts/ops_mailbox.py unread-count` |
| Kërko (sintaksë IMAP) | `... scripts/ops_mailbox.py search "FROM raiffeisen UNSEEN" --limit 20` |
| Lexo një email (read-only) | `... scripts/ops_mailbox.py read <uid>` |
| Shëno si të lexuar | `... scripts/ops_mailbox.py mark-read <uid> [<uid> ...]` |
| Arkivo (hiq nga Inbox) | `... scripts/ops_mailbox.py archive <uid> [<uid> ...]` |
| Vendos etiketë Gmail | `... scripts/ops_mailbox.py label <uid> "Emri i Etiketës"` |
| Dërgo përgjigje | `echo "TRUPI" \| ... scripts/ops_send_reply.py --to X --subject "Re: ..." [--in-reply-to "<id>"]` |

Leximi është gjithmonë me BODY.PEEK — nuk e ndryshon flag-un. Shënimi/arkivimi
e vendos `\Seen`.

## MURI I ZJARRIT — alias-et e lëndëve (kritik, mos e shkel kurrë)

Çdo lëndë e AvokatIM ka një adresë `arifi.arber+<token>@gmail.com`. Postën te
këto adresa e merr `email_ingest.py` (kërkon UNSEEN) dhe e fut si shënim/
dokument në dosjen e lëndës. `ops_mailbox.py` **refuzon vetvetiu** të prekë
flag-un e çdo mesazhi drejtuar një alias-i `+token@` (fusha `matter_alias:true`
në output). MOS provo t'i anashkalosh — nëse i shënon "të lexuar" para se t'i
marrë ingest-i, humbet posta e klientit.

## Korsitë e mailbox-it dhe protokolli

```mermaid
flowchart TD
    mail["Email hyrës"] --> q{"Cila korsi?"}
    q -->|"njoftim i platformës (From = vetë ne)"| sys["Injoro — s'kërkohet veprim"]
    q -->|"alias +token@"| ing["MOS PREK — e merr email_ingest"]
    q -->|"përgjigje outreach XK/DE ose pyetje profesioni/qytetari"| av["AvokatIM: AUTONOM (AVOKATIM-OPS.md)"]
    q -->|"përgjigje nga kompani target DE"| mna["LEAD M&A: draft + PO/JO"]
    q -->|"STOP / opt-out"| opt["Heshtje — e kap triage"]
    q -->|"PERSONALE (bankë, TikTok, privat)"| per["DRAFT + PO/JO — kurrë autonom"]
```

### Korsia PERSONALE — gjithmonë PO/JO (E RE, D-064)

Çdo email që NUK është i AvokatIM dhe kërkon përgjigje (bankë, shërbime si
TikTok/Binance/GitHub, korrespondencë private e Kllosha-s):

1. **KURRË mos përgjigju autonom.** Këto s'janë punë platforme.
2. Nëse ka nevojë përgjigje, përgatit një **draft** dhe dërgoja Kllosha-s në
   Telegram me pyetjen e vetme **"PO (dërgo) / JO (lëre)"**.
3. Firma është **"Arbër"** (ose siç e kërkon konteksti) — JO "AvokatIM" dhe
   JO "Ava Legal". Këto janë email personale, jo të biznesit.
4. Në "PO" → dërgo me `ops_send_reply.py` (regjistrohet vetvetiu te
   `data/ops/replies_log.csv`), pastaj `mark-read`. Në "JO" → lëre; mund ta
   `mark-read` ose `archive` nëse Kllosha e thotë.
5. Shumica e postës personale s'kërkon fare përgjigje (reklama, njoftime).
   Për to: përmblidhi te raporti i mëngjesit, `mark-read`/`archive` sipas
   gjykimit — pa e mbytur Kllosha-n me pyetje.

Kur je i pasigurt nëse një email është "AvokatIM" apo "personal", trajtoje si
**personal** (PO/JO) — gabimi i sigurt.

## Higjiena e inbox-it (detyrë ditore)

- Pas trajtimit të çdo emaili → `mark-read` (dhe `archive` kur s'duhet më në
  Inbox). Synimi: Inbox-i i Kllosha-s të mos mbushet me qindra të palexuar.
- Në raportin e mëngjesit shto një rresht "Higjiena e inbox-it": sa email të
  palexuar gjithsej, cili është më i vjetri, dhe sa i trajtove dje.
- Nisje: sot ka ~106 të palexuar (kryesisht reklama/njoftime + disa DSN
  bounce). Mos i prek me shumicë pa pyetur — kalo nëpër to gradualisht dhe
  raporto çka gjen (p.sh. email nga banka që mund të kërkojë vëmendje).
