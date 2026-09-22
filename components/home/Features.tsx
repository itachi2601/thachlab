import Link from "next/link";
import { ArrowRight } from "lucide-react";
import { Reveal } from "@/components/ui/Reveal";

const steps = [
  {
    title: "Lý thuyết trọng tâm",
    desc: "Ngắn gọn, đúng yêu cầu cần đạt của chương trình 2018, có công thức và hình minh họa đi kèm.",
  },
  {
    title: "Bài tập mẫu",
    desc: "Làm thử vài câu ngay sau phần lý thuyết, chấm tại chỗ để biết mình đã hiểu chưa.",
  },
  {
    title: "Luyện tập và bài tập về nhà",
    desc: "Mỗi câu hỏi được gắn nhãn theo chủ đề và dạng bài. Làm sai câu nào, em biết ngay cần ôn lại phần nào.",
  },
  {
    title: "Kiểm tra",
    desc: "Bài kiểm tra chương, giữa kì và cuối kì chấm tự động, kèm phân tích kết quả và chủ đề cần phụ đạo.",
  },
];

export default function Features() {
  return (
    <section id="features" className="border-t border-line py-20 lg:py-28">
      <div className="mx-auto grid max-w-6xl gap-12 px-6 lg:grid-cols-12 lg:gap-16 lg:px-8">
        <Reveal className="lg:col-span-5">
          <p className="font-mono text-xs uppercase tracking-widest text-cyan-300">Cách học</p>
          <h2 className="mt-3 font-display text-3xl font-bold tracking-tight text-ink sm:text-4xl">
            Một bài học trên ThachLab diễn ra thế nào
          </h2>
          <p className="mt-5 text-base leading-relaxed text-muted">
            Mỗi bài bắt đầu bằng một câu hỏi từ đời thường — như con lắc lò xo ở đầu
            trang — rồi mới đến lý thuyết. Phần còn lại em làm ngay trên web: bài tập
            mẫu, luyện tập, bài về nhà và kiểm tra đều được chấm tự động.
          </p>
          <Link
            href="/lop-hoc"
            className="mt-6 inline-flex items-center gap-1.5 text-sm font-medium text-cyan-300 transition hover:text-cyan-200"
          >
            Xem các lớp đang mở <ArrowRight size={16} />
          </Link>
        </Reveal>

        <Reveal delay={0.1} className="lg:col-span-7">
          <ol className="divide-y divide-line border-y border-line">
            {steps.map((s, i) => (
              <li key={s.title} className="grid gap-2 py-5 sm:grid-cols-[3.5rem_1fr] sm:gap-6">
                <span className="font-mono text-sm text-cyan-300">0{i + 1}</span>
                <div>
                  <h3 className="font-display text-lg font-semibold text-ink">{s.title}</h3>
                  <p className="mt-1 text-sm leading-relaxed text-muted">{s.desc}</p>
                </div>
              </li>
            ))}
          </ol>
        </Reveal>
      </div>
    </section>
  );
}
