-- DT-04 (docs/thachlab-design-thinking-audit.md): thử lịch ôn câu sai 1 → 3 → 7 ngày trên lớp được bật cờ 'on_tap_1_3_7'
-- (bảng feature_flags, 20261017231000). Lớp không có cờ giữ nguyên lịch cũ 2 → 4 → 7 ngày, xoá bẫy sau 2 lần đúng.
--
--                          lớp mặc định (không đổi)     lớp có cờ on_tap_1_3_7
--   mới sai / ôn sai       stage 0, +2 ngày             stage 0, +1 ngày
--   ôn đúng lần 1          stage 1, +4 ngày             stage 1, +3 ngày
--   ôn đúng lần 2          stage 2, cleared, +7 ngày    stage 2, +7 ngày, CHƯA cleared
--   ôn đúng lần 3          —                            stage 3, cleared, +7 ngày
--
-- Cách làm: trigger BEFORE INSERT/UPDATE trên student_mistakes chỉ chỉnh dòng của HS thuộc lớp có cờ; không đụng
-- mistake_review_quiz_submit / trigger gom câu sai nên hàng lớp mặc định không đổi một byte. Lưu ý khi so sánh hai
-- lớp: lớp có cờ cần 3 lần đúng để xoá bẫy (nhiều lần ôn hơn, nhiều RP ôn hơn, trần RP/ngày vẫn như cũ).
-- Bật:  insert into feature_flags (flag, class_id, note) values ('on_tap_1_3_7', <class_id>, 'thử 1/3/7');
-- Tắt:  update feature_flags set enabled = false where flag = 'on_tap_1_3_7' and class_id = <class_id>;
-- Rollback ở cuối file.

create or replace function public.mistake_spaced_137(p_student uuid)
returns boolean
language sql stable security definer set search_path = public
as $$
  select exists (
    select 1
    from public.feature_flags f
    join public.user_classes uc on uc.class_id = f.class_id
    where f.flag = 'on_tap_1_3_7' and f.enabled
      and uc.user_id = p_student and uc.status = 'active'
  );
$$;
revoke all on function public.mistake_spaced_137(uuid) from public, anon, authenticated;

create or replace function public.trg_mistake_lich_137()
returns trigger
language plpgsql security definer set search_path = public
as $$
begin
  if not public.mistake_spaced_137(new.student_id) then
    return new;
  end if;

  if new.stage = 0 and not new.cleared then
    new.next_review_at := greatest(new.last_wrong_at, coalesce(new.last_reviewed_at, new.last_wrong_at)) + interval '1 day';
  elsif tg_op = 'UPDATE' and new.stage > old.stage then
    new.cleared := new.stage >= 3;
    new.next_review_at := coalesce(new.last_reviewed_at, now())
      + case new.stage when 1 then interval '3 days' else interval '7 days' end;
  end if;
  return new;
end;
$$;
revoke all on function public.trg_mistake_lich_137() from public, anon, authenticated;

drop trigger if exists trg_mistake_lich_137 on public.student_mistakes;
create trigger trg_mistake_lich_137
  before insert or update on public.student_mistakes
  for each row execute function public.trg_mistake_lich_137();

-- ---------- ROLLBACK ----------
-- drop trigger if exists trg_mistake_lich_137 on public.student_mistakes;
-- drop function if exists public.trg_mistake_lich_137();
-- drop function if exists public.mistake_spaced_137(uuid);
-- (dòng student_mistakes đã ghi theo lịch 1/3/7 giữ nguyên; stage >= 2 chưa cleared sẽ cần thêm 1 lần đúng — đủ nhỏ để bỏ qua)
