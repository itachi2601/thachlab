import { CONTACT } from "@/lib/contact";

const columns = [
  {
    title: "Lớp học",
    links: [
      { label: "KHTN 9", href: "/lop-hoc/khtn-9" },
      { label: "Vật lý 10", href: "/lop-hoc/lop-10" },
      { label: "Vật lý 11", href: "/lop-hoc/lop-11" },
      { label: "Vật lý 12", href: "/lop-hoc/lop-12" },
      { label: "Sinh viên CTTC", href: "/lop-hoc/cttc" },
    ],
  },
  {
    title: "ThachLab",
    links: [
      { label: "Về thầy Thạch", href: "/#about" },
      { label: "Cách học trên ThachLab", href: "/#features" },
      { label: "Blog", href: "/blog" },
      { label: "Phụ huynh xem kết quả của con", href: "/phu-huynh" },
    ],
  },
  {
    title: "Kết nối",
    links: [
      { label: "Facebook", href: "https://www.facebook.com/ngodieuthach" },
      { label: "Instagram", href: "https://www.instagram.com/ngo_dieu_thach" },
      { label: "TikTok", href: "https://www.tiktok.com/@ngo_dieu_thach" },
    ],
  },
];

// Cột "Liên hệ" lấy từ lib/contact.ts — giá trị nào thầy chưa điền thì bỏ dòng đó, không render
// link rỗng; cả cột không còn dòng nào thì không render (giữ nguyên lưới 4 cột như trước).
const contactItems: { label: string; href?: string }[] = [];
if (CONTACT.phone) contactItems.push({ label: `Gọi ${CONTACT.phone}`, href: `tel:${CONTACT.phone}` });
if (CONTACT.zalo) contactItems.push({ label: "Nhắn Zalo cho thầy", href: CONTACT.zalo });
if (CONTACT.email) contactItems.push({ label: CONTACT.email, href: `mailto:${CONTACT.email}` });
if (CONTACT.area) contactItems.push({ label: CONTACT.area });

const hasContact = contactItems.length > 0;

const gridColumns = hasContact
  ? "sm:grid-cols-2 lg:grid-cols-[1.4fr_1fr_1fr_1fr_1.2fr]"
  : "md:grid-cols-[1.4fr_1fr_1fr_1fr]";

export default function Footer() {
  return (
    <footer id="contact" className="border-t border-line bg-[#04060A]">
      <div className="mx-auto max-w-6xl px-6 py-16 lg:px-8">
        <div className={`grid grid-cols-1 gap-12 ${gridColumns}`}>
          <div>
            <div className="flex items-center gap-2">
              <span className="flex h-8 w-8 items-center justify-center rounded-full bg-primary text-sm font-bold text-white font-display">
                T
              </span>
              <span className="font-display text-lg font-semibold text-ink">
                ThachLab
              </span>
            </div>
            <p className="mt-4 max-w-xs text-sm leading-relaxed text-muted">
              Nền tảng học Vật lý THPT giúp học sinh hiểu bản chất của thế
              giới xung quanh — không chỉ là những công thức trong sách giáo
              khoa.
            </p>
          </div>

          {columns.map((col) => (
            <div key={col.title}>
              <h4 className="font-display text-sm font-semibold text-ink">
                {col.title}
              </h4>
              <ul className="mt-4 space-y-3">
                {col.links.map((item) => (
                  <li key={item.label}>
                    <a
                      href={item.href}
                      {...(item.href.startsWith("http")
                        ? { target: "_blank", rel: "noopener noreferrer" }
                        : {})}
                      className="text-sm text-muted transition-colors hover:text-primary"
                    >
                      {item.label}
                    </a>
                  </li>
                ))}
              </ul>
            </div>
          ))}

          {hasContact && (
            <div>
              <h4 className="font-display text-sm font-semibold text-ink">Liên hệ</h4>
              <ul className="mt-4 space-y-3">
                {contactItems.map((item) => (
                  <li key={item.label}>
                    {item.href ? (
                      <a
                        href={item.href}
                        {...(item.href.startsWith("http")
                          ? { target: "_blank", rel: "noopener noreferrer" }
                          : {})}
                        className="text-sm text-muted transition-colors hover:text-primary"
                      >
                        {item.label}
                      </a>
                    ) : (
                      <span className="text-sm text-muted">{item.label}</span>
                    )}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>

        <div className="mt-16 flex flex-col items-center justify-between gap-4 border-t border-line pt-8 text-xs text-muted sm:flex-row">
          <p>&copy; {new Date().getFullYear()} ThachLab. Mọi quyền được bảo lưu.</p>
          <p>
            Thầy Thạch · Vật lý THPT – KHTN 9{CONTACT.area ? ` · ${CONTACT.area}` : ""}
          </p>
        </div>
      </div>
    </footer>
  );
}
