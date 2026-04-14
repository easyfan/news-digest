#!/usr/bin/env python3
# detect_project_profile.py — 检测当前项目 profile 并写入 /tmp/nd_profile.json
# 用法：python3 detect_project_profile.py <project_root>
# 退出码：0=成功，1=失败
import json, os, sys
_S = os.environ.get('ND_SESSION', '')
def _p(n): return f'/tmp/nd_{_S}_{n}' if _S else f'/tmp/nd_{n}'

project_root = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
project_name = os.path.basename(project_root.rstrip('/'))

BUILTIN_PROFILES = {
    "thinking_of_memory": {
        "display": "thinking_of_memory",
        "focus": "学术论文、数据分析方法、统计建模、机器学习研究",
        "extra_keywords": [
            "data analysis", "statistical", "statistics", "methodology", "empirical",
            "experiment", "dataset", "benchmark", "evaluation metric", "ablation",
            "regression", "classification", "clustering", "time series", "causal",
            "bayesian", "neural network", "transformer", "attention", "loss function",
            "gradient", "training", "inference", "performance", "accuracy", "recall",
            "precision", "f1", "auc", "roc", "cross-validation", "hyperparameter",
            "memory", "retrieval", "knowledge graph", "embedding", "vector store",
            "paper", "arxiv", "preprint", "survey", "review"
        ],
        "preferred_sources": ["arxiv", "hf", "reddit"],
        "learner_instruction": "重点分析该条目的数据分析方法、实验设计、评估指标，以及对现有 memory/retrieval 系统设计的启发。"
    },
    "cc_manager": {
        "display": "cc-manager",
        "focus": "Claude Code harness、agent 编排、多智能体设计、MCP、工具调用",
        "extra_keywords": [
            "claude code", "harness", "agent orchestration", "multi-agent", "subagent",
            "mcp", "model context protocol", "tool use", "tool calling", "function calling",
            "agent design", "agent pattern", "agentic", "workflow automation",
            "prompt engineering", "context window", "system prompt", "claude",
            "anthropic", "hook", "plugin", "skill", "command", "slash command",
            "orchestrator", "coordinator", "supervisor", "swarm", "a2a",
            "agent-to-agent", "handoff", "delegation", "task routing",
            "code generation", "coding agent", "swe-agent", "devin", "opencode",
            "llm ops", "ai infrastructure", "inference", "latency", "token"
        ],
        "preferred_sources": ["anthropic", "hn", "github", "langchain", "clawhub"],
        "learner_instruction": "重点分析该条目对 Claude Code harness 设计、agent 编排模式、skill/plugin 架构的借鉴价值，给出具体采纳方案。"
    }
}

def normalize(s):
    return s.lower().replace('-', '_')

matched_key = None
for key in BUILTIN_PROFILES:
    if normalize(project_name) == normalize(key):
        matched_key = key
        break

user_cfg_path = os.path.expanduser('~/.claude/news-digest-profiles.json')
user_profiles = {}
if os.path.exists(user_cfg_path):
    try:
        user_profiles = json.load(open(user_cfg_path))
        print(f'[profile] 已加载用户配置：{user_cfg_path}')
    except Exception as e:
        print(f'[profile] 用户配置解析失败，使用内置配置：{e}')

all_profiles = {**BUILTIN_PROFILES, **user_profiles}

if matched_key and matched_key in all_profiles:
    profile = all_profiles[matched_key]
    print(f'[profile] 检测到项目 "{project_name}"，启用 profile: {profile["display"]} — 关注方向：{profile["focus"]}')
elif project_name in user_profiles:
    matched_key = project_name
    profile = user_profiles[project_name]
    print(f'[profile] 用户自定义 profile: {profile["display"]} — 关注方向：{profile["focus"]}')
else:
    profile = {"display": "default", "focus": "通用 AI 技术", "extra_keywords": [], "preferred_sources": [], "learner_instruction": ""}
    print(f'[profile] 未匹配项目 profile，使用默认模式（项目名：{project_name}）')
    print(f'[profile] 如需自定义，创建 ~/.claude/news-digest-profiles.json，参考内置格式添加项目配置。')

json.dump(profile, open(_p('profile.json'), 'w'))
