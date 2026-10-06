---
name: project_thachlab_perf_publish_rule
description: "Quy tắc bắt buộc 28/9/2026: mọi nội dung đăng lên thachlab phải tối ưu tốc độ tải — thêm vào AGENTS.md + 6 skill đăng bài/đề"
metadata:
  type: project
  originSessionId: ced67303-e669-4938-ac6d-53a4b0cb65c7
  modified: 2026-10-02T08:19:25.983Z
---

Theo yêu cầu thầy 28/9/2026: "đăng gì cũng phải tối ưu tốc độ tải" — đã thêm quy tắc chính
thức vào `AGENTS.md` (khối `<!-- BEGIN:thachlab-perf-publish -->`, luôn được nạp mỗi phiên
qua `CLAUDE.md`), dựa trên các quyết định đã chốt ở đợt tối ưu 25-27/9
([[project_thachlab_perf_optimization]]): ảnh chèn vào HTML/Storage phải nén trước (rộng tối
đa ~1200px, `scripts/optimize-images.mjs` cho `public/`, tự nén bằng sharp/magick trước khi
encode base64 cho bundle JSON — chưa có bước nén tự động phía nhận), ảnh mới trong code →
`.webp`, không nhúng base64 thẳng vào HTML lưu DB, chunk JS mới phải bọc `LazyErrorBoundary`,
KaTeX giữ đồng bộ ở trang học sinh, không thêm round-trip Supabase thừa ở trang đã tối ưu.

Đã lan quy tắc (thêm 1 đoạn ngắn trỏ về AGENTS.md, không copy nguyên văn) vào 6 skill "đăng":
- `.claude/skills/up-de-kiem-tra/SKILL.md` (trong repo) — bullet "Ảnh:" ở mục Cấu trúc dữ liệu.
- `.claude/skills/dang-de-hang-loat/SKILL.md` (trong repo) — mục An toàn.
- `dang-bai-hoc-thachlab`, `azota`, `ngan-hang-cau-hoi` — sửa ở **Library**
  (`/Users/MAC/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin/f7f31a21-…/46c5a460-…/skills/<tên>/SKILL.md`)
  rồi `cp` sang `~/.codex/skills/<tên>/SKILL.md` (2 bản phải giống hệt, theo quy ước cũ ở
  [[project_thachlab_azota_skill]]).
- `bien-ban-shcn` — chỉ sửa ở Library (không có bản `~/.codex`); ghi chú là bước đăng chỉ có
  text, chưa cần áp quy tắc nén ảnh, áp dụng nếu sau này thêm ảnh.

**Phát hiện phụ — đã điều tra 28/9/2026, thầy chọn CHỜ (chưa sửa tay):** thư mục
`~/.claude/skills/synced/f7f31a21-…_46c5a460-…/` — nơi Skill tool của PHIÊN NÀY thực sự đọc
(hiện trong danh sách skill khả dụng) — đang **lệch bản** so với Library/`~/.codex` cho ít
nhất 2 skill: `ngan-hang-cau-hoi` (thiếu hẳn "Bước 7 — Đăng lên thachlab") và
`dang-bai-hoc-thachlab` (vẫn ở quy trình cũ thủ công qua Browser pane, thiếu quy trình mới
`upload-lesson.mts` đã đổi từ 22/9).

Điều tra thêm cho thấy `synced/` **không phải bản tĩnh** — nó là cache đồng bộ plugin của app
Claude Desktop, có `manifest.json` (gắn `backingPluginId` từng skill) + file
`.last-complete-round`, và **có tự cập nhật lẻ tẻ theo từng skill**, không đồng loạt:
`azota` đã tự khớp Library (28/9), `bien-ban-shcn` và `mathtype-sang-omml` cũng đã tự sync lại
sau mốc gốc 25/9 10:45 — nhưng `ngan-hang-cau-hoi` và `dang-bai-hoc-thachlab` vẫn kẹt nguyên ở
mốc sync gốc đó, chưa rõ vì sao (có thể do nguồn plugin gốc chưa "publish" bản mới, có thể do
kẹt/lỗi). Không có cách nào từ file hệ thống để suy ra chắc chắn logic trigger sync.

→ Đã hỏi thầy 28/9/2026: chọn **"Chờ thêm, không sửa gì bây giờ"** (không phải "để thầy tự xử
lý", cũng không sửa tay ngay). Lý do thầy chọn: đã thấy 3 skill khác tự bắt kịp trong vài
ngày, muốn để cơ chế tự sync có thêm thời gian trước khi can thiệp tay — sửa tay có rủi ro bị
tiến trình tự sync ghi đè ngược không báo trước nếu nguồn plugin gốc chưa cập nhật thật.
**ĐÃ XONG — xác nhận 2026-10-02 (scheduled task `check-skill-sync-catchup`, lần kiểm 2):**
cả `ngan-hang-cau-hoi` (11304 bytes, mtime 28/9 09:01:36) và `dang-bai-hoc-thachlab`
(17676 bytes, mtime 28/9 09:00:56) trong `synced/` đã **tự bắt kịp Library** — `diff -q`
không khác, md5 trùng. Không sửa tay gì cả; quyết định "chờ" của thầy 28/9 là đúng. Bài học:
cơ chế tự sync của Claude Desktop có độ trễ tới ~vài ngày theo từng skill, kiên nhẫn chờ
thay vì copy đè. Scheduled task này có thể xoá.

**Why:** thầy muốn chuẩn chốt "không có ngoại lệ" cho hiệu năng khi đăng nội dung, đặt vào
văn bản luôn được nạp (AGENTS.md) thay vì chỉ nhớ miệng.
**How to apply:** trước khi đăng bài/đề có ảnh, đọc lại mục "Đăng nội dung — luôn tối ưu tốc
độ tải" trong `AGENTS.md`; nếu sửa lại các skill trên, nhớ sửa đúng cả 2 (hoặc 3) bản như ghi
ở trên, đừng chỉ sửa 1 chỗ tưởng là đủ.
