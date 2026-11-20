-- Tỉ lệ theo từng khung video thí nghiệm (tn_id, ban_clip) — CHỈ ĐỌC.
-- Nguồn: public.lesson_clip_views (migration 20261120120000_lesson_clip_views, Việc 6).
-- Chạy: supabase db query --linked -f scripts/sql/ty-le-clip-thi-nghiem.sql   (cần quyền admin/postgres)
-- Quy ước: % đúng tính trên số lượt ĐÃ CHỌN; % bỏ qua trên số lượt TỚI điểm dừng (chọn + bỏ qua) — lượt rời đi trước
-- điểm dừng hay phát lại sau khi đã trả lời không vào mẫu số; % xem hết bỏ lượt chỉ bấm phát rồi thoát (giay_max < 3);
-- câu chốt chỉ tính ở lượt có co_cau_chot. ban_clip khác nhau = clip cũ / clip dựng lại → so hai bản cạnh nhau.

-- ---------- 1. Mọi lượt xem ----------
select v.tn_id, v.ban_clip,
       count(*)                                                     as so_luot,
       count(distinct v.student_id)                                 as so_hs,
       round(100.0 * count(*) filter (where v.du_doan_dung) / nullif(count(v.du_doan), 0), 1)            as pt_dung_du_doan,
       round(100.0 * count(*) filter (where v.du_doan_bo_qua)
             / nullif(count(*) filter (where v.du_doan is not null or v.du_doan_bo_qua), 0), 1)          as pt_bo_qua_du_doan,
       round(100.0 * count(*) filter (where v.co_cau_chot and v.chot_dung)
             / nullif(count(*) filter (where v.co_cau_chot and v.chot is not null), 0), 1)               as pt_dung_chot,
       round(100.0 * count(*) filter (where v.co_cau_chot and v.chot_bo_qua)
             / nullif(count(*) filter (where v.co_cau_chot and (v.chot is not null or v.chot_bo_qua)), 0), 1)  as pt_bo_qua_chot,
       round(100.0 * count(*) filter (where v.xem_het) / nullif(count(*) filter (where v.giay_max >= 3), 0), 1) as pt_xem_het,
       round(avg(v.so_xem_lai), 1)                                  as tb_xem_lai,
       min(v.bat_dau)::date as tu_ngay, max(v.bat_dau)::date as den_ngay
from public.lesson_clip_views v
group by v.tn_id, v.ban_clip
order by v.tn_id, v.ban_clip;

-- ---------- 2. Chỉ LƯỢT ĐẦU của mỗi HS mỗi clip (lượt sau đã biết đáp án) ----------
with dau as (
  select distinct on (v.student_id, v.tn_id, v.ban_clip) v.*
  from public.lesson_clip_views v
  order by v.student_id, v.tn_id, v.ban_clip, v.bat_dau
)
select d.tn_id, d.ban_clip,
       count(*)                                                     as so_hs_luot_dau,
       round(100.0 * count(*) filter (where d.du_doan_dung) / nullif(count(d.du_doan), 0), 1)            as pt_dung_du_doan,
       round(100.0 * count(*) filter (where d.du_doan_bo_qua)
             / nullif(count(*) filter (where d.du_doan is not null or d.du_doan_bo_qua), 0), 1)          as pt_bo_qua_du_doan,
       round(100.0 * count(*) filter (where d.co_cau_chot and d.chot_dung)
             / nullif(count(*) filter (where d.co_cau_chot and d.chot is not null), 0), 1)               as pt_dung_chot,
       round(100.0 * count(*) filter (where d.co_cau_chot and d.chot_bo_qua)
             / nullif(count(*) filter (where d.co_cau_chot and (d.chot is not null or d.chot_bo_qua)), 0), 1)  as pt_bo_qua_chot,
       round(100.0 * count(*) filter (where d.xem_het) / nullif(count(*) filter (where d.giay_max >= 3), 0), 1) as pt_xem_het,
       round(avg(d.so_xem_lai), 1)                                  as tb_xem_lai
from dau d
group by d.tn_id, d.ban_clip
order by d.tn_id, d.ban_clip;

-- ---------- 3. (Tuỳ) Dữ liệu > 12 tháng đã cộng dồn ở lesson_clip_view_rollups ----------
-- Không có "lượt đầu" (đã gộp); so_hs cộng qua các tháng nên có thể đếm trùng một HS ở nhiều tháng.
-- select r.tn_id, r.ban_clip, sum(r.so_luot) so_luot, sum(r.so_hs) so_hs_cong_thang,
--        round(100.0 * sum(r.du_doan_dung) / nullif(sum(r.du_doan_tra_loi), 0), 1) pt_dung_du_doan,
--        round(100.0 * sum(r.du_doan_bo_qua) / nullif(sum(r.so_luot), 0), 1)       pt_bo_qua_du_doan,
--        round(100.0 * sum(r.chot_dung) / nullif(sum(r.chot_tra_loi), 0), 1)       pt_dung_chot,
--        round(100.0 * sum(r.chot_bo_qua) / nullif(sum(r.chot_co), 0), 1)          pt_bo_qua_chot,
--        round(100.0 * sum(r.xem_het) / nullif(sum(r.so_luot), 0), 1)              pt_xem_het
-- from public.lesson_clip_view_rollups r
-- group by r.tn_id, r.ban_clip order by 1, 2;
