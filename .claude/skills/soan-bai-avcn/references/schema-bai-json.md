# Schema `data/bai.json` của một chương AVCN

Mẫu đầy đủ: `content/lesson-samples/avcn-chapter-8-chipping-machining/data/bai.json`. Mọi chuỗi là HTML nhỏ (được phép
`<em> <strong> <b>`), không `<script>`, không `on*=`. Chỗ có nhiều ý → **mảng chuỗi**, mỗi phần tử một ý (script dựng thành
danh sách). Quiz: `dap` là chỉ số 0-based trong `lua_chon`; phản hồi không mở đầu bằng "Đúng."/"Chưa đúng." (script tự thêm);
`fb_no` là gợi ý cách nghĩ lại, **không lộ đáp án**.

| Khoá | Kiểu | Bắt buộc | Ghi chú |
|---|---|---|---|
| `meta.chapter` | int | ✓ | số chương; ảnh ở `public/assets/avcn/chapter-<n>/` |
| `meta.prefix` | str | ✓ | tiền tố id radio, `tl<n>`; tab Bài mẫu tự dùng `tl<n>m` |
| `meta.title_en`, `meta.title_vi` | str | ✓ | |
| `meta.minutes` | int | ✓ | ước lượng đọc (20–30) |
| `meta.doan_tieu_de`, `meta.doan_mo_dau`, `meta.them_nhan` | str | | tiêu đề/lời dẫn mục Đoán và nhãn hộp từ ⭐⭐ khi chương không nói về máy (mặc định = bản Chapter 8) |
| `meta.boi_canh` | obj | | Mở bài bằng bối cảnh (thay mục "bao nhiêu điểm"): `tieu_de` ≤8 chữ, `tinh_huong` 40–60 chữ ngôi "em" cảnh xưởng thật + 2–3 từ khoá trong `<strong>`, `viec_can_lam` 1 câu, `quay_lai` 1 câu hỏi cuối mục Trả bài. Không nhắc điểm/đề. Sinh bằng `npx tsx scripts/sinh-boi-canh-avcn.mts` rồi `--ap-dung` |
| `meta.muc_tieu` | str[] | ✓ | 3 mục tiêu đo được, gắn Part |
| `meta.de_thi` | [str,str,str][] | ✓ | 5 hàng: Part · điểm, đề hỏi gì, học ở mục nào |
| `khoi_dong` | obj[] (2) | ✓ | `{img, hoi, lua_chon[3], dap, fb_ok, fb_no}` — ảnh máy/dụng cụ quen ở xưởng |
| `tu_vung` | obj[] (4) | ✓ | mỗi cụm `{ten, tu[5], quiz}`; `tu[i] = {term, ipa, vi, def, img|null, tier:1}`; `def` là định nghĩa kiểu Part 1 (mệnh đề danh từ ≤ 15 từ); `quiz` dạng Part 1 (4 lựa chọn) |
| `tu_vung_them` | `{term, vi}[]` (≈12) | ✓ | từ ⭐⭐: bộ phận, từ mô tả; dùng cho mục gắn nhãn (`vi` tra theo `term`) |
| `bai_doc` | obj[] (1–3) | ✓ | mỗi Article `{ten, cau[[en, vi]...], quiz, dung_sai}`; `cau` chép **đúng câu giáo trình**, tách ≤ 25 từ/câu, từ ⭐ bọc `<b>`; `quiz` = điền-1-từ 3 lựa chọn; `dung_sai = {hoi, dap:bool, fb_ok, fb_no}`; mỗi câu nên có phần tử thứ 3 `{doan:[{tu, lua_chon[3], dap, giai}] (≤2, từ ⭐/từ thi, bọc `<b>` trong câu), nghia:{từ thường: nghĩa}}` → đố trắc nghiệm rồi chạm xem nghĩa (từ 16/10/2026); câu thiếu phần tử 3 dùng cách cũ: `tu_khoa` (tuỳ chọn) `{từ in đậm: nghĩa}` cho hộp "Đoán nghĩa trước khi đọc" khi nghĩa khác mục Từ vựng (vd Milling = phay, không phải máy phay) |
| `mau_cau` | obj[] (2) | ✓ | `{ten, vd[[en, vi]×3], ghi_chu: str[]}` — chỉ mẫu câu xuất hiện trong Part 4–5 của chương |
| `bang` | obj | | bảng so sánh cuối mục Bài đọc `{ten, cot[], hang[][]}`; thiếu thì dùng bảng 5 phương pháp của Chapter 8. Ở 375 px giữ ≤ 2–3 cột ngắn, ý thứ hai xuống dòng bằng `<br>` (cột hẹp bẻ chữ giữa từ) |
| `gan_nhan` | obj | ✓ | quiz về một bộ phận của hình gắn nhãn. Chương có SVG riêng (chỉ số, không tên): thêm `svg` (tên file trong `public/assets/avcn/chapter-<n>/`), `bo_phan [[term, vi]…]`, `tieu_de`, `mo_ta`, `chu_thich`; thiếu `svg` thì dùng hình máy tiện Chapter 8 |
| `sop` | obj | ✓ | `{hop_tu[5], doan (có "(1) ______"…), dap[5], quiz, tieu_de?, mo_ta?}` — đoạn điền từ kiểu Part 3 lấy từ Vocabulary/Reading của chương, viết lại bằng lời mình |
| `tra_bai` | [hoi, dap][] (6–8) | ✓ | câu hỏi gọi lại, có 1 câu dịch xuôi + 1 câu dịch ngược |
| `de_mau.part1` | obj[] (6) | ✓ | `{q, opts[4], ans, why, img?}`; 1 câu "Look at the picture…" có `img` (khoá ảnh trong credits.json) — không ghi `[hình: …]` vào `q` vì lộ đáp án |
| `de_mau.part1_chien_thuat`, `part2_chien_thuat` | str[] | ✓ | mỗi ý một dòng |
| `de_mau.part2` | obj | ✓ | `{doan, dien:[{q, ans, opts[3], why}×4], ds:[{q, ans:bool, why}×4]}` — `doan` là đoạn Article; `opts` chứa `ans` |
| `de_mau.part3` | obj | ✓ | `{hop_tu[5], doan, dap[5], chien_thuat: str[]}` — `dap[i]` ∈ `hop_tu` |
| `de_mau.part4` | obj | ✓ | `{en, vi, chien_thuat: str[]}` |
| `de_mau.part5` | obj | ✓ | `{vi, en, chien_thuat: str[]}` |
| `luyen_tap.mc` | obj[] (20) | ✓ | `{q, opts[4], ans, why}` — 14 định nghĩa → từ, 3 bộ phận, 3 điền từ từ Article |
| `luyen_tap.tf` | obj[] (3) | ✓ | `{q, st:[[text, bool]×4], why}` — mỗi câu bám một đoạn Article |

Khoá ảnh `img` phải có trong `public/assets/avcn/chapter-<n>/credits.json`; `null` = thẻ không ảnh (chiếm cả hàng).
