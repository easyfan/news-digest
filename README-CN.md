[English](README.md) | [中文](README-CN.md) | [Deutsch](README-de.md) | [Français](README-fr.md) | [Русский](README-ru.md)

# news-digest

Claude Code 多源 AI 技术新闻摘要——从 11 个来源抓取、汇总最新 AI 技术动态，并通过学习层提供智能分析。

```
/news-digest                    # 完整摘要 + 学习层
/news-digest --no-learn         # 仅新闻（快速模式）
/news-digest llm agent          # 按关键词过滤
/news-digest --sources hn,hf    # 指定来源
```

---

## 功能介绍

**步骤 1 — 通知 & 抓取**：输出预计耗时提示（新闻约 20–40 秒，含学习层额外 +60–80 秒），然后通过单次 Bash 调用从 11 个来源抓取内容：

| 来源 | 内容 |
|------|------|
| `hn` | Hacker News 首页 |
| `arxiv` | arXiv cs.AI 最新论文 |
| `hf` | HuggingFace 每日精选论文 |
| `github` | GitHub Trending 仓库 |
| `anthropic` | Anthropic 官方新闻 |
| `openai` | OpenAI 新闻（通过 Jina Reader，绕过 Cloudflare） |
| `reddit` | r/MachineLearning + r/LocalLLaMA + r/agents |
| `langchain` | LangChain 博客 RSS |
| `github_watch` | 追踪仓库的 Release（openclaw、opencode 等） |
| `openclaw` | OpenClaw 博客 RSS |
| `clawhub` | ClawHub 最新 skill 更新 |

**步骤 2 — 过滤 & 去重**：按关键词、来源权重和标题相似度去重。若超过 3 个来源抓取失败，顶部显示 `[诊断]` 部分失败警告；若超过 50% 失败，显示 `⚠️ [严重警告]` 并附故障排查步骤。

**步骤 3 — 输出**结构化 CLI 摘要：

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  AI News Digest  |  2026-03-22  |  23 条
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### Hacker News
1. [标题]
   摘要 · 链接

### HuggingFace 每日精选
1. [论文标题]
   摘要节选 · 链接
...

来源: hn arxiv hf github anthropic  |  失败: openai  |  过滤词: agent mcp
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**步骤 4 — 学习层**（可选，约 60–80 秒）：`news-learner` agent 分析与 AI 工作流相关的条目，与现有 Claude Code skills/agents/patterns 对比，输出优先级推荐：

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  学习机会  |  分析了 2 条
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Adopt] 工具 X — 编排层存在真实缺口
  → 步骤 1：基于此设计创建新 skill
  → 链接: https://...

[Learn] 框架 Y — 与现有模式 Z 有重叠
  → 已归档至 ~/.claude/projects/<project>/memory/tech-watch.md
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

推荐等级：`[Priority Adopt]` → `[Adopt]` → `[Learn]` → `[Skip]`

- **`[Adopt]` / `[Priority Adopt]`**：出现交互式决策提示，输入编号立即执行，`s N` 跳过，`w N` 降级为 `[Learn]`
- **`[Learn]`**：URL 去重后归档至当前项目 memory 目录的 `tech-watch.md`
- **`[Skip]`**：记录在会话中，不写入任何文件

---

## 安装

### 方式 A — Claude Code 插件市场（推荐）

```
/plugin marketplace add easyfan/news-digest
/plugin install news-digest@news-digest
```

> ⚠️ **未经自动化验证**：`/plugin` 是 Claude Code REPL 内置命令，无法通过 `claude -p` 调用，需在 Claude Code 会话中手动执行；不在 skill-test 流水线（looper Stage 5）覆盖范围内。

<!--
### 方式 B — npx（未发布，暂不可用）

```bash
npx news-digest
```
-->

### 方式 B — 安装脚本

```bash
# macOS / Linux
git clone https://github.com/easyfan/news-digest
cd news-digest
./install.sh

# Windows
.\install.ps1
```

```bash
# 选项
./install.sh --dry-run      # 预览变更，不实际写入
./install.sh --uninstall    # 卸载已安装文件
CLAUDE_DIR=/custom ./install.sh   # 指定自定义 Claude 配置目录
```

> ✅ **已验证**：已通过 skill-test 流水线自动化验证（looper Stage 5）。

### 方式 C — 手动

```bash
cp commands/news-digest.md ~/.claude/commands/
cp agents/news-learner.md  ~/.claude/agents/
```

> ✅ **已验证**：已通过 skill-test 流水线自动化验证（looper Stage 5）。

---

## 使用方式

```
/news-digest [topics...] [--sources LIST] [--limit N] [--no-learn]
```

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `topics` | 关键词过滤，空格分隔，OR 逻辑 | 全部条目 |
| `--sources` | 逗号分隔的来源 ID（见上表） | 全部 11 个来源 |
| `--limit N` | 每个来源最多条数 | 5 |
| `--no-learn` | 跳过学习层，仅输出新闻（节省约 60–80 秒） | 关 |
| `--channel` | 输出渠道（目前仅 `cli`；`slack`/`email`/`file` 计划中） | `cli` |

**示例：**

```bash
/news-digest                             # 完整运行，所有来源
/news-digest --no-learn                  # 快速模式——仅新闻，无 agent
/news-digest llm agent mcp               # 关键词过滤
/news-digest --sources hn,arxiv,hf       # 三个来源
/news-digest --sources github --limit 10 # GitHub Trending 前 10
/news-digest mcp --sources anthropic,openai  # 两个官方来源，MCP 过滤
```

---

## 安装的文件

```
~/.claude/
├── commands/
│   └── news-digest.md      # /news-digest 命令
├── agents/
│   └── news-learner.md     # 学习层 agent（自动调用）
└── skills/
    └── news-digest/
        └── SKILL.md        # skill 定义（供 looper T3 触发测试使用）
```

---

## 依赖要求

- **Claude Code** CLI
- **curl**（系统工具）
- **python3**（系统工具）——用于内联脚本中的 JSON/XML 解析
- 无其他依赖

---

## 架构

```
/news-digest（命令协调者）
│
├── 步骤 0：Bash — 解析参数 → /tmp/nd_params.json（topics、sources、limit、no_learn）
├── 步骤 1：输出启动提示（预计耗时）→ Bash: curl 所有来源 → /tmp/nd_*.{json,xml,html}
├── 步骤 2：Bash — Python heredoc：解析 → 过滤 → 去重 → 相关性标记
│           写入 /tmp/nd_deduped.json + /tmp/nd_relevant.json
│           （>50% 来源失败时 ⚠️ 告警；>3 个失败时 [诊断] 警告）
├── 步骤 3：输出格式化 CLI 摘要
│
└── 步骤 4（/tmp/nd_relevant.json 非空且未设 --no-learn 时）：
    └── news-learner（agent）← 接收 relevant_items_path: /tmp/nd_relevant.json
        ├── [进度 1/4] 读取 ~/.claude/ 描述，盘点平台现有能力
        ├── [进度 2/4] 读取 tech-watch.md 历史（如存在）；通过 curl 抓取条目内容
        ├── [进度 3/4] 逐条分析：问题 → 缺口 → 推荐等级
        ├── [进度 4/4] 将 [Learn] 条目写入 tech-watch.md（URL 去重）
        └── 返回 [Adopt]+ 条目的交互式决策提示
```

---

## 实战示例：从新闻摘要到新能力

2026-03-24 的真实采纳循环，展示完整的 `/news-digest` → `news-learner` → 即时决策工作流。

### 触发原因

无过滤运行 `/news-digest`，学习层检测到一条 `[Adopt]` 级条目：

> **"How we monitor internal coding agents for misalignment"** — OpenAI Engineering Blog
> *运行时 agent 行为监控框架：规避行为检测、scope 溢出检查、权限异常检测、意图漂移测量。*

`news-learner` 与平台现有能力对比后发现了**真实缺口**：

```
核心能力: 运行时 agent 行为监控 — 检测意图漂移和规避行为
我们现有: skill-review 仅做静态定义审查，无运行时动态行为监控
推荐等级: [Adopt]
采纳方案:
  1. 创建 agent-monitor agent，读取任务 trace，对照四维检测清单生成告警
  2. 创建 agent-monitoring pattern，指导协调者在高风险任务后触发监控
```

摘要结束时出现决策提示：

```
⚡ 需要立即决策的条目（1 条）：

  1. [Adopt] How we monitor internal coding agents for misalignment
     采纳方案：创建 agent-monitor agent，读取任务 trace，检测意图漂移和规避行为

输入 1 立即执行，s 1 跳过，w 1 降级观察
```

### 构建结果（用户输入 `1`）

同一会话中创建了三个文件：

**`~/.claude/agents/agent-monitor.md`** — 读取已完成任务的 trace 文件，检查四类信号（规避行为、scope 溢出、权限异常、意图漂移），将分级告警写入 `memory/agent-alerts.md`：

| 等级 | 含义 | 协调者行动 |
|------|------|-----------|
| ✅ CLEAN | 正常 | 继续 |
| ⚠️ WATCH | 轻微信号，可能误报 | 记录，追踪趋势 |
| 🚨 ALERT | 高风险信号 | 暂停，通知用户 |
| 🛑 BLOCK | 确认恶意指标 | 停止 + 回滚 |

**`~/.claude/patterns/agent-monitoring.md`** — 协调者指南：哪些任务需要运行后监控，以及如何调用 `agent-monitor`。

**`~/.claude/hooks/post_bash_error.sh`** — 被动监听器，每次 Bash 调用失败时触发，将结构化错误条目写入 `memory/errors.md`，并将高风险模式（非白名单 curl、`rm -rf`、force-push、敏感文件读取）标记到 `memory/agent-alerts.md`。

### 为何重要

从发现到分析缺口、决策、构建的完整循环在一个会话中完成。`news-learner` 识别出平台真实缺失的能力（运行时监控 vs. 静态审查），用户输入 `1` 后新 agent 即刻可用。

这是预期工作流：`/news-digest` 推送值得关注的内容；`news-learner` 将其映射到实际缺口；决策提示让采纳零摩擦。

---

## 开发

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

## 许可证

MIT
