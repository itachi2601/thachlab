#!/bin/bash
# Tai clip lo 9 L10 (18/11/2026) len lesson-clips, thu lai 4 lan, roi them tieu_de_hop.
# Dung: bash scripts/video-thi-nghiem/tai-lo9-l10.sh <tn-id> [<tn-id> ...]
cd "$(dirname "$0")/../.."
nhan_nhin() {
  case "$1" in
    tn-l10-co-nang-bao-toan-02) NHAN="bóng bàn nảy trên mặt bàn"; NHIN="Đọc độ cao đỉnh mỗi lần nảy trên thước.";;
    tn-l10-nang-luong-cong-01) NHAN="bóng tennis nảy trên sàn"; NHIN="Cột năng lượng nào đổi lúc bóng chạm sàn?";;
    tn-l10-dong-nang-the-nang-02) NHAN="con lắc vướng đinh"; NHIN="Quả nặng lên tới vạch nào ở bên kia?";;
    tn-l10-hieu-suat-02) NHAN="kéo xe lên ván nghiêng bốn góc"; NHIN="So công toàn phần với công có ích ở từng góc.";;
    tn-l10-nang-luong-cong-02) NHAN="kéo xe lên máng dài ngắn khác nhau"; NHIN="Số lực kế và tích F·s ở từng máng.";;
    tn-l10-baotoandl-01) NHAN="va chạm mềm trên đệm khí"; NHIN="Thời gian qua cổng quang trước và sau va chạm.";;
    tn-l10-baotoandl-02) NHAN="hai xe va chạm trên đệm khí"; NHIN="Mỗi xe làm gì ngay sau va chạm?";;
    tn-l10-thuchanhdl-01) NHAN="đo động lượng trước và sau va chạm"; NHIN="Thời gian xe qua cổng quang trước và sau va chạm.";;
    tn-l10-thuchanhdl-02) NHAN="hai xe đẩy nhau bằng lò xo"; NHIN="Chiều đi và thời gian qua cổng của mỗi xe.";;
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
