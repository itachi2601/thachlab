import Link from "next/link";
import { ArrowRight, Check } from "lucide-react";
import { Reveal } from "@/components/ui/Reveal";

const stages = [
  {
    grade: "KHTN 9",
    classHref: "/lop-hoc/khtn-9",
    articleHref: "/blog/lo-trinh-hoc-khtn-9-phan-vat-ly-thi-chuyen",
    focus: "Nền tảng KHTN, định hướng thi chuyên",
    detail:
      "Học chắc kiến thức cốt lõi phần Vật lý của KHTN 9, biết liên hệ hiện tượng thực tế và làm quen với bài tổng hợp.",
    topics: ["Vật lý", "Hóa học", "Sinh học", "Ôn tập KHTN"],
    checkpoints: ["Nắm kiến thức trọng tâm", "Biết liên hệ thực tế", "Làm được bài tổng hợp KHTN"],
    image: "/images/learning-path/khtn-9-vat-ly.webp",
  },
  {
    grade: "Lớp 10",
    classHref: "/lop-hoc/lop-10",
    articleHref: "/blog/lo-trinh-hoc-vat-ly-lop-10-dung-de-mat-goc",
    focus: "Nhập môn và nền tảng cơ học",
    detail:
      "Làm quen cách học mới: ít toán đố, nhiều thực tế. Trọng tâm là đọc – vẽ đồ thị chuyển động và vẽ lực cho đúng.",
    topics: ["Động học", "Định luật Newton", "Năng lượng", "Chuyển động tròn"],
    checkpoints: ["Đọc được đồ thị chuyển động", "Vẽ lực đúng", "Biết dùng bảo toàn năng lượng"],
    image: "/images/learning-path/vat-ly-10.jpg",
  },
  {
    grade: "Lớp 11",
    classHref: "/lop-hoc/lop-11",
    articleHref: "/blog/lo-trinh-hoc-vat-ly-lop-11-nam-de-duoi-nhat",
    focus: "Dao động, sóng và điện",
    detail:
      "Năm có nhiều khái niệm trừu tượng nhất. Học chắc bản chất qua thí nghiệm, mô phỏng và đồ thị.",
    topics: ["Dao động", "Sóng cơ & ánh sáng", "Điện trường", "Dòng điện không đổi"],
    checkpoints: ["Phân tích được dao động", "Hiểu sóng và ánh sáng", "Làm chủ điện trường, mạch DC"],
    image: "/images/learning-path/vat-ly-11.jpg",
  },
  {
    grade: "Lớp 12",
    classHref: "/lop-hoc/lop-12",
    articleHref: "/blog/lo-trinh-hoc-vat-ly-lop-12-muon-tang-diem",
    focus: "Nhiệt, khí và vật lý hiện đại",
    detail:
      "Điểm mới của chương trình 2018: Nhiệt học chuyển lên lớp 12, bớt điện xoay chiều phức tạp. Luyện đề theo đúng cấu trúc thi mới.",
    topics: ["Vật lý nhiệt", "Khí lý tưởng", "Từ trường", "Lượng tử & hạt nhân"],
    checkpoints: ["Giải bài nhiệt, khí", "Hiểu từ trường", "Luyện đề theo cấu trúc thi"],
    image: "/images/learning-path/vat-ly-12.jpg",
  },
];

export default function LearningPath() {
  return (
    <section id="learning-path" className="scroll-mt-20 border-t border-line py-20 lg:py-28">
      <div className="mx-auto max-w-6xl px-6 lg:px-8">
        <Reveal className="max-w-2xl">
          <p className="font-mono text-xs uppercase tracking-widest text-cyan-300">Lộ trình lớp 9–12</p>
          <h2 className="mt-3 font-display text-3xl font-bold tracking-tight text-ink sm:text-4xl">
            Chọn lớp em đang học
          </h2>
          <p className="mt-4 text-base leading-relaxed text-muted">
            Chương trình 2018 xếp lại kiến thức khá khác trước, nên mỗi lớp có một
            trọng tâm riêng. Bài tổng quan cho cả ba năm THPT ở{" "}
            <Link
              href="/blog/lo-trinh-hoc-vat-ly-thpt-chuong-trinh-moi-2018"
              className="font-medium text-cyan-300 underline-offset-4 hover:underline"
            >
              đây
            </Link>
            .
          </p>
        </Reveal>

        <div className="mt-10 divide-y divide-line border-y border-line">
          {stages.map((s, i) => (
            <Reveal key={s.grade} delay={i * 0.06}>
              <article className="grid gap-6 py-8 md:grid-cols-[220px_1fr] md:gap-8 lg:grid-cols-[260px_1fr]">
                <Link
                  href={s.classHref}
                  className="block aspect-[4/3] overflow-hidden rounded-lg border border-line md:aspect-auto md:h-full"
                >
                  {/* eslint-disable-next-line @next/next/no-img-element */}
                  <img
                    src={s.image}
                    alt={`Sơ đồ tóm tắt chương trình ${s.grade}`}
                    loading="lazy"
                    decoding="async"
                    className="h-full w-full object-cover object-top"
                  />
                </Link>

                <div className="flex flex-col">
                  <p className="font-mono text-xs uppercase tracking-widest text-cyan-300">{s.grade}</p>
                  <h3 className="mt-1 font-display text-xl font-bold text-ink sm:text-2xl">{s.focus}</h3>
                  <p className="mt-2 max-w-2xl text-sm leading-relaxed text-muted">{s.detail}</p>

                  <div className="mt-4 grid gap-4 sm:grid-cols-2">
                    <div>
                      <p className="text-xs font-medium uppercase tracking-wider text-muted">Trọng tâm</p>
                      <p className="mt-1.5 text-sm text-ink">{s.topics.join(" · ")}</p>
                    </div>
                    <div>
                      <p className="text-xs font-medium uppercase tracking-wider text-muted">Mốc cần đạt</p>
                      <ul className="mt-1.5 space-y-1">
                        {s.checkpoints.map((c) => (
                          <li key={c} className="flex items-start gap-2 text-sm text-ink">
                            <Check size={14} className="mt-1 shrink-0 text-cyan-300" />
                            <span>{c}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  </div>

                  <div className="mt-5 flex flex-wrap items-center gap-x-6 gap-y-2">
                    <Link
                      href={s.classHref}
                      className="inline-flex items-center gap-1.5 text-sm font-semibold text-cyan-300 transition hover:text-cyan-200"
                    >
                      Vào lớp {s.grade.replace(/^Lớp /, "")} <ArrowRight size={16} />
                    </Link>
                    <Link
                      href={s.articleHref}
                      className="text-sm font-medium text-muted underline-offset-4 transition hover:text-ink hover:underline"
                    >
                      Đọc bài lộ trình
                    </Link>
                  </div>
                </div>
              </article>
            </Reveal>
          ))}
        </div>
      </div>
    </section>
  );
}
