import Link from "next/link";
import { ArrowRight, MessageCircle, Phone } from "lucide-react";
import { CONTACT } from "@/lib/contact";

/**
 * Dải "Dành cho phụ huynh" — đặt ngay sau OpenClasses trên trang chủ, trả lời 3 câu phụ huynh
 * hay hỏi khi tìm chỗ học cho con: con học gì · thầy theo dõi ra sao · xem kết quả ở đâu.
 * Giọng của khối này là "thầy – anh chị" (khối học sinh vẫn xưng "em"), không trộn trong cùng một câu.
 */
const QUESTIONS = [
  {
    title: "Con học gì",
    desc: "Lý thuyết, bài tập, đề kiểm tra theo đúng chương trình 2018, bám nhịp lớp trên trường.",
  },
  {
    title: "Thầy theo dõi ra sao",
    desc: "Mỗi bài làm được chấm ngay; câu sai gắn với chủ đề, thầy biết em yếu chỗ nào để phụ đạo.",
  },
  {
    title: "Anh chị xem kết quả ở đâu",
    desc: "Tài khoản phụ huynh xem điểm, bài đã làm, chủ đề còn sai.",
    href: "/phu-huynh",
  },
];

export default function ForParents() {
  return (
    <section className="bg-[#05070B] px-6 pb-10 pt-2 lg:px-12">
      <div className="mx-auto max-w-6xl rounded-2xl border border-line p-5 sm:p-6">
        <div className="grid gap-6 lg:grid-cols-[1fr_16rem] lg:items-start lg:gap-10">
          <div>
            <h2 className="font-display text-xl font-bold text-ink sm:text-2xl">Dành cho phụ huynh</h2>
            <ul className="mt-5 grid gap-5 sm:grid-cols-3 sm:gap-6">
              {QUESTIONS.map((q) => (
                <li key={q.title}>
                  <h3 className="font-display text-base font-semibold text-ink">{q.title}</h3>
                  <p className="mt-1.5 text-sm leading-relaxed text-muted">{q.desc}</p>
                  {q.href && (
                    <Link
                      href={q.href}
                      className="mt-2 inline-flex items-center gap-1 text-sm font-medium text-cyan-300 transition hover:text-cyan-200"
                    >
                      Xem kết quả của con <ArrowRight size={14} />
                    </Link>
                  )}
                </li>
              ))}
            </ul>
          </div>

          <div className="border-t border-line pt-5 lg:border-l lg:border-t-0 lg:pl-8 lg:pt-0">
            <p className="font-display text-base font-semibold text-ink">Học miễn phí trên web</p>
            <div className="mt-3 flex flex-wrap gap-2.5">
              {CONTACT.zalo && (
                <a
                  href={CONTACT.zalo}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center gap-2 rounded-lg bg-cyan-300 px-4 py-2.5 text-sm font-semibold text-slate-950 transition hover:bg-cyan-200"
                >
                  <MessageCircle size={16} /> Nhắn Zalo cho thầy
                </a>
              )}
              {CONTACT.phone && (
                <a
                  href={`tel:${CONTACT.phone}`}
                  className="inline-flex items-center gap-2 rounded-lg border border-line px-4 py-2.5 text-sm font-medium text-ink transition hover:bg-white/5"
                >
                  <Phone size={16} /> Gọi {CONTACT.phone}
                </a>
              )}
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
