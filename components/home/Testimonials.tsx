const testimonials = [
  {
    quote:
      "Trước đây em học thuộc công thức để làm bài, giờ em hiểu vì sao công thức đó tồn tại. Điểm kiểm tra tăng rõ rệt.",
    name: "Minh Anh",
    role: "Học sinh Lớp 11",
  },
  {
    quote:
      "Cách thầy liên hệ Vật lý với thể thao và đời sống khiến những chương khó như Điện trường trở nên dễ hiểu hơn nhiều.",
    name: "Gia Bảo",
    role: "Học sinh Lớp 11",
  },
  {
    quote:
      "Phiếu bài tập phân hoá rõ ràng theo từng mức độ giúp em tự lượng sức và ôn thi tốt nghiệp hiệu quả hơn.",
    name: "Thuỳ Trang",
    role: "Học sinh Lớp 12",
  },
];

export default function Testimonials() {
  return (
    <section className="bg-white py-24 lg:py-32">
      <div className="mx-auto max-w-6xl px-6 lg:px-8">
        <div className="max-w-xl">
          <p className="font-mono text-xs font-medium uppercase tracking-widest text-primary">
            Học sinh nói gì
          </p>
          <h2 className="mt-4 font-display text-3xl font-bold tracking-tight text-ink sm:text-4xl">
            Những thay đổi thật, từ những bài học thật.
          </h2>
        </div>

        <div className="mt-16 grid grid-cols-1 gap-6 lg:grid-cols-3">
          {testimonials.map((t) => (
            <figure
              key={t.name}
              className="flex h-full flex-col justify-between rounded-3xl border border-line bg-bg p-8"
            >
              <blockquote className="font-display text-lg leading-relaxed text-ink">
                &ldquo;{t.quote}&rdquo;
              </blockquote>
              <figcaption className="mt-8 flex items-center gap-3">
                <span className="flex h-10 w-10 items-center justify-center rounded-full bg-primary/10 font-display text-sm font-semibold text-primary">
                  {t.name.charAt(0)}
                </span>
                <div>
                  <p className="text-sm font-semibold text-ink">{t.name}</p>
                  <p className="text-xs text-muted">{t.role}</p>
                </div>
              </figcaption>
            </figure>
          ))}
        </div>
      </div>
    </section>
  );
}
