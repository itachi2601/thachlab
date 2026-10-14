import { Reveal } from "@/components/ui/Reveal";

// Lời nhắn thật của học trò, trích từ album "Những lời yêu thương từ học trò" trên Facebook của thầy Thạch.
// Chỉ giữ 3 câu ngắn + 1 ảnh gốc làm bằng chứng (K3, 14/10/2026): 13 ảnh chụp xếp 3 cột là tường chữ nhỏ, vượt ngưỡng đọc ở 375px (N1, C2).
// Câu trích chép lại từ ảnh, chỉ sửa lỗi gõ; không kèm tên học sinh.
const quotes = [
  "Nhờ có những buổi dạy của thầy, con đã từ một người rất sợ Lý, giờ đây đã dám mơ ước học ngành Vật lý học.",
  "Cái con mới nhận ra là thầy chính là người mà con luôn muốn noi theo, con cũng muốn truyền tải về ngành nhà giáo tuyệt vời như thế nào.",
  "Một câu mà con nhớ như in từ thầy: “Học để chọn được nghề mình muốn”.",
];

export default function Testimonials() {
  return (
    <section className="border-t border-line py-16 lg:py-24">
      <div className="mx-auto max-w-6xl px-6 lg:px-8">
        <Reveal className="max-w-xl">
          <p className="font-mono text-xs uppercase tracking-widest text-primary">Học trò nói gì</p>
          <h2 className="mt-3 font-display text-3xl font-bold tracking-tight text-ink sm:text-4xl">Lời nhắn từ học trò</h2>
          <p className="mt-4 text-base leading-relaxed text-muted">
            Không phải lời chứng thực được biên tập: đây là tin nhắn học trò gửi thầy Thạch sau mỗi mùa thi.
          </p>
        </Reveal>

        <div className="mt-10 grid gap-8 lg:grid-cols-[1fr_320px] lg:items-start">
          <div className="space-y-5">
            {quotes.map((q) => (
              <Reveal key={q}>
                <blockquote className="border-l-4 border-primary pl-4 text-lg leading-relaxed text-ink">{q}</blockquote>
              </Reveal>
            ))}
            <p className="text-sm text-muted">
              Trích từ tin nhắn học trò, đã sửa lỗi gõ và lược tên. Còn nhiều lời nhắn khác trong album{" "}
              <a
                href="https://www.facebook.com/ngodieuthach"
                target="_blank"
                rel="noopener noreferrer"
                className="font-medium text-primary hover:underline"
              >
                &ldquo;Những lời yêu thương từ học trò&rdquo;
              </a>{" "}
              trên Facebook của thầy.
            </p>
          </div>

          <Reveal>
            <figure className="overflow-hidden rounded-xl border border-line">
              {/* eslint-disable-next-line @next/next/no-img-element */}
              <img
                src="/images/testimonials/melbourne.jpg"
                alt="Ảnh chụp tin nhắn gốc: học trò báo tin trúng tuyển ngành Giáo dục, Đại học Melbourne và muốn trở thành giáo viên như thầy"
                loading="lazy"
                decoding="async"
                className="w-full"
              />
              <figcaption className="border-t border-line px-3 py-2 text-sm text-muted">Ảnh chụp tin nhắn gốc</figcaption>
            </figure>
          </Reveal>
        </div>
      </div>
    </section>
  );
}
