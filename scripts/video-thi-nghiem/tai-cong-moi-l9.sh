#!/bin/bash
# Tải 36 clip L9 dựng lại theo cổng mới (Việc 4, "Cổng mới — L9", 27/11/2026) lên lesson-clips (chỉ Storage, KHÔNG ghi DB).
# Mỗi clip: tải mp4 + ảnh bìa (thử lại 4 lần) → khung video-khung/<tn>.json trỏ URL mới → trả kho <tn>.json về bản cũ
# (kho + bài chỉ đổi khi thầy duyệt, như lô 20). Chạy trong tab terminal, ở worktree có .env.local + node_modules.
# Dùng: bash scripts/video-thi-nghiem/tai-cong-moi-l9.sh [tn-id ...]   (không đối số = cả lô)
# Dựng lại trong cùng ngày: BAN=2 bash ... <tn-id> (tên <tn>-<ngày>-2, bucket không ghi đè)
cd "$(dirname "$0")/../.."
LO=(tn-l9-ohm-01 tn-l9-ohm-02 tn-l9-ohm-03 tn-l9-doanmach-01 tn-l9-doanmach-02 tn-l9-doanmach-03 tn-l9-congsuat-01
  tn-l9-congsuat-03 tn-l9-dongthe-01 tn-l9-dongthe-02 tn-l9-dongthe-03 tn-l9-camung-01 tn-l9-camung-02 tn-l9-camung-03
  tn-l9-xoaychieu-01 tn-l9-xoaychieu-02 tn-l9-hoathach-01 tn-l9-hoathach-02 tn-l9-conang-01 tn-l9-conang-02 tn-l9-conang-03
  tn-l9-congco-01 tn-l9-modau-01 tn-l9-modau-02 tn-l9-hsgamthanh-01 tn-l9-hsgamthanh-02 tn-l9-taitao-01 tn-l9-taitao-02
  tn-l9-kinhlup-01 tn-l9-langkinh-01 tn-l9-langkinh-03 tn-l9-pxtp-01 tn-l9-thaukinh-02 tn-l9-thaukinh-03 tn-l9-tieucu-02
  tn-l9-tieucu-03)
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
