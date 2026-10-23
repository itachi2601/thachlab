#!/usr/bin/env python3
"""Gộp out/*.json (kết quả subagent) thành một file SQL nạp vào question_dang.
   python3 .claude/skills/on-tap-dang-bai-tap/scripts/tao-sql.py <thu_muc_lam_viec> <file.sql> [--chi-giu BAI:ID ...]
   Kiểm: đủ id so với in/. --chi-giu BAI:ID: với bài đó chỉ giữ câu ID (dùng khi bài có dạng quá cụ thể)."""
import json, glob, sys, collections
W, OUT = sys.argv[1], sys.argv[2]
keep = collections.defaultdict(set)
if '--chi-giu' in sys.argv:
    for x in sys.argv[sys.argv.index('--chi-giu') + 1:]:
        b, i = x.split(':'); keep[int(b)].add(i)
label = {(x['lesson_id'], x['ord']): x['label'] for x in json.load(open(f'{W}/dangs.json'))}
rows = []
for f in sorted(glob.glob(f'{W}/out/*.json')):
    name = f.split('/')[-1][:-5]; l, _ = map(int, name.split('_'))
    o = json.load(open(f)); a = o['assign']
    ids = {str(q['id']) for q in json.load(open(f'{W}/in/{name}.json'))['questions']}
    assert set(a) == ids, f'{name}: thiếu/thừa id'
    uns = {str(i) for i in o.get('unsure', [])}
    for qid, od in a.items():
        if od is None or (l in keep and qid not in keep[l]): continue
        rows.append((int(qid), l, label[(l, od)], qid in uns))
q = lambda s: "'" + s.replace("'", "''") + "'"
vals = ",\n".join(f"  ({i}, {l}, {q(lab)}, {'true' if u else 'false'})" for i, l, lab, u in rows)
open(OUT, 'w').write(f"""-- Gán dạng bài tập cho câu ngân hàng (sinh bởi skill on-tap-dang-bai-tap). Rollback: delete from public.question_dang where source = 'claude-2026-10-23';
begin;
insert into public.question_dang (question_id, lesson_id, dang_label, unsure, source)
select v.qid, v.lid, v.label, v.unsure, 'claude-2026-10-23'
from (values
{vals}
) as v(qid, lid, label, unsure)
join public.question_bank qb on qb.id = v.qid
on conflict (question_id, lesson_id) do update set dang_label = excluded.dang_label, unsure = excluded.unsure, source = 'claude-2026-10-23';
commit;
""")
c = collections.Counter((l, lab[:48], u) for _, l, lab, u in rows)
for k, v in sorted(c.items()): print(k, v)
print(len(rows), 'câu →', OUT)
