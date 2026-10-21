import Link from "next/link";
import Navbar from "@/components/layout/Navbar";
import Footer from "@/components/layout/Footer";

export const metadata = { title: "Việc của trợ giảng" };

type Task = { when: string; title: string; text: string; href?: string; isNew?: boolean };

// Buổi lên lớp: trước → trong → sau
const CLASS_BEFORE: Task[] = [
  { when: "Đến sớm 10 phút", title: "Nắm nội dung buổi", text: "Hỏi thầy hôm nay dạy bài gì, em nào cần chú ý, bài nào dễ sai." },
  { when: "Trước buổi", title: "Làm thử đề thầy gửi", text: "Làm có đáp án để nắm đề, rồi sang trang Chữa bài.", href: "/tro-giang/xem-truoc" },
];

const CLASS_DURING: Task[] = [
  { when: "10 phút đầu", title: "Kiểm bài tập cả lớp", text: "Ghi lỗi cụ thể lên bài của từng em. Em không làm bài hai buổi liên tiếp thì báo thầy. Việc này nằm trong giờ lên lớp, không tính phí chấm bài riêng." },
  { when: "Khi thầy giảng", title: "Quan sát lớp", text: "Xem em nào mất tập trung, em nào không theo kịp. Không làm việc riêng trong giờ." },
  { when: "Khi lớp làm bài", title: "Đi từng bàn, ít nhất 12 lượt tiếp xúc mỗi buổi", text: "Một em được giúp nhiều lần thì tính nhiều lượt. Gợi ý để em tự làm, không đọc lời giải cho chép. Không bàn điểm số hay năng lực của một em trước các em khác." },
  { when: "Khi thầy giao", title: "Chữa bài thay thầy", text: "Chỉ chữa bài tập, không giảng lý thuyết mới. Chuẩn bị lời giải để thầy đối chiếu. Xem đáp án và tỉ lệ đúng từng câu để chọn câu cần chữa kỹ.", href: "/tro-giang/chua-bai" },
  { when: "Giữa buổi", title: "Hoạt động lớp học (quiz trực tiếp)", text: "Tạo phòng, cho cả lớp quét mã vào chơi.", href: "/tro-giang/do-vui" },
];

const CLASS_AFTER: Task[] = [
  { when: "Cuối buổi", title: "Báo thầy 2–3 em cần chú ý và lý do", text: "Nói cụ thể: em nào, vướng bài nào, lỗi gì." },
  { when: "Ngay sau buổi", title: "Ghi buổi hôm nay trên web", text: "Chọn loại buổi (lên lớp hoặc chữa bài), điền các mục. Buổi chưa được duyệt còn sửa được trong 7 ngày. Không còn ghi công hành chính.", href: "/tro-giang/ghi" },
  { when: "Khi cần", title: "Đăng thông báo cho lớp", text: "Chọn lớp con phụ trách rồi đăng.", href: "/tro-giang/thong-bao" },
  { when: "Hằng tuần", title: "Ghi tiến trình bài dạy", text: "Tick tuần đã dạy, ghi chú cho năm sau. Thầy và trợ giảng dùng chung.", href: "/tro-giang/tien-trinh" },
];

// Buổi phụ đạo: nhận em → đặt lịch → trước → trong → cuối → sau
const TUTOR_STEPS: Task[] = [
  { when: "1 · Hằng tuần", title: "Nhận em cần phụ đạo", text: "Danh sách xếp em còn hổng nhiều lên đầu. Bấm “Tôi nhận” để nhận. Thẻ của em có phiếu xuất phát nếu em đã làm kiểm tra đầu vào. Một buổi tối đa 4 em.", href: "/tro-giang/phu-dao" },
  { when: "2 · Trước buổi", title: "Đăng lịch phụ đạo cho học sinh đặt", text: "Em chọn 1–3 chủ đề và đặt chỗ, chốt trước buổi 6 giờ. Buổi đầy chỗ có hàng chờ; bấm “Mở lượt tiếp” nếu còn chỗ (tối đa 4 em).", href: "/tro-giang/phu-dao?tab=slots" },
  { when: "3 · Trước buổi", title: "Đọc phiếu xuất phát và chuẩn bị bài", text: "Xem chủ đề đã vững (bỏ qua), cần ôn, hiểu chưa đúng, chưa biết. Phụ đạo bắt đầu từ chỗ em hổng, không dò lại phần em đã vững. Nắm bài trước buổi là một điều kiện tính điểm phụ đạo." },
  { when: "4 · Đầu buổi", title: "Dò bài cũ", text: "Mỗi em được hỏi ít nhất một lần. Hỏi để em nhớ lại, không đọc đáp án cho em." },
  { when: "5 · Trong buổi", title: "Dạy lại đúng chủ đề em hổng", text: "Gợi ý từng bước để em tự làm. Không giảng lan sang chủ đề khác. Không bàn điểm số hay năng lực của một em trước các em khác." },
  { when: "6 · Cuối buổi", title: "Tick chủ đề đã dạy, bấm “Mở bài kiểm tra cuối buổi”", text: "Bài mở trong 20 phút, 10 câu. Mỗi em tự đăng nhập tài khoản của mình để làm. Không đưa máy của con cho em." },
  { when: "7 · Ngay sau buổi", title: "Ghi buổi phụ đạo", text: "Phiếu đủ từng em. Nhóm có từ 60% số em đạt (đúng từ 7/10 câu) thì buổi đủ 25 điểm; 40–59% được 12,5; dưới 40% thì buổi đó 0 điểm dù đã tick đủ.", href: "/tro-giang/ghi" },
  { when: "Khi thầy nhờ", title: "Phỏng vấn riêng vài em", text: "Hỏi từng em, thầy không có mặt, gõ nguyên văn lời em, không lưu tên em, không hứa sẽ sửa.", href: "/tro-giang/phong-van", isNew: true },
];

const RULES: string[] = [
  "Vắng thì báo trước ít nhất 24 giờ, việc đột xuất báo ngay khi biết. Muộn quá 15 phút không báo được tính là vắng.",
  "Trang phục gọn gàng. Không dùng điện thoại riêng trong giờ.",
  "Không đưa máy của con cho học sinh làm bài hay đăng nhập.",
  "Không đọc lời giải cho chép; không bàn điểm hay năng lực một em trước các em khác.",
  "Mỗi 20 học sinh có một trợ giảng; con chỉ ghi công những buổi con trực tiếp làm.",
  "Đọc thông báo nhắc của thầy trên chuông và trang Thông báo. Tin nhắc chỉ nói việc của riêng con.",
];

const SCORES: [string, string, string][] = [
  ["Tiếp xúc", "30", "Tỉ lệ đạt 12 lượt tính riêng từng buổi rồi lấy trung bình. Một buổi nhiều lượt không bù cho buổi 0 lượt."],
  ["Phụ đạo", "25", "Mỗi buổi cần: phiếu đủ từng em, đã nắm bài trước buổi, mỗi em được hỏi, và nhóm đạt bài cuối buổi. Từ 60% số em đạt thì đủ 25 điểm, 40–59% được 12,5, dưới 40% thì buổi đó 0 điểm dù đã tick đủ. Tháng không có phụ đạo, thầy nhập điểm."],
  ["Kiểm tra bài tập", "20", "Theo tỉ lệ buổi đã kiểm tra và ghi lỗi."],
  ["Chuyên cần", "15", "Theo tỉ lệ buổi đúng giờ. Vắng được chấp nhận không vào mẫu số; muộn hoặc vắng không báo thì buổi đó không có điểm."],
  ["Thầy quan sát", "10", "Thầy nhập."],
];

function TaskList({ items }: { items: Task[] }) {
  return (
    <ul className="mt-4 space-y-3">
      {items.map((t) => (
        <li key={t.title} className="grid gap-1 rounded-xl border border-white/10 bg-white/5 p-4 sm:grid-cols-[8rem_minmax(0,1fr)] sm:gap-x-4">
          <span className="text-xs font-semibold text-blue-300 sm:pt-0.5">{t.when}</span>
          <div className="min-w-0">
            <h3 className="font-semibold text-white">
              {t.title}
              {t.isNew && <span className="ml-2 rounded-full bg-blue-500/20 px-2 py-0.5 text-xs font-bold text-blue-200">Mới</span>}
            </h3>
            <p className="mt-1 text-sm text-slate-300">{t.text}</p>
            {t.href && (
              <Link href={t.href} className="mt-2 inline-flex min-h-11 items-center text-sm text-blue-300 underline">
                Mở trang này
              </Link>
            )}
          </div>
        </li>
      ))}
    </ul>
  );
}

export default function TaskPage() {
  return (
    <>
      <Navbar />
      <main className="mx-auto max-w-3xl space-y-10 px-5 pb-20 pt-28 text-slate-300">
        <header>
          <p className="text-sm font-semibold uppercase tracking-widest text-blue-300">Vật lý 10 · 11 · 12 — Thạch Ngô</p>
          <h1 className="mt-3 text-3xl font-bold text-white">Việc của trợ giảng</h1>
          <p className="mt-3">Việc con làm trong buổi lên lớp và buổi phụ đạo, kèm bước ghi trên web. Cập nhật 21/10/2026, đọc cùng trang Quy chế.</p>
        </header>

        <section className="rounded-xl border border-white/10 bg-white/5 p-4">
          <h2 className="text-lg font-bold text-white">Con làm để đạt điều gì</h2>
          <ul className="mt-2 list-inside list-disc space-y-1 text-sm">
            <li>Mỗi em trong lớp được giúp ít nhất một lần mỗi buổi, em nào tụt lại thì thầy biết ngay.</li>
            <li>Em còn hổng được kéo lên qua phụ đạo, và có bằng chứng là bài cuối buổi.</li>
            <li>Thầy chỉ giảng, mọi việc còn lại của buổi học do con và thầy chia nhau.</li>
          </ul>
        </section>

        <section>
          <h2 className="text-xl font-bold text-white">A. Buổi lên lớp, làm cùng thầy</h2>
          <h3 className="mt-4 text-sm font-semibold uppercase tracking-widest text-blue-300">Trước buổi</h3>
          <TaskList items={CLASS_BEFORE} />
          <h3 className="mt-6 text-sm font-semibold uppercase tracking-widest text-blue-300">Trong buổi</h3>
          <TaskList items={CLASS_DURING} />
          <h3 className="mt-6 text-sm font-semibold uppercase tracking-widest text-blue-300">Sau buổi</h3>
          <TaskList items={CLASS_AFTER} />
        </section>

        <section>
          <h2 className="text-xl font-bold text-white">B. Buổi phụ đạo, con phụ trách</h2>
          <p className="mt-1 text-sm">Làm theo thứ tự 1 → 7. Phụ đạo chiếm 25 trên 100 điểm tháng.</p>
          <TaskList items={TUTOR_STEPS} />
        </section>

        <section>
          <h2 className="text-xl font-bold text-white">C. Giờ giấc và tác phong, mọi buổi</h2>
          <ul className="mt-3 list-inside list-disc space-y-2">
            {RULES.map((r) => (<li key={r}>{r}</li>))}
          </ul>
        </section>

        <section>
          <h2 className="text-xl font-bold text-white">Em thầy giao và phiếu xuất phát</h2>
          <ul className="mt-3 list-inside list-disc space-y-2">
            <li>Khi thầy giao một em cho con, con nhận thông báo trên chuông. Các mục phụ đạo đang mở của em tự chuyển sang “đã nhận” và hiện ở trang Cần phụ đạo. Mục mới mở cho em về sau cũng tự gán cho con.</li>
            <li>Đọc phiếu xuất phát trong thẻ của em trước buổi đầu: chủ đề đã vững (bỏ qua), cần ôn, hiểu chưa đúng, chưa biết, kèm gợi ý bắt đầu từ đâu. Chỉ thầy và trợ giảng thấy.</li>
            <li>Phụ đạo cho em này bắt đầu từ chủ đề trong phiếu, không dò lại phần em đã vững.</li>
          </ul>
        </section>

        <section>
          <h2 className="text-xl font-bold text-white">Hai bài kiểm tra, đừng nhầm</h2>
          <ul className="mt-3 list-inside list-disc space-y-2">
            <li><b className="text-white">Bài cuối buổi:</b> con mở cuối buổi phụ đạo, 20 phút, 10 câu, em đạt khi đúng từ 7/10 câu (70%). Có tính vào điểm phụ đạo của con.</li>
            <li><b className="text-white">Bài tự kiểm tra thoát “đang mở khoá”:</b> em tự mở ở nhà, 20 câu, thoát khi đúng từ 80%. Không tính vào điểm của con.</li>
          </ul>
        </section>

        <section>
          <h2 className="text-xl font-bold text-white">Điểm tháng (thang 100)</h2>
          <div className="mt-3 overflow-x-auto">
            <table className="w-full min-w-[420px] text-left text-sm">
              <thead>
                <tr className="border-b border-white/15"><th className="p-3">Mục</th><th className="p-3">Điểm</th><th className="p-3">Cách tính</th></tr>
              </thead>
              <tbody>
                {SCORES.map(([name, pts, how]) => (
                  <tr key={name} className="border-b border-white/10 align-top">
                    <td className="p-3 font-semibold text-white">{name}</td>
                    <td className="p-3 font-bold tabular-nums text-white">{pts}</td>
                    <td className="p-3">{how}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          <p className="mt-2 text-sm">Điểm tháng đo đúng các việc ở phần A, B, C: tiếp xúc và kiểm bài (phần A), phụ đạo (phần B), chuyên cần (phần C).</p>
          <p className="mt-3 text-sm">Tháng 10 là tháng chạy thử: chấm và công bố điểm, chưa trừ gì. Từ tháng 11 áp dụng hệ số theo điểm; mức cụ thể chưa chốt, thầy sẽ xem tình hình rồi công bố trước khi áp dụng. Đơn giá, hệ số và việc chia bậc cũng chưa chốt.</p>
        </section>

        <div className="flex flex-wrap gap-3">
          <Link href="/tro-giang/quy-che" className="inline-block rounded-xl bg-blue-600 px-5 py-3 font-semibold text-white">Đọc quy chế đầy đủ</Link>
          <Link href="/tro-giang" className="inline-block rounded-xl border border-white/20 px-5 py-3 font-semibold text-white">Về trang trợ giảng</Link>
        </div>
      </main>
      <Footer />
    </>
  );
}
