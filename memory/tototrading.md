# Memorje: Projekti TotoTrading

**Baza e dijes:** `/home/kllosha/openclaw-knowledge/` (analiza e plotë: `projects/TotoTrading.md`).

TotoTrading (`~/TotoTrading`) është agjent automatik trading-u për **Binance Coin-Margined Perpetual Futures** (~20x leverage), me vendime nga LLM (**DeepSeek `deepseek-chat`** primar) dhe një cikël vetë-optimizimi **AutoResearch** që akordon parametra numerikë (entry/exit weights, pragje DI/ADX/RSI/ATR, SuperTrend).

**Pikat kyçe që duhen mbajtur mend:**
- 3 mode: SCAN (hyrje), MANAGE (mbajtje, shmang fee-trap), EXIT (mbyllje).
- AutoResearch: simulon baseline vs candidate në 20 skenarë; pranon nëse saktësia +≥2%, përndryshe revert. Gjendja: best_score 26.3, i ndalur; dobësia kryesore = ENTRY (filter compliance ~29%).
- Arkitektura: `src/agent`, `src/autoresearch`, `src/data_flow` (BlueWhale, websocket, indikatorë), `src/data/storage` (SQLite `shared_agent_data.db`), `src/web` (dashboard FastAPI :8001).
- Integrime: Binance API, BlueWhale (:8080), DeepSeek; LLM1 lokal Qwen/Ollama tani i hequr.
- **PROBLEM:** ~24.7 GB log të papërmbajtur (`toto_agent.log` 16.9GB + `systemd_service.log` 7.8GB) — duhet rotation/truncate.
- Sekretet janë te `.env` (Binance + LLM keys) — plaintext.
