# Brief soạn (agent A/B/C/D) đợt 4 — đọc sau `_brief-dot4.md`

Ký hiệu: `<cd>` = thư mục CĐ (`content/hsg9/<cd>/`), `<id>` = lesson_id. Dàn ý + số liệu đã chốt: `content/hsg9/<cd>/nguon.md`
(+ `tinh.py`). DÙNG NGUYÊN số liệu, ký hiệu, cấp độ từng dạng trong nguon.md; không tự đổi đề, không tự nâng/giảm cấp.
Thấy số trong nguon.md sai → không tự sửa nguon.md, ghi rõ vào câu trả lời cuối (dòng "NGHI SAI: …").

## Agent A — Lý thuyết
- Theo skill `.claude/skills/soan-bai-ly-thuyet-tuong-tac/SKILL.md` (đọc SKILL.md + chỉ phần reference cần), rút gọn theo
  `docs/PHUONG-PHAP-NOI-DUNG-LY-THUYET.md`. Mẫu cấu trúc + CSS/khối tương tác: `content/hsg9/cd12-nhiet-hoc/theory.src.html`, `build_figs.py`.
- Ghi: `content/hsg9/<cd>/theory.src.html`, `build_figs.py` (hình SVG, thay `<!--FIGn-->`) → chạy ra `theory.html`. Quiz cuối bài tự chấm.
- Chạy thử: `python3 content/hsg9/<cd>/build_figs.py`; render 375px bằng Chrome headless trong scratch riêng, tự xem ảnh, sửa tràn/chữ nhỏ.

## Agent B — Bài tập mẫu Dạng 1–3 · Agent C — Dạng 4 trở đi
- Theo skill `.claude/skills/soan-bai-tap-mau/SKILL.md` (buoc[] tự giải từng bước, bảng phân tích đề, mô phỏng dưới đề, lời giải phong cách thầy).
- Mẫu: `scripts/data/bai-tap-mau/btm153_d123.py`, `btm153_d456.py`, `build-hinh-153.py`. Mỗi module xuất DANG, BUILD, ANALYSIS, SOLS, STEPS, kiem_so (assert số liệu).
- B ghi `scripts/data/bai-tap-mau/btm<id>_d123.py`; C ghi `btm<id>_d456.py` (dạng 4..hết, kể cả dạng 7 nếu có — tên module giữ `d456`).
- Agent B tạo thêm `build-hinh-<id>.py` (sao từ build-hinh-153.py, đổi 153→<id>, BTM<id>_ONLY/BTM<id>_OUT). C và D KHÔNG ghi file này.
- Chạy thử riêng: `BTM<id>_ONLY=btm<id>_d123 BTM<id>_OUT=<scratch>/x.json python3 scripts/data/bai-tap-mau/build-hinh-<id>.py`
  (C dùng `_d456`); rồi validator của skill trên file scratch đó. KHÔNG ghi `scripts/data/bai-tap-mau/<id>.json` thật.
- topic "bài tương tự" lấy theo nguon.md mục YCCĐ (không có YCCĐ thì để như nguon.md ghi).

## Agent D — Tự luận + Luyện tập
- `scripts/data/bai-tap-mau/btm<id>_tl.py` có `tu_luan()` + `kiem_so()` (mẫu `btm153_tl.py`): các bài tự luận trong nguon.md, mỗi bài
  có Hướng dẫn giải trong <details>; soát ĐIỀU KIỆN PHỤ của đề (đề kín: đủ dữ kiện, giả thiết bỏ qua gì ghi rõ).
- `content/hsg9/<cd>/luyen-tap/sinh.py` → `bundle.json` (mẫu `content/hsg9/cd12-nhiet-hoc/luyen-tap/sinh.py`; `thachlab.lesson-bundle/v1`
  chỉ có exam, `theory_html` rỗng, `worked_examples: []`). Mỗi câu có topic/form, đúng một đáp án đã đối chiếu lời giải, mỗi phương án nhiễu
  do một cách sai cụ thể (`assert` khác đáp án đúng). Số liệu khác bài tập mẫu và khác thử thách trong lý thuyết.
- Chạy thử: `BTM<id>_ONLY=btm<id>_tl BTM<id>_OUT=<scratch>/x.json python3 scripts/data/bai-tap-mau/build-hinh-<id>.py` (khi B đã tạo
  build-hinh; chưa có thì tự import module chạy `tu_luan()` + `kiem_so()`), và `python3 content/hsg9/<cd>/luyen-tap/sinh.py`.

## Trả lời cuối (≤12 dòng)
File đã ghi · lệnh chạy thử đã pass · số dạng/bài/câu · "NGHI SAI" nếu có · việc còn dở.
