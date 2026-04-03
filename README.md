[English](README.md) | [中文](README-CN.md) | [Deutsch](README-de.md) | [Français](README-fr.md) | [Русский](README-ru.md)

# news-digest

Multi-source AI news digest for Claude Code — fetches, summarizes, and learns from the latest AI technology news across 11 sources.

```
/news-digest                    # full digest + learning layer
/news-digest --no-learn         # news only (fast mode)
/news-digest llm agent          # filter by keyword
/news-digest --sources hn,hf    # specific sources only
```

---

## What it does

**Step 1 — Notify & fetch**: outputs an estimated-time banner (20–40 s for news, +60–80 s with learning layer) and then fetches from 11 sources in a single Bash call:

| Source | What you get |
|--------|-------------|
| `hn` | Hacker News front page |
| `arxiv` | arXiv cs.AI latest papers |
| `hf` | HuggingFace Daily Papers (curated AI) |
| `github` | GitHub Trending repositories |
| `anthropic` | Anthropic official news |
| `openai` | OpenAI news (via Jina Reader, bypasses Cloudflare) |
| `reddit` | r/MachineLearning + r/LocalLLaMA + r/agents |
| `langchain` | LangChain blog RSS |
| `github_watch` | Tracked repo releases (openclaw, opencode…) |
| `openclaw` | OpenClaw blog RSS |
| `clawhub` | ClawHub latest skill updates |

**Step 2 — Filter & deduplicate** by keyword, source authority, and title similarity. If more than 3 sources fail to return data, a `[Diagnosis]` partial-failure warning is shown at the top; if more than 50% fail, a `⚠️ [Critical Warning]` alert is shown with troubleshooting steps.

**Step 3 — Output** a structured CLI digest:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  AI News Digest  |  2026-03-22  |  23 items
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### Hacker News
1. [Title]
   Summary · link

### HuggingFace Daily Papers
1. [Paper title]
   Abstract excerpt · link
...

Sources: hn arxiv hf github anthropic  |  Failed: openai  |  Filtered by: agent mcp
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Step 4 — Learning layer** (optional, ~60–80 s): the `news-learner` agent analyzes items relevant to your AI workflow, compares them against your existing Claude Code skills/agents/patterns, and outputs prioritized recommendations:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Learning Opportunities  |  2 items analyzed
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Adopt] Tool X — real gap in our orchestration layer
  → Step 1: create new skill based on this design
  → link: https://...

[Learn] Framework Y — overlaps with existing pattern Z
  → archived to ~/.claude/projects/<project>/memory/tech-watch.md
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Recommendation levels: `[Priority Adopt]` → `[Adopt]` → `[Learn]` → `[Skip]`

- **`[Adopt]` / `[Priority Adopt]`**: interactive decision prompt appears; type a number to act, `s N` to skip, `w N` to downgrade to `[Learn]`
- **`[Learn]`**: URL-deduplicated and archived to `tech-watch.md` in the current project's memory directory
- **`[Skip]`**: noted in session, no file written

---

## Install

### Option A — Claude Code plugin (recommended)

```
/plugin marketplace update news-digest
/plugin install news-digest@news-digest
```

> First time? Add the marketplace first:
> ```
> /plugin marketplace add easyfan/news-digest
> /plugin install news-digest@news-digest
> ```

> ⚠️ **Not verified by automated tests**: `/plugin` is a Claude Code REPL built-in and cannot be invoked via `claude -p`. Run manually in a Claude Code session; not covered by skill-test pipeline (looper Stage 5).

<!--
### Option B — npx (not yet published)

```bash
npx news-digest
```
-->

### Option B — install script

```bash
# macOS / Linux
git clone https://github.com/easyfan/news-digest
cd news-digest
./install.sh

# Windows
.\install.ps1
```

```bash
# Options
./install.sh --dry-run      # preview changes without writing
./install.sh --uninstall    # remove installed files
CLAUDE_DIR=/custom ./install.sh   # custom Claude config path
```

> ✅ **Verified**: covered by the skill-test pipeline (looper Stage 5).

### Option C — manual

```bash
cp commands/news-digest.md ~/.claude/commands/
cp agents/news-learner.md  ~/.claude/agents/
```

> ✅ **Verified**: covered by the skill-test pipeline (looper Stage 5).

---

## Usage

```
/news-digest [topics...] [--sources LIST] [--limit N] [--no-learn]
```

| Argument | Description | Default |
|----------|-------------|---------|
| `topics` | Keyword filter — space-separated, OR logic | all items |
| `--sources` | Comma-separated source IDs (see table above) | all 11 sources |
| `--limit N` | Max items per source | 5 |
| `--no-learn` | Skip learning layer, output news only (~60–80 s saved) | off |
| `--channel` | Output channel (`cli` currently available; `slack`/`email`/`file` planned) | `cli` |

**Examples:**

```bash
/news-digest                             # full run, all sources
/news-digest --no-learn                  # fast — news only, no agent
/news-digest llm agent mcp               # keyword filter
/news-digest --sources hn,arxiv,hf       # three sources only
/news-digest --sources github --limit 10 # GitHub Trending top 10
/news-digest mcp --sources anthropic,openai  # two official sources, MCP filter
```

---

## Files installed

```
~/.claude/
├── commands/
│   └── news-digest.md      # /news-digest slash command
├── agents/
│   └── news-learner.md     # learning layer agent (called automatically)
└── skills/
    └── news-digest/
        └── SKILL.md        # skill definition (used by looper T3 trigger test)
```

### Package structure

```
news-digest/
├── .claude-plugin/
│   ├── plugin.json         # CC plugin manifest
│   └── marketplace.json    # marketplace entry
├── commands/news-digest.md
├── agents/news-learner.md
├── skills/news-digest/
│   └── SKILL.md
├── evals/evals.json
├── install.sh
├── install.ps1
└── package.json
```

---

## Requirements

- **Claude Code** CLI
- **curl** (system)
- **python3** (system) — used for JSON/XML parsing in inline scripts
- No other dependencies

---

## Architecture

```
/news-digest (command coordinator)
│
├── Step 0: Bash — parse args → /tmp/nd_params.json (topics, sources, limit, no_learn)
├── Step 1: Output start banner (est. time) → Bash: curl all sources → /tmp/nd_*.{json,xml,html}
├── Step 2: Bash — Python heredoc: parse → filter → deduplicate → relevance-tag
│           writes /tmp/nd_deduped.json + /tmp/nd_relevant.json
│           (⚠️ alert if >50% sources failed; [Diagnosis] if >3 failed)
├── Step 3: Output formatted CLI digest
│
└── Step 4 (if /tmp/nd_relevant.json non-empty and --no-learn not set):
    └── news-learner (agent) ← receives relevant_items_path: /tmp/nd_relevant.json
        ├── [Step 1/4] Reads ~/.claude/ descriptions to inventory platform capabilities
        ├── [Step 2/4] Reads tech-watch.md history (if exists); fetches item content via curl
        ├── [Step 3/4] Analyzes each item: problem → gap → recommendation level
        ├── [Step 4/4] Writes [Learn] items → tech-watch.md (URL-deduplicated)
        └── Returns interactive decision prompt for [Adopt]+ items
```

---

## Living Example: From News Digest to New Capability

A real adoption loop that ran on 2026-03-24, showing the full `/news-digest` → `news-learner` → immediate decision workflow.

### What triggered it

Running `/news-digest` without filters, the learning layer detected one `[Adopt]`-grade item:

> **"How we monitor internal coding agents for misalignment"** — OpenAI Engineering Blog
> *A runtime behavior monitoring framework for coding agents: evasion detection, scope overflow checks, permission anomaly detection, intent drift measurement.*

`news-learner` compared it against the platform's existing capabilities and found a **real gap**:

```
Core capability: runtime agent behavior monitoring — detecting intent drift and evasion
Current state:   skill-review only does static definition analysis; no runtime monitoring
Recommendation:  [Adopt]
Adoption plan:
  1. Create agent-monitor agent: reads task trace, checks against four-signal checklist
  2. Create agent-monitoring pattern: guides coordinators to trigger monitoring after high-risk tasks
```

The decision prompt appeared at the end of the digest:

```
⚡ Action required (1 item):

  1. [Adopt] How we monitor internal coding agents for misalignment
     Plan: create agent-monitor agent, read task trace, detect intent drift and evasion

Enter 1 to act now, s 1 to skip, w 1 to downgrade to [Learn]
```

### What was built (user typed `1`)

Three files created in the same session:

**`~/.claude/agents/agent-monitor.md`** — reads a completed task's trace file and checks four signal categories (evasion, scope overflow, permission anomaly, intent drift), writing graded alerts to `memory/agent-alerts.md`:

| Grade | Meaning | Coordinator action |
|-------|---------|-------------------|
| ✅ CLEAN | Normal | Continue |
| ⚠️ WATCH | Minor signal, possible false positive | Log, track trend |
| 🚨 ALERT | High-risk signal | Pause, notify user |
| 🛑 BLOCK | Confirmed malicious indicators | Stop + rollback |

**`~/.claude/patterns/agent-monitoring.md`** — coordinator guide: which tasks warrant post-run monitoring and how to invoke `agent-monitor`.

**`~/.claude/hooks/post_bash_error.sh`** — passive listener that fires on every failed Bash call, writing structured error entries to `memory/errors.md` and flagging high-risk patterns (non-whitelist curl, `rm -rf`, force-push, sensitive file reads) to `memory/agent-alerts.md`.

### Why this matters

The full loop — surface → analyze gap → decide → build — completed in one session. `news-learner` identified a capability the platform genuinely lacked (runtime monitoring vs. static review), and the new agent was operational the moment the user typed `1`.

This is the intended workflow: `/news-digest` surfaces what's worth knowing; `news-learner` maps it to your actual gaps; the decision prompt makes adoption frictionless.

---

## Development

### Evals

`evals/evals.json` contains 6 test cases covering argument parsing, data fetching, and the learning layer:

| ID | Scenario | What is verified |
|----|----------|-----------------|
| 1 | `/news-digest` (full run, no args) | Fetches all 11 sources, outputs digest, learning layer runs |
| 2 | `/news-digest --no-learn` | Skips the news-learner agent; outputs news summary only |
| 3 | `/news-digest llm agent` (keyword filter) | Only items matching `llm` or `agent` in title/summary are shown |
| 4 | `/news-digest --sources hn,hf --limit 3` | Fetches only specified sources, max 3 items each |
| 5 | MCP/Jina path (`JINA_API_KEY` env var present) | Jina MCP tool is used preferentially for content fetching |
| 6 | Invalid source ID | Outputs error message listing valid source IDs; no fetch attempted |

Manual testing (in a Claude Code session):
```bash
/news-digest --no-learn     # fast verification, eval 2
/news-digest llm            # keyword filter, eval 3
```

Run all evals using skill-creator's eval loop (if installed):
```bash
python ~/.claude/skills/skill-creator/scripts/run_loop.py \
  --skill-path ~/.claude/commands/news-digest.md \
  --evals-path evals/evals.json
```

---

## License

MIT
