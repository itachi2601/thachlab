const links = [
  { label: "Khóa học", href: "#features" },
  { label: "Vật lý quanh ta", href: "#physics-everywhere" },
  { label: "Lộ trình học", href: "#learning-path" },
  { label: "Về ThachLab", href: "#about" },
  { label: "Blog", href: "#blog" },
];

export default function Navbar() {
  return (
    <header className="fixed top-0 inset-x-0 z-50 border-b border-white/10 bg-[#05070B]/90 backdrop-blur-md">
      <nav className="mx-auto flex max-w-6xl items-center justify-between px-6 py-4 lg:px-8">
        <a href="#" className="flex items-center gap-2">
          <span className="flex h-8 w-8 items-center justify-center rounded-lg bg-[#2563EB] text-sm font-bold text-white font-display">
            T
          </span>
          <span className="font-display text-lg font-semibold tracking-tight text-white">
            Thach<span className="text-[#3B82F6]">Lab</span>
          </span>
        </a>

        <ul className="hidden items-center gap-8 md:flex">
          {links.map((link) => (
            <li key={link.href}>
              <a
                href={link.href}
                className="text-sm font-medium text-slate-300 transition-colors hover:text-white"
              >
                {link.label}
              </a>
            </li>
          ))}
        </ul>

        <div className="flex items-center gap-3">
          <a
            href="#dang-nhap"
            className="hidden rounded-full px-4 py-2 text-sm font-medium text-slate-300 transition-colors hover:text-white sm:inline-block"
          >
            Đăng nhập
          </a>
          <a
            href="#hoc-thu"
            className="rounded-full bg-[#2563EB] px-5 py-2.5 text-sm font-semibold text-white shadow-sm shadow-blue-900/30 transition-transform hover:-translate-y-0.5 hover:bg-[#1D4ED8]"
          >
            Học thử miễn phí
          </a>
        </div>
      </nav>
    </header>
  );
}
