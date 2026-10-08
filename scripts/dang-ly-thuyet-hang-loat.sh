#!/usr/bin/env bash
# Đăng lý thuyết cho mọi bài đang ở trạng thái `da-sua` trong content/gemini/hang-doi.md (API đã sửa, lint sạch),
# mỗi bài gọi scripts/cap-nhat-ly-thuyet.sh <thư mục>/theory.html <lesson_id> --yes (chỉ ghi mục Lý thuyết, tự sao lưu),
# xong đổi trạng thái dòng đó thành `da-dang`. Chạy trên Mac, trong tab terminal. Thầy chốt 8/10/2026: không duyệt trước, TA rà trên web.
#   bash scripts/dang-ly-thuyet-hang-loat.sh            # mọi bài da-sua
#   bash scripts/dang-ly-thuyet-hang-loat.sh 3 7 14     # chỉ các lesson_id này (vẫn phải đang da-sua)
set -uo pipefail
cd "$(dirname "$0")/.."
HD=content/gemini/hang-doi.md
ONLY=" $* "
ok=0; loi=0
while IFS='|' read -r _ dir id st rest; do
  dir=$(echo "$dir" | xargs); id=$(echo "$id" | xargs); st=$(echo "$st" | xargs)
  [[ "$st" == "da-sua" && "$id" =~ ^[0-9]+$ ]] || continue
  [[ -z "$*" || "$ONLY" == *" $id "* ]] || continue
  f="content/lesson-samples/$dir/theory.html"
  [[ -f "$f" ]] || { echo "✗ $id: thiếu $f"; loi=$((loi+1)); continue; }
  echo "── $id ($dir) ──"
  if bash scripts/cap-nhat-ly-thuyet.sh "$f" "$id" --yes; then
    python3 - "$HD" "$dir" <<'PY'
import sys,re
p,d=sys.argv[1],sys.argv[2]
L=open(p,encoding='utf8').read().split('\n')
for i,l in enumerate(L):
    c=[x.strip() for x in l.split('|')]
    if len(c)>4 and c[1]==d and c[3]=='da-sua':
        c[3]='da-dang'; c[4]=c[4]+' → đã đăng lý thuyết, chờ TA rà'
        L[i]='| '+' | '.join(c[1:-1])+' |'
open(p,'w',encoding='utf8').write('\n'.join(L))
PY
    ok=$((ok+1))
  else
    echo "✗ $id: đăng lỗi"; loi=$((loi+1))
  fi
done < "$HD"
echo "Xong: $ok bài đã đăng, $loi lỗi. Sao lưu từng bài ở scripts/logs/ly-thuyet-bai<id>-backup-*.json"
