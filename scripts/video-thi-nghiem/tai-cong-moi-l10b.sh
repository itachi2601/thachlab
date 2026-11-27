#!/bin/bash
# Tải 38 clip L10 bài 63–79 dựng lại theo cổng mới (phiên L10b, 27/11/2026) lên lesson-clips (chỉ Storage, KHÔNG ghi DB).
# Mỗi clip: tải mp4 + ảnh bìa (thử lại 4 lần) → khung video-khung/<tn>.json trỏ URL mới → trả kho <tn>.json về bản cũ
# (kho + bài chỉ đổi khi thầy duyệt, như lô 32). Chạy trong tab terminal, ở worktree có .env.local + node_modules.
# Dùng: bash scripts/video-thi-nghiem/tai-cong-moi-l10b.sh [tn-id ...]   (không đối số = cả lô)
# Dựng lại trong cùng ngày: BAN=2 bash ... <tn-id> (tên <tn>-<ngày>-2, bucket không ghi đè)
cd "$(dirname "$0")/../.."
LO=(
  tn-l10-baotoandl-01 tn-l10-baotoandl-02 tn-l10-biendang-01 tn-l10-biendang-02 tn-l10-biendang-03 
  tn-l10-co-nang-bao-toan-01 tn-l10-co-nang-bao-toan-02 tn-l10-cong-suat-01 tn-l10-dong-nang-the-nang-01 
  tn-l10-dong-nang-the-nang-02 tn-l10-dongluong-01 tn-l10-dongluong-02 tn-l10-giaibt-dlh-01 
  tn-l10-giaibt-dlh-02 tn-l10-hieu-suat-01 tn-l10-hieu-suat-02 tn-l10-huongtam-02 tn-l10-huongtam-03 
  tn-l10-huongtam-04 tn-l10-klr-apsuat-01 tn-l10-klr-apsuat-02 tn-l10-klr-apsuat-03 tn-l10-luc-can-luc-nang-02 
  tn-l10-luc-can-luc-nang-03 tn-l10-luc-ma-sat-01 tn-l10-luc-ma-sat-02 tn-l10-luc-ma-sat-03 
  tn-l10-moment-luc-01 tn-l10-moment-luc-02 tn-l10-moment-luc-03 tn-l10-nang-luong-cong-01 
  tn-l10-nang-luong-cong-02 tn-l10-thuchanhdl-01 tn-l10-thuchanhdl-02 tn-l10-thuchanhdl-03 
  tn-l10-thuchanhthl-01 tn-l10-trondeu-02 tn-l10-trondeu-03)
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
