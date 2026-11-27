#!/bin/bash
# Tải lô Cổng mới — L11b (25 clip L11 bài 34–45 + tdhphantu-04 L12, dựng lại theo cổng mới 27/11/2026) lên lesson-clips (chỉ Storage, KHÔNG ghi DB).
# Mỗi clip: tải mp4 + ảnh bìa (thử lại 4 lần) → khung video-khung/<tn>.json trỏ URL mới → trả kho <tn>.json về bản cũ
# (kho + bài chỉ đổi khi thầy duyệt, như lô 20). Chạy trong tab terminal, ở worktree có .env.local + node_modules.
# Dùng: bash scripts/video-thi-nghiem/tai-cong-moi-l11b.sh [tn-id ...]   (không đối số = cả lô)
# Dựng lại trong cùng ngày: BAN=2 bash ... <tn-id> (tên <tn>-<ngày>-2, bucket không ghi đè)
cd "$(dirname "$0")/../.."
LO=(tn-l11-coulomb-01 tn-l11-coulomb-02 tn-l11-cuong-do-dong-dien-02 tn-l11-dien-the-01 tn-l11-dien-the-02
  tn-l11-dien-tro-ohm-01 tn-l11-dien-tro-ohm-02 tn-l11-dien-tro-ohm-03 tn-l11-dien-truong-02 tn-l11-dien-truong-deu-01
  tn-l11-dien-truong-deu-02 tn-l11-dien-truong-deu-03 tn-l11-do-sdd-pin-01 tn-l11-do-sdd-pin-02 tn-l11-dotocdoam-01
  tn-l11-dotocdoam-03 tn-l11-nang-luong-dien-02 tn-l11-nang-luong-dien-03 tn-l11-nguon-dien-01 tn-l11-nguon-dien-02
  tn-l11-nguon-dien-03 tn-l11-the-nang-dien-01 tn-l11-tudien-01 tn-l11-tudien-02 tn-l11-tudien-03 tn-l12-tdhphantu-04)
[ $# -gt 0 ] && LO=(tn-l11-coulomb-01 tn-l11-coulomb-02 tn-l11-cuong-do-dong-dien-02 tn-l11-dien-the-01 tn-l11-dien-the-02
  tn-l11-dien-tro-ohm-01 tn-l11-dien-tro-ohm-02 tn-l11-dien-tro-ohm-03 tn-l11-dien-truong-02 tn-l11-dien-truong-deu-01
  tn-l11-dien-truong-deu-02 tn-l11-dien-truong-deu-03 tn-l11-do-sdd-pin-01 tn-l11-do-sdd-pin-02 tn-l11-dotocdoam-01
  tn-l11-dotocdoam-03 tn-l11-nang-luong-dien-02 tn-l11-nang-luong-dien-03 tn-l11-nguon-dien-01 tn-l11-nguon-dien-02
  tn-l11-nguon-dien-03 tn-l11-the-nang-dien-01 tn-l11-tudien-01 tn-l11-tudien-02 tn-l11-tudien-03 tn-l12-tdhphantu-04)
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
for TN in "${LO[@]}"; do u=$(python3 -c "import json;print(json.load(open('content/thi-nghiem/video-khung/$TN.json'))['video'])"); echo "HEAD $(curl -s -o /dev/null -w '%{http_code}' -I "$u") $(curl -s -o /dev/null -w '%{http_code}' -I "${u%.mp4}.webp") $u"; done
echo "XONG. Lỗi: ${#LOI[@]} ${LOI[*]}"
