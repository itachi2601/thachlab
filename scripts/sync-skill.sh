#!/usr/bin/env bash
# Đồng bộ skill trong repo sang 2 bản còn lại (chạy trên Mac): Library plugin + ~/.codex.
#   bash scripts/sync-skill.sh [tên-skill ...]     (mặc định: soan-quiz-ly-thuyet)
# Lưu ý: scripts/ của skill import features/ từ gốc repo → chỉ chạy được trong repo; hai bản sao dùng để đọc SKILL.md/references.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PLUGIN="$HOME/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin/f7f31a21-6c52-49d5-a50c-771407734c02/46c5a460-bf4a-4f61-be39-e82de406e5ad/skills"
CODEX="$HOME/.codex/skills"
SKILLS=("${@:-soan-quiz-ly-thuyet}")
for s in "${SKILLS[@]}"; do
  src="$ROOT/.claude/skills/$s/"
  [ -d "$src" ] || { echo "Không thấy $src"; exit 1; }
  for dst in "$PLUGIN" "$CODEX"; do
    mkdir -p "$dst/$s"
    rsync -a --delete "$src" "$dst/$s/"
    echo "✓ $s → $dst/$s"
  done
done
