#!/bin/bash
# Tải 21 clip L11 bài 20–33 (Dao động + Sóng) dựng lại theo cổng mới (phiên L11a, 27/11/2026) lên lesson-clips (chỉ Storage, KHÔNG ghi DB).
# Mỗi clip: tải mp4 + ảnh bìa (thử lại 4 lần) → khung video-khung/<tn>.json trỏ URL mới → trả kho <tn>.json về bản cũ
# (kho + bài chỉ đổi khi thầy duyệt, như lô 20). Chạy trong tab terminal, ở worktree có .env.local + node_modules.
# Dùng: bash scripts/video-thi-nghiem/tai-cong-moi-l11a.sh [tn-id ...]   (không đối số = cả lô)
# Dựng lại trong cùng ngày: BAN=2 bash ... <tn-id> (tên <tn>-<ngày>-2, bucket không ghi đè)
cd "$(dirname "$0")/../.."
LO=(tn-l11-baitapdaodong-01 tn-l11-baitapdaodong-02 tn-l11-baitapdaodong-03 tn-l11-baitapnangluong-01
  tn-l11-baitapnangluong-02 tn-l11-baitapsong-04 tn-l11-conangdddh-01 tn-l11-conangdddh-02 tn-l11-daodongdieuhoa-01
  tn-l11-daodongdieuhoa-03 tn-l11-dotansoam-02 tn-l11-giaothoa-03 tn-l11-motadddh-01 tn-l11-motadddh-02 tn-l11-songdung-01
  tn-l11-songngangdoc-02 tn-l11-tatdan-01 tn-l11-tatdan-02 tn-l11-tatdan-03 tn-l11-vantocdddh-01 tn-l11-vantocdddh-02)
[ $# -gt 0 ] && LO=("$@")
LOI=()
for TN in "${LO[@]}"; do
  MP4="scripts/video-thi-nghiem/ra/$TN.mp4"
  [ -f "$MP4" ] || { echo "LOI $TN: thiếu $MP4"; LOI+=("$TN"); continue; }
  ok=0
  for k in 1 2 3 4; do
    echo "== $TN lần $k"
    if npx tsx scripts/tai-clip-len-storage.mts "$MP4" --tn "$TN" --toi-da 55 ${BAN:+--ban $BAN} --apply; then ok=1; break; fi
    sleep 5
  done
  [ $ok = 1 ] || { echo "LOI $TN"; LOI+=("$TN"); continue; }
  python3 - "$TN" <<'EOF'
import json, sys
tn = sys.argv[1]
mp4 = json.load(open(f"content/thi-nghiem/{tn}.json", encoding="utf-8"))["video"]["mp4"]
p = f"content/thi-nghiem/video-khung/{tn}.json"
s = open(p, encoding="utf-8").read(); cu = json.loads(s)["video"]
s = s.replace(json.dumps(cu), json.dumps(mp4), 1); assert json.loads(s)["video"] == mp4
open(p, "w", encoding="utf-8").write(s)
print(f"khung → {mp4}")
EOF
  git checkout -- "content/thi-nghiem/$TN.json"
done
echo "XONG. Lỗi: ${#LOI[@]} ${LOI[*]}"
