#!/bin/bash
# Tai clip lo 4 L11 (16/11/2026) len lesson-clips, thu lai 4 lan, roi them tieu_de_hop.
# Dung: bash scripts/video-thi-nghiem/tai-lo2-l12.sh <tn-id> [<tn-id> ...]
cd "$(dirname "$0")/../.."
nhan_nhin() {
  case "$1" in
    tn-l11-dien-tro-ohm-01) NHAN="đồ thị U–I của điện trở"; NHIN="Tỉ số U/I qua năm lần đo.";;
    tn-l11-dien-tro-ohm-02) NHAN="đồ thị U–I của bóng đèn"; NHIN="So I ở 3,0 V với I ở 6,0 V.";;
    tn-l11-do-sdd-pin-01) NHAN="đo suất điện động của pin"; NHIN="Số chỉ vôn kế tụt thế nào qua từng nấc biến trở?";;
    tn-l11-nguon-dien-03) NHAN="nối tắt pin tiểu (không tự làm)"; NHIN="So số ampe kế của pin mới và pin đã dùng.";;
    tn-l11-tudien-01) NHAN="tụ nạp rồi phóng qua LED"; NHIN="Đèn LED thay đổi thế nào khi pin vẫn còn nối?";;
    tn-l11-tudien-03) NHAN="tụ phẳng tự chế"; NHIN="Số chỉ C sau mỗi lần đổi so với lần gốc.";;
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
