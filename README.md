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

**Step 1 — Fetch** from 11 sources in a single Bash call:

| Source | What you get |
|--------|-------------|
| `hn` | Hacker News front page |
| `arxiv` | arXiv cs.AI latest papers |
| `hf` | HuggingFace Daily Papers (curated AI) |
| `github` | GitHub Trending repositories |
| `anthropic` | Anthropic official news |
| `openai` | OpenAI news (may be Cloudflare-blocked) |
| `reddit` | r/MachineLearning + r/LocalLLaMA + r/agents |
| `langchain` | LangChain blog RSS |
| `github_watch` | Tracked repo releases (openclaw, opencode…) |
| `openclaw` | OpenClaw blog RSS |
| `clawhub` | ClawHub latest skill updates |

**Step 2 — Filter & deduplicate** by keyword, source authority, and title similarity.

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
  → archived to tech-watch.md for later review
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Recommendation levels: `[Priority Adopt]` → `[Adopt]` → `[Learn]` → `[Skip]`

---

## Install

### Option A — Claude Code plugin (recommended)

```
/plugin marketplace add easyfan/news-digest
```

### Option B — npx

```bash
npx news-digest-cc
```

### Option C — install script

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

### Option D — manual

```bash
cp commands/news-digest.md ~/.claude/commands/
cp agents/news-learner.md  ~/.claude/agents/
```

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
| `--no-learn` | Skip learning layer, output news only (fast) | off |

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
│   └── news-digest.md    # /news-digest slash command
└── agents/
    └── news-learner.md   # learning layer agent (called automatically)
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
├── Step 1: Bash — curl all sources → /tmp/nd_*.{json,xml,html}
├── Step 2: Bash — Python heredoc: parse → filter → deduplicate → relevance-tag
├── Step 3: Output formatted CLI digest
│
└── Step 4 (if relevant_items found and --no-learn not set):
    └── news-learner (agent)
        ├── Reads ~/.claude/commands/ + agents/ + patterns/ descriptions
        ├── Reads tech-watch.md history (if exists)
        ├── Fetches full content for each relevant item (curl)
        ├── Analyzes: problem → gap → recommendation level
        ├── Writes [Learn] items → tech-watch.md
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
核心能力: 运行时 agent 行为监控 — 检测意图漂移和规避行为
我们现有: skill-review 仅做静态定义审查，无运行时动态行为监控
推荐等级: [Adopt]
采纳方案:
  1. 创建 agent-monitor agent，读取任务 trace，对照四维检测清单生成告警
  2. 创建 agent-monitoring pattern，指导协调者在高风险任务后触发监控
```

The decision prompt appeared at the end of the digest:

```
⚡ 需要立即决策的条目（1 条）：

  1. [Adopt] How we monitor internal coding agents for misalignment
     采纳方案：创建 agent-monitor agent，读取任务 trace，检测意图漂移和规避行为

输入 1 立即执行，s 1 跳过，w 1 降级观察
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

## License

MIT
