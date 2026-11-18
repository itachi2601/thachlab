#!/bin/bash
# Tai clip lo 7 L10 (18/11/2026) len lesson-clips, thu lai 4 lan, roi them tieu_de_hop.
# Dung: bash scripts/video-thi-nghiem/tai-lo7-l10.sh <tn-id> [<tn-id> ...]
cd "$(dirname "$0")/../.."
nhan_nhin() {
  case "$1" in
    tn-l10-dl1-newton-01) NHAN="hai máng nghiêng"; NHIN="Quãng bi lăn trên máng (2) qua ba lần hạ máng.";;
    tn-l10-dl2-newton-01) NHAN="xe kéo bằng quả nặng, khối lượng giữ nguyên"; NHIN="Các điểm (F, a) xếp thành hình gì?";;
    tn-l10-dl2-newton-02) NHAN="xe chất thêm gia trọng, lực kéo giữ nguyên"; NHIN="Gia tốc đổi thế nào khi xe nặng dần?";;
    tn-l10-newton3-01) NHAN="hai lực kế móc vào nhau"; NHIN="So số chỉ hai lực kế ở mỗi lần kéo.";;
    tn-l10-trong-luc-luc-cang-01) NHAN="dây dọi và tấm bìa treo"; NHIN="Các đường kẻ theo dây dọi gặp nhau ở đâu?";;
    tn-l10-luc-ma-sat-01) NHAN="kéo hộp gỗ bằng lực kế"; NHIN="Số chỉ lực kế ngay lúc hộp bắt đầu trượt.";;
    tn-l10-luc-ma-sat-02) NHAN="đổi mặt tiếp xúc, tốc độ, cho lăn"; NHIN="So số lực kế giữa các lần kéo.";;
    tn-l10-luc-ma-sat-03) NHAN="nâng dần tấm ván"; NHIN="Độ cao h lúc hộp bắt đầu trượt và lúc trượt đều.";;
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
