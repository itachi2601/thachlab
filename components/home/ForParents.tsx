import Image from "next/image";
import Link from "next/link";
import { ArrowRight, MessageCircle, Phone } from "lucide-react";
import { CONTACT } from "@/lib/contact";
import { displayPhone } from "@/components/parent/TeacherContact";

/**
 * Dải "Dành cho phụ huynh" — nền sáng, chữ 18px, nút ≥48px (P1, P4, P5).
 * Ảnh thầy, số năm dạy, và một câu học phí / lịch / chỗ học nằm ngay trong khối này.
 * Giọng "thầy – phụ huynh": xưng "con", không "em".
 * Học phí và lịch không bịa số: web miễn phí (đã công bố), học phí đóng tại trung tâm
 * và lịch từng lớp nằm ở /khoa-hoc.
 */
const QUESTIONS = [
  {
    title: "Con học gì",
    desc: "Lý thuyết, bài tập, đề kiểm tra theo đúng chương trình 2018, bám nhịp lớp trên trường.",
  },
  {
    title: "Thầy theo dõi ra sao",
    desc: "Mỗi bài làm được chấm ngay. Câu sai gắn với phần kiến thức, thầy biết con còn yếu chỗ nào để phụ đạo.",
  },
  {
    title: "Phụ huynh xem kết quả ở đâu",
    desc: "Tài khoản riêng để xem điểm, bài đã làm và phần con còn sai.",
    href: "/phu-huynh",
  },
];

const btn =
  "inline-flex min-h-12 items-center justify-center gap-2 rounded-lg px-4 text-base font-semibold";

export default function ForParents() {
  const phone = CONTACT.phone ? displayPhone(CONTACT.phone) : "";
  const intro = [CONTACT.years ? `${CONTACT.years} năm dạy Vật lý` : "", CONTACT.school]
    .filter(Boolean)
    .join(" · ");

  return (
    <section className="bg-[#f8fafc] px-6 py-10 text-[#0f172a] lg:px-12">
      <div className="mx-auto grid max-w-6xl gap-8 lg:grid-cols-[16rem_1fr] lg:items-start lg:gap-12">
        <div>
          {CONTACT.teacherPhoto && (
            <Image
              src={CONTACT.teacherPhoto}
              alt="Thầy Thạch chụp cùng học sinh trong lớp học"
              width={800}
              height={600}
              sizes="256px"
              className="h-auto w-full max-w-64 rounded-2xl"
            />
          )}
          <p className="mt-4 font-display text-xl font-bold">Thầy Thạch</p>
          {intro && <p className="mt-1 text-lg leading-snug text-[#334155]">{intro}</p>}
        </div>

        <div>
          <h2 className="font-display text-2xl font-bold">Dành cho phụ huynh</h2>
          <p className="mt-3 max-w-xl text-lg leading-relaxed text-[#334155]">
            Bài trên web học miễn phí. Lớp học thêm tại {CONTACT.area.replace(/^Khu vực /i, "khu vực ")}; học phí đóng tại
            trung tâm, lịch từng lớp ở trang đăng ký.
          </p>
          <p className="mt-3">
            <Link href="/khoa-hoc" className={`${btn} bg-[#155e75] text-white hover:bg-[#0e7490]`}>
              Xem lịch và đăng ký <ArrowRight size={18} />
            </Link>
          </p>

          <ul className="mt-6 grid gap-5 sm:grid-cols-3">
            {QUESTIONS.map((q) => (
              <li key={q.title}>
                <h3 className="font-display text-lg font-semibold">{q.title}</h3>
                <p className="mt-1.5 text-lg leading-relaxed text-[#334155]">{q.desc}</p>
                {q.href && (
                  <Link
                    href={q.href}
                    className="mt-2 inline-flex min-h-12 items-center gap-1 text-base font-semibold text-[#155e75] hover:underline"
                  >
                    Xem kết quả của con <ArrowRight size={16} />
                  </Link>
                )}
              </li>
            ))}
          </ul>

          <div className="mt-6 flex flex-wrap gap-3">
            {CONTACT.zalo && (
              <a
                href={CONTACT.zalo}
                target="_blank"
                rel="noopener noreferrer"
                className={`${btn} bg-[#155e75] text-white hover:bg-[#0e7490]`}
              >
                <MessageCircle size={18} /> Nhắn Zalo cho thầy
              </a>
            )}
            {CONTACT.phone && (
              <a
                href={`tel:${CONTACT.phone}`}
                className={`${btn} border border-[#cbd5e1] bg-white text-[#0f172a] hover:bg-[#f1f5f9]`}
              >
                <Phone size={18} /> Gọi {phone}
              </a>
            )}
          </div>
        </div>
      </div>
    </section>
  );
}
