#!/usr/bin/env bash
# Đưa memory của Claude Code (chỉ có trên Mac) vào git: docs/memory/, rồi symlink ngược lại.
# Chạy MỘT LẦN trên Mac, ở gốc repo:  bash scripts/memory-to-git.sh [--dry-run]
#
# Sau khi chạy:
#   - Claude Code trên Mac vẫn đọc/ghi memory ở đường dẫn cũ (là symlink) → không đổi thói quen.
#   - Nội dung nằm trong repo → `git push` là cloud thấy, `git pull` là Mac thấy.
#   - feedback_*.md, user_*.md KHÔNG bị commit (docs/memory/.gitignore) — giữ riêng ở Mac.
# Script KHÔNG commit, KHÔNG xoá gì: thư mục cũ được đổi tên thành ".bak-<giờ>".
set -euo pipefail

DRY=0
[[ "${1:-}" == "--dry-run" ]] && DRY=1

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DEST="$REPO/docs/memory"
# Tên thư mục project của Claude Code = đường dẫn repo, thay "/" bằng "-"
SLUG="$(echo "$REPO" | sed 's#/#-#g')"
SRC="${MEMORY_SRC:-$HOME/.claude/projects/$SLUG/memory}"
# Repo trên Mac của thầy có thể đã đổi chỗ — cho phép ghi đè: MEMORY_SRC=... bash scripts/memory-to-git.sh
STAMP="$(date +%Y%m%d-%H%M%S)"

run() { if [[ $DRY -eq 1 ]]; then echo "[dry-run] $*"; else eval "$@"; fi; }

echo "Repo       : $REPO"
echo "Memory gốc : $SRC"
echo "Đích (git) : $DEST"
echo

if [[ "$(uname)" != "Darwin" && -z "${MEMORY_SRC:-}" ]]; then
  echo "✗ Không phải macOS. Script này chạy trên Mac của thầy (nơi có memory)." >&2
  echo "  Nếu chắc chắn, đặt MEMORY_SRC=<thư mục memory> rồi chạy lại." >&2
  exit 1
fi

if [[ -L "$SRC" ]]; then
  echo "✓ $SRC đã là symlink → $(readlink "$SRC"). Không cần làm gì."
  exit 0
fi

if [[ ! -d "$SRC" ]]; then
  echo "✗ Không thấy thư mục memory: $SRC" >&2
  echo "  Liệt kê các project có memory:" >&2
  ls -d "$HOME"/.claude/projects/*/memory 2>/dev/null >&2 || true
  echo "  Rồi chạy lại: MEMORY_SRC=<đường dẫn đúng> bash scripts/memory-to-git.sh" >&2
  exit 1
fi

if [[ -e "$DEST" && -n "$(ls -A "$DEST" 2>/dev/null)" ]]; then
  echo "✗ $DEST đã có nội dung. Dừng để khỏi ghi đè — kiểm tra tay rồi xoá nếu muốn làm lại." >&2
  exit 1
fi

n_all=$(find "$SRC" -maxdepth 1 -name '*.md' | wc -l | tr -d ' ')
n_proj=$(find "$SRC" -maxdepth 1 -name 'project_*.md' | wc -l | tr -d ' ')
n_priv=$(find "$SRC" -maxdepth 1 \( -name 'feedback_*.md' -o -name 'user_*.md' \) | wc -l | tr -d ' ')
echo "Tìm thấy $n_all file .md: $n_proj project_*, $n_priv feedback_*/user_* (sẽ không commit)."
echo

# 1. Sao lưu
run "cp -a \"$SRC\" \"$SRC.bak-$STAMP\""
echo "1) Đã sao lưu → $SRC.bak-$STAMP"

# 2. Sao chép vào repo
run "mkdir -p \"$DEST\""
run "cp -a \"$SRC/.\" \"$DEST/\""
echo "2) Đã sao chép vào docs/memory/"

# 3. Chặn commit file riêng tư
if [[ $DRY -eq 0 ]]; then
  cat > "$DEST/.gitignore" <<'EOF'
# Ghi chú cá nhân/phản hồi phong cách — chỉ giữ ở Mac, không lên git
feedback_*.md
user_*.md
EOF
else
  echo "[dry-run] ghi docs/memory/.gitignore (feedback_*.md, user_*.md)"
fi
echo "3) Đã chặn feedback_*/user_* khỏi git"

# 4. Thay thư mục gốc bằng symlink
run "mv \"$SRC\" \"$SRC.old-$STAMP\""
run "ln -s \"$DEST\" \"$SRC\""
echo "4) $SRC → $DEST (symlink)"

# 5. Đưa vào staging (không commit)
run "git -C \"$REPO\" add docs/memory"
echo "5) Đã git add docs/memory"

echo
echo "Xong. Kiểm tra:  git status --short docs/memory  &&  ls -l \"$SRC\""
echo "Rồi commit + push để cloud thấy:"
echo "  git commit -m 'chore(memory): đưa memory project vào git (docs/memory)' && git push"
echo "Khi ổn (vài ngày), xoá bản cũ:  rm -rf \"$SRC.old-$STAMP\" \"$SRC.bak-$STAMP\""
echo "Rollback: rm \"$SRC\" && mv \"$SRC.old-$STAMP\" \"$SRC\""
