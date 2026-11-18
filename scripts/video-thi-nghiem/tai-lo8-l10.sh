#!/bin/bash
# Tai clip lo 8 L10 (18/11/2026) len lesson-clips, thu lai 4 lan, roi them tieu_de_hop.
# Dung: bash scripts/video-thi-nghiem/tai-lo8-l10.sh <tn-id> [<tn-id> ...]
cd "$(dirname "$0")/../.."
nhan_nhin() {
  case "$1" in
    tn-l10-luc-can-luc-nang-02) NHAN="chồng phễu giấy rơi đều"; NHIN="So mũi tên lực cản lên 1 phễu và lên 4 phễu.";;
    tn-l10-luc-can-luc-nang-03) NHAN="lực kế, khối nhôm và bình tràn"; NHIN="So độ giảm số chỉ lực kế với nước tràn ra.";;
    tn-l10-klr-apsuat-03) NHAN="chai nhựa đục ba lỗ"; NHIN="Tia ở mỗi lỗ mạnh thế nào ngay tại miệng lỗ?";;
    tn-l10-moment-luc-01) NHAN="đẩy cửa ở nhiều chỗ, nhiều hướng"; NHIN="Lực cần để cửa quay đổi thế nào qua từng lần?";;
    tn-l10-moment-luc-02) NHAN="thước có trục quay ở giữa"; NHIN="Số chỉ lực kế đổi thế nào khi móc xa trục?";;
    tn-l10-thuchanhthl-01) NHAN="ba lực kế giữ nút dây"; NHIN="So F vẽ được với số chỉ lực kế 3.";;
    tn-l10-biendang-01) NHAN="lò xo bút bi kéo nhẹ rồi kéo mạnh"; NHIN="Lò xo có về chiều dài cũ sau mỗi lần thả?";;
    tn-l10-biendang-02) NHAN="treo quả nặng vào lò xo"; NHIN="Độ dãn đổi thế nào khi thêm quả nặng?";;
  esac
}
for TN in "$@"; do
  nhan_nhin "$TN"; ok=0
  for k in 1 2 3 4; do
    echo "== $TN lan $k"
    if npx tsx scripts/tai-clip-len-storage.mts "scripts/video-thi-nghiem/ra/$TN.mp4" --tn "$TN" --toi-da 55 \
        --nhan "$NHAN" --nhin-vao "$NHIN" --apply; then ok=1; break; fi
    sleep 5
  done
  [ $ok = 1 ] || { echo "LOI $TN"; continue; }
  python3 - "$TN" <<'EOF'
import json, sys, re
p = f"content/thi-nghiem/{sys.argv[1]}.json"; s = open(p, encoding="utf-8").read()
if '"tieu_de_hop"' not in s:
    m = re.search(r'(\n(\s*)"poster": [^\n]*?,?\n)', s)
    line = m.group(1); ind = m.group(2)
    if not line.rstrip().endswith(","): line = line.rstrip("\n") + ",\n"
    s = s.replace(m.group(1), line + f'{ind}"tieu_de_hop": "Xem thí nghiệm dựng lại",\n', 1)
    json.loads(s); open(p, "w", encoding="utf-8").write(s)
v = json.loads(s)["video"]; print("OK", sys.argv[1], v["mp4"], v.get("tieu_de_hop"))
EOF
  url=$(python3 -c "import json;print(json.load(open('content/thi-nghiem/$TN.json'))['video']['mp4'])")
  echo "HEAD $(curl -s -o /dev/null -w '%{http_code}' -I "$url") $url"
done
echo XONG
