-- ============================================================================
-- Bảng ghi phỏng vấn HS do trợ giảng làm (thầy chốt 16/10/2026) — bước Thấu cảm của Design Thinking
-- Vấn đề: kênh tự thoát phụ đạo gần như không dùng (docs/ROADMAP.md "Vấn đề gốc đã chốt").
-- Trợ giảng hỏi trực tiếp 3 em theo docs/PHIEU-PHONG-VAN-PHU-DAO-2026-10-16.md rồi ghi nguyên văn câu trả lời ở /tro-giang/phong-van.
-- KHÔNG lưu tên/id học sinh — chỉ mã E1..E3 + nhóm; câu trả lời là văn bản tự do nên nhắc TA không ghi tên em.
-- Thêm: bảng ta_interviews (RLS bật, không ai đọc/ghi trực tiếp), hàm ta_interview_save / ta_interview_list.
-- Không đổi dữ liệu cũ. Cách chạy: bash scripts/run-migrations.sh --yes --only N — lúc nào cũng được.
-- Rollback: perf/rollback/20261016120000_ta_phong_van_phu_dao.down.sql
-- ============================================================================

create table if not exists public.ta_interviews (
  id uuid primary key default gen_random_uuid(),
  assistant_id uuid not null references public.ta_assistants (id) on delete cascade,
  code text not null check (code ~ '^[A-Za-z][0-9]{1,2}$'),
  grp text not null check (grp in ('chua_mo', 'bo_truot', 'da_thoat', 'khac')),
  answers jsonb not null default '{}'::jsonb,
  barrier text,
  wish text,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  unique (assistant_id, code)
);
alter table public.ta_interviews enable row level security;
revoke all on public.ta_interviews from anon, authenticated;

-- Lưu (tạo hoặc ghi đè) một phiếu của chính trợ giảng đang đăng nhập; mỗi TA mỗi mã một phiếu.
create or replace function public.ta_interview_save(p_code text, p_grp text, p_answers jsonb, p_barrier text, p_wish text)
returns uuid
language plpgsql security definer set search_path = public
as $$
declare
  v_ta uuid;
  v_id uuid;
begin
  select id into v_ta from public.ta_assistants where user_id = auth.uid() and active;
  if v_ta is null then
    raise exception 'Không phải trợ giảng' using errcode = '42501';
  end if;
  if coalesce(jsonb_typeof(p_answers), '') <> 'object' or octet_length(p_answers::text) > 20000 then
    raise exception 'Dữ liệu không hợp lệ';
  end if;
  insert into public.ta_interviews (assistant_id, code, grp, answers, barrier, wish)
  values (v_ta, upper(trim(p_code)), p_grp, p_answers, left(p_barrier, 2000), left(p_wish, 2000))
  on conflict (assistant_id, code) do update
    set grp = excluded.grp, answers = excluded.answers, barrier = excluded.barrier, wish = excluded.wish, updated_at = now()
  returning id into v_id;
  return v_id;
end;
$$;
revoke all on function public.ta_interview_save(text, text, jsonb, text, text) from public, anon;
grant execute on function public.ta_interview_save(text, text, jsonb, text, text) to authenticated;

-- Trợ giảng thấy phiếu của mình; admin thấy tất cả (kèm tên trợ giảng).
create or replace function public.ta_interview_list()
returns jsonb
language plpgsql stable security definer set search_path = public
as $$
declare
  v_ta uuid;
  v_admin boolean := public.is_admin();
begin
  select id into v_ta from public.ta_assistants where user_id = auth.uid() and active;
  if v_ta is null and not v_admin then
    raise exception 'Không có quyền' using errcode = '42501';
  end if;
  return coalesce((
    select jsonb_agg(jsonb_build_object(
      'id', i.id, 'code', i.code, 'grp', i.grp, 'answers', i.answers, 'barrier', i.barrier, 'wish', i.wish,
      'by', coalesce(nullif(a.short_name, ''), a.full_name), 'updated_at', i.updated_at)
      order by i.code, i.updated_at desc)
    from public.ta_interviews i join public.ta_assistants a on a.id = i.assistant_id
    where v_admin or i.assistant_id = v_ta
  ), '[]'::jsonb);
end;
$$;
revoke all on function public.ta_interview_list() from public, anon;
grant execute on function public.ta_interview_list() to authenticated;
