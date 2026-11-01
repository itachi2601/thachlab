-- Đo clip bẫy phụ đạo (chặng C, docs/ANALYTICS-SETUP.md mục "Đo clip bẫy phụ đạo"). CHỈ ĐỌC, chỉ số gộp, không cột HS.
-- Chạy: (cd ~/Projects/thachlab && supabase db query --linked -f scripts/sql/do-clip-bay-phu-dao.sql -o table)
-- Sửa mốc D = ngày clip hiện trên web (deploy + kho có video.mp4). Cửa sổ: 14 ngày trước D / 14 ngày sau D.
-- Chỉ chạy khi đã đủ 14 ngày sau D (trước đó số "sau" thiếu, đừng so).
with p as (select timestamptz '2026-11-03 00:00+07' as d),
-- tầng bài (mục phụ đạo mở ở đây) và YCCĐ có clip
bai(topic_id) as (values (66), (67)),
ycd(topic_id) as (values (216), (217), (218), (233), (234)),
w as (
  select 'truoc' k, d - interval '14 days' a, d b from p
  union all select 'sau', d, d + interval '14 days' from p
),
-- 1) tỉ lệ thoát: mục còn mở lúc đầu cửa sổ hoặc mở trong cửa sổ → bao nhiêu % cleared trong cửa sổ
thoat as (
  select w.k, tn.topic_id, count(*) n_muc,
         count(*) filter (where tn.cleared_at >= w.a and tn.cleared_at < w.b) n_thoat
  from w join tutoring_needs tn on tn.topic_id in (select topic_id from bai)
  where tn.first_seen_at < w.b and (tn.cleared_at is null or tn.cleared_at >= w.a) and tn.status <> 'dismissed'
  group by 1, 2
),
-- 2) tự kiểm tra thoát phụ đạo: lượt đạt / lượt nộp
tu_kiem as (
  select w.k, ea.topic_id, count(*) n_luot, count(*) filter (where ea.passed) n_dat
  from w join tutoring_exit_attempts ea on ea.created_at >= w.a and ea.created_at < w.b
  where ea.topic_id in (select topic_id from bai) group by 1, 2
),
-- 3) tỉ lệ sai đúng YCCĐ có clip (kiểm tra + luyện tập)
sai as (
  select w.k, r.topic_id, count(*) n, round(100 - 100 * sum(r.earned) / nullif(sum(r.max), 0)) pct_sai
  from w join (
    select topic_id, earned, max, created_at from exam_question_results
    union all select topic_id, earned, max, created_at from practice_question_results
  ) r on r.created_at >= w.a and r.created_at < w.b
  where r.topic_id in (select topic_id from ycd) group by 1, 2
)
select 'thoat' chi_so, k, topic_id, n_muc n, round(100.0 * n_thoat / nullif(n_muc, 0)) pct from thoat
union all select 'tu_kiem_dat', k, topic_id, n_luot, round(100.0 * n_dat / nullif(n_luot, 0)) from tu_kiem
union all select 'pct_sai', k, topic_id, n, pct_sai from sai
order by 1, 3, 2 desc;
