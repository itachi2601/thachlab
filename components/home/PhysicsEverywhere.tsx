const scenes = [
  {
    tag: "Trượt băng tốc độ",
    formula: "F_ms = μN",
    title: "Vì sao lưỡi giày trượt lại mỏng?",
    desc: "Giảm diện tích tiếp xúc để tăng áp suất lên mặt băng, làm giảm ma sát — chính là bài học về lực ma sát trong chương trình Lớp 10.",
  },
  {
    tag: "Phòng gym",
    formula: "A = F·s",
    title: "Một hiệp deadlift sinh ra bao nhiêu công?",
    desc: "Mỗi lần nâng tạ là một bài toán công và năng lượng — cơ thể chuyển hoá năng lượng hoá học thành công cơ học thực tế.",
  },
  {
    tag: "Cơ khí chế tạo",
    formula: "τ = F·d",
    title: "Cờ lê dài hơn, siết bu-lông dễ hơn?",
    desc: "Mô-men lực giải thích vì sao cánh tay đòn dài lại tạo ra lực xoắn lớn hơn với cùng một lực tác dụng.",
  },
];

export default function PhysicsEverywhere() {
  return (
    <section id="physics-everywhere" className="py-24 lg:py-32">
      <div className="mx-auto max-w-6xl px-6 lg:px-8">
        <div className="max-w-xl">
          <p className="font-mono text-xs font-medium uppercase tracking-widest text-primary">
            Vật lý quanh ta
          </p>
          <h2 className="mt-4 font-display text-3xl font-bold tracking-tight text-ink sm:text-4xl">
            Công thức bước ra khỏi trang sách.
          </h2>
          <p className="mt-4 text-base leading-relaxed text-muted">
            Từ đường băng, phòng tập đến xưởng cơ khí — Vật lý luôn ở đó. Chúng
            tôi tin rằng cách tốt nhất để hiểu một định luật là nhìn thấy nó
            vận hành trong đời sống.
          </p>
        </div>

        <div className="mt-16 grid grid-cols-1 gap-6 lg:grid-cols-3">
          {scenes.map((s) => (
            <article
              key={s.title}
              className="flex flex-col justify-between rounded-3xl border border-line bg-white p-8 transition-shadow hover:shadow-xl hover:shadow-primary/5"
            >
              <div>
                <div className="flex items-center justify-between">
                  <span className="rounded-full bg-primary/5 px-3 py-1 text-xs font-medium text-primary">
                    {s.tag}
                  </span>
                  <span className="font-mono text-sm text-accent">
                    {s.formula}
                  </span>
                </div>
                <h3 className="mt-6 font-display text-lg font-semibold leading-snug text-ink">
                  {s.title}
                </h3>
                <p className="mt-3 text-sm leading-relaxed text-muted">
                  {s.desc}
                </p>
              </div>
            </article>
          ))}
        </div>
      </div>
    </section>
  );
}
