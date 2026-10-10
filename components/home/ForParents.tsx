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

interface SessionGroup {
  /** "Buổi A" cho lớp 2 buổi/tuần; null cho khoá đơn. */
  label: string | null;
  sessions: HomeCourseSession[];
}

interface GradeRow {
  className: string;
  groups: SessionGroup[];
  /** Lớp học 2 buổi/tuần (có nhóm buổi A/B) → in câu "chọn một buổi A và một buổi B". */
  paired: boolean;
}

/**
 * Gom buổi theo khối. Khoá đơn: một nhóm không nhãn. Lớp tách buổi A/B (pairKey/pairSlot): mỗi loại buổi
 * một nhóm có nhãn, xếp A → B. Bỏ buổi trùng, xếp theo thứ rồi giờ. Tên lớp nội bộ ("10L3") không hiện (P8).
 */
function groupByGrade(courses: HomeCourse[]): GradeRow[] {
  type Bucket = Map<string, HomeCourseSession>;
  const byGrade = new Map<string, Map<string, { label: string | null; bucket: Bucket }>>();
  for (const c of courses) {
    const groups = byGrade.get(c.className) ?? new Map();
    const pairKeys = new Set(courses.filter((x) => x.className === c.className && x.pairKey).map((x) => x.pairKey));
    // Một khối có ≥2 lớp tách buổi thì nhãn kèm tên lớp để khỏi lẫn; thường chỉ có một lớp → "Buổi A".
    const label = c.pairSlot ? (pairKeys.size > 1 ? `${c.pairKey} · buổi ${c.pairSlot}` : `Buổi ${c.pairSlot}`) : null;
    const gKey = c.pairSlot ? `${pairKeys.size > 1 ? c.pairKey : ""}|${c.pairSlot}` : "";
    const g = groups.get(gKey) ?? { label, bucket: new Map() as Bucket };
    for (const s of c.schedules) g.bucket.set(`${s.weekday}|${s.start}|${s.end}|${s.location}`, s);
    groups.set(gKey, g);
    byGrade.set(c.className, groups);
  }
  const sortSessions = (a: HomeCourseSession, b: HomeCourseSession) =>
    a.weekday - b.weekday || a.start.localeCompare(b.start);
  return [...byGrade.entries()]
    .map(([className, groups]) => {
      const list = [...groups.entries()]
        .sort(([a], [b]) => a.localeCompare(b))
        .map(([, g]) => ({ label: g.label, sessions: [...g.bucket.values()].sort(sortSessions) }))
        .filter((g) => g.sessions.length > 0);
      return { className, groups: list, paired: list.some((g) => g.label !== null) };
    })
    .filter((g) => g.groups.length > 0)
    .sort((a, b) => Number(a.className) - Number(b.className) || a.className.localeCompare(b.className));
}

function SessionList({ sessions }: { sessions: HomeCourseSession[] }) {
  return (
    <ul className="flex flex-wrap gap-x-5 gap-y-1 text-lg leading-relaxed text-ink">
      {sessions.map((s) => (
        <li key={`${s.weekday}-${s.start}`} className="whitespace-nowrap">
          <span className="font-semibold text-ink">{WEEKDAY[s.weekday] ?? ""}</span>{" "}
          <span className="tabular-nums">
            {s.start}–{s.end}
          </span>
          {s.location && <span className="text-muted"> · {s.location}</span>}
        </li>
      ))}
    </ul>
  );
}

function ClassSchedule({ courses }: { courses: HomeCourse[] | null }) {
  const rows = courses ? groupByGrade(courses) : [];
  if (rows.length === 0) {
    // P9: trạng thái rỗng nói rõ vì sao + việc làm được (nút Zalo nằm ngay dưới).
    return (
      <p className="mt-5 max-w-xl text-lg leading-relaxed text-ink">
        Hiện chưa có lớp nào mở đăng ký. Khi thầy mở lớp mới, lịch sẽ hiện ở đây; anh chị nhắn Zalo để được
        báo trước.
      </p>
    );
  }
  const year = (courses?.find((c) => c.schoolYear)?.schoolYear ?? "").replace("-", "–");
  return (
    <div className="mt-5 max-w-2xl rounded-2xl border border-line bg-surface-2 px-5 py-4">
      <h3 className="font-display text-lg font-semibold">
        Lịch lớp học thêm{year ? ` năm học ${year}` : ""}
      </h3>
      <ul className="mt-1 divide-y divide-line">
        {rows.map((g) => (
          <li key={g.className} className="grid gap-y-1 py-3 sm:grid-cols-[5.5rem_1fr] sm:items-baseline">
            <span className="text-lg font-bold">Lớp {g.className}</span>
            <div className="space-y-1">
              {g.groups.map((grp, i) => (
                <div key={grp.label ?? i} className="flex flex-wrap items-baseline gap-x-3 gap-y-1">
                  {grp.label && (
                    <span className="text-[15px] font-semibold uppercase tracking-wide text-muted">{grp.label}</span>
                  )}
                  <SessionList sessions={grp.sessions} />
                </div>
              ))}
              {g.paired && (
                <p className="text-[18px] leading-relaxed text-muted">
                  Học hai buổi mỗi tuần: chọn một buổi A và một buổi B.
                </p>
              )}
            </div>
          </li>
        ))}
      </ul>
      {/* P19: nói rõ đây là số liệu gì. */}
      <p className="mt-2 text-[18px] leading-relaxed text-muted">
        Mỗi dòng là một buổi trong tuần, lớp nào còn chỗ xem ở trang đăng ký. Lịch do thầy cập nhật khi mở lớp.
      </p>
      <p className="mt-3">
        <Link href="/khoa-hoc" className={`${btn} bg-primary text-white hover:bg-primary-dark`}>
          Xem chi tiết và đăng ký <ArrowRight size={18} />
        </Link>
      </p>
    </div>
  );
}

export default function ForParents({ courses = null }: { courses?: HomeCourse[] | null }) {
  const phone = CONTACT.phone ? displayPhone(CONTACT.phone) : "";
  // Hai dòng giới thiệu, cùng thứ tự với khối "Một chút về thầy Thạch": kinh nghiệm THPT trước, nghề chính sau.
  const introLines = [
    CONTACT.years ? `Hơn ${CONTACT.years} năm luyện Vật lý THPT` : "",
    "Thạc sĩ Đại học Bách khoa TP.HCM",
    CONTACT.school ? `Giảng viên ngành Cơ khí, ${CONTACT.school}` : "",
  ].filter(Boolean);

  return (
    <section className="bg-panel px-6 py-10 text-ink lg:px-12">
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
          {introLines.map((line) => (
            <p key={line} className="mt-1 text-lg leading-snug text-ink">
              {line}
            </p>
          ))}
        </div>

        <div>
          <h2 className="font-display text-2xl font-bold">Dành cho phụ huynh</h2>
          <p className="mt-3 max-w-xl text-lg leading-relaxed text-ink">
            Bài trên web học miễn phí. Lớp học thêm tại {CONTACT.area.replace(/^Khu vực /i, "khu vực ")}; học phí đóng tại
            trung tâm.
          </p>

          <ClassSchedule courses={courses} />

          <ul className="mt-6 grid gap-5 sm:grid-cols-3">
            {QUESTIONS.map((q) => (
              <li key={q.title}>
                <h3 className="font-display text-lg font-semibold">{q.title}</h3>
                <p className="mt-1.5 text-lg leading-relaxed text-ink">{q.desc}</p>
                {q.href && (
                  <Link
                    href={q.href}
                    className="mt-2 inline-flex min-h-12 items-center gap-1 text-base font-semibold text-primary hover:underline"
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
                className={`${btn} bg-primary text-white hover:bg-primary-dark`}
              >
                <MessageCircle size={18} /> Nhắn Zalo cho thầy
              </a>
            )}
            {CONTACT.phone && (
              <a
                href={`tel:${CONTACT.phone}`}
                className={`${btn} border border-line-strong bg-panel text-ink hover:bg-surface-2`}
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
