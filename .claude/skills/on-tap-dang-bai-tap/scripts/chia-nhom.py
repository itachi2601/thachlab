#!/usr/bin/env python3
"""Chia câu ứng viên thành các file in/<bài>_<chủ đề>.json cho subagent gán dạng (tối đa 80 câu mỗi file).
   python3 .claude/skills/on-tap-dang-bai-tap/scripts/chia-nhom.py <thu_muc_lam_viec> [--bo-bai 126 ...]
   Cần dangs.json, cands.json, cands2.json (do lay-dang.sh sinh). --bo-bai: bài có dạng quá cụ thể, không gán."""
import json, os, sys, collections
W = sys.argv[1]
skip = {int(x) for x in sys.argv[sys.argv.index('--bo-bai') + 1:]} if '--bo-bai' in sys.argv else set()
dangs = json.load(open(f'{W}/dangs.json'))
os.makedirs(f'{W}/in', exist_ok=True); os.makedirs(f'{W}/out', exist_ok=True)
groups = collections.defaultdict(list)
for f in ('cands.json', 'cands2.json'):
    if os.path.exists(f'{W}/{f}'):
        for r in json.load(open(f'{W}/{f}')):
            if r['lesson_id'] not in skip:
                groups[(r['lesson_id'], r['topic_id'])].append(r)
for (l, t), qs in groups.items():
    dg = [x for x in dangs if x['lesson_id'] == l and x['topic_id'] == t]
    json.dump({'lesson_id': l, 'topic_id': t,
               'dang': [{'ord': x['ord'], 'label': x['label'], 'problem': x['problem']} for x in dg],
               'questions': [{'id': q['id'], 'type': q['qtype'], 'diff': q['difficulty'], 'q': q['q']} for q in qs[:80]]},
              open(f'{W}/in/{l}_{t}.json', 'w'), ensure_ascii=False)
    print(f'in/{l}_{t}.json: {len(dg)} dạng {[x["ord"] for x in dg]}, {min(len(qs), 80)}/{len(qs)} câu')
