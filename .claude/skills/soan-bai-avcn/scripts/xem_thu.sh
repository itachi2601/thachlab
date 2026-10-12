#!/usr/bin/env bash
# Dựng bản xem thử (tab Học + tab Đề mẫu) cho một bài AVCN và chụp 375 px. Chạy từ gốc repo thachlab, cần Google Chrome.
# Dùng: bash .claude/skills/soan-bai-avcn/scripts/xem_thu.sh content/lesson-samples/avcn-chapter-<n>-<slug>
set -euo pipefail
BAI="${1:?thư mục bài}"
ROOT="$(cd "$(dirname "$0")/../../../.." && pwd)"
S="$ROOT/.claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts"
TITLE="$(python3 -c "import json;m=json.load(open('$BAI/data/bai.json'))['meta'];print(f\"Chapter {m['chapter']}: {m['title_en']}\")")"
SPEAK='<script>document.addEventListener("click",e=>{const b=e.target.closest("[data-tl-speak]");if(!b)return;e.preventDefault();e.stopPropagation();const u=new SpeechSynthesisUtterance(b.dataset.tlSpeak);u.lang="en-US";u.rate=0.9;speechSynthesis.cancel();speechSynthesis.speak(u);});</script></body>'
fix() { # ảnh file:// cho Chrome headless, bỏ lazy để chụp đủ ảnh, thêm nút nghe
  sed -i '' -e "s#src=\"/assets/#src=\"file://$ROOT/public/assets/#g" -e 's# loading="lazy"##g' "$1"/*.html
  python3 - "$1/xem-thu.html" "$SPEAK" <<'PY'
import sys; p, js = sys.argv[1], sys.argv[2]; s = open(p).read(); open(p, "w").write(s.replace("</body>", js, 1))
PY
}
rm -rf "$BAI/xem-thu" "$BAI/xem-thu-de-mau"
python3 "$S/build_preview.py" "$BAI/theory.html" "$BAI/xem-thu" --tieu-de "$TITLE" --phu-de "Anh văn chuyên ngành Cơ khí" >/dev/null
fix "$BAI/xem-thu"
python3 -c "import json;b=json.load(open('$BAI/bundle.json'));open('$BAI/de-mau.preview.html','w').write(''.join(f\"<h3>{w['label']}</h3>{w['body_html']}\" for w in b['worked_examples']))"
python3 "$S/build_preview.py" "$BAI/de-mau.preview.html" "$BAI/xem-thu-de-mau" --tieu-de "Đề mẫu — $TITLE" --phu-de "5 Part, Part 1–3 tự chấm" >/dev/null
rm -f "$BAI/de-mau.preview.html"; fix "$BAI/xem-thu-de-mau"
python3 "$S/chup_anh.py" "$BAI/xem-thu" --kiem-tran | tail -1
python3 "$S/chup_anh.py" "$BAI/xem-thu" | tail -1
python3 "$S/chup_anh.py" "$BAI/xem-thu-de-mau" | tail -1
echo "Mở cho thầy: $BAI/xem-thu/xem-thu.html và $BAI/xem-thu-de-mau/xem-thu.html"
