#!/bin/bash
# Tải lô 32 clip L12 dựng lại theo cổng mới (Việc 4, 26–27/11/2026) lên lesson-clips (chỉ Storage, KHÔNG ghi DB).
# Mỗi clip: tải mp4 + ảnh bìa (thử lại 4 lần) → khung video-khung/<tn>.json trỏ URL mới → trả kho <tn>.json về bản cũ
# (kho + bài chỉ đổi khi thầy duyệt, như lô 20). Chạy trong tab terminal, ở worktree có .env.local + node_modules.
# Dùng: bash scripts/video-thi-nghiem/tai-lo32.sh [tn-id ...]   (không đối số = cả lô)
cd "$(dirname "$0")/../.."
LO=(tn-l12-apsuatdongnang-01 tn-l12-boylecharles-03 tn-l12-chuyenthe-03 tn-l12-noinang-01 tn-l12-noinang-02
  tn-l12-tdhphantu-01 tn-l12-thangnhietdo-02 tn-l12-thangnhietdo-03 tn-l12-thangnhietdo-04 tn-l12-thuchanh-03
  tn-l12-luctu-02 tn-l12-luctu-03 tn-l12-thuchanhtu-02 tn-l12-tutruong-02 tn-l12-tutruong-04 tn-l12-camungdt-01
  tn-l12-mayphatdien-02 tn-l12-udcamung-01 tn-l12-udcamung-02 tn-l12-udcamung-03 tn-l12-xoaychieu-01
  tn-l12-xoaychieu-03 tn-l12-dttruong-01 tn-l12-dttruong-02 tn-l12-dttruong-05 tn-l12-hatnhan-01
  tn-l12-hatnhan-02 tn-l12-nllk-01 tn-l12-phanbach-02 tn-l12-phongxa-01 tn-l12-antoanpx-02 tn-l12-antoanpx-04)
[ $# -gt 0 ] && LO=("$@")
LOI=()
for TN in "${LO[@]}"; do
  MP4="scripts/video-thi-nghiem/ra/$TN.mp4"
  [ -f "$MP4" ] || { echo "LOI $TN: thiếu $MP4"; LOI+=("$TN"); continue; }
  ok=0
  for k in 1 2 3 4; do
    echo "== $TN lần $k"
    if npx tsx scripts/tai-clip-len-storage.mts "$MP4" --tn "$TN" --toi-da 55 --apply; then ok=1; break; fi
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
