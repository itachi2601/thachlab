#!/usr/bin/env bash
# Sinh 3 file SQL (dạng của bài + câu ứng viên) cho MỘT chương, rồi in lệnh chạy trong tab terminal.
#   bash .claude/skills/on-tap-dang-bai-tap/scripts/lay-dang.sh <chapter_id> <thu_muc_lam_viec>
# Chạy lệnh in ra từ GỐC repo (supabase CLI cần nhận project). Không ghi DB.
set -euo pipefail
CH="${1:?cần chapter_id}"; W="${2:?cần thư mục làm việc}"
mkdir -p "$W"
cat > "$W/dangs.sql" <<SQL
select i.lesson_id, l.title as lesson, d.ord::int as ord, d.q ->> 'label' as label, (d.q ->> 'topic_id')::bigint as topic_id, d.q ->> 'topic' as topic,
  left(regexp_replace(coalesce(d.q ->> 'problem_html', ''), '<[^>]+>', ' ', 'g'), 500) as problem
from lesson_items i
join lessons l on l.id = i.lesson_id and l.chapter_id = $CH
cross join lateral jsonb_array_elements(i.questions) with ordinality as d(q, ord)
where i.kind = 'bai_tap_mau' and d.q ->> 'label' like 'Dạng%'
order by i.lesson_id, d.ord;
SQL
for MODE in shared single; do
  if [ "$MODE" = shared ]; then OP='> 1'; F=cands.sql; else OP='= 1'; F=cands2.sql; fi
  cat > "$W/$F" <<SQL
with dangs as (
  select i.lesson_id, (d.q ->> 'topic_id')::bigint as topic_id
  from lesson_items i join lessons l on l.id = i.lesson_id and l.chapter_id = $CH
  cross join lateral jsonb_array_elements(i.questions) d(q)
  where i.kind = 'bai_tap_mau' and d.q ->> 'label' like 'Dạng%'
), grp as (
  select lesson_id, topic_id from dangs group by 1,2 having count(*) $OP
)
select s.lesson_id, qb.topic_id, qb.id, qb.qtype, qb.difficulty, left(regexp_replace(qb.question ->> 'question', '\s+', ' ', 'g'), 420) as q
from grp s join question_bank qb on qb.topic_id = s.topic_id and qb.form = 'bai_tap' and not qb.archived
where coalesce(array_length(qb.lint_flags, 1), 0) = 0
order by s.lesson_id, qb.topic_id, md5(qb.id::text);
SQL
done
echo "Chạy trong tab terminal, từ gốc repo:"
for f in dangs cands cands2; do
  echo "supabase db query --linked --output-format json -f $W/$f.sql > $W/$f.json 2> $W/$f.err"
done
