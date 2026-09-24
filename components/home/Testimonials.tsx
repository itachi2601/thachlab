"use client";

import { useState } from "react";
import { ChevronDown } from "lucide-react";
import { Reveal } from "@/components/ui/Reveal";

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
    src: "/images/testimonials/thu-tay.webp",
    alt: "Bức thư dài của học trò: từ chỗ chọn đại thầy để học, sau ba năm đã dám mơ ước trở thành giáo viên Vật lý",
  },
  {
    src: "/images/testimonials/hoc-bong-diem-9.jpg",
    alt: "Tin nhắn học trò báo được học bổng, điểm trung bình Lý trên 9.0 — và lời đáp của thầy: giúp được các con yêu thích môn học là điều hạnh phúc nhất trong cuộc đời đi dạy",
  },
  {
    src: "/images/testimonials/tuan-anh.webp",
    alt: "Tin nhắn học trò: từ một người rất sợ Lý giờ đã dám mơ ước học ngành Vật lý học",
  },
  {
    src: "/images/testimonials/diem-9-ly.webp",
    alt: "Tin nhắn học trò báo đạt 9 điểm Vật lý và trân trọng kỷ niệm lớp học",
  },
  {
    src: "/images/testimonials/hoc-bong-uc.webp",
    alt: "Tin nhắn học trò báo trúng tuyển đại học hàng đầu ở Úc với học bổng cao",
  },
  {
    src: "/images/testimonials/nguoi-cha-thu-hai.webp",
    alt: "Tin nhắn học trò: thầy là nguồn cảm hứng thay đổi cả định hướng cuộc đời",
  },
  {
    src: "/images/testimonials/thu-phong-bi-xanh.webp",
    alt: "Thư tay của học trò viết trên giấy trắng, kèm phong bì xanh",
  },
  {
    src: "/images/testimonials/thu-gui-thay-thach.webp",
    alt: "Thư tay 'Gửi thầy Thạch' viết trên giấy kem của học trò lớp NP",
  },
  {
    src: "/images/testimonials/thiep-tri-an-vang.jpg",
    alt: "Thiệp tri ân màu vàng từ bộ ba học trò lớp 12CL2",
  },
  {
    src: "/images/testimonials/thu-giay-ke.webp",
    alt: "Thư tay của học trò viết kín một trang giấy kẻ ngang",
  },
  {
    src: "/images/testimonials/loi-tri-an-ca-lop.webp",
    alt: "Trang 'Lời tri ân' với lời nhắn nhiều màu mực của cả lớp gửi thầy",
  },
  {
    src: "/images/testimonials/thu-xuan-quynh-khanh-long.webp",
    alt: "Thư tay có chữ ký của hai học trò Xuân Quỳnh và Khánh Long",
  },
];

const INITIAL_COUNT = 5;

export default function Testimonials() {
  const [expanded, setExpanded] = useState(false);
  const visible = expanded ? messages : messages.slice(0, INITIAL_COUNT);
  const hidden = messages.length - INITIAL_COUNT;

  return (
    <section className="border-t border-line py-20 lg:py-28">
      <div className="mx-auto max-w-6xl px-6 lg:px-8">
        <Reveal className="max-w-xl">
          <p className="font-mono text-xs uppercase tracking-widest text-cyan-300">Học trò nói gì</p>
          <h2 className="mt-3 font-display text-3xl font-bold tracking-tight text-ink sm:text-4xl">
            Lời nhắn từ học trò
          </h2>
          <p className="mt-4 text-base leading-relaxed text-muted">
            Không phải lời chứng thực được biên tập — đây là tin nhắn và thư tay học
            trò gửi thầy Thạch sau mỗi mùa thi, mỗi lần báo tin đỗ đạt.
          </p>
        </Reveal>

        <div className="mt-12 columns-1 gap-5 sm:columns-2 lg:columns-3">
          {visible.map((m, i) => (
            <Reveal key={m.src} delay={i < INITIAL_COUNT ? (i % 3) * 0.06 : 0} className="mb-5 break-inside-avoid">
              <figure className="overflow-hidden rounded-xl border border-line transition-colors hover:border-cyan-400/40">
                {/* eslint-disable-next-line @next/next/no-img-element */}
                <img src={m.src} alt={m.alt} loading="lazy" decoding="async" className="w-full" />
              </figure>
            </Reveal>
          ))}
        </div>

        <div className="mt-8 flex flex-col items-center gap-4 text-center">
          <button
            type="button"
            onClick={() => setExpanded((v) => !v)}
            aria-expanded={expanded}
            className="inline-flex items-center gap-2 rounded-lg border border-line px-5 py-2.5 text-sm font-medium text-ink transition hover:bg-white/5"
          >
            {expanded ? "Thu gọn" : `Xem thêm ${hidden} lời nhắn`}
            <ChevronDown size={16} className={`transition-transform ${expanded ? "rotate-180" : ""}`} />
          </button>
          <p className="text-sm text-muted">
            Trích từ album{" "}
            <a
              href="https://www.facebook.com/ngodieuthach"
              target="_blank"
              rel="noopener noreferrer"
              className="font-medium text-cyan-300 hover:underline"
            >
              &ldquo;Những lời yêu thương từ học trò&rdquo;
            </a>{" "}
            trên Facebook của thầy Thạch.
          </p>
        </div>
      </div>
    </section>
  );
}
