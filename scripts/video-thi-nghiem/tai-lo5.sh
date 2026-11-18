#!/bin/bash
# Tai clip lo 5 L11 am + L9 quang (18/11/2026) len lesson-clips, thu lai 4 lan, roi them tieu_de_hop.
# Dung: bash scripts/video-thi-nghiem/tai-lo5.sh <tn-id> [<tn-id> ...]
cd "$(dirname "$0")/../.."
nhan_nhin() {
  case "$1" in
    tn-l11-dotansoam-02) NHAN="đếm 10 chu kì trên bản ghi âm thoa"; NHIN="Thời gian 10 chu kì đọc được ở ba đoạn khác nhau.";;
    tn-l11-dotocdoam-03) NHAN="độ trễ giữa hai micro"; NHIN="Độ trễ Δt đổi thế nào khi dời micro 2 ra xa?";;
    tn-l9-kinhlup-01) NHAN="hứng ảnh bóng đèn qua kính lúp 5x"; NHIN="Ảnh trên giấy so với bóng đèn: chiều và cỡ thế nào?";;
    tn-l9-langkinh-03) NHAN="ba tia laser qua lăng kính"; NHIN="So góc lệch D của ba màu ở cùng góc tới.";;
    tn-l9-thaukinh-02) NHAN="hứng ảnh cửa sổ bằng kính lúp"; NHIN="Hình cửa sổ trên giấy so với cửa sổ thật thế nào?";;
    tn-l9-thaukinh-03) NHAN="đo d, d' trên thước quang học"; NHIN="Năm giá trị tính từ d và d' so với nhau thế nào?";;
    tn-l9-tieucu-02) NHAN="đo d, d' ở năm vị trí vật"; NHIN="Màn dịch về phía nào khi vật ra xa thấu kính?";;
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
