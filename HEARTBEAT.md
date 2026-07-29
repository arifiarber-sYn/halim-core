# HEARTBEAT.md — kontrollet periodike të Halimit

Në çdo heartbeat kryej këto kontrolle ME RADHË dhe raporto VETËM nëse gjen problem
(përndryshe përgjigju HEARTBEAT_OK). Mbaj gjendjen te `memory/heartbeat-state.json`
që të mos përsëritesh.

## 1. Shërbimet kritike (çdo heartbeat)
```
systemctl --user is-active toto-trading.service opshub.service avokatim.service avokatim-tunnel.service openclaw-gateway.service naturalbeauty-web.service naturalbeauty-voice.service naturalbeauty-webtunnel.service
```
Nëse ndonjë NUK është `active` → lajmëro MENJËHERË. MOS i rinis vetë — vetëm raporto.

## 1b. OpsHub API (çdo heartbeat)
```
curl -s -m 5 http://127.0.0.1:3010/api/health
```
Duhet `{"ok":true,"db":"up"}`. Çdo gjë tjetër → lajmëro.

## 1c. AvokatIM API (çdo heartbeat)
```
curl -s -m 10 http://127.0.0.1:8000/api/health
```
Duhet `{"status":"ok","app":"AvokatIM"}`. Çdo gjë tjetër (timeout, error, bosh)
→ lajmëro MENJËHERË — platforma është LIVE me përdorues realë.
(Detyrat e tjera të AvokatIM — inbox triage 10-minutësh dhe raporti i mëngjesit —
janë cron jobs më vete; roli dhe rregullat te AVOKATIM-OPS.md.)

## 1d. NaturalBeauty API (çdo heartbeat)
```
curl -s -m 5 http://localhost:3005/sq && curl -s -m 5 http://localhost:8791/health
```
Web duhet të kthejë HTML (200), voice duhet `{"ok":true,"stt":true,"tts":true}`.
Nëse ndonjëri dështon → lajmëro.

## 2. Kontejnerët docker (çdo heartbeat)
```
docker ps --format '{{.Names}} {{.Status}}'
```
Duhet të jenë UP: avokatim-caddy, avokatim-db, avokatim-redis, avokatim-livekit,
avokatim-umami, opshub-db.
Kontejner i munguar, i ndalur ose në restart-loop → lajmëro. MOS restart pa leje.

KUJDES sYn: prodhimi i sYn jeton në serverin 172.31.2.50, JO këtu (shiko
~/openclaw-knowledge/projects/sYn.md). Stack-u lokal syn-* u hoq më 2026-07-18.
Nëse ndonjë kontejner syn-* SHFAQET lokalisht, ajo është anomalia — raporto,
por MOS propozo kurrë restaurim/rindezje të stack-ut syn në këtë makinë.

## 2b. sYn prodhimi në server — kontroll read-only (çdo heartbeat)
```
~/scripts/syn-prod-status.sh --check
```
Kanali i vetëm i lejuar për sYn (çelës SSH me forced-command — s'mund të bësh
asgjë tjetër veç leximit të statusit, by design). Interpretimi:
- `verdict=OK` → asgjë; mos e përmend fare.
- `changed=yes` DHE verdict ∈ {DEGRADED, CRITICAL, UNREACHABLE} → lajmëro
  Kllosha-n MENJËHERË me verdiktin + p0 count. Për detaje merr JSON-in e plotë
  (`~/scripts/syn-prod-status.sh`) dhe citoje fushën `criticalAlerts24h`.
- `verdict=ATTENTION` → përmende vetëm në raportin e mëngjesit (jo alarm) —
  alarmet critical i ndjek agjenti HELM në server; ti je kanal njoftimi, jo zgjidhës.
- KURRË mos tento të "rregullosh" gjë në server — as me sudo, as me çelësin
  personal të Kllosha-s. Puna në sYn bëhet nga agjenti HELM në server.

## 3. Disku (2x në ditë mjafton)
```
df -h / | tail -1
```
Nëse përdorimi > 85% → lajmëro me du -sh të folderave më të mëdhenj.

## 4. TotoTrading shëndeti (2x në ditë)
```
journalctl --user -u toto-trading.service --since "-6h" -p err --no-pager | tail -20
```
Gabime të përsëritura → lajmëro me përmbledhje. MOS ndërhy në trading.

## 5. Backup-et (1x në ditë, mëngjes)
- `tail -5 ~/syn-backups/cron.log` — dështime të syn-backup?
- `ls -la /var/log/backup-system-no-usb.flag 2>/dev/null` — nëse ekziston, USB s'ishte i kyçur.

## 6. Siguria — SSH auth (çdo heartbeat)
```
journalctl -u sshd --since "-1h" --no-pager 2>/dev/null | grep -ci 'Failed password\|Invalid user' || echo "s'u lexua"
```
0 = qetësi. Mbi 10 në një orë → lajmëro (sulm brute-force i mundshëm).

## 6b. Siguria — firewall (çdo heartbeat)
```
firewall-cmd --state 2>/dev/null && firewall-cmd --list-ports 2>/dev/null
```
Duhet `running` dhe lista e portave të jetë vetëm ajo që pritet (9090/tcp).
Nëse NUK është `running` ose shfaqen porta të tjera (sidomos range-at e gjera) → lajmëro.

## 6c. Siguria — fail2ban (çdo heartbeat)
```
sudo -n fail2ban-client status sshd 2>/dev/null | head -5
```
Duhet jail `sshd` aktiv. Nëse mungon ose ka Currently banned > 0 → lajmëro.

## Rregulla
- Natën (23:00–08:00) raporto vetëm urgjencat (shërbim i rënë, disk plot).
- Asnjë veprim korrigjues pa leje — vetëm diagnostiko dhe raporto.
