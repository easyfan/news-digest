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

**Step 2 — Filter & deduplicate** by keyword, source authority, and title similarity. If more than 3 sources fail to return data, a `[诊断]` partial-failure warning is shown at the top; if more than 50% fail, a `⚠️ [严重警告]` alert is shown with troubleshooting steps.

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
/plugin marketplace add easyfan/news-digest
/plugin install news-digest@news-digest
```

> **Note**: `/plugin` is a Claude Code REPL built-in command and cannot be invoked via `claude -p` (returns `Unknown skill: plugin`). Automated test pipelines (skill-test Stage 5) do not cover this install path — run it manually in a Claude Code session.

<!--
### Option B — npx (not yet published)

```bash
npx news-digest-cc
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

### Option C — manual

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
├── Step 0: Bash — parse args → /tmp/nd_params.json (topics, sources, limit, no_learn)
├── Step 1: Output start banner (est. time) → Bash: curl all sources → /tmp/nd_*.{json,xml,html}
├── Step 2: Bash — Python heredoc: parse → filter → deduplicate → relevance-tag
│           writes /tmp/nd_deduped.json + /tmp/nd_relevant.json
│           (⚠️ alert if >50% sources failed; [诊断] if >3 failed)
├── Step 3: Output formatted CLI digest
│
└── Step 4 (if /tmp/nd_relevant.json non-empty and --no-learn not set):
    └── news-learner (agent) ← receives relevant_items_path: /tmp/nd_relevant.json
        ├── [进度 1/4] Reads ~/.claude/ descriptions to inventory platform capabilities
        ├── [进度 2/4] Reads tech-watch.md history (if exists); fetches item content via curl
        ├── [进度 3/4] Analyzes each item: problem → gap → recommendation level
        ├── [进度 4/4] Writes [Learn] items → tech-watch.md (URL-deduplicated)
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

## Development

### Evals

`evals/evals.json` 包含 6 个测试用例，覆盖参数解析、数据抓取和学习层的主要路径：

| ID | 场景 | 验证重点 |
|----|------|---------|
| 1 | `/news-digest`（无参数完整运行）| 抓取全部 11 个来源，输出摘要，学习层正常执行 |
| 2 | `/news-digest --no-learn` | 跳过 news-learner agent，仅输出新闻摘要 |
| 3 | `/news-digest llm agent`（关键词过滤）| 仅展示标题或摘要含 `llm`/`agent` 的条目 |
| 4 | `/news-digest --sources hn,hf --limit 3` | 仅抓取指定来源，每源最多 3 条 |
| 5 | MCP/Jina 路径（环境变量 `JINA_API_KEY` 存在）| 优先使用 Jina MCP 工具抓取内容 |
| 6 | 非法来源 ID | 输出错误提示，列出合法来源 ID，不抓取任何内容 |

手动测试（在 Claude Code 会话中）：
```bash
/news-digest --no-learn     # 快速验证，对应 eval 2
/news-digest llm            # 关键词过滤，对应 eval 3
```

使用 skill-creator 的 eval loop 批量运行（如已安装）：
```bash
python ~/.claude/skills/skill-creator/scripts/run_loop.py \
  --skill-path ~/.claude/commands/news-digest.md \
  --evals-path evals/evals.json
```

---

## License

MIT
