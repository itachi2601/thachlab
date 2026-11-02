#!/usr/bin/env bash
# Ghi mục Lý thuyết (lesson_items kind=ly_thuyet) của 16 bài học phần CTTC "WorldSkills — Industrial Mechanics"
# từ content/worldskills-im/_dung/*.html (dựng bằng scripts/build-worldskills-im.mjs). Bài do migration
# 20261102080000 tạo. Chỉ đụng mục ly_thuyet của đúng 16 bài: có rồi thì PATCH body_html, chưa có thì INSERT.
#   bash scripts/dang-worldskills-im.sh          # dựng lại + ghi
#   bash scripts/dang-worldskills-im.sh --dry    # dựng + in việc sẽ làm, không ghi
set -euo pipefail
cd "$(dirname "$0")/.."
node scripts/build-worldskills-im.mjs >/dev/null
URL=$(grep '^NEXT_PUBLIC_SUPABASE_URL=' .env.local | cut -d= -f2-)
KEY=$(grep '^SUPABASE_SERVICE_ROLE_KEY=' .env.local | cut -d= -f2-)
[[ -n "$URL" && -n "$KEY" ]] || { echo "Thiếu NEXT_PUBLIC_SUPABASE_URL / SUPABASE_SERVICE_ROLE_KEY trong .env.local"; exit 1; }
export URL KEY DRY="${1:-}"
python3 - <<'PY'
import json, os, urllib.request, urllib.parse
URL, KEY, DRY = os.environ["URL"], os.environ["KEY"], os.environ["DRY"] == "--dry"
H = {"apikey": KEY, "Authorization": f"Bearer {KEY}", "Content-Type": "application/json", "Prefer": "return=representation"}
def rest(path, method="GET", body=None):
    req = urllib.request.Request(f"{URL}/rest/v1/{path}", data=json.dumps(body).encode() if body is not None else None, headers=H, method=method)
    with urllib.request.urlopen(req) as r: return json.loads(r.read() or b"null")
chs = {c["sort_order"]: c["id"] for c in rest("chapters?subject_code=eq.worldskills-im&select=id,sort_order")}
if len(chs) != 5: raise SystemExit(f"Chưa đủ 5 chương worldskills-im (có {len(chs)}) — chạy migration 20261102080000 trước.")
ids = ",".join(str(v) for v in chs.values())
lessons = {(c["chapter_id"], c["sort_order"]): c for c in rest(f"lessons?chapter_id=in.({ids})&select=id,chapter_id,sort_order,title")}
items = rest(f"lesson_items?kind=eq.ly_thuyet&lesson_id=in.({','.join(str(l['id']) for l in lessons.values())})&select=id,lesson_id")
by_lesson = {i["lesson_id"]: i["id"] for i in items}
idx = json.load(open("content/worldskills-im/_dung/index.json", encoding="utf8"))
n_ins = n_upd = 0
for e in idx:
    l = lessons.get((chs[e["ch"]], e["so"]))
    if not l: raise SystemExit(f"Thiếu bài chương {e['ch']} số {e['so']} trong DB")
    html = open(f"content/worldskills-im/_dung/{e['file']}", encoding="utf8").read()
    row = {"lesson_id": l["id"], "kind": "ly_thuyet", "title": "Nội dung bài", "subtitle": "Song ngữ Anh – Việt, dịch từ tài liệu WorldSkills Shanghai 2026", "body_html": html, "video_url": "", "pdf_url": "", "questions": [], "exam_ids": [], "sort_order": 1}
    act = "PATCH" if l["id"] in by_lesson else "INSERT"
    print(f"{act:6} bài {l['id']:>4} ch{e['ch']}.{e['so']} {l['title'][:48]:50} {e['bytes']//1024} KB")
    if DRY: continue
    if act == "PATCH":
        rest(f"lesson_items?id=eq.{by_lesson[l['id']]}&kind=eq.ly_thuyet", "PATCH", {"body_html": html}); n_upd += 1
    else:
        rest("lesson_items", "POST", row); n_ins += 1
if not DRY:
    chk = rest(f"lesson_items?kind=eq.ly_thuyet&lesson_id=in.({','.join(str(l['id']) for l in lessons.values())})&select=lesson_id,body_html")
    bad = [c["lesson_id"] for c in chk if len(c["body_html"]) < 1000]
    print(f"Đã ghi: {n_ins} chèn, {n_upd} cập nhật; kiểm lại {len(chk)}/16 mục có nội dung" + (f"; NGẮN BẤT THƯỜNG: {bad}" if bad else ""))
PY
echo "Trang bài chỉ đối chiếu DB lúc build → cần: bash scripts/deploy.sh"
