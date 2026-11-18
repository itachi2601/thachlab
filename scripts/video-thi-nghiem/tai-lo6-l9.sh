#!/bin/bash
# Tai clip lo 6 L9 (18/11/2026) len lesson-clips, thu lai 4 lan, roi them tieu_de_hop.
# Dung: bash scripts/video-thi-nghiem/tai-lo6-l9.sh <tn-id> [<tn-id> ...]
cd "$(dirname "$0")/../.."
nhan_nhin() {
  case "$1" in
    tn-l9-doanmach-01) NHAN="ampe kế và vôn kế trong mạch nối tiếp"; NHIN="So số ampe kế khi đổi chỗ, và số vôn kế ở từng đoạn.";;
    tn-l9-doanmach-02) NHAN="ba ampe kế trong mạch song song"; NHIN="So số ampe kế mạch chính với hai số ở hai nhánh.";;
    tn-l9-ohm-02) NHAN="đồ thị I theo U của dây constantan"; NHIN="Bốn điểm (U; I) nằm thế nào trên đồ thị?";;
    tn-l9-ohm-03) NHAN="điện trở của bốn đoạn dây"; NHIN="Số ampe kế đổi thế nào khi đổi dây?";;
    tn-l9-conang-02) NHAN="con lắc vướng đinh"; NHIN="Bên kia đinh, vật lên tới đâu so với vạch ngang?";;
    tn-l9-conang-03) NHAN="bóng cao su nảy cạnh thước"; NHIN="Độ cao mỗi lần nảy so với lần trước.";;
    tn-l9-dongthe-03) NHAN="quả nặng rơi xuống khay cát"; NHIN="So độ sâu vết lõm của từng lần thả.";;
    tn-l9-hsgamthanh-02) NHAN="tiếng vang trước bức tường"; NHIN="Thời gian giữa tiếng vỗ và tiếng vang ở mỗi khoảng cách.";;
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
