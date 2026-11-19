#!/usr/bin/env python3
"""Sinh SQL nạp 10 đề thi thử vào mục Kiểm tra của bài 12 AVCN. Chạy: python3 sql.py [--hien] > x.sql
Mặc định đề ẨN (published=false); --hien bật Hiện cả bài lẫn 10 đề. Chạy lại an toàn (đề cùng tiêu đề → cập nhật câu hỏi)."""
import json, pathlib, sys
HERE = pathlib.Path(__file__).resolve().parent
hien = "true" if "--hien" in sys.argv else "false"
lit = lambda s: "'" + s.replace("'", "''") + "'"
print("begin;")
print("""do $$ declare v_lesson bigint; v_item bigint; v_exam bigint; begin
  select y.id into v_lesson from lessons y join chapters x on x.id = y.chapter_id
    where x.subject_code = 'avcn' and y.sort_order = 12 and y.title like 'Đề thi thử%';
  if v_lesson is null then raise exception 'chưa có bài 12 (chạy migration 20261119150000)'; end if;
  select i.id into v_item from lesson_items i where i.lesson_id = v_lesson and i.kind = 'kiem_tra' order by i.id limit 1;
  if v_item is null then
    insert into lesson_items (lesson_id, kind, title, subtitle, body_html, video_url, pdf_url, questions, exam_ids, sort_order)
    values (v_lesson, 'kiem_tra', 'Đề thi thử', '10 đề, mỗi đề 27 câu — làm theo khung đề cuối kỳ', '', '', '', '[]'::jsonb, '{}', 5)
    returning id into v_item;
  end if;""")
for e in json.load(open(HERE / "exams.json")):
    print(f"""  select x.id into v_exam from exams x join lesson_items i on x.id = any(i.exam_ids) and i.id = v_item where x.title = {lit(e['title'])} limit 1;
  if v_exam is null then
    insert into exams (title, duration_minutes, published, subject_code, topic, difficulty, questions)
    values ({lit(e['title'])}, {e['duration_minutes']}, {hien}, 'avcn', {lit(e['topic'])}, 'trung-binh', {lit(json.dumps(e['questions'], ensure_ascii=False))}::jsonb)
    returning id into v_exam;
    update lesson_items set exam_ids = array_append(exam_ids, v_exam) where id = v_item;
  else
    update exams set questions = {lit(json.dumps(e['questions'], ensure_ascii=False))}::jsonb, published = {hien}, duration_minutes = {e['duration_minutes']} where id = v_exam;
  end if;""")
print(f"  update lessons set published = {hien} where id = v_lesson;\nend $$;\ncommit;")
