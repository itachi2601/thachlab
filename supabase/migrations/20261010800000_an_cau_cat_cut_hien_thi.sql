-- Ẩn 181 câu ngân hàng còn sót lỗi cắt cụt / hiển thị sau đợt de_hong 9/10: phương án rỗng hoặc dính tab,
-- phương án A–D nằm lẫn trong đề, đề thiếu giá trị (công thức/ký hiệu bị rơi), dấu $ lẻ.
-- Nguồn: scripts/quet-cau-cat-cut-ngan-hang.mts (chỉ đọc), id ở scripts/data/cau-cat-cut-hien-thi-ids-20261010.json.
-- Chỉ đặt archived = true cho câu đang hiện; KHÔNG sửa nội dung, KHÔNG đụng exams.questions (đề đã đăng giữ nguyên).
-- Sao lưu trạng thái cũ ra question_bank_cat_cut_20261010 để hoàn tác.

create table if not exists public.question_bank_cat_cut_20261010 as
select id, archived, note
from public.question_bank
where id in (
    88, 477, 479, 480, 2746, 7123, 7142, 8169, 13319, 13822, 13823, 13824, 283015, 295090,
    332117, 381169, 383265, 392996, 395087, 406021, 408551, 412122, 415496, 424912, 431965, 453054, 453376, 453557,
    453953, 454057, 455006, 455405, 456572, 456849, 456852, 456853, 457083, 458002, 458570, 570382, 570395, 575939,
    579723, 579732, 587103, 589489, 614439, 627227, 633140, 647475, 655609, 655615, 658407, 658427, 665130, 673707,
    673720, 673980, 674230, 674762, 674766, 674770, 680710, 680712, 680727, 680855, 681158, 681170, 681433, 681659,
    681751, 681891, 681892, 682034, 682128, 682133, 682317, 682419, 682567, 682578, 682582, 682584, 682608, 682625,
    682672, 682806, 683014, 683060, 683448, 683451, 683473, 683562, 683573, 683575, 683579, 683580, 683602, 683622,
    683624, 683636, 683642, 683663, 683699, 683700, 683749, 683899, 683923, 684212, 684235, 684239, 684362, 684606,
    684657, 685081, 685084, 685166, 685212, 685280, 685282, 685426, 685477, 685479, 685702, 685730, 685740, 685745,
    685746, 685747, 685751, 685758, 685827, 685846, 686042, 686209, 686251, 686266, 1151142, 1151149, 1151154, 1151156,
    1153662, 1153667, 1159267, 1159917, 1161663, 1161896, 1162743, 1163858, 1163872, 1170281, 1184559, 1184560, 1184561, 1184866,
    1186044, 1195685, 1227135, 1229407, 1236320, 1238739, 1238742, 1241977, 1241979, 1241991, 1241993, 1244271, 1244359, 1246835,
    1246840, 1247474, 1248658, 1250161, 1255005, 1342461, 1345582, 1345596, 1345598, 1345602, 1345603, 1348464, 1348466
)
and archived = false;

alter table public.question_bank_cat_cut_20261010 enable row level security;
revoke all on public.question_bank_cat_cut_20261010 from anon, authenticated;

update public.question_bank q
set archived = true,
    note = case when q.note is null or q.note = '' then '[audit 10/2026: cat_cut]'
                else q.note || ' [audit 10/2026: cat_cut]' end,
    updated_at = now()
from public.question_bank_cat_cut_20261010 b
where q.id = b.id;

-- ROLLBACK (chạy tay nếu cần):
-- update public.question_bank q set archived = b.archived, note = b.note
--   from public.question_bank_cat_cut_20261010 b where q.id = b.id;
-- drop table public.question_bank_cat_cut_20261010;
