#!/bin/bash
# Tai clip lo 2 L12 (14/11/2026) len lesson-clips, thu lai 4 lan, roi them tieu_de_hop.
# Dung: bash scripts/video-thi-nghiem/tai-lo2-l12.sh <tn-id> [<tn-id> ...]
cd "$(dirname "$0")/../.."
nhan_nhin() {
  case "$1" in
    tn-l12-luctu-02) NHAN="dây dẫn giữa hai cực nam châm chữ U"; NHIN="Dây lệch về phía nào khi đảo chiều dòng điện?";;
    tn-l12-luctu-03) NHAN="khung dây trong từ trường"; NHIN="Khung dừng lại ở vị trí nào?";;
    tn-l12-thuchanhtu-02) NHAN="cân dòng điện khi đảo chiều dòng"; NHIN="Số cân đổi thế nào khi đảo chiều dòng?";;
    tn-l12-xoaychieu-01) NHAN="biên độ điện áp theo tốc độ quay"; NHIN="So biên độ trên màn khi quay nhanh hơn.";;
    tn-l12-xoaychieu-02) NHAN="hai đèn LED mắc ngược chiều"; NHIN="Đếm số lần hai đèn đổi lượt trong một giây.";;
    tn-l12-mayphatdien-02) NHAN="ba cuộn dây lệch 120°"; NHIN="Thứ tự và nhịp chớp của ba đèn.";;
    tn-l12-phongxa-01) NHAN="số đếm phóng xạ từng phút"; NHIN="Năm số đếm và số đếm phông nền.";;
    tn-l12-antoanpx-02) NHAN="tấm chắn giấy, nhôm, chì"; NHIN="Số đếm sau mỗi tấm chắn.";;
    tn-l12-antoanpx-04) NHAN="liều kế cá nhân bốn tuần"; NHIN="Cộng bốn tuần rồi suy ra liều năm.";;
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
