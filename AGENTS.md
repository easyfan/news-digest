# Agents

## news-learner

**File:** `agents/news-learner.md`
**Model:** sonnet
**Tools:** Bash, Read, Write

深度学习分析 agent。接收 `/news-digest` 检测到的相关条目，盘点平台现有能力，逐条分析并给出与平台的对比、推荐等级和采纳方案。

仅由 `/news-digest` 命令的协调者在检测到相关条目时调用。

### Inputs (from coordinator)

| Field | Description |
|---|---|
| `relevant_items` | JSON array — up to 3 items with `{title, url, source, snippet, metric}` |
| `platform_root` | Path to `~/.claude/` |
| `current_project` | Project slug (e.g. `-workspace`) |
| `scratch` | Output file path for full analysis |

### Output

Structured markdown with per-item analysis:

- **Recommendation levels:** `[Priority Adopt]` / `[Adopt]` / `[Learn]` / `[Skip]`
- **`[Learn]` items** archived to `tech-watch.md` automatically
- **`[Adopt]+` items** trigger an interactive decision prompt in the coordinator
