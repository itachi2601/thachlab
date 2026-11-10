-- Đo "💡 Mẹo nhìn" (chặng 5, docs/KE-HOACH-MEO-GIAI-BAI-TAP.md): tỉ lệ đúng ở "Làm bài tương tự"
-- của dạng CÓ mẹo so với dạng CHƯA có mẹo cùng chương. Nơi gắn mẹo: docs/BANG-MEO-GIAI.md.
-- Chạy: supabase db query --linked -f scripts/sql/do-meo-nhin.sql
-- Chỉ tính lượt 1 (lần đầu thật trong một lần mở trang) và câu đúng dạng (nguon='dang'); bỏ tài khoản thầy/TA/thử.
-- Mỗi câu chỉ được chấm một lần (đáp án lúc bấm Chấm, chưa xem đáp án đúng) nên dung_lan_dau = số câu đúng lần chấm đầu.
-- Mốc bắt đầu đo = ngày deploy (dòng created_at bên dưới).
with base as (
  select a.*, l.chapter_id, l.title as bai
  from similar_practice_attempts a
  join lessons l on l.id = a.lesson_id
  join profiles p on p.id = a.user_id
  where a.luot = 1
    and a.nguon = 'dang'
    and coalesce(p.role, '') not in ('admin', 'instructor', 'tro_giang', 'ta', 'parent')
    and not coalesce(p.is_test, false)
    and a.created_at >= date '2026-11-05'
),
-- Chương có ít nhất một dạng mang mẹo
chuong_co_meo as (select distinct chapter_id from base where co_meo)
-- 1) Từng dạng có mẹo: số lượt, % mở mẹo, tỉ lệ đúng (chia theo mở/không mở mẹo)
select 'A. dạng có mẹo' as nhom, b.chapter_id, b.lesson_id, b.bai, b.dang_no,
       count(*) as so_luot,
       count(distinct b.user_id) as so_hs,
       round(100.0 * avg(b.mo_meo::int), 1) as pct_mo_meo,
       round(100.0 * sum(b.dung_lan_dau) / nullif(sum(b.tong), 0), 1) as pct_dung,
       round(100.0 * sum(b.dung_lan_dau) filter (where b.mo_meo) / nullif(sum(b.tong) filter (where b.mo_meo), 0), 1) as pct_dung_co_mo,
       round(100.0 * sum(b.dung_lan_dau) filter (where not b.mo_meo) / nullif(sum(b.tong) filter (where not b.mo_meo), 0), 1) as pct_dung_khong_mo
from base b
where b.co_meo
group by b.chapter_id, b.lesson_id, b.bai, b.dang_no

union all

-- 2) Đối chứng: các dạng CHƯA có mẹo trong cùng chương, gộp theo chương
select 'B. dạng chưa có mẹo (cùng chương)', b.chapter_id, null, null, null,
       count(*), count(distinct b.user_id), null,
       round(100.0 * sum(b.dung_lan_dau) / nullif(sum(b.tong), 0), 1), null, null
from base b
where not b.co_meo and b.chapter_id in (select chapter_id from chuong_co_meo)
group by b.chapter_id

order by chapter_id, nhom, lesson_id, dang_no;
