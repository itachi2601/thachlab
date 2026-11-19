#!/usr/bin/env python3
"""Sinh SQL đăng 10 đề Kiểm tra từ vựng AVCN vào mục Kiểm tra của bài (Chapter n = lesson 167+n).

- Đề tạo ở trạng thái ẨN (published=false); thầy duyệt rồi mới bật.
- GẮN THÊM vào lesson_items kind='kiem_tra' (giữ đề 30 phút sẵn có của C2/C5/C8 và bài làm của SV);
  bài chưa có mục Kiểm tra thì tạo mục mới.
- Chạy lại an toàn: đề cùng tiêu đề đã gắn → chỉ cập nhật câu hỏi (không tạo đề mới).

  python3 .claude/skills/soan-bai-avcn/scripts/sql_kiem_tra_tu_vung.py > /tmp/x.sql
  cd /Users/MAC/Projects/thachlab && supabase db query --linked -f /tmp/x.sql
"""
import glob, json, pathlib, re

ROOT = pathlib.Path(__file__).resolve().parents[4]


def lit(s: str) -> str:
    return "'" + s.replace("'", "''") + "'"


print("begin;")
for f in sorted(glob.glob(str(ROOT / "content/lesson-samples/avcn-chapter-*/kiem-tra-tu-vung/bundle.json"))):
    ch = int(re.search(r"chapter-(\d+)", f).group(1))
    lesson = 167 + ch
    e = json.load(open(f))["exam"]
    print(f"""do $$
declare v_exam bigint; v_item bigint;
begin
  perform 1 from lessons where id = {lesson} and title like 'Chapter {ch}:%';
  if not found then raise exception 'lesson {lesson} không phải Chapter {ch}'; end if;
  select i.id into v_item from lesson_items i where i.lesson_id = {lesson} and i.kind = 'kiem_tra' order by i.id limit 1;
  select e.id into v_exam from exams e
    join lesson_items i on e.id = any(i.exam_ids) and i.lesson_id = {lesson}
    where e.title = {lit(e['title'])} limit 1;
  if v_exam is not null then
    update exams set questions = {lit(json.dumps(e['questions'], ensure_ascii=False))}::jsonb,
      duration_minutes = {e['duration_minutes']} where id = v_exam;
    raise notice 'Chapter {ch}: cập nhật đề %', v_exam;
    return;
  end if;
  insert into exams (title, duration_minutes, published, subject_code, topic, difficulty, questions)
  values ({lit(e['title'])}, {e['duration_minutes']}, false, 'avcn', {lit(e['topic'])}, 'de',
          {lit(json.dumps(e['questions'], ensure_ascii=False))}::jsonb)
  returning id into v_exam;
  if v_item is null then
    insert into lesson_items (lesson_id, kind, title, subtitle, body_html, video_url, pdf_url, questions, exam_ids, sort_order)
    values ({lesson}, 'kiem_tra', 'Kiểm tra', {lit(f"{len(e['questions'])} câu trắc nghiệm — {e['duration_minutes']} phút")},
            '', '', '', '[]'::jsonb, array[v_exam], 5);
  else
    update lesson_items set exam_ids = array_append(exam_ids, v_exam) where id = v_item;
  end if;
  raise notice 'Chapter {ch}: tạo đề % (ẩn), gắn vào bài {lesson}', v_exam;
end $$;""")
print("commit;")
