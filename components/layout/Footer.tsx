import { CONTACT } from "@/lib/contact";

const columns = [
  {
    title: "Lớp học",
    links: [
      { label: "KHTN 9", href: "/lop-hoc/khtn-9" },
      { label: "Vật lý 10", href: "/lop-hoc/lop-10" },
      { label: "Vật lý 11", href: "/lop-hoc/lop-11" },
      { label: "Vật lý 12", href: "/lop-hoc/lop-12" },
      { label: "Luyện tập", href: "/luyen-tap" },
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

/**
 * variant="app": trang trong app của học sinh đã đăng nhập (/tai-khoan, /lop-hoc/xep-hang, /lop-hoc/ket-qua, /thong-bao —
 * thầy chốt 7/10/2026). Footer tiếp thị (cột Lớp học, Về thầy Thạch, Blog, mạng xã hội) xếp dọc rất dài ở 375px và không
 * phục vụ việc học (N1), lại trùng thanh đáy MobileTabBar → chỉ còn một dòng: bản quyền · Zalo (D2 ≥44px); Báo lỗi đã có nút nổi.
 * variant="parent": dùng ở /phu-huynh (docs/QUY-TAC-THIET-KE-PHU-HUYNH.md). Bản mặc định nền #04060A cố định nên
 * trên trang sáng tiêu đề cột (màu ink = chữ tối) chìm hẳn vào nền đen, và chữ 12–14px dưới sàn 15px của phụ huynh
 * (P1, P2). Bản parent theo theme (bg-panel), chữ ≥15px, link cao ≥48px (P4). Trang khác không đổi.
 */
export default function Footer({ variant = "default" }: { variant?: "default" | "parent" | "app" }) {
  if (variant === "app") {
    const link = "inline-flex min-h-11 items-center text-[13px] text-muted transition-colors hover:text-primary";
    return (
      <footer className="border-t border-line bg-panel">
        {/* Canh trái + chừa lề phải ~9rem ở điện thoại để nút nổi "Báo lỗi / Góp ý" (bug-fab) không đè lên chữ;
            không lặp link Báo lỗi vì nút nổi đã có. */}
        <div className="mx-auto flex max-w-6xl flex-wrap items-center gap-x-5 px-6 py-3 pr-36 text-[13px] text-muted sm:pr-6">
          <span className="inline-flex min-h-11 items-center">&copy; {new Date().getFullYear()} ThachLab</span>
          {CONTACT.zalo && (
            <a href={CONTACT.zalo} target="_blank" rel="noopener noreferrer" className={link}>
              Nhắn Zalo cho thầy
            </a>
          )}
        </div>
      </footer>
    );
  }
  const parent = variant === "parent";
  const bg = parent ? "bg-panel" : "bg-[#04060A]";
  const headCls = parent ? "font-display text-base font-bold text-ink" : "font-display text-sm font-semibold text-ink";
  const listCls = "mt-2 space-y-0";
  const linkCls = parent
    ? "inline-flex min-h-12 items-center text-[15px] text-muted underline-offset-2 transition-colors hover:text-primary hover:underline"
    : "inline-flex min-h-11 items-center text-sm text-muted transition-colors hover:text-primary";
  const textCls = parent ? "text-[15px] text-muted" : "text-sm text-muted";
  return (
    <footer id="contact" className={`border-t border-line ${bg}`}>
      <div className="mx-auto max-w-6xl px-6 py-16 lg:px-8">
        <div className={`grid grid-cols-1 gap-12 ${gridColumns}`}>
          <div>
            <div className="flex items-center gap-2">
              {/* eslint-disable-next-line @next/next/no-img-element */}
              <img src="/brand/logo-mark.svg" alt="" width={32} height={32} className="h-8 w-8" />
              <span className="font-display text-lg font-semibold text-ink">
                ThachLab
              </span>
            </div>
            <p className={`mt-4 max-w-xs leading-relaxed ${textCls}`}>
              Nền tảng học Vật lý THPT giúp học sinh hiểu bản chất của thế
              giới xung quanh — không chỉ là những công thức trong sách giáo
              khoa.
            </p>
          </div>

          {columns.map((col) => (
            <div key={col.title}>
              <h4 className={headCls}>
                {col.title}
              </h4>
              <ul className={listCls}>
                {col.links.map((item) => (
                  <li key={item.label}>
                    <a
                      href={item.href}
                      {...(item.href.startsWith("http")
                        ? { target: "_blank", rel: "noopener noreferrer" }
                        : {})}
                      className={linkCls}
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
              <h4 className={headCls}>Liên hệ</h4>
              <ul className={listCls}>
                {contactItems.map((item) => (
                  <li key={item.label}>
                    {item.href ? (
                      <a
                        href={item.href}
                        {...(item.href.startsWith("http")
                          ? { target: "_blank", rel: "noopener noreferrer" }
                          : {})}
                        className={linkCls}
                      >
                        {item.label}
                      </a>
                    ) : (
                      <span className={`inline-flex ${parent ? "min-h-12" : "min-h-11"} items-center ${textCls}`}>{item.label}</span>
                    )}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>

        <div className={`mt-16 flex flex-col items-center justify-between gap-4 border-t border-line pt-8 text-muted sm:flex-row ${parent ? "text-[15px]" : "text-xs"}`}>
          <p>&copy; {new Date().getFullYear()} ThachLab. Mọi quyền được bảo lưu.</p>
          <p>
            Thầy Thạch · Vật lý THPT – KHTN 9{CONTACT.area ? ` · ${CONTACT.area}` : ""}
          </p>
        </div>
      </div>
    </footer>
  );
}
