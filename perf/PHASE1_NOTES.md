# Sau Pha 1 (main 22e62071, merge perf/assets → perf/bundle → perf/db-index)
Lighthouse desktop (serve tĩnh localhost, không gzip):
| Trang | Score | FCP | LCP | JS | Ảnh | Font | Google req | Supabase req | JS không dùng |
| / | 68→91 | 2.0→0.8s | 4.0→1.9s | 1600→1313KB | 4618→589KB | 15→17 (self-host) | 0 | 0 | 961→838KB |
| /lop-hoc/bai?id=2 | 78→83 | 0.9→0.6s | 3.8→3.1s | 1690→1547KB | 1354→669KB | 12→16 | 0 | 10 | 1034→893KB |
| /kiem-tra/lam?id=118 | 90→90 | 0.9→0.7s | 1.9→2.0s | 1693→1550KB | 0 | 7→14 | 0 | 0 | 1096→956KB |
out/ 41→32 MB; chunks 10.0→9.6 MB; /dashboard 2430→929 KB; /dashboard-thpt 1724→920 KB; / 1058→918; /lop-hoc 1387→952; /quan-tri/dang-de 1311→1024.
Smoke test (trình duyệt): trang chủ + con lắc OK, /lop-hoc OK, /lop-hoc/bai?id=2 ảnh+KaTeX OK, không lỗi console. Trang làm đề/gradebook/quan-tri cần đăng nhập — chưa test.
Migration chờ thầy: supabase/migrations/20260925120000_perf_indexes.sql (7 index).
Cần thầy quyết (Agent B): 2 policy tautology attendance_sessions / equipment_breakdown_reports; class_assessments = true; drop question_bank_grade_idx sau khi theo dõi.
