// Ảnh chụp tin nhắn thật từ học trò — trích từ album "Những lời yêu thương
// từ học trò" trên Facebook của thầy Thạch. Ảnh nào lộ tên học sinh đã được
// che/crop trước khi đăng.
const messages = [
  {
    src: "/images/testimonials/melbourne.jpg",
    alt: "Tin nhắn học trò báo tin trúng tuyển ngành Education, Đại học Melbourne và muốn trở thành giáo viên như thầy",
  },
  {
    src: "/images/testimonials/diem-875-ly.jpg",
    alt: "Tin nhắn học trò khoe đạt 8,75 điểm Vật lý và cảm ơn thầy",
  },
  {
    src: "/images/testimonials/thu-tay.jpg",
    alt: "Bức thư dài của học trò: từ chỗ chọn đại thầy để học, sau ba năm đã dám mơ ước trở thành giáo viên Vật lý",
  },
  {
    src: "/images/testimonials/diem-9-ly.jpg",
    alt: "Tin nhắn học trò báo đạt 9 điểm Vật lý và trân trọng kỷ niệm lớp học",
  },
  {
    src: "/images/testimonials/hoc-bong-uc.jpg",
    alt: "Tin nhắn học trò báo trúng tuyển đại học hàng đầu ở Úc với học bổng cao",
  },
  {
    src: "/images/testimonials/tuan-anh.jpg",
    alt: "Tin nhắn học trò: từ một người rất sợ Lý giờ đã dám mơ ước học ngành Vật lý học",
  },
  {
    src: "/images/testimonials/nguoi-cha-thu-hai.jpg",
    alt: "Tin nhắn học trò: thầy là nguồn cảm hứng thay đổi cả định hướng cuộc đời",
  },
];

export default function Testimonials() {
  return (
    <section className="bg-white py-24 lg:py-32">
      <div className="mx-auto max-w-6xl px-6 lg:px-8">
        <div className="max-w-xl">
          <p className="font-mono text-xs font-medium uppercase tracking-widest text-[#2563EB]">
            Học sinh nói gì
          </p>
          <h2 className="mt-4 font-display text-3xl font-bold tracking-tight text-ink sm:text-4xl">
            Những lời yêu thương từ học trò.
          </h2>
          <p className="mt-4 text-base leading-relaxed text-muted">
            Không phải lời chứng thực được biên tập — đây là những tin nhắn
            thật học trò gửi cho thầy Thạch sau mỗi mùa thi, mỗi lần báo tin
            đỗ đạt.
          </p>
        </div>

        <div className="mt-16 columns-1 gap-6 sm:columns-2 lg:columns-3">
          {messages.map((m) => (
            <figure key={m.src} className="mb-6 break-inside-avoid">
              {/* eslint-disable-next-line @next/next/no-img-element */}
              <img
                src={m.src}
                alt={m.alt}
                loading="lazy"
                className="w-full rounded-2xl border border-line shadow-sm"
              />
            </figure>
          ))}
        </div>

        <p className="mt-10 text-center text-sm text-muted">
          Trích từ album{" "}
          <a
            href="https://www.facebook.com/ngodieuthach"
            target="_blank"
            rel="noopener noreferrer"
            className="font-medium text-[#2563EB] hover:underline"
          >
            &ldquo;Những lời yêu thương từ học trò&rdquo;
          </a>{" "}
          trên Facebook của thầy Thạch.
        </p>
      </div>
    </section>
  );
}
