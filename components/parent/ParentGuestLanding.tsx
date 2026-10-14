import Image from "next/image";
import Link from "next/link";
import { Eye, LineChart, ListChecks, MessageCircle, Phone } from "lucide-react";
import { CONTACT } from "@/lib/contact";
import { displayPhone } from "@/components/parent/TeacherContact";
import ParentFaq from "@/components/parent/ParentFaq";
import ScrollToHash from "@/components/ui/ScrollToHash";

/**
 * Trang khách của /phu-huynh — người xem là PHỤ HUYNH 45–60 tuổi chưa đăng nhập, thường mở link
 * này vì con đưa hoặc vì thầy gửi. Họ cần trả lời 3 câu, theo đúng thứ tự đó (P7, P10, P14):
 *   1. Trang này cho tôi xem gì?
 *   2. Làm sao tôi vào được?  → điện thoại/Zalo trước, form sau (P18)
 *   3. Thầy là ai, có thật không? → ảnh thật + số năm dạy + trường, không hứa hẹn suông
 * Chữ ở đây to hơn trang học sinh theo khối .parent-page (P1), câu ngắn, không viết tắt.
 */
const SEES = [
  {
    icon: LineChart,
    title: "Điểm của con theo thời gian",
    desc: "Bài gần nhất được bao nhiêu, tăng hay giảm so với bài trước, điểm trung bình.",
  },
  {
    icon: ListChecks,
    title: "Con còn yếu phần nào",
    desc: "Từng chủ đề: sai bao nhiêu câu trên tổng số, mở ra xem được đúng câu con làm sai.",
  },
  {
    icon: Eye,
    title: "Con đang được phụ đạo phần nào",
    desc: "Thầy đã nhận phần nào, đã dạy lại chưa, con đã làm đúng lại chưa — cùng bài tập thầy giao.",
  },
];

// Điểm môn Vật lí kỳ thi TN THPT 2025 của học sinh thầy Thạch, chép từ bảng kết quả thật (thay ảnh poster có đủ họ tên — K2, 14/10/2026).
// Chỉ hiện chữ viết tắt họ + đệm, giữ tên gọi: "Tô Anh Tuấn" → "T. A. Tuấn" (P14 bằng chứng thật, P19 nói rõ số liệu là gì, P6 số to thẳng cột).
const TNTHPT_2025: { diem: string; hs: string[] }[] = [
  { diem: "10", hs: ["Tô Anh Tuấn", "Phạm Nhật Hoàng", "Nguyễn Bá Thuấn Anh", "Trần Lương Thanh Tâm", "Bùi Hồ Hải Dương", "Nguyễn Cửu Vân Kha", "Lê Đức Phú"] },
  { diem: "9,75", hs: ["Trần Việt Quỳnh", "Hồ Gia Mẫn", "Mã Vĩnh Phú", "Trần Nhật Nguyên", "Nguyễn Xuân Vinh"] },
  { diem: "9,5", hs: ["Nguyễn Bá Anh Tú", "Nguyễn Duy Thái", "Văn Đình Thuý Vy", "Nguyễn Minh Phú", "Trần Kiên", "Đặng Võ Di Luân", "Ngọc Thi"] },
  { diem: "9,25", hs: ["Trần Gia Bảo", "Trần Tuấn Kiệt", "Nguyễn Dương Khánh", "Võ Quỳnh Trâm", "Trần Nguyễn Gia Bảo", "Mai Hồ Quốc Tuý", "Nguyễn Đăng Huỳnh Nhân"] },
  { diem: "9,1", hs: ["Kiều Minh Trí"] },
];

/** "Tô Anh Tuấn" → "T. A. Tuấn"; tên một chữ giữ nguyên. */
function shortName(full: string) {
  const parts = full.trim().split(/\s+/);
  const given = parts[parts.length - 1];
  const initials = parts.slice(0, -1).map((w) => `${w[0]}.`);
  return [...initials, given].join("\u00a0"); // không cho xuống dòng giữa họ tên
}

function ResultsTable() {
  const total = TNTHPT_2025.reduce((n, r) => n + r.hs.length, 0);
  return (
    <section id="ket-qua" className="scroll-mt-24">
      <h2 className="font-display text-lg font-bold text-ink">Kết quả học sinh của thầy</h2>
      <p className="mt-1 text-ink">
        Điểm môn Vật lí kì thi tốt nghiệp THPT 2025 của {total} em đạt từ 9,1 trở lên (lớp ôn thầy Thạch dạy tại Trung tâm Tri thức NP).
      </p>
      <div className="mt-3 overflow-hidden rounded-xl border border-line bg-panel">
        <table className="w-full border-collapse text-left">
          <caption className="sr-only">Điểm Vật lí tốt nghiệp THPT 2025 của học sinh thầy Thạch, theo từng mức điểm</caption>
          <thead>
            <tr className="border-b border-line text-muted">
              <th scope="col" className="w-24 px-4 py-2 text-[15px] font-semibold">Điểm</th>
              <th scope="col" className="px-4 py-2 text-[15px] font-semibold">Các em đạt mức này</th>
            </tr>
          </thead>
          <tbody>
            {TNTHPT_2025.map((row) => (
              <tr key={row.diem} className="border-b border-line align-top last:border-b-0">
                <th scope="row" className="px-4 py-3 font-display text-2xl font-bold tabular-nums text-primary">{row.diem}</th>
                <td className="px-4 py-3 text-ink">
                  <span className="font-semibold">{row.hs.length} em</span>
                  <span className="text-muted"> — {row.hs.map(shortName).join(", ")}</span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <p className="mt-2 text-muted">
        Tên các em được viết tắt họ và tên đệm. Sau khi đăng ký, phụ huynh chỉ thấy điểm của con mình — không thấy điểm của em khác và điểm của con không hiện công khai.
      </p>
    </section>
  );
}

export default function ParentGuestLanding() {
  const phone = CONTACT.phone ? displayPhone(CONTACT.phone) : "";
  return (
    <div className="space-y-7">
      <div>
        <h1 className="font-display text-2xl font-bold text-ink sm:text-3xl">Theo dõi việc học của con</h1>
        <p className="parent-copy mt-3 text-ink">
          Đây là trang riêng cho phụ huynh. Phụ huynh xem được con đang học tới đâu, mạnh yếu phần nào —
          không cần mượn tài khoản của con và không phải nhắn hỏi thầy mỗi tuần.
        </p>
      </div>

      <section id="phu-huynh-thay-gi" className="scroll-mt-24">
        <h2 className="font-display text-lg font-bold text-ink">Phụ huynh sẽ thấy gì</h2>
        <ul className="mt-3 grid gap-4 sm:grid-cols-3">
          {SEES.map(({ icon: Icon, title, desc }) => (
            <li key={title} className="rounded-2xl border border-line p-4">
              <Icon size={20} className="text-primary" aria-hidden />
              <h3 className="mt-2 font-display font-semibold text-ink">{title}</h3>
              <p className="mt-1 text-muted">{desc}</p>
            </li>
          ))}
        </ul>
      </section>

      <section className="rounded-2xl border border-line bg-surface-2 p-5 sm:p-6">
        <h2 className="font-display text-lg font-bold text-ink">Lấy quyền xem: 3 bước</h2>
        <ol className="mt-4 space-y-4">
          {[
            CONTACT.zalo ? (
              <>
                Nhắn Zalo cho thầy (hoặc gọi <b>{phone}</b>) và cho biết tên con đang học.
              </>
            ) : (
              <>
                Gọi cho thầy theo số <b>{phone}</b> và cho biết tên con đang học.
              </>
            ),
            <>
              Thầy gửi lại một <b>link mời</b> dạng{" "}
              <code className="rounded bg-surface-2 px-1.5 py-0.5 text-[.95em] text-ink">
                thachlab.id.vn/loi-moi?ma=PH…
              </code>
            </>,
            <>
              Mở link, điền họ tên, email và mật khẩu. Tài khoản tự nối với con — phụ huynh{" "}
              <b>không cần mật khẩu của con</b>.
            </>,
          ].map((step, i) => (
            <li key={i} className="flex gap-4">
              <span className="mt-0.5 flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-primary font-display font-bold text-white">
                {i + 1}
              </span>
              <span className="text-ink">{step}</span>
            </li>
          ))}
        </ol>

        <div className="mt-5 flex flex-wrap items-center gap-3">
          {CONTACT.zalo && (
            <a
              href={CONTACT.zalo}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center justify-center gap-2 rounded-xl bg-primary px-5 py-3 text-base font-semibold text-white hover:bg-primary-dark"
            >
              {/* Nhãn ≤ 2 từ: ở 375px + chữ 18px, "Nhắn Zalo cho thầy" xuống 2 dòng (D2) — câu
                  hướng dẫn ngay trên đã nói rõ là nhắn cho thầy. */}
              <MessageCircle size={18} /> Nhắn Zalo
            </a>
          )}
          {CONTACT.phone && (
            <a
              href={`tel:${CONTACT.phone}`}
              className="inline-flex items-center justify-center gap-2 rounded-xl border border-line px-5 py-3 text-base font-semibold text-ink hover:border-line-strong"
            >
              <Phone size={18} /> Gọi {phone}
            </a>
          )}
          <Link
            href="/dang-nhap?next=/phu-huynh"
            className="inline-flex min-h-12 items-center font-semibold text-primary underline-offset-2 hover:underline"
          >
            Đã có tài khoản? Đăng nhập
          </Link>
        </div>
        <p className="mt-3 text-muted">
          Tài khoản phụ huynh chỉ để xem: không sửa được điểm, không thấy điểm của bạn khác, không thấy
          tin nhắn riêng giữa thầy và con.
        </p>
      </section>

      {/* Các mã neo (#ket-qua, #phu-huynh-thay-gi, #thay-dung-lop) dựng sau hydrate nên cần tự cuộn; để ngoài điều kiện ảnh. */}
      <ScrollToHash />
      <ResultsTable />

      <section id="thay-dung-lop" className="flex scroll-mt-24 flex-col gap-4 rounded-2xl border border-line p-5 sm:flex-row sm:items-center">
        {CONTACT.teacherPhoto && (
          <Image
            src={CONTACT.teacherPhoto}
            alt="Thầy Thạch"
            width={120}
            height={90}
            sizes="120px"
            loading="lazy"
            className="h-[90px] w-[120px] rounded-xl border border-line object-cover"
          />
        )}
        <div>
          <h2 className="font-display text-lg font-bold text-ink">Thầy đứng lớp</h2>
          <p className="mt-1 text-ink">
            Thầy Thạch — hơn {CONTACT.years} năm luyện Vật lý THPT và KHTN 9, thạc sĩ Đại học Bách khoa
            TP.HCM, á khoa đầu vào Đại học Sư phạm Kỹ thuật TP.HCM.
            {CONTACT.school ? ` Nghề chính: giảng viên ngành Cơ khí, ${CONTACT.school}.` : ""}
            {CONTACT.area ? ` ${CONTACT.area}.` : ""}
          </p>
        </div>
      </section>

      <ParentFaq />
    </div>
  );
}
