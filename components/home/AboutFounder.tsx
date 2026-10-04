import Image from "next/image";
import Link from "next/link";
import { Reveal } from "@/components/ui/Reveal";
import { CONTACT } from "@/lib/contact";

// Dữ kiện do chính thầy xác nhận (4/10/2026) — không suy diễn thêm bằng cấp/giải thưởng ngoài danh sách này.
const facts = [
  {
    label: "Hiện tại",
    value: `Giảng viên ngành Cơ khí, ${CONTACT.school} — đứng lớp CNC, tiện, phay`,
  },
  {
    label: "Học vấn",
    value: "Thạc sĩ Đại học Bách khoa TP.HCM · Á khoa đầu vào Đại học Sư phạm Kỹ thuật TP.HCM",
  },
  {
    label: "Dạy THPT",
    value: `Luyện Vật lý THPT hơn ${CONTACT.years} năm · KHTN 9, Vật lý 10–12 theo chương trình 2018`,
  },
  // Sở thích để 1 dòng, gần cuối khối — giữ vì là chất riêng của thầy, không phải bằng cấp.
  { label: "Ngoài giờ", value: "Cơ khí chế tạo · Trượt băng nghệ thuật · Gym mỗi ngày" },
];

const socials = [
  { label: "Facebook", href: "https://www.facebook.com/ngodieuthach" },
  { label: "Instagram", href: "https://www.instagram.com/ngo_dieu_thach" },
  { label: "TikTok", href: "https://www.tiktok.com/@ngo_dieu_thach" },
];

/**
 * Khối "Người đứng lớp" — sắp theo thứ tự phụ huynh cần khi tìm chỗ học cho con:
 * ảnh thật (bên trái, trên cùng ở mobile) → số năm luyện THPT + á khoa (trả lời "có nắm chương trình
 * phổ thông không") → nghề chính Cơ khí/Cao Thắng kể như lý do cách dạy khác đi → câu nói về cách dạy
 * → link tới bằng chứng điểm thi ở /phu-huynh → bảng dữ kiện quét nhanh → sở thích (1 dòng) → mạng xã hội.
 * Thứ tự này chốt 4/10/2026 sau khi bàn về cảm nhận của phụ huynh với chữ "cao đẳng": kinh nghiệm THPT
 * và bằng chứng đi trước, chức danh đi sau. Tránh chữ "dạy thêm".
 * Chỉ dùng dữ kiện thầy đã xác nhận (xem `facts`) và lib/contact.ts: không thêm thành tích nào khác.
 */
export default function AboutFounder() {
  const hasPhoto = Boolean(CONTACT.teacherPhoto);

  return (
    <section id="about" className="scroll-mt-20 border-t border-line py-20 lg:py-28">
      <div className="mx-auto grid max-w-6xl gap-12 px-6 lg:grid-cols-12 lg:gap-16 lg:px-8">
        {hasPhoto && (
          <Reveal className="lg:col-span-5">
            <Image
              src={CONTACT.teacherPhoto}
              alt="Thầy Thạch chụp cùng học sinh trong lớp học"
              width={800}
              height={600}
              sizes="(min-width: 1024px) 460px, (min-width: 640px) 88vw, 100vw"
              loading="lazy"
              className="h-auto w-full rounded-2xl border border-line"
            />
          </Reveal>
        )}

        <Reveal delay={0.1} className={hasPhoto ? "lg:col-span-7" : "lg:col-span-12"}>
          <p className="font-mono text-xs uppercase tracking-widest text-cyan-300">Người đứng lớp</p>
          <h2 className="mt-3 font-display text-3xl font-bold tracking-tight text-ink sm:text-4xl">
            Một chút về thầy Thạch
          </h2>
          <p className="mt-5 font-display text-lg leading-snug text-ink">
            Hơn {CONTACT.years} năm luyện Vật lý THPT và giảng dạy cơ khí chế tạo
          </p>
          <p className="mt-4 text-base leading-relaxed text-muted">
            Thầy luyện Vật lý THPT từ hơn {CONTACT.years} năm nay, từng đậu á khoa Đại học Sư phạm Kỹ
            thuật TP.HCM. Hiện thầy dạy KHTN 9 và Vật lý 10–12 theo chương trình 2018, không dạy chính
            khoá ở trường phổ thông nào.
          </p>
          <p className="mt-4 text-base leading-relaxed text-muted">
            Nghề chính của thầy là giảng viên ngành Cơ khí tại {CONTACT.school}, một trong những
            trường đào tạo kỹ sư thực hành hàng đầu Việt Nam. Thầy giảng dạy cơ khí chế tạo — tiện, phay,
            CNC — cùng sinh viên, nên với thầy vật lý chưa bao giờ chỉ nằm trên giấy: mỗi kiến thức
            đều phải đi kèm một ví dụ cụ thể ngoài đời — lực ma sát là chuyện bánh xe, áp suất là chuyện
            nồi áp suất trong bếp — để em hiểu và dùng được, không học thuộc để trả bài.
          </p>
          <blockquote className="mt-8 border-l-2 border-cyan-300 pl-5">
            <p className="font-display text-xl italic leading-snug text-ink">
              &ldquo;Mỗi kiến thức phải gắn với một ví dụ cụ thể trong cuộc sống.&rdquo;
            </p>
          </blockquote>
          <p className="mt-4 text-base leading-relaxed text-muted">
            <Link
              href="/phu-huynh#ket-qua"
              className="font-medium text-cyan-300 underline-offset-4 transition hover:text-cyan-200 hover:underline"
            >
              Xem điểm thi tốt nghiệp 2025 của học trò →
            </Link>
          </p>
          <p className="mt-6 text-base leading-relaxed text-muted">
            ThachLab là nơi thầy gom bài giảng, bài tập và đề kiểm tra của tất cả các lớp đó vào một
            chỗ, để em học ở nhà vẫn theo đúng nhịp trên lớp.
          </p>

          <dl className="mt-8 divide-y divide-line border-y border-line">
            {facts.map((f) => (
              <div key={f.label} className="grid gap-1 py-4 sm:grid-cols-[6.5rem_1fr]">
                <dt className="font-mono text-xs uppercase tracking-widest text-muted">{f.label}</dt>
                <dd className="text-sm text-ink">{f.value}</dd>
              </div>
            ))}
            <div className="grid gap-1 py-4 sm:grid-cols-[6.5rem_1fr]">
              <dt className="font-mono text-xs uppercase tracking-widest text-muted">Theo dõi</dt>
              <dd className="text-sm text-ink">
                <span className="flex flex-wrap gap-x-4 gap-y-1">
                  {socials.map((s) => (
                    <a
                      key={s.label}
                      href={s.href}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="font-medium text-cyan-300 underline-offset-4 transition hover:text-cyan-200 hover:underline"
                    >
                      {s.label}
                    </a>
                  ))}
                </span>
                <span className="mt-1 block text-muted">3.300+ người theo dõi trên Facebook</span>
              </dd>
            </div>
          </dl>
        </Reveal>
      </div>
    </section>
  );
}
