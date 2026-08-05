# CODING-OPS.md — delegimi i kodit (D-065)

> Si Halimi delegon punë kodimi te `coding-agent` (backend **OpenCode + DeepSeek**,
> pa kosto të re — çelësi ekzistues). Lexoje para çdo detyre kodimi.

## Backend
- CLI: **OpenCode** (`opencode`), i konfiguruar në `~/.config/opencode/opencode.json`
  me providerin `deepseek` (çelësi nga `openclaw.json`) → model `deepseek/deepseek-chat`.
- Ekzekutim: `opencode run "<detyra>"` në rrënjën e projektit, PTY:true
  (kërkohet për OpenCode). Për punë të gjata: background mode.

## Rregulli i autonomisë (rosteri D-064)
| Projekt | Kodim autonom | Shënim |
|---|---|---|
| **AvokatIM** | PO | commit + JOURNAL pas çdo ndryshimi |
| **OpsHub** | PO | commit + shënim |
| **NaturalBeauty** | PO | commit + shënim |
| **EdaS** | PO, por **rregulli dy-agjentësh** | një agjent shkruan, tjetri rishikon para commit |
| **TotoTrading** | **KURRË** | para reale — vetëm raport/vëzhgim |
| **BoraLaw** | **KURRË** | vetëm vëzhgim |
| Të tjerat (sYn, CompIM…) | propozo, mos autonom | pa leje eksplicite |

## Guardrails (të detyrueshme)
1. Puno GJITHMONË në një degë/working-copy të projektit real; asnjëherë në `~/clawd`.
2. Pas çdo ndryshimi që kompilon/kalon testet: `git add -A && git commit` me mesazh
   imperativ në anglisht + shto rresht në `docs/agents/JOURNAL.md` të atij projekti
   (nëse e ka atë strukturë).
3. Kurrë `git push --force`, kurrë rishkrim historie, kurrë commit i `.env`/`data/`/`secrets/`.
4. Nëse testet dështojnë ose s'je i sigurt → NDAL, raporto në Telegram, mos commit.
5. Për TotoTrading/BoraLaw: nëse gjen problem, hap vetëm një raport — mos prek kodin.
6. Sekretet nga `secrets/CREDENTIALS.md` përdoren vetëm në makinë; kurrë në kod/commit/log.

## Kur ta përdorësh
- Ndërtim veçorish të reja, refaktorim i madh, rishikim PR-esh (në dir të përkohshëm),
  eksplorim iterativ i skedarëve. JO për fix një-rreshtash (edito vetë).
