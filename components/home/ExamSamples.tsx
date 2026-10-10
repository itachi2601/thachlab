import Link from "next/link";
import { readExamSampleCards } from "@/components/home/exam-samples.server";
import { examSampleLine } from "@/components/home/exam-sample-types";

/**
 * Dải 3 đề mẫu sau mục "Cách học".
 * N2: đúng 3 thẻ. B2: cả thẻ là một liên kết, không thêm nút nổi thứ hai.
 * C1: dòng đọc ≥ 16px. D2: cả thẻ là đích chạm.
 */
export default function ExamSamples() {
  const cards = readExamSampleCards();
  if (cards.length === 0) return null;

  return (
    <section id="de-thi" className="border-t border-line py-20 lg:py-28">
      <div className="mx-auto max-w-6xl px-6 lg:px-8">
        <p className="font-mono text-xs uppercase tracking-widest text-primary">Đề các năm</p>
        <h2 className="mt-3 font-display text-3xl font-bold tracking-tight text-ink sm:text-4xl">
          Đề kiểm tra các năm
        </h2>
        <ul className="mt-8 grid gap-4 lg:grid-cols-3">
          {cards.map((card) => (
            <li key={card.id}>
              <Link
                href={`/kiem-tra/xem-thu?id=${card.id}`}
                className="flex min-h-14 flex-col rounded-xl border border-line px-5 py-4 transition hover:border-primary/50"
              >
                <span className="text-lg font-semibold leading-snug text-ink">{examSampleLine(card)}</span>
                <span className="mt-1 text-base text-muted">
                  {card.questionCount} câu · {card.durationMinutes} phút
                </span>
                <span className="mt-3 text-base font-medium text-primary">Làm miễn phí</span>
              </Link>
            </li>
          ))}
        </ul>
        <p className="mt-6 max-w-2xl text-base leading-relaxed text-muted">
          Đang thử nghiệm đến 2027. Em đăng ký, làm bài, gặp chỗ sai thì báo giúp thầy.
        </p>
      </div>
    </section>
  );
}
