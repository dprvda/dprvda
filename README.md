<h1 align="center">From Senior 3D designer to vibe coding... huh 🤷</h1>

<p align="center">
<i>L'Oréal, Crocs, Lacoste, Breitling, etc. — a small slice of the list.<br>
Always had code under the design work. In March 2026 I went all-in. This was not the plan. Having way too much fun.</i>
</p>

<p align="center">
  <a href="https://ccgather.com/leaderboard"><img src="https://img.shields.io/badge/%E2%9A%A1%20Claude%20tokens-~104B-0d1117?style=for-the-badge&labelColor=0d1117" alt="~104B Claude tokens"></a>
  <a href="https://ccgather.com/leaderboard"><img src="https://img.shields.io/badge/%F0%9F%8F%86%20ccgather-%231%20global-0d1117?style=for-the-badge&labelColor=0d1117" alt="#1 globally on ccgather"></a>
</p>

### The strange journey

5 years designing things for brands you've heard of — always with a scripting layer underneath. Custom Houdini functions and sim setups. Render farms. Project-management app experiments. And one production pipeline that automated rendering **6000 CGI videos** through hundreds of Python scripts gluing C4D, After Effects, Houdini, ffmpeg, Blender, and whatever else the deliverable needed.

It always felt like part of the job, not a career. Then in March 2026 I asked Claude to help with a script. Then I asked for one more thing. Then I forgot to stop. Somewhere in there it stopped being a layer under design work and became *the* thing.

20+ projects on disk now, ~104B Claude tokens through the wire, somehow #1 globally on usage. Some ship to production. Some are research. Some started as one thing and accidentally became another. None were the plan.

### Since March 2026

- **Autonomous research pipelines** — orchestrating swarms of headless AI workers across isolated git worktrees. Stream-JSON parsing of subprocess output, quota-wall recovery (parse → sleep → resume), exhaustion detection, supervisor-of-supervisors crash recovery, multi-channel alerting across 6 fan-outs.
- **Sub-millisecond reactive systems** in Rust — 8-crate workspace, Tokio + lock-free shared-memory IPC, 11 simultaneous venue feeds, deterministic simulation harness with production parity, atomic SQLite-WAL → Parquet snapshots, cross-compilation to ARM production targets.
- **Gamified knowledge platforms** — React 19 + TypeScript, 800+ questions across 40+ topics, additive schema migrations through 15+ versions, server-side merge-on-write for offline-first multi-device sync, confidence-vs-accuracy bias correction.
- **LLM-orchestrated workflow systems** — Python + NetworkX DAG analysis with critical-path resolution, dual-priority decomposition (original intent vs current actionable state), conversational interface with hard ASK-PROPOSE-CONFIRM gates.

Four different systems. Won't tell you which is which.

### How I work

- **Multi-agent throughput, not token efficiency** — fanning out work across parallel Claude workers to squeeze maximum production speed. Tokens are cheap; calendar time is expensive.
- **Custom Claude Code setup** — 10+ domain-specific skills, 9+ slash commands, 8+ hooks across projects for safety gates, rule re-injection, doc freshness checks, and operational discipline
- **Project memory discipline** — 448 markdown files across 20 active projects: feedback, lessons, architecture decisions, session handoffs
- **Hard pre-commit gates** — AI code critic, doc freshness cascades, schema versioning enforcement, supply chain audits, RustSec
- **Operating rules** (from my global CLAUDE.md) — no silent decisions, verify every fix with real data, surgical changes only, root causes not workarounds, no auto-pause

### Stack

Rust (Tokio · Alloy · ONNX · iceoryx2 · sqlx) · Python (Flask · NetworkX · httpx · pytest) · TypeScript / React 19 / Vite / Zustand / TanStack Query · whatever else the problem needs

### Receipts

- Designer for 5 years · developer since March 2026
- ~104B Claude tokens · #1 globally on [ccgather](https://ccgather.com/leaderboard)
- ~1.7B tokens / day average · 1,828 sessions
- 20+ active projects · 448 memory files
- In one project alone: 50 architecture decision records, 12 zero-bypass pre-commit gates, 8 Rust crates, 11 venue feeds
- In another: 820 exam questions, 41 topics, 15 schema versions

---

![stats](https://dprvda-stats.vercel.app/api?username=dprvda&show_icons=true&count_private=true&hide_rank=true&theme=github_dark&hide_border=true)
![langs](https://dprvda-stats.vercel.app/api/top-langs/?username=dprvda&layout=compact&count_private=true&theme=github_dark&hide_border=true&langs_count=8)
![graph](https://github-readme-activity-graph.vercel.app/graph?username=dprvda&theme=github-compact&hide_border=true&area=true)
