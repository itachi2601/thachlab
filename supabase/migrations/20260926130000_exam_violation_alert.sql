-- ============================================================
-- Migration: Cảnh báo phụ đạo khi vi phạm nhiều lúc làm bài
--            (rời tab / thoát toàn màn hình)
--
-- Bối cảnh: exam_results.violation_count/violations đã được ghi từ
-- docs/supabase-migration-exam-proctoring.sql (học sinh tự ghi khi nộp bài)
-- nhưng chưa nối vào hệ thống Cảnh báo phụ đạo (student_alerts) — trợ giảng
-- không có cách nào biết một bài làm có nhiều vi phạm để kiểm tra lại kiến
-- thức thực của học sinh (điểm bài đó có thể không đáng tin).
--
-- Thêm kind='exam_violation': tự tạo cảnh báo khi violation_count >= 3 trong
-- MỘT lần nộp bài (>= 6 thì 'urgent'). KHÔNG tự đóng khi có bài sau đó sạch
-- (khác evaluate_student_alerts) — nghi vấn của một lần vi phạm nặng không
-- biến mất chỉ vì bài kế tiếp không vi phạm; trợ giảng tự đóng khi đã kiểm
-- tra lại kiến thức.
--
-- Idempotent — chạy lại được.
-- Rollback: perf/rollback/20260926130000_exam_violation_alert.down.sql
-- ============================================================

alter table public.student_alerts drop constraint if exists student_alerts_kind_check;
alter table public.student_alerts add constraint student_alerts_kind_check
  check (kind in ('low_score_streak', 'missed_assessment', 'exam_violation'));

create or replace function public.evaluate_exam_violation_alert(p_result_id bigint)
returns void
language plpgsql security definer set search_path = public
as $$
declare
  v_threshold int := 3;
  v_student uuid;
  v_count int;
  v_exam_id bigint;
  v_title text;
  v_class bigint;
begin
  select student_id, violation_count, exam_id
    into v_student, v_count, v_exam_id
    from public.exam_results
    where id = p_result_id;

  if v_student is null or v_count < v_threshold then
    return;
  end if;

  select title into v_title from public.exams where id = v_exam_id;

  -- Ưu tiên lớp gắn với bài kiểm tra định kỳ này; không có thì lấy lớp học sinh đang học.
  select ca.class_id into v_class
    from public.class_assessments ca
    where ca.exam_id = v_exam_id
    limit 1;
  if v_class is null then
    select uc.class_id into v_class
      from public.user_classes uc
      where uc.user_id = v_student
      limit 1;
  end if;

  insert into public.student_alerts
    (student_id, class_id, kind, severity, reason, status)
  values (
    v_student, v_class, 'exam_violation',
    case when v_count >= 6 then 'urgent' else 'warning' end,
    v_count || ' lần rời tab/thoát toàn màn hình khi làm bài "' || coalesce(v_title, '#' || v_exam_id)
      || '" — điểm có thể không phản ánh đúng thực lực, cần kiểm tra lại kiến thức.',
    'open'
  )
  on conflict (student_id, kind) do update set
    severity = excluded.severity,
    reason = excluded.reason,
    class_id = coalesce(excluded.class_id, student_alerts.class_id),
    status = case when student_alerts.status in ('resolved', 'dismissed')
                  then 'open' else student_alerts.status end,
    handled_note = case when student_alerts.status in ('resolved', 'dismissed')
                  then '' else student_alerts.handled_note end;
end;
$$;

-- Gắn thêm vào trigger nộp bài đã có sẵn (exam-analytics.sql) — không tạo trigger mới.
create or replace function public.trg_exam_result_alert()
returns trigger language plpgsql security definer set search_path = public
as $$
begin
  perform public.evaluate_student_alerts(new.student_id);
  perform public.evaluate_exam_violation_alert(new.id);
  return new;
end;
$$;
