#!/bin/bash
# Cổng mới L10b: render mp4 nhóm A (8 clip đã qua cổng B) rồi tải lên Storage (tai-cong-moi-l10b.sh).
cd "$(dirname "$0")"
PY=~/.venvs/video-thi-nghiem/bin/python
for c in baotoandl1 baotoandl2 thuchanhdl1 thuchanhdl2 thuchanhdl3 dongluong1 dongluong2 congsuat1; do
  echo "== render $c $(date +%H:%M:%S)"; $PY render.py $c > /dev/null 2>ra/render-$c.err || echo "LOI render $c"
done
ls -la ra/tn-l10-{baotoandl-0[12],thuchanhdl-0[123],dongluong-0[12],cong-suat-01}.mp4
bash tai-cong-moi-l10b.sh tn-l10-baotoandl-01 tn-l10-baotoandl-02 tn-l10-thuchanhdl-01 tn-l10-thuchanhdl-02 tn-l10-thuchanhdl-03 tn-l10-dongluong-01 tn-l10-dongluong-02 tn-l10-cong-suat-01
