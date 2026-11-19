#!/bin/bash
# Render clip lo 11 (dot 2). Chay trong tab terminal.
cd "$(dirname "$0")"
printf '%s\n' baitapsong4 dotocdoam1 dientruongdeu1 | xargs -P 2 -I{} sh -c '/usr/bin/python3 render.py {} > ra/log-{}.txt 2>&1; echo "xong {}"'
ls -la ra/tn-l11-*.mp4 2>/dev/null
