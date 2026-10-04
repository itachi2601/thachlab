import Image from "next/image";
import Link from "next/link";
import { ArrowRight, MessageCircle, Phone } from "lucide-react";
import { CONTACT } from "@/lib/contact";
import { displayPhone } from "@/components/parent/TeacherContact";
import type { HomeCourse, HomeCourseSession } from "@/components/home/home-stats.server";

/**
 * Dải "Dành cho phụ huynh" — nền sáng, chữ 18px, nút ≥48px (P1, P4, P5).
 * Ảnh thầy, số năm dạy, câu học phí, VÀ lịch tuần các lớp đang mở nằm ngay trong khối này
 * (P7: phụ huynh đang tìm chỗ học hỏi "lớp mấy, học ngày nào" trước; P18: không bắt bấm sang
 * trang khác mới thấy lịch). Lịch đọc từ home-stats.json lúc build (scripts/build-content.mjs),
 * không gọi Supabase khi tải trang chủ; chi tiết từng lớp + nút đăng ký vẫn ở /khoa-hoc.
 * Giọng "thầy – phụ huynh": xưng "con", không "em".
 * Học phí không bịa số (P14): web miễn phí (đã công bố), học phí đóng tại trung tâm.
 * KHÔNG đưa lịch phụ đạo của trợ giảng lên đây: đó là lịch vận hành cho học sinh đã vào lớp
 * (đổi theo tuần, RLS chỉ cho thành viên lớp đọc), không phải thứ để quảng cáo.
 */
const QUESTIONS = [
  {
    title: "Con học gì",
    desc: "Lý thuyết, bài tập, đề kiểm tra theo đúng chương trình 2018, bám nhịp lớp trên trường.",
  },
  {
    title: "Thầy theo dõi ra sao",
    desc: "Mỗi bài làm được chấm ngay. Câu sai gắn với phần kiến thức; phần con còn sai nhiều, trợ giảng mở buổi phụ đạo riêng, lịch buổi hiện trong tài khoản của con.",
  },
  {
    title: "Phụ huynh xem kết quả ở đâu",
    desc: "Tài khoản riêng để xem điểm, bài đã làm và phần con còn sai.",
    href: "/phu-huynh",
  },
];

const btn =
  "inline-flex min-h-12 items-center justify-center gap-2 rounded-lg px-4 text-base font-semibold";

// 1 = Thứ 2 … 7 = Chủ nhật (cùng quy ước thpt_course_schedules.weekday và trang /khoa-hoc).
const WEEKDAY: Record<number, string> = {
  1: "Thứ 2", 2: "Thứ 3", 3: "Thứ 4", 4: "Thứ 5", 5: "Thứ 6", 6: "Thứ 7", 7: "Chủ nhật",
};

interface GradeRow {
  className: string;
  sessions: HomeCourseSession[];
}

/** Gom buổi theo khối, bỏ buổi trùng, xếp theo thứ rồi giờ. Tên lớp nội bộ ("10L3") không hiện (P8). */
function groupByGrade(courses: HomeCourse[]): GradeRow[] {
  const byGrade = new Map<string, Map<string, HomeCourseSession>>();
  for (const c of courses) {
    const m = byGrade.get(c.className) ?? new Map<string, HomeCourseSession>();
    for (const s of c.schedules) m.set(`${s.weekday}|${s.start}|${s.end}|${s.location}`, s);
    byGrade.set(c.className, m);
  }
  return [...byGrade.entries()]
    .map(([className, m]) => ({
      className,
      sessions: [...m.values()].sort((a, b) => a.weekday - b.weekday || a.start.localeCompare(b.start)),
    }))
    .filter((g) => g.sessions.length > 0)
    .sort((a, b) => Number(a.className) - Number(b.className) || a.className.localeCompare(b.className));
}

function ClassSchedule({ courses }: { courses: HomeCourse[] | null }) {
  const rows = courses ? groupByGrade(courses) : [];
  if (rows.length === 0) {
    // P9: trạng thái rỗng nói rõ vì sao + việc làm được (nút Zalo nằm ngay dưới).
    return (
      <p className="mt-5 max-w-xl text-lg leading-relaxed text-[#334155]">
        Hiện chưa có lớp nào mở đăng ký. Khi thầy mở lớp mới, lịch sẽ hiện ở đây; anh chị nhắn Zalo để được
        báo trước.
      </p>
    );
  }
  const year = (courses?.find((c) => c.schoolYear)?.schoolYear ?? "").replace("-", "–");
  return (
    <div className="mt-5 max-w-2xl rounded-2xl border border-[#cbd5e1] bg-white px-5 py-4">
      <h3 className="font-display text-lg font-semibold">
        Lịch lớp học thêm{year ? ` năm học ${year}` : ""}
      </h3>
      <ul className="mt-1 divide-y divide-[#e2e8f0]">
        {rows.map((g) => (
          <li key={g.className} className="grid gap-y-1 py-3 sm:grid-cols-[5.5rem_1fr] sm:items-baseline">
            <span className="text-lg font-bold">Lớp {g.className}</span>
            <ul className="flex flex-wrap gap-x-5 gap-y-1 text-lg leading-relaxed text-[#334155]">
              {g.sessions.map((s) => (
                <li key={`${s.weekday}-${s.start}`} className="whitespace-nowrap">
                  <span className="font-semibold text-[#0f172a]">{WEEKDAY[s.weekday] ?? ""}</span>{" "}
                  <span className="tabular-nums">
                    {s.start}–{s.end}
                  </span>
                  {s.location && <span className="text-[#475569]"> · {s.location}</span>}
                </li>
              ))}
            </ul>
          </li>
        ))}
      </ul>
      {/* P19: nói rõ đây là số liệu gì. */}
      <p className="mt-2 text-[15px] leading-relaxed text-[#475569]">
        Mỗi dòng là một buổi trong tuần, lớp nào còn chỗ xem ở trang đăng ký. Lịch do thầy cập nhật khi mở lớp.
      </p>
      <p className="mt-3">
        <Link href="/khoa-hoc" className={`${btn} bg-[#155e75] text-white hover:bg-[#0e7490]`}>
          Xem chi tiết và đăng ký <ArrowRight size={18} />
        </Link>
      </p>
    </div>
  );
}

export default function ForParents({ courses = null }: { courses?: HomeCourse[] | null }) {
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
            trung tâm.
          </p>

          <ClassSchedule courses={courses} />

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
