const columns = [
  {
    title: "Khóa học",
    links: [
      { label: "Vật lý 10", href: "#learning-path" },
      { label: "Vật lý 11", href: "#learning-path" },
      { label: "Vật lý 12", href: "#learning-path" },
      { label: "Luyện đề THPT", href: "#learning-path" },
    ],
  },
  {
    title: "ThachLab",
    links: [
      { label: "Về chúng tôi", href: "#about" },
      { label: "Phương pháp giảng dạy", href: "#features" },
      { label: "Câu hỏi thường gặp", href: "#" },
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

export default function Footer() {
  return (
    <footer id="contact" className="border-t border-line bg-[#04060A]">
      <div className="mx-auto max-w-6xl px-6 py-16 lg:px-8">
        <div className="grid grid-cols-1 gap-12 md:grid-cols-[1.4fr_1fr_1fr_1fr]">
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
        </div>

        <div className="mt-16 flex flex-col items-center justify-between gap-4 border-t border-line pt-8 text-xs text-muted sm:flex-row">
          <p>&copy; {new Date().getFullYear()} ThachLab. Mọi quyền được bảo lưu.</p>
          <p className="font-mono">Living between equation and motion.</p>
        </div>
      </div>
    </footer>
  );
}
