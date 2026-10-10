#!/usr/bin/env bash
# Xem trước việc thu hồi RP vượt (KHÔNG ghi): chạy migration 20261010410000 trong giao dịch rồi ROLLBACK.
# In tóm tắt + 40 dòng đầu.
set -euo pipefail
cd "$(dirname "$0")/.."
T=$(mktemp -t xemtruoc).sql
{ echo "begin;"; cat supabase/migrations/20261010410000_rank_thu_hoi_rp_vuot.sql
  echo "select b.note, b.awarded as cu, b.new_awarded as moi, left(b.student_id::text, 8) as em, b.source_ref as tuan from public.rank_rp_awards_backup_20261010 b order by b.awarded - b.new_awarded desc limit 40;"
  echo "rollback;"; } > "$T"
supabase db query --linked -f "$T"
echo "(đã rollback — chưa ghi gì)"
