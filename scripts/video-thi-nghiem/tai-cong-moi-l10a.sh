#!/bin/bash
# Tải 29 clip L10 bài 46–62 dựng lại theo cổng mới (phiên L10a, 27/11/2026) lên lesson-clips (chỉ Storage, KHÔNG ghi DB).
# Mỗi clip: tải mp4 + ảnh bìa (thử lại 4 lần) → khung video-khung/<tn>.json trỏ URL mới → trả kho <tn>.json về bản cũ
# (kho + bài chỉ đổi khi thầy duyệt, như lô 20). Chạy trong tab terminal, ở worktree có .env.local + node_modules.
# Dùng: bash scripts/video-thi-nghiem/tai-cong-moi-l10a.sh [tn-id ...]   (không đối số = cả lô)
# Dựng lại trong cùng ngày: BAN=2 bash ... <tn-id> (tên <tn>-<ngày>-2, bucket không ghi đè)
cd "$(dirname "$0")/../.."
LO=(tn-l10-lam-quen-02 tn-l10-an-toan-01 tn-l10-an-toan-02 tn-l10-sai-so-01 tn-l10-sai-so-02 tn-l10-dd-qd-01
  tn-l10-tdvt-01 tn-l10-tdvt-03 tn-l10-do-toc-do-01 tn-l10-do-toc-do-02 tn-l10-dt-dctg-01 tn-l10-dt-dctg-02
  tn-l10-gia-toc-01 tn-l10-gia-toc-02 tn-l10-ctbdd-01 tn-l10-do-g-01 tn-l10-do-g-02 tn-l10-do-g-03
  tn-l10-roi-tu-do-02 tn-l10-roi-tu-do-03 tn-l10-nemngang-02 tn-l10-tonghopluc-02 tn-l10-dl1-newton-01
  tn-l10-dl2-newton-01 tn-l10-dl2-newton-02 tn-l10-newton3-01 tn-l10-trong-luc-luc-cang-01
  tn-l10-trong-luc-luc-cang-02 tn-l10-trong-luc-luc-cang-03)
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
