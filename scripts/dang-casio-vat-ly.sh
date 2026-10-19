#!/usr/bin/env bash
# Đăng 5 gói Casio (lớp "Giải Vật lí trên máy tính cầm tay") vào 5 bài đã tạo bởi migration 20261019120000.
# Bài vẫn ẨN (published=false) cho tới khi thầy duyệt: bật Hiện ở /quan-tri/bai-hoc hoặc --publish.
#   bash scripts/dang-casio-vat-ly.sh              # dựng lại gói + đăng (ghi đè lý thuyết/bài luyện/mini-test)
#   bash scripts/dang-casio-vat-ly.sh --dry        # chỉ dựng + kiểm gói, không ghi DB
#   bash scripts/dang-casio-vat-ly.sh --publish    # sau khi thầy duyệt: bật Hiện cả 5 bài
set -euo pipefail
cd "$(dirname "$0")/.."
python3 scripts/build-casio-vat-ly.py
[[ "${1:-}" == "--dry" ]] && { echo "Dry-run: chỉ dựng gói."; exit 0; }

URL=$(grep '^NEXT_PUBLIC_SUPABASE_URL=' .env.local | cut -d= -f2-)
KEY=$(grep '^SUPABASE_SERVICE_ROLE_KEY=' .env.local | cut -d= -f2-)
[[ -n "$URL" && -n "$KEY" ]] || { echo "Thiếu NEXT_PUBLIC_SUPABASE_URL / SUPABASE_SERVICE_ROLE_KEY trong .env.local"; exit 1; }
export SUPABASE_SERVICE_ROLE_KEY="$KEY"

rest() { curl -fsS "$URL/rest/v1/$1" -H "apikey: $KEY" -H "Authorization: Bearer $KEY" "${@:2}"; }
CH=$(rest "chapters?subject_code=eq.casio-vat-ly&select=id" | python3 -c 'import json,sys;print(json.load(sys.stdin)[0]["id"])')

if [[ "${1:-}" == "--publish" ]]; then
  rest "lessons?chapter_id=eq.$CH" -X PATCH -H "Content-Type: application/json" -d '{"published":true}' -o /dev/null
  rest "exams?subject_code=eq.casio-vat-ly" -X PATCH -H "Content-Type: application/json" -d '{"published":true}' -o /dev/null
  echo "Đã bật Hiện cả 5 bài và 5 đề mini-test Casio."; exit 0
fi

declare -a PAIRS=(
  "wp-01-so-tay-fx580vnx|Sổ tay máy Casio fx-580VN X"
  "wp-03-dao-dong-co|Dao động cơ"
  "wp-04-song-co|Sóng cơ"
  "wp-05-dien-xoay-chieu|Điện xoay chiều"
  "wp-06-dien-tu-anh-sang|Điện từ và sóng ánh sáng"
)
for pair in "${PAIRS[@]}"; do
  dir="${pair%%|*}"; title="${pair##*|}"
  ID=$(rest "lessons?chapter_id=eq.$CH&select=id,title" | python3 -c 'import json,sys;t=sys.argv[1];print(next(x["id"] for x in json.load(sys.stdin) if x["title"]==t))' "$title")
  echo "══ $title (bài $ID) ══"
  npx tsx scripts/upload-lesson.mts "content/casio-vat-ly/_dung/$dir/bundle.json" --lesson "$ID" --target luyen_tap --mode replace
done
# Đề do upload-lesson tạo ra mặc định published=true và hiện trong hub lớp: giữ ẩn cùng bài tới khi duyệt.
rest "exams?subject_code=eq.casio-vat-ly" -X PATCH -H "Content-Type: application/json" -d '{"published":false}' -o /dev/null
echo "Xong. Bài và đề vẫn ẩn. Xem thử ở /quan-tri hoặc lớp /lop-hoc/casio-vat-ly (tài khoản thầy)."
