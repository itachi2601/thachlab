const links = [
  { label: "Khóa học", href: "#features" },
  { label: "Vật lý quanh ta", href: "#physics-everywhere" },
  { label: "Lộ trình học", href: "#learning-path" },
  { label: "Về ThachLab", href: "#about" },
];

export default function Navbar() {
  return (
    <header className="fixed top-0 inset-x-0 z-50 border-b border-line/60 bg-bg/80 backdrop-blur-md">
      <nav className="mx-auto flex max-w-6xl items-center justify-between px-6 py-4 lg:px-8">
        <a href="#" className="flex items-center gap-2">
          <span className="flex h-8 w-8 items-center justify-center rounded-full bg-primary text-sm font-bold text-white font-display">
            T
          </span>
          <span className="font-display text-lg font-semibold tracking-tight text-ink">
            Thach<span className="text-primary">Lab</span>
          </span>
        </a>

        <ul className="hidden items-center gap-8 md:flex">
          {links.map((link) => (
            <li key={link.href}>
              <a
                href={link.href}
                className="text-sm font-medium text-muted transition-colors hover:text-ink"
              >
                {link.label}
              </a>
            </li>
          ))}
        </ul>

        <div className="flex items-center gap-3">
          <a
            href="#hoc-thu"
            className="hidden rounded-full px-4 py-2 text-sm font-medium text-ink transition-colors hover:text-primary sm:inline-block"
          >
            Đăng nhập
          </a>
          <a
            href="#hoc-thu"
            className="rounded-full bg-primary px-5 py-2.5 text-sm font-semibold text-white shadow-sm shadow-primary/20 transition-transform hover:-translate-y-0.5 hover:bg-primary-dark"
          >
            Học thử miễn phí
          </a>
        </div>
      </nav>
    </header>
  );
}
