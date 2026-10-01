import Link from "next/link";

// Thanh vào nhanh dưới Navbar, chỉ ở trang chủ: học sinh quay lại hằng ngày vào thẳng lớp của
// mình (1 click thay vì qua /lop-hoc). Mobile cuộn ngang, mép phải mờ dần để biết còn mục.
// Navbar là fixed (cao 68px mobile / 76px từ sm) nên thanh này tự chừa khoảng trống phía trên.
const items = [
  { label: "KHTN 9", href: "/lop-hoc/khtn-9" },
  { label: "Vật lý 10", href: "/lop-hoc/lop-10" },
  { label: "Vật lý 11", href: "/lop-hoc/lop-11" },
  { label: "Vật lý 12", href: "/lop-hoc/lop-12" },
  { label: "CTTC · CNC", href: "/lop-hoc/cttc" },
  { label: "Xếp hạng", href: "/lop-hoc/xep-hang" },
  { label: "Phụ huynh", href: "/phu-huynh" },
];

export default function PublicSubNav() {
  return (
    <nav aria-label="Vào nhanh" className="border-b border-line bg-[#05070B] pt-[68px] sm:pt-[76px]">
      <div className="mx-auto max-w-6xl px-4 sm:px-6 lg:px-8">
        <ul className="flex gap-1 overflow-x-auto py-2 [scrollbar-width:none] [&::-webkit-scrollbar]:hidden [mask-image:linear-gradient(90deg,black_calc(100%-40px),transparent)] lg:[mask-image:none]">
          {items.map((item) => (
            <li key={item.href} className="shrink-0">
              <Link
                href={item.href}
                className="inline-flex min-h-9 items-center whitespace-nowrap rounded-full px-3.5 text-sm font-medium text-muted transition-colors hover:bg-white/[0.06] hover:text-ink"
              >
                {item.label}
              </Link>
            </li>
          ))}
        </ul>
      </div>
    </nav>
  );
}
