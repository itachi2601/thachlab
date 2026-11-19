#!/bin/bash
# Render clip lo 11 (dot 3, tham so = ten clip). Chay trong tab terminal.
cd "$(dirname "$0")"
printf '%s\n' "$@" | xargs -P 2 -I{} sh -c '/usr/bin/python3 render.py {} > ra/log-{}.txt 2>&1; echo "xong {}"'
ls -la ra/tn-l9-*.mp4 ra/tn-l10-*.mp4 2>/dev/null
