const columns = [
  {
    title: "Khóa học",
    links: ["Vật lý 10", "Vật lý 11", "Vật lý 12", "Luyện đề THPT"],
  },
  {
    title: "ThachLab",
    links: ["Về chúng tôi", "Phương pháp giảng dạy", "Câu hỏi thường gặp"],
  },
  {
    title: "Kết nối",
    links: ["Fanpage", "YouTube", "Email hỗ trợ"],
  },
];

export default function Footer() {
  return (
    <footer className="border-t border-line bg-white">
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
                  <li key={item}>
                    <a
                      href="#"
                      className="text-sm text-muted transition-colors hover:text-primary"
                    >
                      {item}
                    </a>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>

        <div className="mt-16 flex flex-col items-center justify-between gap-4 border-t border-line pt-8 text-xs text-muted sm:flex-row">
          <p>&copy; {new Date().getFullYear()} ThachLab. Mọi quyền được bảo lưu.</p>
          <p className="font-mono">Học để hiểu, không học để nhớ.</p>
        </div>
      </div>
    </footer>
  );
}
