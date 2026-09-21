-- ============================================================
-- Migration: Chống gian lận khi làm bài (theo dõi rời tab/fullscreen)
-- Chạy SAU: supabase-schema.sql
-- Idempotent — chạy lại được.
-- ============================================================

alter table public.exam_results
  add column if not exists violation_count int not null default 0;

alter table public.exam_results
  add column if not exists violations jsonb not null default '[]';
-- violations: mảng event { type: "tab_switch" | "fullscreen_exit", at: ISOString, away_ms: number }
-- Ghi bởi chính học sinh khi nộp bài (cùng cơ chế insert exam_results hiện có),
-- dùng để giáo viên đối chiếu — không phải bằng chứng chống chối cãi tuyệt đối.
