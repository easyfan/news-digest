#!/usr/bin/env bash
# scan_platform.sh — 扫描平台 commands/agents/patterns 的 description 字段
# 用法：bash scan_platform.sh <platform_root>
# 退出码：0=成功（各目录不存在时静默跳过）
set -euo pipefail

PLATFORM_ROOT="${1:?usage: scan_platform.sh <platform_root>}"

scan_dir() {
    local label="$1" dir="$2"
    echo "=== ${label} ==="
    if [ ! -d "$dir" ]; then return; fi
    for f in "$dir"/*.md; do
        [ -f "$f" ] || continue
        name=$(basename "$f" .md)
        desc=$(grep "^description:" "$f" 2>/dev/null | head -1 | sed 's/^description:[[:space:]]*//')
        if [ -n "$desc" ]; then
            echo "$name: $desc"
        else
            echo "$name: [无 description]"
        fi
    done
}

scan_dir "commands" "$PLATFORM_ROOT/commands"
scan_dir "agents"   "$PLATFORM_ROOT/agents"
scan_dir "patterns" "$PLATFORM_ROOT/patterns"
