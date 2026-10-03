import Image from "next/image";
import Link from "next/link";
import { Eye, LineChart, ListChecks, MessageCircle, Phone } from "lucide-react";
import { CONTACT, PARENT_SHOTS } from "@/lib/contact";
import { displayPhone } from "@/components/parent/TeacherContact";
import ParentFaq from "@/components/parent/ParentFaq";

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

export default function ParentGuestLanding() {
  const phone = CONTACT.phone ? displayPhone(CONTACT.phone) : "";
  return (
    <div className="space-y-7">
      <div>
        <h1 className="font-display text-2xl font-bold text-white sm:text-3xl">Theo dõi việc học của con</h1>
        <p className="parent-copy mt-3 text-slate-300">
          Đây là trang riêng cho phụ huynh. Anh chị xem được con đang học tới đâu, mạnh yếu phần nào —
          không cần mượn tài khoản của con và không phải nhắn hỏi thầy mỗi tuần.
        </p>
      </div>

      <section>
        <h2 className="font-display text-lg font-bold text-white">Anh chị sẽ thấy gì</h2>
        <ul className="mt-3 grid gap-4 sm:grid-cols-3">
          {SEES.map(({ icon: Icon, title, desc }) => (
            <li key={title} className="rounded-2xl border border-white/10 p-4">
              <Icon size={20} className="text-cyan-300" aria-hidden />
              <h3 className="mt-2 font-display font-semibold text-white">{title}</h3>
              <p className="mt-1 text-slate-400">{desc}</p>
            </li>
          ))}
        </ul>
      </section>

      <section className="rounded-2xl border border-white/10 bg-white/[.02] p-5 sm:p-6">
        <h2 className="font-display text-lg font-bold text-white">Lấy quyền xem: 3 bước</h2>
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
              <code className="rounded bg-white/[.06] px-1.5 py-0.5 text-[.95em] text-slate-200">
                thachlab.id.vn/loi-moi?ma=PH…
              </code>
            </>,
            <>
              Mở link, điền họ tên, email và mật khẩu. Tài khoản tự nối với con — anh chị{" "}
              <b>không cần mật khẩu của con</b>.
            </>,
          ].map((step, i) => (
            <li key={i} className="flex gap-4">
              <span className="mt-0.5 flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-primary font-display font-bold text-white">
                {i + 1}
              </span>
              <span className="text-slate-300">{step}</span>
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
              className="inline-flex items-center justify-center gap-2 rounded-xl border border-white/15 px-5 py-3 text-base font-semibold text-slate-200 hover:border-white/30"
            >
              <Phone size={18} /> Gọi {phone}
            </a>
          )}
          <Link
            href="/dang-nhap?next=/phu-huynh"
            className="inline-flex min-h-12 items-center font-semibold text-cyan-300 underline-offset-2 hover:underline"
          >
            Đã có tài khoản? Đăng nhập
          </Link>
        </div>
        <p className="mt-3 text-slate-400">
          Tài khoản phụ huynh chỉ để xem: không sửa được điểm, không thấy điểm của bạn khác, không thấy
          tin nhắn riêng giữa thầy và con.
        </p>
      </section>

      {PARENT_SHOTS.length > 0 && (
        <section>
          <h2 className="font-display text-lg font-bold text-white">Kết quả học sinh của thầy</h2>
          <div className={`mt-3 grid gap-4 ${PARENT_SHOTS.length > 1 ? "sm:grid-cols-2" : "max-w-2xl"}`}>
            {PARENT_SHOTS.map((shot) => (
              <figure key={shot.src}>
                <Image
                  src={shot.src}
                  alt={shot.alt}
                  width={shot.width}
                  height={shot.height}
                  sizes="(min-width: 640px) 640px, 92vw"
                  loading="lazy"
                  className="h-auto w-full rounded-xl border border-white/10 bg-white"
                />
                <figcaption className="mt-2 text-slate-400">{shot.alt}</figcaption>
              </figure>
            ))}
          </div>
          <p className="mt-2 text-slate-400">
            Ảnh thật, không phải ảnh minh hoạ. Điểm của con chỉ hiện trong tài khoản của anh chị và
            tài khoản của con — không công khai cho người khác.
          </p>
        </section>
      )}

      <section className="flex flex-col gap-4 rounded-2xl border border-white/10 p-5 sm:flex-row sm:items-center">
        {CONTACT.teacherPhoto && (
          <Image
            src={CONTACT.teacherPhoto}
            alt="Thầy Thạch"
            width={120}
            height={90}
            sizes="120px"
            loading="lazy"
            className="h-[90px] w-[120px] rounded-xl border border-white/10 object-cover"
          />
        )}
        <div>
          <h2 className="font-display text-lg font-bold text-white">Thầy đứng lớp</h2>
          <p className="mt-1 text-slate-300">
            Thầy Thạch — {CONTACT.years} năm dạy Vật lý THPT và KHTN 9.
            {CONTACT.school ? ` Đang dạy tại ${CONTACT.school}.` : ""}
            {CONTACT.area ? ` ${CONTACT.area}.` : ""}
          </p>
        </div>
      </section>

      <ParentFaq />
    </div>
  );
}
