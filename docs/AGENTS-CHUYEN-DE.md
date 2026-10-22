# Quy tắc chuyên đề (tách từ AGENTS.md ngày 22/10/2026, nội dung nguyên văn)

AGENTS.md giữ mỗi mục một dòng trỏ về đây; đọc đúng mục khớp việc đang làm.

# Cập nhật bài lý thuyết đã đăng — chỉ đẩy phần lý thuyết

Sửa/đăng lại nội dung lý thuyết của bài có sẵn: dùng `bash scripts/cap-nhat-ly-thuyet.sh <theory.html|bundle.json> <lesson_id>`
(chỉ ghi cột `body_html` của mục `ly_thuyet`, tự sao lưu ra `scripts/logs/`; hoàn tác bằng `scripts/khoi-phuc-ly-thuyet.mts`).
Không dùng `upload-lesson.mts` cho việc này — nó tạo/ghi cả đề Luyện tập. Công thức có `<`/`>` trong `$…$` phải viết `\lt`/`\gt`.

**Quy tắc (thầy chốt 4/10/2026): đăng lý thuyết chỉ ghi đúng mục Lý thuyết của bài đó, không làm ảnh hưởng
phần còn lại** (Luyện tập, Kiểm tra, Bài tập mẫu, tiêu đề, tiến độ học) hay bài khác. Script đã thực thi quy tắc
này, không dựa vào việc người chạy nhớ: dry-run in rõ phạm vi (mục nào ghi, mục nào bỏ qua), UPDATE ràng buộc cả
`id` lẫn `kind='ly_thuyet'` và đòi đúng 1 dòng, rồi chụp toàn bộ `lesson_items` của bài TRƯỚC/SAU để đối chiếu —
lệch là exit 1 kèm lệnh hoàn tác. Sửa script thì giữ nguyên phần kiểm này, đừng gỡ.

# Quy tắc hình và chú thích trong bài học (thầy chốt 7/10/2026)

- Chú thích, ghi chú, đáp án, bảng ký hiệu có nhiều ý (kể cả trong bài lý thuyết và bài tập): **mỗi ý một dòng riêng**, không ghép nhiều ý vào một dòng bằng "·", ";" hay dấu phẩy. Ngoại lệ duy nhất: dòng 🔑 từ khoá 3–6 chữ.
- **Đường sức từ vẽ nét đứt; đầu mũi tên là hai vạch chéo lệch 30° so với đường chính, đầu nhọn** (helper `field_line`/`field_path`/`chevron` trong `.claude/skills/soan-bai-ly-thuyet-tuong-tac/scripts/svg_lib.py`; chi tiết ở `references/hinh-svg.md`). Hình cũ vẽ đường sức bằng `arrow()`/marker đặc thì sửa khi đụng tới bài.

# Nơi lưu nội dung bồi dưỡng HSG KHTN 9 – Vật lí (thầy chốt 10/10/2026)
Đề, pre-test, chuyên đề, bài soạn cho lớp bồi dưỡng HSG KHTN 9 (và nội dung THCS nền cho lớp đó) **lưu gốc ở**
`/Users/MAC/Documents/THPT/Lop09/00_Dung_chung/HSG_KHTN9_Vat_li/` — đọc `README.md` ở đó để biết cây thư mục
(`01_Chuyen_de`, `02_De_thi_HSG`, `03_Ke_hoach_boi_duong`, `04_Tai_lieu_tham_khao`, `pre test`).
- Mỗi bộ nội dung mới: **một thư mục con riêng**, kèm `README.md` ngắn (chủ đề→câu, file nào là đề/đáp án, chỗ ngoài chuẩn) và script sinh nếu có; không rải file ra thư mục gốc.
- Hình vẽ làm bằng SVG trong script sinh (giữ script cùng thư mục để sửa số liệu rồi chạy lại); kiểm hình bằng PDF đã render trước khi báo xong.
- Soạn xong: giao `kiem-code` (Sonnet) tự giải độc lập rồi đối chiếu đáp án trước khi coi là xong.
- Đưa lên thachlab (số hoá) chỉ làm khi thầy bảo, theo `docs/DANG-DE-TU-WORD.md` / skill đăng đề; bản sao trong repo (`content/…`) chỉ để xem, thư mục Documents là nguồn.

# Trang mẫu chuẩn cho tài liệu/sách của thầy (thầy chốt 10/10/2026)
Mọi tài liệu in/PDF thầy nhờ soạn (đề, chuyên đề, sách…) dàn trang bằng `/Users/MAC/Documents/THPT/Lop09/00_Dung_chung/HSG_KHTN9_Vat_li/_tools/trang-mau-sach/` (`sach_mau.py`, đọc README ở đó). Luôn có **số trang** và đầu trang.
- Đầu trang: `THCS TRẦN VĂN ƠN` + dòng dưới `GV Ngô Diệu Thạch` **chỉ khi thầy yêu cầu** (`school=True`). Không yêu cầu = tài liệu làm cho thầy → `school=False`, không in tên trường.
- Muốn đổi kiểu trang thì sửa ở `sach_mau.py` một chỗ, không chép CSS ra từng tài liệu. Xem PDF đã render trước khi báo xong.

# Link sâu vào trang cần đăng nhập — luôn giữ `?next=` (thầy chốt 10/10/2026)
Mọi đường vào một trang có `RequireAuth` từ bên ngoài (mã QR dán trên bảng/chiếu lên tivi, link Zalo/thông báo, deep link PWA) đều có thể gặp người CHƯA đăng nhập. Từ 10/10/2026 `RequireAuth` tự gắn `?next=<đường dẫn + query>` vào nút Đăng nhập, nên:
- Thêm đường vào mới thì **đừng truyền `loginHref` cứng** (sẽ mất `next`), trừ khi đích quay lại thật sự là trang khác.
- `?next=` phải giữ **cả phần query** (`/kiem-tra/lam/?id=770`) — mất `?id=` là mở sai trang; `/dang-nhap` chỉ nhận đường dẫn nội bộ bắt đầu bằng một `/`.
- Đổi tham số của một trang đích (ví dụ `/kiem-tra/lam` đổi cách nhận mã đề) thì phải sửa **cùng lúc** mọi nơi sinh link tới nó — mã QR và mục quét học sinh gom ở `lib/exam-link.ts`.
- Sinh mã QR/link in ra giấy mà không kiểm bằng cách **giải mã lại** thì coi như chưa kiểm: sai cũng không có lỗi build nào báo. Mẫu: `npx tsx scripts/kiem-qr.mts`.

# Bản quyền khi soạn bài và tìm tài nguyên (thầy chốt 12/10/2026)
Trang công khai `/dieu-khoan` đã cam kết với người học và chủ sở hữu; mọi phiên soạn bài, quiz, đề, bài viết hoặc tìm hình/mô phỏng/video phải giữ đúng cam kết đó:
- **Không chép nguyên văn** SGK, sách tham khảo, bài của trang khác: viết lại bằng lời mình, tự đổi số liệu/ngữ cảnh khi làm bài tập. Lời giải luôn tự soạn.
- **Đề trích hoặc phỏng theo** kỳ thi chính thức, đề sở/trường, sách: ghi nguồn (kỳ thi/đơn vị ra đề, năm, mã đề) vào tên đề hoặc ghi chú câu. Không rõ nguồn thì nói với thầy, đừng đăng như thể tự soạn.
- **Tài nguyên ngoài** (hình, mô phỏng, video, phông, mã): ưu tiên giấy phép mở (PhET CC-BY, Wikimedia Commons, CC0…); ghi tác giả + giấy phép + link ngay trong bài hoặc kế hoạch tài nguyên. Không dùng ảnh/clip không rõ giấy phép; video thì nhúng/dẫn link, không tải lại đăng lên.
- Không rõ giấy phép = **không dùng**, chuyển thành hình tự vẽ SVG hoặc báo thầy.
- Có khiếu nại bản quyền (email ở `lib/contact.ts`, quy trình ở `/dieu-khoan` mục 4): gỡ hoặc thay nội dung ngay, rồi báo thầy.

# Chất lượng đề & câu hỏi khi nạp vào web — hình rõ, đáp án rõ, dò 2 lần (thầy chốt 15/10/2026)
Đề sai/mờ/hỏng hình là mất uy tín của cả website; mọi đường nạp (up-de-kiem-tra, dang-de-hang-loat, ngan-hang-cau-hoi, đăng bài, sửa hàng loạt bằng script) phải đạt:
- **Đề chuẩn**: nhãn như đề thi thật (E1–E3), mỗi câu đủ đề + phương án + **đúng một đáp án đã đối chiếu với lời giải**, có chủ đề/dạng; số câu và phần khớp đề gốc; ghi nguồn nếu trích (mục Bản quyền).
- **Hình rõ**: nền trắng (không xám/đen do chuyển đổi), không lề trắng thừa (nét vẽ ≥ ~35% khung), đủ độ phân giải để đọc nhãn/số trên 375px (ảnh nguồn quá nhỏ bị phóng to thành mờ thì KHÔNG nạp — vẽ lại SVG hoặc báo thầy), ≤150 KB, URL đầy đủ `https://…` (không dính tiền tố `/lessons/<slug>/`), ảnh tải được (HTTP 200).
- **Dò 2 lần, độc lập, trước khi bật Hiện**: lần 1 bằng máy (script: ảnh 200/kích thước/tỉ lệ nét, đủ đáp án, đúng một đáp án, không trùng); lần 2 bằng MẮT trên bản thật — xem ảnh các câu mới/sửa (contact sheet hoặc trang xem thử, 375px), người/agent `kiem-code` khác lần 1, tự giải lại câu tính toán. Chưa qua cả hai lần thì để Ẩn, không báo "xong".
- **Sửa hàng loạt (cắt ảnh, thay URL, đổi đáp án)**: dry-run → xem mẫu bằng mắt → `--apply` có sao lưu → **kiểm lại trên bản đã ghi** (tải ảnh từ Storage/DB, không chỉ file local): mẫu `scripts/kiem-sau-cat-anh.mts`; báo rõ số ảnh lỗi còn lại, không im lặng bỏ qua (các mục `errs` của bản kiểm kê là việc chưa xong).

# Sửa hàng loạt ký hiệu trong ngân hàng câu (S1→$S_1$…) — bài học 15/10/2026
- Chữ+số trần (`t2`, `x2`, `v2/r`, `m2`) có thể là chỉ số dưới HOẶC bình phương/đơn vị: luật regex nào cũng lọt. Quy trình đúng: dry-run → agent `kiem-code` chạy KaTeX trên toàn bộ chuỗi mới + săn ngữ cảnh bình phương → hoàn tác theo id → thêm vào `EXCLUDE_IDS` → chạy lại tới khi dry-run = 0. Mẫu: `scripts/sua-chi-so-duoi-ngan-hang.mts` (`SIM=<sao lưu>` so luật hiện tại với DB; `--undo` ghi đè cả cột nên đừng dùng khi DB đã có khoá backfill mới).
- Không coi URL/`\dfrac d2` là chuỗi thường; luôn chừa vùng URL và đối số không ngoặc.

# Rà UI bằng tài khoản đăng nhập sẵn trong trình duyệt (bài học 15/10/2026)
- Trước khi kết luận "bài/đề không có dữ liệu", xác định tài khoản đang đăng nhập là ai, lớp nào, role gì: RLS `exams` giấu đề gán lớp khác, nên trang hiện "trống" chỉ với tài khoản đó. Đối chiếu bằng truy vấn DB chỉ đọc rồi mới báo.
- Repo không có `.prettierrc`: chạy prettier thì dùng `--print-width 120`, nếu không nó định dạng lại cả file thành diff rác.

# Rà lỗi hàng loạt ngân hàng câu hỏi: ca chắc thì sửa, ca nghi ngờ đưa thầy duyệt bằng HTML (thầy chốt 16/10/2026)
- Số mũ mất `^` (`x.105 Pa`, `a.109 Hz`, `3.108 m/s`): hệ số có thể là **chữ cái** chứ không chỉ chữ số; có khi mất cả dấu trừ (`10.103` = `10.10^-3`) — đối chiếu lời giải/câu anh em trước khi sửa. Script: `scripts/sua-so-mu-ngan-hang.mts --only=mu10` (dry-run → `--apply`, tự sao lưu), quét lại bằng `scripts/quet-so-mu-mo-rong.mts` tới khi chỉ còn ca nghi ngờ.
- **Ca nghi ngờ KHÔNG tự đoán, không chỉ liệt kê trong chat**: ghi `scripts/data/duyet/<đợt>/items.json` (`id`, `ghiChu`, `deXuat`) → `npx tsx scripts/lap-duyet-html.mts <thư-mục>` dựng `duyet.html` (có KaTeX, 4 lựa chọn Sửa theo đề xuất / Sửa theo ý thầy / Bỏ / Giữ + ô yêu cầu sửa, tự lưu `phan-hoi.json` khi thầy chọn file lưu một lần) → gửi/mở cho thầy. Thầy xong thì đọc `phan-hoi.json`, chạy `scripts/ap-dung-duyet.mts <thư-mục>` ("Bỏ" = ẩn `archived=true`, có sao lưu), tự sửa các câu "Sửa" theo đề xuất/ý thầy rồi quét lại và báo.
- Đơn vị mất `^` (`m/s2`, `cm3`) tách đợt riêng: `m2` có thể là khối lượng.

# Lời giải trắc nghiệm trong ngân hàng (18/10/2026)
Viết/viết lại lời giải câu hỏi: theo `docs/QUY-TAC-LOI-GIAI.md` (có đoạn "vì sao phương án khác sai", chỉ nêu lỗi tư duy thật, HS ảo kiểm mẫu 16 câu trước khi ghi). Ghi hàng loạt chỉ vào `question_bank`, không đụng `exams`.

# Sửa hàng loạt câu trong đề/ngân hàng — luôn qua SQL giao dịch (18/10/2026)
`exams.questions` đổi ⇒ `content_hash` đổi ⇒ trigger cũ sinh dòng trùng trong `question_bank`. Từ migration `20261018140000` hàm đồng bộ đã cập nhật dòng cũ, nhưng script sửa hàng loạt vẫn phải: sinh chunk SQL ≤40 câu (tắt `trg_exams_sync_bank`, sửa ngân hàng + bản sao đề, đặt lại hash), sao lưu, và đếm số dòng ngân hàng trước/sau. Mẫu: `scripts/ap-dung-de-hu-opus.mts`, `scripts/sua-so-mu-dong-bo.mts`. Đừng dùng `sua-so-mu-ngan-hang.mts` (chỉ sửa ngân hàng).
