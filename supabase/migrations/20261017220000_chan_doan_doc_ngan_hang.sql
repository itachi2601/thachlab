-- ============================================================================
-- 17/10/2026 — Kiểm tra đầu vào báo "Ngân hàng câu hỏi chưa có câu nào cho các bài này".
-- Nguyên nhân: học sinh chỉ đọc được question_bank qua policy "student reads exit-quiz bank questions",
-- policy đó đòi em đã có mục phụ đạo mở cho bài. Em vào trễ chưa làm chẩn đoán thì chưa có mục nào
-- (đó chính là thứ bài chẩn đoán sẽ mở) → RLS trả rỗng dù ngân hàng có ~2400 câu cho các bài 38–45.
-- Sửa: thêm policy SELECT riêng: em đọc được câu (không lưu trữ) thuộc các bài cần bù / đã bù trong đăng ký
-- joined_late của mình (kể cả yêu cầu cần đạt con), CHỈ khi chưa nộp chẩn đoán (diagnostic_reset xoá dòng
-- entry_diagnostics nên "Cho làm lại" vẫn mở lại được). Không đổi bảng/dữ liệu.
-- Cách chạy: bash scripts/run-migrations.sh --yes --only N (lúc nào cũng chạy được).
-- Rollback: cuối file.
-- ============================================================================

begin;

-- Danh sách bài em đang được phép đọc câu để làm chẩn đoán (rỗng nếu đã nộp hoặc không vào trễ).
-- security definer để policy không phụ thuộc RLS của thpt_registrations/entry_diagnostics.
create or replace function public.diagnostic_bank_topic_ids()
returns bigint[]
language sql stable security definer set search_path = public
as $$
  select coalesce(array_agg(distinct x), '{}')
  from (
    select unnest(r.catchup_topic_ids || r.catchup_done_topic_ids) as x
    from public.thpt_registrations r
    where r.student_id = auth.uid()
      and r.joined_late
      and r.status in ('catchup', 'active')
      and not exists (select 1 from public.entry_diagnostics d where d.student_id = auth.uid())
  ) s;
$$;
revoke all on function public.diagnostic_bank_topic_ids() from public, anon;
grant execute on function public.diagnostic_bank_topic_ids() to authenticated;

drop policy if exists "student reads entry-diagnostic bank questions" on public.question_bank;
create policy "student reads entry-diagnostic bank questions" on public.question_bank
  as permissive
  for select
  to authenticated
  using (
    archived = false
    and (
      topic_id in (select unnest(public.diagnostic_bank_topic_ids()))
      or exists (
        select 1 from public.question_topics t
        where t.id = question_bank.topic_id and t.parent_id in (select unnest(public.diagnostic_bank_topic_ids()))
      )
    )
  );

commit;

-- ---------------------------------------------------------------------------
-- Rollback:
-- begin;
-- drop policy if exists "student reads entry-diagnostic bank questions" on public.question_bank;
-- drop function if exists public.diagnostic_bank_topic_ids();
-- commit;
