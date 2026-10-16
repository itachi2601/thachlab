# Nguồn video ưu tiên cho khái niệm TRỪU TƯỢNG — Crash Course Physics (thầy chốt 16/10/2026)

Playlist: https://www.youtube.com/playlist?list=PL8dPuuaLjXtN0ge7yDk_UA0ldZJdhwkoV (47 tập, có phụ đề tiếng Việt ở ít nhất #17).
Dùng khi bài có đoạn lý thuyết khó hình dung (sóng, trường, thông lượng, dao động, nhiệt, cảm ứng, lượng tử…): **tìm ở đây TRƯỚC**, rồi mới tới `scripts/tim-clip-youtube.py`.

## Quy trình (đã chạy ở bài Giao thoa/Sóng dừng 16/10/2026)
1. Chọn tập theo bảng dưới → tải phụ đề: `python3 -m yt_dlp --skip-download --write-subs --write-auto-subs --sub-langs "vi.*,en.*" --sub-format vtt --extractor-args "youtube:player_client=android" -o "%(id)s" <url>` (429 ở track phụ thì vẫn dùng track đã tải được).
2. Đọc phụ đề, tìm ĐÚNG đoạn nói về khái niệm đang cần (đừng tin thời gian thầy/Claude nhớ; đối chiếu lời) → mốc `giay_bat_dau`/`giay_ket_thuc` ≤ 90 giây, cắt theo ranh câu.
3. Khai trong `content/thi-nghiem/video-theo-bai.json` (`vi_tri: truoc:/sau:<data-exp>`, `nhin_vao` ≤ 25 từ) hoặc field `video` của `tn-*.json`; chèn bằng `scripts/chen-video-thi-nghiem.mts --bai <slug> --apply`; đăng bài đã có trên web bằng `bash scripts/cap-nhat-ly-thuyet.sh <bundle.json> <lesson_id> --yes --chi-video`.
4. Nêu cho thầy chỗ video **khác thuật ngữ bài** (vd. tập 17 nói "chồng chất hai xung", KHÔNG nói "nguồn kết hợp"): bài vẫn phải tự dạy phần đó. Clip minh hoạ trực giác, không thay lý thuyết.
5. Chỉ nhúng/dẫn link (V1–V7, mục Bản quyền ở AGENTS.md); không tải lại đăng.

## Danh mục tập (id | gợi ý bài thachlab)
| # | id | Tên | Hợp với |
|---|---|---|---|
| 1 | ZM8ECpBuQYE | Motion in a Straight Line | L10 chuyển động thẳng |
| 5 | w3BhzYI6zXU | Vectors and 2D Motion | L10 tổng hợp vectơ, ném xiên |
| 6 | kKKM8Y-u7ds | Newton's Laws | L10 ba định luật Newton |
| 7 | fo_pmp5rtzo | Friction | L10 lực ma sát |
| 8 | bpFK2VCRHUs | Uniform Circular Motion | L10 chuyển động tròn, lực hướng tâm |
| 9 | 7gf6YpdvtE0 | Newtonian Gravity | L10 lực hấp dẫn |
| 10 | w4QFJb9a8vo | Work, Energy, and Power | L10 công, năng lượng, công suất |
| 11 | Y-QOfc2XqOk | Collisions | L10 động lượng, va chạm |
| 12–14 | fmXFWi-WfyU / b-HZ1SZPaQw / 9cbF9A6eQNA | Rotational Motion / Torque / Statics | L10 mômen lực, cân bằng |
| 15–16 | b5SqYuWT4-4 / fJefjG3xhW0 | Fluids at Rest / in Motion | áp suất chất lỏng |
| 17 | jxstE6A_CYQ | Simple Harmonic Motion | L11 dao động điều hoà |
| 18 | TfYCnOvNnFU | Traveling Waves | L11 mô tả sóng, phản xạ (5:13–5:58), chồng chất xung (6:02–6:35) — ĐÃ DÙNG ở bài 31, 32 |
| 19–20 | qV4lR9EWGlY / XDsk6tZX55g | Sound / Physics of Music | L11 sóng âm, sóng dừng trên dây/ống |
| 21–25 | 6BHbJ_gBOk0 / WOEvvHbc240 / tuSC0ObB-qY / 4i1MUWJoI0U / p1woKh2mdVQ | Temperature / Kinetic Theory & Phase / Heat / Thermodynamics / Engines | L12 khí lí tưởng, nhiệt, nguyên lí I–II |
| 26–28 | TFlVWf8JX4A / mdulzEfQXDE / ZrMltpK6iAw | Electric Charge / Fields / Voltage & Capacitors | L11 điện trường, tụ điện |
| 29–32 | HXOok3mfMLM / g-wjP1otQWI / -w-VTw0tQlE / vuCJP_5KOlI | Current / Resistors / Circuits / Kirchhoff | L11 dòng điện, mạch điện |
| 33–34 | s94suB5uLWw / 5fqwJyt4Lus | Magnetism / Ampère | L12 từ trường |
| 35–37 | pQp6bmJPU_0 / 9kgzA0Vd8S8 / Jveer7vhjGo | Induction / Power to home / AC | L12 cảm ứng điện từ, điện xoay chiều |
| 38 | K40lNL3KsJ4 | Maxwell's Equations | L12 sóng điện từ |
| 39–42 | Oh4m8Ees-3Q / IRBfpBPELmE / -ob7foUzXaY / SddBPTcmqOk | Geometric Optics / Light Is Waves / Spectra Interference / Optical Instruments | quang, giao thoa ánh sáng (khe Young) |
| 43–46 | AInCqm5nCzw / 7kb1VT0J3DE / qO_W70VegbQ / lUhJL7o6_cA | Relativity / Quantum 1–2 / Nuclear | L12 lượng tử ánh sáng, hạt nhân |
| 47 | VYxYuaDvdM0 | Astrophysics and Cosmology | CĐ Thiên văn HSG |
(#2–4 Derivatives/Integrals, #0 Preview: không dùng cho bài THPT.)
Ghi chú: bản tiếng Việt chỉ xác nhận có ở #17 (16/10/2026); các tập khác kiểm phụ đề `vi` bằng lệnh bước 1 trước khi hứa với thầy.
