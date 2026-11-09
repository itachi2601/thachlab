-- Bài đọc SHCN gắn vào tuần sinh hoạt (chương trình 3 năm, content/shcn-3-nam).
-- lesson_key = "hk1/b03" → sinh viên bấm "Đọc bài tuần này" mở /sinh-hoat/hk1/b03.
-- Cột nullable, bảng ~3 dòng: chạy lúc nào cũng được. RLS giữ nguyên (policy theo dòng, không theo cột).
alter table public.homeroom_weekly_sessions
  add column if not exists lesson_key text
    check (lesson_key is null or lesson_key ~ '^hk[1-6]/b[0-9]{2}$');

comment on column public.homeroom_weekly_sessions.lesson_key is
  'Bài đọc SHCN của tuần, dạng hk1/b03 (lib/shcn/bai-doc.json). Null = không có bài đọc.';

-- Rollback:
-- alter table public.homeroom_weekly_sessions drop column if exists lesson_key;
