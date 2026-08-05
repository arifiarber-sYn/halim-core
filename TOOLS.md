# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

### TikTok Developer

- Email: arifi.arber@gmail.com
- Password: @17364tiktok46371@
- Regjistruar: 2026-07-24

### Kredenciale të përgjithshme (shtuar 2026-07-30)

- Përdoruesi: Kllosha (K e madhe)
- Fjalëkalimi: Eda2026!
- Shënim: Shtuar nga Kllosha më 30 korrik 2026. Ende pa kontekst specifik.

---

## Skills të aktivizuara (D-065, 2026-08-05)

Falas, Linux-safe, të kuruara. CLI-backed skills tregojnë "needs setup" derisa
CLI-ja instalohet në përdorimin e parë (OpenClaw e instalon automatikisht).

| Skill | Për çfarë | Status |
|---|---|---|
| **healthcheck** | Auditim sigurie i makinës (SSH, firewall, update) | ready |
| **skill-creator** | Ndërto/edito skills të reja për detyra specifike | ready |
| **weather** | Moti + parashikim (web_fetch) | ready |
| **session-logs** | Analizo logjet e mia (vetë-përmirësim); do `rg`/`jq` | needs `rg` |
| **summarize** | Transkripto/përmbledh URL/PDF/YouTube (pa API) | CLI on 1st use |
| **blogwatcher** | Monitoro RSS/Atom (ndryshime ligjore, konkurrentë) | CLI on 1st use |
| **nano-pdf** | Redakto PDF me gjuhë natyrale (oferta, dokumente) | CLI on 1st use |
| **mcporter** | Menaxho servera MCP (mundësues për të ardhmen) | CLI on 1st use |

NUK aktivizohen: skills macOS (apple-*, imsg, sonoscli, peekaboo, things-mac),
github/gh-issues (asnjë remote), voice-call/wacli/xurl (me pagesë — më vonë),
model-usage/ordercli (të pavlefshme këtu).

---

Add whatever helps you do your job. This is your cheat sheet.
