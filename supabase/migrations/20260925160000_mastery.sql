-- ============================================================================
-- feat(mastery): nhãn "mức độ thành thạo" theo YCCĐ — nhánh feat/mastery, 25/9/2026
-- ============================================================================
-- Đọc trước: docs/mastery-rules.md (ngưỡng nhãn, công thức, lý do earned/max thay vì
-- is_correct) và feat/SURVEY.md mục 1 + mục 5 (Agent C) — đã khảo sát schema thật.
--
-- CHƯA CHẠY LÊN PRODUCTION. Tên file dùng mốc thời gian SAU
-- 20260925150000 — nếu nhánh feat/difficulty (đang làm song song) cũng để một
-- migration ở đúng mốc này, orchestrator lúc merge sẽ đổi tên 1 trong 2 cho khỏi
-- trùng thứ tự chạy; nội dung ở đây độc lập, không phụ thuộc bảng/cột nào của
-- feat/difficulty.
--
-- Cả 2 hàm đều `security invoker` — chạy dưới quyền người gọi, KHÔNG nới RLS.
-- exam_question_results/practice_question_results đã có policy
-- "student_id = (select auth.uid()) OR teaches_student(student_id)" nên học sinh
-- chỉ đọc được mastery của chính mình qua auth.uid(); giáo viên/trợ giảng dạy em đó
-- có thể gọi get_lesson_mastery/get_chapter_mastery hộ (RLS tự cho phép) — nhưng vì
-- hàm dùng auth.uid() làm "học sinh đang xem" nên hiện chỉ trả kết quả của CHÍNH
-- người gọi; muốn xem hộ học sinh khác cần tham số p_student riêng — để dành cho
-- giai đoạn "Learning Journey" sau, không làm ở đây (giữ phạm vi đúng yêu cầu: nhãn
-- cho học sinh đang đăng nhập).
--
-- Cách chạy (khi thầy xác nhận): supabase db query --linked -f <file này>
-- ============================================================================

begin;

-- ---------------------------------------------------------------------------
-- 1. Nhãn mastery từng YCCĐ của MỘT bài, cho học sinh đang đăng nhập.
--    Trả 1 dòng / YCCĐ (is_summary = false) + 1 dòng tổng kết cả bài
--    (is_summary = true, topic_id/topic_name = null).
--
--    Dữ liệu: gộp exam_question_results + practice_question_results, lấy tối đa
--    10 lượt gần nhất/YCCĐ (created_at desc, gộp cả 2 bảng rồi mới cắt).
--    Ngưỡng: <4 lượt → 'insufficient'; earned/max >=0.8 → 'mastered';
--    >=0.5 → 'practicing'; còn lại → 'weak'. Xem docs/mastery-rules.md mục 2-3.
--
--    Câu hỏi gắn tầng Bài (parent_id is null, không có YCCĐ con) vẫn góp vào nhãn
--    cả bài (qua CTE `groups` gồm cả topic tầng Bài lẫn YCCĐ con) nhưng KHÔNG lộ
--    ra thành một dòng YCCĐ riêng cho client (lọc `where parent_id is not null`
--    ở phần SELECT cuối). Câu topic_id is null bị loại hoàn toàn (không join được).
--
--    TODO (giai đoạn sau, khi feat/difficulty merge xong và exam_question_results/
--    practice_question_results có cột difficulty): cân nhắc trọng số Dễ/TB/Khó khi
--    tính tỉ lệ — xem docs/mastery-rules.md mục 5. Chưa làm ở bản này.
-- ---------------------------------------------------------------------------
create or replace function public.get_lesson_mastery(p_lesson bigint)
returns table (
  topic_id bigint,
  topic_name text,
  sort_order integer,
  answered_count integer,
  level text,
  pct integer,
  is_summary boolean
)
language sql
stable
security invoker
set search_path = public
as $$
  with groups as (
    -- Cả topic tầng Bài (parent_id null) lẫn YCCĐ con (parent_id not null) của bài này —
    -- trigger question_topic_tree_guard() đã copy lesson_id từ cha xuống YCCĐ con nên lọc
    -- thẳng lesson_id = p_lesson là đủ, không cần join lessons/chapters.
    select id, parent_id, name, sort_order
    from public.question_topics
    where lesson_id = p_lesson
  ),
  attempts as (
    select topic_id, earned, max, created_at,
           row_number() over (partition by topic_id order by created_at desc) as rn
    from (
      select topic_id, earned, max, created_at
      from public.exam_question_results
      where student_id = (select auth.uid())
        and topic_id in (select id from groups)
      union all
      select topic_id, earned, max, created_at
      from public.practice_question_results
      where student_id = (select auth.uid())
        and topic_id in (select id from groups)
    ) u
  ),
  last10 as (
    select topic_id, earned, max from attempts where rn <= 10
  ),
  agg as (
    select
      g.id as topic_id,
      g.parent_id,
      g.name as topic_name,
      g.sort_order,
      count(a.topic_id)::int as answered_count,
      coalesce(sum(a.earned), 0)::numeric as sum_earned,
      coalesce(sum(a.max), 0)::numeric as sum_max
    from groups g
    left join last10 a on a.topic_id = g.id
    group by g.id, g.parent_id, g.name, g.sort_order
  ),
  leveled as (
    select
      *,
      case
        when answered_count < 4 or sum_max = 0 then 'insufficient'
        when sum_earned / sum_max >= 0.8 then 'mastered'
        when sum_earned / sum_max >= 0.5 then 'practicing'
        else 'weak'
      end as level
    from agg
  ),
  ranked as (
    select
      *,
      case level when 'weak' then 0 when 'practicing' then 1 when 'mastered' then 2 else null end as rnk
    from leveled
  ),
  lesson_summary as (
    select
      min(rnk) as min_rnk,
      count(*) filter (where rnk is not null) as have_data
    from ranked
  )
  select
    r.topic_id,
    r.topic_name,
    r.sort_order,
    r.answered_count,
    r.level,
    case when r.sum_max = 0 then null else round(r.sum_earned / r.sum_max * 100)::int end as pct,
    false as is_summary
  from ranked r
  where r.parent_id is not null
  union all
  select
    null::bigint,
    null::text,
    2147483647,
    null::integer,
    case
      when ls.have_data = 0 then 'insufficient'
      when ls.min_rnk = 0 then 'weak'
      when ls.min_rnk = 1 then 'practicing'
      else 'mastered'
    end,
    null::integer,
    true
  from lesson_summary ls
  order by is_summary, sort_order;
$$;

revoke all on function public.get_lesson_mastery(bigint) from public;
grant execute on function public.get_lesson_mastery(bigint) to authenticated;

-- ---------------------------------------------------------------------------
-- 2. Nhãn mastery từng BÀI trong một chương (nền cho Learning Journey sau này).
--    Bọc lại get_lesson_mastery qua lateral join — một nguồn logic duy nhất,
--    giống cách ta_monthly_scores bọc ta_monthly_score
--    (supabase/migrations/20260925130000_perf_rpc_gv.sql).
-- ---------------------------------------------------------------------------
create or replace function public.get_chapter_mastery(p_chapter bigint)
returns table (
  lesson_id bigint,
  lesson_title text,
  sort_order integer,
  level text
)
language sql
stable
security invoker
set search_path = public
as $$
  select l.id, l.title, l.sort_order, m.level
  from public.lessons l
  cross join lateral (
    select level from public.get_lesson_mastery(l.id) where is_summary limit 1
  ) m
  where l.chapter_id = p_chapter
  order by l.sort_order;
$$;

revoke all on function public.get_chapter_mastery(bigint) from public;
grant execute on function public.get_chapter_mastery(bigint) to authenticated;

commit;

-- ============================================================================
-- ROLLBACK (chạy khi cần gỡ; client cần tự lùi UI vì không có fallback tự động
-- như các RPC ở 20260925130000_perf_rpc_gv.sql)
-- ============================================================================
-- begin;
-- drop function if exists public.get_chapter_mastery(bigint);
-- drop function if exists public.get_lesson_mastery(bigint);
-- commit;
