// Sinh 12 PHIẾU BUỔI CNC lớp đảo ngược (cnc_lessons id flip-1 … flip-12) từ dữ liệu dưới đây.
// Khuôn: docs/CNC-FLIPPED-THIET-KE-LAI-2026-11-08.md mục 4 (phiếu chỉ TRỎ vào mục bài qua neo #muc-N, không chép bài).
//
//   node content/lesson-samples/cnc-phieu-buoi/build.mjs        → out/flip-N.html + out/flip-N.meta.json
//   bash content/lesson-samples/cnc-phieu-buoi/dang.sh --dry-run  (rồi bỏ --dry-run) → ghi DB bằng scripts/them-bai-cnc.mts
//
// Số bài như trên web: lesson-4-turn = Bài 4, lesson-4-mill = Bài 5, lesson-5 = Bài 6, lesson-6 = Bài 7.
// Tên mục khớp tiêu đề "N. …" trong body_html (id muc-N ghi 8/11/2026). Quiz chuẩn bị: services/cnc-prep.ts.
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const dir = path.dirname(fileURLToPath(import.meta.url));
const out = path.join(dir, "out");

const LESSONS = {
  "lesson-1": { no: 1, muc: ["Từ máy vạn năng đến máy CNC", "Cấu tạo chung", "Bộ phận chính của máy tiện và máy phay", "Đặc tính kỹ thuật", "Hệ trục tọa độ", "Các điểm chuẩn", "Lắp đặt, bảo quản, bảo dưỡng"] },
  "lesson-2": { no: 2, muc: ["Điểm chuẩn khi lập trình", "Cấu trúc chương trình FANUC 21T", "Mặt phẳng, đơn vị, lệnh dịch chuyển", "Bù bán kính mũi dao", "Chu trình tiện và khoan", "Mã M trong chương trình tiện"] },
  "lesson-3": { no: 3, muc: ["Năm điểm chuẩn trên máy phay", "Cấu trúc chương trình FANUC 21M", "Mặt phẳng, đơn vị, lệnh dịch chuyển", "Bù bán kính và bù chiều dài dao", "Chu trình khoan G81, G83, G73", "Chu trình tarô và doa", "Mã M trong chương trình phay"] },
  "lesson-4-turn": { no: 4, muc: ["Cấu tạo máy EMCO TURN 55", "Kiểm tra máy trước khi cấp điện", "Mở máy, về Reference, JOG", "MDI: gõ lệnh, chạy từng câu", "Gá phôi và gá dao", "Bài tập tiện bằng tay", "Điểm chuẩn và xóa dữ liệu cũ", "Cài gốc phôi W (Work Shift)", "Geometry Offset cho từng dao", "Kiểm tra trước khi chạy"] },
  "lesson-4-mill": { no: 5, muc: ["Cấu tạo máy phay MILL 55", "Kiểm tra trước khi cấp điện", "Mở máy, về Reference, JOG", "Trục chính, thay dao, MDI", "Gá phôi và gá dao phay", "Bài tập vận hành phay bằng tay", "Điểm chuẩn và xóa dữ liệu cũ", "Cài chiều dài và bán kính dao", "Cài gốc phôi W theo Z, X, Y", "Kiểm tra cài đặt trước khi phay"] },
  "lesson-5": { no: 6, muc: ["Tiện mặt đầu", "Tiện trụ ngắn và bậc", "Vát cạnh, bo cung, thứ tự nguyên công", "Tiện côn, tiện ren", "Bài tập tổng hợp: năm bước giải"] },
  "lesson-6": { no: 7, muc: ["Phay mặt phẳng", "Phay bậc, cong, cung", "Phay theo biên dạng (profile)", "Khoan lỗ và tarô", "Bài tập tổng hợp: sắp thứ tự nguyên công"] },
};

const href = (id, anchor) => `/lop-hoc/cnc/?bai=${id}${anchor ? `#${anchor}` : ""}`;
// "lesson-2:1" → link tới mục 1 của Bài 2; "lesson-2:mau" → Bài toán mẫu; "lesson-2" → đầu bài.
function muc(ref) {
  const [id, m] = ref.split(":");
  const l = LESSONS[id];
  if (!l) throw new Error(`Không có bài ${id}`);
  if (!m) return `<a href="${href(id)}">Bài ${l.no}</a>`;
  if (m === "mau") return `<a href="${href(id, "bai-mau")}">Bài ${l.no} · bài toán mẫu</a>`;
  const name = l.muc[Number(m) - 1];
  if (!name) throw new Error(`Bài ${id} không có mục ${m}`);
  return `<a href="${href(id, `muc-${m}`)}">Bài ${l.no} · mục ${m}. ${name}</a>`;
}
const links = (refs) => refs.map(muc).join("; ");
// Nhãn ngắn (không lặp tên mục khi câu đã nói nội dung — N4): "Bài 4 · mục 7".
const ref = (r) => { const [id, m] = r.split(":"); return `<a href="${href(id, m === "mau" ? "bai-mau" : `muc-${m}`)}">Bài ${LESSONS[id].no} · ${m === "mau" ? "bài toán mẫu" : `mục ${m}`}</a>`; };

const GATES = {
  G1: "G1 An toàn: đạt quiz an toàn (tab Kiểm tra của Bài 1) và ký nội quy xưởng. Chưa qua G1 thì chưa đứng máy thật.",
  G2: "G2 Lập trình tiện: chương trình tiện chạy WinNC không lỗi (bài tập 1–2 của Bài 2).",
  G3: "G3 Lập trình phay: chương trình phay chạy WinNC không lỗi (bài tập 1–2 của Bài 3).",
  "G4 tiện": "G4 Vận hành tiện: đạt vận hành máy + cài dao và checklist Bài 4. Đạt mới cắt phôi thật trên máy tiện.",
  "G4 phay": "G4 Vận hành phay: đạt vận hành máy + cài dao và checklist Bài 5. Đạt mới cắt phôi thật trên máy phay.",
  G5: "G5 Chi tiết đạt dung sai: chấm theo rubric của giảng viên.",
};

// gv: phút giảng viên dạy (mặc định 60). Hai lượt thực hành chia đều phần còn lại.
const SESSIONS = [
  {
    no: 1, title: "Nhập môn: an toàn, máy, điểm chuẩn, chương trình đầu tiên", gv: 90,
    open: "Mở buổi: giới thiệu môn, cách học lớp đảo ngược, lịch 12 buổi, nội quy xưởng.",
    goals: ["Nêu nội quy xưởng và việc phải làm khi dừng khẩn.", "Chỉ trục X, Z (X, Y, Z) và điểm chuẩn M, W, R trên máy.", "Về Reference, chạy JOG, gõ MDI; nhập và chạy chương trình O0001 trên WinNC."],
    read: null,
    blocks: ["An toàn, 5S, nút dừng khẩn", "Máy CNC và bộ phận chính (" + ref("lesson-1:2") + ", " + ref("lesson-1:3") + ")", "Hệ trục và điểm chuẩn M, W, R (" + ref("lesson-1:5") + ", " + ref("lesson-1:6") + ")", "WinNC FANUC: các chế độ, lệnh cơ bản, cùng viết O0001"],
    real: ["Nhận máy theo checklist, chưa cấp điện khi chưa kiểm xong.", "Mở máy, về Reference, ghi số các trục.", "Thử thách: JOG không phôi, thử % bước tiến; MDI gõ <code>M3 S500;</code> chạy từng câu."],
    winnc: ["Gõ chương trình O0001 dưới đây, chạy mô phỏng.", "Đổi <code>Z-20</code> thành <code>Z-15</code>, dự đoán rồi chạy lại.", "Thử thách: thêm một bậc Ø16 dài 8 mm."],
    extra: `<div class="tl-box tl-box--rule"><p class="tl-label">Chương trình O0001 (trạm WinNC)</p><p><code>N10 G71 G95 G18;</code><br><code>N20 T0202 M6;</code><br><code>N30 M3 S500;</code><br><code>N40 G00 X30 Z5;</code><br><code>N50 G00 X20 Z2;</code><br><code>N60 G01 Z-20 F0.15;</code><br><code>N70 G01 X30;</code><br><code>N80 G00 Z5;</code><br><code>N90 M5;</code><br><code>N100 M30;</code></p><p>Chưa chạy thử trên WinNC của xưởng: lệnh báo lỗi thì ghi lại cho giảng viên.</p></div>`,
    product: ["Ảnh màn hình WinNC chạy xong O0001.", "Bảng số các trục ở Reference."],
    exit: ["Điểm nào do người vận hành đặt: M, R hay W?", "Máy đang quay, phoi quấn vào phôi: làm gì trước tiên?", "Chế độ nào để chạy từng câu lệnh gõ tay?"],
    gates: ["G1"],
  },
  {
    no: 2, title: "Lập trình tiện (1): cấu trúc chương trình, G00/G01", prep: ["lesson-2:1", "lesson-2:2"], lessonId: "lesson-2",
    goals: ["Viết đúng khối lệnh FANUC 21T có G18, G71, G95.", "Ghi X theo đường kính; phân biệt X/Z với U/W.", "Viết chương trình trục bậc chỉ dùng G00/G01."],
    blocks: ["Điểm chuẩn khi lập trình, cấu trúc chương trình", "Mặt phẳng, đơn vị, G00/G01 (" + ref("lesson-2:3") + ")", "X đường kính, X/Z hay U/W: viết chung một trục bậc"],
    real: ["Làm theo " + ref("lesson-4-turn:2") + ", " + ref("lesson-4-turn:3") + ": kiểm máy, Reference, JOG.", "MDI theo " + ref("lesson-4-turn:4") + ": chạy từng câu, không phôi.", "Thử thách: chạy khối chương trình của nhóm, không phôi, tay đặt ở nút dừng."],
    winnc: ["Viết trục bậc Ø20/Ø30 bằng G00/G01.", "Viết lại cùng biên dạng bằng U/W, so kết quả.", "Thử thách: thêm đoạn vát 1×45°."],
    product: ["Chương trình trục bậc (tệp hoặc ảnh màn hình) chạy được trên WinNC."],
    exit: ["Vì sao X trên máy tiện ghi theo đường kính?", "G00 và G01 khác nhau ở điểm nào khi dao đang gần phôi?", "Khi nào dùng U/W thay vì X/Z?"],
  },
  {
    no: 3, title: "Lập trình tiện (2): bù mũi dao, chu trình, mã M", prep: ["lesson-2:4", "lesson-2:5"], lessonId: "lesson-2",
    goals: ["Dùng đúng G41/G42/G40 khi tiện tinh.", "Viết chu trình tiện và khoan theo mẫu.", "Đọc bài toán mẫu rồi tự viết chương trình tiện tinh trục bậc."],
    blocks: ["Bù bán kính mũi dao: vì sao côn và cung bị sai", "Chu trình tiện và khoan", "Mã M; cùng đọc " + ref("lesson-2:mau")],
    real: ["Gá phôi, gá dao theo " + ref("lesson-4-turn:5") + ".", "Tiện mặt đầu bằng tay theo " + ref("lesson-4-turn:6") + ".", "Thử thách: đo phôi sau khi tiện, ghi sai lệch."],
    winnc: ["Viết chương trình tiện tinh trục bậc có bù mũi dao.", "Chuyển phần tiện thô sang chu trình, chạy mô phỏng.", "Thử thách: sửa đến khi chạy không còn báo lỗi."],
    product: ["Bài tập 1–2 của Bài 2 nộp trên web (tab Luyện tập/BTVN)."],
    exit: ["Quên G40 trước khi rút dao thì chuyện gì xảy ra?", "Chu trình tiện giúp chương trình ngắn hơn ở chỗ nào?", "Mã M nào dừng trục chính, mã nào kết thúc chương trình?"],
    gates: ["G2"],
  },
  {
    no: 4, title: "Lập trình phay (1): điểm chuẩn, cấu trúc, dịch chuyển", prep: ["lesson-3:1", "lesson-3:2"], lessonId: "lesson-3",
    goals: ["Chỉ năm điểm chuẩn trên máy phay.", "Viết đúng khối lệnh FANUC 21M có G17, G21, G90.", "Viết chương trình phay rãnh, bậc bằng G00/G01."],
    blocks: ["Năm điểm chuẩn, cấu trúc chương trình 21M", "G17, G90/G91, G00/G01 (" + ref("lesson-3:3") + ")", "Cùng viết chương trình phay rãnh thẳng"],
    real: ["Làm theo " + ref("lesson-4-mill:3") + ": Reference, JOG trên máy phay.", "Thay dao, MDI theo " + ref("lesson-4-mill:4") + ", không phôi.", "Thử thách: chạy khối chương trình rãnh của nhóm, không phôi."],
    winnc: ["Viết chương trình phay rãnh thẳng.", "Viết chương trình phay bậc, chạy mô phỏng.", "Thử thách: viết lại một đoạn bằng G91, so kết quả."],
    product: ["Chương trình rãnh và bậc chạy được trên WinNC."],
    exit: ["Gốc phôi W trên máy phay thường đặt ở đâu, vì sao?", "G90 và G91 cho cùng một điểm đến khác nhau thế nào?", "Lệnh nào chọn mặt phẳng XY?"],
  },
  {
    no: 5, title: "Lập trình phay (2): bù dao, chu trình khoan, mã M", prep: ["lesson-3:4", "lesson-3:5"], lessonId: "lesson-3",
    goals: ["Dùng đúng G41/G42 và G43 H khi phay biên dạng.", "Viết chu trình khoan G81/G83/G73, tarô và doa.", "Viết chương trình phay contour và 4 lỗ."],
    blocks: ["Bù bán kính và bù chiều dài dao", "Chu trình khoan, tarô, doa (" + ref("lesson-3:6") + ")", "Mã M; cùng đọc " + ref("lesson-3:mau")],
    real: ["Gá phôi, gá dao phay theo " + ref("lesson-4-mill:5") + ".", "Phay mặt phẳng bằng tay theo " + ref("lesson-4-mill:6") + ".", "Thử thách: đo chiều dày sau khi phay, ghi sai lệch."],
    winnc: ["Viết chương trình phay contour có bù bán kính.", "Viết chương trình khoan 4 lỗ bằng chu trình.", "Thử thách: sửa đến khi chạy không còn báo lỗi."],
    product: ["Bài tập 1–2 của Bài 3 nộp trên web."],
    exit: ["G41 và G42 chọn theo hướng nào của dao so với đường chạy?", "Khi nào dùng G83 thay vì G81?", "G43 H01 đi với dao nào?"],
    gates: ["G3"],
  },
  {
    no: 6, title: "Vận hành và cài đặt máy tiện", prep: ["lesson-4-turn:8", "lesson-4-turn:9"], lessonId: "lesson-4-turn",
    goals: ["Đặt gốc phôi W (Work Shift) trên máy tiện.", "Nhập Geometry Offset cho từng dao.", "Kiểm tra trước khi chạy rồi chạy chương trình buổi 3 trên phôi."],
    note: "Mục 1–6 của Bài 4 đã làm bằng tay ở buổi 2–3, buổi này chỉ đọc lại nếu quên.",
    blocks: ["Điểm chuẩn và xóa dữ liệu cũ (" + ref("lesson-4-turn:7") + ")", "Đặt W, đo dao, nhập offset ngay trên máy", "Kiểm tra trước khi chạy (" + ref("lesson-4-turn:10") + ")"],
    real: ["Đặt W và đo dao theo phiếu.", "Bạn cùng nhóm kiểm chéo checklist (cổng G4) xong mới chạy chương trình buổi 3 trên phôi: từng câu, rồi tự động.", "Thử thách: đo chi tiết, ghi sai lệch so với bản vẽ."],
    winnc: ["Nhập Work Shift và offset như trên máy thật.", "Mô phỏng chương trình buổi 3 với offset vừa nhập.", "Thử thách: cố ý nhập sai offset, xem dao chạy lệch thế nào."],
    product: ["Checklist vận hành tiện có chữ ký người kiểm chéo.", "Chi tiết buổi 3 cắt trên phôi thật."],
    exit: ["Về Reference xong đã có gốc phôi chưa?", "Work Shift khác Geometry Offset ở đâu?", "Ba việc phải kiểm trước khi bấm chạy tự động?"],
    gates: ["G4 tiện"],
  },
  {
    no: 7, title: "Vận hành và cài đặt máy phay", prep: ["lesson-4-mill:8", "lesson-4-mill:9"], lessonId: "lesson-4-mill",
    goals: ["Dò cạnh, đặt gốc phôi W theo Z, X, Y.", "Cài chiều dài và bán kính dao.", "Chạy chương trình buổi 5 trên phôi thật."],
    note: "Mục 1–6 của Bài 5 đã làm bằng tay ở buổi 4–5, buổi này chỉ đọc lại nếu quên.",
    blocks: ["Điểm chuẩn và xóa dữ liệu cũ (" + ref("lesson-4-mill:7") + ")", "Dò cạnh, cài chiều dài và bán kính dao ngay trên máy", "Kiểm tra cài đặt trước khi phay (" + ref("lesson-4-mill:10") + ")"],
    real: ["Dò cạnh, đặt W theo phiếu.", "Cài dao số 2, số 4; kiểm chéo checklist (cổng G4) xong mới chạy chương trình buổi 5: từng câu, rồi tự động.", "Thử thách: đo chi tiết, ghi sai lệch."],
    winnc: ["Nhập W và offset dao như trên máy thật.", "Mô phỏng chương trình buổi 5 với offset vừa nhập.", "Thử thách: gọi dao này nhưng bù chiều dài dao kia, xem kết quả."],
    product: ["Checklist vận hành phay có chữ ký người kiểm chéo.", "Chi tiết buổi 5 cắt trên phôi thật."],
    exit: ["Dò cạnh bằng dao Ø10, tọa độ cần cộng hay trừ bao nhiêu?", "Thứ tự T và M6 khi thay dao?", "Vì sao phải kiểm H trùng số dao?"],
    gates: ["G4 phay"],
  },
  {
    no: 8, title: "Gia công tiện (1): mặt đầu, trụ, bậc, vát, bo", prep: ["lesson-5:1", "lesson-5:2"], lessonId: "lesson-5",
    goals: ["Lập thứ tự nguyên công cho trục bậc có vát và bo.", "Viết chương trình, kiểm trên WinNC trước khi cắt.", "Cắt trục bậc trên máy thật."],
    blocks: ["Tiện mặt đầu, trụ ngắn, bậc", "Vát cạnh, bo cung (" + ref("lesson-5:3") + ")", "Thứ tự nguyên công: cùng lập cho chi tiết của buổi"],
    real: ["Gá phôi, đặt W, cài dao.", "Cắt trục bậc có vát/bo theo chương trình đã kiểm.", "Thử thách: đo, ghi sai lệch từng kích thước."],
    winnc: ["Viết chương trình trục bậc có vát và bo.", "Chạy mô phỏng, sửa đến khi không còn va chạm.", "Thử thách: rút ngắn chương trình bằng chu trình."],
    product: ["Chương trình đã kiểm WinNC.", "Trục bậc cắt thật kèm bảng đo."],
    exit: ["Vì sao tiện mặt đầu trước?", "Vát 1×45° ở mặt đầu trục Ø30: điểm đầu và điểm cuối của đường vát có X, Z bao nhiêu?", "Lỗi nào em gặp khi mô phỏng?"],
  },
  {
    no: 9, title: "Gia công tiện (2): côn, ren, bài tổng hợp", prep: ["lesson-5:4"], lessonId: "lesson-5",
    goals: ["Viết chương trình tiện côn và tiện ren.", "Giải bài tổng hợp theo năm bước.", "Cắt trục côn có ren, đo và ghi sai lệch."],
    blocks: ["Tiện côn, tiện ren", "Năm bước giải bài tổng hợp (" + ref("lesson-5:5") + ")", "Cùng đọc " + ref("lesson-5:mau")],
    real: ["Cắt trục côn có ren theo chương trình đã kiểm.", "Đo đường kính, chiều dài, kiểm ren.", "Thử thách: ghi sai lệch và nguyên nhân."],
    winnc: ["Viết chương trình côn + ren, mô phỏng.", "Kiểm bước ren và tốc độ trục chính.", "Thử thách: đổi bước ren theo đề mới."],
    product: ["Chi tiết côn có ren + bảng đo (chấm rubric)."],
    exit: ["Vì sao không tăng tốc trục chính khi đang tiện ren?", "Côn ghi X theo đường kính thì tính điểm đầu, điểm cuối thế nào?", "Sai lệch lớn nhất của em do đâu?"],
    gates: ["G5"],
  },
  {
    no: 10, title: "Gia công phay (1): mặt phẳng, bậc, cung", prep: ["lesson-6:1"], lessonId: "lesson-6",
    goals: ["Lập thứ tự nguyên công phay mặt phẳng, bậc, cung.", "Viết chương trình, kiểm trên WinNC trước khi cắt.", "Cắt chi tiết bậc có cung trên máy thật."],
    blocks: ["Phay mặt phẳng", "Phay bậc, cong, cung (" + ref("lesson-6:2") + ")", "Cùng lập thứ tự nguyên công cho chi tiết của buổi"],
    real: ["Gá phôi, dò cạnh, đặt W, cài dao.", "Phay mặt phẳng rồi bậc có cung.", "Thử thách: đo, ghi sai lệch."],
    winnc: ["Viết chương trình phay bậc có cung.", "Mô phỏng, sửa đến khi không còn va chạm.", "Thử thách: đổi bán kính cung, kiểm lại."],
    product: ["Chương trình đã kiểm WinNC.", "Chi tiết bậc có cung kèm bảng đo."],
    exit: ["Bậc sâu 6 mm, mỗi lát cắt tối đa 2 mm: mấy lát, Z từng lát bao nhiêu?", "Cung lõm nhỏ hơn bán kính dao thì sao?", "Lỗi nào em gặp khi mô phỏng?"],
  },
  {
    no: 11, title: "Gia công phay (2): profile, khoan, tarô", prep: ["lesson-6:3", "lesson-6:4"], lessonId: "lesson-6",
    goals: ["Phay theo biên dạng có bù bán kính.", "Khoan và tarô lỗ ren đúng mũi khoan.", "Cắt tấm đế bốn lỗ ren, đo và ghi sai lệch."],
    blocks: ["Phay theo biên dạng (profile)", "Khoan lỗ và tarô: chọn mũi khoan theo ren", "Sắp thứ tự nguyên công (" + ref("lesson-6:5") + "); cùng đọc " + ref("lesson-6:mau")],
    real: ["Cắt tấm đế bốn lỗ ren theo chương trình đã kiểm.", "Đo vị trí lỗ, kiểm ren.", "Thử thách: ghi sai lệch và nguyên nhân."],
    winnc: ["Viết chương trình profile + khoan + tarô.", "Mô phỏng, kiểm thứ tự dao.", "Thử thách: thêm vát mép lỗ."],
    product: ["Tấm đế bốn lỗ ren + bảng đo (chấm rubric)."],
    exit: ["Ren M12 khoan mũi bao nhiêu?", "Dao nằm bên nào của đường chạy khi dùng G41?", "Sai lệch lớn nhất của em do đâu?"],
    gates: ["G5"],
  },
  {
    no: 12, title: "Dự án nhóm: từ bản vẽ đến chi tiết", gv: 30,
    open: "Mở buổi: chia nhóm, nhóm trình bày nhanh thứ tự nguyên công đã lập.",
    goals: ["Đọc bản vẽ đề dự án, lập thứ tự nguyên công.", "Viết và chạy thử toàn bộ chương trình trên WinNC.", "Cắt chi tiết, đo, nộp hồ sơ theo checklist."],
    readText: "Đọc đề dự án giảng viên phát, lập thứ tự nguyên công (giấy hoặc tệp). Cần ôn: " + links(["lesson-5:5", "lesson-6:5"]) + ".",
    blocks: ["Chữa lỗi thường gặp ở buổi 8–11 (30 phút)"],
    real: ["Gá, đặt W, cài dao theo checklist.", "Cắt chi tiết dự án.", "Đo, ghi sai lệch."],
    winnc: ["Chạy thử toàn bộ chương trình, sửa lỗi.", "Kiểm chéo chương trình của nhóm bạn.", "Thử thách: rút ngắn thời gian chạy máy."],
    product: ["Hồ sơ dự án: thứ tự nguyên công, chương trình, ảnh mô phỏng, chi tiết + bảng đo."],
    exit: ["Bước nào tốn thời gian nhất, vì sao?", "Nếu làm lại, em đổi gì trong thứ tự nguyên công?", "Một lỗi an toàn em đã tránh được?"],
    gates: ["G5"],
  },
];

function timeline(gv = 60, open) {
  const lab = (300 - 15 - gv - 15 - 10 - 30) / 2;
  const t = [0, 15, 15 + gv, 30 + gv, 30 + gv + lab, 40 + gv + lab, 40 + gv + 2 * lab, 300];
  return [
    [t[0], t[1], open ?? "Mở buổi: giảng viên chữa <strong>2 câu cả lớp sai nhiều nhất</strong> ở quiz chuẩn bị."],
    [t[1], t[2], "Giảng viên dạy trên máy, các khối dưới đây; sau mỗi khối 2 phút hỏi đáp theo cặp."],
    [t[2], t[3], "Nghỉ."],
    [t[3], t[4], "Lượt 1: nửa lớp ở trạm máy thật, nửa ở trạm WinNC."],
    [t[4], t[5], "Nghỉ, đổi trạm."],
    [t[5], t[6], "Lượt 2: hai nửa đổi trạm."],
    [t[6], t[7], "Kết buổi: phiếu thoát 3 câu, dọn máy 5S, bàn giao máy."],
  ];
}

function build(s) {
  const h = [];
  h.push(`<div class="tl-box"><p class="tl-label">🎯 Mục tiêu buổi ${s.no}</p><ul>${s.goals.map((g) => `<li>${g}</li>`).join("")}</ul></div>`);
  h.push(`<h3 id="toi-truoc">Tối hôm trước · ≤ 20 phút</h3><ul>`);
  if (s.prep) {
    h.push(`<li>Đọc: ${links(s.prep)}.</li>`);
    h.push(`<li>Làm 5 câu <a href="${href(s.lessonId, "cnc-chuan-bi")}">chuẩn bị buổi ${s.no}</a> (cuối tab Lý thuyết của bài), ghi một câu "chỗ em chưa rõ". Không tính điểm.</li>`);
    if (s.note) h.push(`<li>${s.note}</li>`);
  } else if (s.readText) {
    h.push(`<li>${s.readText}</li>`);
  } else {
    h.push(`<li>Buổi đầu không có bài chuẩn bị. Đọc trước ${links(["lesson-1:5", "lesson-1:6"])} nếu có thời gian.</li>`);
  }
  h.push(`</ul>`);
  h.push(`<h3 id="tren-lop">Trên lớp · 300 phút</h3><ul>`);
  for (const [a, b, text] of timeline(s.gv, s.open)) h.push(`<li><strong>${a}–${b}':</strong> ${text}</li>`);
  h.push(`</ul><h4>Giảng viên dạy</h4><ol>${s.blocks.map((b) => `<li>${b}</li>`).join("")}</ol>`);
  const station = (label, items) =>
    `<div class="tl-box tl-box--exp"><p class="tl-label">${label}</p><ol class="tl-steps">${items.map((x, i) => `<li><strong>${i < 2 ? `Nhiệm vụ ${i + 1}` : "Thử thách"}:</strong> ${x.replace(/^Thử thách: /, "")}</li>`).join("")}</ol></div>`;
  h.push(station("Trạm máy thật · 2–3 người một máy, đổi vai mỗi việc", s.real));
  h.push(station("Trạm WinNC", s.winnc));
  if (s.extra) h.push(s.extra);
  h.push(`<h3 id="nop">Nộp cuối buổi</h3><ul>${s.product.map((p) => `<li>${p}</li>`).join("")}</ul>`);
  h.push(`<h4>Phiếu thoát · 3 câu</h4><ol>${s.exit.map((q) => `<li>${q}</li>`).join("")}</ol>`);
  if (s.gates?.length) h.push(`<div class="tl-box tl-box--rule"><p class="tl-label">Cổng của buổi ${s.no}</p><ul>${s.gates.map((g) => `<li>${GATES[g]}</li>`).join("")}</ul></div>`);
  return h.join("\n") + "\n";
}

fs.mkdirSync(out, { recursive: true });
for (const s of SESSIONS) {
  const html = build(s);
  if ((html.match(/\$/g) ?? []).length % 2) throw new Error(`flip-${s.no}: số dấu $ lẻ`);
  fs.writeFileSync(path.join(out, `flip-${s.no}.html`), html);
  fs.writeFileSync(
    path.join(out, `flip-${s.no}.meta.json`),
    JSON.stringify({ id: `flip-${s.no}`, title: `Buổi ${s.no} · ${s.title}`, short: `Buổi ${s.no} · ${s.title.split(":")[0]}`, duration: "300 phút" }),
  );
  console.log(`flip-${s.no}`, html.length, "ký tự");
}
