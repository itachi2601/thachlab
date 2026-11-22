#!/bin/bash
# Tai clip lo 10 L11 dien + L9 cam ung, dien, nang luong (18/11/2026) len lesson-clips, thu lai 4 lan, roi them tieu_de_hop.
# Dung: bash scripts/video-thi-nghiem/tai-lo10.sh <tn-id> [<tn-id> ...]
cd "$(dirname "$0")/../.."
nhan_nhin() {
  case "$1" in
    tn-l11-coulomb-01) NHAN="thước nhựa cọ tóc đưa lại gần lon nhôm"; NHIN="Lon nhôm đứng yên, lăn lại gần hay lăn ra xa thước?";;
    tn-l11-dien-truong-deu-03) NHAN="tia electron giữa hai bản kim loại"; NHIN="Có hiệu điện thế giữa hai bản, tia cong về phía nào?";;
    tn-l9-camung-01) NHAN="đưa nam châm vào, ra cuộn dây"; NHIN="Kim điện kế lệch lúc nào, về phía nào?";;
    tn-l9-camung-02) NHAN="đóng, giữ, ngắt công tắc nam châm điện"; NHIN="Kim điện kế lệch ở bước nào?";;
    tn-l9-camung-03) NHAN="nam châm quay trước cuộn dây có hai LED"; NHIN="Hai LED sáng thế nào khi nam châm quay?";;
    tn-l9-xoaychieu-01) NHAN="kim nam châm cạnh nam châm điện"; NHIN="Nguồn đổi chiều chậm thì kim làm gì?";;
    tn-l9-xoaychieu-02) NHAN="đèn 6 V với nguồn một chiều và xoay chiều"; NHIN="Vôn kế xoay chiều chỉ bao nhiêu?";;
    tn-l9-modau-01) NHAN="một dòng điện, ba thang đo"; NHIN="Đổi thang thì màn hình hiện gì?";;
    tn-l9-modau-02) NHAN="vôn kế mắc nối tiếp với đèn"; NHIN="Vôn kế mắc sai chỗ chỉ bao nhiêu?";;
    tn-l9-hoathach-01) NHAN="vòng tuần hoàn nước trong bát"; NHIN="Giọt nước dưới màng bọc đến từ đâu?";;
    tn-l9-hoathach-02) NHAN="nến đun lon nước 8 phút"; NHIN="Bao nhiêu phần nhiệt của nến vào nước?";;
    tn-l9-taitao-01) NHAN="tua-bin gió mô hình trước quạt"; NHIN="Gió mạnh hơn thì vôn kế chỉ thế nào?";;
    tn-l9-taitao-02) NHAN="pin mặt trời dưới đèn bàn"; NHIN="Che bớt pin, tắt đèn thì quạt thế nào?";;
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
