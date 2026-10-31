# Làm nhiều bài một đợt + chọn mô hình (tách nguyên văn từ SKILL.md 31/10/2026)

Chỉ đọc khi soạn ≥2 bài một đợt hoặc khi thuê subagent.

## Làm nhiều bài một đợt — thuê subagent song song (chốt 4/10/2026)

Thầy hỏi 4/10/2026: "gọi subagent làm song song các bài có tiết kiệm token hơn không?" — **Có, nhưng tiết kiệm
token của PHIÊN CHÍNH, không phải tổng token của cả hệ thống.** Mỗi lượt trong phiên chính gửi lại toàn bộ
ngữ cảnh; soạn 14 bài trong phiên chính thì ngữ cảnh phình theo cấp số cộng (14 bài cũ + 14 bản nháp + log
lint + ảnh), tốn hơn hẳn khoản lặp ~30–50k token mà mỗi subagent phải trả để đọc lại SKILL.md + bài mẫu.
Subagent có ngữ cảnh riêng, xong là vứt; phiên chính chỉ nhận một bản tóm tắt JSON.

**Quy tắc chọn:**
- Đợt **≥ 3 bài** → chia lô 4–5 bài, mỗi bài một subagent soạn, chạy song song; mỗi bài thêm một subagent
  **kiểm chéo độc lập**; chỉ gọi subagent thứ ba (sửa) khi bản kiểm chéo có lỗi.
- Đợt **1–2 bài** → tự làm trong phiên chính; thuê agent chỉ tốn thêm mà không được lợi gì.

**Prompt cho agent soạn phải TỰ CHỨA** (agent KHÔNG thấy hội thoại, không thấy skill nếu không được chỉ):
repo (chạy mọi lệnh từ gốc `thachlab`) · `lesson_id` + tên bài + chương · thư mục bài mới · tiền tố id quiz
(`tl<bài>-`) và tiền tố file thí nghiệm (`tn-l12-<slug>-NN.json`) · danh sách file **phải đọc** (SKILL.md,
`references/linh-kien-html.md`, `references/hinh-svg.md`, `references/phuong-phap-day-tq.md`, một bài mẫu mới
nhất, `content/thi-nghiem/README.md` + 1 file mẫu, `public/data/lessons/<id>.json` để giữ đủ ý bắt buộc) ·
sản phẩm (theory.html 6 phần, `build_figs.py`, file thí nghiệm, `bundle.json`) · **ràng buộc cứng chép nguyên**
(`.tl-quiz` input ngay trước label + anh em trực tiếp, cấm `<script>/<style>/on*=`, `\lt`/`\gt`, bảng ≤3 cột,
cấm vai "thầy", độ dài ~2.000–2.500 từ) · **lệnh kiểm chính xác** (lint_theory, lint_do_dai, check_quizzes,
thi_nghiem, build_preview, chup_anh `--kiem-tran`, chup_anh, validate_bundle) · yêu cầu **xem ảnh bằng mắt**
(`--kiem-tran` không bắt được nhãn chồng chữ) · **cấm** git commit/push, ghi DB, sửa `app/globals.css`, sửa
file của bài khác · định dạng JSON trả về.

**Prompt cho agent kiểm chéo:** đọc `theory.html` + file thí nghiệm + `bundle.json`; tự giải lại **từng quiz**
và xác nhận đúng 1 đáp án đúng / các đáp án sai chắc chắn sai; tính lại mọi số liệu trong bảng, bài toán mẫu,
biến thể, thử thách; soát ràng buộc cấu trúc; đối chiếu bản cũ xem có bỏ sót ý bắt buộc; trả JSON
`{ok, issues:[{muc_do, vi_tri, van_de, cach_sua}]}`. Agent này KHÔNG sửa bài.

**Việc phiên chính phải tự làm (đừng giao agent):**
1. Chạy `thi_nghiem.py` **một lần cuối** để sinh `content/thi-nghiem/index.json` — file dùng chung, chạy song
   song thì lần ghi sau đè lần trước và có thể thiếu mục.
2. `git commit` (chỉ file của đợt), ghi DB `bash scripts/cap-nhat-ly-thuyet.sh <theory.html> <lesson_id> --yes`,
   deploy, cập nhật `docs/STATE.md` + memory.

**Chạy song song an toàn:** `chup_anh.py` mở Chrome với `--user-data-dir` tạm riêng + cổng debug ngẫu nhiên nên
chạy song song được, nhưng 14 Chrome cùng lúc ngốn RAM → chạy theo lô 4–5 bài. `thi_nghiem.py` ghi `index.json`
dùng chung: agent vẫn nên chạy nó để tự kiểm liên kết `data-exp`, nếu báo lỗi do file của bài khác đang ghi dở
thì chạy lại một lần, **tuyệt đối không sửa file của bài khác**.

**Bài học vận hành (bắt buộc, đã trả giá 4/10/2026):**
- **Đưa ĐỦ danh sách lỗi cho agent sửa.** Bản kiểm chéo trả 8–14 lỗi/bài; cắt ngắn JSON (từng cắt ở 4 000 ký
  tự) làm agent sửa chỉ thấy 6 lỗi đầu → vòng kiểm sau tìm lại đúng những lỗi đã bị bỏ. Cho nguyên JSON
  (`slice(0, 30000)`) và yêu cầu sửa **cả `chan` lẫn `nen_sua`**, kèm lý do cho mục không sửa.
- **Kiểm hai vòng là bình thường, không phải làm lại.** Vòng 2 trên 5 bài vẫn bắt được 3–4 lỗi `chan`/bài
  (số liệu thí nghiệm mâu thuẫn, mũi tên SVG ngược chiều, phản hồi quiz gọi tên phương án không tồn tại, số
  hình không theo thứ tự). Đừng tin báo cáo "đã sửa hết" của agent soạn.
- **Nhiều phiên cùng chạy → không ghi đè.** Đợt này một phiên khác đã soạn và đăng bài 15 (id 126) trước;
  bài đó bị **bỏ khỏi danh sách đăng**, bản của mình để nguyên, không ghi đè (đúng luật "xung đột" trong
  `AGENTS.md`). Trước khi đăng phải `select` lại `lesson_items` để biết bài nào vừa được phiên khác đăng.
- **`chup_anh.py` cắt mục dài thành khúc.** Mục II nhiều mục con chụp ở scale=2 có thể cao 15 000–20 000 px:
  WebP/VP8 cứng trần 16 383 px (script chết giữa vòng) và ảnh đó cũng không ai soi được. Từ 4/10/2026 script
  tự cắt thành `sec-2a`, `sec-2b`… mỗi khúc ≤ 5 000 px và xoá khúc cũ của lần chạy trước.
- **`xem-thu/` không commit.** 13 bài lớp 12 cho ra 43 MB ảnh — nặng vĩnh viễn cho repo, mà sinh lại được
  bằng hai lệnh (`build_preview.py` rồi `chup_anh.py`). Commit `theory.html` + `theory.src.html` +
  `build_figs.py` + `build_bundle.py` + `bundle.json` là đủ; để `xem-thu/` lại trên máy cho thầy xem.
- **Rà hiện trạng bằng DB, đừng tin `public/data/`.** `public/data/lessons/<id>.json` là bản build tĩnh cuối
  cùng, **không phải DB**: bài 2 hiện `tl=false` trong file tĩnh nhưng DB đã có bản tương tác từ trước → suýt
  chọn lại bài đã xong và suýt đăng đè. Trước khi chọn bài phải `select kind, body_html from lesson_items`
  (`kind='ly_thuyet'`) rồi mới kết luận bài nào còn thiếu.
- **Tiền tố id theo `lesson_id`, không theo "Bài N".** Lớp 12 có **hai "Bài 14"** (chương Từ trường id 125 và
  chương Hạt nhân id 15) — đánh theo số bài là trùng và khó tra. Đặt `tl125-…`, `tl15-…` theo id; nhờ vậy mới
  phát hiện phiên khác đang dùng `tl15-` cho bài 15 (khác bài với `tl15-` của mình).
- **Giữ bộ ba nguồn `theory.src.html` + `build_figs.py` + `build_bundle.py`.** Nguồn chứa mốc `<!--FIGn-->`;
  `build_figs.py` sinh hình rồi dựng `theory.html`; `build_bundle.py` dựng `bundle.json` từ `theory.html`.
  Ba bản luôn khớp byte, sửa một chỗ không sợ quên đồng bộ (13 bài đợt này đều theo khuôn đó).
- **Đăng theo lô rồi deploy MỘT lần.** 13 bài ghi DB mất ~2 phút (`cap-nhat-ly-thuyet.sh … --yes` trong vòng
  lặp, log `scripts/logs/dang-13-bai-l12-*.log`); chỉ deploy một lần ở cuối, đừng deploy từng bài.
- **Kiểm chứng ba tầng sau khi đăng** (đừng tin "chắc là lên rồi"): (1) **DB** — `lesson_items` của đúng bài có
  `tl-quiz`; (2) **bản build** — đọc `out/data/lessons/<id>.json` trong worktree deploy xem có `tl-quiz`;
  (3) **web thật** — `curl https://thachlab.id.vn/data/lessons/<id>.json`. Hosting chỉ kéo bản mới sau **5–10
  phút**, nên lần `curl` đầu vẫn ra bài cũ là bình thường — phải chờ rồi kiểm lại mới kết luận.

**Đo đợt 4/10/2026 (14 bài Vật lí 12, trừ bài thực hành đo + kiểm tra):** 1 bài chạy thử một mình + 3 lô
(3 + 5 + 5 bài) + 1 vòng kiểm lại 5 bài = **~50 lượt subagent**, khoảng **2 giờ** tính từ lúc bắt đầu soạn đến
lúc đăng xong; **mọi bài đều có ít nhất một lỗi `chan`** do bản kiểm chéo bắt được (nhiều nhất 4 lỗi/bài),
5 bài phải sửa hai vòng. Kết quả: 13 bài đăng DB + deploy (bài 15 id 126 bỏ vì phiên khác đăng trước).

## Chọn mô hình Claude cho từng việc (đề xuất 4/10/2026; đã đo 5/10/2026 trên 2 đợt thật — xem Nhật ký)

Mỗi bài có 4 loại việc đòi hỏi khác nhau; chọn mô hình theo việc, không theo bài:

| Việc | Mô hình | Vì sao |
|---|---|---|
| Soạn nội dung (giọng không vai "thầy", mở bài, câu dự đoán, bẫy, phân tích lỗi sai) + **vẽ SVG** | **Opus 5.5** (agent soạn) | Cần cảm quan sư phạm và suy luận không gian; SVG là chỗ hay sai nhất (chương 1 VL12 gặp 6 lỗi hình, mũi tên ngược chiều, nhãn chồng chữ). Mô hình mạnh hơn ít vòng sửa hơn. |
| Kiểm chéo (giải lại từng quiz, tính lại số liệu, soát ràng buộc) | **Sonnet 5.5** | Việc đối chiếu, rẻ hơn nhiều, đủ dùng. Nên là mô hình KHÁC agent soạn để không lặp cùng điểm mù. |
| Bài thực hành / bài ứng dụng đơn giản (khuôn lặp, ít hình) | **Sonnet 5.5** soạn thẳng | Tiết kiệm; vẫn qua kiểm chéo như thường. |
| Đóng gói bundle, xem thử, validate, ghi DB | script (`build_bundle.py`, `validate_bundle`, `cap-nhat-ly-thuyet.sh`) | Không cần mô hình mạnh. **Không dùng Haiku để soạn.** |

- Khối nhiều hình vector/đường sức (Vật lí 10 động học–động lực học, Vật lí 11 điện trường) → ưu tiên Opus cho agent soạn.
- Chỉ định mô hình bằng tham số `model` của công cụ Agent khi thuê agent soạn/kiểm (xem mục "thuê subagent song song").
- **Luồng chính (điều phối) chạy Sonnet**, không chạy Fable/Opus: nó chỉ chia việc, đọc JSON tóm tắt và chạy script. Fable dùng cho **đúng agent soạn nội dung** khi thầy yêu cầu, và agent đó soạn **trọn bài** (nội dung + SVG + bundle) — không tách "Fable viết chữ, Sonnet code hình" (đo 5/10/2026: tách làm mỗi bài qua 2 agent full-context + thêm agent "sửa hình", tốn gấp đôi).
- Làm theo **lô theo chương** (ví dụ 6 bài Điện trường L11) để dùng chung thư viện SVG và khung bài.
- Muốn chắc: soạn **cùng một bài** bằng hai mô hình, so số lỗi `chan` mà bản kiểm chéo bắt được rồi cập nhật bảng này.
