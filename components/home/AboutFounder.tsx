const traits = [
  { label: "Giảng dạy", value: "KHTN 9 & Vật lý THPT" },
  { label: "Đam mê", value: "Cơ khí chế tạo" },
  { label: "Thể thao", value: "Trượt băng tốc độ" },
  { label: "Rèn luyện", value: "Gym mỗi ngày" },
];

export default function AboutFounder() {
  return (
    <section id="about" className="py-24 lg:py-32">
      <div className="mx-auto max-w-6xl px-6 lg:px-8">
        <div className="grid grid-cols-1 items-start gap-16 lg:grid-cols-[0.9fr_1.1fr]">
          <div>
            <p className="font-mono text-xs font-medium uppercase tracking-widest text-primary">
              Người sáng lập
            </p>
            <h2 className="mt-4 font-display text-3xl font-bold tracking-tight text-ink sm:text-4xl">
              Một giáo viên Vật lý, một người luôn đặt câu hỏi.
            </h2>
            <p className="mt-6 text-base leading-relaxed text-muted">
              ThachLab được sáng lập bởi một giáo viên Vật lý trực tiếp giảng
              dạy KHTN 9 và chương trình THPT. Với niềm yêu thích cơ khí chế
              tạo, những giờ trên đường trượt băng tốc độ và phòng gym, mọi bài
              giảng đều bắt nguồn từ một điều đơn giản: mỗi bài học nên bắt
              đầu bằng một câu hỏi.
            </p>

            <blockquote className="mt-8 border-l-2 border-accent pl-6">
              <p className="font-display text-xl italic leading-snug text-ink">
                &ldquo;Hiểu bản chất, không học thuộc công thức.&rdquo;
              </p>
            </blockquote>
          </div>

          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
            {traits.map((t) => (
              <div
                key={t.label}
                className="rounded-3xl border border-line bg-white p-6"
              >
                <p className="font-mono text-xs uppercase tracking-widest text-muted">
                  {t.label}
                </p>
                <p className="mt-2 font-display text-lg font-semibold text-ink">
                  {t.value}
                </p>
              </div>
            ))}

            <div className="col-span-full rounded-3xl bg-primary p-6">
              <p className="font-mono text-xs uppercase tracking-widest text-white/70">
                Triết lý giảng dạy
              </p>
              <p className="mt-2 font-display text-lg font-semibold text-white">
                Mỗi bài học bắt đầu bằng một câu hỏi.
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
