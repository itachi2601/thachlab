-- ============================================================================
-- Rollback: 20261011150000_student_mistakes_spaced_review.sql
-- ============================================================================

drop trigger if exists trg_practice_question_results_mistake on public.practice_question_results;
drop function if exists public.trg_ingest_practice_question_mistake();

drop trigger if exists trg_exam_question_results_mistake on public.exam_question_results;
drop function if exists public.trg_ingest_exam_question_mistake();

drop function if exists public.mistake_review_quiz_submit(bigint, jsonb);
drop function if exists public.mistake_review_quiz_start(int);
drop function if exists public.mistake_stats_of(uuid);

drop table if exists public.student_mistake_review_attempts;
drop table if exists public.student_mistakes;
