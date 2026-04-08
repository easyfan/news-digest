---
name: news-digest
description: |
  从 HN、arXiv、GitHub Trending、Anthropic、OpenAI、HuggingFace 等多平台抓取 AI 技术新闻，生成摘要并通过 news-learner agent 分析与现有能力的差距，输出 [Adopt]/[Learn] 建议。
  用于："/news-digest"、"看看最新 AI 新闻"、"今天有什么技术动态"、"抓一下新闻"、"AI 最近有什么进展"、"news digest"、"latest AI news"、"tech news"、"what's new in AI"。
  支持 --no-learn（跳过学习层，仅摘要）和 --mode=cron（非交互批处理）。不适用于非 AI 领域新闻或单篇文章的解读。
license: MIT
metadata:
  version: "1.0.0"
  author: cc-meta-project
  platforms: claude-code
  requires: "commands/news-digest.md + agents/news-learner.md"
---

# news-digest

Multi-source AI news fetching, summarization, and intelligent learning layer analysis.

## Install

```bash
# Option A: Claude Code plugin marketplace
/plugin marketplace add easyfan/news-digest

# Option B: npx (no clone needed)
npx news-digest

# Option C: clone and run install script
./install.sh              # macOS / Linux
.\install.ps1             # Windows

# Option D: manual copy
cp commands/news-digest.md ~/.claude/commands/
cp agents/news-learner.md  ~/.claude/agents/
```

## Usage

```
/news-digest                          # full digest from all sources (with learning layer)
/news-digest --no-learn               # fast mode — news only
/news-digest llm agent                # filter by keyword
/news-digest --sources hn,arxiv,hf    # specific sources only
/news-digest --limit 10               # max 10 items per source
/news-digest mcp --sources anthropic,openai
```

## Sources

| Source ID | Name | Content |
|-----------|------|---------|
| `hn` | Hacker News | Front page posts |
| `arxiv` | arXiv cs.AI | AI papers |
| `hf` | HuggingFace Daily Papers | Curated AI papers |
| `github` | GitHub Trending | Trending repositories |
| `anthropic` | Anthropic News | Official updates |
| `openai` | OpenAI News | Official updates |
| `reddit` | Reddit AI communities | r/MachineLearning + r/LocalLLaMA + r/agents |
| `langchain` | LangChain Blog | Blog RSS |
| `github_watch` | GitHub repo watch | Tracked repository releases |
| `openclaw` | OpenClaw Blog | OpenClaw updates |
| `clawhub` | ClawHub Skills | Latest skill updates |
| `devto` | DEV Community | AI articles (tag:ai, top reacted) |

## Requirements

- `curl` (system)
- `python3` (system — used for JSON/XML parsing)
- Claude Code CLI
