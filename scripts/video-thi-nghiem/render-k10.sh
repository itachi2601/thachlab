#!/bin/bash
# Dung lai 4 clip K10 (bo nut A-D trong mp4) + thuchanhtu4 ban 3 (19/11/2026). Chay trong tab terminal.
cd "$(dirname "$0")"
printf '%s\n' thuchanhtu4 boyle mayphat1 thuchanhtu3 | xargs -P 2 -I{} sh -c '/usr/bin/python3 render.py {} > ra/log-{}.txt 2>&1; echo "xong {}"'
ls -la ra/*.mp4
