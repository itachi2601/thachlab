#!/bin/bash
# Tai clip lo 11 (19/11/2026) len lesson-clips, thu lai 4 lan, roi them tieu_de_hop.
# Dung: bash scripts/video-thi-nghiem/tai-lo11.sh <tn-id> [<tn-id> ...]
cd "$(dirname "$0")/../.."
nhan_nhin() {
  case "$1" in
    tn-l11-songdung-01) NHAN="dây thun rung bằng tay"; NHIN="Vung nhanh hơn thì số múi dây thế nào?";;
    tn-l11-songngangdoc-02) NHAN="sóng dọc trên lò xo slinky"; NHIN="Tần số tăng thì khoảng cách hai vùng nén thế nào?";;
    tn-l11-giaothoa-03) NHAN="laser qua khe Young"; NHIN="Đặt màn xa hơn thì khoảng vân thế nào?";;
    tn-l11-baitapsong-04) NHAN="ống bịt một đầu, nối thêm ống"; NHIN="Ống dài gấp đôi thì tần số cộng hưởng thế nào?";;
    tn-l11-dotocdoam-01) NHAN="ống cộng hưởng có nước, âm thoa"; NHIN="Hạ mực nước, âm to lần thứ hai ở đâu?";;
    tn-l11-dien-truong-deu-01) NHAN="bột trong dầu giữa hai lá đồng nhiễm điện"; NHIN="Hai lá lại gần thì điện trường giữa chúng thế nào?";;
    tn-l9-khucxa-02) NHAN="tia sáng từ không khí vào khối nhựa"; NHIN="Tăng góc tới thì góc khúc xạ đổi thế nào?";;
    tn-l9-pxtp-01) NHAN="tia sáng từ khối nhựa ra không khí"; NHIN="Tăng góc tới, khi nào tia khúc xạ biến mất?";;
    tn-l9-langkinh-01) NHAN="tia sáng qua lăng kính"; NHIN="Tăng góc tới thì góc lệch đổi thế nào?";;
    tn-l10-nemngang-01) NHAN="bi ném ngang và bi thả cùng lúc"; NHIN="Hai bi chạm đất cùng lúc hay lệch nhau?";;
    tn-l9-doanmach-03) NHAN="tháo một bóng ở mạch nối tiếp và song song"; NHIN="Tháo một bóng thì bóng còn lại sáng thế nào?";;
    tn-l9-hsgamthanh-01) NHAN="thước nhô ra mép bàn gảy"; NHIN="Thước nhô ra ngắn hay dài thì âm cao hơn?";;
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
