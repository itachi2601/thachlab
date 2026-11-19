#!/bin/bash
# Render clip lo 11 (dot 1). Chay trong tab terminal.
cd "$(dirname "$0")"
printf '%s\n' songdung1 songngangdoc2 giaothoa3 | xargs -P 2 -I{} sh -c '/usr/bin/python3 render.py {} > ra/log-{}.txt 2>&1; echo "xong {}"'
ls -la ra/songdung1*.mp4 ra/*songngangdoc*.mp4 ra/*giaothoa*.mp4 2>/dev/null
