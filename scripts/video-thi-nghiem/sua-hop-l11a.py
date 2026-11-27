#!/usr/bin/env python3
"""Cổng mới L11a (27/11/2026, thầy duyệt "sửa cả hộp"): giấu số đọc/kết luận trong hộp exp đứng TRƯỚC video
vào <details> "(xem sau video)" — mẫu có sẵn ở l11-thuc-hanh-do-tan-so-am. Ghi cả theory.src.html, theory.html, bundle.json.
Dùng: python3 scripts/video-thi-nghiem/sua-hop-l11a.py [--apply]"""
import json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
D = '<details class="tl-details"><summary>{}</summary>{}</details>'
S = [
 ("l11-tat-dan-cuong-buc",
  '<li><strong>Quan sát:</strong> $A$ lớn nhất ở $2{,}0$ Hz. $1{,}5$ Hz và $2{,}5$ Hz cùng số đọc.</li>\n<li><strong>Rút ra:</strong> đỉnh tại $f = f_0$.</li>',
  '<li><strong>Quan sát:</strong> ghi $A$ ở mỗi tần số (xem video bên dưới).' + D.format('Số đọc (xem sau video)', '$A$ lớn nhất ở $2{,}0$ Hz. $1{,}5$ Hz và $2{,}5$ Hz cùng số đọc.') + '</li>\n<li><strong>Rút ra:</strong> ' + D.format('Kết luận (xem sau video)', 'đỉnh tại $f = f_0$.') + '</li>'),
 ("l11-tat-dan-cuong-buc",
  '<li><strong>Quan sát:</strong> sau 2 s, không khí còn rõ, nước yếu, dầu gần hết.</li>\n<li><strong>Rút ra:</strong> càng nhớt, biên độ tụt càng nhanh.</li>',
  '<li><strong>Quan sát:</strong> sau 2 s, so đỉnh còn lại ở ba chỗ (xem video bên dưới).' + D.format('Kết quả (xem sau video)', 'không khí còn rõ, nước yếu, dầu gần hết.') + '</li>\n<li><strong>Rút ra:</strong> ' + D.format('Kết luận (xem sau video)', 'càng nhớt, biên độ tụt càng nhanh.') + '</li>'),
 ("l11-bai-tap-nang-luong-dao-dong",
  '<li><strong>Quan sát:</strong> bảng dưới (số minh hoạ',
  '<li><strong>Quan sát:</strong> xem video bên dưới, rồi mở bảng cuối hộp (số minh hoạ'),
 ("l11-bai-tap-nang-luong-dao-dong",
  '<li><strong>Rút ra:</strong> tỉ số $W/A^2$',
  '<li><strong>Rút ra:</strong> <details class="tl-details"><summary>Kết luận (xem sau video)</summary>tỉ số $W/A^2$'),
 ("l11-bai-tap-nang-luong-dao-dong",
  'số đo thấp hơn chừng 2–7%.</li>\n</ol>\n<table class="tl-table">\n<thead><tr><th>$A$ (cm)</th><th>$v_{\\max}$ đo (cm/s)</th>',
  'số đo thấp hơn chừng 2–7%.</details></li>\n</ol>\n<details class="tl-details"><summary>Bảng số (xem sau video)</summary>\n<table class="tl-table">\n<thead><tr><th>$A$ (cm)</th><th>$v_{\\max}$ đo (cm/s)</th>'),
 ("l11-bai-tap-nang-luong-dao-dong",
  '<tr><td>4</td><td>55,0</td><td>37,8</td></tr>\n</tbody>\n</table>\n</div>\n<!--video:tn-l11-baitapnangluong-01-->',
  '<tr><td>4</td><td>55,0</td><td>37,8</td></tr>\n</tbody>\n</table>\n</details>\n</div>\n<!--video:tn-l11-baitapnangluong-01-->'),
 ("l11-co-nang-dao-dong",
  '<li><strong>Quan sát:</strong> Trên cao, vận tốc bằng không, thế năng $mgh=196$ J. Ở đáy, thế năng về mốc, động năng $196$ J, tốc độ khoảng $3{,}13$ m/s.</li>',
  '<li><strong>Quan sát:</strong> tính thế năng trên cao, động năng và tốc độ ở đáy (xem video bên dưới).' + D.format('Số tính (xem sau video)', 'Trên cao, vận tốc bằng không, thế năng $mgh=196$ J. Ở đáy, thế năng về mốc, động năng $196$ J, tốc độ khoảng $3{,}13$ m/s.') + '</li>'),
 ("l11-van-toc-gia-toc",
  '<p>Sai số ước lượng: $\\Delta v_{max}\\approx 1{,}06$ cm/s và $\\Delta a$ tại biên $\\approx 10{,}5$ cm/s². Lệch $v_{max}$ giữa lần 3 và lần 4 chỉ $0{,}55$ cm/s — nhỏ hơn phần do thước, $0{,}025\\times 31{,}42\\approx 0{,}79$ cm/s.</p>\n<details class="tl-details tl-more">\n<summary>Xem năm lần và cách cộng sai số</summary>\n',
  '<details class="tl-details tl-more">\n<summary>Sai số: năm lần và cách cộng (xem sau video)</summary>\n<p>Sai số ước lượng: $\\Delta v_{max}\\approx 1{,}06$ cm/s và $\\Delta a$ tại biên $\\approx 10{,}5$ cm/s². Lệch $v_{max}$ giữa lần 3 và lần 4 chỉ $0{,}55$ cm/s — nhỏ hơn phần do thước, $0{,}025\\times 31{,}42\\approx 0{,}79$ cm/s.</p>\n'),
]
apply = "--apply" in sys.argv
loi = 0
js = lambda t: json.dumps(t, ensure_ascii=False)[1:-1]
for slug, old, new in S:
    for f in ("theory.src.html", "theory.html", "bundle.json"):
        p = ROOT / f"content/lesson-samples/{slug}/{f}"
        s = p.read_text(encoding="utf-8")
        o, n = (js(old), js(new)) if f == "bundle.json" else (old, new)
        c = s.count(o)
        if c != 1:
            print(f"LOI {slug}/{f}: thấy {c} chỗ cho «{old[:50]}»"); loi += 1; continue
        if apply:
            p.write_text(s.replace(o, n), encoding="utf-8")
    print(f"ok {slug}: «{old[:60]}»")
if apply:
    for slug in {x[0] for x in S}:
        json.loads((ROOT / f"content/lesson-samples/{slug}/bundle.json").read_text(encoding="utf-8"))
print("lỗi:", loi)
