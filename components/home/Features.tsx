const features = [
  {
    label: "01",
    title: "Hiểu bản chất, không học vẹt",
    desc: "Mỗi bài học bắt đầu bằng một câu hỏi thực tế, dẫn dắt học sinh tự suy luận ra công thức thay vì ghi nhớ máy móc.",
  },
  {
    label: "02",
    title: "Trực quan hoá mọi hiện tượng",
    desc: "Mô phỏng chuyển động, dao động, điện trường... được minh hoạ sinh động, giúp khái niệm trừu tượng trở nên dễ hình dung.",
  },
  {
    label: "03",
    title: "Phân hoá theo năng lực",
    desc: "Bài tập trải dài từ nhận biết, thông hiểu đến vận dụng cao, phù hợp với từng học sinh trong mọi giai đoạn ôn luyện.",
  },
  {
    label: "04",
    title: "Bám sát chương trình mới",
    desc: "Nội dung được xây dựng theo đúng Chương trình GDPT 2018, tương thích Cánh Diều, Kết nối tri thức và Chân trời sáng tạo.",
  },
];

export default function Features() {
  return (
    <section id="features" className="bg-white py-24 lg:py-32">
      <div className="mx-auto max-w-6xl px-6 lg:px-8">
        <div className="max-w-xl">
          <p className="font-mono text-xs font-medium uppercase tracking-widest text-primary">
            Vì sao ThachLab
          </p>
          <h2 className="mt-4 font-display text-3xl font-bold tracking-tight text-ink sm:text-4xl">
            Được thiết kế cho cách học sinh thực sự hiểu Vật lý.
          </h2>
        </div>

        <div className="mt-16 grid grid-cols-1 gap-px overflow-hidden rounded-3xl border border-line bg-line sm:grid-cols-2">
          {features.map((f) => (
            <div
              key={f.label}
              className="group flex flex-col gap-4 bg-white p-8 transition-colors hover:bg-bg lg:p-10"
            >
              <span className="font-mono text-sm text-accent">{f.label}</span>
              <h3 className="font-display text-xl font-semibold text-ink">
                {f.title}
              </h3>
              <p className="text-sm leading-relaxed text-muted">{f.desc}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
