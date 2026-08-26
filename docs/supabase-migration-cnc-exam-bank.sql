-- Cho phép bảng exams lưu luôn ngân hàng câu hỏi trắc nghiệm CNC (Bài học/Bài kiểm tra
-- vận hành máy), thay vì viết cứng trong services/cnc-lms.ts và data/cnc/*.json.
-- Mỗi ngân hàng CNC là 1 dòng exams với cnc_key duy nhất (vd "lesson-2", "operation-turn"),
-- luôn published = false nên không lộ ra trang /kiem-tra công khai.

alter table public.exams add column if not exists cnc_key text unique;
