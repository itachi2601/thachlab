import { Reveal } from "@/components/ui/Reveal";

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
    <section id="features" className="relative overflow-hidden py-24 lg:py-32">
      <div
        aria-hidden
        className="glow-blob left-[30%] top-[40%] h-[340px] w-[340px] bg-cyan-600/20"
      />
      <div className="relative mx-auto max-w-6xl px-6 lg:px-8">
        <Reveal className="max-w-xl">
          <p className="font-mono text-xs font-medium uppercase tracking-widest text-cyan-300">
            Vì sao ThachLab
          </p>
          <h2 className="mt-4 font-display text-3xl font-bold tracking-tight text-ink sm:text-4xl">
            Được thiết kế cho cách học sinh{" "}
            <span className="text-gradient">thực sự hiểu Vật lý.</span>
          </h2>
        </Reveal>

        <div className="mt-16 grid grid-cols-1 gap-5 sm:grid-cols-2">
          {features.map((f, i) => (
            <Reveal key={f.label} delay={i * 0.08}>
              <div className="glass glass-hover flex h-full flex-col gap-4 rounded-3xl p-8 lg:p-10">
                <span className="font-mono text-sm text-accent">{f.label}</span>
                <h3 className="font-display text-xl font-semibold text-ink">
                  {f.title}
                </h3>
                <p className="text-sm leading-relaxed text-muted">{f.desc}</p>
              </div>
            </Reveal>
          ))}
        </div>
      </div>
    </section>
  );
}
