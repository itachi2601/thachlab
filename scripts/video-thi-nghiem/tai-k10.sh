#!/bin/bash
# Tai 4 clip K10 (bo nut A-D) len lesson-clips voi --ban 2, thu lai 4 lan, roi HEAD 200 (19/11/2026). Chay trong tab terminal.
cd "$(dirname "$0")/../.."
for TN in tn-l12-thuchanhtu-04 tn-l12-boylecharles-01 tn-l12-mayphatdien-01 tn-l12-thuchanhtu-03; do
  ok=0
  for k in 1 2 3 4; do
    echo "== $TN lan $k"
    if npx tsx scripts/tai-clip-len-storage.mts "scripts/video-thi-nghiem/ra/$TN.mp4" --tn "$TN" --toi-da 55 --ban 2 --apply; then ok=1; break; fi
    sleep 5
  done
  [ $ok = 1 ] || echo "LOI $TN"
done
for TN in tn-l12-thuchanhtu-04 tn-l12-boylecharles-01 tn-l12-mayphatdien-01 tn-l12-thuchanhtu-03; do
  U=$(/usr/bin/python3 -c "import json,sys;print(json.load(open('content/thi-nghiem/$TN.json'))['video']['mp4'])")
  echo "$TN $(curl -s -o /dev/null -w '%{http_code}' -I "$U") $U"
done
