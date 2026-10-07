-- Supabase cảnh báo CRITICAL rls_disabled_in_public (3/10/2026): 7 bảng sao lưu do các đợt dọn dữ liệu tạo ra
-- không bật RLS nên anon (khoá công khai) đọc/ghi/xoá được. Bật RLS, không tạo policy => anon/authenticated bị chặn hoàn toàn;
-- service_role và postgres (migration, script *.mts) vẫn bypass RLS nên không ảnh hưởng gì tới việc khôi phục.
-- Thu thêm quyền của anon/authenticated cho chắc (phòng thủ nhiều lớp).

alter table public.question_bank_backup_20260930          enable row level security;
alter table public.question_bank_dedup_backup_20261006    enable row level security;
alter table public.question_bank_dedup_backup_20261006b   enable row level security;
alter table public.question_bank_dedup_backup_20261006c   enable row level security;
alter table public.question_bank_grade_fix_20261004       enable row level security;
alter table public.rank_fix_attempts_backup_20260930      enable row level security;
alter table public.tutoring_exit_attempts_backup_20260930 enable row level security;

revoke all on public.question_bank_backup_20260930          from anon, authenticated;
revoke all on public.question_bank_dedup_backup_20261006    from anon, authenticated;
revoke all on public.question_bank_dedup_backup_20261006b   from anon, authenticated;
revoke all on public.question_bank_dedup_backup_20261006c   from anon, authenticated;
revoke all on public.question_bank_grade_fix_20261004       from anon, authenticated;
revoke all on public.rank_fix_attempts_backup_20260930      from anon, authenticated;
revoke all on public.tutoring_exit_attempts_backup_20260930 from anon, authenticated;

-- ROLLBACK (không nên dùng — sẽ mở lại lỗ hổng):
-- alter table public.<bảng> disable row level security;
-- grant all on public.<bảng> to anon, authenticated;
