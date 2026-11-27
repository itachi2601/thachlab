#!/bin/bash
# Cổng mới L10b: render mp4 các clip đã qua cổng B rồi tải lên Storage. Đối số: <tên clip>:<tn-id> ...
#   bash scripts/video-thi-nghiem/render-l10b.sh conang1:tn-l10-co-nang-bao-toan-01 ...
cd "$(dirname "$0")"
PY=~/.venvs/video-thi-nghiem/bin/python; TN=()
for p in "$@"; do c=${p%%:*}; TN+=("${p##*:}")
  echo "== render $c $(date +%H:%M:%S)"; $PY render.py $c > /dev/null 2>ra/render-$c.err || echo "LOI render $c"
done
bash tai-cong-moi-l10b.sh "${TN[@]}"
