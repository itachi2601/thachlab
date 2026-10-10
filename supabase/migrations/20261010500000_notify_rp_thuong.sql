-- ============================================================================
-- 10/10/2026 — Báo qua chuông khi em được cộng RP thưởng (mục tiêu tuần · tiến bộ tuần · mục tiêu cả lớp)
--
-- Trước đây ba khoản này cộng âm thầm, em chỉ thấy khi mở lịch sử RP. Một trigger duy nhất trên rank_rp_ledger
-- (AFTER INSERT, amount > 0, source_kind in weekly_goal / progress_week / class_goal) gửi một thông báo chuông
-- tới em (+ phụ huynh đã nối, giống thông báo "đã chấm bài tập về nhà"), bấm vào tới /lop-hoc/xep-hang.
-- KHÔNG báo: luyện tập/sửa sai/chuỗi ngày/lý thuyết (đã có báo ngay tại màn hình), bài tập về nhà (homework_check_set đã tự
-- gửi "+N RP"), dòng điều chỉnh âm. Lỗi trong phần báo chỉ bị nuốt, không bao giờ làm hỏng việc cộng RP.
-- Không gửi bù cho RP đã cộng trước đây. Chỉ thêm hàm + trigger mới.
-- Cách chạy: bash scripts/run-migrations.sh — giờ nào cũng được.
-- Rollback: perf/rollback/20261010500000_notify_rp_thuong.down.sql
-- ============================================================================

create or replace function public.trg_notify_rp_bonus()
returns trigger
language plpgsql security definer set search_path = public
as $$
declare
  v_title text;
begin
  if new.amount <= 0 or new.source_kind not in ('weekly_goal', 'progress_week', 'class_goal') then
    return new;
  end if;
  v_title := '+' || new.amount || ' RP · ' || case new.source_kind
    when 'weekly_goal' then 'Đạt mục tiêu tuần'
    when 'progress_week' then 'Tiến bộ so với 2 tuần trước'
    else 'Cả lớp đạt mục tiêu tuần'
  end;
  begin
    perform public.notify_student_side(new.student_id, 'rp_bonus', v_title, left(coalesce(new.reason, ''), 200),
      '/lop-hoc/xep-hang', '/phu-huynh');
  exception when others then
    raise warning 'trg_notify_rp_bonus: %', sqlerrm;
  end;
  return new;
end; $$;

drop trigger if exists trg_notify_rp_bonus on public.rank_rp_ledger;
create trigger trg_notify_rp_bonus
  after insert on public.rank_rp_ledger
  for each row execute function public.trg_notify_rp_bonus();
