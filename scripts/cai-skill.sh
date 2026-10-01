#!/usr/bin/env bash
# Cài skill của repo về máy Mac: symlink .claude/skills/* -> ~/.claude/skills và ~/.codex/skills.
# Repo là nguồn duy nhất; pull xong là mọi nơi thấy bản mới. Không ghi đè thư mục thật đã có.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
for dest in "$HOME/.claude/skills" "$HOME/.codex/skills"; do
  mkdir -p "$dest"
  for src in "$ROOT"/.claude/skills/*/; do
    name="$(basename "$src")"; link="$dest/$name"
    if [ -L "$link" ]; then ln -sfn "${src%/}" "$link"; echo "cập nhật  $link"
    elif [ -e "$link" ]; then echo "BỎ QUA   $link đã là thư mục thật — diff rồi xoá tay nếu muốn thay bằng symlink"
    else ln -s "${src%/}" "$link"; echo "đã cài    $link"; fi
  done
done
